"""Provider-neutral runner for the question-bank pipeline (review / fix jobs), for the AI Orchestrator extension.

The Claude `Workflow` tool is one engine for this pipeline.  This script is a second engine that needs no Workflow tool:
it derives the next job for every chapter from the files on disk (testbank_status.py), runs it with the `claude` CLI or
the `codex` CLI, and when one provider reports a usage limit it falls over to the other.

    python3 pipeline_runner.py status                      # table of chapter / Master-slice states
    python3 pipeline_runner.py plan                        # the jobs it would run now (no model calls)
    python3 pipeline_runner.py selftest [--provider X]     # tiny job to prove each CLI works (reads, runs a command, writes a file)
    python3 pipeline_runner.py loop [--provider auto|claude|codex] [--jobs 4] [--chapters L1W2,L1W3,MASTER-L1] [--once]

RULES
  * Use ONE engine per chapter at a time.  Stop the Workflow runs (or pass --chapters that they are not working on)
    before using this runner on the same chapters.
  * Jobs never publish anything.  Publishing to staging is `python3 testbank_publish.py` (staging only).
  * A chapter is accepted only when a FRESH independent review has no blocking findings (see tasks/testbank_pipeline.md);
    the runner reviews with a clean worker session every time.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import testbank_status as st

PORTAL = Path(__file__).parent
ROOT = PORTAL.parent
BANK = PORTAL / "testbank"
STATE = BANK / "runner_state.json"
LOCKS = BANK / ".locks"
CODEX = os.environ.get("CODEX_BIN") or str(next(iter(sorted(Path.home().glob(".vscode/extensions/openai.chatgpt-*/bin/macos-aarch64/codex"))), "codex"))
CLAUDE = os.environ.get("CLAUDE_BIN") or "claude"
JOB_TIMEOUT = 45 * 60
LIMIT_RE = re.compile(r"session limit|weekly limit|usage limit|rate limit|hit your limit|quota|too many requests|429", re.I)
NET_RE = re.compile(r"ENOTFOUND|Can't reach the API|ECONNRESET|ETIMEDOUT|network is unreachable|Could not resolve", re.I)
MAX_ROUNDS = 30
ADJ_MIN_ROUNDS = 8        # from this many review rounds on, a chapter that keeps hovering at a few findings is adjudicated
ADJ_MAX_BLOCKING = 15
_lock = threading.Lock()


# ─── prompts (single source of truth: the Workflow scripts' templates) ─────────────────────────────

def _template(js_file, fn):
    js = (ROOT / "tasks" / js_file).read_text("utf-8")
    m = re.search(r"function " + fn + r"\([^)]*\) \{\n  return `(.*?)`\n\}", js, re.S)
    if not m:
        sys.exit(f"cannot find {fn} in {js_file}")
    return m.group(1)


def render_review(name, n):
    """Review prompt for a chapter (L1W5) or a Master slice (MASTER-L2)."""
    if name.startswith("MASTER-L"):
        tpl = _template("master_workflow.js", "reviewPrompt")
        vals = {"PORTAL": str(PORTAL), "ROOT": str(ROOT), "L": name[-1], "n": str(n)}
        for k, v in vals.items():
            tpl = tpl.replace("${" + k + "}", v)
        return tpl + "\n\nFinish by replying with the same findings list, the number of fully sound questions, and a one-line verdict."
    tpl = _template("testbank_workflow.js", "reviewPrompt")
    d = json.loads((BANK / "designs" / f"{name}.json").read_text("utf-8")) if (BANK / "designs" / f"{name}.json").exists() else \
        {"taughtBefore": "Only this chapter (the first chapter): ism / fi'l / harf and their recognition signs.",
         "forbidden": "Everything taught in later chapters.", "policy": "A one-letter prefix is joined to its word unless the stem says otherwise.", "caveats": []}
    vals = {"PORTAL": str(PORTAL), "ROOT": str(ROOT), "ch": name, "n": str(n), "d.taughtBefore": d["taughtBefore"],
            "d.forbidden": d["forbidden"], "d.policy": d["policy"], "d.caveats.join(' || ') || 'none'": " || ".join(d["caveats"]) or "none"}
    for k, v in vals.items():
        tpl = tpl.replace("${" + k + "}", v)
    return tpl + "\n\nFinish by replying with the same findings list (max 60 lines), the number of fully sound questions, and a one-line verdict."


def render_fix(name, review_file):
    master = name.startswith("MASTER-L")
    files = f"{PORTAL}/testbank/parts/MASTER/L{name[-1]}W*.json" if master else f"{PORTAL}/testbank/parts/{name}/*.json"
    design = "portal/testbank/designs/<chapter>.json" if master else f"portal/testbank/designs/{name}.json (the pilot L1W1 has none: see testbank/L1W1.json)"
    return f"""You are fixing independent-review findings in the Quran Arabic question bank. Project root: {ROOT} (code in portal/). No paid APIs.
Read first: {ROOT}/tasks/testbank_brief.md (authoring rules 1-20 incl. 'Hint = the rule'), {ROOT}/tasks/testbank_pipeline.md{', ' + str(ROOT) + '/tasks/master_blueprint.md' if master else ''}, and the docstring of {PORTAL}/testbank_tool.py (file format).
The review to fix: {review_file} (one finding per line: id | severity | problem | fix). Design / allowed knowledge: {design}.
Fix EVERY line, including minor ones. Edit ONLY the part files {files} (never testbank/<chapter>.json or MASTER.json; they are regenerated).
Where a question changes, rewrite ALL four 'why' texts in en and tr so they stay coherent; replacement questions are NEW questions on different words/ayahs/asks (keep the id) that follow every brief rule; no ayah used more than twice; correct-answer positions stay balanced; keep per-topic counts and difficulty split. If you disagree with a finding, list it in your final reply with the reason instead of ignoring it.
After editing run, from {PORTAL}: python3 testbank_tool.py part <each edited file>  (0 errors required), then python3 testbank_tool.py check {'MASTER' if master else name}  (the JSON it prints must contain \\"ok\\": true for a chapter).
Final reply: at most 10 lines: ids you changed and any disagreement."""


def render_adjudicate(name, review_file, n):
    master = name.startswith("MASTER-L")
    bank = f"{PORTAL}/testbank/MASTER.json (only the questions with ids M-L{name[-1]}W*)" if master else f"{PORTAL}/testbank/{name}.json"
    files = f"{PORTAL}/testbank/parts/MASTER/L{name[-1]}W*.json" if master else f"{PORTAL}/testbank/parts/{name}/*.json"
    out = f"{PORTAL}/testbank/reviews/{name}_adjudication{n}.txt"
    return f"""You are the ADJUDICATOR for the Quran Arabic question bank (project root {ROOT}, code in portal/). No paid APIs.
Several fresh reviewers keep finding a few different small issues in every round, so the loop does not settle. Your job is to separate REAL defects from NITPICKS, and fix the real ones.
Read first: {ROOT}/tasks/testbank_brief.md (rules 1-20 and 'Hint = the rule'), the 'Defining duplicate' and 'What a hint-leak is' sections of {ROOT}/tasks/testbank_pipeline.md{', ' + str(ROOT) + '/tasks/master_blueprint.md' if master else ''}, and the docstring of {PORTAL}/testbank_tool.py.
The latest independent review (round {n}): {review_file}. The bank it reviewed: {bank}. Qur'an text for checking ayahs: {ROOT}/Irab Kitaplari/_kelime/qurancom.json. Lectures: {PORTAL}/lectures.json; design/allowed knowledge: {PORTAL}/testbank/designs/<chapter>.json.
For EVERY finding in the review, open the actual question and decide independently, with evidence:
 - REAL: a student would be misled or a rule is truly broken: a wrong or genuinely ambiguous answer (a second defensible option), a false statement in any explanation, knowledge from a LATER chapter needed, a hint that names a question's word/answer (narrow definition), a Turkish sentence that is ungrammatical or changes the meaning, a true duplicate by the pipeline definition, an ayah/quote mismatch.
 - NITPICK: an arguable preference, harmless style or wording, an over-strict reading of a rule, a stem/option nuance no student would trip on, or a finding that is itself mistaken.
Be a careful skeptic in BOTH directions: do not rubber-stamp the reviewer and do not dismiss real errors. wrong-answer / explanation-error / out-of-scope findings are REAL unless you can show with evidence that the finding itself is mistaken.
Write {out} with one line per finding: <id> | REAL or NITPICK | evidence (one sentence), and as the LAST line exactly: TOTAL REAL: <k>, NITPICK: <m>
For every REAL finding fix it by editing ONLY the part files {files} (never testbank/<chapter>.json or MASTER.json; they are regenerated), following the same rules as a fix (all four 'why' texts en+tr for a changed question, replacement questions new, balanced answer positions, no ayah over twice), then run from {PORTAL}: python3 testbank_tool.py part <each edited file> (0 errors required) and python3 testbank_tool.py check {'MASTER' if master else name}.
If REAL = 0 do NOT edit any part file. Final reply: at most 6 lines with the counts."""


# ─── providers ─────────────────────────────────────────────────────────────────────────────────

def load_state():
    return json.loads(STATE.read_text("utf-8")) if STATE.exists() else {}


def save_state(s):
    with _lock:
        STATE.write_text(json.dumps(s, indent=1), "utf-8")


WEEKLY_CAP = 85          # percent of the weekly allowance at which a provider is no longer used
USAGE_TTL = 600          # seconds a usage reading is trusted


def _codex_weekly():
    """(used percent, reset epoch) of Codex's weekly window via `codex app-server` (account/rateLimits/read)."""
    import select
    p = subprocess.Popen([CODEX, "app-server"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    try:
        for o in ({"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "runner", "version": "1"}}},
                  {"method": "initialized"}, {"id": 2, "method": "account/rateLimits/read"}):
            p.stdin.write(json.dumps(o) + "\n"); p.stdin.flush()
        end = time.time() + 30
        while time.time() < end:
            if select.select([p.stdout], [], [], 1)[0]:
                line = p.stdout.readline()
                if not line:
                    break
                d = json.loads(line)
                if d.get("id") == 2:
                    rl = d["result"]["rateLimits"]
                    wins = [w for w in (rl.get("primary"), rl.get("secondary")) if w]
                    week = [w for w in wins if (w.get("windowDurationMins") or 0) >= 7 * 1440] or wins
                    if not week:
                        return None
                    w = max(week, key=lambda x: x["usedPercent"])
                    return w["usedPercent"], w.get("resetsAt") or 0
    except Exception:
        return None
    finally:
        p.kill()
    return None


def _claude_weekly():
    """(used percent, reset epoch) from the rate_limit_event objects Claude Code emits; None if no weekly signal.
    The CLI only reports a seven_day event (with utilization) once the weekly window is near its limit, so a missing
    signal means 'below the warning threshold'; a non-'allowed' seven_day status counts as exhausted."""
    env = {k: v for k, v in os.environ.items() if not (k == "CLAUDECODE" or k.startswith("CLAUDE_CODE_"))}
    try:
        r = subprocess.run([CLAUDE, "-p", "Reply OK", "--output-format", "stream-json", "--verbose"], capture_output=True,
                           text=True, timeout=180, env=env, cwd=ROOT)
    except Exception:
        return None
    best = None
    for line in r.stdout.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        info = d.get("rate_limit_info") if d.get("type") == "rate_limit_event" else None
        if not info or not str(info.get("rateLimitType", "")).startswith("seven_day"):
            continue
        u = info.get("utilization")
        pct = (u * 100 if u is not None and u <= 1 else u) if u is not None else (100 if info.get("status") not in ("allowed", "allowed_warning") else 0)
        if info.get("status") not in ("allowed", "allowed_warning"):
            pct = 100
        if best is None or pct > best[0]:
            best = (pct, info.get("resetsAt") or 0)
    return best or (0, 0)


_usage_lock = threading.Lock()


def weekly_usage(p, force=False):
    with _usage_lock:
        return _weekly_usage(p, force)


def _weekly_usage(p, force):
    """Cached weekly usage for provider p -> (percent, reset epoch) or None when unreadable."""
    s = load_state()
    c = s.get(f"{p}_usage")
    if c and not force and time.time() - c["at"] < USAGE_TTL:
        return c["pct"], c["reset"]
    got = _codex_weekly() if p == "codex" else _claude_weekly()
    man = s.get(f"{p}_manual")
    if man and time.time() - man["at"] < 6 * 3600 and (got is None or got[0] < man["pct"]):
        got = (man["pct"], man["reset"])      # owner-entered reading (CLI gives none until near the limit)
    if got is None:
        return (c["pct"], c["reset"]) if c else None
    s = load_state(); s[f"{p}_usage"] = {"pct": got[0], "reset": got[1], "at": time.time()}; save_state(s)
    return got


def weekly_blocked_until(p):
    """Epoch until which p must not be used because its weekly usage is at or above WEEKLY_CAP (0 = usable)."""
    u = weekly_usage(p)
    if u and u[0] >= WEEKLY_CAP:
        return u[1] or time.time() + 3600
    return 0


def provider_ready(p):
    s = load_state()
    if time.time() < s.get(f"{p}_until", 0):
        return False
    wb = weekly_blocked_until(p)
    if wb > time.time():
        if not s.get(f"{p}_cap_logged") == wb:
            s = load_state(); s[f"{p}_cap_logged"] = wb; save_state(s)
            print(f"  [{p}] weekly usage >= {WEEKLY_CAP}%: not used until {time.strftime('%a %d %b %H:%M', time.localtime(wb))}", flush=True)
        return False
    return True


def mark_limited(p, minutes=45):
    s = load_state(); s[f"{p}_until"] = time.time() + minutes * 60; save_state(s)
    print(f"  [{p}] usage limit reported: pausing it for {minutes} min", flush=True)


def run_provider(p, prompt):
    """Run one job with provider p. Returns (ok, kind, text) where kind in ok|limit|network|error|timeout."""
    out_file = BANK / f".last_{p}_{os.getpid()}_{threading.get_ident()}.txt"
    if p == "claude":
        cmd = [CLAUDE, "-p", "--permission-mode", "acceptEdits", "--allowedTools", "Bash Read Write Edit Glob Grep", "--output-format", "text"]
    else:
        cmd = [CODEX, "exec", "-s", "workspace-write", "-C", str(ROOT), "--skip-git-repo-check", "--ephemeral", "-o", str(out_file), "-"]
    try:
        # a worker started from inside another Claude Code session must not inherit its "nested session" guard
        env = {k: v for k, v in os.environ.items() if not (k == "CLAUDECODE" or k.startswith("CLAUDE_CODE_"))}
        r = subprocess.run(cmd, input=prompt, cwd=ROOT, capture_output=True, text=True, timeout=JOB_TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return False, "timeout", f"{p} job exceeded {JOB_TIMEOUT // 60} min"
    except FileNotFoundError:
        return False, "error", f"{p} CLI not found ({cmd[0]})"
    text = (out_file.read_text("utf-8") if out_file.exists() else "") or r.stdout
    out_file.unlink(missing_ok=True)
    blob = text + "\n" + r.stdout[-2000:] + "\n" + r.stderr[-2000:]
    if LIMIT_RE.search(blob) and r.returncode != 0 or (LIMIT_RE.search(text[:600]) and len(text) < 800):
        return False, "limit", blob[-400:]
    if NET_RE.search(blob) and r.returncode != 0:
        return False, "network", blob[-300:]
    if r.returncode != 0:
        return False, "error", blob[-600:]
    return True, "ok", text


def run_job(prompt, provider, label):
    order = ["claude", "codex"] if provider == "auto" else [provider]
    attempt = 0
    while attempt < 6:
        ready = [p for p in order if provider_ready(p)]
        if not ready:
            wait = min(max(load_state().get(f"{p}_until", 0), weekly_blocked_until(p)) for p in order) - time.time()
            print(f"  [{label}] all providers paused (limit or >= {WEEKLY_CAP}% weekly); waiting {max(60, int(min(wait, 1800)))}s of {int(wait)}s", flush=True)
            time.sleep(max(60, min(1800, wait)))
            continue            # waiting for a limit/weekly reset is not a failed attempt
        attempt += 1
        p = ready[0]
        print(f"  [{label}] running with {p}", flush=True)
        ok, kind, text = run_provider(p, prompt)
        if ok:
            return True, p, text
        if kind == "limit":
            mark_limited(p)
        elif kind == "network":
            print(f"  [{label}] network problem; retrying in 5 min", flush=True); time.sleep(300)
        else:
            print(f"  [{label}] {p} failed ({kind}): {text[-200:]}", flush=True)
            if len(order) == 1:
                return False, p, text
            order = order[1:] + order[:1]
    return False, order[0], "gave up after 6 attempts"


# ─── jobs ──────────────────────────────────────────────────────────────────────────────────────

def all_rows():
    mf = BANK / "accepted.json"
    manual = json.loads(mf.read_text("utf-8")) if mf.exists() else {}
    rows = [st.chapter_state(c, manual) for c in st.ALL] + [st.master_state(L) for L in (1, 2, 3)]
    return rows


def plan(only=None):
    jobs = []
    for r in all_rows():
        name = r["chapter"]
        if only and name not in only:
            continue
        if r["state"] == "accepted":
            continue
        if r["round"] >= MAX_ROUNDS:
            jobs.append((name, "exhausted", r)); continue
        kind = {"needs-review": "review", "needs-re-review": "review", "needs-fix": "fix", "authoring": "author"}[r["state"]]
        if kind == "fix" and r["round"] >= ADJ_MIN_ROUNDS and (r["blocking"] or 0) <= ADJ_MAX_BLOCKING:
            kind = "adjudicate"
        jobs.append((name, kind, r))
    return jobs


def locked(name):
    f = LOCKS / f"{name}.lock"
    return f.exists() and time.time() - f.stat().st_mtime < JOB_TIMEOUT + 300


def do_job(name, kind, r, provider):
    LOCKS.mkdir(exist_ok=True)
    (LOCKS / f"{name}.lock").write_text(str(os.getpid()))
    try:
        master = name.startswith("MASTER-L")
        tool = [sys.executable, "testbank_tool.py", "check", "MASTER" if master else name]
        if kind == "review":
            subprocess.run(tool, cwd=PORTAL, capture_output=True)                      # assemble the bank the reviewer will read
            n = st.max_review_number(name) + 1
            out = BANK / "reviews" / f"{name}_review{n}.txt"
            ok, p, text = run_job(render_review(name, n), provider, f"{name} review {n}")
            good = ok and st.review_valid(out)
            print(f"{name}: review {n} by {p}: {'written' if good else 'FAILED (missing/empty/malformed review file)'}", flush=True)
            return good
        if kind == "fix":
            rev = st.latest_review(name)
            ok, p, text = run_job(render_fix(name, rev[1]), provider, f"{name} fix {rev[0]}")
            chk = subprocess.run(tool, cwd=PORTAL, capture_output=True, text=True).stdout.strip().split("\n")[-1:]
            good = ok and ('"ok": true' in "".join(chk) or master)
            print(f"{name}: fix of review {rev[0]} by {p}: {'done' if good else 'FAILED'} {''.join(chk)[:160]}", flush=True)
            return good
        if kind == "adjudicate":
            rev = st.latest_review(name)
            n = rev[0]
            out = BANK / "reviews" / f"{name}_adjudication{n}.txt"
            out.unlink(missing_ok=True)
            ok, p, text = run_job(render_adjudicate(name, rev[1], n), provider, f"{name} adjudicate {n}")
            body = out.read_text("utf-8") if out.exists() else ""
            m = re.search(r"TOTAL REAL:\s*(\d+),\s*NITPICK:\s*(\d+)", body)
            if not (ok and m):
                print(f"{name}: adjudication {n} by {p}: FAILED (no TOTAL line)", flush=True)
                return False
            real, nit = int(m.group(1)), int(m.group(2))
            if real == 0:
                with _lock:
                    mf = BANK / "accepted.json"
                    acc = json.loads(mf.read_text("utf-8")) if mf.exists() else {}
                    acc[name] = {"note": f"adjudicated after review {n}: 0 real findings, {nit} nitpick(s) rejected (reviews/{name}_adjudication{n}.txt)",
                                 "after": time.time()}
                    mf.write_text(json.dumps(acc, indent=1, ensure_ascii=False), "utf-8")
                print(f"{name}: adjudication {n} by {p}: 0 REAL, {nit} NITPICK -> ACCEPTED (adjudicated)", flush=True)
            else:
                print(f"{name}: adjudication {n} by {p}: {real} REAL fixed, {nit} NITPICK; needs a fresh review", flush=True)
            return True
        print(f"{name}: '{kind}' jobs are not handled by this runner (use the Workflow engine)", flush=True)
        return False
    finally:
        (LOCKS / f"{name}.lock").unlink(missing_ok=True)


def cmd_status(_):
    sys.argv = ["testbank_status.py"]
    st.main()


def cmd_plan(a):
    only = set(a.chapters.split(",")) if a.chapters else None
    for name, kind, r in plan(only):
        print(f"{name:10} {kind:10} (state {r['state']}, rounds {r['round']}, blocking {r['blocking']}){'  LOCKED' if locked(name) else ''}")


def cmd_loop(a):
    only = set(a.chapters.split(",")) if a.chapters else None
    ex = ThreadPoolExecutor(max_workers=a.jobs)
    running = {}
    failures = {}
    while True:
        todo = [(n, k, r) for n, k, r in plan(only) if k in ("review", "fix", "adjudicate") and not locked(n) and n not in running and failures.get(n, 0) < 3]
        for n, k, r in todo[: max(0, a.jobs - len(running))]:
            print(f"-> {n}: {k}", flush=True)
            running[n] = ex.submit(do_job, n, k, r, a.provider)
        if not running:
            print("nothing left to run (everything accepted, exhausted, locked or failing)")
            break
        done = [n for n, f in running.items() if f.done()]
        for n in done:
            f = running.pop(n)
            try:
                ok = f.result()
            except Exception as e:                              # keep the loop alive
                print(f"{n}: job crashed: {e}", flush=True); ok = False
            failures[n] = 0 if ok else failures.get(n, 0) + 1
        if a.once and not running:
            break
        time.sleep(5)
    ex.shutdown()


def cmd_review(a):
    """Force a fresh review of NAME even if it is already accepted (cross-provider confirmation)."""
    for name in a.names.split(","):
        rows = {r["chapter"]: r for r in all_rows()}
        print(name, "->", "ok" if do_job(name, "review", rows[name], a.provider) else "FAILED", flush=True)


def main_provider(name):
    """Provider that did most of the recent review/adjudication work on NAME (from the runner logs); None if unknown."""
    tally = {}
    for lf in ("runner.log", "runner_codex.log"):
        f = ROOT / "tasks" / lf
        if f.exists():
            for line in f.read_text("utf-8", "ignore").splitlines():
                m = re.match(rf"{re.escape(name)}: (?:review|adjudication) \d+ by (claude|codex)", line)
                if m:
                    tally[m.group(1)] = tally.get(m.group(1), 0) + 1
    return max(tally, key=tally.get) if tally else None


def audit_one(name):
    """Fresh review of an ACCEPTED chapter by the OTHER provider. Findings withdraw a manual acceptance so the normal loop
    (fix -> fresh review -> adjudication) takes over; a clean review leaves it accepted."""
    mp = main_provider(name)
    mp = mp or "claude"          # no log entry = accepted by the earlier Claude Workflow engine
    auditor = "codex" if mp == "claude" else "claude"
    if weekly_blocked_until(auditor) > time.time():
        print(f"{name}: DEFERRED (auditor {auditor} is at >= {WEEKLY_CAP}% weekly)", flush=True)
        return None
    print(f"{name}: audit by {auditor} (accepted work was mainly {mp})", flush=True)
    rows = {r["chapter"]: r for r in all_rows()}
    if not do_job(name, "review", rows[name], auditor):
        return False
    rev = st.latest_review(name)
    blocking = st.blocking_count(rev[1])
    with _lock:
        af = BANK / "audit.json"
        au = json.loads(af.read_text("utf-8")) if af.exists() else {}
        au[name] = {"auditor": auditor, "review": rev[0], "blocking": blocking, "at": time.strftime("%F %H:%M")}
        af.write_text(json.dumps(au, indent=1), "utf-8")
        if blocking:
            mf = BANK / "accepted.json"
            acc = json.loads(mf.read_text("utf-8")) if mf.exists() else {}
            if acc.pop(name, None) is not None:
                mf.write_text(json.dumps(acc, indent=1, ensure_ascii=False), "utf-8")
    print(f"{name}: AUDIT by {auditor}: {'CLEAN' if not blocking else f'{blocking} blocking finding(s) -> back in the pipeline'}", flush=True)
    return True


def cmd_audit(a):
    names = a.names.split(",")
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        res = dict(zip(names, ex.map(audit_one, names)))
    print("audit summary:", {k: ("clean/findings recorded" if v else "deferred" if v is None else "failed") for k, v in res.items()}, flush=True)


def cmd_selftest(a):
    probe = BANK / ".runner_selftest.txt"
    prompt = (f"Self-test. Use your shell tool to run: python3 -c \"print(6*7)\" . Then write the result (just the number) into the file {probe} "
              "using your file-writing ability. Finally reply with the single word DONE.")
    for p in ([a.provider] if a.provider != "auto" else ["claude", "codex"]):
        probe.unlink(missing_ok=True)
        t = time.time()
        ok, kind, text = run_provider(p, prompt)
        wrote = probe.exists() and probe.read_text().strip()
        print(f"{p}: ok={ok} kind={kind} file={wrote!r} reply={text.strip()[:60]!r} ({time.time() - t:.0f}s)")
        probe.unlink(missing_ok=True)


def cmd_usage(a):
    if a.claude_pct is not None:
        reset = time.mktime(time.strptime(a.reset, "%Y-%m-%d %H:%M")) if a.reset else 0
        s = load_state(); s["claude_manual"] = {"pct": a.claude_pct, "reset": reset, "at": time.time()}
        s.pop("claude_usage", None); save_state(s)
    for p in ("claude", "codex"):
        u = weekly_usage(p, force=True)
        st = load_state().get(f"{p}_until", 0)
        guess = p == "claude" and u is not None and u[0] == 0 and not load_state().get("claude_manual")
        txt = "unreadable" if u is None else ("not reported by the CLI (assumed below the warning threshold; enter yours with --claude-pct)" if guess else f"{u[0]:.0f}% of weekly allowance") + (f", resets {time.strftime('%a %d %b %H:%M', time.localtime(u[1]))}" if u[1] else "")
        print(f"{p:7} {txt} | cap {WEEKLY_CAP}% -> {'PAUSED' if not provider_ready(p) else 'usable'}"
              + (f" | session-limit pause until {time.strftime('%H:%M', time.localtime(st))}" if st > time.time() else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    p = sub.add_parser("usage"); p.add_argument("--claude-pct", type=float, help="enter the weekly % from claude.ai usage page (valid 6 h)")
    p.add_argument("--reset", help='weekly reset as "YYYY-MM-DD HH:MM"'); p.set_defaults(fn=cmd_usage)
    p = sub.add_parser("plan"); p.add_argument("--chapters"); p.set_defaults(fn=cmd_plan)
    p = sub.add_parser("selftest"); p.add_argument("--provider", default="auto", choices=["auto", "claude", "codex"]); p.set_defaults(fn=cmd_selftest)
    p = sub.add_parser("review"); p.add_argument("names"); p.add_argument("--provider", default="auto", choices=["auto", "claude", "codex"]); p.set_defaults(fn=cmd_review)
    p = sub.add_parser("audit"); p.add_argument("names"); p.add_argument("--jobs", type=int, default=6); p.set_defaults(fn=cmd_audit)
    p = sub.add_parser("loop"); p.add_argument("--provider", default="auto", choices=["auto", "claude", "codex"])
    p.add_argument("--jobs", type=int, default=4); p.add_argument("--chapters"); p.add_argument("--once", action="store_true"); p.set_defaults(fn=cmd_loop)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

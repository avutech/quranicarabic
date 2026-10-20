"""Where is every chapter in the question-bank pipeline? Derived only from files on disk, so it survives crashes.

    python3 testbank_status.py            # table + summary
    python3 testbank_status.py --json     # machine readable
    python3 testbank_status.py --unaccepted   # space-separated chapter ids that still need work

A chapter is 'accepted' when its latest independent review (testbank/reviews/<ch>_review<N>.txt) lists no blocking
finding AND no part file was modified after that review (a rewrite needs a fresh review), or when it is listed in
testbank/accepted.json (manual acceptance, e.g. the L1W1 pilot).  'idle' = minutes since any pipeline file or
workflow journal changed; a long idle time while chapters are unaccepted means the workflows stopped.
"""
import glob, json, os, re, sys, time
from pathlib import Path

BANK = Path(__file__).parent / "testbank"
WF = Path.home() / ".claude" / "projects" / "-Users-ahmedugur-Documents-Claude-Projects-Quran-Arabic"
BLOCKING = {"wrong-answer", "ambiguous", "explanation-error", "out-of-scope", "hint-leak", "turkish", "duplicate"}
ALL = [f"L{L}W{W}" for L in (1, 2, 3) for W in range(1, 15)]


def latest_review(ch):
    best = None
    for f in BANK.glob(f"reviews/{ch}_review*.txt"):
        m = re.search(r"_review(\d+)\.txt$", f.name)
        if m and (best is None or int(m.group(1)) > best[0]):
            best = (int(m.group(1)), f)
    return best


def blocking_count(f):
    n = 0
    for line in f.read_text("utf-8").splitlines():
        parts = [p.strip().lower() for p in line.split("|")]
        if len(parts) >= 3 and parts[1] in BLOCKING:
            n += 1
    return n


def chapter_state(ch, manual):
    parts_dir = BANK / "parts" / ch
    files = sorted(parts_dir.glob("*.json")) if parts_dir.exists() else []
    design_f = BANK / "designs" / f"{ch}.json"
    expected = None
    if design_f.exists():
        d = json.loads(design_f.read_text("utf-8"))
        expected = sum(1 + (1 if t["target"] > 15 else 0) for t in d["topics"])
    rev = latest_review(ch)
    row = {"chapter": ch, "files": len(files), "expected": expected, "round": rev[0] if rev else 0, "blocking": None}
    if ch in manual:
        row.update(state="accepted", note=manual[ch])
        return row
    if expected is not None and len(files) < expected:
        row["state"] = "authoring"
    elif not rev:
        row["state"] = "needs-review"
    else:
        row["blocking"] = blocking_count(rev[1])
        newest_part = max((f.stat().st_mtime for f in files), default=0)
        if newest_part > rev[1].stat().st_mtime:
            row["state"] = "needs-re-review"
        elif row["blocking"] == 0:
            row["state"] = "accepted"
        else:
            row["state"] = "needs-fix"
    return row


def idle_minutes():
    newest = 0
    for pat in (str(BANK / "parts" / "*" / "*.json"), str(BANK / "reviews" / "*.txt"),
                # NOT agent-*.jsonl transcripts: a throttled agent keeps writing retry requests for hours with no progress
                str(WF / "*" / "subagents" / "workflows" / "*" / "journal.jsonl")):
        for f in glob.glob(pat):
            newest = max(newest, os.path.getmtime(f))
    return round((time.time() - newest) / 60, 1) if newest else None


def main():
    mf = BANK / "accepted.json"
    manual = json.loads(mf.read_text("utf-8")) if mf.exists() else {}
    rows = [chapter_state(ch, manual) for ch in ALL]
    summary = {}
    for r in rows:
        summary[r["state"]] = summary.get(r["state"], 0) + 1
    if "--unaccepted" in sys.argv:
        print(" ".join(r["chapter"] for r in rows if r["state"] != "accepted"))
        return
    out = {"idleMinutes": idle_minutes(), "summary": summary, "chapters": rows}
    if "--json" in sys.argv:
        print(json.dumps(out, ensure_ascii=False))
        return
    print(f"idle for {out['idleMinutes']} min | {summary}")
    for r in rows:
        print(f"{r['chapter']:6} {r['state']:16} files {r['files']}/{r['expected']}  review rounds {r['round']}  blocking {r['blocking']}")


if __name__ == "__main__":
    main()

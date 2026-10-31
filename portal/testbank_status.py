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


def review_valid(f):
    """A review counts only if it is non-empty and either lists findings or states a sound-count / verdict."""
    try:
        t = f.read_text("utf-8")
    except OSError:
        return False
    if not t.strip():
        return False
    if any(len(l.split("|")) >= 3 and l.split("|")[1].strip().lower() in BLOCKING | {"minor"} for l in t.splitlines()):
        return True
    low = t.lower()
    return "sound" in low or "verdict" in low


def latest_review(ch, valid_only=True):
    """(round, file) of the newest review; with valid_only an empty/malformed newest file is skipped."""
    best = None
    for f in BANK.glob(f"reviews/{ch}_review*.txt"):
        m = re.search(r"_review(\d+)\.txt$", f.name)
        if m and (best is None or int(m.group(1)) > best[0]) and (not valid_only or review_valid(f)):
            best = (int(m.group(1)), f)
    return best


def max_review_number(ch):
    nums = [int(m.group(1)) for f in BANK.glob(f"reviews/{ch}_review*.txt") if (m := re.search(r"_review(\d+)\.txt$", f.name))]
    return max(nums, default=0)


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
        m = manual[ch]
        newest_part = max((f.stat().st_mtime for f in files), default=0)
        if isinstance(m, dict) and newest_part > m.get("after", 0) + 1:
            row["note"] = "adjudicated acceptance withdrawn: part files changed afterwards"
        else:
            row.update(state="accepted", note=m["note"] if isinstance(m, dict) else m)
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


def master_state(level):
    """Master Exam slice for one level: authoring -> needs-review -> needs-fix / needs-re-review -> accepted."""
    name = f"MASTER-L{level}"
    pd = BANK / "parts" / "MASTER"
    files = [pd / f"L{level}W{w}.json" for w in range(1, 15)]
    have = [f for f in files if f.exists()]
    rev = latest_review(name)
    row = {"chapter": name, "files": len(have), "expected": 14, "round": rev[0] if rev else 0, "blocking": None}
    mf = BANK / "accepted.json"
    man = json.loads(mf.read_text("utf-8")).get(name) if mf.exists() else None
    if man is not None and len(have) == 14:
        newest = max(f.stat().st_mtime for f in have)
        if not (isinstance(man, dict) and newest > man.get("after", 0) + 1):
            row.update(state="accepted", note=man["note"] if isinstance(man, dict) else man)
            return row
    if len(have) < 14:
        row["state"] = "authoring"
    elif not rev:
        row["state"] = "needs-review"
    else:
        row["blocking"] = blocking_count(rev[1])
        if max(f.stat().st_mtime for f in have) > rev[1].stat().st_mtime:
            row["state"] = "needs-re-review"
        else:
            row["state"] = "accepted" if row["blocking"] == 0 else "needs-fix"
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
    master = [master_state(L) for L in (1, 2, 3)]
    out = {"idleMinutes": idle_minutes(), "summary": summary, "chapters": rows, "master": master,
           "masterAccepted": all(m["state"] == "accepted" for m in master)}
    if "--json" in sys.argv:
        print(json.dumps(out, ensure_ascii=False))
        return
    print(f"idle for {out['idleMinutes']} min | {summary}")
    for m in master:
        print(f"{m['chapter']:10} {m['state']:16} files {m['files']}/{m['expected']}  review rounds {m['round']}  blocking {m['blocking']}")
    for r in rows:
        print(f"{r['chapter']:6} {r['state']:16} files {r['files']}/{r['expected']}  review rounds {r['round']}  blocking {r['blocking']}")


if __name__ == "__main__":
    main()

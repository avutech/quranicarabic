"""Publish newly ACCEPTED question banks to the staging branch (never production).

    python3 testbank_publish.py            # commit + push new/changed accepted banks to origin/staging
    python3 testbank_publish.py --dry-run  # only list what would be published

Safety rules (owner: "just to staging"):
  * only chapters testbank_status.py reports as 'accepted' (a fresh independent review with no blocking findings,
    no part file edited after it) are published; unreviewed banks stay local;
  * each bank must pass `testbank_tool.py validate` and the backend tests must pass;
  * it must be run on the local branch `staging-tests` (tracking origin/staging) and it only ever pushes
    `staging-tests:staging`.  Production is never touched.
"""
import subprocess
import sys
from pathlib import Path

import testbank_status as st

PORTAL = Path(__file__).parent
ROOT = PORTAL.parent
PY = str(PORTAL / "venv" / "bin" / "python")
BRANCH = "staging-tests"


def run(cmd, cwd=ROOT, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"FAILED: {' '.join(cmd)}\n{r.stdout}{r.stderr}")
    return r


def main():
    dry = "--dry-run" in sys.argv
    manual = st.json.loads((st.BANK / "accepted.json").read_text("utf-8")) if (st.BANK / "accepted.json").exists() else {}
    accepted = [r["chapter"] for r in (st.chapter_state(c, manual) for c in st.ALL) if r["state"] == "accepted"]
    todo = []
    for ch in accepted:
        rel = f"portal/testbank/{ch}.json"
        if not (ROOT / rel).exists():
            continue
        if run(["git", "status", "--porcelain", rel]).stdout.strip():      # new or modified vs the staging commit
            todo.append((ch, rel))
    print("accepted:", len(accepted), "| to publish:", [c for c, _ in todo])
    if not todo or dry:
        return
    if run(["git", "branch", "--show-current"]).stdout.strip() != BRANCH:
        sys.exit(f"refusing: not on branch {BRANCH}")
    for ch, _ in todo:
        r = run([PY, "testbank_tool.py", "validate", ch], cwd=PORTAL, check=False)
        if r.returncode:
            sys.exit(f"{ch} failed validation, not publishing\n{r.stdout}")
    t = run([PY, "-m", "unittest", "test_tests_api"], cwd=PORTAL, check=False)
    if t.returncode:
        sys.exit(f"backend tests failed, not publishing\n{t.stderr[-800:]}")
    run(["git", "add"] + [rel for _, rel in todo])
    names = ", ".join(c for c, _ in todo)
    run(["git", "commit", "-q", "-m",
         f"Question banks: add accepted chapters {names}\n\nEach passed an independent review with no blocking findings.\n\n"
         "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"])
    run(["git", "push", "origin", f"{BRANCH}:staging"])
    print("published to staging:", names)


if __name__ == "__main__":
    main()

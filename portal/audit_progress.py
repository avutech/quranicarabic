"""Progress of the ayah-to-ayah audit. usage: venv/bin/python audit_progress.py [packages.json]"""
import json
import sys
from collections import Counter
from pathlib import Path

LIB = Path(__file__).parent.parent / "irab_library"
RES = LIB / "audit" / "results"
done = [json.loads(p.read_text("utf-8")) for p in sorted(RES.glob("*.done.json"))] if RES.exists() else []
rows = []
for p in sorted(RES.glob("*.jsonl")) if RES.exists() else []:
    rows += [json.loads(x) for x in p.read_text("utf-8").splitlines() if x.strip()]
total = None
if len(sys.argv) > 1:
    total = len(json.loads(Path(sys.argv[1]).read_text("utf-8")))
surahs = sorted({d["surah"] for d in done})
print(f"chunks finished: {len(done)}" + (f" of {total}" if total else "") + f" | surahs touched: {len(surahs)} | verdicts recorded: {len(rows)}")
print("verdicts:", dict(Counter(r["verdict"] for r in rows)))
bad = [r for r in rows if r["verdict"] in ("SOURCE_MISPLACED", "SOURCE_DEFECT", "TRANSLATION_UNFIXED", "TEACHER")]
print(f"open items needing a human: {len(bad)}")

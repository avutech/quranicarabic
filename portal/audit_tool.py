"""Helper for the ayah-to-ayah audit agents. See irab_library/audit/RULES.md.

  venv/bin/python audit_tool.py findings <surah> <from> <to> [high,medium,low]   candidate findings + ayahs without an entry
  venv/bin/python audit_tool.py sample   <surah> <from> <to> [n=6]                spread sample of entries per book for the semantic check
  venv/bin/python audit_tool.py show     <surah> <key>                            Quran text, meals, Arabic entry, Turkish and English side by side
  venv/bin/python audit_tool.py verdict  <surah> <chunk> <key> <check> <VERDICT> "<note>"
  venv/bin/python audit_tool.py done     <surah> <chunk> "<summary>"
"""
import fcntl
import json
import sys
import time
from pathlib import Path

LIB = Path(__file__).parent.parent / "irab_library"
AUD = LIB / "audit"
RES = AUD / "results"
VERDICTS = {"OK", "SOURCE_MISPLACED", "SOURCE_DEFECT", "TRANSLATION_FIXED", "TRANSLATION_UNFIXED", "GAP", "TEACHER"}
TR_MEAL, EN_MEAL = "77", "20"          # Diyanet; Saheeh International


def load(s):
    return json.loads((AUD / f"s{int(s):03d}.json").read_text("utf-8"))


def entries(s):
    return {f"{e['b']}:{e['s']}-{e['e']}": e for e in json.loads((LIB / f"s{int(s):03d}.json").read_text("utf-8"))["entries"]}


def reading(lang, book, s, key):
    p = LIB / f"{lang}_parts" / book / f"s{int(s):03d}.json"
    return (json.loads(p.read_text("utf-8")) if p.exists() else {}).get(key)


def cmd_findings(s, a, z, sev="high,medium,low"):
    d, a, z = load(s), int(a), int(z)
    want = set(sev.split(","))
    fs = [f for f in d["findings"] if a <= f["from"] <= z and f["sev"] in want]
    print(f"surah {s} ayahs {a}-{z}: {len(fs)} findings ({sev}); surah has {d['ayahs']} ayahs")
    for f in fs:
        print(json.dumps(f, ensure_ascii=False))
    for b, miss in d["gaps"].items():
        m = [x for x in miss if a <= x <= z]
        if m:
            print(f"GAP {b}: no entry for ayahs {m[0]}-{m[-1]} ({len(m)} ayahs)")


def cmd_sample(s, a, z, n=6):
    n, a, z = int(n), int(a), int(z)
    by = {}
    for k, e in entries(s).items():
        if a <= int(e["s"]) <= z:
            by.setdefault(e["b"], []).append(k)
    for b, ks in by.items():
        ks.sort(key=lambda k: int(k.split(":")[1].split("-")[0]))
        pick = ks if len(ks) <= max(n, 8) else [ks[round(i * (len(ks) - 1) / (n - 1))] for i in range(n)]
        print(b, " ".join(k.split(":")[1] for k in pick))


def cmd_show(s, key):
    e = entries(s)[key]
    w = json.loads((LIB / "w" / f"s{int(s):03d}.json").read_text("utf-8"))
    for a in range(int(e["s"]), int(e["e"]) + 1):
        v = w[str(a)]
        print(f"--- ayah {s}:{a}\nQuran: {' '.join(x['ar'] for x in v['w'])}\nDiyanet: {v['m'].get(TR_MEAL)}\nEnglish: {v['m'].get(EN_MEAL)}")
    print(f"=== ARABIC ({key})\n{e['t']}")
    for lang in ("tr", "en"):
        r = reading(lang, e["b"], s, key)
        print(f"=== {lang.upper()}\n{r['t'] if r else '(none)'}")


def cmd_verdict(s, chunk, key, check, verdict, note=""):
    if verdict not in VERDICTS:
        sys.exit(f"verdict must be one of {sorted(VERDICTS)}")
    RES.mkdir(parents=True, exist_ok=True)
    line = json.dumps({"surah": int(s), "chunk": chunk, "key": key, "check": check, "verdict": verdict, "note": note,
                       "at": time.strftime("%Y-%m-%d %H:%M")}, ensure_ascii=False)
    with open(RES / f"s{int(s):03d}_{chunk}.jsonl", "a", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(line + "\n")
    print("recorded")


def cmd_done(s, chunk, summary):
    RES.mkdir(parents=True, exist_ok=True)
    p = RES / f"s{int(s):03d}_{chunk}.jsonl"
    rows = [json.loads(x) for x in p.read_text("utf-8").splitlines()] if p.exists() else []
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    (RES / f"s{int(s):03d}_{chunk}.done.json").write_text(json.dumps(
        {"surah": int(s), "chunk": chunk, "verdicts": counts, "summary": summary, "at": time.strftime("%Y-%m-%d %H:%M")},
        ensure_ascii=False, indent=1), "utf-8")
    print("done", counts)


if __name__ == "__main__":
    cmds = {"findings": cmd_findings, "sample": cmd_sample, "show": cmd_show, "verdict": cmd_verdict, "done": cmd_done}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]](*sys.argv[2:])

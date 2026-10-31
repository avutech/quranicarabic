"""Deterministic ayah-to-ayah match audit for the i'rab library (Arabic source / Turkish / English).

For every book entry (b, surah, ayah range s-e) it checks:
  S  structure     the range is valid for the surah; per book/surah the entries do not overlap; gaps are reported
  Q  source->ayah  Quranic quotations ﴿…﴾ / {…} inside the Arabic entry are found in the entry's own ayah range
                   (OK), in a nearby ayah of the same surah (NEAR: possible misplacement), elsewhere in the
                   Quran (XREF: normally a cross-reference), or nowhere (UNFOUND: garbled/not Quranic text)
  P  provenance    the Turkish/English reading points at exactly this entry (surah, range, sha1)
  T  retention     Quranic quotations of the source survive in the reading in Arabic script
  X  tr vs en      Turkish and English readings keep the same quotations and have a sane length ratio

Output: irab_library/audit/sNNN.json (findings per surah) and audit/summary.json.
Findings are only *candidates*: the per-surah agents decide (see audit/RULES.md).

usage: venv/bin/python audit_ayah_match.py [surah ...]
"""
import hashlib
import json
import re
import sys
from pathlib import Path

LIB = Path(__file__).parent.parent / "irab_library"
OUT = LIB / "audit"
HARAKAT = re.compile(r"[ً-ٰٟۖ-ۭـ]")
QUOTE = re.compile(r"[﴿{]([^﴾}]{1,400})[﴾}]")
MIN_Q = 8        # normalized letters; shorter quotations ("قال") occur everywhere and prove nothing
NEAR = 5         # ayahs either side counted as "nearby"


def norm(s):
    s = HARAKAT.sub("", s)
    for a, b in (("ٱ", "ا"), ("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ى", "ي"), ("ة", "ه"), ("ؤ", "و"), ("ئ", "ي")):
        s = s.replace(a, b)
    s = re.sub(r"[^ء-غف-ي ]", " ", s)    # Arabic letters only
    s = s.replace("ء", "").replace("ا", "")   # skeleton: hamza/alef spelling differs between the Quran text and the books
    return re.sub(r"\s+", " ", s).strip()


def quotes(text):
    out = []
    for q in QUOTE.findall(text):
        n = norm(q)
        if len(n.replace(" ", "")) >= MIN_Q:
            out.append(n)
    return out


def load_quran():
    quran = {}
    for s in range(1, 115):
        w = json.loads((LIB / "w" / f"s{s:03d}.json").read_text("utf-8"))
        quran[s] = {int(a): norm(" ".join(x["ar"] for x in v["w"])) for a, v in w.items()}
    return quran


def main(only):
    quran = load_quran()
    whole = "|".join(t for s in quran.values() for t in s.values())
    OUT.mkdir(exist_ok=True)
    summary = {}
    for s in only or range(1, 115):
        ayahs = quran[s]
        n_ay = max(ayahs)
        src = json.loads((LIB / f"s{s:03d}.json").read_text("utf-8"))["entries"]
        tr = en = {}
        books = sorted({e["b"] for e in src})
        readings = {}
        for lang in ("tr", "en"):
            readings[lang] = {}
            for b in books:
                p = LIB / f"{lang}_parts" / b / f"s{s:03d}.json"
                if p.exists():
                    readings[lang].update(json.loads(p.read_text("utf-8")))
        findings, per_book = [], {}
        cover = {}
        for e in src:
            b, a0, a1 = e["b"], int(e["s"]), int(e["e"])
            key = f"{b}:{e['s']}-{e['e']}"
            ent = {"key": key, "book": b, "surah": s, "from": a0, "to": a1}
            st = per_book.setdefault(b, {"entries": 0, "S": 0, "Q_near": 0, "Q_xref": 0, "Q_unfound": 0, "P": 0, "T": 0, "X": 0})
            st["entries"] += 1
            # S: structure
            if not (1 <= a0 <= a1 <= n_ay):
                findings.append({**ent, "check": "S", "sev": "high", "msg": f"range outside surah (1-{n_ay})"}); st["S"] += 1
                continue
            for a in range(a0, a1 + 1):
                if a in cover.setdefault(b, {}):
                    findings.append({**ent, "check": "S", "sev": "medium", "msg": f"ayah {a} also covered by {cover[b][a]}"}); st["S"] += 1
                cover[b][a] = key
            # Q: source -> ayah
            rng = " ".join(ayahs[a] for a in range(a0, a1 + 1))
            near = " ".join(ayahs[a] for a in range(max(1, a0 - NEAR), min(n_ay, a1 + NEAR) + 1))
            qs = quotes(e["t"])
            if qs:
                inr = [q for q in qs if q in rng]
                rest = [q for q in qs if q not in rng]
                nr = [q for q in rest if q in near]
                xr = [q for q in rest if q not in near and q in whole]
                uf = [q for q in rest if q not in whole]
                if len(inr) * 2 < len(qs):                 # fewer than half the quotations belong to this range
                    if len(nr) >= max(1, len(xr), len(uf)):
                        findings.append({**ent, "check": "Q", "sev": "high", "kind": "NEAR", "quotes": len(qs), "in_range": len(inr),
                                         "msg": "quotations belong to a nearby ayah, not this range: possible misplacement", "examples": nr[:2]}); st["Q_near"] += 1
                    elif len(xr) >= len(uf):
                        findings.append({**ent, "check": "Q", "sev": "low", "kind": "XREF", "quotes": len(qs), "in_range": len(inr),
                                         "msg": "quotations come from elsewhere in the Quran (cross-reference?)", "examples": xr[:2]}); st["Q_xref"] += 1
                    else:
                        findings.append({**ent, "check": "Q", "sev": "low", "kind": "UNFOUND", "quotes": len(qs), "in_range": len(inr),
                                         "msg": "quotations not found in the Quran text (garbled source or non-Quranic words)", "examples": uf[:2]}); st["Q_unfound"] += 1
            # P / T / X: readings
            r = {lg: readings[lg].get(key) for lg in ("tr", "en")}
            body = {}
            for lg, rd in r.items():
                if not rd:
                    findings.append({**ent, "check": "P", "sev": "high", "lang": lg, "msg": "no reading"}); st["P"] += 1
                    continue
                sr = rd.get("src", {})
                bad = []
                if str(sr.get("sure")) != str(s): bad.append(f"surah {sr.get('sure')}")
                if (str(sr.get("ayet_bas")), str(sr.get("ayet_son"))) != (str(e["s"]), str(e["e"])): bad.append(f"range {sr.get('ayet_bas')}-{sr.get('ayet_son')}")
                if sr.get("book") != b: bad.append(f"book {sr.get('book')}")
                if sr.get("sha1") != hashlib.sha1(e["t"].encode("utf-8")).hexdigest(): bad.append("sha1 differs: source changed")
                if bad:
                    findings.append({**ent, "check": "P", "sev": "high", "lang": lg, "msg": "provenance mismatch: " + "; ".join(bad)}); st["P"] += 1
                body[lg] = norm(rd["t"])
                if qs:
                    kept = sum(1 for q in qs if q in body[lg])
                    if kept < 0.8 * len(qs) and len(qs) >= 2:
                        findings.append({**ent, "check": "T", "sev": "medium", "lang": lg, "quotes": len(qs), "kept": kept,
                                         "msg": "reading keeps fewer than 80% of the source's Quranic quotations"}); st["T"] += 1
            if "tr" in body and "en" in body:
                lt, le = len(r["tr"]["t"]), len(r["en"]["t"])
                ratio = lt / max(1, le)
                kt = sum(1 for q in qs if q in body["tr"]); ke = sum(1 for q in qs if q in body["en"])
                if (len(e["t"]) > 150 and not 0.55 <= ratio <= 1.9) or (qs and abs(kt - ke) > max(2, 0.25 * len(qs))):
                    findings.append({**ent, "check": "X", "sev": "medium", "msg": f"Turkish and English differ: length ratio tr/en {ratio:.2f}, quotations kept tr {kt} / en {ke} of {len(qs)}"}); st["X"] += 1
        gaps = {}
        for b in books:
            miss = [a for a in range(1, n_ay + 1) if a not in cover.get(b, {})]
            if miss:
                gaps[b] = miss
        (OUT / f"s{s:03d}.json").write_text(json.dumps(
            {"surah": s, "ayahs": n_ay, "entries": len(src), "per_book": per_book, "gaps": gaps, "findings": findings},
            ensure_ascii=False, indent=1), "utf-8")
        summary[s] = {"entries": len(src), "findings": len(findings), "high": sum(f["sev"] == "high" for f in findings),
                      "medium": sum(f["sev"] == "medium" for f in findings), "low": sum(f["sev"] == "low" for f in findings),
                      "gap_books": len(gaps)}
    if not only:
        (OUT / "summary.json").write_text(json.dumps(summary, indent=1), "utf-8")
    tot = {k: sum(v[k] for v in summary.values()) for k in ("entries", "findings", "high", "medium", "low")}
    print(tot)


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]])

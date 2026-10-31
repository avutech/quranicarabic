"""Guardrails for translated i'rab readings (Turkish and English).

Used in two places:
  - tr_tool.py put: check_entry() runs before every save; ERRORS block the save,
    WARNINGS are printed so the translating agent can fix them.
  - audit:  venv/bin/python guardrails.py audit [--lang tr|en] [--book ID]
    scans every saved reading and writes irab_library/guardrails_report.json.

Rules come from irab_library/glossary_tr.md and glossary_en.md.
"""

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

LIB = Path(__file__).parent.parent / "irab_library"

HARAKAT = re.compile(r"[ً-ٰٟۖ-ۭـ]")      # vowel marks, small signs, tatweel
QURAN_QUOTE = re.compile(r"﴿([^﴾]{1,200})﴾")
TR_LETTERS = re.compile(r"[ğşıİĞŞ]")
TR_ONLY_WORD = re.compile(r"\b(?:ve|bir|için|olarak|olan|ile|değil|şöyle|dir|dır)\b")
EN_WORD = re.compile(r"\b(?:the|and|of|is|which|that|with)\b", re.I)
BANNED = {
    "tr": {r"müteall[ıi]kd[ıi]r\b": "use «mütealliktir»", r"müteallık": "use «müteallik»",
           r"\bmastar": "use «masdar»"},
    "en": {},
}


def strip_ar(s):
    return HARAKAT.sub("", s).replace("ٱ", "ا").replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").strip()


def arabic_len(s):
    return len(HARAKAT.sub("", s))


def check_entry(lang, src, text):
    """Return (errors, warnings) for one translated entry."""
    errors, warnings = [], []
    body = text.strip()
    if not body:
        return ["empty translation"], []
    # 1. completeness: translation far shorter than the (unvowelled) Arabic → likely summarised/truncated
    ratio = len(body) / max(1, arabic_len(src))
    if ratio < 0.45 and arabic_len(src) > 120:
        errors.append(f"too short ({ratio:.2f} × the Arabic): translate the WHOLE entry, no summarising")
    elif ratio < 0.8 and arabic_len(src) > 120:
        warnings.append(f"short ({ratio:.2f} × the Arabic): check nothing is left out")
    # 2. Quranic quotations must survive in Arabic script
    src_q = Counter(strip_ar(q) for q in QURAN_QUOTE.findall(src))
    if src_q:
        tr_plain = strip_ar(body)
        missing = [q for q in src_q if q and q not in tr_plain]
        if len(missing) > max(1, len(src_q) // 2):
            errors.append(f"{len(missing)} of {len(src_q)} Quranic quotations ﴿…﴾ are missing — keep them in Arabic script: {missing[:3]}")
        elif missing:
            warnings.append(f"Quranic quotation(s) not found verbatim: {missing[:3]}")
    # 3. footnotes [[…]] must be carried over
    fn_src = src.count("[[")
    fn_tr = len(re.findall(r"\[(?:Dipnot|Note):", body))
    if fn_src and fn_tr < fn_src:
        warnings.append(f"source has {fn_src} footnote(s) [[…]] but only {fn_tr} «[{'Dipnot' if lang == 'tr' else 'Note'}: …]»")
    # 4. language leakage
    latin = re.sub(r"[؀-ۿﭐ-﷿ﹰ-﻿]+", " ", body)
    if lang == "en":
        if len(TR_LETTERS.findall(latin)) >= 4 or len(TR_ONLY_WORD.findall(latin)) >= 4:
            errors.append("Turkish text detected in an English reading — translate into English")
    else:
        words = max(1, len(latin.split()))
        if len(EN_WORD.findall(latin)) / words > 0.08 and not TR_LETTERS.search(latin):
            errors.append("English text detected in a Turkish reading — translate into Turkish")
    # 5. glossary spellings
    for pat, fix in BANNED[lang].items():
        if re.search(pat, body):
            errors.append(f"glossary: {fix}")
    return errors, warnings


def audit(lang=None, book=None):
    report = {"errors": [], "warnings": 0, "checked": 0, "provenance_bad": []}
    for lg in ([lang] if lang else ["tr", "en"]):
        for f in sorted((LIB / f"{lg}_parts").glob(f"{book or '*'}/s*.json")):
            s = int(f.stem[1:])
            src = {f"{e['b']}:{e['s']}-{e['e']}": e["t"]
                   for e in json.loads((LIB / f.name).read_text("utf-8"))["entries"]}
            for key, r in json.loads(f.read_text("utf-8")).items():
                report["checked"] += 1
                if key not in src or r.get("src", {}).get("sha1") != hashlib.sha1(src[key].encode("utf-8")).hexdigest():
                    report["provenance_bad"].append(f"{lg} s{s} {key}")
                    continue
                errs, warns = check_entry(lg, src[key], r["t"])
                report["warnings"] += len(warns)
                for e in errs:
                    report["errors"].append(f"{lg} s{s} {key}: {e}")
    (LIB / "guardrails_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), "utf-8")
    return report


if __name__ == "__main__":
    if sys.argv[1:2] != ["audit"]:
        sys.exit(__doc__)
    args = dict(zip(sys.argv[2::2], sys.argv[3::2]))
    r = audit(args.get("--lang"), args.get("--book"))
    print(f"checked {r['checked']} readings: {len(r['errors'])} errors, {r['warnings']} warnings, "
          f"{len(r['provenance_bad'])} provenance problems")
    for e in r["errors"][:20]:
        print("  ERROR", e)
    sys.exit(1 if r["errors"] or r["provenance_bad"] else 0)

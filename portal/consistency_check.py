"""Consistency checks on the word-role tags, with no human in the loop.

Compares the tags against things we already trust: the corpus morphology of each word, the books against each
other, and the pairs that must go together. Everything it flags is a *suspect*, not a verdict — the output
(irab_library/roles/QUALITY.md, QUALITY_suspects.json) is the worklist for the scholar sample.
    python3 consistency_check.py
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import build_word_roles as B

LIB = B.LIB
morph, check_morphology = B.morph, B.check_morphology
INNA = {B.skeleton(w) for w in ("إنّ", "أنّ", "كأنّ", "لكنّ", "لعلّ", "ليت")}      # accusative particles that need a khabar


def main():
    suspects, counts, examples = [], Counter(), defaultdict(list)
    total_tags = Counter()
    disagree, disagree_ex = Counter(), []
    cov = Counter()
    form_roles = defaultdict(Counter)                       # word form -> role counts
    form_total = Counter()
    dense = []

    for s in range(1, 115):
        words = json.loads((LIB / "w" / f"s{s:03d}.json").read_text("utf-8"))
        res, _, merged = B.build_surah(s)
        for a, byword in res.items():
            ws = words[a]["w"]
            n_roles_ayah = sum(len(ts) for ts in byword.values())
            if len(ws) >= 4 and n_roles_ayah / len(ws) > 0.9:
                dense.append((f"{s}:{a}", n_roles_ayah, len(ws)))
            for i, ts in byword.items():
                m = morph(ws[int(i)])
                if len({t["r"] for t in ts}) >= 3:
                    suspects.append({"ref": f"{s}:{a}#{i}", "rule": "word carries 3+ different roles", "role": "*"})
                    if len(examples["3+ roles on one word"]) < 6:
                        examples["3+ roles on one word"].append(f"{s}:{a} {ws[int(i)]['ar']} ({'+'.join(t['r'] for t in ts)})")
                    counts["3+ roles on one word"] += 1
                for t in ts:
                    total_tags[t["r"]] += 1
                    bad = check_morphology(t["r"], t["scope"], m)
                    if bad:
                        counts[bad] += 1
                        suspects.append({"ref": f"{s}:{a}#{i}", "rule": bad, "role": t["r"], "books": len(t["src"])})
                        if len(examples[bad]) < 4:
                            examples[bad].append(f"{s}:{a} {ws[int(i)]['ar']} ({'+'.join(x['b'][:3] for x in t['src'])})")
                    form_roles[B.skeleton(ws[int(i)]["ar"])][t["r"]] += 1
        for a, ws in words.items():
            for i, w in enumerate(ws["w"]):
                form_total[B.skeleton(w["ar"])] += 1
                p = w["pa"]
                shown = {t["r"] for t in res.get(a, {}).get(str(i), [])}
                if "واو الحال" in p:                         # corpus: a wāw of ḥāl must have a hal tag on its word
                    cov["wāw al-ḥāl words (corpus)"] += 1
                    cov["…of which tagged hal"] += "hal" in shown
        # the books against each other (all tags, not only the shown ones)
        for a, byword in merged.items():
            per_role = defaultdict(lambda: defaultdict(set))
            for i, r in byword.items():
                for role, t in r.items():
                    if not t["alt"]:
                        for src in t["src"]:
                            per_role[role][src["b"]].add(i)
            for role, books in per_role.items():
                bl = list(books.items())
                for x in range(len(bl)):
                    for y in range(x + 1, len(bl)):
                        if bl[x][0] == B.QAC or bl[y][0] == B.QAC:
                            continue
                        disagree[(role, "both name it")] += 1
                        if not bl[x][1] & bl[y][1]:
                            disagree[(role, "…on different words")] += 1
                            if len(disagree_ex) < 40:
                                disagree_ex.append(f"{s}:{a} {role} {bl[x][0][:3]}={sorted(bl[x][1])} vs {bl[y][0][:3]}={sorted(bl[y][1])}")
    # inna / kāna must have a khabar
    inna_ayahs = inna_with = 0
    for s in range(1, 115):
        words = json.loads((LIB / "w" / f"s{s:03d}.json").read_text("utf-8"))
        roles = json.loads((LIB / "roles" / f"s{s:03d}.json").read_text("utf-8"))
        for a, ws in words.items():
            if any("حرف نصب" in w["pa"] and "مصدري" not in w["pa"] and B.skeleton(w["ar"]).lstrip("وف") in INNA for w in ws["w"]):
                inna_ayahs += 1
                inna_with += any(t["r"] == "haber" for ts in roles.get(a, {}).values() for t in ts)

    # same word form, wildly different tagging rate
    common = [(f, n) for f, n in form_total.most_common(400) if n >= 40 and f]
    split = []
    for f, n in common:
        r = form_roles[f]
        for role, c in r.items():
            if 0.25 <= c / n <= 0.75 and c >= 30:
                split.append((f, n, role, c))

    lines = ["# Word-role consistency report", "", "Generated by `portal/consistency_check.py`. Everything here is a *suspect*, not a verdict.", ""]
    lines += ["## Published tags", ", ".join(f"{r}: {n}" for r, n in total_tags.most_common()), ""]
    lines += ["## 1. Tag vs the word's own grammar (corpus morphology)"]
    for k, n in counts.most_common():
        lines.append(f"- **{k}**: {n} — e.g. " + "; ".join(examples.get(k, [])))
    lines += ["", "## 2. Books against each other (non-alternative tags, same ayah, same role)"]
    for role in B.ROLES:
        both, diff = disagree[(role, "both name it")], disagree[(role, "…on different words")]
        lines.append(f"- {role}: {both} book pairs name it in the same ayah; {diff} of them put it on **different words** ({diff / both:.0%})" if both else f"- {role}: —")
    lines += ["", "Examples:", *[f"- {e}" for e in disagree_ex[:15]], ""]
    lines += ["## 3. Coverage against independent evidence"]
    lines.append(f"- corpus 'wāw al-ḥāl' words: {cov['wāw al-ḥāl words (corpus)']}, tagged hal: {cov['…of which tagged hal']} ({cov['…of which tagged hal'] / max(1, cov['wāw al-ḥāl words (corpus)']):.0%})")
    lines.append(f"- ayahs containing an inna-type particle: {inna_ayahs}, of which have a haber tag: {inna_with} ({inna_with / max(1, inna_ayahs):.0%})")
    lines += ["", "## 4. Same word form, tagged in only part of its occurrences (25–75%)",
              "A form such as `هو` is not tagged every time: books name the role in some ayahs only. Large splits show where coverage is uneven.", ""]
    for f, n, role, c in sorted(split, key=lambda x: -x[1])[:25]:
        lines.append(f"- `{f}` ({n} occurrences): {role} on {c} ({c / n:.0%})")
    lines += ["", f"## 5. Ayahs with almost every word tagged (>90%): {len(dense)}", ", ".join(f"{r} ({n}/{w})" for r, n, w in dense[:20]), ""]
    (LIB / "roles" / "QUALITY.md").write_text("\n".join(lines), "utf-8")
    (LIB / "roles" / "QUALITY_suspects.json").write_text(json.dumps(suspects, ensure_ascii=False), "utf-8")
    print("\n".join(lines))
    print(f"\nsuspects: {len(suspects)} of {sum(total_tags.values())} tags")


if __name__ == "__main__":
    main()

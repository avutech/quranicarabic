"""Compare every sentence_structure rule with the book-sourced tags (the oracle). Prints, per rule:
   hit      a book names the same role on the same word
   near     … on a neighbouring word (an anchor convention)
   other    a book names a *different* role on this word (e.g. the book says mübteda where we say ism-i inne)
   miss     the books name this role in the ayah, but not here
   silent   no book names this role in the ayah — nothing to compare with
    python3 validate_structure.py [examples-per-rule]
"""
import json
import sys
from collections import Counter, defaultdict

import build_word_roles as B
import sentence_structure as SS

B.USE_DERIVED = False                               # compare the rules with the books alone

N_EX = int(sys.argv[1]) if len(sys.argv) > 1 else 3
res = defaultdict(Counter)
ex = defaultdict(lambda: defaultdict(list))
for s in range(1, 115):
    words = json.loads((B.LIB / "w" / f"s{s:03d}.json").read_text("utf-8"))
    _, _, merged = B.build_surah(s)
    for a, v in words.items():
        a = int(a)
        ws = v["w"]
        book = merged.get(a, {})
        for i, role, scope, rule, gov in SS.derive(ws):
            same_role_words = {j for j, r in book.items() if role in r and not r[role]["alt"]}
            other_here = {r for r in book.get(i, {}) if r != role and r in ("mubteda", "haber") and not book[i][r]["alt"]}
            if i in same_role_words:
                k = "hit"
            elif role in ("ismInna", "ismKana"):
                k = "other" if "mubteda" in other_here else "silent"
            elif {i - 1, i + 1} & same_role_words:
                k = "near"
            elif other_here:
                k = "other"
            elif same_role_words:
                k = "miss"
            else:
                k = "silent"
            res[rule][k] += 1
            if len(ex[rule][k]) < N_EX:
                ex[rule][k].append(f"{s}:{a} #{i + 1} {ws[i]['ar']}")
print(f"{'rule':26} {'total':>6} {'hit':>6} {'near':>6} {'other':>6} {'miss':>6} {'silent':>7}   agree = hit+near / (hit+near+other+miss)")
for rule in sorted(res):
    c = res[rule]; t = sum(c.values()); judged = c['hit'] + c['near'] + c['other'] + c['miss']
    print(f"{rule:26} {t:6} {c['hit']:6} {c['near']:6} {c['other']:6} {c['miss']:6} {c['silent']:7}   {((c['hit'] + c['near']) / judged if judged else float('nan')):.0%} of {judged}")
for rule in sorted(ex):
    for k in ("other", "miss"):
        if ex[rule][k]:
            print(f"  {rule} {k}: " + "; ".join(ex[rule][k]))

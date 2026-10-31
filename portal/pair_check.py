"""QA for the word-role tags: pairs that must go together.
  mübteda → haber   (the khabar may be an omitted word or sit in the next ayah)
  şart    → cevap   (the answer may be omitted or sit in a later ayah)
  cevap   → şart    (the condition may sit in the previous ayah)
and contradictions: one word that is both mübteda and haber (or şart and cevap) at word level.
    python3 pair_check.py        # prints counts, writes irab_library/roles/PAIRING.md
"""
import glob, json, re
from collections import Counter, defaultdict
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "irab_library"
WINDOW = 3                                           # ayahs: a sentence rarely runs further
PAIRS = (("mubteda", "haber", +1), ("sart", "cevap", +1), ("cevap", "sart", -1))


def load():
    roles = {}                                       # (surah, ayah) -> {role: count}
    conflicts = []
    for f in sorted(glob.glob(str(LIB / "roles" / "s*.json"))):
        s = int(Path(f).stem[1:])
        for a, words in json.loads(Path(f).read_text("utf-8")).items():
            c = Counter()
            for i, ts in words.items():
                for t in ts:
                    c[t["r"]] += 1
                word_roles = {t["r"] for t in ts if t["scope"] == "word"}
                for x, y in (("mubteda", "haber"), ("sart", "cevap")):
                    if x in word_roles and y in word_roles:
                        conflicts.append((s, int(a), int(i), x, y))
            roles[(s, int(a))] = c
    return roles, conflicts


def unpaired(roles):
    out = defaultdict(list)
    for (s, a), c in roles.items():
        for have, need, direction in PAIRS:
            if not c[have]:
                continue
            near = [roles.get((s, a + d * direction), Counter())[need] for d in range(0, WINDOW + 1)]
            if not any(near):
                out[f"{have}_without_{need}"].append((s, a))
    return out


if __name__ == "__main__":
    roles, conflicts = load()
    un = unpaired(roles)
    total = Counter(r for c in roles.values() for r in c)
    lines = ["# Word-role pairing check", "",
             f"Ayahs with tags: {len(roles)}. Window for the partner: this ayah and the next {WINDOW} (previous {WINDOW} for cevap→şart).", ""]
    for have, need, _ in PAIRS:
        key = f"{have}_without_{need}"
        n_have = sum(1 for c in roles.values() if c[have])
        lines.append(f"- **{have} → {need}**: {len(un[key])} of {n_have} ayahs have no {need} nearby")
    lines += ["", f"- **Contradictions** (same word is both roles at word level): {len(conflicts)}", ""]
    for key, lst in un.items():
        lines += [f"## {key} ({len(lst)})", ", ".join(f"{s}:{a}" for s, a in lst[:300]), ""]
    (LIB / "roles" / "PAIRING.md").write_text("\n".join(lines), "utf-8")
    print("\n".join(lines[:9]))

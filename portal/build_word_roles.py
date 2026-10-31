"""Grammar-role tags (mübteda / haber / hâl / şart / cevâb-ı şart) for the word-by-word grid.

Rule-based, no AI: reads the classical i'rab books already in irab_library/, finds the ﴿word﴾ heads
of each entry, aligns them to the ayah's words, and tags a word when the book's own line names the
role. Primary source: al-I'rāb al-Muyassar (muyesser-irab); cross-check: Da'ās (daas-irab).
Every tag keeps its book, entry key and the quoted line (provenance rule).

    python3 build_word_roles.py            # all surahs -> irab_library/roles/sNNN.json
    python3 build_word_roles.py 2:146      # print the tags of one ayah
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "irab_library"
PRIMARY, CHECK = "muyesser-irab", "daas-irab"
BOOKS = (PRIMARY, CHECK)

# ── Arabic skeletons ─────────────────────────────────────────────────────────
_MARKS = re.compile("[ً-ٰٟۖ-ۭـ࣓-ࣿ]")


def skeleton(s):
    """Letters only: no vowels, no alef, no hamza, so ءَاتَيْنَـٰهُمُ == آتيناهم."""
    s = _MARKS.sub("", s)
    s = s.translate(str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ة": "ه"}))
    return re.sub("[اءؤئ\\s\u200b-\u200f]", "", s)


def coarse(sk):
    """Fallback key that ignores و / ي, for hamza-carrier spelling differences (يَؤُدُهُ vs يَـُٔودُهُ)."""
    return re.sub("[ويى]", "", sk)


def tokens(s):
    return re.findall("[ء-يٱ]+", _MARKS.sub("", s))


# ── role vocabulary (compared in skeleton form: alef/hamza are dropped) ─────────
ROLES = ("mubteda", "haber", "hal", "sart", "cevap")
_sk = lambda *ws: {skeleton(w) for w in ws}
MUB = _sk("مبتدأ")
KHA = _sk("خبر", "خبرا")
KHA_POSS = _sk("خبره", "خبرها", "خبرهما", "خبرهم")    # "X خبرها": X is the predicate; "وخبره جملة …" is not
OMITTED = _sk("محذوف", "المحذوف", "لمحذوف")
HAL = _sk("حال", "حالا", "حالية")
ALHAL, ON_IN = skeleton("الحال"), _sk("على", "في")
SART = _sk("شرط", "شرطية", "شرطي", "الشرط")
COND_ADJ = _sk("شرطية", "شرطي")
COND_HEAD = _sk("أداة", "اسم", "حرف", "ظرف", "فعل", "جملة", "وفعل", "للشرط")
COND_BOTH = _sk("وجوابه", "والجواب", "وجوابها", "وجوابها")
JAWAB, JAWAB_OF = _sk("جواب", "جوابا"), _sk("لو", "لولا", "إذا", "لما", "شرط", "الشرط")
CLAUSE = _sk("جملة", "الجملة", "جمل")
PROCLITIC_NAMES = _sk("الواو", "الفاء", "اللام")


def _bare(w, vocab, prefixes="وف"):
    """The word itself, or the word after a one-letter prefix (default: conjunction و / ف), when in vocab."""
    return w in vocab or (len(w) > 2 and w[0] in prefixes and w[1:] in vocab)


def role_tokens(toks):
    """[(index, role)] for the role words in one clause (tokens already skeleton-normalised)."""
    out = []
    for i, w in enumerate(toks):
        prev = toks[i - 1] if i else ""
        nxt = toks[i + 1] if i + 1 < len(toks) else ""
        if _bare(w, MUB) and prev not in KHA:                       # مبتدأ, never لمبتدأ / المبتدأ
            out.append((i, "mubteda"))
        elif _bare(w, KHA) or (i > 0 and _bare(w, KHA_POSS)):
            out.append((i, "haber"))
        elif _bare(w, HAL) or (_bare(w, {ALHAL}) and prev in ON_IN):
            out.append((i, "hal"))
        elif _bare(w, JAWAB, "وفلب") and nxt in JAWAB_OF:         # جواب الشرط / جواب لو / جواب إذا …
            if toks[i + 2:i + 3] != [] and toks[i + 2] in OMITTED:
                continue                                              # an omitted answer has no word to mark
            out.append((i, "cevap"))
        elif _bare(w, SART, "وفلب"):
            # "إن شرطية", "اسم شرط", "فعل الشرط", "جملة الشرط" — not "جواب الشرط", "جملتا الشرط والجواب"
            named = w in COND_ADJ or prev in COND_HEAD
            if named and nxt not in COND_BOTH:
                out.append((i, "sart"))
    return out


def norm_tokens(text):
    return [skeleton(t) for t in tokens(text)]


# ── entry parsing ────────────────────────────────────────────────────────────
HEAD = re.compile(r"﴿([^﴾]{1,120})﴾")


def split_muyassar(text):
    """Muyassar: one line per head, `﴿head﴾: body`; a line not starting with ﴿ continues the previous."""
    lines = []
    for ln in text.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        m = re.match(r"^﴿([^﴾]{1,120})﴾\s*:?\s*(.*)$", ln)
        if m:
            lines.append([m.group(1), m.group(2)])
        elif lines:
            lines[-1][1] += " " + ln
    return [(h, b) for h, b in lines]


def split_inline(text, W=None, align_fn=None):
    """Da'ās: heads run inline. A ﴿…﴾ starts a new head after a full stop / new line, or — when the ayah's
    words are known — when it names the next unprocessed word(s) of the ayah (not a back-reference)."""
    heads, p = [], 0
    for m in HEAD.finditer(text):
        before = text[:m.start()].rstrip()
        ok = not before or before[-1] in ".\n"
        if W is not None:
            idx = align_fn(m.group(1), W, p)
            near = idx is not None and p <= idx[0] <= p + 3
            ok = ok or (near and not re.search("(?:لـ|بـ|على|من|إلى|جملة|والجملة|عن)\\s*$", before))
            if ok and idx is not None and idx[0] >= p:
                p = idx[-1] + 1
        if ok:
            heads.append(m)
    out = []
    for k, m in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else len(text)
        out.append((m.group(1), text[m.end():end].strip()))
    return out


# ── alignment: ﴿head﴾ → word indexes of the ayah ─────────────────────────────
def align(head, W, p):
    """Find the head's words in the ayah; prefer the first match at/after the pointer p."""
    ht = norm_tokens(head)
    if not ht or len(ht) > len(W):
        return None
    for key in (lambda x: x, coarse):
        k = [key(x) for x in ht]
        hits = [i for i in range(len(W) - len(ht) + 1) if [key(x) for x in W[i:i + len(ht)]] == k]
        if hits:
            start = next((i for i in hits if i >= p), hits[0])
            return list(range(start, start + len(ht)))
    return None


def clause_items(clause):
    """Skeleton tokens of a clause plus, per token, the ﴿quote﴾ that most recently preceded it."""
    toks, quote_before, cur, starts_with_quote = [], [], None, clause.lstrip().startswith("﴿")
    for part in re.split(r"(﴿[^﴾]*﴾)", clause):
        if part.startswith("﴿"):
            cur = part[1:-1]
        else:
            for t in tokens(part):
                toks.append(skeleton(t)); quote_before.append(cur)
    return toks, quote_before, starts_with_quote


NOT_A_WORD = _sk("اسم", "فعل", "حرف", "الجار", "جار", "الجملة", "جملة", "جملتا")      # never the subject of a role
OTHER_SUBJECT = _sk("المصدر", "المؤول", "مصدر", "الجار", "جار", "الجملة", "جملة")    # "والمصدر المؤول … مبتدأ": not the head


# Function words the books use in their descriptions ("في جواب لو"): never resolved to an ayah word by uniqueness
FUNCTION_WORDS = _sk("في", "من", "على", "إلى", "إن", "أن", "لا", "ما", "هو", "هي", "كان", "قد", "ثم", "أو", "بين", "عن", "لو", "إذا", "الذي", "التي")


def resolve(tok, W, idx):
    """Word index a book's token names: a word of the head first, else a word that is unique in the ayah."""
    for cand in (tok, tok[1:] if tok[:1] in "وف" else None):
        if not cand:
            continue
        hit = [i for i in idx if W[i] == cand]
        if hit:
            return hit[0]
        allhits = [i for i, x in enumerate(W) if x == cand]
        if len(allhits) == 1 and cand not in FUNCTION_WORDS:
            return allhits[0]
    return None


def tag_line(head, body, idx, W):
    """Roles named in one line, bound to word indexes. -> [(word, role, scope, alt, conf)]
    A tag is "high" only when the book names its subject: the head itself, a word before the role in the
    same clause ("وعليم خبرها"), or "جملة X". A bare "والجملة … خبر" says nothing about where it starts → "low"."""
    body = HEAD.sub(lambda m: "﴿" + re.sub("[،.؛:]", " ", m.group(1)) + "﴾", body)   # keep quotes whole
    found = []
    for a, seg in enumerate(re.split(r"\sأو\s", " " + body)):          # later alternatives are flagged
        for clause in re.split(r"[،.؛:]", seg):
            toks, qb, starts_q = clause_items(clause)
            roles = role_tokens(toks)
            if not roles:
                continue
            ri = roles[0][0]
            ck = [k for k, t in enumerate(toks) if _bare(t, CLAUSE)]
            word, conf, scope = idx[0], "low", "word"
            if ck:                                                     # a sentence-level role
                scope = "clause"
                m = re.search(r"جمل[ةتا]*\s*﴿([^﴾]+)﴾", clause)         # only "جملة ﴿X﴾" names its sentence
                quote = m.group(1) if m else None
                q_idx = align(quote, W, 0) if quote else None
                named = resolve(toks[ck[0] + 1], W, idx) if ck[0] + 1 < len(toks) and ck[0] + 1 != ri else None
                if q_idx:
                    word, conf = q_idx[0], "high"                      # "وجملة ﴿X﴾ خبر…"
                elif named is not None:
                    word, conf = named, "high"                         # "وجملة أنشأناهن خبر إن"
                # else: bare "والجملة …" — where the sentence starts is not said → stays low
            else:
                before = toks[:ri]
                first_is_pp = "جر" in before and any(_bare(t, OMITTED) for t in toks)    # "جار ومجرور متعلقان بمحذوف خبر"
                order = before if first_is_pp else list(reversed(before))               # the PP starts at its first word
                subj = next((r for r in (resolve(t, W, idx) for t in order if t not in NOT_A_WORD) if r is not None), None)
                if subj is not None:
                    word, conf = subj, "high"
                elif len(idx) == 1 and not any(t in OTHER_SUBJECT for t in before):
                    word, conf = idx[0], "high"                        # "﴿الله﴾: مبتدأ"
                elif toks[0] in PROCLITIC_NAMES:
                    word, conf = idx[0], "high"                        # "الواو حالية"
            for _, role in roles:
                found.append((word, role, scope, a > 0, conf))
    return found


def ayah_tags(ayah_words, entries):
    """entries: [(book, key, entry text)] -> {word: {role: tag}} merged over books."""
    W = [skeleton(re.sub("[ۖ-ۭ]", "", w["ar"])) for w in ayah_words]
    merged = defaultdict(dict)
    stats = {"lines": 0, "aligned": 0}
    for book, key, text in entries:
        p = 0
        lines = split_muyassar(text) if book == PRIMARY else split_inline(text, W, align)
        for head, body in lines:
            stats["lines"] += 1
            idx = align(head, W, p)
            if idx is None:
                continue
            stats["aligned"] += 1
            p = idx[-1] + 1
            for word, role, scope, alt, conf in tag_line(head, body, idx, W):
                src = {"b": book, "k": key, "q": f"﴿{head}﴾ {body}"[:400]}
                t = merged[word].setdefault(role, {"r": role, "scope": scope, "alt": alt, "conf": conf, "src": []})
                if not any(s["b"] == book for s in t["src"]):
                    t["src"].append(src)
                t["alt"] = t["alt"] and alt
                t["conf"] = "high" if "high" in (t["conf"], conf) else "low"
                if scope == "word":
                    t["scope"] = "word"
    return merged, stats


def load_entries(surah, ayah):
    out = []
    data = json.loads((LIB / f"s{surah:03d}.json").read_text("utf-8"))
    for e in data["entries"]:
        if e["b"] in BOOKS and e["s"] == e["e"] == ayah:
            out.append((e["b"], f"{e['b']}:{e['s']}-{e['e']}", e["t"]))
    return out


def displayable(t):
    """Shown to students: the book names the subject word (high) and it is its primary reading, or both books agree.
    Everything else stays out until a scholar has looked at it."""
    return not t["alt"] and (t["conf"] == "high" or len(t["src"]) > 1)


def build_surah(surah, only=None):
    words = json.loads((LIB / "w" / f"s{surah:03d}.json").read_text("utf-8"))
    data = json.loads((LIB / f"s{surah:03d}.json").read_text("utf-8"))
    by_ayah = defaultdict(list)
    for e in data["entries"]:
        if e["b"] in BOOKS and e["s"] == e["e"]:
            by_ayah[e["s"]].append((e["b"], f"{e['b']}:{e['s']}-{e['e']}", e["t"]))
    res, tot = {}, {"lines": 0, "aligned": 0}
    for a, ents in by_ayah.items():
        if only and a != only:
            continue
        w = words.get(str(a), {}).get("w")
        if not w:
            continue
        merged, st = ayah_tags(w, ents)
        tot["lines"] += st["lines"]; tot["aligned"] += st["aligned"]
        shown = {i: [t for t in r.values() if displayable(t)] for i, r in merged.items()}
        shown = {str(i): sorted(ts, key=lambda t: ROLES.index(t["r"])) for i, ts in sorted(shown.items()) if ts}
        if shown:
            res[str(a)] = shown
    return res, tot


if __name__ == "__main__":
    if len(sys.argv) > 1:
        s, a = map(int, sys.argv[1].split(":"))
        res, tot = build_surah(s, a)
        w = json.loads((LIB / "w" / f"s{s:03d}.json").read_text("utf-8"))[str(a)]["w"]
        print(tot)
        for i, tags in res.get(str(a), {}).items():
            print(i, w[int(i)]["ar"], [(t["r"], t["scope"], "alt" if t["alt"] else "", t["conf"], len(t["src"])) for t in tags])
        sys.exit()
    (LIB / "roles").mkdir(exist_ok=True)
    grand = {"lines": 0, "aligned": 0}
    counts = defaultdict(int)
    for s in range(1, 115):
        res, tot = build_surah(s)
        grand["lines"] += tot["lines"]; grand["aligned"] += tot["aligned"]
        for a in res.values():
            for tags in a.values():
                for t in tags:
                    counts[(t["r"], "confirmed" if len(t["src"]) > 1 else "single")] += 1
        (LIB / "roles" / f"s{s:03d}.json").write_text(json.dumps(res, ensure_ascii=False, separators=(",", ":")), "utf-8")
    print(grand, f"aligned {grand['aligned'] / max(1, grand['lines']):.1%}")
    for k in sorted(counts):
        print(k, counts[k])

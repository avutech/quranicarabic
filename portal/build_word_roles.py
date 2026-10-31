"""Grammar-role tags (mübteda / haber / hâl / şart / cevâb-ı şart) for the word-by-word grid.

Rule-based, no AI: reads the classical i'rab books already in irab_library/, finds the ﴿word﴾ heads
of each entry, aligns them to the ayah's words, and tags a word when the book's own line names the
role. Sources: al-I'rāb al-Muyassar (muyesser-irab), Da'ās (daas-irab) and Ṣāfī's al-Jadwal (safi-cedvel); a tag is
published when a book names the role's subject word, or when two books agree.
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
MUYASSAR, DAAS, SAFI = "muyesser-irab", "daas-irab", "safi-cedvel"
QAC = "qac"                                                     # Quranic Arabic Corpus morphology (already the grid's source)
BOOKS = (MUYASSAR, DAAS, SAFI)

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
COND_HEAD = _sk("أداة", "اسم", "حرف", "ظرف", "فعل", "جملة", "وفعل", "للشرط", "معنى")      # "متضمن معنى الشرط"
COND_BOTH = _sk("وجوابه", "والجواب", "وجوابها", "وجوابها")
JAWAB, JAWAB_OF = _sk("جواب", "جوابا"), _sk("لو", "لولا", "إذا", "لما", "شرط", "الشرط")
CLAUSE = _sk("جملة", "الجملة", "جمل")
PROCLITIC_NAMES = _sk("الواو", "الفاء", "اللام")
ALT_MARK = _sk("يجوز", "ويجوز", "قيل", "وقيل", "يحتمل", "ويحتمل", "ممكن")


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
        elif _bare(w, KHA) or (i > 0 and _bare(w, KHA_POSS) and not _bare(prev, MUB | KHA)):
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
PAREN = re.compile(r"\(([^()]{1,60})\)")
NOTE = re.compile(r"\[\[(.*?)\]\]", re.S)                       # a book's own alternative readings / footnotes


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


BACKREF = _sk("ب", "ل", "من", "على", "إلى", "عن", "مثل", "ك", "بدل", "نعت", "في", "جملة", "والجملة", "لـ")
LETTERS = {skeleton(k): v for k, v in {"الواو": "و", "الفاء": "ف", "اللام": "ل", "الكاف": "ك", "الباء": "ب", "الهاء": "ه",
                                         "التاء": "ت", "النون": "ن", "السين": "س", "الميم": "م", "الياء": "ي"}.items()}


def split_inline(text, W, delim, first_ok=lambda b: True, stems=False):
    """Heads run inline (Da'ās ﴿…﴾, Ṣāfī (…)). A delimited word is a head — not a back-reference — when it names
    the next unprocessed word(s) of the ayah (within 3), or a letter (الواو / الفاء / اللام…) of the next word,
    and is not introduced by a preposition ("متعلق ب (فريقا)")."""
    heads, p = [], 0
    for m in delim.finditer(text):
        before = tokens(text[:m.start()])[-1:]
        prev = skeleton(before[0]) if before else ""
        starts = not text[:m.start()].strip() or text[:m.start()].rstrip()[-1] in ".\n"
        if prev in BACKREF and not starts:
            continue
        key = skeleton("".join(tokens(m.group(1))))
        if key in LETTERS:
            L = LETTERS[key]
            if p < len(W) and W[p].startswith(L):
                heads.append((m, [p]))
            elif 0 < p <= len(W) and W[p - 1].endswith(L):
                heads.append((m, [p - 1]))                        # a suffix letter: الهاء / الكاف
            continue
        idx = align(m.group(1), W, p)
        if (idx is None or idx[0] < p) and stems:                  # Ṣāfī lists a stem and its suffix apart: (رب) + (الكاف)
            stem = skeleton("".join(tokens(m.group(1))))
            near = [i for i in range(p, min(p + 4, len(W))) if len(stem) >= 2 and stem in W[i]]
            idx = [near[0]] if near and len(tokens(m.group(1))) == 1 else idx
        if idx is not None and (starts or p <= idx[0] <= p + 3) and first_ok(m.group(1)):
            heads.append((m, idx))
            if idx[0] >= p:
                p = idx[-1] + 1
    out = []
    for k, (m, idx) in enumerate(heads):
        end = heads[k + 1][0].start() if k + 1 < len(heads) else len(text)
        out.append((m.group(1), text[m.end():end].strip(), idx))
    return out


def safi_parts(text):
    """Ṣāfī: the `* الإعراب:` section = a paragraph of (word) descriptions + `جملة: «…» في محل …` lines."""
    sec = text.split("* الإعراب:", 1)[-1] if "* الإعراب:" in text else text
    sec = re.split(r"\n\*\s", sec, maxsplit=1)[0]
    words, clauses = [], []
    for ln in sec.split("\n"):
        ln = ln.strip()
        if re.match(r"^و?جملة:", ln):                         # one line can hold several `وجملة: «…» … ` statements
            for m in re.finditer(r"و?جملة:\s*«([^»]+)»(.*?)(?=و?جملة:\s*«|$)", ln):
                clauses.append((m.group(1), m.group(2).strip()))
        elif ln:
            words.append(ln)
    return " ".join(words), clauses


# ── alignment: head → word indexes ───────────────────────────────────────────
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
OTHER_SUBJECT = _sk("المصدر", "المؤول", "مصدر", "الجملة", "جملة")                # "والمصدر المؤول … مبتدأ": not the head
PP_WORDS = _sk("الجار", "جار")                                                    # "جار ومجرور … خبر مقدم" describes the head only when it opens the clause
# Function words the books use in their descriptions ("في جواب لو"): never resolved to an ayah word by uniqueness
FUNCTION_WORDS = _sk("في", "من", "على", "إلى", "إن", "أن", "لا", "ما", "هو", "هي", "كان", "قد", "ثم", "أو", "بين", "عن", "لو", "إذا", "الذي", "التي")


def resolve(tok, W, idx):
    """Word index a book's token names: a word of the head first, else a word that is unique in the ayah."""
    if tok in ("و", "ف"):                                          # a bare conjunction before a ﴿quote﴾, not a word of the ayah
        return None
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
    same clause ("وعليم خبرها"), or "جملة X". A bare "والجملة … خبر" says nothing about where it starts → "low".
    Text in [[…]] is the book's alternative reading: flagged alt."""
    body = HEAD.sub(lambda m: "﴿" + re.sub("[،.؛:]", " ", m.group(1)) + "﴾", body)   # keep quotes whole
    found = []
    chunks = [(c, k % 2 == 1) for k, c in enumerate(NOTE.split(body))]
    for chunk, is_note in chunks:
        pieces = re.split(r"(?:الثاني|الثالث|الرابع|الخامس|السادس)\s*:", chunk)   # "الأول: … الثاني: …" — wujūh, only the first is primary
        segs = [(n, seg) for k, piece in enumerate(pieces) for n, seg in enumerate(re.split(r"\sأو\s", " " + piece)) if True for n in [n + (k > 0)]]
        for a, seg in segs:                                                # later alternatives are flagged
            for clause in re.split(r"[،.؛:]", seg):
                toks, qb, starts_q = clause_items(clause)
                if any(_bare(t, ALT_MARK) for t in toks):                  # "يجوز أن يكون خبرا": a permitted reading
                    toks_alt = True
                else:
                    toks_alt = False
                roles = role_tokens(toks)
                prev_ri = -1
                for ri, role in roles:                                     # each role has its own subject, found in its own stretch
                    seg_start, prev_ri = prev_ri + 1, ri
                    before = toks[seg_start:ri]
                    ck = [k for k in range(seg_start, ri) if _bare(toks[k], CLAUSE)]
                    word, conf, scope = idx[0], "low", "word"
                    if ck:                                                 # a sentence-level role
                        scope = "clause"
                        m = re.search(r"جمل[ةتا]*\s*﴿([^﴾]+)﴾", clause)     # only "جملة ﴿X﴾" names its sentence
                        quote = m.group(1) if m else None
                        q_idx = align(quote, W, 0) if quote else None
                        nxt_k = ck[-1] + 1
                        named = resolve(toks[nxt_k], W, idx) if nxt_k < ri else None
                        if q_idx:
                            word, conf = q_idx[0], "high"                  # "وجملة ﴿X﴾ خبر…"
                        elif named is not None:
                            word, conf = named, "high"                     # "وجملة أنشأناهن خبر إن"
                    else:
                        first_is_pp = "جر" in before and any(_bare(t, OMITTED) for t in before)   # "جار ومجرور متعلقان بمحذوف خبر"
                        order = before if first_is_pp else list(reversed(before))               # the PP starts at its first word
                        subj = next((r for r in (resolve(t, W, idx) for t in order if t not in NOT_A_WORD) if r is not None), None)
                        if subj is None and qb[ri]:                        # "و﴿إذا﴾ ظرف … متضمن معنى الشرط": the quote is the subject
                            q = align(qb[ri], W, 0)
                            subj = q[0] if q else None
                        if subj is not None:
                            word, conf = subj, "high"
                        elif len(idx) == 1 and not any(t in OTHER_SUBJECT or (t in PP_WORDS and k > 1) for k, t in enumerate(before)):
                            word, conf = idx[0], "high"                    # "﴿الله﴾: مبتدأ"
                        elif before[:1] and before[0] in PROCLITIC_NAMES:
                            word, conf = idx[0], "high"                    # "الواو حالية"
                    found.append((word, role, scope, is_note or a > 0 or toks_alt, conf))
    return found


def tag_safi_clause(quote, body, W):
    """Ṣāfī's `جملة: «X…» في محل رفع خبر المبتدأ` — the sentence is named, so the role goes on its first word."""
    q = re.split(r"\.\.|…", quote)[0]
    for n in (3, 2, 1):
        toks_q = tokens(q)[:n]
        if not toks_q:
            return []
        idx = align(" ".join(toks_q), W, 0)
        if idx and not (len(toks_q) == 1 and skeleton(toks_q[0]) in FUNCTION_WORDS):
            roles = role_tokens(norm_tokens(body))
            return [(idx[0], r, "clause", False, "high") for _, r in roles]
    return []


# ── one entry → raw tags ─────────────────────────────────────────────────────
def entry_tags(book, text, W):
    """-> [(word, role, scope, alt, conf, quote)] for one entry; W = skeleton words of the entry's ayah range."""
    out, lines = [], []
    if book == MUYASSAR:
        for head, body in split_muyassar(text):
            idx = align(head, W, 0)
            lines.append((head, body, idx))
        # sequential alignment (a head repeats earlier words only by quoting them)
        p, lines = 0, []
        for head, body in split_muyassar(text):
            idx = align(head, W, p)
            if idx:
                p = idx[-1] + 1
            lines.append((head, body, idx))
    elif book == DAAS:
        lines = split_inline(text, W, HEAD)
    else:
        words, clauses = safi_parts(text)
        lines = split_inline(words, W, PAREN, stems=True)
        for quote, body in clauses:
            for word, role, scope, alt, conf in tag_safi_clause(quote, body, W):
                out.append((word, role, scope, alt, conf, f"جملة: «{quote}» {body}"[:400]))
    for head, body, idx in lines:
        if not idx:
            continue
        for word, role, scope, alt, conf in tag_line(head, body, idx, W):
            out.append((word, role, scope, alt, conf, f"{head} — {body}"[:400]))
    return out, sum(1 for *_, idx in lines if idx), len(lines)


def sk_words(words):
    return [skeleton(re.sub("[ۖ-ۭ]", "", w["ar"])) for w in words]


REL_PRONOUNS = _sk("الذي", "الذين", "التي", "اللاتي", "اللائي", "اللذان", "اللتان")   # corpus tags some relatives as conditional: left to the books


def displayable(t):
    """Shown to students: the book names the subject word (high) and it is its primary reading, or two books agree."""
    return not t["alt"] and (t["conf"] == "high" or len(t["src"]) > 1)


CONFLICTS = []                                                 # words the books contradict themselves on, kept for review
EXCLUSIVE = (("mubteda", "haber"), ("sart", "cevap"))          # one word can't be both at word level


def settle(surah, ayah, word, tags):
    """A word is not both subject and predicate (nor both şart and cevap). More book support wins; a tie shows neither."""
    for x, y in EXCLUSIVE:
        tx = next((t for t in tags if t["r"] == x and t["scope"] == "word"), None)
        ty = next((t for t in tags if t["r"] == y and t["scope"] == "word"), None)
        if tx and ty:
            nx, ny = len(tx["src"]), len(ty["src"])
            drop = [ty] if nx > ny else [tx] if ny > nx else [tx, ty]
            CONFLICTS.append({"ref": f"{surah}:{ayah}#{word}", "roles": [x, y], "support": [nx, ny],
                              "dropped": [t["r"] for t in drop]})
            tags = [t for t in tags if t not in drop]
    return tags


def build_surah(surah, only=None):
    words = json.loads((LIB / "w" / f"s{surah:03d}.json").read_text("utf-8"))
    data = json.loads((LIB / f"s{surah:03d}.json").read_text("utf-8"))
    merged = defaultdict(lambda: defaultdict(dict))               # ayah -> word -> role -> tag
    tot = {"lines": 0, "aligned": 0}
    for e in data["entries"]:
        if e["b"] not in BOOKS:
            continue
        rng = [a for a in range(e["s"], e["e"] + 1) if words.get(str(a), {}).get("w") and (not only or a == only or e["s"] != e["e"])]
        if not rng or (only and not e["s"] <= only <= e["e"]):
            continue
        W, owner = [], []                                         # concatenated words of the entry's ayahs
        for a in range(e["s"], e["e"] + 1):
            ws = sk_words(words.get(str(a), {}).get("w", []))
            W += ws; owner += [(a, i) for i in range(len(ws))]
        tags, aligned, nlines = entry_tags(e["b"], e["t"], W)
        tot["lines"] += nlines; tot["aligned"] += aligned
        key = f"{e['b']}:{e['s']}-{e['e']}"
        for word, role, scope, alt, conf, quote in tags:
            a, i = owner[word]
            t = merged[a][i].setdefault(role, {"r": role, "scope": scope, "alt": alt, "conf": conf, "src": []})
            if not any(s["b"] == e["b"] for s in t["src"]):
                t["src"].append({"b": e["b"], "k": key, "q": quote})
            t["alt"] = t["alt"] and alt
            t["conf"] = "high" if "high" in (t["conf"], conf) else "low"
            if scope == "clause":
                t["scope"] = "clause"                              # a book that names the sentence beats one that doesn't
    for a in range(1, 300):                                       # the corpus names conditional / answer particles itself
        ws = words.get(str(a), {}).get("w")
        if not ws or (only and a != only):
            continue
        for i, w in enumerate(ws):
            for needle, role in (("أداة شرط", "sart"), ("حرف جواب الشرط", "cevap")):
                if needle in w["pa"] and skeleton(w["ar"]) not in REL_PRONOUNS:
                    t = merged[a][i].setdefault(role, {"r": role, "scope": "word", "alt": False, "conf": "high", "src": []})
                    if not any(x["b"] == QAC for x in t["src"]):
                        t["src"].append({"b": QAC, "k": f"qac:{surah}:{a}:{i + 1}", "q": f"{w['pa']} — {w['pt']}"})
    res = {}
    for a, byword in sorted(merged.items()):
        if only and a != only:
            continue
        shown = {str(i): sorted(settle(surah, a, i, [t for t in r.values() if displayable(t)]), key=lambda t: ROLES.index(t["r"]))
                 for i, r in sorted(byword.items())}
        shown = {i: ts for i, ts in shown.items() if ts}
        if shown:
            res[str(a)] = shown
    return res, tot, merged


def prune_orphan_answers(res, window=3):
    """An answer needs a condition. A cevap that only one book names, with no şart in this ayah or the 3 before it, is dropped."""
    n = 0
    for a in sorted(res, key=int):
        near = [res.get(str(int(a) - d), {}) for d in range(window + 1)]
        has_sart = any(t["r"] == "sart" for ayah in near for ts in ayah.values() for t in ts)
        if has_sart:
            continue
        for i in list(res[a]):
            kept = [t for t in res[a][i] if not (t["r"] == "cevap" and len(t["src"]) == 1)]
            n += len(res[a][i]) - len(kept)
            if kept:
                res[a][i] = kept
            else:
                del res[a][i]
        if not res[a]:
            del res[a]
    return n


def print_ayah(s, a):
    res, tot, _ = build_surah(s, a)
    w = json.loads((LIB / "w" / f"s{s:03d}.json").read_text("utf-8"))[str(a)]["w"]
    print(tot)
    for i, tags in res.get(str(a), {}).items():
        print(i, w[int(i)]["ar"], [(t["r"], t["scope"], "+".join(x["b"][:3] for x in t["src"])) for t in tags])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print_ayah(*map(int, sys.argv[1].split(":")))
        sys.exit()
    (LIB / "roles").mkdir(exist_ok=True)
    grand = {"lines": 0, "aligned": 0}
    counts = defaultdict(int)
    pruned = 0
    for s in range(1, 115):
        res, tot, _ = build_surah(s)
        grand["lines"] += tot["lines"]; grand["aligned"] += tot["aligned"]
        for a in res.values():
            for tags in a.values():
                for t in tags:
                    counts[(t["r"], len(t["src"]))] += 1
        pruned += prune_orphan_answers(res)
        (LIB / "roles" / f"s{s:03d}.json").write_text(json.dumps(res, ensure_ascii=False, separators=(",", ":")), "utf-8")
    (LIB / "roles" / "CONFLICTS.json").write_text(json.dumps(CONFLICTS, ensure_ascii=False, indent=0), "utf-8")
    print(grand, f"aligned {grand['aligned'] / max(1, grand['lines']):.1%}")
    print(f"single-source cevap tags with no şart in the 3 ayahs before: dropped {pruned}")
    ties = sum(1 for c in CONFLICTS if len(c["dropped"]) == 2)
    print(f"contradictions: {len(CONFLICTS)} (resolved by support {len(CONFLICTS) - ties}, tie → neither shown {ties})")
    for k in sorted(counts):
        print(k, counts[k])

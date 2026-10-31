"""Sentence-structure roles derived from the words' own grammar (no book involved).

Three kinds of sentence are told apart, because their parts have different names:
  nominal sentence       مبتدأ + خبر            (mübteda + haber)
  إنّ and its sisters     اسم إنّ + خبر إنّ       (ism-i inne + haber-i inne)   — the ism is NOT a mübteda
  كان and its sisters     اسم كان + خبر كان       (ism-i kâne + haber-i kâne)   — likewise
Every rule is conservative (it stays silent rather than guess) and carries a name; validate_structure.py compares each
rule with the book-sourced tags, and only rules that agree with the books are switched on in ENABLED.
"""
import re

from build_word_roles import skeleton

PAUSE_END = re.compile("[\u06D6-\u06D8\u06DA\u06DC]")             # a waqf sign after the word: a sentence boundary (not ۛ, which pairs two stops)
LEAD = ("حرف عطف", "حرف استئناف", "واو الحال", "حرف استفهام")  # particles glued in front of the word
NEW_CLAUSE = ("حرف استئناف", "واو الحال")                      # …and the ones that open a new clause
PRON = {skeleton(w) for w in ("هو", "هي", "هم", "هما", "هن", "أنت", "أنتم", "أنتما", "أنتن", "أنا", "نحن")}
INNA = {skeleton(w) for w in ("إن", "إنّ", "أنّ", "كأنّ", "لكنّ", "لعلّ", "ليت")}
KANA_ROOTS = {"ك و ن", "ل ي س", "ص ب ح", "ظ ل ل", "ب ي ت", "ص ي ر", "ض ح ي", "م س ي"}
CASES = {"مرفوع": "nom", "منصوب": "acc", "مجرور": "gen", "مجزوم": "jus"}

ENABLED = {                                                   # rules that agree with the books at 90% or more (validate_structure.py)
    "nominal.pronoun", "nominal.demonstrative", "nominal.noun",   # 98% · 99% · 98%
    "nominal.khabar.word", "nominal.khabar.clause",               # 93% · 98%
    "inna.ism.attached", "inna.ism.noun", "inna.khabar.word",     # no book tags to compare the ism with (sampled by hand) · 92%
    "kana.ism.noun",                                              # sampled by hand
}                                                             # off: nominal.khabar.pp (76%: which PP?), kana.khabar.word (82%)


def parts(w):
    return [p.strip() for p in w["pa"].split("+")]


def core(w):
    """The word's parts without the particles glued in front of it."""
    ps = parts(w)
    while ps and ps[0] in LEAD:
        ps = ps[1:]
    return ps


def case(w):
    return next((v for k, v in CASES.items() if k in w.get("da", "")), "")


def starts_clause(words, i):
    if i == 0:
        return True
    if PAUSE_END.search(words[i - 1]["ar"]):
        return True
    return any(p in NEW_CLAUSE for p in parts(words[i]))


def stem(w):
    sk = skeleton(re.sub("[ۖ-ۭ]", "", w["ar"]))
    return sk[1:] if sk[:1] in "وف" and len(sk) > 1 else sk


def kind(w):
    """noun / proper / dem / rel / pron / verb / pp / particle — from the word's first content part."""
    c = core(w)
    if not c:
        return "particle"
    head = c[0]
    if head == "حرف جر":
        return "pp"
    if head.startswith("حرف") or head.startswith("أداة") or head == "لام التوكيد":
        return "particle"
    if head.startswith("فعل"):
        return "verb"
    if head == "اسم إشارة":
        return "dem"
    if head == "اسم موصول":
        return "rel"
    if head == "ضمير":
        return "pron" if stem(w) in PRON and len(c) == 1 else "attached"
    if head in ("اسم", "اسم علم", "صفة"):
        return "noun"
    return "particle"


def definite(w):
    """A proper name, or a noun with the article ٱل — an indefinite noun that opens a sentence is often a khabar (of an omitted mübteda)."""
    return "اسم علم" in parts(w) or bool(re.match("^[وف]?[\u064B-\u0652]*\u0671", w["ar"]))


def is_inna(w):
    """إنّ / أنّ / كأنّ / لكنّ / لعلّ / ليت — alone, or with an attached pronoun (أَنَّهُۥ، إِنَّكَ). Not إنّما (kāffa) and not the
    verb-particles لن / كي / أن."""
    ps = parts(w)
    if "حرف نصب" not in ps or "حرف كاف" in ps or "حرف مصدري" in ps:
        return False
    sk = stem(w)
    for base in INNA:
        if sk == base or (sk.startswith(base) and has_attached_pronoun(w) and len(sk) - len(base) <= 3):
            return True
    return False


def has_attached_pronoun(w):
    ps = parts(w)
    return ps[-1] == "ضمير" if ps else False


def is_kana(w):
    return kind(w) == "verb" and w.get("r", "").strip() in KANA_ROOTS


def khabar_of(words, i, nxt):
    """The predicate right after the mübteda at i, as (index, scope, rule) — or None when it is not clear."""
    j = nxt(i)
    if j is None:
        return None
    kj = kind(words[j])
    if kj == "noun" and case(words[j]) == "nom" and not starts_clause(words, j):
        return (j, "word", "nominal.khabar.word")
    if kj == "pp":
        k = nxt(j)
        while k is not None and case(words[k]) == "gen" and kind(words[k]) == "noun":   # بِكُلِّ شَىْءٍ: the complement of the preposition
            k = nxt(k)
        if k is not None and kind(words[k]) == "noun" and case(words[k]) == "nom" and not starts_clause(words, k):
            return None                                            # the PP only qualifies the noun that follows: that noun is the khabar
        return (j, "word", "nominal.khabar.pp")
    if kj in ("verb", "rel") and not starts_clause(words, j):
        return (j, "clause", "nominal.khabar.clause")
    return None


def derive(words):
    """-> [(word index, role, scope, rule, gov)] for one ayah. role ∈ mubteda/haber/ismInna/ismKana."""
    out = []
    n = len(words)

    def nxt(i):
        return i + 1 if i + 1 < n and not PAUSE_END.search(words[i]["ar"]) else None

    # ── إنّ and sisters: the ism is not a mübteda ───────────────────────────────
    covered = set()                                              # words already named as an ism / khabar of inna or kāna
    for i, w in enumerate(words):
        if not is_inna(w):
            continue
        ism = None
        if has_attached_pronoun(w):
            out.append((i, "ismInna", "word", "inna.ism.attached", "inna")); ism = i
        else:
            j = nxt(i)
            if j is not None and case(words[j]) == "acc" and kind(words[j]) == "noun":
                out.append((j, "ismInna", "word", "inna.ism.noun", "inna")); ism = j; covered.add(j)
            elif j is not None and kind(words[j]) in ("dem", "rel", "pron") and "حرف جر" not in parts(words[j]):
                out.append((j, "ismInna", "word", "inna.ism.noun", "inna")); ism = j; covered.add(j)
        if ism is not None:
            k = nxt(ism)
            if k is not None and kind(words[k]) == "noun" and case(words[k]) == "nom":
                out.append((k, "haber", "word", "inna.khabar.word", "inna")); covered.add(k)

    # ── كان and sisters ────────────────────────────────────────────────────────
    for i, w in enumerate(words):
        if not is_kana(w) or "حرف نصب" in parts(w):
            continue
        j = nxt(i)
        if j is not None and kind(words[j]) == "noun" and case(words[j]) == "nom":
            out.append((j, "ismKana", "word", "kana.ism.noun", "kana")); covered.add(j)
            k = nxt(j)
            if k is not None and kind(words[k]) == "noun" and case(words[k]) == "acc":
                out.append((k, "haber", "word", "kana.khabar.word", "kana")); covered.add(k)

    # ── plain nominal sentences ───────────────────────────────────────────────
    after_kaffa = {i + 1 for i, w in enumerate(words) if "حرف كاف" in parts(w) and "حرف نصب" in parts(w)}
    for i, w in enumerate(words):
        if i in covered:
            continue
        if not (starts_clause(words, i) or i in after_kaffa):
            continue
        k = kind(w)
        c0 = core(w)
        if i == 0 and any(p.startswith("حرف نداء") for p in parts(w)):
            continue
        if k == "pron":
            rule = "nominal.pronoun"
        elif k == "dem":
            rule = "nominal.demonstrative"
        elif k == "noun" and case(w) == "nom" and c0 and c0[0] != "صفة" and definite(w):
            rule = "nominal.noun"
        else:
            continue
        khabar = khabar_of(words, i, nxt)
        if khabar is None and rule == "nominal.noun":              # a bare noun without a predicate is often the khabar of an omitted mübteda
            continue
        out.append((i, "mubteda", "word", rule, None))
        if khabar:
            out.append((khabar[0], "haber", khabar[1], khabar[2], None))
    return out

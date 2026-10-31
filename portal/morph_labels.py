"""Arabic / Turkish labels for Quranic Arabic Corpus morphology tags.

Input: the segments of one word from quranic-corpus-morphology-0.4.txt (the
original, unmodified Quranic Arabic Corpus v0.4 file; GPL, credit + link to
corpus.quran.com required), each (form, tag, feature string).
Output: {"pos_ar", "pos_tr", "det_ar", "det_tr", "root", "lemma"} for the word grid.
Turkish terms follow irab_library/glossary_tr.md.
"""

# Part-of-speech tags → (Arabic, Turkish)
POS = {
    # nominals
    "N": ("اسم", "İsim"), "PN": ("اسم علم", "Özel isim"), "ADJ": ("صفة", "Sıfat"),
    "IMPN": ("اسم فعل أمر", "Emir ism-i fiili"), "PRON": ("ضمير", "Zamir"),
    "DEM": ("اسم إشارة", "İsm-i işaret"), "REL": ("اسم موصول", "İsm-i mevsûl"),
    "T": ("ظرف زمان", "Zaman zarfı"), "LOC": ("ظرف مكان", "Mekân zarfı"),
    # verbs
    "PERF": ("فعل ماض", "Fi'l-i mâzî"), "IMPF": ("فعل مضارع", "Fi'l-i muzâri"),
    "IMPV": ("فعل أمر", "Fi'l-i emr"),
    # particles
    "P": ("حرف جر", "Harf-i cer"), "EMPH": ("لام التوكيد", "Te'kîd lâmı"),
    "PRP": ("لام التعليل", "Ta'lîl lâmı"), "CONJ": ("حرف عطف", "Atıf harfi"),
    "SUB": ("حرف مصدري", "Masdar harfi"), "ACC": ("حرف نصب", "Nasb harfi"),
    "AMD": ("حرف استدراك", "İstidrâk harfi"), "ANS": ("حرف جواب", "Cevap harfi"),
    "AVR": ("حرف ردع", "Red' harfi"), "CAUS": ("حرف سببية", "Sebebiyye harfi"),
    "CERT": ("حرف تحقيق", "Tahkîk harfi"), "CIRC": ("واو الحال", "Hâl vâvı"),
    "COM": ("واو المعية", "Maiyyet vâvı"), "COND": ("أداة شرط", "Şart edatı"),
    "EQ": ("حرف تسوية", "Tesviye harfi"), "EXH": ("حرف تحضيض", "Tahdîd harfi"),
    "EXL": ("حرف تفصيل", "Tafsîl harfi"), "EXP": ("أداة استثناء", "İstisnâ edatı"),
    "FUT": ("حرف استقبال", "İstikbâl harfi"), "INC": ("حرف ابتداء", "İbtidâ harfi"),
    "INT": ("حرف تفسير", "Tefsîr harfi"), "INTG": ("أداة استفهام", "İstifhâm edatı"),
    "NEG": ("حرف نفي", "Nefy harfi"), "PREV": ("حرف كاف", "Kâff harfi"),
    "PRO": ("حرف نهي", "Nehy harfi"), "REM": ("حرف استئناف", "İsti'nâf harfi"),
    "RES": ("أداة حصر", "Hasr edatı"), "RET": ("حرف إضراب", "İdrâb harfi"),
    "RSLT": ("حرف جواب الشرط", "Şart cevabı harfi"), "SUP": ("حرف زائد", "Zâide harf"),
    "SUR": ("حرف فجاءة", "Mufâcee harfi"), "VOC": ("حرف نداء", "Nidâ harfi"),
    "INL": ("حروف مقطعة", "Hurûf-ı mukattaa"), "DET": ("ال التعريف", "Harf-i ta'rîf"),
    "ATT": ("ها التنبيه", "Tenbîh hâsı"), "ADDR": ("حرف خطاب", "Hitap harfi"),
}
# Derived nominal forms (shown as detail)
DERIVED = {"ACT_PCPL": ("اسم فاعل", "İsm-i fâil"), "PASS_PCPL": ("اسم مفعول", "İsm-i mef'ûl"),
           "VN": ("مصدر", "Masdar")}
CASE = {"NOM": ("مرفوع", "Merfû"), "ACC": ("منصوب", "Mansûb"), "GEN": ("مجرور", "Mecrûr")}
MOOD = {"IND": ("مرفوع", "Merfû"), "SUBJ": ("منصوب", "Mansûb"), "JUS": ("مجزوم", "Meczûm")}
PERSON = {"1": ("متكلم", "mütekellim"), "2": ("مخاطب", "muhâtab"), "3": ("غائب", "gâib")}
GENDER = {"M": ("مذكر", "müzekker"), "F": ("مؤنث", "müennes")}
NUMBER = {"S": ("مفرد", "müfred"), "D": ("مثنى", "tesniye"), "P": ("جمع", "cemi")}
VERB_FORM = {1: "mücerred", 2: "tef'îl", 3: "mufâale", 4: "if'âl", 5: "tefa''ul", 6: "tefâul",
             7: "infiâl", 8: "iftiâl", 9: "if'ilâl", 10: "istif'âl", 11: "if'îlâl"}
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI"}


def _pgn(tag):
    """'3MP' / 'MS' / '1S' → (Arabic, Turkish) person-gender-number, or None."""
    p = tag[0] if tag[:1] in PERSON else ""
    rest = tag[len(p):]
    if not rest or any(c not in "MFSDP" for c in rest):
        return None
    ar, tr = [], []
    if p:
        ar.append(PERSON[p][0]); tr.append(PERSON[p][1])
    for c in rest:
        src = GENDER if c in GENDER and c != "P" else NUMBER
        if c == "P" and (len(rest) == 1 or rest.index(c) > 0):
            src = NUMBER
        if c in src:
            ar.append(src[c][0]); tr.append(src[c][1])
    return " ".join(ar), " ".join(tr)


BUCKWALTER = dict(zip("'|>&<}AbptvjHxd*rzs$SDTZEg_fqklmnhwYyFNKaui~o`{^#", "ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْٰٱٓ۟"))


def to_arabic(bw):
    return "".join(BUCKWALTER.get(c, c) for c in bw)


def _segment(tag, feats):
    """tag = the file's TAG column (the segment's part of speech)."""
    tags = feats.split("|")
    info = dict(t.split(":", 1) for t in tags[1:] if ":" in t and not t.endswith("+"))
    flags = [t for t in tags[1:] if ":" not in t]
    label = POS.get(tag) or (POS["PERF"] if tag == "V" else POS["N"])
    if tag == "V":
        label = POS[next((t for t in flags if t in ("PERF", "IMPF", "IMPV")), "PERF")]
    return tag, label, flags, info, tags[0]


def word_labels(segments):
    """segments: list of (form, category, features) for one word, in order."""
    parts_ar, parts_tr, det_ar, det_tr = [], [], [], []
    root = lemma = ""
    for _form, tag, feats in segments:
        pos, (lab_ar, lab_tr), flags, info, kind = _segment(tag, feats)
        if pos == "DET":            # the article is part of the word, not a separate label
            continue
        parts_ar.append(lab_ar); parts_tr.append(lab_tr)
        if kind != "STEM":
            continue
        # in roots the corpus writes hamza as "A"
        root = to_arabic(info.get("ROOT", "").replace("A", ">")) or root
        lemma = to_arabic(info.get("LEM", "")) or lemma
        if "PCPL" in flags:
            d = DERIVED["ACT_PCPL" if "ACT" in flags else "PASS_PCPL"]
            det_ar.append(d[0]); det_tr.append(d[1])
        if "VN" in flags:
            det_ar.append(DERIVED["VN"][0]); det_tr.append(DERIVED["VN"][1])
        if tag == "V":
            form = next((f.strip("()") for f in flags if f.startswith("(")), "I")
            n = {v: k for k, v in ROMAN.items()}.get(form, 1)
            det_ar.append(f"الوزن {ROMAN.get(n, n)}")
            det_tr.append(f"{VERB_FORM.get(n, n)} bâbı")
            if "PASS" in flags:
                det_ar.append("مبني للمجهول"); det_tr.append("meçhul")
            # an imperfect verb with no MOOD tag is indicative (merfû)
            mood = info.get("MOOD", "IND" if "IMPF" in flags else None)
            if mood in MOOD:
                m = MOOD[mood]; det_ar.append(m[0]); det_tr.append(m[1])
        elif tag != "V":
            for f in flags:
                if f in CASE:
                    det_ar.append(CASE[f][0]); det_tr.append(CASE[f][1])
        for f in flags:
            pgn = _pgn(f)
            if pgn:
                det_ar.append(pgn[0]); det_tr.append(pgn[1].capitalize())
    return {
        "pos_ar": " + ".join(parts_ar), "pos_tr": " + ".join(parts_tr),
        "det_ar": "، ".join(det_ar), "det_tr": ", ".join(det_tr),
        "root": " ".join(root), "lemma": lemma,
    }


def load_corpus(path):
    """→ {(s, a, w): [(form, tag, feats), ...]} from quranic-corpus-morphology-0.4.txt."""
    words = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.startswith("("):
                continue                     # copyright header and column titles
            loc, form, tag, feats = line.rstrip("\n").split("\t")
            s, a, w, _seg = (int(x) for x in loc.strip("()").split(":"))
            words.setdefault((s, a, w), []).append((form, tag, feats))
    return words

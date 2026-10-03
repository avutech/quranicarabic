"""Download an i'rab book from shamela.ws into the irab_kutuphane_*.json format.

    venv/bin/python fetch_shamela.py ukbari-tibyan makki-mushkil
    venv/bin/python fetch_shamela.py --sample makki-mushkil     # parse cache, print Fatiha + Baqara 1-20

Writes  Irab Kitaplari/irab_kutuphane_<code>.json
Schema  {kaynak, kod, kitap, muellif, vefat, not, indirilme,
         girdiler: [{sure, ayet_bas, ayet_son, metin}]}

Two phases:
 1. download — every page https://shamela.ws/book/<id>/<n> is fetched once,
    sequentially (DELAY between requests, honest User-Agent; shamela.ws has no
    robots.txt). Only the text block (div.nass) is kept, in a resumable page
    cache under CACHE_DIR (outside the repo).
 2. parse — pages are joined into one paragraph stream (paragraphs cut by a
    page break are glued back), surah boundaries come from the book's shamela
    table of contents, the shamela editor's "[السورة: n]" cross-references and
    any footnote block (div.hamesh / "____") are dropped, and the stream is cut
    into per-ayah entries:
      * ukbari-tibyan: the edition's ayah headers "قال تعالى: (… (٥))" carry
        ayah numbers; every header starts a new entry.
      * makki-mushkil: no numbers in the text; the lemma each "قوله {…}"
        paragraph opens with is looked up in the Quran text (tanzil
        simple-clean via api.alquran.cloud) and the lemmas of a surah are
        aligned to mushaf order (align()); paragraphs without a lemma
        continue the current entry.
"""

import datetime as dt
import html as htmllib
import json
import re
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

OUT_DIR = Path(__file__).parent.parent / "Irab Kitaplari"
CACHE_DIR = Path(tempfile.gettempdir()) / "learnirab_shamela_cache"
UA = "learnirab-indexer/1.0"
DELAY = 0.7
QURAN_URL = "https://api.alquran.cloud/v1/quran/quran-simple-clean"

BOOKS = {
    "ukbari-tibyan": {
        "id": 22928,
        "kitap": "التبيان في إعراب القرآن",
        "muellif": "أبو البقاء عبد الله بن الحسين العكبري",
        "vefat": "616",
        "baski": "تحقيق علي محمد البجاوي، عيسى البابي الحلبي",
    },
    "makki-mushkil": {
        "id": 5538,
        "kitap": "مشكل إعراب القرآن",
        "muellif": "مكي بن أبي طالب القيسي",
        "vefat": "437",
        "baski": "تحقيق حاتم صالح الضامن، مؤسسة الرسالة، ط2 1405",
    },
}

VERSES = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111, 110, 98, 135,
          112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53,
          89, 59, 37, 35, 38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12,
          12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19, 36, 25, 22, 17, 19, 26,
          30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6]


# ───────────────────────────── download ─────────────────────────────

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8")
        except Exception as e:
            if attempt == 4:
                raise
            print(f"  retry {url} ({e})", file=sys.stderr)
            time.sleep(3 * (attempt + 1))


def extract_page(h):
    """The text block of one shamela page: div.nass (+ div.hamesh if any)."""
    i = h.find('<div class="nass')
    j = h.find('<div id="appended_pages"', i)
    if i < 0 or j < 0:
        return None
    return h[i:j]


def download(code):
    book = BOOKS[code]
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_f = CACHE_DIR / f"{code}.json"
    cache = json.loads(cache_f.read_text("utf-8")) if cache_f.exists() else {}
    if "last" not in cache:
        first = fetch(f"https://shamela.ws/book/{book['id']}/1")
        last = max(int(n) for n in re.findall(rf'shamela\.ws/book/{book["id"]}/(\d+)#p1', first))
        cache = {"last": last, "pages": {"1": extract_page(first)}}
        time.sleep(DELAY)
    pages = cache["pages"]
    for n in range(1, cache["last"] + 1):
        if str(n) in pages:
            continue
        pages[str(n)] = extract_page(fetch(f"https://shamela.ws/book/{book['id']}/{n}"))
        time.sleep(DELAY)
        if n % 25 == 0 or n == cache["last"]:
            cache_f.write_text(json.dumps(cache, ensure_ascii=False), "utf-8")
            print(f"{code}: page {n}/{cache['last']}", flush=True)
    cache_f.write_text(json.dumps(cache, ensure_ascii=False), "utf-8")
    return cache


def fetch_toc(code):
    """[(page_id, title)] of the top-level chapters, from the book card page."""
    bid = BOOKS[code]["id"]
    f = CACHE_DIR / f"{code}.toc.html"
    if not f.exists():
        f.write_text(fetch(f"https://shamela.ws/book/{bid}"), "utf-8")
    h = f.read_text("utf-8")
    h = h[h.find("فهرس الموضوعات"):]
    return [(int(p), htmllib.unescape(t).strip())
            for p, t in re.findall(rf'<a[^>]*href="https://shamela\.ws/book/{bid}/(\d+)"[^>]*>([^<]*)</a>', h)]


# ───────────────────────────── text helpers ─────────────────────────────

TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def norm(t):
    """Skeleton for matching: no diacritics, unified alef/ya/ta marbuta/hamza seats."""
    t = TASHKEEL.sub("", t)
    t = re.sub("[أإآٱ]", "ا", t)
    t = t.replace("ى", "ي").replace("ئ", "ي").replace("ؤ", "و").replace("ة", "ه").replace("ء", "")
    t = re.sub(r"[^ء-ي ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def skel(t):
    """Coarser key for Quran lookup: hamza and its seats dropped, since the
    books spell hamza differently from the mushaf (تبرؤوا/تبرءوا, استيأسوا/استيئسوا)."""
    return norm(re.sub("[أإؤئء]", "", TASHKEEL.sub("", t)))


def html_to_text(frag):
    frag = re.sub(r"<a [^>]*class=\"btn_tag[^>]*>.*?</a>", "", frag, flags=re.S)
    frag = re.sub(r"<br\s*/?>", " ", frag)
    t = htmllib.unescape(re.sub(r"<[^>]+>", "", frag))
    # editor's cross-references after quotations ([الْأَنْعَامِ: ١٦١]) and print-page marks ([٧٤])
    t = re.sub(r"\s*\[(?:[^\]0-9٠-٩]{2,40}:?\s*)?[0-9٠-٩][0-9٠-٩\s،,و-]*\]", "", t)
    return re.sub(r"[ \t\u00a0]+", " ", t).strip()


def page_paragraphs(page_html):
    """Author paragraphs of one page; footnotes (div.hamesh, or text after a
    '____' separator) are dropped."""
    if not page_html:
        return []
    body = re.split(r'<div class="hamesh', page_html)[0]
    paras = []
    for p in re.findall(r"<p[^>]*>(.*?)</p>", body, flags=re.S):
        t = html_to_text(p)
        if re.fullmatch(r"_{3,}.*", t, flags=re.S):
            break                                   # footnote block follows
        if t:
            paras.append(t)
    return paras


# Standard surah names (index = surah number) + the variant titles Makki uses.
SURAH_NAMES = [None] + (
    "الفاتحة البقرة آل_عمران النساء المائدة الأنعام الأعراف الأنفال التوبة يونس هود يوسف "
    "الرعد إبراهيم الحجر النحل الإسراء الكهف مريم طه الأنبياء الحج المؤمنون النور "
    "الفرقان الشعراء النمل القصص العنكبوت الروم لقمان السجدة الأحزاب سبأ فاطر يس "
    "الصافات ص الزمر غافر فصلت الشورى الزخرف الدخان الجاثية الأحقاف محمد الفتح "
    "الحجرات ق الذاريات الطور النجم القمر الرحمن الواقعة الحديد المجادلة الحشر الممتحنة "
    "الصف الجمعة المنافقون التغابن الطلاق التحريم الملك القلم الحاقة المعارج نوح الجن "
    "المزمل المدثر القيامة الإنسان المرسلات النبأ النازعات عبس التكوير الانفطار المطففين الانشقاق "
    "البروج الطارق الأعلى الغاشية الفجر البلد الشمس الليل الضحى الشرح التين العلق "
    "القدر البينة الزلزلة العاديات القارعة التكاثر العصر الهمزة الفيل قريش الماعون الكوثر "
    "الكافرون النصر المسد الإخلاص الفلق الناس"
).split()
SURAH_NAMES = [n and n.replace("_", " ") for n in SURAH_NAMES]
assert len(SURAH_NAMES) == 115 and SURAH_NAMES[114] == "الناس"
ALIASES = {"الحمد": 1, "المؤمنين": 23, "المؤمن": 40, "حم السجده": 41, "حم عسق": 42, "نون والقلم": 68,
           "سال سايل": 70, "قل اوحي": 72, "قل او حي": 72, "هل اتي": 76, "يتسالون": 78, "الم نشرح": 94,
           "لم يكن": 98, "الهاكم": 102, "ارايت": 107, "تبت": 111}


def surah_of_title(title):
    t = norm(title)
    t = re.sub(r"^(تفسير |تفسر |شرح )?(مشكل )?(اعراب )?(سوره |سوري )?", "", t)
    t = re.sub(r" (عليه|عليها|عليهم) السلام$| صلي الله عليه وسلم$| جل ذكره$", "", t).strip()
    for i, n in enumerate(SURAH_NAMES[1:], 1):
        if norm(n) == t:
            return i
    return {norm(k): v for k, v in ALIASES.items()}.get(t)


# ───────────────────────────── Quran matcher ─────────────────────────────

class Quran:
    def __init__(self):
        f = CACHE_DIR / "quran-simple-clean.json"
        if not f.exists():
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            f.write_text(fetch(QURAN_URL), "utf-8")
        surahs = json.loads(f.read_text("utf-8"))["data"]["surahs"]
        self.text, self.starts = {}, {}
        for s in surahs:
            parts, starts, pos = [], [], 1
            for a in s["ayahs"]:
                t = skel(a["text"].lstrip("﻿"))
                if s["number"] not in (1, 9) and a["numberInSurah"] == 1:
                    t = re.sub(r"^بسم الله الرحمن الرحيم ?", "", t)
                starts.append(pos)
                parts.append(t)
                pos += len(t) + 1
            self.text[s["number"]] = " " + " ".join(parts) + " "
            self.starts[s["number"]] = starts

    def ayah_at(self, s, off):
        st = self.starts[s]
        lo, hi = 0, len(st) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if st[mid] <= off:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    def candidates(self, s, quote):
        """All places of `quote` in surah s as [(first, last, weight)]. A
        leading و/ف may differ from the mushaf. If the full quote is absent
        (variant reading, spelling) its longest present prefix counts, at a
        lower weight; a single short word is too ambiguous for that."""
        words = skel(quote).split()
        if not words or s not in self.text:
            return []
        words[0] = re.sub(r"^[وف](?=\S{2})", "", words[0])
        txt = self.text[s]
        for n in range(len(words), 0, -1):
            if n < len(words) and n == 1 and len(words[0]) < 4:
                break
            # spaces are optional: the mushaf joins words like اوكلما, ياايها
            pat = re.compile(r" [وف]?" + " ?".join(map(re.escape, "".join(words[:n]))) + " ")
            hits = [(self.ayah_at(s, m.start() + 1), self.ayah_at(s, m.end() - 2),
                     1.0 if n == len(words) else 0.6) for m in pat.finditer(txt)]
            if hits:
                return hits
        return []

    def find(self, s, quote, cur):
        """(first, last, weight) of `quote` at or after ayah `cur` (else just before)."""
        hits = self.candidates(s, quote)
        fwd = next((h for h in hits if h[0] >= cur), None)
        back = next((h for h in reversed(hits) if h[0] < cur), None)
        h = fwd if fwd and (fwd[0] - cur <= 15 or not back) else back
        return h


def align(cands, n_ayahs):
    """Pick at most one candidate per lemma so that the picked ayahs follow
    the mushaf order (small step-backs allowed: the author often returns to a
    word of the previous ayah). Maximises matched lemmas, lightly penalising
    jumps. cands: [[(first, last, weight)], …] → [(first, last) | None, …]."""
    NEG = float("-inf")
    best = [(0.0, None)] + [(NEG, None)] * n_ayahs     # per start ayah: (score, state)
    states = {}                                          # (i, k) -> (score, prev state)
    for i, cs in enumerate(cands):
        new = []
        for k, (a, b, w) in enumerate(cs):
            top, ptr = NEG, None
            for p in range(0, n_ayahs + 1):
                sc = best[p][0]
                if sc == NEG:
                    continue
                d = a - max(p, 1)
                pen = 0.004 * d if d >= 0 else (0.3 * -d if -d <= 3 else None)
                if pen is not None and sc - pen > top:
                    top, ptr = sc - pen, best[p][1]
            if top > NEG:
                states[(i, k)] = (top + w, ptr)
                new.append((a, top + w, (i, k)))
        for a, sc, st in new:
            if sc > best[a][0]:
                best[a] = (sc, st)
    st = max(best, key=lambda x: x[0])[1]
    picked = [None] * len(cands)
    while st is not None:
        i, k = st
        picked[i] = cands[i][k][:2]
        st = states[st][1]
    return picked


# ───────────────────────────── segmentation ─────────────────────────────

GOD = r"(?:تعالى|عز وجل|جل وعز|تبارك وتعالى|سبحانه|جل ذكره|جلت عظمته)"
EPITHET = r"(?:" + GOD + r"\s*)?:?\s*"
LEAD = r"^(?:و?(?:قال|قوله)\s*" + EPITHET + ")"


def continues(prev, nxt):
    """Is `nxt` (first paragraph of a page) the rest of `prev` (last paragraph
    of the previous page)? Not if prev ends a sentence or nxt opens a lemma."""
    bare = TASHKEEL.sub("", nxt).lstrip()
    return not (re.search(r"[.:!؟»]\s*$", prev) or re.match(LEAD + r"[({]", bare)
                or bare[:1] in "({" or len(bare) < 80 and surah_of_title(bare))

class Para(str):
    """A paragraph's text plus the shamela pages it was read from."""
    def __new__(cls, text, pages):
        obj = super().__new__(cls, text)
        obj.pages = tuple(pages)
        return obj


def paragraph_stream(code, cache):
    """Yield (surah, paragraph) for the whole book, skipping surah headings
    and bare basmalas. Paragraphs cut by a page break are glued back."""
    toc = fetch_toc(code)
    starts = {}                                         # page -> [(title, surah)]
    last_s = 0
    for page, title in toc:
        s = 1 if "الاستفتاح" in title else surah_of_title(title)
        if s is None or s <= last_s and not (s == 1 and last_s == 1):
            if last_s:                                  # trailing appendix: stop there
                starts.setdefault(page, []).append((title, 0))
            continue                                    # intro, isti'adha
        starts.setdefault(page, []).append((title, s))
        last_s = s
    toc_surahs = {s for v in starts.values() for _, s in v if s}
    end_page = max(int(k) for k in cache["pages"])
    pages, prev = {}, None                              # page -> [paragraph]
    for n in range(1, end_page + 1):
        ps = [Para(t, [n]) for t in page_paragraphs(cache["pages"].get(str(n)))]
        if ps and prev and n not in starts and continues(prev[-1], ps[0]):
            prev[-1] = Para(prev[-1] + " " + ps.pop(0), prev[-1].pages + (n,))
        pages[n] = ps
        prev = ps or prev

    cur = 0
    basmala = norm("بسم الله الرحمن الرحيم")
    for n in range(1, end_page + 1):
        ps = pages[n]
        cuts = {}                                       # paragraph index -> surah
        used = set()
        for title, s in starts.get(n, []):
            key = norm(title).split()[-1]
            k = next((i for i, p in enumerate(ps) if i not in used and len(p) < 120
                      and ("سور" in norm(p)[:14] or key in norm(p).split())), None)
            if k is None:
                k = 0
                print(f"  {code}: heading for {title!r} not found on page {n}", file=sys.stderr)
            else:
                used.add(k)
            cuts[k] = s
        for i, p in enumerate(ps):
            if i in cuts:
                cur = cuts[i]
            elif cur and len(p) < 80 and surah_of_title(p) == cur + 1 and cur + 1 not in toc_surahs:
                cur += 1                                # heading the shamela TOC lacks
                continue
            if i in used or norm(p) == basmala or len(p) < 60 and cur and surah_of_title(p) == cur:
                continue                                # heading, basmala
            if cur:
                yield cur, p




NUM = r"\(\s*([٠-٩]+)\s*\)"


def bracketed(t):
    """(inside, rest) of the bracket t opens with, honouring nested (n)."""
    depth = 0
    for i, ch in enumerate(t):
        depth += ch in "({"
        depth -= ch in ")}"
        if depth == 0:
            return t[1:i], t[i + 1:]
    return t[1:], ""


def tibyan_anchor(s, text, cur, quran):
    """Ayah range opened by an ayah header of the edition, else None.
    Headers look like  قال تعالى: (اهدنا الصراط المستقيم (٦) صراط الذين …)
    where each (n) closes ayah n and words after the last number spill into
    n+1. The numbers have occasional typos (٣١٦ for ٢١٦), so a header whose
    quote is found in the mushaf at another place is placed by its text."""
    bare = TASHKEEL.sub("", text)
    m = re.match(LEAD, bare)
    if not m:
        return None
    body, trailing = bare[m.end():], None
    is_qal = re.match(r"^قال\s*" + GOD, bare) is not None   # «قال تعالى» introduces a header
    if body[:1] in "({":
        quote, rest = bracketed(body)
        trailing = re.match(r"\s*" + NUM, rest)          # (…) (١١٥)
        nums = re.findall(NUM, quote) + ([trailing.group(1)] if trailing else [])
    elif is_qal:                                        # header without brackets
        quote, nums = " ".join(body.split()[:10]), []
    else:
        return None
    if not nums and not is_qal:
        return None                                     # «قوله: (ذلك)» — a word of the current ayah
    nums = [int(x.translate(AR_DIGITS)) for x in nums]
    words = re.sub(NUM, " ", quote)
    found = quran.find(s, words, cur) if len(norm(words).split()) >= 3 or not nums else None
    if nums and 1 <= nums[0] <= VERSES[s - 1] and nums[-1] <= VERSES[s - 1]:
        if not found or found[2] < 1 or nums[0] in found[:2]:
            spill = trailing is None and nums[-1] < VERSES[s - 1] and norm(re.split(NUM, quote)[-1])
            return nums[0], nums[-1] + (1 if spill else 0)
    return found[:2] if found else None


def makki_lemma(text):
    """The Quranic lemma a Makki paragraph opens with, if any: {…} in most of
    the book; in the later surahs the braces are missing, so the first words
    after «قوله» are returned and the matcher keeps their longest prefix
    that occurs in the surah."""
    bare = TASHKEEL.sub("", text)
    m = re.match(LEAD + r"\{([^}]*)\}", bare) or re.match(r"^\s*\{([^}]*)\}", bare)
    if m:
        return m.group(1)
    m = re.match(r"^و?قوله\s*" + EPITHET + r"([^{(]+)", bare)
    return " ".join(m.group(1).split()[:7]) if m and "{" not in bare[:40] else None


def build_entries(s, paras, ranges, headers):
    """Group a surah's paragraphs into entries. A paragraph with a range opens
    a new entry unless it falls inside the current one (or, for a step back,
    inside an earlier one, which it is filed under); others continue."""
    out, entry = [], None
    for text, rng in zip(paras, ranges):
        if rng and not headers and entry and rng[0] < entry["ayet_bas"]:
            prev = next((e for e in reversed(out) if e["ayet_bas"] <= rng[0] <= e["ayet_son"]), None)
            if prev:
                prev["metin"].append(text)
                prev["_pages"].update(text.pages)
                continue
        if rng and (headers or entry is None or not entry["ayet_bas"] <= rng[0] <= entry["ayet_son"]):
            entry = {"sure": s, "ayet_bas": rng[0], "ayet_son": max(rng), "metin": [], "_pages": set()}
            out.append(entry)
        elif rng:
            entry["ayet_son"] = max(entry["ayet_son"], rng[1])
        elif entry is None:                             # text before a surah's first anchor
            entry = {"sure": s, "ayet_bas": 1, "ayet_son": 1, "metin": [], "_pages": set()}
            out.append(entry)
        entry["metin"].append(text)
        entry["_pages"].update(text.pages)
    for e in out:
        e["metin"] = "\n".join(e["metin"])
    return [e for e in out if e["metin"]]


def segment(code, cache, quran):
    by_surah = {}
    for s, text in paragraph_stream(code, cache):
        by_surah.setdefault(s, []).append(text)
    out = []
    for s, paras in by_surah.items():
        if code == "ukbari-tibyan":
            ranges, cur = [], 1
            for t in paras:
                r = tibyan_anchor(s, t, cur, quran)
                cur = r[0] if r else cur
                ranges.append(r)
        else:
            lemmas = [makki_lemma(t) for t in paras]
            idx = [i for i, l in enumerate(lemmas) if l]
            picked = align([quran.candidates(s, lemmas[i]) for i in idx], VERSES[s - 1])
            ranges = [None] * len(paras)
            for i, r in zip(idx, picked):
                ranges[i] = r
        out += build_entries(s, paras, ranges, headers=code == "ukbari-tibyan")
    # mushaf order; an ayah the author came back to keeps a single entry
    merged = []
    for e in sorted(out, key=lambda e: (e["sure"], e["ayet_bas"])):
        if merged and (merged[-1]["sure"], merged[-1]["ayet_bas"]) == (e["sure"], e["ayet_bas"]):
            merged[-1]["metin"] += "\n" + e["metin"]
            merged[-1]["ayet_son"] = max(merged[-1]["ayet_son"], e["ayet_son"])
            merged[-1]["_pages"] |= e["_pages"]
        else:
            merged.append(e)
    for e in merged:
        e["ref"] = make_ref(code, cache, sorted(e.pop("_pages")))
    return merged


def make_ref(code, cache, pages):
    """Where an entry comes from. print_pages uses the printed-edition page
    number shamela attaches to each page (data-page-num; the book card states
    «ترقيم الكتاب موافق للمطبوع»); it is left out if any page lacks one."""
    bid = BOOKS[code]["id"]
    ref = {"site": "shamela.ws", "code": code, "file": f"irab_kutuphane_{code}.json",
           "url": f"https://shamela.ws/book/{bid}/{pages[0]}",
           "shamela_pages": [pages[0], pages[-1]]}
    nums = [re.search(r'data-page-num="(\d+)"', cache["pages"][str(n)] or "") for n in pages]
    nums = [int(m.group(1)) for m in nums if m and int(m.group(1)) > 0]
    if len(nums) == len(pages):
        ref["print_pages"] = [min(nums), max(nums)]
    return ref


def write_book(code, girdiler):
    b = BOOKS[code]
    book = {
        "kaynak": f"shamela.ws/book/{b['id']}",
        "kod": code,
        "kitap": b["kitap"],
        "muellif": b["muellif"],
        "vefat": b["vefat"],
        "not": f"Metin: {b['baski']}. Sayfa ayraçları ve muhakkik dipnotları çıkarıldı; "
               "ayet sınırları otomatik belirlendi.",
        "indirilme": dt.datetime.now(dt.timezone.utc).isoformat(),
        "girdiler": girdiler,
    }
    out = OUT_DIR / f"irab_kutuphane_{code}.json"
    out.write_text(json.dumps(book, ensure_ascii=False, indent=1), "utf-8")
    ayahs = {(g["sure"], a) for g in girdiler for a in range(g["ayet_bas"], g["ayet_son"] + 1)}
    print(f"{code}: wrote {out.name} — {len(girdiler)} entries, {len(ayahs)} distinct ayahs, "
          f"{len({g['sure'] for g in girdiler})} surahs")


def sample(girdiler):
    for g in girdiler:
        if g["sure"] == 1 or (g["sure"] == 2 and g["ayet_bas"] <= 20):
            print(f"\n── {g['sure']}:{g['ayet_bas']}-{g['ayet_son']}  ({len(g['metin'])} chars)")
            print(g["metin"][:220].replace("\n", " ¶ "), "…", g["metin"][-80:].replace("\n", " ¶ "))


if __name__ == "__main__":
    args = sys.argv[1:] or sys.exit(__doc__)
    only_sample = args[0] == "--sample"
    quran = Quran()
    for c in [a for a in args if not a.startswith("--")]:
        cache = json.loads((CACHE_DIR / f"{c}.json").read_text("utf-8")) if only_sample else download(c)
        g = segment(c, cache, quran)
        if only_sample:
            sample(g)
            print(f"\n{c}: {len(g)} entries (sample run, nothing written)")
        else:
            write_book(c, g)

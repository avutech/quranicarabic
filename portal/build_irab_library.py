"""Build the per-ayah I'rab library index from the classical i'rab books.

Source:  Irab Kitaplari/irab_kutuphane_*.json   (local only, gitignored)
         Schema: {kod, kitap, muellif, vefat, girdiler:[{sure, ayet_bas, ayet_son, metin}]}
Output:  irab_library/books.json                 catalog (committed)
         irab_library/s001.json … s114.json      entries per surah (committed)

Each surah file is {"surah": N, "entries": [{"b": book_id, "s": first_ayah,
"e": last_ayah, "t": text}]}. An entry that covers a range of ayahs (e.g. 1:1–3)
is stored once; the client shows it for every ayah with s <= ayah <= e.

The output lives at the repo root, NOT under portal/, because portal/ is served
publicly by the catch-all static route. The server exposes it only via the
login-protected /api/irab-library endpoints.

Run:  venv/bin/python build_irab_library.py
"""

import hashlib
import html
import json
import re
import zipfile
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "Irab Kitaplari"
OUT_DIR = BASE_DIR / "irab_library"

# Display catalog, ordered chronologically by the author's death (hijri).
# `source` = json file code for books that are already digital; PDF-only
# books are listed with status "pending" until their OCR text is indexed.
CATALOG = [
    {"id": "farraa", "source": "farraa",
     "title": {"ar": "معاني القرآن", "tr": "Meâni'l-Kur'ân", "en": "Ma'ani al-Qur'an"},
     "author": {"ar": "أبو زكريا الفراء", "tr": "Ebû Zekeriyyâ el-Ferrâ", "en": "Abu Zakariyya al-Farra'"},
     "death_h": 207, "death_m": 822},
    {"id": "akhfash", "source": "akhfash",
     "title": {"ar": "معاني القرآن", "tr": "Meâni'l-Kur'ân", "en": "Ma'ani al-Qur'an"},
     "author": {"ar": "الأخفش الأوسط", "tr": "Ahfeş el-Evsat", "en": "al-Akhfash al-Awsat"},
     "death_h": 215, "death_m": 830},
    {"id": "zajjaj", "source": "zajjaj",
     "title": {"ar": "معاني القرآن وإعرابه", "tr": "Meâni'l-Kur'ân ve İ'râbuh", "en": "Ma'ani al-Qur'an wa I'rabuh"},
     "author": {"ar": "أبو إسحاق الزجاج", "tr": "Ebû İshâk ez-Zeccâc", "en": "Abu Ishaq al-Zajjaj"},
     "death_h": 311, "death_m": 923},
    {"id": "nahhas-irab", "source": "iraab-alnahas",
     "title": {"ar": "إعراب القرآن", "tr": "İ'râbü'l-Kur'ân", "en": "I'rab al-Qur'an"},
     "author": {"ar": "أبو جعفر النحاس", "tr": "Ebû Ca'fer en-Nahhâs", "en": "Abu Ja'far al-Nahhas"},
     "death_h": 338, "death_m": 950},
    {"id": "nahhas-meani", "source": "nahaas-meanings",
     "title": {"ar": "معاني القرآن", "tr": "Meâni'l-Kur'ân", "en": "Ma'ani al-Qur'an"},
     "author": {"ar": "أبو جعفر النحاس", "tr": "Ebû Ca'fer en-Nahhâs", "en": "Abu Ja'far al-Nahhas"},
     "death_h": 338, "death_m": 950},
    {"id": "mekki-muskil", "source": None,
     "title": {"ar": "مشكل إعراب القرآن", "tr": "Müşkilü İ'râbi'l-Kur'ân", "en": "Mushkil I'rab al-Qur'an"},
     "author": {"ar": "مكي بن أبي طالب القيسي", "tr": "Mekkî b. Ebû Tâlib", "en": "Makki ibn Abi Talib"},
     "death_h": 437, "death_m": 1045},
    {"id": "ukberi-tibyan", "source": None,
     "title": {"ar": "التبيان في إعراب القرآن", "tr": "et-Tibyân fî İ'râbi'l-Kur'ân", "en": "al-Tibyan fi I'rab al-Qur'an"},
     "author": {"ar": "أبو البقاء العكبري", "tr": "Ebü'l-Bekā el-Ukberî", "en": "Abu al-Baqa' al-'Ukbari"},
     "death_h": 616, "death_m": 1219},
    {"id": "celaleyn", "source": None, "kind": "tafsir", "loader": "celaleyn_docx",
     "title": {"ar": "تفسير الجلالين", "tr": "Tefsîru'l-Celâleyn", "en": "Tafsir al-Jalalayn"},
     "author": {"ar": "جلال الدين المحلي وجلال الدين السيوطي",
                "tr": "Celâleddîn el-Mahallî (ö. 864) ve Celâleddîn es-Suyûtî",
                "en": "Jalal al-Din al-Mahalli (d. 864) & Jalal al-Din al-Suyuti"},
     "death_h": 911, "death_m": 1505},
    {"id": "semin-durr", "source": "aldur-almasoon",
     "title": {"ar": "الدر المصون في علوم الكتاب المكنون", "tr": "ed-Dürrü'l-Masûn", "en": "al-Durr al-Masun"},
     "author": {"ar": "السمين الحلبي", "tr": "es-Semîn el-Halebî", "en": "al-Samin al-Halabi"},
     "death_h": 756, "death_m": 1355},
    {"id": "safi-cedvel", "source": None,
     "title": {"ar": "الجدول في إعراب القرآن", "tr": "el-Cedvel fî İ'râbi'l-Kur'ân", "en": "al-Jadwal fi I'rab al-Qur'an"},
     "author": {"ar": "محمود صافي", "tr": "Mahmûd Sâfî", "en": "Mahmud Safi"},
     "death_h": 1376, "death_m": 1956},
    {"id": "dervis-irab", "source": None,
     "title": {"ar": "إعراب القرآن وبيانه", "tr": "İ'râbu'l-Kur'ân ve Beyânuhu", "en": "I'rab al-Qur'an wa Bayanuh"},
     "author": {"ar": "محيي الدين الدرويش", "tr": "Muhyiddîn ed-Derviş", "en": "Muhyi al-Din al-Darwish"},
     "death_h": 1403, "death_m": 1982},
]

CELALEYN_DIR = BASE_DIR / "Celaleyn Arapca Sureler (Yeni Format)"
AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def load_celaleyn_docx():
    """Parse the 114 Celâleyn surah files (one .docx per surah). Each ayah is
    a paragraph "<n> – <tafsir>"; page headers "سورة … – (صفحة n)" mark the
    page within that file, kept in the per-entry reference."""
    ayah_par = re.compile(r"^\s*([٠-٩0-9]+)\s*[–-]\s*")
    page_par = re.compile(r"\(صفحة\s*([٠-٩0-9]+)\)")
    out = []
    for f in sorted(CELALEYN_DIR.glob("[0-9][0-9][0-9]_*.docx")):
        surah = int(f.name[:3])
        xml = zipfile.ZipFile(f).read("word/document.xml").decode("utf-8")
        page = None
        for i, par in enumerate(re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)):
            text = html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", par))).strip()
            if (m := page_par.search(text)) and text.startswith("سورة"):
                page = int(m.group(1).translate(AR_DIGITS))
            elif m := ayah_par.match(text):
                ayah = int(m.group(1).translate(AR_DIGITS))
                out.append({"sure": surah, "ayet_bas": ayah, "ayet_son": ayah,
                            "metin": text[m.end():],
                            "ref": {"site": "local", "file": f"{CELALEYN_DIR.name}/{f.name}",
                                    "page_in_file": page, "paragraph": i + 1}})
    return {"kaynak": "local", "girdiler": out,
            "not": "Yerel .docx sûre dosyaları (114 dosya); ayet başına bir paragraf."}


LOADERS = {"celaleyn_docx": load_celaleyn_docx}

PAGE_MARKER = re.compile(r"\(p-[٠-٩0-9]+\)")   # printed-page markers (zajjaj)
MULTISPACE = re.compile(r"[ \t]{2,}")


def clean(text: str) -> str:
    text = PAGE_MARKER.sub("", text)
    text = MULTISPACE.sub(" ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    if not SRC_DIR.is_dir():
        sys.exit(f"source folder missing: {SRC_DIR}")
    OUT_DIR.mkdir(exist_ok=True)

    by_surah = {s: [] for s in range(1, 115)}
    books_out = []
    for book in CATALOG:
        meta = {"kind": "irab", **{k: v for k, v in book.items() if k not in ("source", "loader")}}
        if book.get("loader"):
            data = LOADERS[book["loader"]]()
        elif not book["source"]:
            books_out.append({**meta, "status": "pending", "entries": 0, "ayahs": 0})
            continue
        else:
            data = json.loads((SRC_DIR / f"irab_kutuphane_{book['source']}.json").read_text("utf-8"))
        covered, n = set(), 0
        for e in data["girdiler"]:
            s, a, b = int(e["sure"]), int(e["ayet_bas"]), int(e["ayet_son"])
            text = clean(e["metin"])
            if not text or not (1 <= s <= 114) or b < a:
                continue
            # Every entry carries its own source reference so any i'rab shown
            # can be traced to the exact book, source and page it came from.
            ref = e.get("ref") or {"site": data.get("kaynak", ""), "code": book["source"],
                                   "file": f"irab_kutuphane_{book['source']}.json"}
            if ref["site"] == "tafsir.app":
                ref["url"] = f"https://tafsir.app/{book['source']}/{s}/{a}"
            by_surah[s].append({"b": book["id"], "s": a, "e": b, "t": text, "ref": ref})
            covered.update((s, x) for x in range(a, b + 1))
            n += 1
        books_out.append({**meta, "status": "ready",
                          "source": {"site": data.get("kaynak", ""), "code": book["source"] or book.get("loader"),
                                     "file": (f"irab_kutuphane_{book['source']}.json" if book["source"]
                                              else CELALEYN_DIR.name),
                                     "title_in_source": data.get("kitap", ""),
                                     "author_in_source": data.get("muellif", ""),
                                     "downloaded_at": data.get("indirilme", ""),
                                     "note": data.get("not", "")},
                          "entries": n, "ayahs": len(covered)})
        print(f"  {book['id']:14} {n:5} entries, {len(covered):5} ayahs")

    order = {b["id"]: i for i, b in enumerate(CATALOG)}
    for s, entries in by_surah.items():
        entries.sort(key=lambda x: (order[x["b"]], x["s"]))
        write_atomic(OUT_DIR / f"s{s:03d}.json",
                     json.dumps({"surah": s, "entries": entries}, ensure_ascii=False, separators=(",", ":")))
    write_atomic(OUT_DIR / "books.json", json.dumps({"books": books_out}, ensure_ascii=False, indent=1))
    total = sum(f.stat().st_size for f in OUT_DIR.glob("s*.json"))
    print(f"wrote {OUT_DIR}/ — 114 surah files, {total / 1e6:.1f} MB")
    merge_translations()


def merge_translations():
    """Merge irab_library/tr_parts/<book>/sNNN.json (written via tr_tool.py)
    into irab_library/tr/sNNN.json, the file the server reads."""
    merged, stale = {}, []
    for f in sorted((OUT_DIR / "tr_parts").glob("*/s*.json")):
        surah = int(f.stem[1:])
        sources = {f"{e['b']}:{e['s']}-{e['e']}": e["t"]
                   for e in json.loads((OUT_DIR / f.name).read_text("utf-8"))["entries"]}
        for key, reading in json.loads(f.read_text("utf-8")).items():
            if key not in sources:
                stale.append(f"{key} (s{surah}): source entry no longer exists")
                continue
            sha = hashlib.sha1(sources[key].encode("utf-8")).hexdigest()
            src = reading.get("src")
            if not src:   # saved before provenance was recorded — backfill from the key
                book, rng = key.split(":")
                first, last = (int(x) for x in rng.split("-"))
                src = {"book": book, "sure": surah, "ayet_bas": first, "ayet_son": last,
                       "sha1": sha, "backfilled": True}
            reading = {**reading, "src": src, "stale": src["sha1"] != sha}
            if reading["stale"]:
                stale.append(f"{key} (s{surah}): Arabic source changed since translation")
            merged.setdefault(f.name, {})[key] = reading
    tr_dir = OUT_DIR / "tr"
    tr_dir.mkdir(exist_ok=True)
    for name, readings in merged.items():
        write_atomic(tr_dir / name, json.dumps(readings, ensure_ascii=False, separators=(",", ":")))
    print(f"merged Turkish readings: {sum(len(r) for r in merged.values())} entries in {len(merged)} surahs")
    for msg in stale:
        print(f"  STALE {msg}")


def write_atomic(path, text):
    """Write via a temp file + rename so readers (server, tr_tool) never see a partial file."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, "utf-8")
    tmp.replace(path)


if __name__ == "__main__":
    main()

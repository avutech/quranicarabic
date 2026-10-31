"""Download an i'rab book from tafsir.app into the irab_kutuphane_*.json format.

    venv/bin/python fetch_tafsir_app.py aljadwal [more codes…]

Writes  Irab Kitaplari/irab_kutuphane_<code>.json
Schema  {kaynak, kod, kitap, muellif, vefat, not, indirilme,
         girdiler: [{sure, ayet_bas, ayet_son, metin}]}

Resumable: progress is checkpointed to <file>.partial after every surah.
Polite: one request at a time per book with a short delay. Text is stored
as delivered (including [[…]] footnotes); cleanup happens in
build_irab_library.py.
"""

import datetime as dt
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUT_DIR = Path(__file__).parent.parent / "Irab Kitaplari"
API = "https://tafsir.app/get.php"
DELAY = 0.3

# Ayah counts per surah (Hafs, 6236 total)
VERSES = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111, 110, 98, 135,
          112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53,
          89, 59, 37, 35, 38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12,
          12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19, 36, 25, 22, 17, 19, 26,
          30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6]
assert sum(VERSES) == 6236


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "learnirab-indexer/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def get(src, s, a):
    url = f"{API}?{urllib.parse.urlencode({'src': src, 's': s, 'a': a})}"
    for attempt in range(5):
        try:
            return fetch_json(url)
        except Exception as e:
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))
            print(f"  retry {s}:{a} ({e})", file=sys.stderr)


def fetch_book(code):
    sources = fetch_json("https://tafsir.app/sources/sources.json")
    meta = sources.get(code, {})
    out = OUT_DIR / f"irab_kutuphane_{code}.json"
    partial = out.with_suffix(".json.partial")
    state = json.loads(partial.read_text("utf-8")) if partial.exists() else {"done_surah": 0, "girdiler": []}

    for s in range(state["done_surah"] + 1, 115):
        a = 1
        while a <= VERSES[s - 1]:
            d = get(code, s, a)
            text = (d.get("data") or "").strip()
            if "ayahs_start" in d and d.get("ayahs"):
                start = int(d["ayahs_start"])
                end = start + len(d["ayahs"]) - 1
            else:
                start = end = a
            if text and not (state["girdiler"] and state["girdiler"][-1]["sure"] == s
                             and state["girdiler"][-1]["ayet_bas"] == start):
                state["girdiler"].append({"sure": s, "ayet_bas": start, "ayet_son": end, "metin": text})
            a = max(a, end) + 1
            time.sleep(DELAY)
        state["done_surah"] = s
        partial.write_text(json.dumps(state, ensure_ascii=False), "utf-8")
        print(f"{code}: surah {s} done ({len(state['girdiler'])} entries)", flush=True)

    book = {
        "kaynak": "tafsir.app",
        "kod": code,
        "kitap": meta.get("الاسم") or meta.get("short_name") or code,
        "muellif": meta.get("المؤلف", ""),
        "vefat": meta.get("الوفاة", ""),
        "not": "Ham metin; [[...]] dipnotları korunmuştur.",
        "indirilme": dt.datetime.now(dt.timezone.utc).isoformat(),
        "girdiler": state["girdiler"],
    }
    out.write_text(json.dumps(book, ensure_ascii=False, indent=1), "utf-8")
    partial.unlink()
    print(f"{code}: wrote {out.name} — {len(state['girdiler'])} entries")


if __name__ == "__main__":
    for c in sys.argv[1:] or sys.exit(__doc__):
        fetch_book(c)

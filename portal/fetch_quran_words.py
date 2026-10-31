"""Download word-by-word data and Turkish meals from the quran.com API.

    venv/bin/python fetch_quran_words.py

Writes  Irab Kitaplari/_kelime/qurancom.json   (local only, gitignored)
        {"meta": {...}, "meals": {id: {name, author}},
         "ayahs": {"s:a": {"t": {meal_id: text}, "w": [[arabic, translit, english], ...]}}}

Word order follows quran.com word positions (ayah-end markers dropped), which
match the Quranic Arabic Corpus word numbering used by build_irab_library.py.
"""

import datetime as dt
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent.parent / "Irab Kitaplari" / "_kelime" / "qurancom.json"
API = "https://api.quran.com/api/v4"
# Meals on quran.com: Turkish first (77 = default on the page), then English.
MEALS = [77, 52, 124, 112, 210, 20, 85]
TAG = re.compile(r"<[^>]+>")
FOOTNOTE = re.compile(r"<sup[^>]*>.*?</sup>", re.S)   # translators' footnote markers


def get(path):
    for attempt in range(5):
        try:
            req = urllib.request.Request(API + path, headers={"User-Agent": "learnirab-indexer/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if attempt == 4:
                raise
            print(f"  retry {path} ({e})", file=sys.stderr)
            time.sleep(2 * (attempt + 1))


def main():
    names = {t["id"]: {"name": t["name"], "author": t.get("author_name", ""), "lang": t.get("language_name", "")}
             for lang in ("tr", "en") for t in get(f"/resources/translations?language={lang}")["translations"]}
    meals = {str(m): names.get(m, {"name": str(m), "author": ""}) for m in MEALS}
    ayahs = {}
    for s in range(1, 115):
        page = 1
        while page:
            d = get(f"/verses/by_chapter/{s}?words=true&word_fields=text_uthmani"
                    f"&translations={','.join(map(str, MEALS))}&per_page=50&page={page}")
            for v in d["verses"]:
                words = [[w["text_uthmani"], (w.get("transliteration") or {}).get("text") or "",
                          (w.get("translation") or {}).get("text") or ""]
                         for w in v["words"] if w.get("char_type_name") == "word"]
                meal = {str(t["resource_id"]): TAG.sub("", FOOTNOTE.sub("", t["text"])).strip() for t in v.get("translations", [])}
                ayahs[v["verse_key"]] = {"t": meal, "w": words}
            page = d["pagination"].get("next_page")
            time.sleep(0.3)
        print(f"surah {s}: {sum(1 for k in ayahs if k.startswith(f'{s}:'))} ayahs", flush=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "meta": {"source": "api.quran.com/api/v4", "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                 "fields": "word text (Uthmani), transliteration, English word translation; Turkish meals"},
        "meals": meals, "ayahs": ayahs}, ensure_ascii=False), "utf-8")
    print(f"wrote {OUT} — {len(ayahs)} ayahs")


if __name__ == "__main__":
    main()

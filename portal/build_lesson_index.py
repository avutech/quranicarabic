"""
Read all 42 lesson PDFs and build a persistent grammar concept index.

Input:  portal/lessons_raw/Level-{1,2,3}__<filename>.txt   (one per PDF)
Output: portal/lessons_index.json                          (canonical, kept forever)

For each lesson, asks Claude:
  - What is the verified title (EN/TR/AR)?
  - 2-sentence summary of what it teaches
  - List of grammar concepts with Arabic+EN+TR names, keywords, examples

Run:
  cd portal
  export ANTHROPIC_API_KEY=...
  venv/bin/python build_lesson_index.py
"""

import os
import json
import re
import sys
import time
from pathlib import Path
import anthropic

ROOT = Path(__file__).parent
RAW_DIR = ROOT / "lessons_raw"
OUT_FILE = ROOT / "lessons_index.json"
CACHE_FILE = ROOT / "lessons_index_cache.json"

# Map filename → (level_id, week, current_title from data.js) so we can
# diff afterwards. We sort by level then week number parsed from filename.

WEEK_RE = re.compile(r"(\d+)(?:st|nd|rd|th)?\s+Lesson", re.IGNORECASE)

PROMPT = """You are reading a Quranic-Arabic grammar lesson and producing a structured index entry.

The text below was extracted from a PDF (formatting is broken — Arabic and Turkish/English are interleaved). Read carefully and produce a JSON object describing what this lesson teaches.

Required output (return ONLY valid JSON, no prose):
{{
  "verified_title": {{
    "en": "<the lesson's actual topic in English, concise>",
    "tr": "<the lesson's actual topic in Turkish, concise>",
    "ar": "<the lesson's actual topic in Arabic, concise>"
  }},
  "summary": "<2-3 sentences in English describing what is taught>",
  "concepts": [
    {{
      "name": {{
        "ar": "<Arabic grammar term, e.g. الإضافة>",
        "en": "<English term, e.g. Idafa (genitive construction)>",
        "tr": "<Turkish term, e.g. İsim Tamlaması>"
      }},
      "keywords": ["<lowercase English/transliterated keywords for matching, e.g. mudaf, mudaf ilayh, kasra ending, possessive>"],
      "examples": ["<short Arabic example phrase from the lesson, with diacritics>"]
    }}
  ]
}}

Guidance:
- The "verified_title" should be what THIS lesson is actually about, even if the PDF heading is generic
- Include 2-6 concepts per lesson — only the central grammar phenomena
- "keywords" must be useful for matching to a verse later (use technical terms a parser would emit: e.g. "fatha", "tanwin", "mansub", "majzum", "form II", "active participle", "broken plural")
- "examples" should be Arabic-only with diacritics, ≤30 chars each
- If the text is corrupt or non-grammatical, do your best from context

Lesson source filename: {filename}
Currently labeled in app as: {current_label}
Level: {level}, Week: {week}

Text:
---
{text}
---

Return ONLY the JSON object."""


def load_cache():
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}


def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2))


def parse_response(raw):
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start >= 0 and end > start:
            return json.loads(raw[start : end + 1])
        raise


def call_claude(client, text, filename, current_label, level, week):
    if len(text) > 25000:
        text = text[:25000]
    prompt = PROMPT.format(
        filename=filename,
        current_label=current_label,
        level=level,
        week=week,
        text=text,
    )
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    return parse_response(msg.content[0].text)


def parse_filename(stem):
    """e.g. 'Level-1__1st Lesson Line Spacing 2.0' -> (level=1, week=1)"""
    parts = stem.split("__", 1)
    level_str = parts[0].replace("Level-", "")
    level = int(level_str)
    rest = parts[1] if len(parts) > 1 else ""
    m = WEEK_RE.search(rest)
    week_in_level = int(m.group(1)) if m else 0
    # Convert lesson number to week within level
    if level == 1:
        week = week_in_level
    elif level == 2:
        week = week_in_level - 14
    elif level == 3:
        week = week_in_level - 28
    return level, week, week_in_level


def load_data_js_titles():
    """Parse current titles from data.js so we can show them in the diff."""
    data_js = (ROOT / "data.js").read_text()
    # Very simple regex grab of title objects per lesson — best effort.
    # Each lesson appears as: week: N, pdf: '...', title: { en: '...', tr: '...', ar: '...' }
    titles = {}
    pattern = re.compile(
        r"week:\s*(\d+),\s*pdf:\s*'([^']+)'.*?title:\s*\{\s*en:\s*'((?:[^'\\]|\\.)*)'\s*,\s*tr:\s*'((?:[^'\\]|\\.)*)'\s*,\s*ar:\s*'((?:[^'\\]|\\.)*)'",
        re.DOTALL,
    )
    for m in pattern.finditer(data_js):
        week = int(m.group(1))
        pdf = m.group(2)
        if pdf.startswith("Level-1/"):
            level = 1
        elif pdf.startswith("Level-2/"):
            level = 2
        else:
            level = 3
        titles[(level, week)] = {
            "en": m.group(3).replace("\\'", "'"),
            "tr": m.group(4).replace("\\'", "'"),
            "ar": m.group(5).replace("\\'", "'"),
        }
    return titles


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    cache = load_cache()
    txt_files = sorted(RAW_DIR.glob("*.txt"))

    current_titles = load_data_js_titles()
    print(f"📚 {len(txt_files)} lesson files; {len(cache)} cached; {len(current_titles)} current titles in data.js\n")

    index = {}  # key: (level, week) -> entry

    for i, txt_path in enumerate(txt_files, 1):
        stem = txt_path.stem
        level, week, lesson_no = parse_filename(stem)
        key = f"L{level}W{week}"
        current = current_titles.get((level, week), {"en": "?", "tr": "?", "ar": "?"})
        current_label = f"{current['en']} / {current['tr']}"

        if stem in cache:
            entry = cache[stem]
            print(f"[{i:2}/{len(txt_files)}] L{level}W{week:>2} (Lesson {lesson_no:>2})  cached")
        else:
            text = txt_path.read_text()
            print(f"[{i:2}/{len(txt_files)}] L{level}W{week:>2} (Lesson {lesson_no:>2})  extracting...", end=" ", flush=True)
            try:
                entry = call_claude(client, text, stem, current_label, level, week)
                print(f"✓ {len(entry.get('concepts', []))} concepts")
                cache[stem] = entry
                save_cache(cache)
                time.sleep(0.5)
            except Exception as e:
                print(f"FAILED: {e}")
                continue

        entry["level"] = level
        entry["week"] = week
        entry["lesson_id"] = key
        entry["pdf_filename"] = stem
        entry["current_title"] = current
        index[key] = entry

    # Sort by level then week
    sorted_index = dict(sorted(index.items(), key=lambda kv: (kv[1]["level"], kv[1]["week"])))

    OUT_FILE.write_text(json.dumps(sorted_index, ensure_ascii=False, indent=2))
    print(f"\n✅ Wrote {OUT_FILE} ({len(sorted_index)} lessons)")

    # Print diff report
    print("\n" + "=" * 100)
    print("TITLE DIFF (PDF-derived vs current data.js):")
    print("=" * 100)
    print(f"{'Lesson':<10} {'Match':<8} {'Current (EN)':<45} {'PDF says (EN)':<45}")
    print("-" * 100)
    matches = 0
    for key, entry in sorted_index.items():
        cur_en = entry.get("current_title", {}).get("en", "?")
        new_en = entry.get("verified_title", {}).get("en", "?")
        same = cur_en.strip().lower() == new_en.strip().lower()
        if same:
            matches += 1
        marker = "✅" if same else "⚠️"
        print(f"{key:<10} {marker:<8} {cur_en[:43]:<45} {new_en[:43]:<45}")
    print(f"\n{matches}/{len(sorted_index)} titles match exactly.")
    print(f"Full PDF-derived index saved to {OUT_FILE.name} (always preserved).")


if __name__ == "__main__":
    main()

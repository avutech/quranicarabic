"""
Translate all practice questions in data.js from English-only to multilingual.

Reads data.js, finds every `{ type: '...', q: '...', expected: '...' }` block
inside a lesson's questions array, and rewrites them as:
  { type: '...', q: {en, tr, ar}, expected: {en, tr, ar} }

Uses Gemini Flash for translation (~$0.05 total).
Idempotent: skips questions whose `q` is already an object.

Run:
  cd portal
  venv/bin/python translate_questions.py     # picks up GEMINI_API_KEY from .env
"""

import os
import re
import json
import sys
from pathlib import Path
from google import genai
from google.genai import types as genai_types

ROOT = Path(__file__).parent
DATA_JS = ROOT / "data.js"
ENV_FILE = ROOT / ".env"


def load_env():
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def js_quote(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


# ---- Find question blocks where `q` is still a plain string -----------------
# Matches:  { type: 'grammar', q: 'What is X?', expected: 'Y' }
QUESTION_RE = re.compile(
    r"\{\s*type:\s*'([^']+)'\s*,\s*q:\s*'((?:[^'\\]|\\.)*)'\s*,\s*expected:\s*'((?:[^'\\]|\\.)*)'\s*\}",
    re.DOTALL,
)


def main():
    load_env()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set (check portal/.env)", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    text = DATA_JS.read_text()
    matches = list(QUESTION_RE.finditer(text))
    print(f"Found {len(matches)} plain-English question blocks to translate.")

    if not matches:
        print("Nothing to do — all questions already multilingual.")
        return

    # Collect unique question/expected pairs
    items = []
    for m in matches:
        q = m.group(2).encode().decode("unicode_escape") if "\\" in m.group(2) else m.group(2)
        e = m.group(3).encode().decode("unicode_escape") if "\\" in m.group(3) else m.group(3)
        items.append({"q_en": q, "e_en": e})

    # Batch translate, ~25 items per call
    translations = {}
    BATCH = 25
    for i in range(0, len(items), BATCH):
        batch = items[i : i + BATCH]
        prompt = (
            "Translate the following Quranic-Arabic learning practice questions and reference answers "
            "from English into Turkish AND Arabic. Keep all Arabic terms (e.g. أَلِف, مُسْلِمٌ) intact and unchanged. "
            "Return strict JSON: an array of objects { tr_q, ar_q, tr_e, ar_e } in the same order as the input.\n\n"
            f"Input ({len(batch)} items):\n{json.dumps(batch, ensure_ascii=False)}\n\n"
            "Return ONLY the JSON array."
        )
        print(f"  translating batch {i // BATCH + 1} ({len(batch)} items)...", end=" ", flush=True)
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=15000,
            ),
        )
        try:
            arr = json.loads(resp.text or "[]")
        except json.JSONDecodeError:
            print("FAILED parse")
            continue
        if len(arr) != len(batch):
            print(f"⚠️  got {len(arr)} translations for {len(batch)} items — skipping batch")
            continue
        for src, tgt in zip(batch, arr):
            translations[(src["q_en"], src["e_en"])] = tgt
        print("✓")

    print(f"Got {len(translations)} translation pairs. Rewriting data.js...")

    # Rewrite each question in data.js
    def replacer(m):
        type_ = m.group(1)
        q_en = m.group(2).encode().decode("unicode_escape") if "\\" in m.group(2) else m.group(2)
        e_en = m.group(3).encode().decode("unicode_escape") if "\\" in m.group(3) else m.group(3)
        tgt = translations.get((q_en, e_en))
        if not tgt:
            return m.group(0)  # unchanged if translation missing
        return (
            "{ type: '" + js_quote(type_) + "', "
            "q: { en: '" + js_quote(q_en) + "', "
            "tr: '" + js_quote(tgt.get("tr_q", q_en)) + "', "
            "ar: '" + js_quote(tgt.get("ar_q", q_en)) + "' }, "
            "expected: { en: '" + js_quote(e_en) + "', "
            "tr: '" + js_quote(tgt.get("tr_e", e_en)) + "', "
            "ar: '" + js_quote(tgt.get("ar_e", e_en)) + "' } }"
        )

    new_text = QUESTION_RE.sub(replacer, text)
    DATA_JS.write_text(new_text)
    print(f"✅ Updated data.js — {len(translations)} questions now multilingual.")


if __name__ == "__main__":
    main()

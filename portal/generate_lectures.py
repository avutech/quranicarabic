#!/usr/bin/env python3
"""Generate multilingual `lecture` content for every lesson except L1W1
(which is hand-authored as the canonical style reference). Output:
portal/lectures.json keyed by lesson_id (e.g. "L1W2").

Re-runnable: existing entries in lectures.json are kept; only missing
lesson_ids are filled in. Stop and rerun any time.

Usage:
    cd portal
    venv/bin/python generate_lectures.py            # generate all missing
    venv/bin/python generate_lectures.py L2W3       # generate just one
    venv/bin/python generate_lectures.py --force    # regenerate all
"""
import json
import os
import sys
import time
from pathlib import Path

PORTAL_DIR = Path(__file__).parent
LESSONS_INDEX = PORTAL_DIR / "lessons_index.json"
OUT_FILE = PORTAL_DIR / "lectures.json"
ENV_FILE = PORTAL_DIR / ".env"

# Pull GEMINI_API_KEY out of .env if needed
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v

import anthropic

CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# The hand-authored L1W1 lecture — used as a style reference in the prompt
L1W1_REFERENCE = {
    "sections": [
        {
            "title": {
                "en": "Why classify words?",
                "tr": "Kelimeleri neden sınıflandırırız?",
                "ar": "لماذا نصنّف الكلمات؟"
            },
            "body": {
                "en": "Classical Arabic grammar — and therefore the language of the Qur'an — divides every word into exactly **three categories** (أقسام الكلمة)…",
                "tr": "Klasik Arapça gramer — ve dolayısıyla Kur'an'ın dili — her kelimeyi tam olarak **üç kategoriye** (أقسام الكلمة) ayırır…",
                "ar": "يقسّم النحو الكلاسيكي — وبذلك لغة القرآن الكريم — كل كلمة إلى **ثلاث فئات** (أقسام الكلمة)…"
            }
        },
        {
            "title": {
                "en": "الاسم — The Noun (Ism)",
                "tr": "الاسم — İsim",
                "ar": "الاسم"
            },
            "body": {
                "en": "An **ism** names a person, place, thing, idea, or quality… **How to recognize an ism:**\n- It can carry tanwīn\n- It can carry the definite article **ال**\n- …",
                "tr": "**İsim**, bir kişiyi, yeri, şeyi, kavramı veya niteliği adlandırır… **İsmi tanıma yolları:**\n- Tenvin alabilir\n- Belirlilik takısı **ال** alabilir\n- …",
                "ar": "**الاسم** يدلّ على شخص أو مكان… **علامات الاسم:**\n- يقبل التنوين\n- يقبل **ال** التعريف\n- …"
            },
            "examples": [
                {"ar": "مُحَمَّدٌ", "gloss": {"en": "Muhammad (a name)", "tr": "Muhammed (özel ad)", "ar": "اسم علم"}},
                {"ar": "كِتَابٌ", "gloss": {"en": "a book", "tr": "bir kitap", "ar": "كتاب"}}
            ]
        }
    ]
}


def build_prompt(lesson_id, lesson):
    """Build the Gemini prompt for one lesson."""
    title_en = lesson["verified_title"].get("en", "")
    title_tr = lesson["verified_title"].get("tr", "")
    title_ar = lesson["verified_title"].get("ar", "")
    summary = lesson.get("summary", "")
    concepts = lesson.get("concepts", [])

    concept_block = "\n".join(
        f"- **{c['name'].get('en','?')}** ({c['name'].get('ar','')}): "
        f"keywords [{', '.join(c.get('keywords', []))}]; "
        f"seed examples [{', '.join(c.get('examples', []))}]"
        for c in concepts
    )

    return f"""You are an expert Quranic Arabic grammar teacher writing a multilingual study lecture for a self-study portal. The student selects their language; you must produce content fluently in **English, Turkish, AND Arabic** so that flipping the language toggle gives a native-feeling explanation.

## LESSON TO COVER
- **Lesson ID:** {lesson_id}
- **Title (EN):** {title_en}
- **Title (TR):** {title_tr}
- **Title (AR):** {title_ar}
- **Summary:** {summary}

### Concepts in this lesson
{concept_block}

## STYLE REFERENCE (this is the lecture for L1W1; match its tone, depth, and structure)

```json
{json.dumps(L1W1_REFERENCE, ensure_ascii=False, indent=2)}
```

## OUTPUT — return ONLY valid JSON matching this schema:

{{
  "sections": [
    {{
      "title": {{ "en": "...", "tr": "...", "ar": "..." }},
      "body":  {{ "en": "<markdown allowed: **bold**, bullet lists with `- `, blank lines for paragraphs>",
                  "tr": "<same>",
                  "ar": "<same, written naturally in Arabic>" }},
      "examples": [
        {{ "ar": "<short Arabic example>", "gloss": {{ "en": "...", "tr": "...", "ar": "..." }} }}
      ]
    }}
  ]
}}

## RULES — MANDATORY

1. **3 to 5 sections per lecture.** First section is an intro / motivation; final section is an applied recognition exercise that uses one or more real Quranic phrases (where natural).
2. **All three languages every time.** Each `title` and `body` MUST have `en`, `tr`, and `ar` keys filled with substantive native-quality content (not machine-translated stubs).
3. **Preserve Arabic tokens** — Quranic words, names of grammar concepts (الاسم, مبتدأ, etc.), and example phrases stay in Arabic script regardless of the surrounding language. Inline transliteration in parentheses is welcome the first time a term appears.
4. **Examples are MANDATORY.** Every section that introduces a grammatical concept, paradigm, pattern, or recognition exercise MUST include **3–6 example cards** in the `examples` array. The only sections allowed to have an empty `examples` array are pure-recap/intro sections that explicitly do not introduce a concept. **At minimum 3 of your sections must have examples.** Each example: short Arabic word/phrase plus a brief gloss in all three languages. DO NOT bury all examples in the body prose — they belong in the structured `examples` array so the UI can render them as visual cards.
5. **Plain teaching tone** — clear, second-person, encouraging. Avoid academic stiffness.
6. **Use markdown lightly.** `**bold**` for terms, `- ` bullets for lists. Do NOT include section headings inside `body`; the section's `title` already prints above it.
7. **Length:** each `body` should be roughly 80–180 words in each language (don't pad).
8. Quranic example phrases, where used, should be authentic and recognizable.

NOW produce the lecture for **{lesson_id} — {title_en}**.
"""


def generate(lesson_id, lesson, retries=2):
    prompt = build_prompt(lesson_id, lesson)
    raw = ""
    for attempt in range(retries + 1):
        try:
            resp = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=16000,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
            if not raw:
                raise RuntimeError("empty response")
            # Claude doesn't have response_mime_type — strip ```json fences if present
            if raw.startswith("```"):
                raw = raw.strip("`").lstrip("json").strip()
            return json.loads(raw)
        except json.JSONDecodeError:
            start, end = raw.find("{"), raw.rfind("}")
            if start >= 0 and end > start:
                try:
                    return json.loads(raw[start:end + 1])
                except json.JSONDecodeError:
                    pass
            if attempt == retries:
                raise
        except anthropic.RateLimitError as e:
            wait = 30
            print(f"  ⏳  rate-limited, sleeping {wait}s …", flush=True)
            time.sleep(wait)
            continue
        except Exception:
            if attempt == retries:
                raise
            time.sleep(3)
    raise RuntimeError(f"failed after {retries} retries")


def main():
    args = sys.argv[1:]
    force = "--force" in args
    explicit = [a for a in args if not a.startswith("--")]

    index = json.loads(LESSONS_INDEX.read_text())
    out = json.loads(OUT_FILE.read_text()) if OUT_FILE.exists() else {}

    # Always skip L1W1 — hand-authored in data.js
    targets = []
    for lid, lesson in sorted(index.items(), key=lambda kv: (kv[1].get("level", 0), kv[1].get("week", 0))):
        if explicit and lid not in explicit:
            continue
        if lid == "L1W1":
            continue
        if lid in out and not force:
            continue
        targets.append((lid, lesson))

    print(f"Generating {len(targets)} lectures (model: {CLAUDE_MODEL})…", flush=True)
    for i, (lid, lesson) in enumerate(targets, 1):
        title = lesson["verified_title"].get("en", "?")
        print(f"[{i}/{len(targets)}] {lid} — {title}", flush=True)
        try:
            data = generate(lid, lesson)
            out[lid] = data
            # write incrementally so we can resume from a crash
            OUT_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2))
            sections = len(data.get("sections", []))
            print(f"   ✓ {sections} sections", flush=True)
        except Exception as e:
            print(f"   ✗ {e}", flush=True)
            continue
        # gentle pacing — flash-lite has 30 RPM on free tier
        time.sleep(2)

    print(f"\nAll done. lectures.json now has {len(out)} entries.", flush=True)


if __name__ == "__main__":
    main()

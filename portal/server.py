import os
import sys
import json
import re
from pathlib import Path
from flask import Flask, send_from_directory, request, jsonify, abort
from google import genai
from google.genai import types as genai_types


def humanize_gemini_error(exc):
    """Turn raw Gemini SDK errors (especially 429s) into clear user-facing
    messages. Returns (status_code, message) — message is plain text the
    frontend can show directly."""
    msg = str(exc)
    # Quota / rate-limit error
    if "RESOURCE_EXHAUSTED" in msg or "429" in msg or "quota" in msg.lower():
        # Extract the retry-after seconds if present
        retry_match = re.search(r"retry in (\d+(?:\.\d+)?)\s*s", msg, re.IGNORECASE)
        if not retry_match:
            retry_match = re.search(r"'retryDelay':\s*'(\d+)s'", msg)
        if retry_match:
            secs = int(float(retry_match.group(1))) + 1
            mins = secs // 60
            human_wait = f"about {mins} minute{'s' if mins != 1 else ''}" if mins >= 1 else f"{secs} seconds"
            return 429, (
                f"⏳ Gemini's free-tier rate limit reached. Please wait {human_wait} and try again.\n\n"
                "The free tier allows ~10–20 requests per minute. To remove this limit entirely, "
                "enable billing at https://aistudio.google.com/apikey (Gemini Flash costs ~$0.001 per analysis)."
            )
        return 429, (
            "⏳ Gemini's free-tier daily quota reached. Please try again in a few minutes.\n\n"
            "To remove this limit, enable billing at https://aistudio.google.com/apikey "
            "(Gemini Flash costs ~$0.001 per analysis — very cheap)."
        )
    # Auth error
    if "401" in msg or "API key" in msg or "invalid x-api-key" in msg.lower():
        return 401, "❌ Your GEMINI_API_KEY is invalid or expired. Update it in portal/.env and restart the server."
    # Generic
    return 500, str(exc)

app = Flask(__name__)

BASE_DIR = Path(__file__).parent.parent
PDF_DIR = BASE_DIR / "Kuran-Kerim Arapcasi"
PORTAL_DIR = Path(__file__).parent
LESSONS_INDEX_FILE = PORTAL_DIR / "lessons_index.json"
ENV_FILE = PORTAL_DIR / ".env"


def load_env_file():
    """If portal/.env exists and ANTHROPIC_API_KEY isn't already set, read it
    from there. File format: KEY=value (one per line, # for comments)."""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


load_env_file()


def load_lessons_index():
    """Load the PDF-derived 42-lesson concept index, return a compact summary
    string suitable for inclusion in the i'rab prompt."""
    if not LESSONS_INDEX_FILE.exists():
        return None, ""
    data = json.loads(LESSONS_INDEX_FILE.read_text())
    lines = []
    for key, entry in data.items():
        title = entry.get("verified_title", {}).get("en", "?")
        concepts = entry.get("concepts", [])
        concept_strs = []
        for c in concepts:
            name = c.get("name", {}).get("en", "?")
            kws = c.get("keywords", [])
            concept_strs.append(f"{name} [{', '.join(kws)}]")
        lines.append(f"  {key} (Level {entry['level']} Week {entry['week']}): {title} — {'; '.join(concept_strs)}")
    return data, "\n".join(lines)


LESSONS_INDEX, LESSONS_INDEX_SUMMARY = load_lessons_index()


@app.route("/")
def index():
    return send_from_directory(str(PORTAL_DIR), "index.html")


@app.route("/pdfs/<path:filename>")
def serve_pdf(filename):
    try:
        return send_from_directory(str(PDF_DIR), filename)
    except Exception:
        abort(404)


@app.route("/<path:filename>")
def static_files(filename):
    try:
        return send_from_directory(str(PORTAL_DIR), filename)
    except Exception:
        abort(404)


@app.route("/api/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    question = data.get("question", "")
    user_answer = data.get("answer", "")
    expected = data.get("expected", "")
    topic = data.get("topic", "")
    language = data.get("language", "en")

    lang_names = {"en": "English", "tr": "Turkish", "ar": "Arabic"}
    response_lang = lang_names.get(language, "English")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY environment variable is not set"}), 500

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""You are a Quranic Arabic language teacher evaluating a student's answer.

Topic: {topic}
Question: {question}
Expected Answer (reference): {expected}
Student's Answer: {user_answer}

Respond in {response_lang}. Keep it to 4–6 sentences max.

Format your response:
- Start with one of: ✅ Correct! / ⚠️ Partially Correct / ❌ Not Quite
- If wrong or partial: explain the grammatical rule or reasoning clearly
- Give the correct answer with explanation
- Be warm and encouraging
- When referencing Arabic words, always include Arabic script with transliteration"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai_types.GenerateContentConfig(max_output_tokens=600),
        )
        return jsonify({"feedback": response.text or ""})

    except Exception as e:
        code, friendly = humanize_gemini_error(e)
        return jsonify({"error": friendly}), code


@app.route("/api/irab", methods=["POST"])
def irab():
    data = request.get_json() or {}
    verse = (data.get("verse") or "").strip()
    language = data.get("language", "en")
    if not verse:
        return jsonify({"error": "No verse provided"}), 400

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY environment variable is not set"}), 500
    if LESSONS_INDEX is None:
        return jsonify({"error": "lessons_index.json not found — run build_lesson_index.py first"}), 500

    lang_names = {"en": "English", "tr": "Turkish", "ar": "Arabic"}
    response_lang = lang_names.get(language, "English")

    prompt = f"""You are an expert in Quranic Arabic grammar. Analyze Quranic verses word-by-word and return a JSON array. Each element represents one word/particle.

## LANGUAGE — CRITICAL

ALL human-readable text fields MUST be written in **{response_lang}**. This applies to:
- `meaning` (full word meaning)
- `notes` (grammar notes)
- `role` (the descriptive English-style label part — translate the English gloss; keep transliterated Arabic terms in parens unchanged)
- every `reason` inside `lesson_refs`

Technical Arabic grammar terms in transliteration (e.g. "marfu'", "harf jarr", "ism fa'il", "Form II", "fa'il", "mubtada", "khabar", "mawsul", "mudaf") stay UNCHANGED — they are universal terminology. Only translate the English/explanatory wording around them.

Examples for `role` if {response_lang} is Turkish:
  English form:  "Relative pronoun (Mawsul) — mubtada"
  Turkish form:  "İsm-i Mevsul — mubtada"
  English form:  "Subject (fa'il)"
  Turkish form:  "Özne (fa'il)"
  English form:  "Direct object (maf'ul bih)"
  Turkish form:  "Düz tümleç (maf'ul bih)"

Examples for `role` if {response_lang} is Arabic:
  English form:  "Subject (fa'il)"
  Arabic form:   "الفاعل"
  English form:  "Direct object (maf'ul bih)"
  Arabic form:   "المفعول به"

If {response_lang} is English: keep everything as the role rules describe below.

## OUTPUT

Return ONLY a valid JSON array. No prose, no markdown, no explanation outside the array.

## JSON SCHEMA (one object per word)

{{
  "word": "Arabic word as it appears in the verse",
  "transliteration": "romanized transliteration",
  "meaning": "{response_lang} meaning (concise)",
  "type": "fi'l | ism | harf",
  "root": "Arabic root letters (e.g. ك ف ر) — null if none",
  "form": "morphological form — see rules below",
  "case_mood": "grammatical case or verb mood — see rules below",
  "role": "syntactic role in the sentence — see rules below",
  "notes": "any critical grammar rule, exception, or scholarly disagreement — null if none",
  "lesson_refs": [
    {{ "lesson_id": "<exact lesson_id from the curriculum index below>", "reason": "<one short sentence in {response_lang} explaining why this lesson applies>" }}
  ]
}}

## FIELD RULES

### type
- "fi'l" — any verb (madi, mudari, amr, passive)
- "ism" — any noun, adjective, pronoun, relative pronoun, demonstrative, participle, masdar
- "harf" — any particle (preposition, conjunction, negation, interrogative, etc.)

### form (examples by type)
For fi'l:
  "Form I, madi" / "Form I, mudari, marfu'" / "Form IV, amr" / "Form VII, madi, passive"
  Always include: Form number (I–X) + tense/mode + passive if applicable
  For defective/hollow/doubled roots add: "Form I, madi (naqis ya'i)" etc.

For ism:
  "ism fa'il, Form IV" / "ism maf'ul, Form I" / "masdar, Form II"
  "sifa mushabbaha (fa'il)" / "siga mubalaġa (fa'ul)" / "ism tafḍil"
  "jam' mudhakkar salim" / "jam' mu'annas salim" / "jam' mukassar"
  "muntaha al-jumu' (ghayr munsarif)" / "ism maqsur" / "ism mamdud"
  "asma' al-khamsa (abi/akhi/hami/fami/dhi)"
  For pronouns: "mutasil damir" / "munfasil damir"
  For particles used as nouns: describe accordingly

For harf:
  Describe function: "harf jarr" / "harf 'atf (ta'qib)" / "harf nafi" / "harf nahi" /
  "harf tawkid wa nasb (inna)" / "harf shart jazim" / "harf masdariyya wa nasb" etc.

### case_mood
For nouns/adjectives:
  "marfu'" / "mansub" / "majrur"
  Add how: "marfu' (damma)" / "mansub (fatha)" / "majrur (kasra)"
  For irregular: "marfu' (waw) — jam' mudhakkar salim" / "mansub/majrur (ya) — jam' mudhakkar salim"
  For ghayr munsarif: "majrur (fatha) — ghayr munsarif"
  For maqsur/mamdud: "marfu' (muqaddar)"
  For indeclinables: "mabni 'ala al-fath / damm / kasr / sukun, fi mahall ___"

For verbs:
  "marfu' (damma)" / "mansub (fatha)" / "majzum (sukun)" / "majzum (hazf nun)"
  "mabni 'ala al-fath (madi)" / "mabni 'ala al-sukun (amr)"
  For passive: add "passive — na'ib fa'il: ___"

For particles:
  "mabni" or null

### role
Use concise English labels:
  Subject (fa'il) | Doer (fa'il) | Subject of kana | Predicate | Predicate of kana
  Direct object (maf'ul bih) | Second object | Substitute object (na'ib fa'il)
  Adjective (sifa) | Appositive (badal) | Emphasis (tawkid) | Conjunction (ma'tuf)
  Hal (circumstantial acc.) | Tamyiz (specification) | Maf'ul mutlaq | Maf'ul lah | Maf'ul fih
  Mudaf | Mudaf ilayhi | Prepositional phrase (jar-majrur) | Linked to verb/noun (muta'alliq)
  Subject of relative clause (sila) | Conditional verb | Conditional response (jawab shart)
  Oath object (muqsam bih) | Predicate (khabar muqaddam) | Delayed subject (mubtada muakhkhar)
  Conjunction (harf) | Negation particle | Interrogative | Vocative | Response to negation (ijab)
  Relative pronoun | Demonstrative | Attached pronoun — object | Attached pronoun — possessive

### notes
**WRITE THE EXPLANATORY PROSE IN {response_lang}** — only the transliterated Arabic terms stay unchanged.
Include ONLY genuinely important grammar points that a learner needs:
- Irregular morphology
- Scholarly ikhtilaaf
- Hidden/implied elements
- Unusual i'rab
- Ghayr munsarif reasons
- Emphasis/rhetorical function affecting grammar
- Ta'liq, sedd al-masad, iltiqaa al-sakinayn, fakk al-idgham
- Qira'at variants that change i'rab
- null if nothing critical to add

Examples of well-written notes in different languages (same content):
  English: "Hollow verb: waw → ya in passive (qawala → qila)."
  Turkish: "İçi boş fiil (ecvef): mechul yapıda waw → ya'ya dönüşür (qawala → qila)."
  Arabic:  "فعل أجوف: تنقلب الواو ياءً في المجهول (قَوَلَ → قِيلَ)."

### lesson_refs
- Reference ONLY `lesson_id` values that appear in the curriculum index below — never invent IDs.
- 0–3 entries per word. Pick the lessons that most directly explain THIS word's grammar phenomenon.
- Empty array if no lesson clearly applies.

## CURRICULUM INDEX

Use these exact `lesson_id` strings only:

{LESSONS_INDEX_SUMMARY}

## IMPORTANT RULES

1. Every word in the verse gets its own object — particles (wa, fa, la, ma, in etc.) included.
2. For attached pronouns that are part of a word (e.g. هُمْ in أَعْمَالَهُمْ), analyze the full word as one object AND note the pronoun's role in the notes field. Do NOT split them into separate objects unless the pronoun is a clear standalone clitic.
3. For inna/anna and sisters: the word itself is "harf"; its attached pronoun (إِنَّهُ) gets analyzed as one unit with notes explaining the ism of inna.
4. Keep all field values SHORT — no full sentences except in notes.
5. "form" field is null for pure particles (prepositions, conjunctions, negations) that have no morphological derivation.
6. Always return the Arabic word exactly as it appears in the verse (with full diacritics if provided).

## EXAMPLE

Input verse: وَصَدُّواْ عَن سَبِيلِ ٱللَّهِ

Output:
[
  {{
    "word": "وَ",
    "transliteration": "wa",
    "meaning": "and",
    "type": "harf",
    "root": null,
    "form": null,
    "case_mood": "mabni",
    "role": "Conjunction",
    "notes": null,
    "lesson_refs": []
  }},
  {{
    "word": "صَدُّواْ",
    "transliteration": "ṣaddū",
    "meaning": "they hindered / turned away",
    "type": "fi'l",
    "root": "ص د د",
    "form": "Form II, madi (mudha'af)",
    "case_mood": "mabni 'ala al-damm (jam' waw)",
    "role": "Main verb — subject implied (hum)",
    "notes": "Mudha'af root: idgham obligatory in madi. Form II intensifies: repeated obstruction",
    "lesson_refs": [
      {{ "lesson_id": "L1W13", "reason": "Past tense (madi) verb conjugation" }},
      {{ "lesson_id": "L3W13", "reason": "Form II augmented verb pattern" }}
    ]
  }},
  {{
    "word": "عَن",
    "transliteration": "'an",
    "meaning": "from / about",
    "type": "harf",
    "root": null,
    "form": "harf jarr",
    "case_mood": "mabni",
    "role": "Preposition",
    "notes": null,
    "lesson_refs": [
      {{ "lesson_id": "L1W8", "reason": "Preposition (harf al-jarr) governs following noun in genitive" }}
    ]
  }},
  {{
    "word": "سَبِيلِ",
    "transliteration": "sabīli",
    "meaning": "path",
    "type": "ism",
    "root": "س ب ل",
    "form": "ism (fa'il pattern — sifa mushabaha)",
    "case_mood": "majrur (kasra) — first noun in idafa",
    "role": "Mudaf ilayhi (of 'an) — Mudaf",
    "notes": null,
    "lesson_refs": [
      {{ "lesson_id": "L1W4", "reason": "First term of an idafa (genitive construction)" }}
    ]
  }},
  {{
    "word": "ٱللَّهِ",
    "transliteration": "allāhi",
    "meaning": "Allah",
    "type": "ism",
    "root": "أ ل ه",
    "form": "proper noun ('alam)",
    "case_mood": "majrur (kasra)",
    "role": "Mudaf ilayhi",
    "notes": null,
    "lesson_refs": [
      {{ "lesson_id": "L1W4", "reason": "Second term of an idafa takes genitive case" }}
    ]
  }}
]

## VERSE TO ANALYZE

{verse}

## FINAL REMINDER

Write `meaning`, `notes`, `role` (the descriptive prose), and every `lesson_refs[].reason` in **{response_lang}**. The example above happens to be in English to illustrate the schema — DO NOT copy its language. If {response_lang} is Turkish, write Turkish. If Arabic, write Arabic. If English, write English. Transliterated Arabic technical terms (fa'il, mubtada, marfu', mansub, idafa, etc.) and Arabic script in parentheses stay unchanged."""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=8000,
            ),
        )
        raw = (response.text or "").strip()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            # Fallback: locate JSON array or object bounds in case of extra text
            for open_ch, close_ch in (("[", "]"), ("{", "}")):
                start = raw.find(open_ch)
                end = raw.rfind(close_ch)
                if start >= 0 and end > start:
                    try:
                        payload = json.loads(raw[start : end + 1])
                        break
                    except json.JSONDecodeError:
                        continue
            else:
                return jsonify({"error": "Could not parse model output as JSON", "raw": raw[:500]}), 500
        # Normalize: prompt returns a top-level array; wrap it for the frontend
        if isinstance(payload, list):
            payload = {"words": payload}
        return jsonify(payload)
    except Exception as e:
        code, friendly = humanize_gemini_error(e)
        return jsonify({"error": friendly}), code


if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: GEMINI_API_KEY is not set. Practice feedback and i'rab will not work.")
        print("   Add it to portal/.env as: GEMINI_API_KEY=your_key_here")
    print(f"📂 PDF directory: {PDF_DIR}")
    print(f"🌐 Portal running at: http://localhost:8081")
    app.run(port=8081, debug=False)

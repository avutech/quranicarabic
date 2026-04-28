import os
import sys
import json
from pathlib import Path
from flask import Flask, send_from_directory, request, jsonify, abort
import anthropic

app = Flask(__name__)

BASE_DIR = Path(__file__).parent.parent
PDF_DIR = BASE_DIR / "Kuran-Kerim Arapcasi"
PORTAL_DIR = Path(__file__).parent
LESSONS_INDEX_FILE = PORTAL_DIR / "lessons_index.json"


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

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY environment variable is not set"}), 500

    try:
        client = anthropic.Anthropic(api_key=api_key)

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

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        return jsonify({"feedback": message.content[0].text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/irab", methods=["POST"])
def irab():
    data = request.get_json() or {}
    verse = (data.get("verse") or "").strip()
    language = data.get("language", "en")
    if not verse:
        return jsonify({"error": "No verse provided"}), 400

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY environment variable is not set"}), 500
    if LESSONS_INDEX is None:
        return jsonify({"error": "lessons_index.json not found — run build_lesson_index.py first"}), 500

    lang_names = {"en": "English", "tr": "Turkish", "ar": "Arabic"}
    response_lang = lang_names.get(language, "English")

    prompt = f"""You are a Quranic-Arabic grammar analyst.

Below is the user's verse / phrase. Produce a strict-JSON i'rab (grammatical analysis) word by word.

For every word, identify which lessons in OUR 42-lesson curriculum cover the grammar phenomenon at play. Reference lessons ONLY by their `lesson_id` from the index below. Do not invent lesson IDs.

Curriculum index (`lesson_id`: title — concepts):
{LESSONS_INDEX_SUMMARY}

User's text: {verse}

Respond in {response_lang} for human-readable fields. Return ONLY valid JSON in this exact shape:

{{
  "translation": "<full meaning of the verse in {response_lang}, 1-2 sentences>",
  "words": [
    {{
      "ar": "<the word with diacritics>",
      "transliteration": "<latin transliteration>",
      "meaning": "<this word's meaning in {response_lang}>",
      "type": "<ism | fi'l | harf>",
      "root": "<3-letter root if applicable, else empty>",
      "case_mood": "<e.g. marfu' (nominative), mansub (accusative), majzum (jussive), or null>",
      "role": "<short syntactic role: e.g. mubtada, khabar, mudaf, fa'il, maf'ul bih, harf jarr, harf nasb...>",
      "form": "<for verbs: Form I-X, past/present/imperative; or null>",
      "lesson_refs": [
        {{ "lesson_id": "<L_W_>", "reason": "<one sentence in {response_lang} explaining why this lesson applies>" }}
      ]
    }}
  ],
  "overall_notes": "<optional 1-2 sentence note about sentence structure, in {response_lang}>"
}}

Be terse but precise. If a word's role spans multiple lessons (e.g. مَا types, إنَّ + accusative), include up to 3 lesson_refs."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        # Strip code fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            if raw.endswith("```"):
                raw = raw.rsplit("\n", 1)[0]
            raw = raw.replace("```json", "").replace("```", "").strip()
        # Find JSON object bounds
        start = raw.find("{")
        end = raw.rfind("}")
        if start >= 0 and end > start:
            raw = raw[start : end + 1]
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as je:
            return jsonify({"error": f"Could not parse model output as JSON: {je}", "raw": raw[:500]}), 500
        return jsonify(payload)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  WARNING: ANTHROPIC_API_KEY is not set. Practice feedback will not work.")
        print("   Set it with: export ANTHROPIC_API_KEY=your_key_here")
    print(f"📂 PDF directory: {PDF_DIR}")
    print(f"🌐 Portal running at: http://localhost:8081")
    app.run(port=8081, debug=False)

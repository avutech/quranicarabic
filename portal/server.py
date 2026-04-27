import os
import sys
from pathlib import Path
from flask import Flask, send_from_directory, request, jsonify, abort
import anthropic

app = Flask(__name__)

BASE_DIR = Path(__file__).parent.parent
PDF_DIR = BASE_DIR / "Kuran-Kerim Arapcasi"
PORTAL_DIR = Path(__file__).parent


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


if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  WARNING: ANTHROPIC_API_KEY is not set. Practice feedback will not work.")
        print("   Set it with: export ANTHROPIC_API_KEY=your_key_here")
    print(f"📂 PDF directory: {PDF_DIR}")
    print(f"🌐 Portal running at: http://localhost:8081")
    app.run(port=8081, debug=False)

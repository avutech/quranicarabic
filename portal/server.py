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

# Model selection — overridable via .env
# Free tier limits per model (AI Studio, no billing):
#   gemini-2.5-flash       : 10 RPM, 250 RPD   (best quality)
#   gemini-2.5-flash-lite  : 30 RPM, 1500 RPD  (good quality, much higher free quota)
#   gemini-2.5-pro         : 5  RPM, 100 RPD   (highest quality, paid recommended)
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")


# Shared i'rab field-rule reference — injected into both /api/irab and
# /api/self-check so the "correct" analysis follows the same standardized
# vocabulary in both places.
IRAB_FIELD_RULES = """### type
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

For particles: "mabni" or null

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
Include ONLY genuinely important grammar points that a learner needs:
- Irregular morphology (e.g. "Hollow verb: waw > ya in passive")
- Scholarly ikhtilaaf
- Hidden/implied elements (e.g. "Subject pronoun hum implied in verb")
- Unusual i'rab (e.g. "la nafiya lil-jins: ism mabni 'ala al-fath")
- Ghayr munsarif reason
- Emphasis/rhetorical function affecting grammar
- Ta'liq, sedd al-masad, iltiqaa al-sakinayn, fakk al-idgham
- Qira'at variants that change i'rab
- null if nothing critical to add"""

# Simplified version of the i'rab rules — for beginners. Same JSON shape,
# but plain everyday vocabulary instead of advanced Arabic-grammar terminology.
IRAB_FIELD_RULES_SIMPLE = """### type
- "verb" — any action word (past, present, command, passive)
- "noun" — names, things, people, descriptions, pronouns
- "particle" — short connector words (and, in, from, not, the, etc.)

### form (keep it short and beginner-friendly)
For verbs:   "past tense" / "present tense" / "command" / "past, passive" / "present, passive"
For nouns:   "common noun" / "proper noun (name)" / "adjective" / "pronoun" / "plural noun" / "feminine noun"
For particles: leave null OR a one-word function tag like "preposition" / "conjunction" / "negation"

### case_mood (use plain English with the Arabic term in parentheses)
For nouns:
  "nominative (marfu')" — the subject form, usually with a damma
  "accusative (mansub)" — the object form, usually with a fatha
  "genitive (majrur)"  — after a preposition or in a possession chain, usually with a kasra
  "indeclinable (mabni)" — pronouns, demonstratives that don't change

For verbs:
  "indicative (marfu')" / "subjunctive (mansub)" / "jussive (majzum)"
  "past tense — fixed (mabni)" / "command — fixed (mabni)"

For particles: "fixed (mabni)" or null

### role (use plain English labels first; Arabic term in parens)
Subject (fa'il) | Object (maf'ul) | Predicate (khabar) | Subject of sentence (mubtada)
Adjective (sifa) | Possessor (mudaf) | Possessed-of (mudaf ilayhi)
Preposition (jarr) | Conjunction | Negation particle | Question particle
Pronoun — subject | Pronoun — object | Pronoun — possessive
Vocative (calling) | Cause/Reason | Time/Place

### notes
Add only if a beginner would be confused without it. One short sentence max. null otherwise.
Examples of good simple notes:
  "The 'ed' ending shows it's past tense — like 'walked' in English."
  "This is a pronoun stuck onto the noun, meaning 'his/her/their'."
  "The verb here has no visible subject — 'he/she/they' is hidden inside it."
"""

IRAB_GLOBAL_RULES = """1. Every word in the verse gets its own object — particles (wa, fa, la, ma, in etc.) included.
2. For attached pronouns that are part of a word (e.g. هُمْ in أَعْمَالَهُمْ), analyze the full word as one object AND note the pronoun's role in the notes field. Do NOT split them unless the pronoun is a clear standalone clitic.
3. For inna/anna and sisters: the word itself is "harf"; its attached pronoun gets analyzed as one unit with notes explaining the ism of inna.
4. Keep all field values SHORT — no full sentences except in notes.
5. "form" field is null for pure particles that have no morphological derivation.
6. Always return the Arabic word exactly as it appears in the verse (with full diacritics if provided)."""


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
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai_types.GenerateContentConfig(max_output_tokens=600),
        )
        return jsonify({"feedback": response.text or ""})

    except Exception as e:
        code, friendly = humanize_gemini_error(e)
        return jsonify({"error": friendly}), code


@app.route("/api/feedback-issue", methods=["POST"])
def feedback_issue():
    """Create a GitHub issue (and optionally upload a screenshot) using a
    repo-scoped Personal Access Token stored in .env as GITHUB_TOKEN."""
    import urllib.request
    import urllib.error
    import base64
    import uuid
    from datetime import datetime, timezone

    data = request.get_json() or {}
    issue_type = data.get("type", "bug")  # 'bug' or 'enhancement'
    title = (data.get("title") or "").strip()
    body = (data.get("body") or "").strip()
    screenshot_data_url = data.get("screenshot")  # data:image/png;base64,...

    if not title:
        return jsonify({"error": "Title is required"}), 400

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return jsonify({"error": "GITHUB_TOKEN not configured on server. Add it to portal/.env."}), 500

    repo = os.environ.get("GITHUB_REPO", "avutech/quranicarabic")
    api_base = "https://api.github.com"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "QuranicArabicPortal-Feedback/1.0",
    }

    def github_request(method, path, payload=None):
        url = f"{api_base}{path}"
        body_bytes = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(url, data=body_bytes, method=method, headers={
            **headers,
            "Content-Type": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, json.loads(resp.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode(errors="replace")
            return e.code, {"error": err_body}

    # 1. If a screenshot was attached, upload it to feedback-screenshots/<uuid>.png
    image_md = ""
    if screenshot_data_url and screenshot_data_url.startswith("data:image/"):
        try:
            header, b64 = screenshot_data_url.split(",", 1)
            ext = "png" if "png" in header else ("jpg" if "jpeg" in header or "jpg" in header else "png")
            ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            filename = f"feedback-screenshots/{ts}-{uuid.uuid4().hex[:8]}.{ext}"
            put_status, put_resp = github_request(
                "PUT",
                f"/repos/{repo}/contents/{filename}",
                {
                    "message": f"feedback screenshot ({ts})",
                    "content": b64,
                    "branch": "main",
                },
            )
            if put_status in (200, 201):
                download_url = put_resp.get("content", {}).get("download_url")
                if download_url:
                    image_md = f"\n\n---\n\n**Screenshot:**\n\n![screenshot]({download_url})\n"
            else:
                image_md = f"\n\n_(Screenshot upload failed: HTTP {put_status})_\n"
        except Exception as e:
            image_md = f"\n\n_(Screenshot upload error: {e})_\n"

    # 2. Create the issue
    labels = ["bug", "bugs to fix"] if issue_type == "bug" else ["enhancement", "improvements to consider"]
    prefix = "[Bug] " if issue_type == "bug" else "[Enhancement] "
    issue_status, issue_resp = github_request(
        "POST",
        f"/repos/{repo}/issues",
        {
            "title": prefix + title,
            "body": body + image_md,
            "labels": labels,
        },
    )
    if issue_status not in (200, 201):
        return jsonify({"error": f"GitHub API returned HTTP {issue_status}", "detail": issue_resp.get("error", "")[:500]}), 500
    return jsonify({
        "ok": True,
        "issue_url": issue_resp.get("html_url"),
        "issue_number": issue_resp.get("number"),
    })


@app.route("/api/self-check", methods=["POST"])
def self_check():
    """Compare a learner's per-word i'rab attempt to a fresh expert analysis
    and return per-field grading + corrective feedback."""
    data = request.get_json() or {}
    verse = (data.get("verse") or "").strip()
    language = data.get("language", "en")
    user_answers = data.get("user_answers") or []
    complexity = data.get("complexity", "complex")  # "simple" or "complex"
    if complexity not in ("simple", "complex"):
        complexity = "complex"

    if not verse:
        return jsonify({"error": "No verse provided"}), 400
    if not isinstance(user_answers, list) or not user_answers:
        return jsonify({"error": "user_answers (list) is required"}), 400

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY environment variable is not set"}), 500

    lang_names = {"en": "English", "tr": "Turkish", "ar": "Arabic"}
    response_lang = lang_names.get(language, "English")

    user_block = "\n".join(
        f"  Word {i + 1} — {ua.get('arabic', '?')}\n"
        f"    user_meaning: {ua.get('meaning') or '(empty)'}\n"
        f"    user_role:    {ua.get('role') or '(empty)'}\n"
        f"    user_notes:   {ua.get('notes') or '(empty)'}"
        for i, ua in enumerate(user_answers)
    )

    prompt = f"""You are an expert Quranic Arabic grammar teacher grading a student's word-by-word i'rab attempt.

## LANGUAGE
All prose (correct.meaning, correct.role, correct.notes, feedback, overall_feedback) MUST be written in **{response_lang}**. Keep transliterated Arabic technical terms (mubtada, fa'il, mansub, marfu', etc.) and Arabic script unchanged.

## I'RAB FIELD RULES — these govern the `correct` field you produce for each word

{IRAB_FIELD_RULES_SIMPLE if complexity == "simple" else IRAB_FIELD_RULES}

## COMPLEXITY MODE: {complexity.upper()}
{("This is a beginner-friendly grading. Keep `correct.role`, `correct.case_mood`, and `correct.notes` SHORT and use plain English with the Arabic term in parentheses (e.g. 'subject (fa'il)'). Avoid advanced terminology like 'sifa mushabbaha', 'jam' mudhakkar salim', 'maf'ul mutlaq' unless absolutely necessary." if complexity == "simple" else "This is the full advanced grading. Use precise classical Arabic-grammar terminology (mubtada, khabar, fa'il, sifa mushabbaha, jam' mudhakkar salim, maf'ul mutlaq, ghayr munsarif, na'ib fa'il, etc.) wherever applicable.")}
GRADING TOLERANCE: Be lenient about *terminology* the student uses — if they wrote a simple word like "subject" but the correct answer in this complexity mode is "Mubtada", credit it as "correct" (or "partial" if they missed something else about the word). The student's vocabulary level may be below the complexity mode they picked.

## GLOBAL I'RAB RULES — MANDATORY

{IRAB_GLOBAL_RULES}

## VERSE
{verse}

## STUDENT'S ANSWERS (one entry per word, IN THIS ORDER — keep the same order in your output)
{user_block}

## YOUR TASK
1. Produce the correct word-by-word i'rab for the verse, matching the student's word boundaries (one output entry per student entry, same Arabic surface form). Apply the I'RAB FIELD RULES above when filling `correct.role` and `correct.notes`.
2. For each word, compare the student's three fields (meaning, role, notes) against the correct answer and assign a grade:
   - "correct"   — substantively right (synonyms / wording differences are fine)
   - "partial"   — partially right but missing a key piece OR slightly off
   - "incorrect" — wrong
   - "missing"   — student left it blank
3. Produce a short corrective `feedback` for the student in {response_lang} (1–3 sentences) per word — only mention what they got wrong or missed; if all three fields are correct, congratulate them briefly.
4. Produce an `overall_feedback` (2–4 sentences in {response_lang}) summarizing strengths and the single most important thing to focus on next.

## OUTPUT — return ONLY valid JSON with this schema:
{{
  "words": [
    {{
      "arabic": "<the word — same as student's input>",
      "user":    {{ "meaning": "...", "role": "...", "notes": "..." }},
      "correct": {{ "meaning": "...", "role": "...", "notes": "..." }},
      "scores":  {{ "meaning": "correct|partial|incorrect|missing",
                    "role":    "correct|partial|incorrect|missing",
                    "notes":   "correct|partial|incorrect|missing" }},
      "feedback": "<1–3 sentences in {response_lang}>"
    }}
  ],
  "overall_feedback": "<2–4 sentences in {response_lang}>"
}}

If a field has substantive correct content but the student left it blank, mark that field as "missing" (not "correct"). For `notes`, only return an empty string in `correct.notes` if there is genuinely nothing important to add for that word — otherwise fill in the actual grammatical note the learner should have written.
"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=16000,
            ),
        )
        raw = (response.text or "").strip()
        if not raw:
            return jsonify({"error": "Empty response from model"}), 502

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            for open_ch, close_ch in (("{", "}"), ("[", "]")):
                start, end = raw.find(open_ch), raw.rfind(close_ch)
                if start >= 0 and end > start:
                    try:
                        payload = json.loads(raw[start:end + 1])
                        break
                    except json.JSONDecodeError:
                        continue
            else:
                return jsonify({"error": "Could not parse model output as JSON"}), 502

        # Deterministic guardrail: if the student left a field blank but the
        # correct answer has substantive content, force the score to "missing".
        # If both are blank, force "correct" (nothing to say is fine).
        for w in payload.get("words") or []:
            user_fields = w.get("user") or {}
            correct_fields = w.get("correct") or {}
            scores = w.get("scores") or {}
            for field in ("meaning", "role", "notes"):
                u = (user_fields.get(field) or "").strip()
                c = (correct_fields.get(field) or "").strip()
                if not u and c:
                    scores[field] = "missing"
                elif not u and not c:
                    scores[field] = "correct"
            w["scores"] = scores

        return jsonify(payload)

    except Exception as e:
        code, friendly = humanize_gemini_error(e)
        return jsonify({"error": friendly}), code


@app.route("/api/learn-deep", methods=["POST"])
def learn_deep():
    """Generate a guided deep-dive explanation of a specific grammar concept
    from a specific lesson. Pulls context from lessons_index.json and asks
    Gemini to produce explanation + worked examples in the user's language."""
    data = request.get_json() or {}
    level = data.get("level")
    week = data.get("week")
    concept_index = data.get("concept_index")
    language = data.get("language", "en")

    if level is None or week is None or concept_index is None:
        return jsonify({"error": "level, week, and concept_index are required"}), 400

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY environment variable is not set"}), 500
    if LESSONS_INDEX is None:
        return jsonify({"error": "lessons_index.json not found"}), 500

    lesson_key = f"L{level}W{week}"
    lesson = LESSONS_INDEX.get(lesson_key)
    if not lesson:
        return jsonify({"error": f"Lesson {lesson_key} not found"}), 404

    concepts = lesson.get("concepts", [])
    if not (0 <= concept_index < len(concepts)):
        return jsonify({"error": "concept_index out of range"}), 400

    concept = concepts[concept_index]
    lang_names = {"en": "English", "tr": "Turkish", "ar": "Arabic"}
    response_lang = lang_names.get(language, "English")

    concept_name_ar = concept.get("name", {}).get("ar", "")
    concept_name_en = concept.get("name", {}).get("en", "")
    concept_name_target = concept.get("name", {}).get(language, concept_name_en)
    keywords = ", ".join(concept.get("keywords", []))
    examples_seed = "\n".join(f"  - {e}" for e in concept.get("examples", [])) or "  (none provided)"
    lesson_title_target = lesson.get("verified_title", {}).get(language, lesson.get("verified_title", {}).get("en", ""))
    lesson_summary = lesson.get("summary", "")

    prompt = f"""You are an expert teacher of Quranic Arabic grammar producing a guided deep-dive lesson on a single concept.

## LANGUAGE — CRITICAL
Write ALL prose in **{response_lang}** (explanation, rules, walkthroughs). Keep transliterated technical terms (mubtada, fa'il, mansub, etc.) and Arabic script unchanged.

## CONTEXT — The lesson this concept lives in
- Lesson: Level {level}, Week {week}: {lesson_title_target}
- Lesson summary: {lesson_summary}

## TARGET CONCEPT
- Name: {concept_name_target} ({concept_name_ar})
- Keywords: {keywords}
- Seed example tokens to include or expand:
{examples_seed}

## OUTPUT FORMAT
Return ONLY valid JSON (no markdown, no prose outside the JSON), matching this schema:

{{
  "title": "<concept title in {response_lang}>",
  "arabic_name": "{concept_name_ar}",
  "overview": "<2–4 sentence high-level intro to what this concept is, in {response_lang}>",
  "rules": [
    "<rule 1: a clear, specific grammatical rule or pattern, with the Arabic term in transliteration where appropriate>",
    "<rule 2>",
    "<rule 3 — aim for 3–6 rules total>"
  ],
  "examples": [
    {{
      "arabic": "<short Arabic word/phrase/sentence>",
      "translation": "<translation into {response_lang}>",
      "walkthrough": "<3–6 sentence i'rab-style walkthrough that shows how this concept applies, in {response_lang}. Use bullet form `- ` if helpful. Mention case, marker, role, etc.>"
    }},
    {{ "arabic": "...", "translation": "...", "walkthrough": "..." }},
    {{ "arabic": "...", "translation": "...", "walkthrough": "..." }}
  ],
  "common_mistakes": [
    "<a typical learner error and how to avoid it, in {response_lang}>",
    "<another, optional>"
  ]
}}

GUIDELINES:
- Provide exactly 3 examples; prefer Quranic examples over invented ones.
- Each walkthrough should isolate the target concept (don't expand into unrelated grammar).
- Keep total length under ~600 words to stay focused.
- Where you cite Arabic, also include the transliteration in parentheses on first occurrence.

NOW produce the JSON."""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=8000,
            ),
        )
        raw = (response.text or "").strip()
        if not raw:
            return jsonify({"error": "Empty response from model"}), 502

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            for open_ch, close_ch in (("{", "}"), ("[", "]")):
                start, end = raw.find(open_ch), raw.rfind(close_ch)
                if start >= 0 and end > start:
                    try:
                        payload = json.loads(raw[start:end + 1])
                        break
                    except json.JSONDecodeError:
                        continue
            else:
                return jsonify({"error": "Could not parse model output as JSON"}), 502

        # Convert the index's "Level-1__1st Lesson..." format to a real
        # filesystem path "Level-1/1st Lesson....pdf" for the frontend link.
        pdf_filename = lesson.get("pdf_filename")
        if pdf_filename:
            real_path = pdf_filename.replace("__", "/") + ".pdf"
            if (PDF_DIR / real_path).exists():
                payload["pdf_path"] = real_path
            else:
                payload["pdf_path"] = pdf_filename  # best-effort fallback
        payload["lesson_title"] = lesson_title_target
        payload["level"] = level
        payload["week"] = week
        payload["lesson_id"] = lesson_key
        return jsonify(payload)

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

    prompt = f"""You are an expert in Quranic Arabic grammar. Analyze Quranic verses word-by-word and return a JSON object. The top-level object contains a verse-wide `translation` and a `words` array; each element of `words` represents one word/particle.

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

Return ONLY a valid JSON object. No prose, no markdown, no explanation outside the JSON.

## JSON SCHEMA

{{
  "translation": "<a single complete, natural-flowing translation of the ENTIRE verse into {response_lang} — 1–3 sentences. This is for the learner to read at a glance, before they study the word-by-word breakdown.>",
  "words": [
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
  ]
}}

## FIELD RULES — MANDATORY

These rules are not suggestions. Every word object MUST follow them exactly. If a rule conflicts with brevity, follow the rule. If a label isn't listed below, do not invent one — pick the closest match from the list.

{IRAB_FIELD_RULES}

**WRITE the explanatory prose inside `notes` in {response_lang}** — only the transliterated Arabic terms stay unchanged. Examples of well-written notes in different languages (same content):
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

## IMPORTANT RULES — MANDATORY

These six rules are non-negotiable. Every output must satisfy all of them.

{IRAB_GLOBAL_RULES}

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
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=16000,
            ),
        )
        raw = (response.text or "").strip()
        finish_reason = None
        try:
            finish_reason = str(response.candidates[0].finish_reason) if response.candidates else None
        except Exception:
            pass

        if not raw:
            print(f"[irab] empty response, finish_reason={finish_reason}", file=sys.stderr)
            return jsonify({
                "error": (
                    f"⚠️ Gemini returned an empty response (reason: {finish_reason or 'unknown'}).\n\n"
                    "Try again, or simplify the verse if it's very long."
                )
            }), 502

        payload = None
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            # Try truncated-array salvage: model may have been cut off mid-element
            for open_ch, close_ch in (("[", "]"), ("{", "}")):
                start = raw.find(open_ch)
                end = raw.rfind(close_ch)
                if start >= 0 and end > start:
                    try:
                        payload = json.loads(raw[start : end + 1])
                        break
                    except json.JSONDecodeError:
                        continue
            # If still failing, attempt to truncate to last complete object inside an array
            if payload is None and raw.startswith("["):
                # Find last "}," and close the array there
                last = raw.rfind("},")
                if last > 0:
                    try:
                        payload = json.loads(raw[: last + 1] + "]")
                        print(f"[irab] salvaged truncated array up to char {last}", file=sys.stderr)
                    except json.JSONDecodeError:
                        pass

        if payload is None:
            print(f"[irab] parse failure, finish_reason={finish_reason}, raw len={len(raw)}", file=sys.stderr)
            print(f"[irab] raw start: {raw[:300]}", file=sys.stderr)
            print(f"[irab] raw end:   {raw[-300:]}", file=sys.stderr)
            err_msg = "⚠️ Could not parse the model's response as JSON.\n\n"
            if finish_reason and "MAX_TOKENS" in finish_reason.upper():
                err_msg += "The response was cut off (output too long). Try a shorter verse, or wait and retry — model may have been verbose."
            else:
                err_msg += f"Reason: {finish_reason or 'unknown'}. Try clicking Analyze again — Gemini occasionally returns malformed JSON."
            return jsonify({"error": err_msg, "raw_preview": raw[:300]}), 502

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
    print(f"🤖 Gemini model: {GEMINI_MODEL}")
    print(f"🌐 Portal running at: http://localhost:8081")
    app.run(port=8081, debug=False)

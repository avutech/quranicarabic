import functools
import os
import sys
import json
import re
import time
import unicodedata
from pathlib import Path
from flask import Flask, send_from_directory, request, jsonify, abort, redirect
from google import genai
from google.genai import types as genai_types

import db as user_db
from auth import auth_bp, login_required, admin_required, current_user_row, current_user_dict


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
    # Transient model overload (Gemini returns 503 UNAVAILABLE under high demand)
    if "503" in msg or "UNAVAILABLE" in msg or "overloaded" in msg.lower():
        return 503, (
            "⚠️ The AI is busy right now (high demand). "
            "Please wait a few seconds and try again — this usually clears up quickly."
        )
    # Generic
    return 500, str(exc)


def gemini_generate(client, *, model, contents, config=None, _retries=3):
    """Wrapper around client.models.generate_content that automatically retries
    transient 503/UNAVAILABLE (model-overloaded) errors with exponential backoff.
    Non-transient errors propagate immediately to humanize_gemini_error()."""
    delay = 1.0
    for attempt in range(_retries):
        try:
            return client.models.generate_content(
                model=model, contents=contents, config=config
            )
        except Exception as e:
            msg = str(e)
            transient = "503" in msg or "UNAVAILABLE" in msg or "overloaded" in msg.lower()
            if not transient or attempt == _retries - 1:
                raise
            time.sleep(delay)
            delay *= 2

app = Flask(__name__)
app.register_blueprint(auth_bp)

# Seed admin on startup if the users table is empty.
user_db.init_db()
_seed_pw = user_db.ensure_seed_admin("ahmugur@gmail.com")
if _seed_pw:
    print("=" * 70, file=sys.stderr)
    print("🔑  Seed admin created: ahmugur@gmail.com", file=sys.stderr)
    print(f"    Initial password: {_seed_pw}", file=sys.stderr)
    print("    Save this — it won't be shown again. Change it via the admin panel.", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

BASE_DIR = Path(__file__).parent.parent
PDF_DIR = BASE_DIR / "Kuran-Kerim Arapcasi"
DERSLER_DIR = BASE_DIR / "Dersler"
IRAB_LIBRARY_DIR = BASE_DIR / "irab_library"
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


# Shared i'rab field-rule reference — injected into /api/self-check so the
# "correct" analysis follows a standardized vocabulary.
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

# OpenAI model settings
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")


@app.route("/")
def index():
    return send_from_directory(str(PORTAL_DIR), "index.html")


def _lesson_id_for_pdf(filename: str):
    """Infer the L{N}W{M} lesson key from the requested PDF path. Returns
    None if the PDF doesn't belong to any specific lesson (e.g. shared
    reference materials, vocab, bablar — those are always allowed)."""
    # Lesson PDFs live under Level-1/, Level-2/, Level-3/
    m = re.match(r"^Level-([123])/(\d+)(?:st|nd|rd|th)?\s*Lesson", filename)
    if m:
        level, lesson_num = int(m.group(1)), int(m.group(2))
        # Level-1/1st..14th, Level-2/15th..28th, Level-3/29th..42nd
        if level == 1:
            week = lesson_num
        elif level == 2:
            week = lesson_num - 14
        else:
            week = lesson_num - 28
        if 1 <= week <= 14:
            return f"L{level}W{week}"
    return None


def _resolve_pdf_name(filename):
    """macOS stores filenames decomposed (NFD); data.js references the composed
    (NFC) form. On a Linux server these don't match byte-for-byte, so a direct
    lookup 404s on any name with Turkish/Arabic characters. Return whichever
    Unicode form actually exists on disk, falling back to the original."""
    base = Path(PDF_DIR)
    for form in (filename,
                 unicodedata.normalize("NFC", filename),
                 unicodedata.normalize("NFD", filename)):
        if (base / form).is_file():
            return form
    return filename


@app.route("/pdfs/<path:filename>")
def serve_pdf(filename):
    user = current_user_row()
    if not user:
        return jsonify({"error": "auth required"}), 401
    # Gate the per-lesson PDFs by unlock; reference materials stay open.
    # Admins always have full access.
    lesson_id = _lesson_id_for_pdf(filename)
    if lesson_id and user["role"] != "admin":
        unlocks = user_db.effective_unlocks(user["id"])
        if lesson_id not in unlocks:
            return jsonify({"error": "this lesson is locked"}), 403
    try:
        return send_from_directory(str(PDF_DIR), _resolve_pdf_name(filename))
    except Exception:
        abort(404)


# ─── Tashîh-i Hurûf lesson site (public) ─────────────────────────────────────
# The 26-week Tashîh-i Hurûf curriculum in Dersler/ is deliberately OPEN: no
# login, no per-lesson unlock. It is static reading material, unlike the graded
# 42-lesson course, so it is served straight from disk with no auth check.
# Pages inside it link to each other and to assets/ with RELATIVE paths, so the
# trailing slash matters — /dersler alone would resolve assets/ against "/".

@app.route("/dersler")
def dersler_index_redirect():
    return redirect("/dersler/", code=301)


@app.route("/dersler/")
@app.route("/dersler/<path:filename>")
def serve_dersler(filename="index.html"):
    # send_from_directory uses safe_join, so "../" escapes are rejected here.
    try:
        return send_from_directory(str(DERSLER_DIR), filename)
    except Exception:
        abort(404)


# ─── I'rab library (classical i'rab books, per ayah) ─────────────────────────
# Built by build_irab_library.py into <repo>/irab_library/ — deliberately
# outside portal/ so the catch-all static route below can't serve it without
# a login. Turkish readings live in irab_library/tr/sNNN.json, keyed
# "<book>:<first>-<last>" → {"t": text, "reviewed": bool}.

@functools.lru_cache(maxsize=None)
def _irab_library_file(name):
    path = IRAB_LIBRARY_DIR / name
    if not path.is_file():
        return None
    return json.loads(path.read_text("utf-8"))


@app.get("/api/irab-library/books")
@login_required
def irab_library_books():
    data = _irab_library_file("books.json")
    if data is None:
        return jsonify({"error": "irab library not built"}), 500
    return jsonify(data)


@app.get("/api/irab-library/<int:surah>/<int:ayah>")
@login_required
def irab_library_ayah(surah, ayah):
    if not (1 <= surah <= 114) or ayah < 1:
        abort(404)
    data = _irab_library_file(f"s{surah:03d}.json")
    if data is None:
        return jsonify({"error": "irab library not built"}), 500
    tr = _irab_library_file(f"tr/s{surah:03d}.json") or {}
    entries = []
    for e in data["entries"]:
        if e["s"] <= ayah <= e["e"]:
            item = dict(e)
            reading = tr.get(f"{e['b']}:{e['s']}-{e['e']}")
            if reading:
                item["tr"] = reading
            entries.append(item)
    word_data = (_irab_library_file(f"w/s{surah:03d}.json") or {}).get(str(ayah), {})
    return jsonify({"surah": surah, "ayah": ayah, "entries": entries,
                    "words": word_data.get("w", []), "meals": word_data.get("m", {})})


# Only the frontend's own assets are public. portal/ also holds .env (API
# keys), users.db and the server source, so this must stay an allowlist.
PUBLIC_PORTAL_FILES = {"data.js", "vocab.js", "lessons_index.js", "lessons_index.json", "lectures.json"}


@app.route("/<path:filename>")
def static_files(filename):
    if filename not in PUBLIC_PORTAL_FILES:
        abort(404)
    try:
        return send_from_directory(str(PORTAL_DIR), filename)
    except Exception:
        abort(404)


@app.route("/api/feedback", methods=["POST"])
@login_required
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

        response = gemini_generate(client,
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
@login_required
def self_check():
    """Compare a learner's per-word i'rab attempt to a fresh expert analysis
    and return per-field grading + corrective feedback."""
    if not user_db.is_module_active("self-check"):
        return jsonify({"error": "This module is turned off."}), 403
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
        response = gemini_generate(client,
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
@login_required
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

    # Inject any admin-uploaded resources for this lesson as additional context
    prompt += _lesson_instructor_context(level, week)

    try:
        client = genai.Client(api_key=api_key)
        response = gemini_generate(client,
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


# ─── Admin endpoints (user management) ────────────────────────────────────────

def _all_lessons():
    return user_db.all_lesson_ids()

# Backwards-compat: callers still reference ALL_LESSONS as a sequence;
# we expose a property-like via the helper. For places that need it as a value
# at request time, call _all_lessons().
ALL_LESSONS = []  # populated lazily; see _all_lessons() below


@app.get("/api/admin/users")
@admin_required
def admin_list_users():
    rows = user_db.list_users()
    classrooms = user_db.list_classrooms()
    # We need classroom_id per user; list_users doesn't include it, so fetch fresh.
    out = []
    with user_db.db() as conn:
        full_rows = conn.execute(
            "SELECT id, email, role, created_at, last_login, classroom_id, first_name, last_name FROM users ORDER BY id"
        ).fetchall()
    for r in full_rows:
        cid = r["classroom_id"]
        out.append({
            "id": r["id"],
            "email": r["email"],
            "first_name": r["first_name"] or "",
            "last_name": r["last_name"] or "",
            "display_name": user_db.display_name(r),
            "role": r["role"],
            "created_at": r["created_at"],
            "last_login": r["last_login"],
            "classroom_id": cid,
            "personal_unlocks": user_db.get_unlocks(r["id"]),
            "effective_unlocks": user_db.effective_unlocks(r["id"]),
        })
    return jsonify({
        "users": out,
        "all_lessons": _all_lessons(),
        "classrooms": classrooms,
    })


@app.post("/api/admin/users")
@admin_required
def admin_create_user():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = data.get("role") or "user"
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    classroom_id = data.get("classroom_id")
    if classroom_id in (0, "0", ""):
        classroom_id = None
    if classroom_id is not None and (not isinstance(classroom_id, int) or not user_db.get_classroom(classroom_id)):
        return jsonify({"error": "invalid classroom_id"}), 400
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    if role not in ("user", "admin"):
        return jsonify({"error": "role must be 'user' or 'admin'"}), 400
    try:
        uid = user_db.create_user(email, password, role, first_name, last_name)
    except Exception as e:
        return jsonify({"error": f"could not create user: {e}"}), 400
    if classroom_id is not None:
        user_db.assign_user_to_classroom(uid, classroom_id)
    return jsonify({"id": uid, "email": email, "role": role, "classroom_id": classroom_id}), 201


@app.post("/api/admin/users/<int:user_id>/name")
@admin_required
def admin_update_name(user_id):
    data = request.get_json(silent=True) or {}
    if not user_db.find_user_by_id(user_id):
        return jsonify({"error": "user not found"}), 404
    user_db.update_user_name(user_id, data.get("first_name", ""), data.get("last_name", ""))
    return jsonify({"ok": True})


@app.delete("/api/admin/users/<int:user_id>")
@admin_required
def admin_delete_user(user_id):
    me = current_user_row()
    if me and me["id"] == user_id:
        return jsonify({"error": "you cannot delete yourself"}), 400
    user_db.delete_user(user_id)
    return jsonify({"ok": True})


@app.post("/api/admin/users/<int:user_id>/unlocks")
@admin_required
def admin_set_unlocks(user_id):
    """Replace the user's unlock set with the supplied list. Body: {lesson_ids: [...]}."""
    data = request.get_json(silent=True) or {}
    ids = data.get("lesson_ids")
    if not isinstance(ids, list):
        return jsonify({"error": "lesson_ids (list) required"}), 400
    valid = [lid for lid in ids if lid in _all_lessons()]
    user_db.set_unlocks(user_id, valid)
    return jsonify({"unlocks": user_db.get_unlocks(user_id)})


@app.post("/api/admin/users/<int:user_id>/role")
@admin_required
def admin_set_role(user_id):
    """Change a user's role. Refuses to demote the last admin (lockout safety)."""
    data = request.get_json(silent=True) or {}
    new_role = (data.get("role") or "").strip()
    if new_role not in ("user", "admin"):
        return jsonify({"error": "role must be 'user' or 'admin'"}), 400
    target = user_db.find_user_by_id(user_id)
    if not target:
        return jsonify({"error": "user not found"}), 404
    # If demoting an admin, ensure at least one admin remains
    if target["role"] == "admin" and new_role != "admin":
        with user_db.db() as conn:
            n = conn.execute("SELECT COUNT(*) AS n FROM users WHERE role = 'admin'").fetchone()["n"]
        if n <= 1:
            return jsonify({"error": "cannot demote the last admin"}), 400
    with user_db.db() as conn:
        conn.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    return jsonify({"ok": True, "id": user_id, "role": new_role})


@app.post("/api/admin/users/<int:user_id>/password")
@admin_required
def admin_reset_password(user_id):
    data = request.get_json(silent=True) or {}
    new_pw = data.get("password") or ""
    if len(new_pw) < 6:
        return jsonify({"error": "password must be at least 6 characters"}), 400
    if not user_db.find_user_by_id(user_id):
        return jsonify({"error": "user not found"}), 404
    user_db.update_password(user_id, new_pw)
    return jsonify({"ok": True})


# ─── Classroom admin endpoints ────────────────────────────────────────────────

@app.get("/api/admin/classrooms")
@admin_required
def admin_list_classrooms():
    rooms = user_db.list_classrooms()
    out = []
    for c in rooms:
        unlocks = user_db.get_classroom_unlocks(c["id"])
        # Need full member rows to access first/last name
        with user_db.db() as conn:
            members = conn.execute(
                "SELECT id, email, role, first_name, last_name FROM users WHERE classroom_id = ? ORDER BY first_name, last_name, email",
                (c["id"],),
            ).fetchall()
        out.append({
            **c,
            "unlocks": unlocks,
            "members": [{
                "id": m["id"],
                "email": m["email"],
                "role": m["role"],
                "display_name": user_db.display_name(m),
            } for m in members],
        })
    return jsonify({"classrooms": out, "all_lessons": _all_lessons()})


@app.post("/api/admin/classrooms")
@admin_required
def admin_create_classroom():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    try:
        cid = user_db.create_classroom(name)
    except Exception as e:
        return jsonify({"error": f"could not create classroom: {e}"}), 400
    return jsonify({"id": cid, "name": name}), 201


@app.delete("/api/admin/classrooms/<int:cid>")
@admin_required
def admin_delete_classroom(cid):
    if not user_db.get_classroom(cid):
        return jsonify({"error": "classroom not found"}), 404
    user_db.delete_classroom(cid)
    return jsonify({"ok": True})


@app.post("/api/admin/classrooms/<int:cid>/rename")
@admin_required
def admin_rename_classroom(cid):
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    if not user_db.get_classroom(cid):
        return jsonify({"error": "classroom not found"}), 404
    user_db.rename_classroom(cid, name)
    return jsonify({"ok": True, "id": cid, "name": name})


@app.post("/api/admin/classrooms/<int:cid>/unlocks")
@admin_required
def admin_set_classroom_unlocks(cid):
    data = request.get_json(silent=True) or {}
    ids = data.get("lesson_ids")
    if not isinstance(ids, list):
        return jsonify({"error": "lesson_ids (list) required"}), 400
    if not user_db.get_classroom(cid):
        return jsonify({"error": "classroom not found"}), 404
    valid = [lid for lid in ids if lid in _all_lessons()]
    user_db.set_classroom_unlocks(cid, valid)
    return jsonify({"unlocks": user_db.get_classroom_unlocks(cid)})


@app.post("/api/admin/users/<int:user_id>/classroom")
@admin_required
def admin_assign_classroom(user_id):
    """Body: {classroom_id: <int|null>}. null/0 = unassign."""
    data = request.get_json(silent=True) or {}
    cid = data.get("classroom_id")
    if cid in (0, "0", ""):
        cid = None
    if cid is not None:
        if not isinstance(cid, int) or not user_db.get_classroom(cid):
            return jsonify({"error": "invalid classroom_id"}), 400
    if not user_db.find_user_by_id(user_id):
        return jsonify({"error": "user not found"}), 404
    user_db.assign_user_to_classroom(user_id, cid)
    return jsonify({"ok": True, "user_id": user_id, "classroom_id": cid})


# ─── Module activation endpoints ──────────────────────────────────────────────

@app.get("/api/modules")
@login_required
def list_module_states():
    """Public (any logged-in user): which modules are turned off.
    The frontend uses this to hide deactivated modules from the sidebar."""
    return jsonify({"inactive": user_db.get_inactive_modules()})


@app.get("/api/admin/modules")
@admin_required
def admin_list_modules():
    """Admin: the full map of module_id -> active for modules that have an
    explicit state. Modules not present here are active by default."""
    return jsonify({"states": user_db.get_module_states()})


@app.post("/api/admin/modules")
@admin_required
def admin_set_module():
    """Body: {module_id: <str>, active: <bool>}."""
    data = request.get_json(silent=True) or {}
    module_id = (data.get("module_id") or "").strip()
    active = data.get("active")
    if not module_id:
        return jsonify({"error": "module_id required"}), 400
    if not isinstance(active, bool):
        return jsonify({"error": "active (bool) required"}), 400
    user_db.set_module_active(module_id, active)
    return jsonify({"ok": True, "module_id": module_id, "active": active})


# ─── Levels (built-in 1-3 + admin-defined extras) ────────────────────────────

@app.get("/api/levels")
@login_required
def list_levels_endpoint():
    """Public to all authenticated users — drives the dynamic sidebar / pickers."""
    return jsonify({"levels": user_db.list_all_levels()})


@app.post("/api/admin/levels")
@admin_required
def admin_create_level():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    try:
        weeks = int(data.get("week_count") or 14)
    except (ValueError, TypeError):
        return jsonify({"error": "week_count must be an integer"}), 400
    if not name:
        return jsonify({"error": "name required"}), 400
    try:
        level_num = user_db.create_extra_level(
            name, weeks,
            name_tr=data.get("name_tr") or "",
            name_ar=data.get("name_ar") or "",
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"level_num": level_num, "name": name, "week_count": weeks}), 201


@app.patch("/api/admin/levels/<int:level_num>")
@admin_required
def admin_patch_level(level_num):
    if level_num <= 3:
        return jsonify({"error": "built-in levels cannot be modified"}), 400
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    name_tr = data.get("name_tr")
    name_ar = data.get("name_ar")
    weeks = data.get("week_count")
    try:
        if weeks is not None:
            weeks = int(weeks)
        user_db.update_extra_level(level_num, name=name, week_count=weeks,
                                    name_tr=name_tr, name_ar=name_ar)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True})


@app.delete("/api/admin/levels/<int:level_num>")
@admin_required
def admin_delete_level(level_num):
    if level_num <= 3:
        return jsonify({"error": "built-in levels cannot be deleted"}), 400
    try:
        user_db.delete_extra_level(level_num)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True})


# ─── Resources (admin-uploadable per-lesson content) ──────────────────────────

import uuid as _uuid
from werkzeug.utils import secure_filename

UPLOADS_DIR = PORTAL_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50 MB
ALLOWED_MIMES = {
    "pdf":   {"application/pdf"},
    "image": {"image/png", "image/jpeg", "image/gif", "image/webp", "image/svg+xml"},
    "audio": {"audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg", "audio/x-m4a", "audio/mp4"},
}


def _user_can_see_lesson(user, level, week):
    if not user:
        return False
    if user["role"] == "admin":
        return True
    return f"L{level}W{week}" in user_db.effective_unlocks(user["id"])


@app.get("/api/resources")
@login_required
def list_resources_endpoint():
    """List resources for a lesson (or empty list if user has no access)."""
    try:
        level = int(request.args.get("level", "0"))
        week  = int(request.args.get("week", "0"))
    except ValueError:
        return jsonify({"error": "level/week must be integers"}), 400
    if not user_db.is_valid_lesson(level, week):
        return jsonify({"error": "invalid level/week"}), 400
    user = current_user_row()
    if not _user_can_see_lesson(user, level, week):
        return jsonify({"resources": []})   # silent — same as having no access
    return jsonify({"resources": user_db.list_resources(level=level, week=week)})


@app.get("/uploads/<path:filename>")
@login_required
def serve_upload(filename):
    """Serve uploaded files, gated by the resource's lesson unlock."""
    user = current_user_row()
    # Find the resource that owns this file
    with user_db.db() as conn:
        row = conn.execute(
            "SELECT level, week FROM resources WHERE file_path = ?",
            (filename,),
        ).fetchone()
    if not row:
        abort(404)
    if not _user_can_see_lesson(user, row["level"], row["week"]):
        return jsonify({"error": "this lesson is locked"}), 403
    return send_from_directory(str(UPLOADS_DIR), filename, as_attachment=False)


@app.post("/api/admin/resources")
@admin_required
def create_resource_endpoint():
    """Create a resource. Multipart for file uploads, JSON for link/note."""
    user = current_user_row()
    # Two paths: multipart (file upload) vs JSON (link/note)
    if request.files:
        # Multipart file upload
        try:
            level = int(request.form.get("level", "0"))
            week  = int(request.form.get("week", "0"))
        except ValueError:
            return jsonify({"error": "level/week required"}), 400
        title = (request.form.get("title") or "").strip()
        kind = (request.form.get("kind") or "").strip()
        if not title:
            return jsonify({"error": "title required"}), 400
        if kind not in ("pdf", "image", "audio"):
            return jsonify({"error": "kind must be pdf, image, or audio for file uploads"}), 400
        if not user_db.is_valid_lesson(level, week):
            return jsonify({"error": "invalid level/week"}), 400
        extract_model = (request.form.get("model") or "gemini").strip().lower()
        if extract_model not in EXTRACT_MODELS:
            extract_model = "gemini"

        f = request.files.get("file")
        if not f or not f.filename:
            return jsonify({"error": "file is required"}), 400

        mime = (f.mimetype or "").lower()
        allowed = ALLOWED_MIMES.get(kind, set())
        if allowed and mime not in allowed:
            return jsonify({"error": f"unsupported file type for kind '{kind}': {mime}"}), 400

        # Read into memory only enough to reject if too large
        f.stream.seek(0, 2)
        size = f.stream.tell()
        f.stream.seek(0)
        if size > MAX_UPLOAD_BYTES:
            return jsonify({"error": f"file too large (max {MAX_UPLOAD_BYTES // (1024*1024)} MB)"}), 413

        # Build a safe storage path: uploads/L{N}W{M}/<uuid>-<safe-original>
        subdir = f"L{level}W{week}"
        (UPLOADS_DIR / subdir).mkdir(parents=True, exist_ok=True)
        safe_name = secure_filename(f.filename) or "file"
        unique = f"{_uuid.uuid4().hex[:8]}-{safe_name}"
        rel_path = f"{subdir}/{unique}"
        f.save(str(UPLOADS_DIR / rel_path))

        rid = user_db.create_resource(
            level=level, week=week, title=title, kind=kind,
            file_path=rel_path, mime=mime, size=size,
            uploaded_by=user["id"],
        )
        # Mark pending; kick off extraction in a background thread so the upload
        # response returns immediately. Audio is skipped (no vision support).
        with user_db.db() as conn:
            conn.execute("UPDATE resources SET extraction_status = ? WHERE id = ?",
                         ("pending" if kind in ("pdf", "image") else "skip", rid))
        if kind in ("pdf", "image"):
            import threading
            threading.Thread(target=_extract_and_store, args=(rid, rel_path, mime, kind, extract_model), daemon=True).start()
        return jsonify({"id": rid, "file_path": rel_path}), 201

    # JSON path: link or note
    data = request.get_json(silent=True) or {}
    try:
        level = int(data.get("level", 0))
        week  = int(data.get("week", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "level/week required"}), 400
    title = (data.get("title") or "").strip()
    kind = (data.get("kind") or "").strip()
    if not user_db.is_valid_lesson(level, week):
        return jsonify({"error": "invalid level/week"}), 400
    if not title:
        return jsonify({"error": "title required"}), 400
    if kind == "link":
        url = (data.get("url") or "").strip()
        if not (url.startswith("http://") or url.startswith("https://")):
            return jsonify({"error": "url must start with http:// or https://"}), 400
        rid = user_db.create_resource(level=level, week=week, title=title, kind="link",
                                       url=url, uploaded_by=user["id"])
    elif kind == "note":
        body = (data.get("body") or "").strip()
        if not body:
            return jsonify({"error": "body required for notes"}), 400
        rid = user_db.create_resource(level=level, week=week, title=title, kind="note",
                                       body=body, uploaded_by=user["id"])
    else:
        return jsonify({"error": "kind must be 'link' or 'note' for JSON requests"}), 400
    # link/note kinds — their body/url IS the content, no extraction needed
    with user_db.db() as conn:
        conn.execute("UPDATE resources SET extraction_status = ? WHERE id = ?", ("skip", rid))
    return jsonify({"id": rid}), 201


@app.patch("/api/admin/resources/<int:rid>")
@admin_required
def update_resource_endpoint(rid):
    if not user_db.get_resource(rid):
        return jsonify({"error": "not found"}), 404
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title required"}), 400
    user_db.update_resource_title(rid, title)
    return jsonify({"ok": True, "title": title})


@app.post("/api/admin/resources/<int:rid>/reextract")
@admin_required
def reextract_resource_endpoint(rid):
    """Re-run Claude vision on an existing PDF/image resource so the AI can
    regenerate the structured lecture (e.g. after the extractor prompt was
    improved). No-op for link/note/audio."""
    row = user_db.get_resource(rid)
    if not row:
        return jsonify({"error": "not found"}), 404
    if row["kind"] not in ("pdf", "image"):
        return jsonify({"error": "only pdf/image resources can be re-extracted"}), 400
    if not row["file_path"]:
        return jsonify({"error": "missing file_path"}), 400
    data = request.get_json(silent=True) or {}
    extract_model = (data.get("model") or "gemini").strip().lower()
    if extract_model not in EXTRACT_MODELS:
        extract_model = "gemini"
    # Mark pending immediately + kick off background extraction
    with user_db.db() as conn:
        conn.execute("UPDATE resources SET extraction_status = ? WHERE id = ?", ("pending", rid))
    import threading
    threading.Thread(
        target=_extract_and_store,
        args=(rid, row["file_path"], row["mime"], row["kind"], extract_model),
        daemon=True,
    ).start()
    return jsonify({"ok": True})


@app.delete("/api/admin/resources/<int:rid>")
@admin_required
def delete_resource_endpoint(rid):
    file_path = user_db.delete_resource(rid)
    if file_path:
        try:
            (UPLOADS_DIR / file_path).unlink(missing_ok=True)
        except Exception:
            pass
    return jsonify({"ok": True})



# ─── Claude vision extraction (admin uploads → searchable text) ──────────────

# Anthropic vision size caps (well below our 50 MB upload cap)
_CLAUDE_MAX_PDF_BYTES = 32 * 1024 * 1024
_CLAUDE_MAX_IMG_BYTES = 5 * 1024 * 1024


def _extract_and_store(resource_id: int, rel_path: str, mime: str, kind: str, model: str = "gemini") -> None:
    """Background extractor: the admin-selected model reads the file, returns
    (a) plain text for Deep-Learn context injection and (b) a structured
    multilingual lecture for inline rendering. Both are stored on the row."""
    status = "failed"
    text = None
    lecture_json = None
    try:
        result = _extract_resource(rel_path, mime, kind, model)
        if result:
            text = result.get("text")
            lecture = result.get("lecture")
            if lecture:
                lecture_json = json.dumps(lecture, ensure_ascii=False)
            status = "done" if (text or lecture_json) else "failed"
    except Exception as e:
        print(f"[extract] resource {resource_id} failed: {e}", file=sys.stderr)
    try:
        with user_db.db() as conn:
            conn.execute(
                "UPDATE resources SET extracted_text = ?, lecture_data = ?, extraction_status = ? WHERE id = ?",
                (text, lecture_json, status, resource_id),
            )
    except Exception as e:
        print(f"[extract] db update failed for {resource_id}: {e}", file=sys.stderr)


# Shared extractor instruction — used by every provider so output is identical.
_EXTRACT_INSTRUCTION = """Read this Quranic-Arabic study material and produce a single JSON object with TWO keys:

1. "text" — full plain-text transcription. Preserve all Arabic, English, Turkish text. Include headings, lists, tables. Do NOT summarize — transcribe everything you can read.

2. "lecture" — a multilingual lecture object structured for direct rendering in the study portal. Match this exact schema:

{
  "sections": [
    {
      "title": { "en": "...", "tr": "...", "ar": "..." },
      "body":  { "en": "<markdown allowed: **bold**, *italic*, bullet lists with `- `, numbered lists, blank lines for paragraphs>",
                  "tr": "<same, written naturally in Turkish>",
                  "ar": "<same, written naturally in Arabic>" },
      "examples": [
        { "ar": "<short Arabic example>", "gloss": { "en": "...", "tr": "...", "ar": "..." } }
      ]
    }
  ]
}

LECTURE RULES:
- 2–5 sections that walk through the material as a teacher would
- Every title and body MUST have en/tr/ar keys filled with substantive content (not stubs)
- 0–6 example cards per section (skip when the section is pure prose intro/recap)
- Preserve Arabic words/phrases in Arabic script everywhere; transliteration in parens on first occurrence
- Plain teaching tone, second-person, encouraging
- Each body ~80–180 words per language

Return ONLY the JSON object — no prose around it, no markdown fences.
"""

EXTRACT_MODELS = ("gemini", "openai")   # Claude disabled system-wide


def _parse_extract_json(raw):
    """Parse an extractor's JSON output ({text, lecture}), tolerating code
    fences and surrounding prose. Returns {"text":…, "lecture":…} or None."""
    if not raw:
        return None
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lstrip().lower().startswith("json"):
            raw = raw.lstrip()[4:]
        raw = raw.strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        s, e = raw.find("{"), raw.rfind("}")
        if s >= 0 and e > s:
            try:
                parsed = json.loads(raw[s:e + 1])
            except json.JSONDecodeError:
                return None
        else:
            return None
    return {
        "text": parsed.get("text") or None,
        "lecture": parsed.get("lecture") if isinstance(parsed.get("lecture"), dict) else None,
    }


def _read_upload_b64(rel_path, kind):
    """Read an uploaded file as base64, enforcing the per-kind size caps.
    Returns the base64 string, or None if missing/oversized."""
    full = UPLOADS_DIR / rel_path
    if not full.exists():
        return None
    size = full.stat().st_size
    if kind == "pdf" and size > _CLAUDE_MAX_PDF_BYTES:
        print(f"[extract] PDF too big ({size} bytes) — skipping", file=sys.stderr)
        return None
    if kind == "image" and size > _CLAUDE_MAX_IMG_BYTES:
        print(f"[extract] image too big ({size} bytes) — skipping", file=sys.stderr)
        return None
    import base64
    with open(full, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _extract_with_claude(rel_path, mime, kind):
    """Claude Sonnet vision: transcription + structured lecture. PDF + image."""
    if kind not in ("pdf", "image"):
        return None
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    b64 = _read_upload_b64(rel_path, kind)
    if not b64:
        return None
    import anthropic
    content_block = (
        {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": b64}}
        if kind == "pdf"
        else {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}}
    )
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        messages=[{"role": "user", "content": [content_block, {"type": "text", "text": _EXTRACT_INSTRUCTION}]}],
    )
    raw = "".join(b.text for b in msg.content if hasattr(b, "text")).strip()
    return _parse_extract_json(raw)


def _extract_with_gemini(rel_path, mime, kind):
    """Gemini vision: transcription + structured lecture. PDF + image."""
    if kind not in ("pdf", "image"):
        return None
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    full = UPLOADS_DIR / rel_path
    if not full.exists():
        return None
    size = full.stat().st_size
    if kind == "pdf" and size > _CLAUDE_MAX_PDF_BYTES:
        return None
    if kind == "image" and size > _CLAUDE_MAX_IMG_BYTES:
        return None
    with open(full, "rb") as f:
        raw_bytes = f.read()
    part = genai_types.Part.from_bytes(
        data=raw_bytes, mime_type=("application/pdf" if kind == "pdf" else mime)
    )
    client = genai.Client(api_key=api_key)
    resp = gemini_generate(
        client,
        model="gemini-2.5-flash",
        contents=[part, _EXTRACT_INSTRUCTION],
        config=genai_types.GenerateContentConfig(response_mime_type="application/json", max_output_tokens=16000),
    )
    return _parse_extract_json((resp.text or "").strip())


def _extract_with_openai(rel_path, mime, kind):
    """ChatGPT (gpt-4o) vision. Images only — OpenAI's API can't read PDFs here."""
    if kind != "image":
        if kind == "pdf":
            print("[extract] ChatGPT can't read PDFs — pick Gemini for PDF resources.", file=sys.stderr)
        return None
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    b64 = _read_upload_b64(rel_path, kind)
    if not b64:
        return None
    import openai
    client = openai.OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=16000,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": [
            {"type": "text", "text": _EXTRACT_INSTRUCTION},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
        ]}],
    )
    return _parse_extract_json((resp.choices[0].message.content or "").strip())


_EXTRACTORS = {"gemini": _extract_with_gemini, "openai": _extract_with_openai}   # Claude disabled


def _extract_resource(rel_path, mime, kind, model="gemini"):
    """Run the admin-selected vision model over an uploaded PDF/image and return
    {"text":…, "lecture":…} or None. Defaults to Gemini (cheapest, highest limits)."""
    return _EXTRACTORS.get(model, _extract_with_gemini)(rel_path, mime, kind)


def _lesson_instructor_context(level: int, week: int) -> str:
    """Collect all admin-uploaded resources for a lesson and return them as a
    prompt-ready block. Returns '' if there are no resources."""
    with user_db.db() as conn:
        rows = conn.execute(
            "SELECT title, kind, url, body, extracted_text FROM resources WHERE level = ? AND week = ? ORDER BY id",
            (level, week),
        ).fetchall()
    if not rows:
        return ""
    parts = []
    for r in rows:
        if r["kind"] == "link":
            parts.append(f"### [LINK] {r['title']} — {r['url']}")
        elif r["kind"] == "note":
            parts.append(f"### [NOTE] {r['title']}\n{r['body']}")
        elif r["extracted_text"]:
            parts.append(f"### [{r['kind'].upper()}] {r['title']}\n{r['extracted_text']}")
        # PDFs/images without extracted_text yet are skipped silently
    if not parts:
        return ""
    return (
        "\n\n## INSTRUCTOR-PROVIDED MATERIAL FOR THIS LESSON\n\n"
        "The instructor has uploaded the following supplementary content. Incorporate it naturally "
        "into your explanation where relevant, and cite it (e.g. \"as your instructor noted...\"):\n\n"
        + "\n\n".join(parts)
    )


if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: GEMINI_API_KEY is not set. Practice feedback and i'rab will not work.")
        print("   Add it to portal/.env as: GEMINI_API_KEY=your_key_here")
    print(f"📂 PDF directory: {PDF_DIR}")
    print(f"🤖 Gemini model: {GEMINI_MODEL}")
    print(f"🌐 Portal running at: http://localhost:8081")
    # threaded=True: serve concurrent requests in parallel worker threads, so
    # multiple users (or multiple sessions of one shared account) operate
    # independently and simultaneously rather than being queued one-by-one.
    app.run(port=8081, debug=False, threaded=True)

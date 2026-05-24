import os
import sys
import json
import re
import time
import unicodedata
from pathlib import Path
from flask import Flask, send_from_directory, request, jsonify, abort
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
# The Curriculum-Limited (grounded) module lets the user pick the Gemini model
# per analysis. GEMINI_GROUNDED_MODEL is the DEFAULT (used when none selected)
# and is the model the context cache is built for. Picking a non-default model
# still works — it runs with the full curriculum inlined instead of cached.
GEMINI_GROUNDED_MODEL = os.environ.get("GEMINI_GROUNDED_MODEL", "gemini-2.5-flash-lite")
# Models the user is allowed to select for the grounded module.
GROUNDED_MODEL_CHOICES = {
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
}


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

# OpenAI / curriculum-grounded model settings
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")


def load_curriculum_text(compact=False):
    """Flatten lectures.json into a plain-text knowledge base for the
    curriculum-grounded modules.
      - full (compact=False): every section's full body + examples. ~250k
        tokens — fine for big-context models (Gemini 1M, Claude 200k+).
      - compact (compact=True): section titles + examples only. ~20k tokens —
        safe for gpt-4o's 128k window and tier-1 per-minute rate limits.
    Returns '' if the file is absent."""
    f = PORTAL_DIR / "lectures.json"
    if not f.exists():
        return ""
    try:
        data = json.loads(f.read_text())
    except Exception:
        return ""
    chunks = []
    if compact:
        for lesson_id, lec in data.items():
            titles, examples = [], []
            for sec in lec.get("sections", []):
                tt = (sec.get("title", {}) or {}).get("en", "")
                if tt:
                    titles.append(tt)
                for ex in sec.get("examples", []):
                    gloss = (ex.get("gloss", {}) or {}).get("en", "")
                    examples.append(f"{ex.get('ar', '')} = {gloss}")
            chunks.append(
                f"[{lesson_id}] Topics: {'; '.join(titles)}"
                + (f" | Examples: {', '.join(examples)}" if examples else "")
            )
    else:
        for lesson_id, lec in data.items():
            chunks.append(f"\n===== LESSON {lesson_id} =====")
            for sec in lec.get("sections", []):
                title = (sec.get("title", {}) or {}).get("en", "")
                body = (sec.get("body", {}) or {}).get("en", "") or ""
                chunks.append(f"## {title}")
                if body:
                    chunks.append(body)
                for ex in sec.get("examples", []):
                    gloss = (ex.get("gloss", {}) or {}).get("en", "")
                    chunks.append(f"  • {ex.get('ar', '')} — {gloss}")
    return "\n".join(chunks)


CURRICULUM_FULL = load_curriculum_text(compact=False)
CURRICULUM_COMPACT = load_curriculum_text(compact=True)

# ─── Gemini context cache for the curriculum ─────────────────────────────────
# The 42-week curriculum is uploaded to Gemini ONCE as a cached context; grounded
# i'rab calls then reference it instead of re-sending ~250k tokens each time.
CURRICULUM_CACHE_FILE = PORTAL_DIR / "curriculum_cache.json"
CURRICULUM_CACHE_TTL = "2592000s"   # 30 days
_cache_build_lock = __import__("threading").Lock()
# system instruction baked into the cache
CURRICULUM_CACHE_SYSTEM = (
    "You are a curriculum-grounded Quranic Arabic grammar assistant. The cached "
    "content is the COMPLETE 42-week curriculum and is your SOLE source of "
    "grammatical knowledge. Use only the terminology, classifications, and rules "
    "that appear in it. Do not introduce concepts absent from this curriculum. "
    "If a verse contains a phenomenon the curriculum does not cover, say so in "
    "that word's notes field."
)


def _cache_meta_load():
    if CURRICULUM_CACHE_FILE.exists():
        try:
            return json.loads(CURRICULUM_CACHE_FILE.read_text())
        except Exception:
            return None
    return None


def _cache_meta_save(meta):
    try:
        CURRICULUM_CACHE_FILE.write_text(json.dumps(meta, indent=2))
    except Exception as e:
        print(f"[cache] meta save failed: {e}", file=sys.stderr)


def build_curriculum_cache():
    """Create (or replace) the Gemini context cache holding the full curriculum.
    Returns the meta dict, or raises on failure."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    if not CURRICULUM_FULL:
        raise RuntimeError("Curriculum (lectures.json) is empty")
    client = genai.Client(api_key=api_key)
    # Delete any previous cache so we don't accrue storage on stale copies
    old = _cache_meta_load()
    if old and old.get("name"):
        try:
            client.caches.delete(name=old["name"])
        except Exception:
            pass
    cache = client.caches.create(
        model=GEMINI_GROUNDED_MODEL,
        config=genai_types.CreateCachedContentConfig(
            contents=[CURRICULUM_FULL],
            system_instruction=CURRICULUM_CACHE_SYSTEM,
            ttl=CURRICULUM_CACHE_TTL,
            display_name="quran-42week-curriculum",
        ),
    )
    from datetime import datetime, timezone, timedelta
    meta = {
        "name": cache.name,
        "model": GEMINI_GROUNDED_MODEL,
        "token_count": getattr(cache.usage_metadata, "total_token_count", None),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "expires_at": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
    }
    _cache_meta_save(meta)
    print(f"[cache] built curriculum cache {cache.name} ({meta['token_count']} tokens)", file=sys.stderr)
    return meta


def get_curriculum_cache():
    """Return the cache meta if a valid, non-expired cache exists for the
    current model; otherwise None."""
    meta = _cache_meta_load()
    if not meta or not meta.get("name"):
        return None
    if meta.get("model") != GEMINI_GROUNDED_MODEL:
        return None
    from datetime import datetime, timezone
    try:
        exp = datetime.fromisoformat(meta["expires_at"])
        if exp <= datetime.now(timezone.utc):
            return None
    except Exception:
        return None
    return meta


def ensure_curriculum_cache():
    """Return a valid cache meta — self-healing: if none exists or it expired,
    rebuild it automatically. Thread-safe so concurrent grounded calls don't
    each kick off a build. Returns None only if the build itself fails."""
    meta = get_curriculum_cache()
    if meta:
        return meta
    with _cache_build_lock:
        # Re-check inside the lock — another thread may have just built it
        meta = get_curriculum_cache()
        if meta:
            return meta
        try:
            return build_curriculum_cache()
        except Exception as e:
            print(f"[cache] auto-rebuild failed: {e}", file=sys.stderr)
            return None


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


@app.route("/<path:filename>")
def static_files(filename):
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


@app.route("/api/irab", methods=["POST"])
@login_required
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

Technical Arabic grammar terms must use the conventional spelling of {response_lang}'s OWN grammar pedagogy — NOT a foreign transliteration:
- {response_lang} = English → academic transliteration: ism, fi'l, harf, fa'il, mubtada, khabar, marfu', mansub, majrur, majzum, mabni, mudaf, idafa, harf jarr, mufrad, jam'.
- {response_lang} = Turkish → standard TURKISH spelling: isim, fiil, harf, fâil, mübteda, haber, merfû', mansûb, mecrûr, meczûm, mebnî, muzâf, izâfet, harf-i cerr, müfred, cemi, kesra (esre), damme (ötre), fetha (üstün), mef'ûlün bih. Do NOT write the English transliteration ("majrur", "marfu'", "ism", "fa'il", "kasra", "idafa", "mufrad") when the language is Turkish — use "mecrûr", "merfû'", "isim", "fâil", "kesra", "izâfet", "müfred".
- {response_lang} = Arabic → Arabic script: اسم، فعل، حرف، فاعل، مبتدأ، خبر، مرفوع، منصوب، مجرور، مجزوم، مبني، مضاف، إضافة.
Apply this to EVERY field that names a grammar term — `type`, `form`, `case_mood`, `role` — and to the prose in `notes`. Translate the explanatory wording around the terms into {response_lang} too.

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

**WRITE the explanatory prose inside `notes` in {response_lang}** — and write the technical grammar terms in their {response_lang}-conventional spelling (see the term table above). Examples of well-written notes in different languages (same content):
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

Write `meaning`, `notes`, `role`, `type`, `form`, `case_mood` (all human-readable text), and every `lesson_refs[].reason` in **{response_lang}**. The example above happens to be in English to illustrate the schema — DO NOT copy its language. If {response_lang} is Turkish, write Turkish. If Arabic, write Arabic. If English, write English. Technical grammar terms must use the {response_lang}-conventional spelling (Turkish: isim, fiil, fâil, merfû', mansûb, mecrûr, mebnî, müfred, izâfet — NOT ism, marfu', majrur, mufrad)."""

    prompt += _lang_trailer(language)

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



# ─── Multi-model I'rab comparison ─────────────────────────────────────────────

def _make_irab_prompt(verse: str, language: str) -> str:
    """Build the standard I'rab prompt. Used by both /api/irab (single model)
    and /api/irab-compare (multi-model side-by-side)."""
    lang_names = {"en": "English", "tr": "Turkish", "ar": "Arabic"}
    response_lang = lang_names.get(language, "English")
    return f"""You are an expert in Quranic Arabic grammar. Analyze Quranic verses word-by-word and return a JSON object. The top-level object contains a verse-wide `translation` and a `words` array; each element of `words` represents one word/particle.

## LANGUAGE — CRITICAL

ALL human-readable text fields MUST be written in **{response_lang}**. This applies to:
- `meaning` (full word meaning)
- `notes` (grammar notes)
- `role` (the descriptive English-style label part — translate the English gloss; keep transliterated Arabic terms in parens unchanged)
- every `reason` inside `lesson_refs`

Technical Arabic grammar terms must use the conventional spelling of {response_lang}'s OWN grammar pedagogy — NOT a foreign transliteration:
- {response_lang} = English → academic transliteration: ism, fi'l, harf, fa'il, mubtada, khabar, marfu', mansub, majrur, majzum, mabni, mudaf, idafa, harf jarr, mufrad, jam'.
- {response_lang} = Turkish → standard TURKISH spelling: isim, fiil, harf, fâil, mübteda, haber, merfû', mansûb, mecrûr, meczûm, mebnî, muzâf, izâfet, harf-i cerr, müfred, cemi, kesra (esre), damme (ötre), fetha (üstün), mef'ûlün bih. Do NOT write the English transliteration ("majrur", "marfu'", "ism", "fa'il", "kasra", "idafa", "mufrad") when the language is Turkish — use "mecrûr", "merfû'", "isim", "fâil", "kesra", "izâfet", "müfred".
- {response_lang} = Arabic → Arabic script: اسم، فعل، حرف، فاعل، مبتدأ، خبر، مرفوع، منصوب، مجرور، مجزوم، مبني، مضاف، إضافة.
Apply this to EVERY field that names a grammar term — `type`, `form`, `case_mood`, `role` — and to the prose in `notes`. Translate the explanatory wording around the terms into {response_lang} too.

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

**WRITE the explanatory prose inside `notes` in {response_lang}** — and write the technical grammar terms in their {response_lang}-conventional spelling (see the term table above). Examples of well-written notes in different languages (same content):
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

Write `meaning`, `notes`, `role`, `type`, `form`, `case_mood` (all human-readable text), and every `lesson_refs[].reason` in **{response_lang}**. The example above happens to be in English to illustrate the schema — DO NOT copy its language. If {response_lang} is Turkish, write Turkish. If Arabic, write Arabic. If English, write English. Technical grammar terms must use the {response_lang}-conventional spelling (Turkish: isim, fiil, fâil, merfû', mansûb, mecrûr, mebnî, müfred, izâfet — NOT ism, marfu', majrur, mufrad).
"""


def _parse_irab_json(raw: str):
    """Robust JSON parse with truncated-array salvage."""
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    for open_ch, close_ch in (("{", "}"), ("[", "]")):
        s, e = raw.find(open_ch), raw.rfind(close_ch)
        if s >= 0 and e > s:
            try:
                return json.loads(raw[s : e + 1])
            except json.JSONDecodeError:
                continue
    if raw.startswith("["):
        last = raw.rfind("},")
        if last > 0:
            try:
                return json.loads(raw[: last + 1] + "]")
            except json.JSONDecodeError:
                pass
    return None


def _run_irab_gemini(prompt: str) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY not set", "model_label": f"Gemini ({GEMINI_MODEL})"}
    try:
        client = genai.Client(api_key=api_key)
        resp = gemini_generate(client,
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=16000,
            ),
        )
        raw = (resp.text or "").strip()
        parsed = _parse_irab_json(raw)
        if not parsed:
            return {"error": "Gemini returned unparseable output", "model_label": f"Gemini ({GEMINI_MODEL})"}
        if isinstance(parsed, list):
            parsed = {"words": parsed}
        parsed["model_label"] = f"Gemini ({GEMINI_MODEL})"
        return parsed
    except Exception as e:
        _, friendly = humanize_gemini_error(e)
        return {"error": friendly, "model_label": f"Gemini ({GEMINI_MODEL})"}


def _run_irab_claude(prompt: str) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY not set", "model_label": "Claude Sonnet 4.6"}
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=16000,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = "".join(b.text for b in msg.content if hasattr(b, "text")).strip()
        if raw.startswith("```"):
            raw = raw.strip("`").lstrip("json").strip()
        parsed = _parse_irab_json(raw)
        if not parsed:
            return {"error": "Claude returned unparseable output", "model_label": "Claude Sonnet 4.6"}
        if isinstance(parsed, list):
            parsed = {"words": parsed}
        parsed["model_label"] = "Claude Sonnet 4.6"
        return parsed
    except Exception as e:
        return {"error": str(e), "model_label": "Claude Sonnet 4.6"}


def _run_irab_openai(prompt: str, model: str = None) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    use_model = model or OPENAI_MODEL
    label = f"ChatGPT ({use_model})"
    if not api_key:
        return {"error": "OPENAI_API_KEY not set — add it to portal/.env to enable ChatGPT.",
                "model_label": label}
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=use_model,
            max_tokens=16000,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        raw = (resp.choices[0].message.content or "").strip()
        parsed = _parse_irab_json(raw)
        if not parsed:
            return {"error": "ChatGPT returned unparseable output", "model_label": label}
        if isinstance(parsed, list):
            parsed = {"words": parsed}
        parsed["model_label"] = label
        return parsed
    except Exception as e:
        return {"error": str(e), "model_label": label}


def _lang_trailer(language: str) -> str:
    """A final language directive appended AFTER the prompt's worked example.
    The example is in English and is the last thing the model reads before
    answering — without this trailer its recency pulls the output to English."""
    lang_names = {"en": "English", "tr": "Turkish", "ar": "Arabic"}
    response_lang = lang_names.get(language, "English")
    if response_lang == "English":
        return ""
    return (
        f"\n\n=====================================================\n"
        f"⚠ FINAL REMINDER — OUTPUT LANGUAGE: {response_lang}\n"
        f"The worked EXAMPLE above is written in English ONLY to show the JSON "
        f"structure. It is NOT a language model to copy. Your actual answer's "
        f"`translation`, `meaning`, `notes`, `role`, `type`, `form`, `case_mood`, and "
        f"every `lesson_refs[].reason` MUST be written in {response_lang}. Technical "
        f"grammar terms use the {response_lang}-conventional spelling — for Turkish "
        f"write isim/fiil/fâil/merfû'/mansûb/mecrûr/mebnî/müfred/izâfet, NOT "
        f"ism/marfu'/majrur/mufrad/idafa. "
        f"Produce the JSON now, with all prose in {response_lang}.\n"
        f"=====================================================\n"
    )


def _grounding_preamble(curriculum_text: str, language: str = "en") -> str:
    """Shared grounding instruction. If curriculum_text is given it's inlined;
    if empty, the curriculum is assumed to be supplied via a context cache."""
    lang_names = {"en": "English", "tr": "Turkish", "ar": "Arabic"}
    response_lang = lang_names.get(language, "English")
    # The curriculum context is in English, which pulls the model toward an
    # English response. Override that loudly, up front, before anything else.
    lang_banner = (
        f"⚠ RESPONSE LANGUAGE: {response_lang}. EVERY human-readable text field "
        f"(`translation`, `meaning`, `notes`, `role`, and each `lesson_refs[].reason`) "
        f"MUST be written in {response_lang}. The curriculum reference material below "
        f"is in English ONLY as source material — DO NOT mirror its language. Your "
        f"output language is {response_lang}, regardless of the curriculum's language. "
        f"Technical grammar terms use the {response_lang}-conventional spelling — for "
        f"Turkish: isim, fiil, fâil, merfû', mansûb, mecrûr, mebnî, müfred, izâfet "
        f"(NOT ism, marfu', majrur, mufrad, idafa).\n\n"
    )
    head = lang_banner + (
        "You are a CURRICULUM-GROUNDED grammar assistant. Analyze the verse using "
        "ONLY the grammatical framework, terminology, rules, and examples taught in "
        "the 42-week curriculum. That curriculum is your SOLE source of knowledge.\n\n"
        "STRICT GROUNDING RULES:\n"
        "- Use only terminology, classifications, and rules present in the curriculum.\n"
        "- Do NOT introduce grammatical concepts or methods absent from the curriculum.\n"
        "- If the verse has a phenomenon the curriculum does not cover, say so in that "
        "word's `notes` field (e.g. \"not covered in the 42-week curriculum\").\n"
        "- Keep the analysis at the level a student of this curriculum would recognize.\n\n"
        "MANDATORY SOURCE TAGGING — add a `source` field to EVERY word object:\n"
        "- `source`: \"curriculum\"  → the word's grammar is fully explained by the "
        "42-week curriculum AND you cite at least one valid `lesson_refs` entry.\n"
        "- `source`: \"outside\"     → your analysis of this word relies on ANY grammar "
        "knowledge, terminology, or rules NOT found in the 42-week curriculum.\n"
        "Be honest and conservative: if you are not certain the curriculum covers it, "
        "tag it \"outside\". The `source` field is REQUIRED on every word.\n\n"
    )
    if curriculum_text:
        return (head
                + "===== 42-WEEK CURRICULUM (your only knowledge source) =====\n"
                + curriculum_text
                + "\n===== END OF CURRICULUM =====\n\n")
    return head


def _audit_grounding(parsed: dict) -> dict:
    """Verify a grounded i'rab result against the real 42-week curriculum.

    - Drops `lesson_refs` whose `lesson_id` does not exist in LESSONS_INDEX
      (catches the model inventing lesson numbers).
    - Reclassifies any word tagged "curriculum" but left with zero valid
      lesson_refs as "outside" — a curriculum claim with no citation is not
      provably grounded.
    - Attaches a `grounding` summary {curriculum, outside, total} so the UI
      can show exactly how much of the analysis is curriculum-backed."""
    if not isinstance(parsed, dict) or parsed.get("error"):
        return parsed
    valid_ids = set(LESSONS_INDEX.keys()) if LESSONS_INDEX else set()
    words = parsed.get("words") or []
    n_curriculum = n_outside = 0
    for w in words:
        if not isinstance(w, dict):
            continue
        refs = w.get("lesson_refs") or []
        kept, dropped = [], []
        for r in refs:
            rid = (r or {}).get("lesson_id")
            (kept if rid in valid_ids else dropped).append(r)
        w["lesson_refs"] = kept
        src = (w.get("source") or "").strip().lower()
        if src not in ("curriculum", "outside"):
            # Model omitted/garbled the tag — infer from citations.
            src = "curriculum" if kept else "outside"
        # A "curriculum" claim with no valid citation is not provably grounded.
        if src == "curriculum" and not kept:
            src = "outside"
        if dropped:
            # Invented lesson IDs are themselves an out-of-curriculum signal.
            src = "outside"
        w["source"] = src
        if src == "curriculum":
            n_curriculum += 1
        else:
            n_outside += 1
    parsed["grounding"] = {
        "curriculum": n_curriculum,
        "outside": n_outside,
        "total": n_curriculum + n_outside,
    }
    return parsed


def _run_irab_gemini_cached(verse: str, language: str, model: str = None) -> dict:
    """Grounded Gemini run. `model` is the user-selected Gemini model (defaults
    to GEMINI_GROUNDED_MODEL). If it matches the model the context cache was
    built for, the cache is used (cheap); otherwise the full curriculum is
    inlined so grounding stays intact for any selected model."""
    use_model = model if model in GROUNDED_MODEL_CHOICES else GEMINI_GROUNDED_MODEL
    short = use_model.replace("gemini-2.5-", "")          # "flash-lite", "flash", "pro"
    label = f"Gemini {short}"
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY not set", "model_label": label}

    cache_meta = ensure_curriculum_cache()   # self-healing — built for GEMINI_GROUNDED_MODEL
    use_cache = bool(cache_meta and cache_meta.get("model") == use_model)
    base_prompt = _make_irab_prompt(verse, language) + _lang_trailer(language)
    try:
        client = genai.Client(api_key=api_key)
        if use_cache:
            # Curriculum lives in the cache — only the verse prompt is sent fresh.
            prompt = _grounding_preamble("", language) + base_prompt
            cfg = genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=16000,
                cached_content=cache_meta["name"],
            )
        else:
            # Selected model has no matching cache — inline the FULL curriculum
            # so grounding is identical, just billed per-request instead.
            prompt = _grounding_preamble(CURRICULUM_FULL, language) + base_prompt
            cfg = genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=16000,
            )
        # Gemini occasionally returns malformed/truncated JSON — retry up to 3x
        parsed = None
        for attempt in range(3):
            resp = gemini_generate(client,model=use_model, contents=prompt, config=cfg)
            raw = (resp.text or "").strip()
            parsed = _parse_irab_json(raw)
            if parsed:
                break
            print(f"[irab-grounded] unparseable output, retry {attempt + 1}/3", file=sys.stderr)
        if not parsed:
            return {"error": "Gemini returned unparseable output after 3 attempts — try again.",
                    "model_label": label}
        if isinstance(parsed, list):
            parsed = {"words": parsed}
        parsed["model_label"] = label + (" ✓cache" if use_cache else " (inline)")
        return _audit_grounding(parsed)
    except Exception as e:
        _, friendly = humanize_gemini_error(e)
        return {"error": friendly, "model_label": label}


@app.post("/api/irab-compare")
@login_required
def irab_compare():
    """Run the same verse through multiple models, side-by-side.
    grounded=true → models are constrained to the 42-week curriculum:
      - Gemini uses the context CACHE (cheap, no re-send)
      - Claude gets the full curriculum inline
      - OpenAI gets the compact curriculum inline (fits its context window)"""
    data = request.get_json() or {}
    verse = (data.get("verse") or "").strip()
    language = data.get("language", "en")
    models = data.get("models") or ["gemini", "claude"]
    grounded = bool(data.get("grounded"))
    gemini_model = data.get("gemini_model")   # user-picked model for the grounded module
    if not verse:
        return jsonify({"error": "verse required"}), 400
    if LESSONS_INDEX is None:
        return jsonify({"error": "lessons_index.json not found"}), 500

    plain_prompt = _make_irab_prompt(verse, language) + _lang_trailer(language)

    if grounded:
        claude_prompt = _grounding_preamble(CURRICULUM_FULL, language) + plain_prompt
        openai_prompt = _grounding_preamble(CURRICULUM_COMPACT, language) + plain_prompt
        runners = {
            "gemini": lambda: _run_irab_gemini_cached(verse, language, gemini_model),
            "claude": lambda: _audit_grounding(_run_irab_claude(claude_prompt)),
            # gpt-4o-mini: high tier-1 rate limits + 128k window — handles the
            # curriculum-injected prompt that gpt-4o's per-request cap rejects.
            "openai": lambda: _audit_grounding(_run_irab_openai(openai_prompt, model="gpt-4o-mini")),
        }
    else:
        runners = {
            "gemini": lambda: _run_irab_gemini(plain_prompt),
            "claude": lambda: _run_irab_claude(plain_prompt),
            "openai": lambda: _run_irab_openai(plain_prompt),
        }
    selected = [m for m in models if m in runners] or ["gemini", "claude"]

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(len(selected), 1)) as ex:
        futures = {m: ex.submit(runners[m]) for m in selected}
        results = {m: f.result() for m, f in futures.items()}
    return jsonify({"results": results})


@app.get("/api/admin/curriculum-cache")
@admin_required
def curriculum_cache_status():
    meta = get_curriculum_cache()
    if meta:
        return jsonify({"status": "active", **meta})
    stale = _cache_meta_load()
    return jsonify({"status": "none", "previous": stale})


@app.post("/api/admin/curriculum-cache/build")
@admin_required
def curriculum_cache_build():
    try:
        meta = build_curriculum_cache()
        return jsonify({"status": "active", **meta})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

EXTRACT_MODELS = ("gemini", "claude", "openai")


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
            print("[extract] ChatGPT can't read PDFs — pick Gemini or Claude for PDF resources.", file=sys.stderr)
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


_EXTRACTORS = {"gemini": _extract_with_gemini, "claude": _extract_with_claude, "openai": _extract_with_openai}


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

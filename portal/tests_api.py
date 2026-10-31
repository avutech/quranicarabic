"""Practice tests, level exams and the Master Exam (multiple choice, graded on the server).

Question banks live in testbank/<L#W#>.json (and optionally testbank/MASTER.json); format in testbank_tool.py.
The browser never receives the correct option or any explanation until a question is finished.

Test kinds
    chapter  20 questions from one chapter's pool, balanced across its topics
    level    20 questions from the 14 chapters of one level (chapters balanced, then topics)
    master   50 questions from MASTER.json (levels balanced, then chapters, then topics)
    drill    10 questions on one topic (opened from a report's "practice this topic" link)

Scoring (per question): 1st try 1.0, 2nd try 0.5, 3rd try 0.25, otherwise 0; using the hint
multiplies by 0.75.  The report separates knowledge ("mastery" = right on the first try, no hint)
from points, so hints and retries never make a topic look weaker than it is.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import random
import re
import threading
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, Response, jsonify, request

from auth import login_required, admin_required, current_user_row
import db as user_db

tests_bp = Blueprint("tests", __name__, url_prefix="/api/tests")

BANK_DIR = Path(__file__).parent / "testbank"
LENGTHS = {"chapter": 20, "level": 20, "master": 50, "drill": 10}
TRY_POINTS = [1.0, 0.5, 0.25]          # points by number of tries used
HINT_FACTOR = 0.75
MAX_TRIES = len(TRY_POINTS)
MIN_RANK = 2                           # a topic needs this many questions to be ranked strong/weak

_lock = threading.Lock()
_cache = {"sig": None, "banks": {}}


# ─── Banks ───────────────────────────────────────────────────────────────────

def load_banks():
    """{chapter_id: bank} with questions indexed; reloads when any file changes."""
    files = sorted(f for f in BANK_DIR.glob("*.json") if re.match(r"(L\dW\d+|MASTER)\.json$", f.name))   # not accepted.json etc.
    sig = tuple((f.name, f.stat().st_mtime_ns) for f in files)
    with _lock:
        if _cache["sig"] == sig:
            return _cache["banks"]
        banks = {}
        for f in files:
            b = json.loads(f.read_text("utf-8"))
            cid = b["chapter"]
            b["topic_by_id"] = {t["id"]: t for t in b["topics"]}
            b["q_by_id"] = {q["id"]: q for q in b["questions"]}
            for q in b["questions"]:
                q.setdefault("chapter", cid if cid != "MASTER" else q.get("chapter"))
            banks[cid] = b
        _cache.update(sig=sig, banks=banks)
        return banks


def find_question(qid):
    for b in load_banks().values():
        if qid in b["q_by_id"]:
            return b["q_by_id"][qid], b
    return None, None


def chapter_level(cid):
    m = re.match(r"L(\d)W(\d+)$", cid or "")
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def topic_info(qid_chapter, topic_id, banks):
    """Title/rule/section of a topic; for MASTER questions the topic lives in its own chapter's bank."""
    b = banks.get(qid_chapter)
    return b["topic_by_id"].get(topic_id) if b else None


# ─── Sampling ────────────────────────────────────────────────────────────────

def count(node):
    return len(node) if isinstance(node, list) else sum(count(c) for c in node.values())


def hsample(n, node, rng, seen):
    """Pick n questions from a nested {key: node} / [questions] tree, spreading evenly across children.

    Leaves prefer questions the student has seen least (so repeated runs rotate through the pool)."""
    if isinstance(node, list):
        order = sorted(node, key=lambda q: (seen.get(q["id"], 0), rng.random()))
        return order[:n]
    caps = {k: count(c) for k, c in node.items() if count(c)}
    take = dict.fromkeys(caps, 0)
    left = min(n, sum(caps.values()))
    while left > 0:
        open_keys = [k for k in caps if take[k] < caps[k]]
        rng.shuffle(open_keys)
        base = max(1, left // len(open_keys))
        for k in open_keys:
            add = min(base, caps[k] - take[k], left)
            take[k] += add
            left -= add
            if left == 0:
                break
    out = []
    for k, m in take.items():
        if m:
            out += hsample(m, node[k], rng, seen)
    return out


def build_tree(questions, levels):
    """Group questions by the given key functions, e.g. [level, chapter, topic]."""
    root = {}
    for q in questions:
        node = root
        for i, key in enumerate(levels):
            k = key(q)
            if i == len(levels) - 1:
                node.setdefault(k, []).append(q)
            else:
                node = node.setdefault(k, {})
    return root


def allowed_chapters(user, banks):
    """Chapters this student is cleared for (same lesson unlocks as the lessons themselves; admins: all)."""
    have = {c for c in banks if c != "MASTER"}
    if user["role"] == "admin":
        return have
    return have & set(user_db.effective_unlocks(user["id"]))


def pool_for(kind, banks, level=None, chapter=None, topic=None, allowed=None):
    """Questions a test may draw from. Level exams and the Master Exam only use chapters in `allowed`."""
    qs = []
    if kind in ("chapter", "drill"):
        b = banks.get(chapter)
        qs = list(b["questions"]) if b else []
        if kind == "drill":
            qs = [q for q in qs if q["topic"] == topic]
    elif kind == "level":
        qs = [q for cid, b in banks.items() if chapter_level(cid)[0] == level and (allowed is None or cid in allowed)
              for q in b["questions"]]
    elif kind == "master":
        b = banks.get("MASTER")
        qs = [q for q in (b["questions"] if b else []) if allowed is None or q.get("chapter") in allowed]
    return qs


def sample_test(kind, banks, rng, seen, level=None, chapter=None, topic=None, allowed=None):
    qs = pool_for(kind, banks, level, chapter, topic, allowed)
    n = LENGTHS[kind]
    if kind == "master":
        tree = build_tree(qs, [lambda q: chapter_level(q["chapter"])[0], lambda q: q["chapter"], lambda q: q["topic"]])
    elif kind == "level":
        tree = build_tree(qs, [lambda q: q["chapter"], lambda q: q["topic"]])
    else:
        tree = build_tree(qs, [lambda q: q["topic"]])
    picked = hsample(n, tree, rng, seen)
    rng.shuffle(picked)
    return picked


# ─── Storage ─────────────────────────────────────────────────────────────────

def init_tables():
    with user_db.db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS tests_attempts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                kind        TEXT NOT NULL,
                scope       TEXT NOT NULL,
                total       INTEGER NOT NULL,
                created_at  TEXT NOT NULL,
                finished_at TEXT,
                points      REAL,
                max_points  REAL
            );
            CREATE INDEX IF NOT EXISTS idx_tests_attempts_user ON tests_attempts(user_id, kind, scope);
            CREATE TABLE IF NOT EXISTS tests_items (
                attempt_id INTEGER NOT NULL REFERENCES tests_attempts(id) ON DELETE CASCADE,
                pos        INTEGER NOT NULL,
                qid        TEXT NOT NULL,
                chapter    TEXT NOT NULL,
                topic      TEXT NOT NULL,
                perm       TEXT NOT NULL,              -- JSON: shown option i = original option perm[i]
                tries      TEXT NOT NULL DEFAULT '[]', -- JSON: shown indexes chosen so far
                hint       INTEGER NOT NULL DEFAULT 0,
                points     REAL NOT NULL DEFAULT 0,
                done       INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (attempt_id, pos)
            );
            CREATE INDEX IF NOT EXISTS idx_tests_items_qid ON tests_items(qid);
            CREATE TABLE IF NOT EXISTS question_reports (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                qid        TEXT NOT NULL,
                note       TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            -- scholar review (admin screen): an approval/comment belongs to one VERSION of a question (content_hash)
            CREATE TABLE IF NOT EXISTS question_reviews (
                qid          TEXT PRIMARY KEY,
                content_hash TEXT NOT NULL,
                reviewer_id  INTEGER REFERENCES users(id) ON DELETE SET NULL,
                approved_at  TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS question_comments (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                qid          TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                user_id      INTEGER REFERENCES users(id) ON DELETE SET NULL,
                body         TEXT NOT NULL,
                resolved     INTEGER NOT NULL DEFAULT 0,
                created_at   TEXT NOT NULL,
                resolved_at  TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_question_comments_qid ON question_comments(qid);
        """)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def seen_counts(conn, user_id):
    rows = conn.execute(
        "SELECT i.qid, COUNT(*) c FROM tests_items i JOIN tests_attempts a ON a.id = i.attempt_id "
        "WHERE a.user_id = ? GROUP BY i.qid", (user_id,)).fetchall()
    return {r["qid"]: r["c"] for r in rows}


def can_open_chapter(user, cid):
    if user["role"] == "admin":
        return True
    return cid in user_db.effective_unlocks(user["id"])


def public_question(q, perm):
    opts = []
    for i in perm:
        o = q["options"][i]
        opts.append({"ar": o["ar"]} if "ar" in o else {"text": o["text"]})
    return {"id": q["id"], "topic": q["topic"], "chapter": q.get("chapter"), "difficulty": q["difficulty"],
            "ref": q["ref"], "quote": q["quote"], "stem": q["stem"], "options": opts}


def reveal(q, perm, tries):
    """Per shown option: its explanation, and whether it is the correct one."""
    return [{"why": q["options"][i]["why"], "correct": i == q["correct"], "tried": k in tries}
            for k, i in enumerate(perm)]


def get_item(conn, attempt_id, pos, user_id):
    a = conn.execute("SELECT * FROM tests_attempts WHERE id = ? AND user_id = ?", (attempt_id, user_id)).fetchone()
    if not a:
        return None, None
    it = conn.execute("SELECT * FROM tests_items WHERE attempt_id = ? AND pos = ?", (attempt_id, pos)).fetchone()
    return a, it


def item_points(tries_used, hint):
    return TRY_POINTS[tries_used - 1] * (HINT_FACTOR if hint else 1.0)


# ─── Endpoints ───────────────────────────────────────────────────────────────

@tests_bp.get("/catalog")
@login_required
def catalog():
    banks = load_banks()
    user = current_user_row()
    chapters = {}
    for cid, b in banks.items():
        if cid == "MASTER":
            continue
        chapters[cid] = {"pool": len(b["questions"]), "open": can_open_chapter(user, cid),
                         "topics": [{"id": t["id"], "title": t["title"], "section": t.get("section"),
                                     "n": sum(1 for q in b["questions"] if q["topic"] == t["id"])} for t in b["topics"]]}
    levels = {str(L): sum(1 for c in chapters if chapter_level(c)[0] == L) for L in (1, 2, 3)}
    cleared = allowed_chapters(user, banks)
    level_info = {str(L): {"exam": levels[str(L)] >= 14,                      # all 14 chapters have question banks
                           "open": any(chapter_level(c)[0] == L for c in cleared),   # student is cleared for >= 1 chapter
                           "cleared": sum(chapter_level(c)[0] == L for c in cleared)} for L in (1, 2, 3)}
    master_pool = len(banks["MASTER"]["questions"]) if "MASTER" in banks else 0
    with user_db.db() as conn:
        best = {}
        for r in conn.execute(
                "SELECT kind, scope, MAX(100.0 * points / max_points) p, COUNT(*) n FROM tests_attempts "
                "WHERE user_id = ? AND finished_at IS NOT NULL AND max_points > 0 GROUP BY kind, scope", (user["id"],)):
            best[f"{r['kind']}:{r['scope']}"] = {"best": round(r["p"]), "attempts": r["n"]}
    return jsonify({"chapters": chapters, "chaptersPerLevel": levels, "levels": level_info,
                    "master": {"pool": master_pool, "open": bool(master_pool and cleared)},
                    "lengths": LENGTHS, "best": best})


@tests_bp.post("/start")
@login_required
def start():
    data = request.get_json(silent=True) or {}
    kind = data.get("kind")
    if kind not in LENGTHS:
        return jsonify({"error": "unknown test kind"}), 400
    user = current_user_row()
    banks = load_banks()
    chapter, topic, level = data.get("chapter"), data.get("topic"), None
    if kind in ("chapter", "drill"):
        if chapter not in banks or chapter == "MASTER":
            return jsonify({"error": "no questions for this chapter yet"}), 404
        if not can_open_chapter(user, chapter):
            return jsonify({"error": "chapter locked"}), 403
        scope = chapter if kind == "chapter" else f"{chapter}:{topic}"
        if kind == "drill" and topic not in banks[chapter]["topic_by_id"]:
            return jsonify({"error": "unknown topic"}), 400
    elif kind == "level":
        level = int(data.get("level") or 0)
        if level not in (1, 2, 3) or sum(chapter_level(c)[0] == level for c in banks) < 14:
            return jsonify({"error": "the level exam opens when all 14 chapters of the level have questions"}), 404
        scope = f"L{level}"
        if not any(chapter_level(c)[0] == level for c in allowed_chapters(user, banks)):
            return jsonify({"error": "level locked"}), 403
    else:
        if "MASTER" not in banks:
            return jsonify({"error": "Master Exam is not available yet"}), 404
        scope = "ALL"
        if not allowed_chapters(user, banks):
            return jsonify({"error": "no unlocked lessons"}), 403
    with user_db.db() as conn:
        seen = seen_counts(conn, user["id"])
        picked = sample_test(kind, banks, random.Random(), seen, level, chapter, topic, allowed_chapters(user, banks))
        if not picked:
            return jsonify({"error": "no questions available"}), 404
        cur = conn.execute("INSERT INTO tests_attempts (user_id, kind, scope, total, created_at) VALUES (?,?,?,?,?)",
                           (user["id"], kind, scope, len(picked), now()))
        aid = cur.lastrowid
        items = []
        for pos, q in enumerate(picked):
            perm = list(range(4))
            random.shuffle(perm)
            conn.execute("INSERT INTO tests_items (attempt_id, pos, qid, chapter, topic, perm) VALUES (?,?,?,?,?,?)",
                         (aid, pos, q["id"], q["chapter"], q["topic"], json.dumps(perm)))
            items.append({"pos": pos, **public_question(q, perm)})
    topics = {}
    for q in picked:
        t = topic_info(q["chapter"], q["topic"], banks)
        topics[f"{q['chapter']}:{q['topic']}"] = {"title": t["title"], "section": t.get("section")}
    return jsonify({"attemptId": aid, "kind": kind, "scope": scope, "total": len(items),
                    "tryPoints": TRY_POINTS, "hintFactor": HINT_FACTOR, "items": items, "topics": topics})


@tests_bp.post("/hint")
@login_required
def hint():
    d = request.get_json(silent=True) or {}
    user = current_user_row()
    with user_db.db() as conn:
        a, it = get_item(conn, d.get("attemptId"), d.get("pos"), user["id"])
        if not it:
            return jsonify({"error": "not found"}), 404
        if it["done"]:
            return jsonify({"error": "question already finished"}), 409
        conn.execute("UPDATE tests_items SET hint = 1 WHERE attempt_id = ? AND pos = ?", (a["id"], it["pos"]))
    t = topic_info(it["chapter"], it["topic"], load_banks())
    return jsonify({"rule": t["rule"], "title": t["title"], "factor": HINT_FACTOR})


@tests_bp.post("/answer")
@login_required
def answer():
    d = request.get_json(silent=True) or {}
    user = current_user_row()
    try:
        choice = int(d.get("choice"))
    except (TypeError, ValueError):
        return jsonify({"error": "bad choice"}), 400
    with user_db.db() as conn:
        a, it = get_item(conn, d.get("attemptId"), d.get("pos"), user["id"])
        if not it:
            return jsonify({"error": "not found"}), 404
        if it["done"]:
            return jsonify({"error": "question already finished"}), 409
        if a["finished_at"]:
            return jsonify({"error": "test already finished"}), 409
        q, _ = find_question(it["qid"])
        perm, tries = json.loads(it["perm"]), json.loads(it["tries"])
        if choice not in range(4) or choice in tries:
            return jsonify({"error": "bad choice"}), 400
        tries.append(choice)
        right = perm[choice] == q["correct"]
        out_of_tries = len(tries) >= MAX_TRIES
        done = right or out_of_tries
        points = item_points(len(tries), it["hint"]) if right else 0.0
        conn.execute("UPDATE tests_items SET tries = ?, points = ?, done = ? WHERE attempt_id = ? AND pos = ?",
                     (json.dumps(tries), points, int(done), a["id"], it["pos"]))
    res = {"correct": right, "done": done, "points": points, "triesUsed": len(tries),
           "chosen": {"index": choice, "why": q["options"][perm[choice]]["why"]}}
    if done:
        res["options"] = reveal(q, perm, tries)
        res["correctIndex"] = perm.index(q["correct"])
    return jsonify(res)


def build_report(conn, attempt, user_id):
    banks = load_banks()
    items = conn.execute("SELECT * FROM tests_items WHERE attempt_id = ? ORDER BY pos", (attempt["id"],)).fetchall()
    cells = {}
    hints = retries = 0
    for it in items:
        tries = json.loads(it["tries"])
        first_try = bool(it["done"]) and len(tries) == 1 and it["points"] > 0 and not it["hint"]
        eventually = it["points"] > 0
        hints += it["hint"]
        retries += max(0, len(tries) - 1)
        c = cells.setdefault((it["chapter"], it["topic"]), {"n": 0, "mastered": 0, "eventually": 0})
        c["n"] += 1
        c["mastered"] += first_try
        c["eventually"] += eventually
    life = {}
    for r in conn.execute(
            "SELECT i.chapter, i.topic, COUNT(*) n, "
            "SUM(CASE WHEN i.done = 1 AND i.hint = 0 AND i.points = 1.0 THEN 1 ELSE 0 END) m "
            "FROM tests_items i JOIN tests_attempts a ON a.id = i.attempt_id "
            "WHERE a.user_id = ? AND i.done = 1 GROUP BY i.chapter, i.topic", (user_id,)):
        life[(r["chapter"], r["topic"])] = {"n": r["n"], "mastery": round(100 * r["m"] / r["n"])}
    topics = []
    for (cid, tid), c in cells.items():
        t = topic_info(cid, tid, banks) or {"title": {"en": tid, "tr": tid}}
        lv, wk = chapter_level(cid)
        topics.append({"chapter": cid, "level": lv, "week": wk, "topic": tid, "title": t["title"],
                       "section": t.get("section"), "n": c["n"], "mastered": c["mastered"],
                       "eventually": c["eventually"], "mastery": round(100 * c["mastered"] / c["n"]),
                       "lifetime": life.get((cid, tid))})
    ranked = sorted((t for t in topics if t["n"] >= MIN_RANK), key=lambda t: (t["mastery"], -t["n"]))
    # a topic can be in only one list; with few topics, weak takes priority
    weak = [t for t in ranked if t["mastery"] < 100][:5]
    strong = [t for t in reversed(ranked) if t not in weak and t["mastery"] >= 50][:3]
    levels = {}
    for t in topics:
        s = levels.setdefault(str(t["level"]), {"n": 0, "mastered": 0})
        s["n"] += t["n"]
        s["mastered"] += t["mastered"]
    for s in levels.values():
        s["mastery"] = round(100 * s["mastered"] / s["n"])
    hist = [{"points": r["points"], "max": r["max_points"], "at": r["finished_at"]} for r in conn.execute(
        "SELECT points, max_points, finished_at FROM tests_attempts WHERE user_id = ? AND kind = ? AND scope = ? "
        "AND finished_at IS NOT NULL AND id != ? ORDER BY id DESC LIMIT 5",
        (user_id, attempt["kind"], attempt["scope"], attempt["id"]))]
    return {"attemptId": attempt["id"], "kind": attempt["kind"], "scope": attempt["scope"],
            "points": attempt["points"], "max": attempt["max_points"],
            "percent": round(100 * attempt["points"] / attempt["max_points"]) if attempt["max_points"] else 0,
            "questions": len(items), "masteredCount": sum(c["mastered"] for c in cells.values()),
            "hintsUsed": hints, "retries": retries, "weak": weak, "strong": strong,
            "topics": sorted(topics, key=lambda t: (t["chapter"], t["topic"])), "levels": levels, "history": hist}


@tests_bp.post("/finish")
@login_required
def finish():
    d = request.get_json(silent=True) or {}
    user = current_user_row()
    with user_db.db() as conn:
        a = conn.execute("SELECT * FROM tests_attempts WHERE id = ? AND user_id = ?",
                         (d.get("attemptId"), user["id"])).fetchone()
        if not a:
            return jsonify({"error": "not found"}), 404
        if not a["finished_at"]:
            pts = conn.execute("SELECT COALESCE(SUM(points), 0) FROM tests_items WHERE attempt_id = ?", (a["id"],)).fetchone()[0]
            conn.execute("UPDATE tests_attempts SET finished_at = ?, points = ?, max_points = ? WHERE id = ?",
                         (now(), pts, float(a["total"]), a["id"]))
            a = conn.execute("SELECT * FROM tests_attempts WHERE id = ?", (a["id"],)).fetchone()
        return jsonify(build_report(conn, a, user["id"]))


@tests_bp.post("/report-question")
@login_required
def report_question():
    d = request.get_json(silent=True) or {}
    note = (d.get("note") or "").strip()[:1000]
    qid = d.get("qid") or ""
    q, _ = find_question(qid)
    if not q or not note:
        return jsonify({"error": "question and note required"}), 400
    with user_db.db() as conn:
        conn.execute("INSERT INTO question_reports (user_id, qid, note, created_at) VALUES (?,?,?,?)",
                     (current_user_row()["id"], qid, note, now()))
    return jsonify({"ok": True})


# ─── Scholar review (admin only) ────────────────────────────────────────────────────────────────
# A scholar goes through every question, approves it or leaves comments.  Both are tied to the question's content
# hash: when we edit a question afterwards its approval no longer counts and old comments are flagged "changed since".

def content_hash(q):
    core = {k: q.get(k) for k in ("stem", "options", "correct", "quote", "ref")}
    return hashlib.sha1(json.dumps(core, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


def _who(conn, uid):
    r = conn.execute("SELECT email, first_name, last_name FROM users WHERE id = ?", (uid,)).fetchone() if uid else None
    if not r:
        return "(deleted user)"
    name = f"{r['first_name'] or ''} {r['last_name'] or ''}".strip()
    return name or r["email"]


def _review_state(conn, qids_hashes):
    """{qid: {approved, approvedBy, approvedAt, comments:[...]}} for [(qid, hash)]."""
    out = {}
    rv = {r["qid"]: r for r in conn.execute("SELECT * FROM question_reviews")}
    cm = {}
    for c in conn.execute("SELECT * FROM question_comments ORDER BY id"):
        cm.setdefault(c["qid"], []).append(c)
    for qid, h in qids_hashes:
        r = rv.get(qid)
        approved = bool(r and r["content_hash"] == h)
        out[qid] = {
            "approved": approved,
            "approvedStale": bool(r and not approved),          # approved an earlier version of the text
            "approvedBy": _who(conn, r["reviewer_id"]) if approved else None,
            "approvedAt": r["approved_at"] if approved else None,
            "comments": [{"id": c["id"], "body": c["body"], "by": _who(conn, c["user_id"]), "at": c["created_at"],
                          "resolved": bool(c["resolved"]), "stale": c["content_hash"] != h} for c in cm.get(qid, [])],
        }
    return out


def _full_question(q, topics, state):
    t = topics.get(q["topic"]) or {}
    return {"id": q["id"], "chapter": q.get("chapter"), "topic": q["topic"], "topicTitle": t.get("title"),
            "difficulty": q["difficulty"], "ref": q["ref"], "quote": q["quote"], "stem": q["stem"],
            "options": [{"ar": o["ar"], "why": o["why"]} if "ar" in o else {"text": o["text"], "why": o["why"]}
                        for o in q["options"]],
            "correct": q["correct"], "review": state}


@tests_bp.get("/review/tree")
@admin_required
def review_tree():
    banks = load_banks()
    with user_db.db() as conn:
        rows = {cid: [(q["id"], content_hash(q)) for q in b["questions"]] for cid, b in banks.items()}
        st = _review_state(conn, [x for v in rows.values() for x in v])
    chapters = {}
    for cid, items in rows.items():
        chapters[cid] = {"total": len(items),
                         "approved": sum(st[i]["approved"] for i, _ in items),
                         "open": sum(1 for i, _ in items for c in st[i]["comments"] if not c["resolved"])}
    return jsonify({"chapters": chapters})


@tests_bp.get("/review/chapter/<cid>")
@admin_required
def review_chapter(cid):
    banks = load_banks()
    b = banks.get(cid)
    if not b:
        return jsonify({"error": "unknown chapter"}), 404
    if cid == "MASTER":                    # a Master question's topic lives in its own chapter's bank
        topics_of = lambda q: banks[q["chapter"]]["topic_by_id"] if q.get("chapter") in banks else {}
        order = lambda q: (q.get("chapter") or "", q["id"])
    else:
        topics_of = lambda q: b["topic_by_id"]
        idx = {t["id"]: i for i, t in enumerate(b["topics"])}
        order = lambda q: (idx.get(q["topic"], 99), q["id"])
    qs = sorted(b["questions"], key=order)
    with user_db.db() as conn:
        st = _review_state(conn, [(q["id"], content_hash(q)) for q in qs])
    return jsonify({"chapter": cid, "questions": [_full_question(q, topics_of(q), st[q["id"]]) for q in qs]})


def _review_target(qid):
    q, _ = find_question(qid)
    return q


@tests_bp.post("/review/<qid>/approve")
@admin_required
def review_approve(qid):
    q = _review_target(qid)
    if not q:
        return jsonify({"error": "unknown question"}), 404
    with user_db.db() as conn:
        conn.execute("INSERT INTO question_reviews (qid, content_hash, reviewer_id, approved_at) VALUES (?,?,?,?) "
                     "ON CONFLICT(qid) DO UPDATE SET content_hash=excluded.content_hash, "
                     "reviewer_id=excluded.reviewer_id, approved_at=excluded.approved_at",
                     (qid, content_hash(q), current_user_row()["id"], now()))
        return jsonify({"ok": True, "review": _review_state(conn, [(qid, content_hash(q))])[qid]})


@tests_bp.post("/review/<qid>/unapprove")
@admin_required
def review_unapprove(qid):
    q = _review_target(qid)
    if not q:
        return jsonify({"error": "unknown question"}), 404
    with user_db.db() as conn:
        conn.execute("DELETE FROM question_reviews WHERE qid = ?", (qid,))
        return jsonify({"ok": True, "review": _review_state(conn, [(qid, content_hash(q))])[qid]})


@tests_bp.post("/review/<qid>/comment")
@admin_required
def review_comment(qid):
    q = _review_target(qid)
    body = ((request.get_json(silent=True) or {}).get("body") or "").strip()[:4000]
    if not q or not body:
        return jsonify({"error": "question and comment required"}), 400
    with user_db.db() as conn:
        conn.execute("INSERT INTO question_comments (qid, content_hash, user_id, body, created_at) VALUES (?,?,?,?,?)",
                     (qid, content_hash(q), current_user_row()["id"], body, now()))
        return jsonify({"ok": True, "review": _review_state(conn, [(qid, content_hash(q))])[qid]})


@tests_bp.post("/review/comment/<int:cid>/resolve")
@admin_required
def review_resolve(cid):
    resolved = bool((request.get_json(silent=True) or {}).get("resolved", True))
    with user_db.db() as conn:
        c = conn.execute("SELECT qid FROM question_comments WHERE id = ?", (cid,)).fetchone()
        q = _review_target(c["qid"]) if c else None
        if not q:
            return jsonify({"error": "unknown comment"}), 404
        conn.execute("UPDATE question_comments SET resolved = ?, resolved_at = ? WHERE id = ?",
                     (1 if resolved else 0, now() if resolved else None, cid))
        return jsonify({"ok": True, "review": _review_state(conn, [(q["id"], content_hash(q))])[q["id"]]})


@tests_bp.delete("/review/comment/<int:cid>")
@admin_required
def review_delete_comment(cid):
    with user_db.db() as conn:
        c = conn.execute("SELECT qid FROM question_comments WHERE id = ?", (cid,)).fetchone()
        q = _review_target(c["qid"]) if c else None
        if not q:
            return jsonify({"error": "unknown comment"}), 404
        conn.execute("DELETE FROM question_comments WHERE id = ?", (cid,))
        return jsonify({"ok": True, "review": _review_state(conn, [(q["id"], content_hash(q))])[q["id"]]})


@tests_bp.get("/review/export")
@admin_required
def review_export():
    """Every comment with its question, as CSV (default) or JSON (?format=json): the worklist for editing the banks."""
    only_open = request.args.get("open") == "1"
    banks = load_banks()
    rows = []
    with user_db.db() as conn:
        for c in conn.execute("SELECT * FROM question_comments ORDER BY qid, id"):
            if only_open and c["resolved"]:
                continue
            q, b = find_question(c["qid"])
            if not q:
                continue
            rows.append({"question_id": q["id"], "chapter": q.get("chapter") or b["chapter"], "topic": q["topic"],
                         "question_en": q["stem"]["en"], "correct_option": "ABCD"[q["correct"]],
                         "comment": c["body"], "by": _who(conn, c["user_id"]), "at": c["created_at"],
                         "status": "resolved" if c["resolved"] else "open",
                         "question_changed_since": c["content_hash"] != content_hash(q)})
    if request.args.get("format") == "json":
        return jsonify({"comments": rows})
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]) if rows else ["question_id", "comment"])
    w.writeheader()
    w.writerows(rows)
    return Response("\ufeff" + buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=question_review_comments.csv"})

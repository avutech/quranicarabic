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

import json
import random
import re
import threading
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, jsonify, request

from auth import login_required, current_user_row
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


def pool_for(kind, banks, level=None, chapter=None, topic=None):
    qs = []
    if kind in ("chapter", "drill"):
        b = banks.get(chapter)
        qs = list(b["questions"]) if b else []
        if kind == "drill":
            qs = [q for q in qs if q["topic"] == topic]
    elif kind == "level":
        qs = [q for cid, b in banks.items() if chapter_level(cid)[0] == level for q in b["questions"]]
    elif kind == "master":
        b = banks.get("MASTER")
        qs = list(b["questions"]) if b else []
    return qs


def sample_test(kind, banks, rng, seen, level=None, chapter=None, topic=None):
    qs = pool_for(kind, banks, level, chapter, topic)
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
    with user_db.db() as conn:
        best = {}
        for r in conn.execute(
                "SELECT kind, scope, MAX(100.0 * points / max_points) p, COUNT(*) n FROM tests_attempts "
                "WHERE user_id = ? AND finished_at IS NOT NULL AND max_points > 0 GROUP BY kind, scope", (user["id"],)):
            best[f"{r['kind']}:{r['scope']}"] = {"best": round(r["p"]), "attempts": r["n"]}
    return jsonify({"chapters": chapters, "chaptersPerLevel": levels,
                    "master": {"pool": len(banks["MASTER"]["questions"]) if "MASTER" in banks else 0},
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
    else:
        if "MASTER" not in banks:
            return jsonify({"error": "Master Exam is not available yet"}), 404
        scope = "ALL"
    with user_db.db() as conn:
        seen = seen_counts(conn, user["id"])
        picked = sample_test(kind, banks, random.Random(), seen, level, chapter, topic)
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

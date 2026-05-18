"""SQLite schema + helpers for users, sessions, and per-user lesson unlocks.

Schema:
    users      (id, email UNIQUE, password_hash, role, created_at, last_login)
    sessions   (token PK, user_id, created_at, expires_at)
    unlocks    (user_id, lesson_id, granted_at)  PRIMARY KEY(user_id, lesson_id)

`role` is 'admin' or 'user'. `lesson_id` is e.g. "L1W3".
"""
from __future__ import annotations

import os
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Iterable, Optional

import bcrypt

DB_PATH = Path(__file__).parent / "users.db"
SESSION_TTL = timedelta(days=30)


# ─── Connection helpers ───────────────────────────────────────────────────────

def _connect() -> sqlite3.Connection:
    # timeout=30: if another thread holds the write lock, wait up to 30s
    # instead of immediately raising "database is locked".
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    # WAL mode lets readers and a writer proceed concurrently — essential when
    # many users (including several sharing one account) hit the server at
    # once. journal_mode is persisted in the DB file; the rest are per-conn.
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn


@contextmanager
def db():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Create tables if they don't exist. Idempotent (also handles light migrations)."""
    with db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role          TEXT NOT NULL DEFAULT 'user',
                created_at    TEXT NOT NULL,
                last_login    TEXT
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token      TEXT PRIMARY KEY,
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);

            CREATE TABLE IF NOT EXISTS unlocks (
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                lesson_id  TEXT NOT NULL,
                granted_at TEXT NOT NULL,
                PRIMARY KEY (user_id, lesson_id)
            );

            CREATE TABLE IF NOT EXISTS classrooms (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS classroom_unlocks (
                classroom_id INTEGER NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
                lesson_id    TEXT NOT NULL,
                granted_at   TEXT NOT NULL,
                PRIMARY KEY (classroom_id, lesson_id)
            );

            CREATE TABLE IF NOT EXISTS module_states (
                module_id  TEXT PRIMARY KEY,
                active     INTEGER NOT NULL DEFAULT 1,
                updated_at TEXT NOT NULL
            );
        """)
        # Migrations
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(users)")}
        if "classroom_id" not in cols:
            conn.execute("ALTER TABLE users ADD COLUMN classroom_id INTEGER REFERENCES classrooms(id) ON DELETE SET NULL")
        if "first_name" not in cols:
            conn.execute("ALTER TABLE users ADD COLUMN first_name TEXT")
        if "last_name" not in cols:
            conn.execute("ALTER TABLE users ADD COLUMN last_name TEXT")


# ─── Password helpers ─────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def check_password(plain: str, hashed: str) -> bool:
    if not plain or not hashed:
        return False
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


# ─── User CRUD ────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_user(email: str, password: str, role: str = "user",
                first_name: str = "", last_name: str = "") -> int:
    """Create a user; returns the new user_id. Raises sqlite3.IntegrityError on dup."""
    email = email.strip().lower()
    if not email or not password:
        raise ValueError("email and password are required")
    first = (first_name or "").strip() or None
    last = (last_name or "").strip() or None
    with db() as conn:
        cur = conn.execute(
            "INSERT INTO users (email, password_hash, role, created_at, first_name, last_name) VALUES (?, ?, ?, ?, ?, ?)",
            (email, hash_password(password), role, now_iso(), first, last),
        )
        return cur.lastrowid


def update_user_name(user_id: int, first_name: str, last_name: str) -> None:
    first = (first_name or "").strip() or None
    last = (last_name or "").strip() or None
    with db() as conn:
        conn.execute("UPDATE users SET first_name = ?, last_name = ? WHERE id = ?",
                     (first, last, user_id))


def display_name(row) -> str:
    """Return 'First Last' if both set, just one if only one is, else email."""
    if row is None:
        return ""
    first = row["first_name"] if "first_name" in row.keys() else None
    last = row["last_name"] if "last_name" in row.keys() else None
    parts = [p for p in (first, last) if p and p.strip()]
    return " ".join(parts) if parts else row["email"]


def find_user_by_email(email: str) -> Optional[sqlite3.Row]:
    with db() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?", (email.strip().lower(),)
        ).fetchone()


def find_user_by_id(user_id: int) -> Optional[sqlite3.Row]:
    with db() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def list_users() -> list[sqlite3.Row]:
    with db() as conn:
        return conn.execute(
            "SELECT id, email, role, created_at, last_login FROM users ORDER BY id"
        ).fetchall()


def delete_user(user_id: int) -> None:
    with db() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))


def update_password(user_id: int, new_password: str) -> None:
    with db() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (hash_password(new_password), user_id),
        )


def touch_last_login(user_id: int) -> None:
    with db() as conn:
        conn.execute("UPDATE users SET last_login = ? WHERE id = ?", (now_iso(), user_id))


# ─── Sessions ─────────────────────────────────────────────────────────────────

def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + SESSION_TTL
    with db() as conn:
        conn.execute(
            "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (token, user_id, now_iso(), expires.isoformat()),
        )
    return token


def session_user(token: Optional[str]) -> Optional[sqlite3.Row]:
    """Look up the user for a session token if it's still valid; expire-cleanup along the way."""
    if not token:
        return None
    with db() as conn:
        row = conn.execute(
            """SELECT u.* FROM sessions s
               JOIN users u ON u.id = s.user_id
               WHERE s.token = ? AND s.expires_at > ?""",
            (token, now_iso()),
        ).fetchone()
        if not row:
            # Best-effort cleanup if it was expired
            conn.execute("DELETE FROM sessions WHERE token = ? AND expires_at <= ?",
                         (token, now_iso()))
        return row


def delete_session(token: str) -> None:
    with db() as conn:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))


# ─── Unlocks ──────────────────────────────────────────────────────────────────

def get_unlocks(user_id: int) -> list[str]:
    with db() as conn:
        rows = conn.execute(
            "SELECT lesson_id FROM unlocks WHERE user_id = ? ORDER BY lesson_id",
            (user_id,),
        ).fetchall()
        return [r["lesson_id"] for r in rows]


def set_unlocks(user_id: int, lesson_ids: Iterable[str]) -> None:
    """Replace the user's full unlock set with the given list."""
    ids = sorted({lid.strip() for lid in lesson_ids if lid and lid.strip()})
    with db() as conn:
        conn.execute("DELETE FROM unlocks WHERE user_id = ?", (user_id,))
        if ids:
            ts = now_iso()
            conn.executemany(
                "INSERT INTO unlocks (user_id, lesson_id, granted_at) VALUES (?, ?, ?)",
                [(user_id, lid, ts) for lid in ids],
            )


def add_unlocks(user_id: int, lesson_ids: Iterable[str]) -> None:
    """Grant additional unlocks (no-op if already granted)."""
    ts = now_iso()
    with db() as conn:
        for lid in lesson_ids:
            lid = lid.strip()
            if not lid:
                continue
            conn.execute(
                "INSERT OR IGNORE INTO unlocks (user_id, lesson_id, granted_at) VALUES (?, ?, ?)",
                (user_id, lid, ts),
            )


def remove_unlocks(user_id: int, lesson_ids: Iterable[str]) -> None:
    with db() as conn:
        for lid in lesson_ids:
            lid = lid.strip()
            if not lid:
                continue
            conn.execute("DELETE FROM unlocks WHERE user_id = ? AND lesson_id = ?", (user_id, lid))


def is_unlocked(user_id: int, lesson_id: str) -> bool:
    with db() as conn:
        row = conn.execute(
            "SELECT 1 FROM unlocks WHERE user_id = ? AND lesson_id = ?",
            (user_id, lesson_id),
        ).fetchone()
        return bool(row)


# ─── Classrooms ───────────────────────────────────────────────────────────────

def list_classrooms() -> list[dict]:
    """Return all classrooms with their unlock count + member count."""
    with db() as conn:
        rows = conn.execute("""
            SELECT c.id, c.name, c.created_at,
                   (SELECT COUNT(*) FROM classroom_unlocks cu WHERE cu.classroom_id = c.id) AS unlock_count,
                   (SELECT COUNT(*) FROM users u WHERE u.classroom_id = c.id) AS member_count
            FROM classrooms c
            ORDER BY c.name
        """).fetchall()
        return [dict(r) for r in rows]


def get_classroom(classroom_id: int) -> Optional[sqlite3.Row]:
    with db() as conn:
        return conn.execute("SELECT * FROM classrooms WHERE id = ?", (classroom_id,)).fetchone()


def create_classroom(name: str) -> int:
    name = (name or "").strip()
    if not name:
        raise ValueError("classroom name required")
    with db() as conn:
        cur = conn.execute(
            "INSERT INTO classrooms (name, created_at) VALUES (?, ?)",
            (name, now_iso()),
        )
        return cur.lastrowid


def rename_classroom(classroom_id: int, new_name: str) -> None:
    new_name = (new_name or "").strip()
    if not new_name:
        raise ValueError("name required")
    with db() as conn:
        conn.execute("UPDATE classrooms SET name = ? WHERE id = ?", (new_name, classroom_id))


def delete_classroom(classroom_id: int) -> None:
    """Delete a classroom; users in it have classroom_id reset to NULL by FK rule."""
    with db() as conn:
        conn.execute("DELETE FROM classrooms WHERE id = ?", (classroom_id,))


def get_classroom_unlocks(classroom_id: int) -> list[str]:
    with db() as conn:
        rows = conn.execute(
            "SELECT lesson_id FROM classroom_unlocks WHERE classroom_id = ? ORDER BY lesson_id",
            (classroom_id,),
        ).fetchall()
        return [r["lesson_id"] for r in rows]


def set_classroom_unlocks(classroom_id: int, lesson_ids: Iterable[str]) -> None:
    ids = sorted({lid.strip() for lid in lesson_ids if lid and lid.strip()})
    with db() as conn:
        conn.execute("DELETE FROM classroom_unlocks WHERE classroom_id = ?", (classroom_id,))
        if ids:
            ts = now_iso()
            conn.executemany(
                "INSERT INTO classroom_unlocks (classroom_id, lesson_id, granted_at) VALUES (?, ?, ?)",
                [(classroom_id, lid, ts) for lid in ids],
            )


def assign_user_to_classroom(user_id: int, classroom_id: Optional[int]) -> None:
    """Set classroom_id (None = unassign)."""
    with db() as conn:
        conn.execute("UPDATE users SET classroom_id = ? WHERE id = ?", (classroom_id, user_id))


def list_classroom_members(classroom_id: int) -> list[sqlite3.Row]:
    with db() as conn:
        return conn.execute(
            "SELECT id, email, role FROM users WHERE classroom_id = ? ORDER BY email",
            (classroom_id,),
        ).fetchall()


def effective_unlocks(user_id: int) -> list[str]:
    """A user's effective unlock set = personal unlocks ∪ their classroom's unlocks."""
    user = find_user_by_id(user_id)
    if not user:
        return []
    personal = set(get_unlocks(user_id))
    classroom_id = user["classroom_id"] if "classroom_id" in user.keys() else None
    if classroom_id:
        personal |= set(get_classroom_unlocks(classroom_id))
    return sorted(personal)


# ─── Module activation ────────────────────────────────────────────────────────
# Modules (the feature areas in REFERENCE_TOPICS — Letters, Verbs, Vocab Quiz,
# I'rab, etc.) are active by default. A row in module_states only exists once an
# admin has explicitly changed a module's state; absence of a row means active.

def get_module_states() -> dict[str, bool]:
    """Return {module_id: active_bool} for every module an admin has touched."""
    with db() as conn:
        rows = conn.execute("SELECT module_id, active FROM module_states").fetchall()
        return {r["module_id"]: bool(r["active"]) for r in rows}


def get_inactive_modules() -> list[str]:
    """Module ids that have been explicitly turned off."""
    with db() as conn:
        rows = conn.execute(
            "SELECT module_id FROM module_states WHERE active = 0 ORDER BY module_id"
        ).fetchall()
        return [r["module_id"] for r in rows]


def set_module_active(module_id: str, active: bool) -> None:
    module_id = (module_id or "").strip()
    if not module_id:
        raise ValueError("module_id required")
    with db() as conn:
        conn.execute(
            """INSERT INTO module_states (module_id, active, updated_at)
               VALUES (?, ?, ?)
               ON CONFLICT(module_id) DO UPDATE SET active = excluded.active,
                                                    updated_at = excluded.updated_at""",
            (module_id, 1 if active else 0, now_iso()),
        )


def is_module_active(module_id: str) -> bool:
    with db() as conn:
        row = conn.execute(
            "SELECT active FROM module_states WHERE module_id = ?", (module_id,)
        ).fetchone()
        return True if row is None else bool(row["active"])


# ─── Seed admin ───────────────────────────────────────────────────────────────

def ensure_seed_admin(email: str = "ahmugur@gmail.com") -> Optional[str]:
    """If the users table is empty, create a seed admin and return the
    randomly-generated initial password (so the caller can print it).
    Returns None if the table already has users."""
    init_db()
    with db() as conn:
        n = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
    if n > 0:
        return None
    initial_pw = os.environ.get("ADMIN_INITIAL_PASSWORD") or secrets.token_urlsafe(12)
    create_user(email, initial_pw, role="admin")
    # Grant admin every lesson by default so they can browse the full curriculum
    all_lessons = [f"L{L}W{W}" for L in (1, 2, 3) for W in range(1, 15)]
    user = find_user_by_email(email)
    if user:
        set_unlocks(user["id"], all_lessons)
    return initial_pw

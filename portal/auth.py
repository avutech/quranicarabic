"""Flask request-level auth helpers: cookie reading, decorators, and
the small public endpoints (/api/auth/login, /api/auth/logout, /api/me)."""
from __future__ import annotations

from functools import wraps
from typing import Optional

from flask import Blueprint, jsonify, request, make_response, g

from db import (
    check_password,
    create_session,
    delete_session,
    find_user_by_email,
    effective_unlocks,
    session_user,
    touch_last_login,
)

SESSION_COOKIE = "qa_session"
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# ─── Request-level helpers ───────────────────────────────────────────────────

def current_user_row():
    """Lazily resolve the user row for the current request (cached on g)."""
    if "_user_cache" in g.__dict__:
        return g._user_cache
    token = request.cookies.get(SESSION_COOKIE)
    user = session_user(token)
    g._user_cache = user
    return user


def current_user_dict() -> Optional[dict]:
    user = current_user_row()
    if not user:
        return None
    return {
        "id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "unlocks": effective_unlocks(user["id"]),
    }


def login_required(fn):
    @wraps(fn)
    def wrapped(*a, **kw):
        if not current_user_row():
            return jsonify({"error": "auth required"}), 401
        return fn(*a, **kw)
    return wrapped


def admin_required(fn):
    @wraps(fn)
    def wrapped(*a, **kw):
        u = current_user_row()
        if not u:
            return jsonify({"error": "auth required"}), 401
        if u["role"] != "admin":
            return jsonify({"error": "admin only"}), 403
        return fn(*a, **kw)
    return wrapped


# ─── Public auth endpoints ───────────────────────────────────────────────────

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    user = find_user_by_email(email)
    if not user or not check_password(password, user["password_hash"]):
        return jsonify({"error": "invalid email or password"}), 401
    token = create_session(user["id"])
    touch_last_login(user["id"])
    resp = make_response(jsonify({
        "id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "unlocks": effective_unlocks(user["id"]),
    }))
    resp.set_cookie(
        SESSION_COOKIE, token,
        httponly=True, samesite="Lax",
        secure=request.is_secure,
        max_age=60 * 60 * 24 * 30,
        path="/",
    )
    return resp


@auth_bp.post("/logout")
def logout():
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        delete_session(token)
    resp = make_response(jsonify({"ok": True}))
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp


@auth_bp.get("/me")
def me():
    u = current_user_dict()
    if not u:
        return jsonify({"authenticated": False}), 200
    return jsonify({"authenticated": True, "user": u})

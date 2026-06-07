import datetime
from typing import List, Optional, Dict, Any
import bcrypt
from database import get_connection


# ─────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_user(name: str, email: str, password: str) -> Optional[Dict]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, hash_password(password), "user")
        )
        conn.commit()
        # First user becomes admin
        count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 1:
            cursor.execute("UPDATE users SET role = 'admin' WHERE email = ?", (email,))
            conn.commit()
        return get_user_by_email(email)
    except Exception:
        return None
    finally:
        conn.close()


def authenticate(email: str, password: str) -> Optional[Dict]:
    conn = get_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND is_active = 1",
            (email,)
        ).fetchone()
        if user and check_password(password, user["password"]):
            conn.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user["id"],)
            )
            conn.commit()
            return dict(user)
        return None
    finally:
        conn.close()


def get_user_by_email(email: str) -> Optional[Dict]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_all_users() -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, name, email, role, plan, created_at, last_login, is_active FROM users ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_user_plan(user_id: int, plan: str) -> bool:
    conn = get_connection()
    try:
        conn.execute("UPDATE users SET plan = ? WHERE id = ?", (plan, user_id))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def count_users() -> int:
    conn = get_connection()
    try:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    finally:
        conn.close()


# ─────────────────────────────────────────────
# SESSIONS & MESSAGES
# ─────────────────────────────────────────────

def create_session(user_id: int, title: str = "New Session", focus: str = None) -> str:
    import uuid
    conn = get_connection()
    session_id = str(uuid.uuid4())[:12]
    try:
        conn.execute(
            "INSERT INTO sessions (id, user_id, title, focus) VALUES (?, ?, ?, ?)",
            (session_id, user_id, title, focus)
        )
        conn.commit()
        return session_id
    finally:
        conn.close()


def add_message(session_id: str, role: str, content: str, focus: str = None, tokens: int = 0):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO messages (session_id, role, content, focus, tokens_used) VALUES (?, ?, ?, ?, ?)",
            (session_id, role, content, focus, tokens)
        )
        conn.execute(
            "UPDATE sessions SET updated_at = CURRENT_TIMESTAMP, message_count = message_count + 1 WHERE id = ?",
            (session_id,)
        )
        conn.commit()
    finally:
        conn.close()


def get_session_messages(session_id: str, limit: int = 50) -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,)
        ).fetchall()
        return [dict(r) for r in rows][-limit:]
    finally:
        conn.close()


def get_user_sessions(user_id: int) -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM sessions WHERE user_id = ? ORDER BY updated_at DESC",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ─────────────────────────────────────────────
# PROVIDERS (LLM MODELS)
# ─────────────────────────────────────────────

def get_all_providers() -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM providers ORDER BY priority").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_active_providers() -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM providers WHERE status = 'active' ORDER BY priority"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_provider_status(provider_id: str, status: str) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE providers SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, provider_id)
        )
        conn.commit()
        return True
    finally:
        conn.close()


def update_provider_rate_limit(provider_id: str, rate_limit: int) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE providers SET rate_limit = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (rate_limit, provider_id)
        )
        conn.commit()
        return True
    finally:
        conn.close()


# ─────────────────────────────────────────────
# AGENTS
# ─────────────────────────────────────────────

def get_all_agents() -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM agents ORDER BY priority").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_active_agents() -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM agents WHERE status = 'active' ORDER BY priority"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_agent_status(agent_id: str, status: str) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE agents SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, agent_id)
        )
        conn.commit()
        return True
    finally:
        conn.close()


def update_agent_provider(agent_id: str, provider_id: str) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE agents SET default_provider = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (provider_id, agent_id)
        )
        conn.commit()
        return True
    finally:
        conn.close()


# ─────────────────────────────────────────────
# CONTACT MESSAGES
# ─────────────────────────────────────────────

def save_contact_message(name: str, email: str, subject: str, message: str) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
            (name, email, subject, message)
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_contact_messages(unread_only: bool = False) -> List[Dict]:
    conn = get_connection()
    try:
        query = "SELECT * FROM contact_messages"
        if unread_only:
            query += " WHERE is_read = 0"
        query += " ORDER BY created_at DESC"
        rows = conn.execute(query).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ─────────────────────────────────────────────
# USAGE LOGS
# ─────────────────────────────────────────────

def log_usage(user_id: int, provider_id: str, agent_id: str,
              tokens: int = 0, latency: float = 0, success: bool = True):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO usage_logs (user_id, provider_id, agent_id, tokens_used, latency_ms, success) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, provider_id, agent_id, tokens, latency, 1 if success else 0)
        )
        conn.commit()
    finally:
        conn.close()


def get_usage_stats() -> Dict:
    conn = get_connection()
    try:
        stats = conn.execute("""
            SELECT
                COUNT(*) as total_requests,
                COALESCE(SUM(tokens_used), 0) as total_tokens,
                COALESCE(AVG(latency_ms), 0) as avg_latency,
                COALESCE(SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END), 0) as failed
            FROM usage_logs
        """).fetchone()
        return dict(stats)
    finally:
        conn.close()


# ─────────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────────

def get_setting(key: str, default: str = "") -> str:
    conn = get_connection()
    try:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default
    finally:
        conn.close()


def set_setting(key: str, value: str) -> bool:
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = CURRENT_TIMESTAMP
        """, (key, value, value))
        conn.commit()
        return True
    finally:
        conn.close()


def get_all_settings() -> Dict:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM settings").fetchall()
        return {r["key"]: r["value"] for r in rows}
    finally:
        conn.close()

"""
DMIT AI Consultant — SQLite tables for chat threads and messages.
Uses the same SQLite database as the rest of the platform.
"""
from __future__ import annotations
import logging
from api.db.connection import get_conn

logger = logging.getLogger(__name__)

_SCHEMA = """
-- Chat threads: one per (session_id, partner_id)
CREATE TABLE IF NOT EXISTS chat_threads (
    id          TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    session_id  TEXT NOT NULL,
    partner_id  TEXT NOT NULL,
    title       TEXT,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    last_active TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_chat_threads_session ON chat_threads(session_id, partner_id);

-- Chat messages: per thread
CREATE TABLE IF NOT EXISTS chat_messages (
    id           TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    thread_id    TEXT NOT NULL REFERENCES chat_threads(id) ON DELETE CASCADE,
    role         TEXT NOT NULL,
    content      TEXT NOT NULL,
    chart_specs  TEXT NOT NULL DEFAULT '[]',
    widget_specs TEXT NOT NULL DEFAULT '[]',
    intent       TEXT,
    agents_used  TEXT,
    created_at   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_chat_messages_thread ON chat_messages(thread_id, created_at);
"""


def init_chat_db() -> None:
    """Create chat tables. Safe to call repeatedly (IF NOT EXISTS)."""
    with get_conn() as conn:
        conn.executescript(_SCHEMA)
        # Idempotent: add title column to existing tables
        try:
            conn.execute("ALTER TABLE chat_threads ADD COLUMN title TEXT")
            conn.commit()
        except Exception:
            pass
        conn.commit()
    logger.info("ChatDB: chat_threads + chat_messages tables ready")


# ── Thread operations ─────────────────────────────────────────────────────────

def get_or_create_thread(session_id: str, partner_id: str) -> str:
    """Return existing thread ID or create a new one."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id FROM chat_threads WHERE session_id=? AND partner_id=? LIMIT 1",
            (session_id, partner_id),
        ).fetchone()
        if row:
            thread_id = row["id"]
            conn.execute(
                "UPDATE chat_threads SET last_active=strftime('%Y-%m-%dT%H:%M:%SZ','now') WHERE id=?",
                (thread_id,),
            )
            conn.commit()
            return thread_id

        conn.execute(
            "INSERT INTO chat_threads (session_id, partner_id) VALUES (?,?)",
            (session_id, partner_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id FROM chat_threads WHERE session_id=? AND partner_id=? LIMIT 1",
            (session_id, partner_id),
        ).fetchone()
        return row["id"]


def get_thread(thread_id: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM chat_threads WHERE id=?", (thread_id,)
        ).fetchone()
    return dict(row) if row else None


# ── Message operations ────────────────────────────────────────────────────────

def save_message(
    thread_id: str,
    role: str,
    content: str,
    chart_specs: list | None = None,
    widget_specs: list | None = None,
    intent: str | None = None,
    agents_used: list | None = None,
) -> str:
    import json
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO chat_messages
               (thread_id, role, content, chart_specs, widget_specs, intent, agents_used)
               VALUES (?,?,?,?,?,?,?)""",
            (
                thread_id,
                role,
                content,
                json.dumps(chart_specs or []),
                json.dumps(widget_specs or []),
                intent,
                json.dumps(agents_used or []),
            ),
        )
        conn.execute(
            "UPDATE chat_threads SET last_active=strftime('%Y-%m-%dT%H:%M:%SZ','now') WHERE id=?",
            (thread_id,),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id FROM chat_messages WHERE thread_id=? ORDER BY created_at DESC LIMIT 1",
            (thread_id,),
        ).fetchone()
    return row["id"] if row else ""


def get_messages(thread_id: str, limit: int = 50) -> list[dict]:
    import json
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM chat_messages WHERE thread_id=? ORDER BY created_at ASC LIMIT ?",
            (thread_id, limit),
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["chart_specs"]  = json.loads(d.get("chart_specs",  "[]") or "[]")
        d["widget_specs"] = json.loads(d.get("widget_specs", "[]") or "[]")
        d["agents_used"]  = json.loads(d.get("agents_used",  "[]") or "[]")
        result.append(d)
    return result


def get_recent_history(thread_id: str, limit: int = 10) -> list[dict]:
    """Last N messages formatted for LLM context."""
    messages = get_messages(thread_id, limit=limit * 2)
    return [{"role": m["role"], "content": m["content"]} for m in messages[-limit:]]


def set_thread_title(thread_id: str, title: str) -> None:
    """Update a thread's display title."""
    with get_conn() as conn:
        conn.execute(
            "UPDATE chat_threads SET title=? WHERE id=?",
            (title[:80], thread_id),
        )
        conn.commit()


def get_thread_title(thread_id: str) -> str | None:
    with get_conn() as conn:
        row = conn.execute("SELECT title FROM chat_threads WHERE id=?", (thread_id,)).fetchone()
    return row["title"] if row else None

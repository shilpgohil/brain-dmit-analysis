"""
SQLite / PostgreSQL persistence for DMIT analysis sessions.
Uses get_conn() from api.db.connection — works with both SQLite (local) and
PostgreSQL/Neon (production).
"""
from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict

from api.db.connection import get_conn


def _json_default(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return {"__type__": "datetime", "value": obj.isoformat()}
    if isinstance(obj, Enum):
        return obj.value
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _json_object_hook(d: Dict[str, Any]) -> Any:
    if isinstance(d, dict) and d.get("__type__") == "datetime":
        return datetime.fromisoformat(d["value"])
    return d


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id         TEXT PRIMARY KEY,
                data       TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def load_all_sessions() -> Dict[str, Any]:
    init_db()
    store: Dict[str, Any] = {}
    with get_conn() as conn:
        rows = conn.execute("SELECT id, data FROM sessions").fetchall()
    for row in rows:
        try:
            store[row["id"]] = json.loads(row["data"], object_hook=_json_object_hook)
        except json.JSONDecodeError:
            continue
    return store


def save_session(session_id: str, session: Dict[str, Any]) -> None:
    init_db()
    payload = json.dumps(session, default=_json_default)
    now = datetime.now().isoformat()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO sessions (id, data, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                data       = excluded.data,
                updated_at = excluded.updated_at
            """,
            (session_id, payload, now),
        )
        conn.commit()


def delete_session(session_id: str) -> None:
    init_db()
    with get_conn() as conn:
        conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn.commit()

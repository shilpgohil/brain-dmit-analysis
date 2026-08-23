"""
Admin CRUD against the admins table.
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from api.db.connection import get_conn


def get_admin_by_email(email: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM admins WHERE email = ? AND is_active = 1", (email,)
        ).fetchone()
    return dict(row) if row else None


def get_admin_by_id(admin_id: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM admins WHERE id = ? AND is_active = 1", (admin_id,)
        ).fetchone()
    return dict(row) if row else None


def create_admin(email: str, password_hash: str, name: str) -> Dict[str, Any]:
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO admins (email, password_hash, name) VALUES (?, ?, ?)",
            (email, password_hash, name),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM admins WHERE email = ?", (email,)).fetchone()
    return dict(row)


def update_admin_password(admin_id: str, new_hash: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE admins SET password_hash = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') "
            "WHERE id = ?",
            (new_hash, admin_id),
        )
        conn.commit()

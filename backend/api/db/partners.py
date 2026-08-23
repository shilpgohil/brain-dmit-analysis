"""
Partner CRUD against the partners table.
"""
from __future__ import annotations
import re
import uuid
from typing import Any, Dict, List, Optional
from api.db.connection import get_conn


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:60]


def _unique_slug(base: str) -> str:
    candidate = _slugify(base)
    with get_conn() as conn:
        existing = {
            row[0]
            for row in conn.execute(
                "SELECT public_slug FROM partners WHERE public_slug LIKE ?",
                (candidate + "%",),
            ).fetchall()
        }
    if candidate not in existing:
        return candidate
    suffix = 2
    while f"{candidate}-{suffix}" in existing:
        suffix += 1
    return f"{candidate}-{suffix}"


def get_partner_by_email(email: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM partners WHERE email = ? AND deleted_at IS NULL", (email,)
        ).fetchone()
    return dict(row) if row else None


def get_partner_by_id(partner_id: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM partners WHERE id = ? AND deleted_at IS NULL", (partner_id,)
        ).fetchone()
    return dict(row) if row else None


def get_partner_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM partners WHERE public_slug = ? AND deleted_at IS NULL AND is_active = 1",
            (slug,),
        ).fetchone()
    return dict(row) if row else None


def list_partners(include_inactive: bool = False) -> List[Dict[str, Any]]:
    clause = "" if include_inactive else "AND is_active = 1"
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT * FROM partners WHERE deleted_at IS NULL {clause} ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def create_partner(
    *,
    email: str,
    password_hash: str,
    name: str,
    centre_name: str = "",
    phone: str = "",
    city: str = "",
    state: str = "",
    plan_id: Optional[str] = None,
    allocated_by: Optional[str] = None,
    notes: str = "",
) -> Dict[str, Any]:
    slug = _unique_slug(f"{name}-{centre_name or 'dmit'}")
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO partners
              (email, password_hash, name, centre_name, phone, city, state,
               plan_id, allocated_by, notes, public_slug)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (email, password_hash, name, centre_name, phone, city, state,
             plan_id, allocated_by, notes, slug),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM partners WHERE email = ?", (email,)).fetchone()
    return dict(row)


def update_partner(partner_id: str, **fields) -> None:
    allowed = {"name", "centre_name", "phone", "city", "state", "plan_id",
               "is_active", "notes", "photo_url", "onboarding_completed"}
    sets = {k: v for k, v in fields.items() if k in allowed}
    if not sets:
        return
    sql = ", ".join(f"{k} = ?" for k in sets)
    with get_conn() as conn:
        conn.execute(
            f"UPDATE partners SET {sql}, updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') "
            f"WHERE id = ?",
            (*sets.values(), partner_id),
        )
        conn.commit()


def soft_delete_partner(partner_id: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE partners SET deleted_at = strftime('%Y-%m-%dT%H:%M:%SZ','now'), "
            "is_active = 0 WHERE id = ?",
            (partner_id,),
        )
        conn.commit()


def update_partner_password(partner_id: str, new_hash: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE partners SET password_hash = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') "
            "WHERE id = ?",
            (new_hash, partner_id),
        )
        conn.commit()

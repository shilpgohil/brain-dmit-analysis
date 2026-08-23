"""
Public endpoints (no auth): report QR view, partner intake form.
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.db.connection import get_conn
from api.db.partners import get_partner_by_slug
from api.store import session_store

router = APIRouter(prefix="/public", tags=["public"])


# ── Report QR landing ─────────────────────────────────────────────────────

@router.get("/report/{token}")
async def get_public_report(token: str):
    """Called when someone scans the QR on a printed DMIT report."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM session_reports WHERE public_token = ?", (token,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Report not found")
    report = dict(row)

    # Check expiry
    if report.get("expires_at"):
        from datetime import datetime, timezone
        exp = datetime.fromisoformat(report["expires_at"].replace("Z", "+00:00"))
        if datetime.now(timezone.utc) > exp:
            return {"status": "expired", "message": "This report link has expired."}

    # Increment view count
    with get_conn() as conn:
        conn.execute(
            "UPDATE session_reports SET view_count = view_count + 1, "
            "last_viewed_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') WHERE public_token = ?",
            (token,),
        )
        conn.commit()

    # Load session data for display
    session = session_store.get(report["session_id"])
    if not session:
        raise HTTPException(status_code=404, detail="Session data not available")

    # Load partner info (scrubbed)
    with get_conn() as conn:
        partner_row = conn.execute(
            "SELECT name, centre_name, city, state FROM partners WHERE id = ?",
            (report["partner_id"],),
        ).fetchone()
    partner_info = dict(partner_row) if partner_row else {}

    # Return scrubbed public view
    return {
        "status": "valid",
        "subject_name": session.get("subject_name", "Subject"),
        "analysis_date": report["generated_at"][:10],
        "report_valid_until": report.get("expires_at", "")[:10] if report.get("expires_at") else None,
        "view_count": report["view_count"] + 1,
        "analysed_by": {
            "name": partner_info.get("name", ""),
            "centre": partner_info.get("centre_name", ""),
            "city": partner_info.get("city", ""),
        },
        # Summarised results — parse quotients from JSON string if present
        "quotients": __import__("json").loads(report["quotients_json"]) if report.get("quotients_json") else None,
        "finger_count": session.get("finger_count", 0),
    }


# ── Partner QR intake landing ─────────────────────────────────────────────

@router.get("/partner/{slug}/intake")
async def get_partner_intake_page(slug: str):
    """Returns partner's public profile for the intake QR landing page."""
    partner = get_partner_by_slug(slug)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {
        "id": partner["id"],
        "name": partner["name"],
        "centre_name": partner.get("centre_name"),
        "city": partner.get("city"),
        "state": partner.get("state"),
        "phone": partner.get("phone"),
    }


class IntakeRequest(BaseModel):
    subject_name: str
    subject_age: Optional[int] = None
    subject_phone: Optional[str] = None
    purpose: Optional[str] = None
    note: Optional[str] = None


@router.post("/partner/{slug}/intake", status_code=201)
async def submit_intake_request(slug: str, body: IntakeRequest):
    """Client submits their details via the partner's QR card intake form."""
    partner = get_partner_by_slug(slug)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO intake_requests (partner_id, subject_name, subject_age, subject_phone, purpose, note) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (partner["id"], body.subject_name, body.subject_age,
             body.subject_phone, body.purpose, body.note),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id FROM intake_requests WHERE partner_id = ? ORDER BY submitted_at DESC LIMIT 1",
            (partner["id"],),
        ).fetchone()
    return {"ok": True, "intake_id": row[0] if row else None}


# ── Partner requests (public interest form) ───────────────────────────────

class PartnerInterestRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    centre_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    plan_interest: Optional[str] = None
    message: Optional[str] = None


@router.post("/request-access", status_code=201)
async def submit_partner_request(body: PartnerInterestRequest):
    """Public interest form submission → lands in admin's pending requests."""
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO partner_requests (name, email, phone, centre_name, city, state, plan_interest, message) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (body.name, body.email, body.phone, body.centre_name,
             body.city, body.state, body.plan_interest, body.message),
        )
        conn.commit()
    return {"ok": True, "message": "Request received. We'll be in touch within 24 hours."}

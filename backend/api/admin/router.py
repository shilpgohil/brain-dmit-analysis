"""
Admin management: partners, plans, features, requests.
All routes require admin JWT scope.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.auth.dependencies import get_current_admin
from api.auth.security import hash_password
from api.db.partners import (
    create_partner, get_partner_by_id, list_partners,
    update_partner, soft_delete_partner,
)
from api.db.features import (
    list_features, list_plans, get_plan_features,
    upsert_plan_feature, set_partner_override, remove_partner_override,
    list_partner_overrides, seed_features_and_plans,
)
from api.db.connection import get_conn
from api.store import session_store

router = APIRouter(prefix="/admin", tags=["admin"])


# ── Partner management ────────────────────────────────────────────────────

class CreatePartnerRequest(BaseModel):
    email: str
    password: str
    name: str
    centre_name: str = ""
    phone: str = ""
    city: str = ""
    state: str = ""
    plan_id: Optional[str] = None
    notes: str = ""


class UpdatePartnerRequest(BaseModel):
    name: Optional[str] = None
    centre_name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    plan_id: Optional[str] = None
    notes: Optional[str] = None


@router.get("/partners")
async def list_all_partners(
    include_inactive: bool = False,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    partners = list_partners(include_inactive=include_inactive)
    # Attach session count per partner
    with get_conn() as conn:
        counts = {
            row[0]: row[1]
            for row in conn.execute(
                "SELECT partner_id, COUNT(*) FROM sessions WHERE partner_id IS NOT NULL GROUP BY partner_id"
            ).fetchall()
        }
    for p in partners:
        p["session_count"] = counts.get(p["id"], 0)
        p.pop("password_hash", None)
    return partners


@router.get("/partners/{partner_id}")
async def get_partner_detail(
    partner_id: str,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    partner = get_partner_by_id(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    partner.pop("password_hash", None)
    partner["overrides"] = list_partner_overrides(partner_id)
    return partner


@router.post("/partners", status_code=201)
async def create_new_partner(
    body: CreatePartnerRequest,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    partner = create_partner(
        email=body.email,
        password_hash=hash_password(body.password),
        name=body.name,
        centre_name=body.centre_name,
        phone=body.phone,
        city=body.city,
        state=body.state,
        plan_id=body.plan_id,
        allocated_by=admin["id"],
        notes=body.notes,
    )
    partner.pop("password_hash", None)
    _audit(admin["id"], "partner.create", "partner", partner["id"], new_value={"email": body.email})
    return partner


@router.patch("/partners/{partner_id}")
async def update_partner_detail(
    partner_id: str,
    body: UpdatePartnerRequest,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    partner = get_partner_by_id(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    fields = body.model_dump(exclude_none=True)
    if fields:
        update_partner(partner_id, **fields)
        _audit(admin["id"], "partner.update", "partner", partner_id, new_value=fields)
    return {"ok": True}


@router.patch("/partners/{partner_id}/activate")
async def activate_partner(partner_id: str, admin: Dict[str, Any] = Depends(get_current_admin)):
    update_partner(partner_id, is_active=1)
    _audit(admin["id"], "partner.activate", "partner", partner_id)
    return {"ok": True}


@router.patch("/partners/{partner_id}/deactivate")
async def deactivate_partner(partner_id: str, admin: Dict[str, Any] = Depends(get_current_admin)):
    update_partner(partner_id, is_active=0)
    _audit(admin["id"], "partner.deactivate", "partner", partner_id)
    return {"ok": True}


@router.delete("/partners/{partner_id}", status_code=204)
async def delete_partner(partner_id: str, admin: Dict[str, Any] = Depends(get_current_admin)):
    soft_delete_partner(partner_id)
    _audit(admin["id"], "partner.delete", "partner", partner_id)


# ── Feature overrides ──────────────────────────────────────────────────────

class OverrideRequest(BaseModel):
    feature_id: str
    feature_value: str
    reason: str = ""
    expires_at: Optional[str] = None


@router.put("/partners/{partner_id}/features")
async def set_feature_override(
    partner_id: str,
    body: OverrideRequest,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    set_partner_override(
        partner_id, body.feature_id, body.feature_value,
        admin["id"], body.reason, body.expires_at,
    )
    _audit(admin["id"], "feature.override", "partner", partner_id,
           new_value={"feature_id": body.feature_id, "value": body.feature_value})
    return {"ok": True}


@router.delete("/partners/{partner_id}/features/{feature_id}", status_code=204)
async def remove_feature_override(
    partner_id: str, feature_id: str,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    remove_partner_override(partner_id, feature_id)
    _audit(admin["id"], "feature.override.remove", "partner", partner_id)


# ── Plan management ───────────────────────────────────────────────────────

class CreatePlanRequest(BaseModel):
    name: str
    display_name: str
    description: str = ""
    color_hex: str = "#6b7280"
    sort_order: int = 0


class UpsertPlanFeatureRequest(BaseModel):
    feature_id: str
    feature_value: str


@router.get("/plans")
async def get_plans(admin: Dict[str, Any] = Depends(get_current_admin)):
    return list_plans()


@router.get("/plans/{plan_id}/features")
async def get_plan_features_detail(
    plan_id: str,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    return get_plan_features(plan_id)


@router.post("/plans", status_code=201)
async def create_plan(body: CreatePlanRequest, admin: Dict[str, Any] = Depends(get_current_admin)):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO plans (name, display_name, description, color_hex, sort_order, created_by) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (body.name, body.display_name, body.description, body.color_hex, body.sort_order, admin["id"]),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM plans WHERE name = ?", (body.name,)).fetchone()
    _audit(admin["id"], "plan.create", "plan", row["id"])
    return dict(row)


@router.put("/plans/{plan_id}/features")
async def update_plan_feature(
    plan_id: str,
    body: UpsertPlanFeatureRequest,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    upsert_plan_feature(plan_id, body.feature_id, body.feature_value, admin["id"])
    _audit(admin["id"], "plan.feature.update", "plan", plan_id,
           new_value={"feature_id": body.feature_id, "value": body.feature_value})
    return {"ok": True}


# ── Feature catalog ───────────────────────────────────────────────────────

@router.get("/features")
async def get_features(admin: Dict[str, Any] = Depends(get_current_admin)):
    return list_features()


# ── Partner requests (interest form) ─────────────────────────────────────

@router.get("/requests")
async def list_partner_requests(
    status_filter: str = "pending",
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM partner_requests WHERE status = ? ORDER BY submitted_at DESC",
            (status_filter,),
        ).fetchall()
    return [dict(r) for r in rows]


class ApproveRequestBody(BaseModel):
    password: str
    plan_id: Optional[str] = None


@router.post("/requests/{request_id}/approve", status_code=201)
async def approve_partner_request(
    request_id: str,
    body: ApproveRequestBody,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    with get_conn() as conn:
        req = conn.execute(
            "SELECT * FROM partner_requests WHERE id = ?", (request_id,)
        ).fetchone()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    req = dict(req)
    partner = create_partner(
        email=req["email"],
        password_hash=hash_password(body.password),
        name=req["name"],
        centre_name=req.get("centre_name", ""),
        phone=req.get("phone", ""),
        city=req.get("city", ""),
        state=req.get("state", ""),
        plan_id=body.plan_id,
        allocated_by=admin["id"],
    )
    now = "strftime('%Y-%m-%dT%H:%M:%SZ','now')"
    with get_conn() as conn:
        conn.execute(
            "UPDATE partner_requests SET status = 'approved', reviewed_by = ?, "
            f"reviewed_at = {now}, created_partner_id = ? WHERE id = ?",
            (admin["id"], partner["id"], request_id),
        )
        conn.commit()
    partner.pop("password_hash", None)
    return partner


@router.patch("/requests/{request_id}/reject", status_code=204)
async def reject_partner_request(
    request_id: str,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    with get_conn() as conn:
        conn.execute(
            "UPDATE partner_requests SET status = 'rejected', reviewed_by = ?, "
            "reviewed_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') WHERE id = ?",
            (admin["id"], request_id),
        )
        conn.commit()


# ── Dashboard overview ────────────────────────────────────────────────────

@router.get("/dashboard")
async def admin_dashboard(admin: Dict[str, Any] = Depends(get_current_admin)):
    with get_conn() as conn:
        total_partners   = conn.execute("SELECT COUNT(*) FROM partners WHERE deleted_at IS NULL").fetchone()[0]
        active_partners  = conn.execute("SELECT COUNT(*) FROM partners WHERE is_active = 1 AND deleted_at IS NULL").fetchone()[0]
        total_sessions   = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        pending_requests = conn.execute("SELECT COUNT(*) FROM partner_requests WHERE status = 'pending'").fetchone()[0]
        today_sessions   = conn.execute(
            "SELECT COUNT(*) FROM sessions WHERE substr(data, 1, 1) = '{' AND "
            "updated_at >= date('now')"
        ).fetchone()[0]
    return {
        "total_partners": total_partners,
        "active_partners": active_partners,
        "total_sessions": total_sessions,
        "pending_requests": pending_requests,
        "today_sessions": today_sessions,
    }


# ── Utility ───────────────────────────────────────────────────────────────

def _audit(
    actor_id: str, action: str,
    target_type: str | None = None,
    target_id: str | None = None,
    old_value: Any = None,
    new_value: Any = None,
) -> None:
    import json
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO audit_logs (actor_id, actor_type, action, target_type, target_id, old_value, new_value) "
            "VALUES (?, 'admin', ?, ?, ?, ?, ?)",
            (actor_id, action, target_type, target_id,
             json.dumps(old_value) if old_value else None,
             json.dumps(new_value) if new_value else None),
        )
        conn.commit()

"""
Partner auth endpoints: POST /auth/login|refresh|logout|me|change-password
"""
from __future__ import annotations
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, EmailStr

from api.auth.security import (
    verify_password, create_access_token, create_refresh_token,
    decode_refresh_token, generate_public_token, hash_password,
    REFRESH_TTL_DAYS,
)
from api.auth.dependencies import get_current_partner
from api.db.admins import get_admin_by_email, get_admin_by_id
from api.db.partners import get_partner_by_email, get_partner_by_id, update_partner_password
from api.db.features import get_effective_features
from api.db.connection import get_conn

router = APIRouter(prefix="/auth", tags=["auth"])
_COOKIE = "partner_refresh_token"
_COOKIE_PATH = "/api/auth"
_SECURE = os.getenv("ENVIRONMENT", "development") == "production"


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


def _set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=_COOKIE,
        value=token,
        httponly=True,
        secure=_SECURE,
        samesite="none" if _SECURE else "lax",
        path=_COOKIE_PATH,
        max_age=REFRESH_TTL_DAYS * 86400,
    )


def _store_refresh(jti: str, user_id: str, user_type: str) -> None:
    exp = (datetime.now(timezone.utc) + timedelta(days=REFRESH_TTL_DAYS)).isoformat()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO refresh_tokens (jti, user_id, user_type, expires_at) VALUES (?, ?, ?, ?)",
            (jti, user_id, user_type, exp),
        )
        conn.commit()


def _revoke_refresh(jti: str) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE refresh_tokens SET is_revoked = 1 WHERE jti = ?", (jti,))
        conn.commit()


# ── Partner login ─────────────────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
async def partner_login(body: LoginRequest, response: Response):
    partner = get_partner_by_email(body.email)
    if not partner or not verify_password(body.password, partner["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not partner["is_active"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account deactivated")

    access_token, _ = create_access_token(partner["id"], "partner")
    refresh_token, jti = create_refresh_token(partner["id"], "partner")
    _store_refresh(jti, partner["id"], "partner")
    _set_refresh_cookie(response, refresh_token)
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
async def partner_refresh(request: Request, response: Response):
    token = request.cookies.get(_COOKIE)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")
    try:
        payload = decode_refresh_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if payload.get("scope") != "partner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # Check not revoked
    with get_conn() as conn:
        row = conn.execute(
            "SELECT is_revoked FROM refresh_tokens WHERE jti = ?", (payload["jti"],)
        ).fetchone()
    if not row or row[0]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    partner = get_partner_by_id(payload["sub"])
    if not partner or not partner["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    _revoke_refresh(payload["jti"])
    access_token, _ = create_access_token(partner["id"], "partner")
    new_refresh, new_jti = create_refresh_token(partner["id"], "partner")
    _store_refresh(new_jti, partner["id"], "partner")
    _set_refresh_cookie(response, new_refresh)
    return TokenResponse(access_token=access_token)


@router.post("/logout", status_code=204)
async def partner_logout(request: Request, response: Response):
    token = request.cookies.get(_COOKIE)
    if token:
        try:
            payload = decode_refresh_token(token)
            _revoke_refresh(payload.get("jti", ""))
        except Exception:
            pass
    response.delete_cookie(_COOKIE, path=_COOKIE_PATH)


@router.get("/me")
async def partner_me(partner: Dict[str, Any] = Depends(get_current_partner)):
    features = get_effective_features(partner["id"])
    return {
        "user": {
            "id": partner["id"],
            "email": partner["email"],
            "name": partner["name"],
            "centre_name": partner.get("centre_name"),
            "phone": partner.get("phone"),
            "city": partner.get("city"),
            "state": partner.get("state"),
            "public_slug": partner.get("public_slug"),
            "plan_id": partner.get("plan_id"),
            "onboarding_completed": bool(partner.get("onboarding_completed")),
        },
        "features": features,
    }


@router.post("/change-password", status_code=204)
async def partner_change_password(
    body: ChangePasswordRequest,
    partner: Dict[str, Any] = Depends(get_current_partner),
):
    if not verify_password(body.current_password, partner["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password incorrect")
    update_partner_password(partner["id"], hash_password(body.new_password))


@router.post("/onboarding/complete", status_code=204)
async def complete_onboarding(partner: Dict[str, Any] = Depends(get_current_partner)):
    from api.db.partners import update_partner
    update_partner(partner["id"], onboarding_completed=1)

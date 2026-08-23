"""
Admin auth endpoints: POST /admin/auth/login|refresh|logout|me|change-password
"""
from __future__ import annotations
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel

from api.auth.security import (
    verify_password, create_access_token, create_refresh_token,
    decode_refresh_token, hash_password, REFRESH_TTL_DAYS,
)
from api.auth.dependencies import get_current_admin
from api.db.admins import get_admin_by_email, get_admin_by_id, update_admin_password
from api.db.connection import get_conn

router = APIRouter(prefix="/admin/auth", tags=["admin-auth"])
_COOKIE = "admin_refresh_token"
_COOKIE_PATH = "/api/admin/auth"
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


def _set_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=_COOKIE, value=token, httponly=True,
        secure=_SECURE, samesite="none" if _SECURE else "lax",
        path=_COOKIE_PATH, max_age=REFRESH_TTL_DAYS * 86400,
    )


def _store(jti: str, admin_id: str) -> None:
    exp = (datetime.now(timezone.utc) + timedelta(days=REFRESH_TTL_DAYS)).isoformat()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO refresh_tokens (jti, user_id, user_type, expires_at) VALUES (?, ?, 'admin', ?)",
            (jti, admin_id, exp),
        )
        conn.commit()


def _revoke(jti: str) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE refresh_tokens SET is_revoked = 1 WHERE jti = ?", (jti,))
        conn.commit()


@router.post("/login", response_model=TokenResponse)
async def admin_login(body: LoginRequest, response: Response):
    admin = get_admin_by_email(body.email)
    if not admin or not verify_password(body.password, admin["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token, _ = create_access_token(admin["id"], "admin")
    refresh_token, jti = create_refresh_token(admin["id"], "admin")
    _store(jti, admin["id"])
    _set_cookie(response, refresh_token)
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
async def admin_refresh(request: Request, response: Response):
    token = request.cookies.get(_COOKIE)
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")
    try:
        payload = decode_refresh_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if payload.get("scope") != "admin":
        raise HTTPException(status_code=403)
    with get_conn() as conn:
        row = conn.execute(
            "SELECT is_revoked FROM refresh_tokens WHERE jti = ?", (payload["jti"],)
        ).fetchone()
    if not row or row[0]:
        raise HTTPException(status_code=401, detail="Token revoked")
    admin = get_admin_by_id(payload["sub"])
    if not admin:
        raise HTTPException(status_code=401)
    _revoke(payload["jti"])
    access_token, _ = create_access_token(admin["id"], "admin")
    new_refresh, new_jti = create_refresh_token(admin["id"], "admin")
    _store(new_jti, admin["id"])
    _set_cookie(response, new_refresh)
    return TokenResponse(access_token=access_token)


@router.post("/logout", status_code=204)
async def admin_logout(request: Request, response: Response):
    token = request.cookies.get(_COOKIE)
    if token:
        try:
            payload = decode_refresh_token(token)
            _revoke(payload.get("jti", ""))
        except Exception:
            pass
    response.delete_cookie(_COOKIE, path=_COOKIE_PATH)


@router.get("/me")
async def admin_me(admin: Dict[str, Any] = Depends(get_current_admin)):
    return {
        "id": admin["id"],
        "email": admin["email"],
        "name": admin["name"],
        "role": "admin",
    }


@router.post("/change-password", status_code=204)
async def admin_change_password(
    body: ChangePasswordRequest,
    admin: Dict[str, Any] = Depends(get_current_admin),
):
    if not verify_password(body.current_password, admin["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password incorrect")
    update_admin_password(admin["id"], hash_password(body.new_password))

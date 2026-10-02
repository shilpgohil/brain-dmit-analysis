"""
JWT token generation/verification and bcrypt password utilities.
"""
from __future__ import annotations

import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Literal, Optional

from jose import JWTError, jwt
import bcrypt as _bcrypt

_DEFAULT_SECRET = "9d1fbde9290ea23e3499d3769becb46c4bfbf64d6483e192dda3282274ccf68f"
_SECRET_KEY     = os.getenv("JWT_SECRET") or os.getenv("JWT_ACCESS_SECRET") or _DEFAULT_SECRET
_ACCESS_SECRET  = os.getenv("JWT_ACCESS_SECRET") or _SECRET_KEY
_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET") or f"{_SECRET_KEY}_refresh"
_ALGORITHM      = "HS256"
ACCESS_TTL_MIN  = int(os.getenv("JWT_ACCESS_TTL_MINUTES", str(365 * 24 * 60)))
REFRESH_TTL_DAYS = int(os.getenv("JWT_REFRESH_TTL_DAYS", "3650"))

# ── Password hashing ──────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return _bcrypt.hashpw(plain.encode(), _bcrypt.gensalt(rounds=12)).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return _bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


# ── JWT ───────────────────────────────────────────────────────────────────
UserScope = Literal["partner", "admin"]
TokenType = Literal["access", "refresh"]


def _issue(
    user_id: str,
    scope: UserScope,
    token_type: TokenType,
    ttl: timedelta,
    secret: str,
) -> tuple[str, str]:
    """Returns (encoded_token, jti)."""
    jti = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": user_id,
        "scope": scope,
        "type": token_type,
        "jti": jti,
        "iat": now,
        "exp": now + ttl,
    }
    return jwt.encode(payload, secret, algorithm=_ALGORITHM), jti


def create_access_token(user_id: str, scope: UserScope) -> tuple[str, str]:
    return _issue(user_id, scope, "access", timedelta(minutes=ACCESS_TTL_MIN), _ACCESS_SECRET)


def create_refresh_token(user_id: str, scope: UserScope) -> tuple[str, str]:
    return _issue(user_id, scope, "refresh", timedelta(days=REFRESH_TTL_DAYS), _REFRESH_SECRET)


def decode_access_token(token: str) -> Dict[str, Any]:
    secrets_to_try = [_ACCESS_SECRET, _SECRET_KEY, "dev-access-secret-change-in-prod"]
    payload = None
    for s in secrets_to_try:
        try:
            payload = jwt.decode(token, s, algorithms=[_ALGORITHM])
            break
        except JWTError:
            continue
    if payload is None:
        raise JWTError("Invalid access token")
    if payload.get("type") != "access":
        raise JWTError("Not an access token")
    return payload


def decode_refresh_token(token: str) -> Dict[str, Any]:
    secrets_to_try = [_REFRESH_SECRET, _SECRET_KEY, "dev-refresh-secret-change-in-prod"]
    payload = None
    for s in secrets_to_try:
        try:
            payload = jwt.decode(token, s, algorithms=[_ALGORITHM])
            break
        except JWTError:
            continue
    if payload is None:
        raise JWTError("Invalid refresh token")
    if payload.get("type") != "refresh":
        raise JWTError("Not a refresh token")
    return payload


def generate_public_token(length: int = 12) -> str:
    """URL-safe random token for public report/partner QR links."""
    return secrets.token_urlsafe(length)[:length]

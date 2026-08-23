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

# ── Config (from env, with safe defaults for local dev) ───────────────────
_ACCESS_SECRET  = os.getenv("JWT_ACCESS_SECRET",  "dev-access-secret-change-in-prod")
_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET", "dev-refresh-secret-change-in-prod")
_ALGORITHM      = "HS256"
ACCESS_TTL_MIN  = int(os.getenv("JWT_ACCESS_TTL_MINUTES",  "480"))   # 8 h
REFRESH_TTL_DAYS = int(os.getenv("JWT_REFRESH_TTL_DAYS",   "30"))

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
    """Raises JWTError on invalid/expired token."""
    payload = jwt.decode(token, _ACCESS_SECRET, algorithms=[_ALGORITHM])
    if payload.get("type") != "access":
        raise JWTError("Not an access token")
    return payload


def decode_refresh_token(token: str) -> Dict[str, Any]:
    payload = jwt.decode(token, _REFRESH_SECRET, algorithms=[_ALGORITHM])
    if payload.get("type") != "refresh":
        raise JWTError("Not a refresh token")
    return payload


def generate_public_token(length: int = 12) -> str:
    """URL-safe random token for public report/partner QR links."""
    return secrets.token_urlsafe(length)[:length]

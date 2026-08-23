"""
FastAPI dependencies: get_current_partner, get_current_admin, require_feature.
"""
from __future__ import annotations
from typing import Any, Callable, Dict
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.auth.security import decode_access_token
from api.db.admins import get_admin_by_id
from api.db.partners import get_partner_by_id
from api.db.features import get_effective_features

_bearer = HTTPBearer(auto_error=False)

_HTTP_401 = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="Not authenticated",
                          headers={"WWW-Authenticate": "Bearer"})
_HTTP_403_INACTIVE = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                   detail="Account is deactivated")
_HTTP_403_SCOPE = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Insufficient permissions")


def _extract_token(creds: HTTPAuthorizationCredentials | None) -> Dict[str, Any]:
    if not creds:
        raise _HTTP_401
    try:
        return decode_access_token(creds.credentials)
    except Exception:
        raise _HTTP_401


async def get_current_partner(
    creds: HTTPAuthorizationCredentials = Depends(_bearer),
) -> Dict[str, Any]:
    payload = _extract_token(creds)
    if payload.get("scope") != "partner":
        raise _HTTP_403_SCOPE
    partner = get_partner_by_id(payload["sub"])
    if not partner:
        raise _HTTP_401
    if not partner["is_active"]:
        raise _HTTP_403_INACTIVE
    return partner


async def get_current_admin(
    creds: HTTPAuthorizationCredentials = Depends(_bearer),
) -> Dict[str, Any]:
    payload = _extract_token(creds)
    if payload.get("scope") != "admin":
        raise _HTTP_403_SCOPE
    admin = get_admin_by_id(payload["sub"])
    if not admin:
        raise _HTTP_401
    if not admin["is_active"]:
        raise _HTTP_403_INACTIVE
    return admin


def require_feature(feature_key: str, error_detail: str | None = None):
    """Dependency factory — rejects partners who don't have the named feature."""

    async def _check(partner: Dict[str, Any] = Depends(get_current_partner)) -> Dict[str, Any]:
        features = get_effective_features(partner["id"])
        val = features.get(feature_key, "false")
        if val in ("false", "0", "", "False"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_detail or f"Feature '{feature_key}' is not enabled on your plan.",
            )
        return partner

    return _check

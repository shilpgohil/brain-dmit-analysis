"""
Cloudflare R2 (S3-compatible) object storage utility.

All functions are no-ops / raise graceful errors when R2 is not configured.
Set these environment variables to enable R2:
  CF_ACCOUNT_ID  — Cloudflare Account ID
  R2_ACCESS_KEY  — R2 API token access key
  R2_SECRET_KEY  — R2 API token secret key
  R2_BUCKET      — bucket name  (default: dmit-files)
  R2_PUBLIC_URL  — public base URL, e.g. https://pub-xxxx.r2.dev
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional

_CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "")
_R2_ACCESS_KEY = os.environ.get("R2_ACCESS_KEY", "")
_R2_SECRET_KEY = os.environ.get("R2_SECRET_KEY", "")

BUCKET = os.environ.get("R2_BUCKET", "dmit-files")
PUBLIC_BASE_URL = os.environ.get("R2_PUBLIC_URL", "").rstrip("/")

# R2 is enabled only when all three credentials are present.
ENABLED: bool = bool(_CF_ACCOUNT_ID and _R2_ACCESS_KEY and _R2_SECRET_KEY)


def _client():
    if not ENABLED:
        raise RuntimeError(
            "R2 storage is not configured. "
            "Set CF_ACCOUNT_ID, R2_ACCESS_KEY, and R2_SECRET_KEY."
        )
    import boto3

    return boto3.client(
        "s3",
        endpoint_url=f"https://{_CF_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=_R2_ACCESS_KEY,
        aws_secret_access_key=_R2_SECRET_KEY,
        region_name="auto",
    )


def upload_file(local_path: Path, key: str) -> str:
    """
    Upload *local_path* to R2 under *key*.
    Returns the public URL (empty string if R2 is not configured).
    """
    if not ENABLED:
        return ""
    _client().upload_file(str(local_path), BUCKET, key)
    return f"{PUBLIC_BASE_URL}/{key}" if PUBLIC_BASE_URL else ""


def download_to_temp(key: str, suffix: str = "") -> Optional[Path]:
    """
    Download R2 object *key* to a local temp file.
    Returns the temp Path, or None if R2 is not configured.
    """
    if not ENABLED:
        return None
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        _client().download_fileobj(BUCKET, key, tmp)
    finally:
        tmp.close()
    return Path(tmp.name)


def delete_prefix(prefix: str) -> None:
    """Delete all objects whose key starts with *prefix*."""
    if not ENABLED:
        return
    s3 = _client()
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    for obj in resp.get("Contents", []):
        s3.delete_object(Bucket=BUCKET, Key=obj["Key"])


def get_presigned_url(key: str, expires: int = 3600) -> Optional[str]:
    """
    Generate a time-limited presigned download URL.
    Returns None if R2 is not configured.
    """
    if not ENABLED:
        return None
    return _client().generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=expires,
    )


def public_url(key: str) -> Optional[str]:
    """Return the public URL for *key*, or None if R2 is not configured / no public base URL."""
    if not ENABLED or not PUBLIC_BASE_URL:
        return None
    return f"{PUBLIC_BASE_URL}/{key}"

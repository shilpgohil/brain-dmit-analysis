"""
S3-compatible object storage utility.

Supports Cloudflare R2, Backblaze B2, and any S3-compatible provider.

For Cloudflare R2 (requires card):
  CF_ACCOUNT_ID  = your Cloudflare account ID
  R2_ACCESS_KEY  = R2 API token access key
  R2_SECRET_KEY  = R2 API token secret key
  R2_BUCKET      = dmit-files
  R2_PUBLIC_URL  = https://pub-xxxx.r2.dev

For Backblaze B2 (no card needed, free 10 GB):
  STORAGE_ENDPOINT = https://s3.us-west-004.backblazeb2.com  (your B2 region endpoint)
  R2_ACCESS_KEY    = B2 keyID
  R2_SECRET_KEY    = B2 applicationKey
  R2_BUCKET        = dmit-files
  R2_PUBLIC_URL    = https://f003.backblazeb2.com/file/dmit-files
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional

_CF_ACCOUNT_ID    = os.environ.get("CF_ACCOUNT_ID", "")
_R2_ACCESS_KEY    = os.environ.get("R2_ACCESS_KEY", "")
_R2_SECRET_KEY    = os.environ.get("R2_SECRET_KEY", "")
_STORAGE_ENDPOINT = os.environ.get("STORAGE_ENDPOINT", "")

BUCKET          = os.environ.get("R2_BUCKET", "dmit-files")
PUBLIC_BASE_URL = os.environ.get("R2_PUBLIC_URL", "").rstrip("/")

# Resolve the S3 endpoint:
#  1. Explicit STORAGE_ENDPOINT (Backblaze B2, MinIO, Wasabi, etc.)
#  2. Auto-build from CF_ACCOUNT_ID (Cloudflare R2)
if _STORAGE_ENDPOINT:
    _ENDPOINT_URL = _STORAGE_ENDPOINT
elif _CF_ACCOUNT_ID:
    _ENDPOINT_URL = f"https://{_CF_ACCOUNT_ID}.r2.cloudflarestorage.com"
else:
    _ENDPOINT_URL = ""

ENABLED: bool = bool(_ENDPOINT_URL and _R2_ACCESS_KEY and _R2_SECRET_KEY)


def _client():
    if not ENABLED:
        raise RuntimeError(
            "Object storage is not configured. "
            "Set STORAGE_ENDPOINT (or CF_ACCOUNT_ID), R2_ACCESS_KEY, and R2_SECRET_KEY."
        )
    import boto3

    # Derive region from endpoint URL (e.g. "s3.us-west-004.backblazeb2.com" → "us-west-004")
    # Cloudflare R2 uses "auto"; B2 needs the region extracted from the endpoint hostname.
    region = "auto"
    if "backblazeb2.com" in _ENDPOINT_URL:
        # hostname format: s3.<region>.backblazeb2.com
        try:
            region = _ENDPOINT_URL.split("//")[1].split(".")[1]  # e.g. "us-west-004"
        except Exception:
            region = "us-west-004"

    return boto3.client(
        "s3",
        endpoint_url=_ENDPOINT_URL,
        aws_access_key_id=_R2_ACCESS_KEY,
        aws_secret_access_key=_R2_SECRET_KEY,
        region_name=region,
    )


def upload_file(local_path: Path, key: str) -> str:
    """Upload *local_path* to bucket under *key*. Returns the public URL, or '' on failure."""
    if not ENABLED:
        return ""
    try:
        _client().upload_file(str(local_path), BUCKET, key)
        return f"{PUBLIC_BASE_URL}/{key}" if PUBLIC_BASE_URL else ""
    except Exception as _e:
        import logging as _log
        _log.getLogger(__name__).warning("Storage upload failed for key %s: %s", key, _e)
        return ""


def download_to_temp(key: str, suffix: str = "") -> Optional[Path]:
    """Download object *key* to a local temp file. Returns the Path, or None."""
    if not ENABLED:
        return None
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        try:
            _client().download_fileobj(BUCKET, key, tmp)
        finally:
            tmp.close()
        return Path(tmp.name)
    except Exception as _e:
        import logging as _log
        _log.getLogger(__name__).warning("Storage download failed for key %s: %s", key, _e)
        return None


def delete_prefix(prefix: str) -> None:
    """Delete all objects whose key starts with *prefix*."""
    if not ENABLED:
        return
    s3 = _client()
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    for obj in resp.get("Contents", []):
        s3.delete_object(Bucket=BUCKET, Key=obj["Key"])


def get_presigned_url(key: str, expires: int = 3600) -> Optional[str]:
    """Generate a time-limited presigned download URL. Returns None if not configured."""
    if not ENABLED:
        return None
    return _client().generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=expires,
    )


def public_url(key: str) -> Optional[str]:
    """Return the public URL for *key*, or None if not configured."""
    if not ENABLED or not PUBLIC_BASE_URL:
        return None
    return f"{PUBLIC_BASE_URL}/{key}"

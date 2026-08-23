"""
Shared helpers for API routes.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Tuple

FINGER_POSITIONS = ("R1", "R2", "R3", "R4", "R5", "L1", "L2", "L3", "L4", "L5")
# Extensions we can decode end-to-end (OpenCV + browser upload). WSQ is not
# supported — consumer USB scanners export BMP/PNG/JPEG/TIFF.
ALLOWED_IMAGE_EXTENSIONS = (".bmp", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")
ALLOWED_IMAGE_EXTENSIONS_SET = frozenset(ALLOWED_IMAGE_EXTENSIONS)
PALM_POSITIONS = ("LPALM", "RPALM")
_POSITION_RE = re.compile(r"^(R[1-5]|L[1-5])", re.IGNORECASE)


def parse_finger_position(filename: str) -> Optional[str]:
    """Extract L1–R5 slot id from saved filename (e.g. R1.bmp, L3Center.jpg)."""
    stem = Path(filename).stem
    m = _POSITION_RE.match(stem)
    if m:
        return m.group(1).upper()
    name = stem.lower()
    for pos in FINGER_POSITIONS:
        if pos.lower() in name:
            return pos
    return None


def is_palm_position(pos: Optional[str]) -> bool:
    return bool(pos) and pos.upper() in PALM_POSITIONS


def parse_palm_position(filename: str) -> Optional[str]:
    """Extract LPALM/RPALM slot id from a filename (e.g. Lpalm.png)."""
    stem = Path(filename).stem.upper()
    if "LPALM" in stem:
        return "LPALM"
    if "RPALM" in stem:
        return "RPALM"
    return None


def palm_hand_label(slot: str) -> str:
    return "Left" if slot.upper() == "LPALM" else "Right"


def image_extension(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return ext if ext in ALLOWED_IMAGE_EXTENSIONS_SET else ""


def is_allowed_image_filename(filename: str) -> bool:
    return image_extension(filename) != ""


def validate_image_upload(filename: str, content: bytes) -> Tuple[bool, str]:
    """
    Reject unsupported or unreadable uploads before they enter the pipeline.
    Returns (ok, error_message).
    """
    if not filename or not filename.strip():
        return False, "Upload filename is missing."

    ext = image_extension(filename)
    if not ext:
        allowed = ", ".join(ALLOWED_IMAGE_EXTENSIONS)
        return False, f"Unsupported file type for '{filename}'. Use: {allowed}."

    if not content:
        return False, f"File '{filename}' is empty."

    # Palm photos can be large; fingerprint scanner BMPs are typically < 2 MB.
    if len(content) > 25 * 1024 * 1024:
        return False, f"File '{filename}' exceeds the 25 MB upload limit."

    try:
        import cv2
        import numpy as np

        arr = np.frombuffer(content, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
        if img is None:
            return False, (
                f"Could not read image '{filename}'. "
                "The file may be corrupt or use an unsupported encoding."
            )
        if img.ndim < 2 or img.shape[0] < 32 or img.shape[1] < 32:
            return False, f"Image '{filename}' is too small to analyze (minimum 32×32 px)."
    except Exception as exc:
        return False, f"Failed to validate '{filename}': {exc}"

    return True, ""


def slot_filename(slot_id: str, original_name: str) -> str:
    """Build canonical upload name: R1.bmp, L2.jpg, etc."""
    ext = image_extension(original_name) or ".bmp"
    return f"{slot_id.upper()}{ext}"


def thumbnail_url_for_path(image_path: Optional[str]) -> Optional[str]:
    if not image_path:
        return None
    p = Path(image_path)
    if not p.exists():
        return None
    # uploads/{session_id}/R1.bmp -> /uploads/{session_id}/R1.bmp
    parts = p.parts
    if "uploads" in parts:
        idx = parts.index("uploads")
        rel = "/".join(parts[idx:])
        return f"/{rel.replace(chr(92), '/')}"
    return None

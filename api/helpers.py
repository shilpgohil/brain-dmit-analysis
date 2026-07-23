"""
Shared helpers for API routes.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

FINGER_POSITIONS = ("R1", "R2", "R3", "R4", "R5", "L1", "L2", "L3", "L4", "L5")
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


def slot_filename(slot_id: str, original_name: str) -> str:
    """Build canonical upload name: R1.bmp, L2.jpg, etc."""
    ext = Path(original_name).suffix.lower() or ".bmp"
    if ext not in (".bmp", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"):
        ext = ".bmp"
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

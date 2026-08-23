"""
Session management routes.
"""
from __future__ import annotations

import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from api.auth.dependencies import get_current_partner, get_current_admin
from api.helpers import (
    is_palm_position,
    parse_finger_position,
    parse_palm_position,
    slot_filename,
    validate_image_upload,
)
from api.schemas import (
    AnalysisSession,
    AnalysisStatus,
    CreateSessionRequest,
    SessionListItem,
)
from api.store import persist_session, remove_session, session_store
import api.storage as storage

router = APIRouter(prefix="/sessions", tags=["sessions"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("", response_model=AnalysisSession)
async def create_session(
    body: CreateSessionRequest,
    partner=Depends(get_current_partner),
):
    session_id = str(uuid.uuid4())
    now = datetime.now()
    session = {
        "id": session_id,
        "partner_id": partner["id"],
        "subject_name": body.subject_name,
        "subject_age": body.subject_age,
        "subject_gender": body.subject_gender,
        "subject_dob": body.subject_dob,
        "school": body.school,
        "counsellor": body.counsellor,
        "parent_name": body.parent_name,
        "created_at": now,
        "updated_at": now,
        "status": AnalysisStatus.PENDING,
        "finger_count": 0,
        "completed_fingers": 0,
        "image_paths": [],
        "finger_slots": {},
        "palm_slots": {},
        "pipeline_stages": [],
        "notes": body.notes,
    }
    session_store[session_id] = session
    (UPLOAD_DIR / session_id).mkdir(parents=True, exist_ok=True)
    persist_session(session_id)
    return AnalysisSession(
        **{
            k: v
            for k, v in session.items()
            if k not in ("image_paths", "notes", "finger_slots", "palm_slots")
        }
    )


@router.post("/{session_id}/images")
async def upload_images(
    session_id: str,
    files: List[UploadFile] = File(...),
    finger_positions: Optional[str] = Form(None),
    partner=Depends(get_current_partner),
):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_store[session_id]
    if session.get("partner_id") and session.get("partner_id") != partner["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    positions: List[str] = []
    if finger_positions:
        positions = [p.strip().upper() for p in finger_positions.split(",") if p.strip()]

    saved = []
    slot_map = session.get("finger_slots", {})
    palm_map = session.get("palm_slots", {})

    existing_paths = list(session.get("image_paths", []))
    for i, f in enumerate(files):
        fname = f.filename or f"finger_{i}.bmp"
        content = await f.read()
        ok, err = validate_image_upload(fname, content)
        if not ok:
            raise HTTPException(status_code=400, detail=err)

        explicit = positions[i] if i < len(positions) else None
        pos = explicit or parse_finger_position(fname) or parse_palm_position(fname)

        if is_palm_position(pos):
            # Palm prints are stored for the record but NOT added to image_paths:
            # the fingerprint pipeline must never try to extract ridges from a palm.
            dest = session_dir / slot_filename(pos, fname)
            with dest.open("wb") as buf:
                buf.write(content)
            palm_map[pos.upper()] = str(dest)
            # Mirror to R2 if enabled
            if storage.ENABLED and pos:
                r2_key = f"uploads/{session_id}/{dest.name}"
                r2_url = storage.upload_file(dest, r2_key)
                r2_urls = session.get("r2_slot_urls", {})
                r2_urls[pos.upper()] = r2_url
                session["r2_slot_urls"] = r2_urls
            saved.append(str(dest))
            continue

        dest_name = slot_filename(pos, fname) if pos else fname
        dest = session_dir / dest_name

        with dest.open("wb") as buf:
            buf.write(content)

        path_str = str(dest)
        saved.append(path_str)
        if pos:
            # Re-uploading a slot replaces the previous image: drop the old
            # path so the same finger is never analyzed twice (and the canonical
            # {SLOT}.{ext} path is never duplicated in image_paths).
            old_path = slot_map.get(pos)
            if old_path and old_path in existing_paths:
                existing_paths.remove(old_path)
            slot_map[pos] = path_str
            # Mirror to R2 if enabled
            if storage.ENABLED:
                r2_key = f"uploads/{session_id}/{dest.name}"
                r2_url = storage.upload_file(dest, r2_key)
                r2_urls = session.get("r2_slot_urls", {})
                r2_urls[pos.upper()] = r2_url
                session["r2_slot_urls"] = r2_urls
        if path_str not in existing_paths:
            existing_paths.append(path_str)

    session["image_paths"] = existing_paths
    session["finger_slots"] = slot_map
    session["palm_slots"] = palm_map
    session["finger_count"] = len(session["image_paths"])
    session["updated_at"] = datetime.now()
    persist_session(session_id)

    return {"uploaded": len(saved), "total": session["finger_count"], "paths": saved}


@router.get("", response_model=List[SessionListItem])
async def list_sessions(
    limit: int = 50,
    offset: int = 0,
    partner=Depends(get_current_partner),
):
    """Partners see their own sessions only."""
    items = []
    sorted_sessions = sorted(
        (s for s in session_store.values() if s.get("partner_id") == partner["id"]),
        key=lambda s: s.get("created_at", datetime.min),
        reverse=True,
    )
    for s in sorted_sessions[offset : offset + limit]:
        items.append(
            SessionListItem(
                id=s["id"],
                subject_name=s.get("subject_name"),
                created_at=s["created_at"],
                status=s["status"],
                finger_count=s.get("finger_count", 0),
                has_report=bool(s.get("report_path")),
            )
        )
    return items


@router.get("/{session_id}", response_model=AnalysisSession)
async def get_session(session_id: str, partner=Depends(get_current_partner)):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")
    s = session_store[session_id]
    if s.get("partner_id") != partner["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return AnalysisSession(
        **{k: v for k, v in s.items() if k not in ("image_paths", "notes", "result", "report_path", "finger_slots")}
    )


@router.delete("/{session_id}")
async def delete_session(session_id: str, partner=Depends(get_current_partner)):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")
    s = session_store[session_id]
    if s.get("partner_id") != partner["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    remove_session(session_id)
    # Remove local upload dir
    session_dir = UPLOAD_DIR / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)
    # Remove R2 objects (uploads + report)
    if storage.ENABLED:
        storage.delete_prefix(f"uploads/{session_id}/")
        storage.delete_prefix(f"reports/{session_id}.")
    return {"deleted": session_id}

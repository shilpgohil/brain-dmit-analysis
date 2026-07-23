"""
Session management routes.
"""
from __future__ import annotations

import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from api.helpers import (
    is_palm_position,
    parse_finger_position,
    parse_palm_position,
    slot_filename,
)
from api.schemas import (
    AnalysisSession,
    AnalysisStatus,
    CreateSessionRequest,
    SessionListItem,
)
from api.store import persist_session, remove_session, session_store

router = APIRouter(prefix="/sessions", tags=["sessions"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("", response_model=AnalysisSession)
async def create_session(body: CreateSessionRequest):
    session_id = str(uuid.uuid4())
    now = datetime.now()
    session = {
        "id": session_id,
        "subject_name": body.subject_name,
        "subject_age": body.subject_age,
        "subject_gender": body.subject_gender,
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
):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_store[session_id]
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
        explicit = positions[i] if i < len(positions) else None
        pos = explicit or parse_finger_position(f.filename or "") or parse_palm_position(f.filename or "")

        if is_palm_position(pos):
            # Palm prints are stored for the record but NOT added to image_paths:
            # the fingerprint pipeline must never try to extract ridges from a palm.
            dest = session_dir / slot_filename(pos, f.filename)
            with dest.open("wb") as buf:
                shutil.copyfileobj(f.file, buf)
            palm_map[pos.upper()] = str(dest)
            saved.append(str(dest))
            continue

        dest_name = slot_filename(pos, f.filename) if pos else (f.filename or f"finger_{i}.bmp")
        dest = session_dir / dest_name

        with dest.open("wb") as buf:
            shutil.copyfileobj(f.file, buf)

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
async def list_sessions(limit: int = 50, offset: int = 0):
    items = []
    sorted_sessions = sorted(
        session_store.values(),
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
async def get_session(session_id: str):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")
    s = session_store[session_id]
    return AnalysisSession(
        **{k: v for k, v in s.items() if k not in ("image_paths", "notes", "result", "report_path", "finger_slots")}
    )


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found")
    remove_session(session_id)
    session_dir = UPLOAD_DIR / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)
    return {"deleted": session_id}

"""
DMIT AI Consultant — FastAPI router.
POST /api/sessions/{session_id}/chat  → NDJSON stream
GET  /api/sessions/{session_id}/chat/history → last 50 messages
DELETE /api/sessions/{session_id}/chat → clear thread
"""
from __future__ import annotations

import json
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from api.auth.dependencies import get_current_partner, require_feature
from api.ai_consultant.db import (
    get_or_create_thread, get_thread, get_messages, save_message, get_thread_title, set_thread_title
)
from api.ai_consultant.orchestrator.orchestrator import get_orchestrator
from api.store import session_store

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ai_consultant"])


class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None


# ── POST chat ──────────────────────────────────────────────────────────────────

@router.post("/sessions/{session_id}/chat")
async def chat(
    session_id: str,
    body: ChatRequest,
    partner=Depends(require_feature("ai_consultant", "AI Consultant is not enabled on your plan.")),
):
    """Stream a DMIT AI consultant response as NDJSON."""
    # ── Verify session ownership ──────────────────────────────────────────────
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.get("partner_id") and session.get("partner_id") != partner["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    if session.get("status") != "completed":
        raise HTTPException(
            status_code=400,
            detail="Analysis must be completed before using the AI consultant."
        )

    # ── Load result data ──────────────────────────────────────────────────────
    result = session.get("result") or {}
    if not result:
        raise HTTPException(status_code=400, detail="No analysis results found for this session.")

    query   = body.message.strip()
    if not query:
        raise HTTPException(status_code=422, detail="Message cannot be empty.")

    partner_id = partner["id"]

    # ── Get/create thread ─────────────────────────────────────────────────────
    thread_id = body.thread_id or get_or_create_thread(session_id, partner_id)

    # Validate thread ownership if supplied
    if body.thread_id:
        thread = get_thread(body.thread_id)
        if not thread or thread["partner_id"] != partner_id:
            raise HTTPException(status_code=403, detail="Thread not found or access denied.")

    # ── Save user message ─────────────────────────────────────────────────────
    save_message(thread_id, "user", query)

    # ── Build merged session data ─────────────────────────────────────────────
    # result may be a Pydantic AnalysisResult model — convert to plain dict
    if hasattr(result, "model_dump"):
        result_dict = result.model_dump()
    elif hasattr(result, "dict"):
        result_dict = result.dict()
    elif isinstance(result, dict):
        result_dict = result
    else:
        result_dict = {}

    session_data = {
        "session_id":     session_id,
        "subject_name":   session.get("subject_name"),
        "subject_age":    session.get("subject_age"),
        "subject_gender": session.get("subject_gender"),
        "subject_dob":    session.get("subject_dob"),
        "school":         session.get("school"),
        "counsellor":     session.get("counsellor"),
        "created_at":     session.get("created_at"),
        **result_dict,
    }

    # ── Stream ─────────────────────────────────────────────────────────────────
    orchestrator = get_orchestrator()

    async def _generate():
        full_text: list[str] = []
        chart_specs:  list[dict] = []
        widget_specs: list[dict] = []

        try:
            gen = await orchestrator.process_request(
                session_id=session_id,
                partner_id=partner_id,
                query=query,
                session_data=session_data,
                thread_id=thread_id,
            )
            async for chunk_json in gen:
                yield chunk_json + "\n"
                # Collect for persistence
                try:
                    chunk = json.loads(chunk_json)
                    ct = chunk.get("chunk_type")
                    if ct == "text":
                        full_text.append(chunk.get("response", ""))
                    elif ct == "chart" and chunk.get("chart"):
                        chart_specs.append(chunk["chart"])
                    elif ct == "widget" and chunk.get("widget"):
                        widget_specs.append(chunk["widget"])
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Chat stream error: {e}", exc_info=True)
            from api.ai_consultant.types import DMITStreamChunk
            yield DMITStreamChunk(
                chunk_type="status", status="error",
                status_message="Something went wrong. Please try again."
            ).model_dump_json() + "\n"
            # Always emit visible text so the user never sees an empty bubble
            yield DMITStreamChunk(
                chunk_type="text",
                response="Sorry — something went wrong while preparing the answer. Please try again.",
            ).model_dump_json() + "\n"
            yield DMITStreamChunk(
                chunk_type="done", stream_completed=True
            ).model_dump_json() + "\n"
            return

        # ── Persist assistant message ─────────────────────────────────────────
        assistant_text = "".join(full_text).strip()
        if assistant_text:
            save_message(
                thread_id, "assistant", assistant_text,
                chart_specs=chart_specs, widget_specs=widget_specs,
            )

        # ── Generate title if this is the first exchange ──────────────────────
        existing_title = get_thread_title(thread_id)
        if not existing_title and assistant_text:
            import asyncio
            candidate = session_data.get("subject_name") or "Candidate"
            async def _gen_title():
                from api.ai_consultant.llm_provider import generate_thread_title
                title = await generate_thread_title(query, candidate)
                set_thread_title(thread_id, title)
            asyncio.create_task(_gen_title())

    return StreamingResponse(
        _generate(),
        media_type="application/x-ndjson",
        headers={
            "X-Thread-Id": thread_id,
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ── GET history ────────────────────────────────────────────────────────────────

@router.get("/sessions/{session_id}/chat/history")
async def chat_history(
    session_id: str,
    partner=Depends(get_current_partner),
):
    """Return the chat thread and message history for a session."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.get("partner_id") and session.get("partner_id") != partner["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    thread_id = get_or_create_thread(session_id, partner["id"])
    messages  = get_messages(thread_id, limit=60)

    return {
        "thread_id": thread_id,
        "session_id": session_id,
        "title": get_thread_title(thread_id),
        "messages": messages,
        "total": len(messages),
    }


# ── DELETE (clear thread) ──────────────────────────────────────────────────────

@router.delete("/sessions/{session_id}/chat")
async def clear_chat(
    session_id: str,
    partner=Depends(get_current_partner),
):
    """Delete the chat thread and all messages for a session."""
    from api.db.connection import get_conn
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.get("partner_id") and session.get("partner_id") != partner["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    with get_conn() as conn:
        conn.execute(
            "DELETE FROM chat_threads WHERE session_id=? AND partner_id=?",
            (session_id, partner["id"]),
        )
        conn.commit()
    return {"ok": True, "message": "Chat history cleared."}

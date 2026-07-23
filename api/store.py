"""
Session store with SQLite persistence.
"""
from __future__ import annotations

from typing import Any, Dict

from api.persistence import delete_session as _delete_db, load_all_sessions, save_session

session_store: Dict[str, Any] = {}

# Statuses that mean "a pipeline run is in progress". Background runs are
# in-process and do not survive a server restart, so any session loaded from
# SQLite in one of these states is permanently stuck (and the 409 guard would
# block re-runs forever). They are flipped to failed on startup.
_IN_FLIGHT_STATUSES = {
    "preprocessing",
    "extracting",
    "mapping",
    "extending",
    "generating_report",
}


def init_store() -> None:
    global session_store
    session_store = load_all_sessions()

    # Recover sessions stranded mid-run by a previous server shutdown.
    for session_id, session in session_store.items():
        status = session.get("status")
        if isinstance(status, str) and status in _IN_FLIGHT_STATUSES:
            session["status"] = "failed"
            session["error"] = "Analysis was interrupted by a server restart. Run the analysis again."
            for stage in session.get("pipeline_stages", []):
                if stage.get("status") == "running":
                    stage["status"] = "failed"
                    stage["detail"] = "Interrupted by server restart"
            save_session(session_id, session)


def persist_session(session_id: str) -> None:
    session = session_store.get(session_id)
    if session is not None:
        save_session(session_id, session)


def remove_session(session_id: str) -> None:
    session_store.pop(session_id, None)
    _delete_db(session_id)

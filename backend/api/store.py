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
    # Mutate the existing dict in place rather than rebinding `session_store`
    # to a new object. Route modules (sessions.py, analysis.py) are imported
    # — and bind their own local name via `from api.store import session_store`
    # — before this runs, so reassigning the module attribute would orphan
    # their reference to the pre-init empty dict: every session created via
    # the API would silently vanish into a dict that persistence and the
    # health check could never see, and nothing would ever reach SQLite.
    session_store.clear()
    session_store.update(load_all_sessions())

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

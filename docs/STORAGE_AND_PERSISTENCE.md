# Storage & Persistence

> Source of truth: `api/store.py`, `api/persistence.py`, `api/routes/*.py`, `api/main.py`.

The platform uses a deliberately simple two-tier storage model: an **in-memory dict** as the live store, mirrored to a **single-table SQLite database** for durability, plus the **filesystem** for binary artifacts (uploaded images and generated PDFs).

## 1. Layers at a glance

| Layer | Location | Holds | Lifetime |
|---|---|---|---|
| In-memory store | `api/store.py` → `session_store: Dict[str, Any]` | Full session dicts (metadata, image paths, slots, pipeline stages, result, report path) | Process lifetime; rebuilt from SQLite at startup |
| SQLite | `data/sessions.db` (`api/persistence.py`, `DB_PATH = Path("data/sessions.db")`) | JSON-serialized snapshot of every session | Durable across restarts |
| Filesystem — uploads | `uploads/{session_id}/{SLOT}.{ext}` | Raw fingerprint images | Until `DELETE /api/sessions/{id}` |
| Filesystem — output | `output/dmit_report_{session_id}.pdf` | Generated premium PDF reports | Never auto-deleted |
| Filesystem — CLI output | `output/scientific_reports/dmit_scientific_{ts}.pdf` | PDFs from the standalone CLI pipeline (`integrated_dmit_pipeline.py`) | Never auto-deleted |

`data/`, `uploads/`, and `output/` are all relative to the **process working directory** — the API must be started from the project root (as `start_api.ps1` does), or sessions/uploads will land in the wrong place.

## 2. In-memory store (`api/store.py`)

```python
session_store: Dict[str, Any] = {}

def init_store():           # called once in api/main.py at import time
    session_store = load_all_sessions()   # hydrate from SQLite

def persist_session(id):    # write-through: routes call this after every mutation
    save_session(id, session_store[id])

def remove_session(id):     # pop from memory + DELETE row
    ...
```

- `init_store()` runs at module import in `api/main.py`, so a restarted server resumes with all previously persisted sessions.
- Every route that mutates a session calls `persist_session(session_id)` afterwards (create, upload, run start, pipeline completion/failure). The store is **write-through**, not write-behind.
- The background pipeline thread mutates the same dict objects, then persists once at the end of the run (and on failure). **Intermediate stage updates are visible to pollers immediately** (shared memory) but are only flushed to SQLite at terminal states — a crash mid-run loses in-flight stage state and the session reloads in its last persisted status (see Known limitations).

## 3. SQLite schema (`api/persistence.py`)

Single table, schema-on-write JSON blob:

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id          TEXT PRIMARY KEY,   -- session UUID
    data        TEXT NOT NULL,      -- JSON snapshot of the entire session dict
    updated_at  TEXT NOT NULL       -- ISO timestamp of last save
);
```

- `init_db()` is invoked lazily by every operation (`load_all_sessions`, `save_session`, `delete_session`), creating `data/` and the table on demand.
- Upserts use `INSERT … ON CONFLICT(id) DO UPDATE`.
- Connections: a new `sqlite3.connect(DB_PATH, check_same_thread=False)` per operation, `row_factory = sqlite3.Row`.

### JSON serialization rules

`save_session` uses `json.dumps(session, default=_json_default)`:

| Python type | Serialized as |
|---|---|
| `datetime` | `{"__type__": "datetime", "value": "<isoformat>"}` (round-trips via `_json_object_hook` on load) |
| `Enum` (e.g. `AnalysisStatus`) | its `.value` string |
| Pydantic models (`AnalysisResult`, …) | `model_dump(mode="json")` |
| Anything else non-JSON-able | raises `TypeError` |

On load (`load_all_sessions`), rows that fail `json.JSONDecodeError` are silently skipped. Note the asymmetry: a stored `AnalysisResult` comes back as a **plain dict**, not a model — `GET /api/analysis/{id}` handles this by re-validating (`AnalysisResult(**r)`) and caching the model back into the session. Statuses also come back as plain strings; the comparisons in routes work because `AnalysisStatus` is a `str` Enum.

## 4. Session document shape

What actually lives in `session_store[id]` / the `data` column (superset of the API's `AnalysisSession` model):

```jsonc
{
  "id": "105e4ce6-…",
  "subject_name": "Jane", "subject_age": 14, "subject_gender": "Female",
  "notes": "…",
  "created_at": "<datetime>", "updated_at": "<datetime>",
  "status": "completed",                  // AnalysisStatus value
  "finger_count": 10, "completed_fingers": 10,
  "image_paths": ["uploads/105e…/L1.bmp", "…"],     // ordered upload list (drives the pipeline)
  "finger_slots": {"L1": "uploads/…/L1.bmp", "…"},  // slot → path map (upload grid)
  "pipeline_stages": [ {"id": "extraction", "label": "…", "status": "completed", "duration_ms": 8123.4, "detail": null}, … ],
  "result": { /* serialized AnalysisResult */ },     // only after a completed run
  "report_path": "output/dmit_report_105e….pdf",     // only when PDF was generated
  "error": "…"                                       // only after a failed run
}
```

`image_paths` (not `finger_slots`) is what `POST /api/analysis/run` feeds to `IntegratedDMITPipeline.analyze_multiple_fingers`; `finger_slots` exists for the upload-grid UX and slot bookkeeping.

## 5. File storage conventions

### Uploads

- Path: `uploads/{session_id}/`, created at session creation and again defensively on upload.
- Canonical naming: when a finger slot is known, the file is renamed to `{SLOT}{ext}` (e.g. `R1.bmp`, `L3.jpg`) via `api.helpers.slot_filename`. Extension whitelist: `.bmp .jpg .jpeg .png .tif .tiff .webp` (others coerced to `.bmp`).
- Served publicly at `/uploads/{session_id}/{name}` through the `StaticFiles` mount; `api.helpers.thumbnail_url_for_path` converts a stored path to that URL (returns `None` if the file no longer exists).

### Reports

- API-generated reports: `output/dmit_report_{session_id}.pdf`, written by `PremiumReportGenerator.create_report`. Path stored in `session["report_path"]`; downloaded through `GET /api/analysis/{id}/report/download` (also reachable via the `/output` static mount).
- CLI pipeline reports: `output/scientific_reports/dmit_scientific_{YYYYMMDD_HHMMSS}.pdf` from `IntegratedDMITPipeline.generate_advanced_3d_pdf` (advanced 3D generator path).

### Deletion semantics

`DELETE /api/sessions/{id}` removes: memory entry, SQLite row, and the entire `uploads/{id}/` tree. It does **not** remove `output/dmit_report_{id}.pdf` — orphaned reports accumulate in `output/`.

## 6. Concurrency model

- FastAPI handlers are `async` but the store is plain dict access on the event loop thread — no locks.
- The pipeline runs in a worker thread (`asyncio.to_thread(_run_pipeline_sync, …)`) and mutates the shared session dict concurrently with read endpoints. CPython's GIL makes individual dict operations atomic; there is no transactional consistency beyond that.
- The `409` guard in `POST /api/analysis/run` prevents two concurrent runs for the same session (statuses other than `pending|failed|completed` are rejected).
- SQLite is opened with `check_same_thread=False` and short-lived connections; concurrent writers are serialized by SQLite's own locking.

## 7. Known limitations (acknowledged in `memory-bank/progress.md` and `docs/PRODUCT_ROADMAP.md`)

| Limitation | Impact | Planned remedy |
|---|---|---|
| Background runs are in-process FastAPI tasks | A server restart mid-run leaves the session stuck in its last persisted in-flight status (`preprocessing`) with no recovery/retry path | Durable queue (Celery/Redis) — roadmap Phase 2 |
| SQLite single-file store | Fine for single-instance dev; no multi-writer/multi-node story | PostgreSQL — roadmap Phase 2 |
| No auth | All sessions and reports are publicly reachable by anyone with network access | JWT/Clerk — roadmap Phase 2 |
| Duplicate slot uploads append to `image_paths` | Same image can be analyzed twice; `finger_count` over-counts | Not addressed in code |
| Reports never garbage-collected | `output/` grows unboundedly | Not addressed in code |

# Error Handling

> Source of truth: `api/routes/*.py`, `api/main.py`, `integrated_dmit_pipeline.py`, `dmit_intelligence_mapper.py`.

This document catalogs how failures are detected, propagated, surfaced, and (where applicable) swallowed across the stack.

## 1. HTTP error responses (API layer)

All explicit errors use FastAPI's `HTTPException` with a `detail` string:

| Status | Where | Condition | Detail |
|---|---|---|---|
| 404 | all session/analysis routes | `session_id not in session_store` | `"Session not found"` |
| 400 | `POST /api/analysis/run` | session has no `image_paths` | `"No images uploaded for this session"` |
| 409 | `POST /api/analysis/run` | session status is in-flight (not `pending`/`failed`/`completed`) | `"Session is already {status}"` |
| 404 | `GET /api/analysis/{id}/report/download` | no `report_path` or file missing on disk | `"Report not yet generated"` |
| 422 | any route | Pydantic validation failure (malformed body/params) | FastAPI default validation payload |

There is no global exception middleware; an unexpected exception inside a request handler returns FastAPI's default `500`.

## 2. Pipeline failure semantics (`api/routes/analysis.py::_run_pipeline_sync`)

The background runner is wrapped in one outer `try/except Exception`:

- On any uncaught error: `session["status"] = FAILED`, `session["error"] = str(e)`, every stage still `running` is flipped to `failed` with the exception string in `detail`, full traceback logged via `logger.exception`, and the session is persisted.
- Clients discover the failure by polling `GET /api/analysis/{id}`, which returns `status: "failed"` + `error_message` + the stage list. **The HTTP status of the poll remains 200** — failure is conveyed in the body, not the status code.

### Graceful degradation inside a run

| Failure | Handling | Surfaced as |
|---|---|---|
| Individual finger fails (load/extract/map error) | `analyze_multiple_fingers` catches per-image, logs, continues with the rest | `warnings: ["N of M fingerprints could not be analyzed"]`; `completed_fingers < finger_count` |
| **All** fingers fail | `raise ValueError("No fingers successfully analyzed")` | whole run `failed` |
| Preprocessing fails for an image | `analyze_single_finger` falls back to `cv2.imread(path, IMREAD_GRAYSCALE)` on the raw file | silent (warning log only) |
| Image unreadable even directly | `ValueError("Failed to load or process image: …")` | per-finger failure (above) |
| PDF generation throws | caught locally; analysis still **completes** | `warnings: ["Report generation failed: …"]`, `report` stage `failed`, `report_url: null` |
| Missing image file before run | `FileNotFoundError` raised per finger | per-finger failure |

Design intent: a partial analysis is preferred over a hard failure; only zero-success aborts the run.

## 3. Startup / import errors

- `api/main.py::_warm_imports()` probes the four heavy components at startup, never raising — failures are recorded as `components[name] = False` and reported by `GET /api/health` (`status: "degraded"`). The app still serves; only the routes that import the failed module at call time would error.
- `integrated_dmit_pipeline.py` (standalone CLI use) is stricter: failed core imports log and `sys.exit(1)`.

## 4. Defensive patterns in core code

### `dmit_intelligence_mapper.py`
- All feature reads use `features.get(key, 0)` (or `or 0` guards for possible `None`, e.g. `cross_spectral_fusion_score`, `spectral_coherence`) — missing features degrade scores toward 0 rather than raising.
- Unknown `finger_type_str` falls back to `FingerType.UNKNOWN`, which disables the primary-lobe boost logic and produces undampened generic lobe potentials.
- All outputs clamped to `[0, 1]`.

### `integrated_dmit_pipeline.py` aggregation
- `get_avg_score` falls back from primary fingers to **all** profiles when no finger of the primary type exists, and to `0.0` when no profiles at all.
- Holistic extension pass injects neutral features (`atd_average_angle = None`, averaged `tfrc_normalized` defaulting to 0.5) "so extensions don't crash".

### Persistence (`api/persistence.py`)
- Corrupt JSON rows are skipped silently at load (`json.JSONDecodeError → continue`).
- Non-serializable objects raise `TypeError` at save time (would surface as a pipeline/route error).

### Helpers
- `thumbnail_url_for_path` returns `None` for missing files instead of broken URLs.
- `PatternType` coercion in `_normalize_finger_results` maps any unexpected raw value to `PatternType.UNKNOWN`.

## 5. Report-layer behavior (real-data-only policy)

The PDF layers follow a "no fabricated values" rule (see `memory-bank/activeContext.md` fix log):
- Missing lobe/MI/EQ data renders as **N/A** or an explanatory message instead of a default (e.g. `0%`, `'visual'` learning style defaults were removed).
- `advanced_3d_pdf_generator`'s `RealDataProcessor.validate_real_data(pipeline_data)` returns `(is_valid, errors)` and generation is refused on invalid/missing real data rather than silently substituting values.
- ATD-angle metrics are palm-only; the architecture mandate (`system_architecture.md` §4.3) is to omit ATD-based visuals entirely rather than chart fake `0.5` constants.

## 6. Frontend-visible warnings vs errors

| Channel | Content |
|---|---|
| `AnalysisResult.error_message` | terminal failure reason (run failed) |
| `AnalysisResult.warnings[]` | non-fatal degradations (skipped fingers, PDF failure) |
| `PipelineStage.detail` | per-stage failure string |
| `GET /api/health.status` | `"degraded"` when any core import failed |

## 7. Known weak spots (code-verified)

- **Poll returns 200 on failure** — clients must inspect `status`, not HTTP codes.
- **Stuck in-flight sessions**: if the process dies mid-run, the persisted status remains e.g. `preprocessing` forever; the `409` guard then blocks re-runs until the status is manually changed (no timeout/requeue logic exists).
- **No upload validation**: corrupt/non-image files are accepted at upload and only fail later inside the pipeline (per-finger warning).
- **Silent data-shape mismatches**: extraction helpers use `.get(..., 0)` chains, so renamed keys upstream degrade silently to zeros (the historical `left_hemisphere` vs `left_hemisphere_bias` mismatch is a live example — see `API_REFERENCE.md`).
- **`honest_full_system_audit.md`** documents historical critical issues; several (mapper pseudoscience inputs, TFRC normalization `/200`, preprocessing never called) have since been fixed in code — read that audit as a point-in-time snapshot, not the current state.

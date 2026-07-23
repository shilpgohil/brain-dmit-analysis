# API Reference

> Source of truth: `api/main.py`, `api/routes/sessions.py`, `api/routes/analysis.py`, `api/schemas.py`.
> All schemas are Pydantic v2 models defined in `api/schemas.py`.

The DMIT Platform API is a FastAPI application (`api.main:app`, title "DMIT Analysis Platform API", version `3.2`) that wraps the Python analysis pipeline for the Next.js frontend.

- **Base URL (default dev):** `http://localhost:8001`
- **All application routes are prefixed with `/api`.**
- **Interactive docs:** `/api/docs` (Swagger UI), `/api/redoc` (ReDoc), `/api/openapi.json` (OpenAPI spec)
- **Auth:** none. There is no authentication or authorization anywhere in the API.
- **CORS:** configured via `CORS_ORIGINS` / `CORS_ORIGIN_REGEX` env vars; defaults allow any `http://localhost:<port>` / `http://127.0.0.1:<port>` origin (see `CONFIGURATION.md`).

## Static mounts

| Mount | Directory | Purpose |
|---|---|---|
| `/uploads` | `uploads/` | Serves uploaded fingerprint images (thumbnails). `thumbnail_url` values in responses point here. |
| `/output` | `output/` | Serves generated artifacts (PDF reports land in `output/`). |

Both directories are created at startup (`Path(...).mkdir(exist_ok=True)`).

---

## Endpoint index

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | System/component health and queue depth |
| POST | `/api/sessions` | Create an analysis session |
| GET | `/api/sessions` | List sessions (paginated) |
| GET | `/api/sessions/{session_id}` | Get one session's metadata |
| DELETE | `/api/sessions/{session_id}` | Delete session + its uploaded images |
| POST | `/api/sessions/{session_id}/images` | Upload fingerprint images to a session |
| POST | `/api/analysis/run` | Start the analysis pipeline (background task) |
| GET | `/api/analysis/{session_id}` | Poll analysis status / fetch full result |
| GET | `/api/analysis/{session_id}/report/download` | Download the generated PDF report |
| POST | `/api/analysis/{session_id}/upload` | Alternate upload endpoint (same behavior as `/api/sessions/{id}/images`) |

---

## GET `/api/health`

Defined in `api/main.py`. Returns `SystemStatus`.

Component availability is determined **once at process startup** by `_warm_imports()`, which attempts to import the four heavy pipeline modules and records success per component:

| Component key | Import probed |
|---|---|
| `feature_extractor` | `optimized_feature_extractor_clean.OptimizedFeatureExtractor` |
| `intelligence_mapper` | `dmit_intelligence_mapper.map_features_to_dmit_profile` |
| `extensions_engine` | `dmit_extensions.engine.DMITExtensionsEngine` |
| `pdf_generator` | `premium_pdf_report.PremiumReportGenerator` |

Response (`SystemStatus`):

```json
{
  "status": "operational",            // "operational" if ALL components imported, else "degraded"
  "pipeline_version": "3.2-Scientific-Full",
  "components": { "feature_extractor": true, "intelligence_mapper": true, "extensions_engine": true, "pdf_generator": true },
  "total_sessions": 17,
  "processing_queue": 0               // count of sessions in any in-flight status
}
```

`processing_queue` counts sessions whose status is one of `preprocessing`, `extracting`, `mapping`, `extending`, `generating_report`.

---

## Sessions (`api/routes/sessions.py`, router prefix `/sessions`, tag `sessions`)

### POST `/api/sessions`

Create a new analysis session.

**Request body** — `CreateSessionRequest` (all fields optional):

```json
{ "subject_name": "Jane", "subject_age": 14, "subject_gender": "Female", "notes": "career guidance" }
```

**Behavior / side effects:**
- Generates `session_id = uuid4()`.
- Creates an in-memory session dict with `status: "pending"`, empty `image_paths`, `finger_slots`, `pipeline_stages`.
- Creates the directory `uploads/{session_id}/`.
- Persists the session to SQLite (`data/sessions.db`) via `persist_session`.

**Response** — `AnalysisSession` (internal keys `image_paths`, `notes`, `finger_slots` are stripped):

```json
{
  "id": "105e4ce6-…", "subject_name": "Jane", "subject_age": 14,
  "created_at": "2026-06-11T15:00:00", "updated_at": "2026-06-11T15:00:00",
  "status": "pending", "finger_count": 0, "completed_fingers": 0, "pipeline_stages": []
}
```

Note: `subject_gender` is accepted and stored (used later in the PDF report metadata) but is not part of the `AnalysisSession` response model.

### POST `/api/sessions/{session_id}/images`

Upload one or more fingerprint images (multipart form).

**Request (multipart/form-data):**
- `files`: one or more image files (required).
- `finger_positions` (optional form field): comma-separated slot ids aligned with file order, e.g. `L1,L2,L3,L4,L5,R1,R2,R3,R4,R5`.

**Slot resolution logic:**
1. If `finger_positions[i]` is provided, it is used (uppercased).
2. Otherwise `parse_finger_position(filename)` (`api/helpers.py`) tries to extract `R1`–`L5` from the filename (prefix match like `R1.bmp`, `L3Center.jpg`, then substring match).
3. If a slot is resolved, the file is saved under the canonical name `{SLOT}{ext}` via `slot_filename` (e.g. `R1.bmp`). Allowed extensions: `.bmp .jpg .jpeg .png .tif .tiff .webp`; anything else is coerced to `.bmp`.
4. If no slot can be resolved, the original filename (or `finger_{i}.bmp`) is used and the file is **not** registered in `finger_slots`.

**Side effects:** files written to `uploads/{session_id}/`; session `image_paths`, `finger_slots`, `finger_count`, `updated_at` updated and persisted.

**Response:**

```json
{ "uploaded": 10, "total": 10, "paths": ["uploads/105e…/L1.bmp", "…"] }
```

**Errors:** `404` `{"detail": "Session not found"}`.

**Caveats (by design of the code):**
- There is no MIME/type or content validation of the uploaded bytes — anything sent is written to disk.
- Uploading the same slot twice overwrites the file on disk but **appends a duplicate path** to `image_paths` (`finger_count` then over-counts; the pipeline would analyze the same image twice).

### GET `/api/sessions`

List sessions, newest first (sorted by `created_at` descending).

**Query params:** `limit` (default 50), `offset` (default 0).

**Response** — `List[SessionListItem]`:

```json
[ { "id": "…", "subject_name": "Jane", "created_at": "…", "status": "completed", "finger_count": 10, "has_report": true } ]
```

`has_report` is `bool(session["report_path"])`.

### GET `/api/sessions/{session_id}`

Returns `AnalysisSession` for one session (strips `image_paths`, `notes`, `result`, `report_path`, `finger_slots`).
**Errors:** `404` if unknown id.

### DELETE `/api/sessions/{session_id}`

Removes the session from the in-memory store and SQLite, and deletes the whole `uploads/{session_id}/` directory (`shutil.rmtree`). Generated PDF reports in `output/` are **not** deleted.

**Response:** `{ "deleted": "<session_id>" }` — **Errors:** `404`.

---

## Analysis (`api/routes/analysis.py`, router prefix `/analysis`, tag `analysis`)

### POST `/api/analysis/run`

Starts the full pipeline as a FastAPI `BackgroundTasks` job (executed via `asyncio.to_thread`, i.e. in-process, non-durable).

**Request body** — `AnalyzeRequest`:

```json
{ "session_id": "105e4ce6-…", "use_preprocessing": true, "generate_pdf": true }
```

| Field | Default | Meaning |
|---|---|---|
| `session_id` | required | Target session |
| `use_preprocessing` | `true` | Run `FingerToFingerprintPipeline` (finger photo → fingerprint) before extraction |
| `generate_pdf` | `true` | Run `PremiumReportGenerator.create_report` after analysis |

**Validation / errors:**
- `404` — session not found.
- `400` — `"No images uploaded for this session"`.
- `409` — session is currently in an in-flight status. A run is allowed only from `pending`, `failed` or `completed` (re-run supported).

**Side effects on accept:** status set to `preprocessing`; any previous `result`, `error`, `report_path` are cleared; session persisted; background task scheduled.

**Response:** `{ "session_id": "…", "status": "started" }` (returns immediately; poll the GET endpoint).

**Pipeline stage tracking:** the background runner `_run_pipeline_sync` builds five stages and updates each with `status` (`pending → running → completed | failed`), `duration_ms`, and optional `detail`:

| Stage id | Label |
|---|---|
| `preprocessing` | Image Preprocessing |
| `extraction` | Feature Extraction (`detail: "85 biometric features per finger"`) |
| `mapping` | Intelligence Mapping |
| `extensions` | Extension Analysis (`detail: "40+ extension modules"`) |
| `report` | Report Generation (detail `"Skipped"` when `generate_pdf=false`) |

### GET `/api/analysis/{session_id}`

Poll for status or fetch the completed result. Always returns an `AnalysisResult`; the shape depends on session state:

1. **Completed** (`session["result"]` exists): full result, with `report_url` set to `/api/analysis/{session_id}/report/download` when a report exists.
2. **Failed**: `status: "failed"` with `error_message` and the stage list (failed stage carries the exception string in `detail`).
3. **In flight / pending**: minimal result with current `status` and live `pipeline_stages` for progress UIs.

**`AnalysisResult` fields** (see `api/schemas.py` for exact types):

| Field | Type | Notes |
|---|---|---|
| `session_id`, `status`, `subject_name`, `created_at` | — | always present |
| `error_message` | `str?` | only on failure |
| `fingers` | `List[FingerBiometrics]` | per-finger biometrics (see below) |
| `brain_lobes` | `BrainLobeCapacity?` | 5 lobes + 2 hemispheres, each 0–1 |
| `multiple_intelligences` | `MultipleIntelligences?` | 9 Gardner intelligences, 0–1 |
| `learning_styles` | `LearningStyles?` | visual / auditory / kinesthetic, 0–1 |
| `personality` | `PersonalityProfile?` | Big Five, 0–1 |
| `extensions` | `List[ExtensionResult]` | sorted by `primary_score` desc |
| `career_matches` | `List[CareerMatch]` | up to 12, sorted by `match_score` desc |
| `pipeline_stages` | `List[PipelineStage]` | live progress |
| `report_url` | `str?` | download path when PDF generated |
| `processing_time_ms` | `float?` | wall-clock of the whole run |
| `total_features_extracted` | `int` | sum of consolidated feature counts across fingers |
| `warnings` | `List[str]` | e.g. partial finger failures, PDF failure |

**`FingerBiometrics`** (built by `_normalize_finger_results` from raw pipeline output):

| Field | Source |
|---|---|
| `finger_id` | slot (`L1`–`R5`) or finger type |
| `finger_type` | thumb/index/middle/ring/little |
| `finger_position` | `L1`–`R5` slot, parsed from pipeline info or filename |
| `pattern_type` | `PatternType` enum: `whorl`, `loop`, `arch`, `accidental`, `unknown` (invalid values coerced to `unknown`) |
| `pattern_subtype` | optional string |
| `ridge_count` | `int(consolidated_features["tfrc"])` |
| `fractal_dimension` | `box_counting_dimension` |
| `quality_score` / `quality_tier` | from extractor summary |
| `minutiae_count`, `entropy` | from features |
| `image_path` / `thumbnail_url` | upload path; `/uploads/...` URL via `thumbnail_url_for_path` |
| `raw_features` | all scalar (int/float/str/bool) consolidated features |

**`ExtensionResult` mapping rules** (`_extract_extensions`):
- Only extensions returning dicts with at least one numeric value are included.
- `primary_score` = `scores["overall"]` → `scores["score"]` → first numeric value (in that priority).
- Display name humanized from class-style names (`LeftRightBrainExtension` → `Left Right Brain`).
- `category` assigned from a hardcoded ~40-entry `category_map` (Cognitive, Social, Career, Wellness, Intelligence, …), defaulting to `General`.

**`CareerMatch` mapping rules** (`_extract_careers`):
- Reads `extension_results["career_guidance"]` and maps 13 known keys (8 `*_career` fields + 5 `*_careers` cluster fields) to human titles via `CAREER_FIELD_LABELS`; only scores `> 0` are kept.
- Fallback: if no career fields found, derives matches from `entrepreneurial_aptitude` sub-scores.
- Result truncated to top 12 by `match_score`.

### GET `/api/analysis/{session_id}/report/download`

Returns the generated PDF as `FileResponse` with `media_type="application/pdf"` and filename `DMIT_Report_{subject_name|session_id}.pdf`.

**Errors:** `404` `"Session not found"`; `404` `"Report not yet generated"` (no `report_path` or file missing on disk).

### POST `/api/analysis/{session_id}/upload`

Functionally identical to `POST /api/sessions/{session_id}/images` (duplicate implementation kept on the analysis router). Same multipart contract, slot logic, side effects, and response shape.

---

## Schemas and enums (`api/schemas.py`)

### Enums

| Enum | Values |
|---|---|
| `AnalysisStatus` | `pending`, `preprocessing`, `extracting`, `mapping`, `extending`, `generating_report`, `completed`, `failed` |
| `PatternType` | `whorl`, `loop`, `arch`, `accidental`, `unknown` |
| `FingerPosition` | `R1`–`R5`, `L1`–`L5` (defined but not referenced by any route; slots are plain strings in practice) |

### Models

| Model | Purpose |
|---|---|
| `SingularPoint` | `{x, y, type: "core"|"delta"}` — defined; `FingerBiometrics.singular_points` is never populated by the current pipeline normalization (always `None`). |
| `FingerBiometrics` | Per-finger biometric summary (see above) |
| `BrainLobeCapacity` | `prefrontal_lobe`, `posterior_frontal`, `parietal_lobe`, `temporal_lobe`, `occipital_lobe`, `left_hemisphere`, `right_hemisphere` — all `Field(ge=0, le=1)` |
| `MultipleIntelligences` | 9 floats, all 0–1 |
| `LearningStyles` | `visual`, `auditory`, `kinesthetic` — 0–1 |
| `PersonalityProfile` | Big Five — 0–1 |
| `ExtensionResult` | `name`, `category`, `scores: Dict[str,float]`, `primary_score`, `description?`, `recommendations?` |
| `CareerMatch` | `title`, `category`, `match_score`, `key_strengths` (always `[]` in current code) |
| `PipelineStage` | `id`, `label`, `status`, `duration_ms?`, `detail?` |
| `AnalysisSession` | Session metadata (no images/results) |
| `AnalysisResult` | Full analysis payload |
| `CreateSessionRequest`, `AnalyzeRequest`, `SessionListItem`, `SystemStatus` | Request/listing/health models |

### Hemisphere key mismatch (known quirk)

`_extract_brain_lobes` reads `bm.get("left_hemisphere", 0)` / `bm.get("right_hemisphere", 0)`, but the pipeline aggregation (`integrated_dmit_pipeline._aggregate_results_scientifically`) emits `left_hemisphere_bias` / `right_hemisphere_bias`. As a result the API's `brain_lobes.left_hemisphere` / `right_hemisphere` are always `0` in aggregated results. *(Documented as-is; this is a code gap, not a doc inference.)*

---

## Typical client flow

```text
POST /api/sessions                          → session_id
POST /api/sessions/{id}/images              → upload 10 prints with finger_positions=L1..R5
POST /api/analysis/run                      → {"status": "started"}
GET  /api/analysis/{id}   (poll every ~3s)  → status transitions: preprocessing → extracting → … → completed
GET  /api/analysis/{id}/report/download     → PDF
```

A working end-to-end client is `scripts/test_api_premium_report.py` (uses `httpx`, polls every 3 s, max wait 600 s).

# Backend FastAPI Architecture & Computer Vision Pipeline Rules

## 1. System Topology & Service Boundaries
- **Runtime**: Python 3.12+ (isolated virtualenv `.venv`).
- **Framework**: FastAPI (async-first routers, Pydantic v2 schemas).
- **Default Port**: `http://localhost:8001` (Interactive Swagger docs at `/api/docs`).
- **Persistence**: SQLite database stored at `data/dmit.db`.
- **CV Engine**: Pure OpenCV / NumPy / SciPy without heavy ML inference in the live request path for instantaneous response times.

---

## 2. Five-Stage Image Preprocessing Pipeline
When a user uploads raw finger photos, `backend/preprocessing_images/pipeline.py` executes:

1. **Stage 1 (Segmentation)**: Skin tone HSV thresholding + morphological closure to isolate finger from background.
2. **Stage 2 (Validation)**: Blur verification using Laplacian variance ($Var(\Delta) > 100$) and illumination balance check.
3. **Stage 3 (ROI Detection)**: Bounding box crop isolating the distal phalanx (fingertip).
4. **Stage 4 (Nail Removal)**: High-curvature boundary detection to crop out fingernails and specular reflection zones.
5. **Stage 5 (Ridge Enhancement)**: CLAHE contrast normalization followed by oriented Gabor filter bank (8 angles: $0^\circ, 22.5^\circ, \dots, 157.5^\circ$).

---

## 3. 85-Feature Extraction & Quality Gating
`backend/optimized_feature_extractor_clean.py` categorizes features into 3 quality tiers:
- **Tier 1 (High Quality)**: Full 85-feature extraction including minutiae adjacency graph, fractal dimension, and FFT spectral bands.
- **Tier 2 (Medium Quality)**: 45 core features (statistics, primary minutiae, orientation field, ridge frequency).
- **Tier 3 (Low Quality / Fallback)**: Fundamental ridge flow statistics + manual review flag in output payload.

---

## 4. API Endpoints & State Machine Contracts
- `POST /api/sessions`: Create analysis session with client metadata.
- `POST /api/sessions/{id}/images`: Upload multi-part image payload mapped to finger slots (`L1`..`L5`, `R1`..`R5`, `LPALM`, `RPALM`).
- `POST /api/analysis/run`: Spawn background pipeline task; emit stage progress (`PREPROCESSING`, `EXTRACTING`, `MAPPING`, `EXTENSIONS`, `REPORT_READY`).
- `GET /api/analysis/{id}`: Fetch status and full DMIT JSON result vector.
- `GET /api/analysis/{id}/report/download`: Generate and stream 19-section premium PDF report.

---

## 5. Error Handling & Data Integrity
- Zero Unhandled 500s: All exceptions must be caught, logged via structured logging, and converted to descriptive HTTP responses.
- Real Data Only Policy: If a finger slot is omitted, downstream analyzers must handle `None` gracefully without throwing `KeyError` or imputing fake ridge counts.

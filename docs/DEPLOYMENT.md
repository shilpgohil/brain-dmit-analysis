# Deployment & Operations

> Local setup, running, testing, packaging, and the known failure points — grounded in the actual scripts and code in this repo. There is currently **no Dockerfile, no CI config, and no production deployment manifest**; this doc covers the real dev workflow plus pragmatic guidance for hardening.

## 1. Prerequisites

| Requirement | Notes |
|---|---|
| Windows + PowerShell (as used here) or any OS with Python | Launch scripts are `.ps1`; commands translate directly to bash |
| Python 3.12 | `.venv` in repo was built with CPython 3.12 (`__pycache__/*.cpython-312*`) |
| Node.js 18+ | Next.js 16 requires modern Node |
| ~2 GB disk | venv + node_modules + artifacts |

No GPU, no model downloads — the live pipeline is pure OpenCV/NumPy. (Ignore the old README's torch/transformers instructions; nothing in the live path imports them.)

## 2. Local setup

```powershell
# from the repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt        # tensorflow/keras are listed but unused; skip them if installs fail:
# pip install numpy opencv-python scipy matplotlib reportlab Pillow fastapi "uvicorn[standard]" python-multipart pydantic httpx

cd frontend
npm install
# REQUIRED for the stock launchers (API runs on 8001, frontend defaults to 8000):
"NEXT_PUBLIC_API_URL=http://localhost:8001/api" | Out-File -Encoding ascii .env.local
cd ..
```

## 3. Running

```powershell
.\start_api.ps1        # uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
                       # Swagger: http://localhost:8001/api/docs
.\start_frontend.ps1   # next dev → http://localhost:3000
```

**Run both from the project root.** All storage paths (`data/`, `uploads/`, `output/`) are CWD-relative; starting uvicorn from elsewhere silently relocates your database and uploads.

Sanity check: `GET http://localhost:8001/api/health` should return `"status": "operational"` with all four components `true`. `"degraded"` means a core import failed — run `python -c "import integrated_dmit_pipeline"` to see the real traceback.

## 4. Generating a report

### Via the UI
`http://localhost:3000/analysis/new` → fill subject → drop 10 prints onto the R1–R5 / L1–L5 grid → Run → watch the pipeline tracker → download PDF from the results page.

### Via the API (curl-style)

```bash
SID=$(curl -s -X POST localhost:8001/api/sessions -H 'content-type: application/json' \
      -d '{"subject_name":"Test"}' | jq -r .id)
curl -s -X POST "localhost:8001/api/sessions/$SID/images" \
      -F files=@finger_prints/L1Center.bmp -F files=@finger_prints/R1Center.bmp \
      -F finger_positions=L1,R1
curl -s -X POST localhost:8001/api/analysis/run -H 'content-type: application/json' \
      -d "{\"session_id\":\"$SID\",\"use_preprocessing\":true,\"generate_pdf\":true}"
# poll until completed, then:
curl -o report.pdf "localhost:8001/api/analysis/$SID/report/download"
```

### Via the CLI pipeline (no API; uses the other PDF engine)

```powershell
.\.venv\Scripts\python.exe test_complete_pipeline.py
# reads finger_prints/*.bmp → output/scientific_reports/dmit_scientific_*.pdf
```

## 5. Testing the system

| Test | Command | Needs |
|---|---|---|
| Full HTTP E2E (premium PDF) | `python scripts/test_api_premium_report.py` | API running on 8001; 10 BMPs in `finger_prints/` |
| CLI pipeline E2E | `python test_complete_pipeline.py` | `finger_prints/` |
| Preprocessing only | `python create_dummy_image.py; python test_preprocessing.py` | writes to `test_output/preprocessing_results/` |
| 3D generator unit-ish | `python test_advanced_3d_pdf_generator.py` | saved pipeline JSON at `test_output/new_pipeline_test/new_pipeline_results.json` |
| Frontend build check | `cd frontend; npm run build` | — |

There is **no pytest suite** despite pytest being in requirements — the `test_*.py` files are runnable scripts, not collected tests.

## 6. Packaging / production guidance

What exists today is a dev topology. To productionize with minimal change:

1. **API:** `uvicorn api.main:app --host 0.0.0.0 --port 8001 --workers 1` — ⚠️ must stay **single-process**: the in-memory `session_store` and in-process background tasks are not shareable across workers. Scale-out requires the roadmap's Phase 2 items (PostgreSQL + Celery/Redis queue) first.
2. **Frontend:** `npm run build && npm run start` (or deploy `frontend/` to Vercel/Node host) with `NEXT_PUBLIC_API_URL` pointed at the API origin.
3. **Reverse proxy:** terminate TLS, proxy `/api`, `/uploads`, `/output` to uvicorn and `/` to Next. Lock down `CORS_ORIGINS` to the real frontend origin and replace the permissive `CORS_ORIGIN_REGEX`.
4. **State:** persist `data/`, `uploads/`, `output/` on a durable volume; back up `data/sessions.db`.
5. **Add before exposing publicly:** authentication (none exists), upload size/type validation, and report retention/cleanup (PDFs are never garbage-collected).

A Dockerfile would be straightforward (python:3.12-slim + `libgl1` for OpenCV + requirements + `uvicorn api.main:app`), but none is provided in the repo.

## 7. Common failure points & fixes

| Symptom | Root cause | Fix |
|---|---|---|
| Frontend shows network errors, API logs nothing | Port mismatch: frontend default targets `:8000/api`, API runs on 8001 | Set `NEXT_PUBLIC_API_URL=http://localhost:8001/api` in `frontend/.env.local`, restart `npm run dev` |
| `/api/health` → `degraded` | One of the 4 warm imports failed (usually OpenCV/matplotlib install issue) | `python -c "import optimized_feature_extractor_clean, dmit_intelligence_mapper, dmit_extensions.engine, premium_pdf_report"` and fix the traceback; restart API (components are probed only at startup) |
| `409 Session is already preprocessing` on re-run | Server restarted mid-run; session stranded in in-flight status (no requeue logic) | Delete the session, or manually flip its status in `data/sessions.db` (`UPDATE sessions SET data=...`), then re-run |
| Analysis `failed` with `No fingers successfully analyzed` | All images unreadable/non-fingerprint (e.g. corrupt uploads — uploads are not validated) | Re-upload valid grayscale prints; try `use_preprocessing=false` for scanner BMPs |
| Result completed but `report_url` null + warning `Report generation failed` | Exception inside `PremiumReportGenerator` (analysis itself succeeded) | Check API log (`logger.exception`); commonly missing matplotlib or font issues; re-run with `generate_pdf=true` after fixing |
| Hemisphere values are 0 in API/result UI | Known key mismatch `left_hemisphere` vs `left_hemisphere_bias` | Code fix required in `api/routes/analysis.py::_extract_brain_lobes` (PDF is unaffected — it reads both spellings) |
| Sessions/uploads "disappear" | API started from a different working directory | Always launch from repo root (`start_api.ps1` does) |
| Same finger analyzed twice / finger_count too high | Re-uploading a slot appends a duplicate path to `image_paths` | Delete and recreate the session, or dedupe `image_paths` before running |
| Thumbnails broken in UI | File removed from `uploads/` or API origin mismatch | `thumbnail_url_for_path` returns null for missing files; verify `/uploads/...` resolves on the API origin |
| Windows console Unicode errors in CLI scripts | Emoji logging vs cp1252 console | Scripts already call `sys.stdout.reconfigure(encoding='utf-8')`; use Windows Terminal/UTF-8 codepage |

## 8. Operational notes

- **Logs:** plain `logging` to stdout (pipeline at INFO with emoji markers); no log files, no structured logging.
- **Monitoring:** `/api/health` exposes component booleans + `processing_queue` count — suitable for a simple uptime probe.
- **Data growth:** `output/*.pdf` and `uploads/*` grow unboundedly; `DELETE /api/sessions/{id}` cleans uploads but not the PDF.
- **Concurrency:** one analysis per session enforced (409); multiple sessions can run concurrently, each consuming a CPU thread for the duration (~seconds for scanner BMPs, longer with preprocessing on photos).

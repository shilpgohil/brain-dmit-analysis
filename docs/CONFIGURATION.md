# Configuration

> Every configurable value in the system, where it lives, and its default. The project has **no `.env` loader, no settings module, and no config files** for the backend — configuration is environment variables read directly plus hardcoded constants.

## 1. Backend environment variables (`api/main.py`)

| Variable | Default | Effect |
|---|---|---|
| `CORS_ORIGINS` | `http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001` | Comma-separated exact allowed origins |
| `CORS_ORIGIN_REGEX` | `http://(localhost\|127\.0\.0\.1):\d+` | Regex allowing **any** localhost port (covers Next.js picking 3001/3002…) |

These are the **only** environment variables the backend reads. Host/port are CLI args to uvicorn, not env.

## 2. Frontend environment variables (`frontend/src/lib/api.ts`)

| Variable | Default | Effect |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000/api` | API base URL (must include the `/api` suffix) |

⚠️ **Port mismatch gotcha:** `start_api.ps1` launches the backend on port **8001**, but the frontend default targets **8000**. For the stock launchers to work together, create `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8001/api
```

(`.env*` is gitignored; no `.env` file ships with the repo.)

The `/settings` page stores `dmit_api_url` and a PDF-quality preference in `localStorage`, but **nothing reads them** — `api.ts` only consults `NEXT_PUBLIC_API_URL` at build/dev time. Treat the settings page as UI-only today.

## 3. Ports & process flags

| Component | Where set | Value |
|---|---|---|
| API (recommended launcher) | `start_api.ps1` → `uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload` | **8001** |
| API (`python -m api.main`) | `api/main.py` `__main__` block | 8001, reload=True |
| Frontend dev | `start_frontend.ps1` → `npm run dev` | **3000** (Next auto-increments if busy) |
| E2E test client | `scripts/test_api_premium_report.py` `BASE` | `http://127.0.0.1:8001/api` |

## 4. Filesystem path constants (all relative to CWD — run from repo root)

| Constant | Where | Value |
|---|---|---|
| `DB_PATH` | `api/persistence.py` | `data/sessions.db` |
| `UPLOAD_DIR` | `api/routes/sessions.py` | `uploads/` |
| `OUTPUT_DIR` | `api/routes/analysis.py` | `output/` |
| Static mounts | `api/main.py` | `/uploads` → `uploads/`, `/output` → `output/` |
| CLI report default | `integrated_dmit_pipeline.py`, `premium_pdf_report/generator.py` | `output/scientific_reports/` |
| Premium PDF (API) | `api/routes/analysis.py` | `output/dmit_report_{session_id}.pdf` |
| Watermark asset | `premium_pdf_report/assets/cover_brain_watermark.png` | baked-in package asset |

## 5. Pipeline/runtime options (per-request, not env)

`POST /api/analysis/run` body (`AnalyzeRequest`):

| Field | Default | Meaning |
|---|---|---|
| `use_preprocessing` | `true` | Run `FingerToFingerprintPipeline` (segmentation→validation→ROI→nail removal→Gabor enhancement) before extraction; on failure falls back to raw grayscale load |
| `generate_pdf` | `true` | Produce the premium PDF after analysis |

Constructor-level options:

| Option | Where | Default |
|---|---|---|
| `IntegratedDMITPipeline(use_preprocessing=…)` | pipeline | `True` |
| `OptimizedFeatureExtractor.extract_optimized_features(quality_level=…)` | extractor | `'auto'` (also accepts `'basic'|'core'|'advanced'|'comprehensive'|'high'`) |
| `PatternClassifier(config=…)` | classifier | `{block_size: 8, gaussian_sigma: 2.0, poincare_threshold: 0.40, min_confidence: 0.5, max_cores: 2, max_deltas: 2}` |
| `FingerToFingerprintPipeline(config=…)` | preprocessing | see threshold table in `COMPONENTS.md` §6 |

## 6. Tunable thresholds (hardcoded, documented for maintainers)

| Area | Constant | Value | File |
|---|---|---|---|
| Quality tiers | basic/core/advanced/comprehensive cuts | 0.30 / 0.40 / 0.50 | `optimized_feature_extractor_clean.py` |
| TFRC normalization | divisor | 25.0 | `dmit_intelligence_mapper.py`, `dmit_extensions/engine.py` |
| Non-primary lobe damping | multiplier | 0.2 | `dmit_intelligence_mapper.py` |
| Pattern boosts | whorl/loop/arch modifiers | +0.10…+0.25 | `dmit_intelligence_mapper.py` |
| Upload extension whitelist | `.bmp .jpg .jpeg .png .tif .tiff .webp` | — | `api/helpers.py::slot_filename` |
| Poll cadence (frontend) | interval | 1800 ms | `frontend/src/app/analysis/[id]/page.tsx` |
| Score tier colors | ≥0.75 / 0.60 / 0.45 / 0.30 | — | `premium_pdf_report/theme.py::score_color` |
| Chart DPI | 150 | — | both PDF engines |
| Extension strengths cut | MI ≥ 0.55 strengths, < 0.55 development | — | `premium_pdf_report/sections/executive_summary.py`, `development.py` |

## 7. Dependencies

### Python (`requirements.txt`)

```text
numpy, opencv-python, scipy, matplotlib, reportlab, Pillow,
fastapi>=0.110.0, uvicorn[standard]>=0.27.0, python-multipart>=0.0.9, pydantic>=2.0.0,
pytest, pydot, graphviz,
tensorflow, keras        # ⚠ listed but NOT imported by any live code path (FingerNet legacy)
```

`advanced_3d_pdf_generator/requirements.txt` additionally lists `plotly`, `pandas`, `seaborn` — of which only matplotlib/reportlab/numpy are actually used by that package.

Suggested minimal install for the live system: `numpy opencv-python scipy matplotlib reportlab Pillow fastapi uvicorn[standard] python-multipart pydantic` (+ `httpx` for `scripts/test_api_premium_report.py`).

### Node (`frontend/package.json`)

Next 16.2.6 · React 19.2.4 · Tailwind v4 (`@tailwindcss/postcss`) · recharts ^3.8.1 · framer-motion ^12 · lenis · lucide-react · clsx · tailwind-merge. (radix-ui, three, gsap, zustand are installed but unused.)

## 8. What is *not* configurable (would require code changes)

- Auth (none exists), rate limits, upload size limits.
- SQLite path/engine (hardcoded `data/sessions.db`).
- Report branding (counsellor default name, "Ridge Analysis" org, watermark art) — constants in `premium_pdf_report/`.
- Extension registry — manual list in `dmit_extensions/engine.py`.
- `advanced_3d_pdf_generator` `theme`/`style` parameters — accepted but no-ops.

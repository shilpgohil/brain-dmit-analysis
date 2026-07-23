# DMIT Analysis Platform

**Dermatoglyphics Multiple Intelligence Test — biometric analysis pipeline, REST API, web app, and PDF report engine.**

Version 3.2 ("Scientific-Full") · Python 3.12 + FastAPI backend · Next.js 16 frontend · OpenCV/NumPy computer vision (no ML models in the live path)

---

## What it does

Upload up to 10 fingerprint images (one per finger, slots `L1`–`L5` / `R1`–`R5`). The platform:

1. **Preprocesses** raw finger photos into fingerprint-like images (segmentation → validation → fingertip ROI → nail removal → CLAHE + Gabor ridge enhancement) — optional, on by default.
2. **Extracts ~85 biometric features** per finger (statistics, minutiae, fractal, topological, graph, ridge, spectral, pattern analytics) with quality-tiered processing, plus CADA pattern classification (arch/loop/whorl/accidental, 23 subtypes) via Poincaré singular-point detection and core→delta TFRC ridge counting.
3. **Maps features to a DMIT profile** using research-paper-backed "Table 1.1" finger→brain-lobe correlations: thumb→prefrontal (personality), index→posterior frontal (logic), middle→parietal (kinesthetic), ring→temporal (linguistic/musical), little→occipital (visual). Produces 9 Gardner multiple intelligences, 5 brain lobes + hemisphere biases, VAK learning styles, and Big Five personality — aggregated across fingers by weighted slots, not naive averaging.
4. **Runs 41 extension analyzers** (emotional intelligence, career guidance, leadership, memory, neurodivergence, …) over the combined feature/profile vector.
5. **Serves results** as JSON through a FastAPI backend with live pipeline-stage progress, rendered by a cinematic dark-themed Next.js app (radar/bar/pie charts, per-finger drill-down, session archive, comparison).
6. **Generates a premium PDF report** — 19 sections, ivory/gold design, matplotlib charts, real-data-only policy (missing data renders as N/A or is omitted; never fabricated).

**Scientific honesty:** palm-only metrics (ATD angle) and pseudoscientific features (quantum consciousness, brain criticality) return `None` by design and are excluded from scoring. The interpretation layer follows DMIT theory; it is not presented as validated clinical science. See `system_architecture.md` and `docs/ERROR_HANDLING.md` §5.

## Quick start

```powershell
# 1. Python env (from repo root)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Frontend
cd frontend
npm install
"NEXT_PUBLIC_API_URL=http://localhost:8001/api" | Out-File -Encoding ascii .env.local   # API runs on 8001
cd ..

# 3. Run (two terminals, both from repo root)
.\start_api.ps1        # → http://localhost:8001/api/docs
.\start_frontend.ps1   # → http://localhost:3000
```

Then open `http://localhost:3000/analysis/new`, assign prints to the 10-slot hand grid, and run. Sample scanner prints live in `finger_prints/` (`L1Center.bmp` … `R5Center.bmp`).

End-to-end smoke test (API must be running): `python scripts/test_api_premium_report.py`.

## Repository layout

| Path | Purpose |
|---|---|
| `api/` | FastAPI backend: sessions, uploads, analysis runner, SQLite persistence |
| `frontend/` | Next.js 16 app (App Router, Tailwind v4, Recharts) |
| `integrated_dmit_pipeline.py` | Pipeline orchestrator + Table 1.1 aggregation |
| `optimized_feature_extractor_clean.py` | 85-feature CV extractor (quality tiers) |
| `pattern_classifier.py` | Singular points, pattern families/subtypes, TFRC |
| `dmit_intelligence_mapper.py` | Features → MI / lobes / VAK / Big Five |
| `preprocessing_images/` | 5-stage finger-photo → fingerprint pipeline |
| `dmit_extensions/` | Extension engine + 41 registered analyzers |
| `premium_pdf_report/` | API report engine (19-section premium PDF) |
| `advanced_3d_pdf_generator/` | CLI report engine (legacy/alternate PDF) |
| `data/` · `uploads/` · `output/` | Runtime state: SQLite DB, images, PDFs |
| `docs/` | **Full documentation suite** + product roadmap |

## API at a glance

```text
GET  /api/health                                 component status, queue depth
POST /api/sessions                               create session
POST /api/sessions/{id}/images                   upload prints (finger_positions=L1..R5)
POST /api/analysis/run                           start pipeline (background)
GET  /api/analysis/{id}                          poll status / fetch full result
GET  /api/analysis/{id}/report/download          premium PDF
GET  /api/sessions · DELETE /api/sessions/{id}   archive management
```

Interactive docs: `http://localhost:8001/api/docs`. Full contract: [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md).

## Documentation

The complete reverse-engineered documentation suite lives in [`docs/`](docs/README.md):

- [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) — layers, boundaries, dependency graph, scientific model
- [`DATA_FLOW.md`](docs/DATA_FLOW.md) — request lifecycle from upload to PDF
- [`COMPONENTS.md`](docs/COMPONENTS.md) — file-by-file reference (feature catalog, extension registry, frontend inventory)
- [`API_REFERENCE.md`](docs/API_REFERENCE.md) — endpoints, schemas, validation, errors
- [`DIAGRAMS.md`](docs/DIAGRAMS.md) — Mermaid architecture/sequence/state/storage diagrams
- [`STORAGE_AND_PERSISTENCE.md`](docs/STORAGE_AND_PERSISTENCE.md) · [`ERROR_HANDLING.md`](docs/ERROR_HANDLING.md) · [`CONFIGURATION.md`](docs/CONFIGURATION.md) · [`DEPLOYMENT.md`](docs/DEPLOYMENT.md) · [`CHANGELOG_NOTES.md`](docs/CHANGELOG_NOTES.md)
- [`PRODUCT_ROADMAP.md`](docs/PRODUCT_ROADMAP.md) — audiences and phased delivery plan

## Current limitations (honest)

- No authentication; CORS open to localhost; uploads unvalidated — **dev/demo posture** (hardening is roadmap Phase 2).
- Background analysis runs in-process (FastAPI background task) — not durable across restarts; single-process deployment only.
- SQLite single-file session store; generated PDFs are never garbage-collected.
- Known code gaps are catalogued in [`docs/COMPONENTS.md`](docs/COMPONENTS.md) §12 (e.g. hemisphere key mismatch in the API, unpopulated `singular_points`, 14 unregistered legacy extensions).

## License / status

Internal project; large portions are uncommitted work-in-progress (see `docs/CHANGELOG_NOTES.md`). Conventional commits (`feat:`, `fix:`, `docs:` …) are the house style.

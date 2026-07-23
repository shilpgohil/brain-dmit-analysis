# Changelog Notes (reverse-engineered)

> There is no formal CHANGELOG in this repository. These notes reconstruct the project's evolution from `memory-bank/`, `honest_full_system_audit.md`, version strings in code, git status, and dated artifacts. Items marked *(inference)* are deduced from evidence rather than an explicit record.

## Version strings currently in code

| Component | Version | Where |
|---|---|---|
| FastAPI app | `3.2` | `api/main.py` (`FastAPI(version="3.2")`) |
| Pipeline | `3.2-Scientific-Full` | `integrated_dmit_pipeline.py::pipeline_version`, `/api/health` |
| Intelligence mapper | `2.0 (Scientific Refinement)` | `dmit_intelligence_mapper.py` docstring (`mapping_standard: "2.0_SCIENTIFIC_RESEARCH_PAPER"`) |
| Advanced 3D generator | `3.0 - Real Data Only` | `advanced_3d_pdf_generator` docstrings |
| Legacy README | `3.0 - Advanced 3D Integration` | root `README.md` header (predates the API/frontend) |

## Timeline (newest first)

### PDF report repair session — May 30, 2026 (`memory-bank/activeContext.md`)
- Fixed extension-key mismatches that caused "Data not available" in the premium report's Cognitive/Social/Leadership sections (`cognitive_social_career.py` `COGNITIVE_KEYS`/`SOCIAL_KEYS`/`LEADERSHIP_KEYS` aligned with actual extension output keys such as `memory_processing_score`, `communication_effectiveness_score`).
- Fixed `creativity_score` → `creativity_index_score` in `executive_summary.py`.
- `premium_pdf_report/generator.py`: pattern-family integers (0=arch, 1=loop, 2=whorl, 3=accidental) now mapped to strings; fixed a broken `per_finger` loop; bolder cover brain neural pattern (dark goldenrod, thicker lines, more nodes/gyri).
- Eliminated hardcoded fallbacks across report sections (`brain.py` 0% → N/A, `intelligence.py` no `'visual'`/EQ defaults, `development.py` early-return when MI missing).
- Layout fixes: `two_col()` overflow mode, `chart_image()` in `KeepTogether`, `repeatRows=1`/`splitByRow=1` on long tables, finger cards in `KeepTogether`.
- Verified end-to-end: real fingerprints → pipeline → 72 KB PDF, 9/9 cognitive, 8/8 social, 11/11 leadership scores populated.

### Scientific-accuracy remediation pass — *(inference, post-audit)*
`honest_full_system_audit.md` documented critical issues; the current code contains explicit `FIX:` comments addressing several of them:
- `dmit_intelligence_mapper.py`: interpersonal/intrapersonal/extraversion/neuroticism no longer weighted on `brain_criticality_score` / `neural_avalanches` / `quantum_consciousness_score`; TFRC normalization corrected from `/200` to `/25`.
- Preprocessing (`preprocessing_images.FingerToFingerprintPipeline`) is now wired into `IntegratedDMITPipeline` (the audit's "dead code" finding no longer holds).
- The audit file itself was **not** updated and should be read as historical.

### Backend API + persistence — *(inference, May 2026)*
- New `api/` package (untracked in git): FastAPI app, session/analysis routers, Pydantic schemas, SQLite persistence (`api/persistence.py`, `data/sessions.db`), write-through in-memory store. Supersedes the earlier purely in-memory store noted in `memory-bank/progress.md` ("Session store is in-memory — needs SQLite" is now partially resolved via SQLite).
- Static serving of `/uploads` and `/output` added in `api/main.py` (progress.md's "image thumbnails not served" is now resolved).
- Finger-slot upload contract (`finger_positions=L1..R5`, canonical `{SLOT}.{ext}` filenames) added via `api/helpers.py`.

### Frontend replacement — *(inference, May 2026)*
- Old `dmit-nextjs/` app deleted (git status shows `D dmit-nextjs/*`), replaced by the new `frontend/` Next.js app (untracked): 12+ routes, dark premium design system, Recharts visualizations, polling-based pipeline tracker. See `docs/PRODUCT_ROADMAP.md` (last updated 2026-05-16) for the route/feature matrix.

### Premium report generator — *(inference)*
- `premium_pdf_report/` package added as the API's report engine (`PremiumReportGenerator.create_report`), with cover watermark brain art, charts, and sectioned layout; the older `advanced_3d_pdf_generator` remains the CLI pipeline's report path.

### Scientific mapping rework — v3.1/3.2 *(inference)*
- `integrated_dmit_pipeline.py` rewritten around finger-type identification and Table 1.1 weighted-slot aggregation (Thumb→Prefrontal/personality, Index→Posterior-Frontal/logic, Middle→Parietal/kinesthetic, Ring→Temporal/musical-linguistic, Little→Occipital/visual).
- `dmit_intelligence_mapper.py` v2.0: per-finger primary-lobe boost with 0.2× dampening of non-primary lobes; pattern-family modifiers (whorl/loop/arch boosts) per research-paper findings.

### Original v3.0 platform — July 2025 (root `README.md`)
- 85-feature extractor (`optimized_feature_extractor_clean.py`), 61 extension modules, `advanced_3d_pdf_generator`, original Next.js UI (`dmit-nextjs/`), no API layer.

## Currently uncommitted (git status snapshot)

A large body of work is untracked/modified and not yet committed, including: the entire `api/` package, `frontend/` app, `docs/PRODUCT_ROADMAP.md`, `data/sessions.db`, `finger_prints/` test images, `dermatoglyphics_reverified_package/` (84-page scanned reference document + OCR), `clients idea/` (client report format references), modifications to all `dmit_extensions/*` and `advanced_3d_pdf_generator/core|visual/*`, and the deletion of `dmit-nextjs/`. Committing this work in reviewable chunks (per the conventional-commits workflow rule) is an outstanding task.

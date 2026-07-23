# Architecture

> Reverse-engineered from source. Companion docs: `DATA_FLOW.md` (runtime lifecycle), `COMPONENTS.md` (per-module reference), `DIAGRAMS.md` (all Mermaid diagrams), `API_REFERENCE.md` (endpoints).

## 1. What this system is

The **DMIT Analysis Platform** ingests up to 10 fingerprint images (one per finger, slots `L1`–`L5`, `R1`–`R5`), extracts ~85 biometric features per finger with classical computer vision (OpenCV/NumPy — no ML models in the live path), maps those features onto DMIT/Gardner constructs (multiple intelligences, brain lobes, learning styles, Big Five), runs 41 registered "extension" analyzers (EQ, career guidance, leadership, …), and produces:

1. A JSON analysis result served over a REST API and rendered in a Next.js web app.
2. A multi-section premium PDF report (ReportLab + matplotlib).

**Audience:** DMIT counselors/clinics, individuals, schools, and demo/investor showcases (see `docs/PRODUCT_ROADMAP.md`).

**Scientific posture:** the platform's own audit (`honest_full_system_audit.md`) and architecture mandate (`system_architecture.md`) drive a "biometric truth first / real data only" policy — palm-only metrics (ATD) and pseudoscientific features (quantum consciousness, brain criticality) now return `None`, mappings were rewritten to use real biometric measures, and report sections omit or mark `N/A` rather than fabricate values. The interpretive layer (features → psychology) remains DMIT theory, not validated science.

## 2. Layer model

```text
┌──────────────────────────────────────────────────────────────────────────┐
│  PRESENTATION                                                            │
│  frontend/  — Next.js 16 / React 19 / Tailwind v4 / Recharts (client-side│
│  only; talks to the API via fetch; polls analysis status every 1.8 s)    │
└────────────────────────────────▲─────────────────────────────────────────┘
                                 │ REST (JSON + multipart), static /uploads /output
┌────────────────────────────────┴─────────────────────────────────────────┐
│  API LAYER  api/                                                         │
│  main.py (app, CORS, static mounts, /api/health, warm imports)           │
│  routes/sessions.py (CRUD + upload)   routes/analysis.py (run/poll/PDF)  │
│  schemas.py (Pydantic v2)  helpers.py (slots)  store.py + persistence.py │
└────────────────────────────────▲─────────────────────────────────────────┘
                                 │ in-process call (asyncio.to_thread background task)
┌────────────────────────────────┴─────────────────────────────────────────┐
│  ORCHESTRATION  integrated_dmit_pipeline.py — IntegratedDMITPipeline     │
│  per-finger analysis + Table 1.1 weighted aggregation                    │
├──────────────────────────────────────────────────────────────────────────┤
│  CORE PROCESSING                                                         │
│  preprocessing_images/  (5-stage finger photo → fingerprint)             │
│  optimized_feature_extractor_clean.py  (85-feature extraction, tiers)    │
│  pattern_classifier.py  (Poincaré singular points, CADA families, TFRC)  │
│  dmit_intelligence_mapper.py  (features → MI/lobes/VAK/Big-Five)         │
│  dmit_extensions/  (engine + 41 registered extension analyzers)          │
├──────────────────────────────────────────────────────────────────────────┤
│  REPORTING                                                               │
│  premium_pdf_report/  (API path: 19-section ivory/gold ReportLab report) │
│  advanced_3d_pdf_generator/  (CLI path: 16-section dark-theme report)    │
├──────────────────────────────────────────────────────────────────────────┤
│  PERSISTENCE                                                             │
│  api/store.py (in-memory dict) ⇄ api/persistence.py (SQLite              │
│  data/sessions.db) + filesystem (uploads/, output/)                      │
└──────────────────────────────────────────────────────────────────────────┘
```

### Layer boundaries (as enforced by code)

- **Frontend ↔ API:** strictly HTTP. The frontend has no server-side code of its own (App Router pages are all client components; no Next API routes). Types in `frontend/src/lib/types.ts` mirror `api/schemas.py` by hand.
- **API ↔ Core:** the API imports `IntegratedDMITPipeline` and `PremiumReportGenerator` lazily inside the background task. Core modules know nothing about HTTP or sessions.
- **Extraction ↔ Interpretation:** `OptimizedFeatureExtractor` deliberately returns `intelligence_scores: {}` — all psychology mapping is owned by `dmit_intelligence_mapper.py` (one-way: features → profile). Extensions consume a *flat* dict of features + mapped MI scores via `DMITExtensionsEngine.run_all_extensions`.
- **Reporting:** both PDF engines are pure consumers of the pipeline result dict; they never call back into extraction.

## 3. Two report engines (important)

| | `premium_pdf_report/` | `advanced_3d_pdf_generator/` |
|---|---|---|
| Caller | **API** (`api/routes/analysis.py`) | **CLI pipeline** (`integrated_dmit_pipeline.run_complete_pipeline`) and `test_advanced_3d_pdf_generator.py` |
| Entry | `PremiumReportGenerator.create_report(pipeline_data, output_path, session)` | `create_3d_report(pipeline_data, output_path=…)` → `Simple3DGenerator` |
| Look | Ivory/gold, Times serif, 19 sections, cover brain watermark | Dark navy theme, 16 sections |
| Validation | No upfront validation; per-section gating + N/A policy | `RealDataProcessor.validate_real_data` hard-rejects invalid input (`ValueError`) |
| Charts | matplotlib → base64 PNG → ReportLab | matplotlib → base64 PNG → ReportLab (despite "3D" branding, charts are 2D; plotly imported but unused) |
| Output | `output/dmit_report_{session_id}.pdf` | `output/scientific_reports/dmit_scientific_{ts}.pdf` |

They share no code; the premium report is the product-facing one.

## 4. Synchronous vs asynchronous behavior

- **Request handlers** are `async def` but do trivial work (dict access, file writes).
- **The analysis run** is the only long operation. `POST /api/analysis/run` schedules `_run_pipeline(...)` on FastAPI `BackgroundTasks`; that coroutine immediately hops to a thread (`asyncio.to_thread(_run_pipeline_sync, …)`) because the pipeline is fully synchronous, CPU-bound OpenCV/NumPy code. The event loop stays responsive for polling.
- **Progress** is communicated by mutating `session["pipeline_stages"]` in shared memory; pollers see updates live. Nothing is durable mid-run (a crash strands the session in its last persisted status — see `ERROR_HANDLING.md`).
- There is **no job queue, no worker process, no WebSocket**; concurrency = number of threads FastAPI's default thread pool will give to `to_thread`.

## 5. Internal dependency graph and call chains

### Import graph (live path)

```text
api.main
 ├── api.routes.sessions ──► api.helpers, api.schemas, api.store
 ├── api.routes.analysis ──► api.helpers, api.schemas, api.store
 │       └─(lazy, in task)─► integrated_dmit_pipeline, premium_pdf_report
 └── api.store ──► api.persistence (sqlite3)

integrated_dmit_pipeline
 ├── preprocessing_images (FingerToFingerprintPipeline → 5 stage classes)
 ├── optimized_feature_extractor_clean (OptimizedFeatureExtractor)
 │       └── pattern_classifier (PatternClassifier; optional import)
 ├── dmit_intelligence_mapper (map_features_to_dmit_profile, FingerType)
 ├── dmit_extensions.engine (DMITExtensionsEngine → 41 extension classes)
 └── advanced_3d_pdf_generator (create_3d_report)   # CLI-only branch

premium_pdf_report.generator
 ├── premium_pdf_report.theme / charts / cover_background
 └── premium_pdf_report.sections.{cover,intro,executive_summary,fingerprint,
       brain,intelligence,cognitive_social_career,development} ──► sections.helpers
```

### Main call chain (API-triggered analysis)

```text
POST /api/analysis/run
 └─ _run_pipeline_sync(session_id, use_preprocessing, generate_pdf)
     ├─ IntegratedDMITPipeline(use_preprocessing)
     │   └─ analyze_multiple_fingers(image_paths)
     │       ├─ for each image: analyze_single_finger(path)
     │       │    ├─ _identify_finger_type(filename)          # L1/R1/_00… → thumb…little
     │       │    ├─ FingerToFingerprintPipeline.process()    # optional; fallback cv2.imread
     │       │    ├─ OptimizedFeatureExtractor.extract_optimized_features(image)
     │       │    │    └─ PatternClassifier.classify()        # family, subtype, cores/deltas, TFRC
     │       │    ├─ map_features_to_dmit_profile(features, finger_type)
     │       │    └─ DMITExtensionsEngine.run_all_extensions({features ∪ MI})
     │       └─ _aggregate_results_scientifically(results)    # Table 1.1 weighted slots
     │            └─ run_all_extensions(holistic_features)    # second, holistic pass
     ├─ _normalize_finger_results / _extract_* → AnalysisResult (Pydantic)
     └─ PremiumReportGenerator.create_report(full_result, output_path, session_meta)
```

## 6. The scientific aggregation model (Table 1.1)

The defining architectural decision of v3.x: **each finger is the primary signal source for one brain lobe / intelligence family**, per CADA-style "Table 1.1" mappings, instead of naive averaging across all 10 fingers.

| Finger | Brain lobe | Drives |
|---|---|---|
| Thumb (L1/R1) | Prefrontal | Inter/intrapersonal MI, existential, all Big Five |
| Index (L2/R2) | Posterior frontal | Logical-mathematical MI, spatial (co-driver), visual (co-driver) |
| Middle (L3/R3) | Parietal | Bodily-kinesthetic MI, kinesthetic learning |
| Ring (L4/R4) | Temporal | Linguistic + musical MI, auditory learning, naturalistic (co) |
| Little (L5/R5) | Occipital | Spatial (co), visual learning, naturalistic (co) |

Mechanics (two cooperating pieces):
1. **Mapper** (`dmit_intelligence_mapper._map_brain_hemispheres_and_lobes`): for a known finger, the primary lobe gets the full computed potential; all other lobes get **0.2×** (80% penalty). Pattern-family modifiers from the research paper are applied (whorl boosts logic/conscientiousness, loop boosts interpersonal/agreeableness, etc.).
2. **Pipeline aggregator** (`_aggregate_results_scientifically`): per trait, averages only the profiles of the **primary finger type(s)** (e.g. `logical_mathematical` from INDEX fingers only), falling back to all fingers when none of the primary type exist. Hemisphere biases average across all fingers.

A second, **holistic extension pass** then runs `run_all_extensions` over the aggregated MI scores (plus neutral physical features) to produce the report-level `extension_results`.

## 7. Feature extraction tiers

`OptimizedFeatureExtractor.extract_optimized_features(image, quality_level='auto')` self-assesses image quality (contrast 0.30, ridge clarity 0.30, SNR 0.20, histogram spread 0.20) and chooses a tier:

| Tier | Auto threshold | Adds |
|---|---|---|
| `basic` | score < 0.30 | pattern classification + ~21 basic features (stats, minutiae, fractal, topology, graph, TFRC, ridge, spectral, meta) |
| `core` | ≥ 0.30 | +33 (correlation dim, persistence, centralities, ridge flow, wavelets, cross-spectral; quantum/criticality keys present but `None`) |
| `advanced` | ≥ 0.40 | +27 advanced pattern analytics (whorl layering, double loop, peacock's eye, ATD placeholders=None, symmetry, fractal-ridge) |
| `comprehensive` | ≥ 0.50 | +18 comprehensive scalars (skewness, kurtosis, eigenvector centrality, spectral entropy, …) |

Output contract: `{extraction_summary, consolidated_features, intelligence_scores: {}, quality_metrics, timestamp, optimization_version}`. See `COMPONENTS.md` §3 for the full feature catalog.

## 8. Extension engine model

- Manual registry: `dmit_extensions/engine.py::extension_registry` lists **41 classes** (14 more modules exist but are unregistered legacy).
- Uniform interface: subclass `DMITExtensionBase`, implement `analyze(features: Dict) -> Dict`.
- Engine preprocessing: `adapt_features` (aliases, `pattern_family`→`pattern_type` string, `tfrc_normalized = min(1, tfrc/25)`), `_add_intelligence_aliases`, `_sanitize_features` (None→0.0).
- Output: `{ExtensionClassName: analyze_result_dict}`; an extension exception yields `{"error": msg}` for that key only.
- Convention: primary score key is `{domain}_score` or `{domain}_index`; **no `overall`/`recommendations` keys are actually produced** (the API's lookups for those are dormant fallbacks).
- Extensions always produce scores (defaults for missing features) — the **real-data-only enforcement lives in the mapper and report layers**, not in extensions.

## 9. Trust boundaries & security posture (current state)

- No authentication/authorization on any endpoint.
- Uploads are written to disk without content validation; static mounts expose all of `uploads/` and `output/` publicly.
- CORS is open to any localhost port by default (regex).
- SQLite file and PDFs are unencrypted on local disk.
This is acceptable for the current single-operator dev/demo deployment and is explicitly slated for Phase 2 hardening in `docs/PRODUCT_ROADMAP.md`.

## 10. Dormant / legacy assets (verified)

| Asset | Status |
|---|---|
| `FingerNet/` | Referenced by old docs; **directory effectively absent, zero imports** — not integrated |
| `dmit-nextjs/` | Deleted (replaced by `frontend/`) |
| `advanced_3d_pdf_generator/core/ai_engine.py` (`AIContentGenerator`) | Orphaned, never imported |
| 14 unregistered extensions (`creativity.py`, `leadership.py`, `memory.py`, `problem_solving.py`, …) | Exist but not in the registry — never run |
| `dmit_extensions/dashboard_pdf_generator.py`, `plotly_graph_generator.py`, `page_templates.py`, `visual_elements.py` | Support code for an older dashboard PDF; outside the live path |
| `create_bulletproof_dmit_analysis` (mapper) | Legacy compatibility wrapper |
| `quantum_dmit_pdf_generator.py`, `next_gen_dmit_enhancer.py` (named in old README) | **Do not exist** in the repo |

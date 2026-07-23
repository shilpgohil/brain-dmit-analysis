# Components Reference

> Folder-by-folder, file-by-file reference for every meaningful module. Exact class/function names from source. See `ARCHITECTURE.md` for how these fit together and `DATA_FLOW.md` for runtime order.

## Repository map

```text
brain-dmit-analysis/
├── api/                          # FastAPI backend (live product API)
├── frontend/                     # Next.js 16 web app (live product UI)
├── integrated_dmit_pipeline.py   # Orchestrator: per-finger analysis + aggregation
├── optimized_feature_extractor_clean.py   # 85-feature CV extractor
├── pattern_classifier.py         # Poincaré singular points, CADA pattern families, TFRC
├── dmit_intelligence_mapper.py   # Features → MI / brain lobes / VAK / Big Five
├── preprocessing_images/         # Finger photo → fingerprint (5 stages)
├── dmit_extensions/              # Extension engine + 41 registered analyzers
├── premium_pdf_report/           # API report engine (ivory/gold, 19 sections)
├── advanced_3d_pdf_generator/    # CLI report engine (dark theme, 16 sections)
├── docs/                         # This documentation suite + product roadmap
├── memory-bank/                  # Working agent context (activeContext, progress)
├── data/sessions.db              # SQLite session store (runtime)
├── uploads/ · output/            # Runtime artifacts (images, PDFs)
├── finger_prints/                # 10 real scanner BMPs (L1Center…R5Center) for tests
├── fingers/ · preprocessing_images tests    # preprocessing test inputs
├── dermatoglyphics_reverified_package/      # 84-page scanned reference book + OCR JSON
├── clients idea/                 # Client-facing report format references (PDF/DOCX)
├── scripts/test_api_premium_report.py       # E2E API test client
├── test_*.py                     # Root-level test/demo scripts
├── start_api.ps1 · start_frontend.ps1       # Dev launchers
├── requirements.txt              # Python deps
└── README.md · USAGE_GUIDE.md · system_architecture.md · honest_full_system_audit.md
```

---

## 1. `api/` — FastAPI backend

| File | Contents |
|---|---|
| `main.py` | App factory: `FastAPI(version="3.2", docs_url="/api/docs")`; `_warm_imports()` probes 4 core components for `/api/health`; CORS from `CORS_ORIGINS`/`CORS_ORIGIN_REGEX`; static mounts `/uploads`, `/output`; includes both routers; `GET /api/health`. `__main__` runs uvicorn on port 8001. |
| `schemas.py` | All Pydantic v2 models + enums (`AnalysisStatus`, `PatternType`, `FingerPosition`, `FingerBiometrics`, `BrainLobeCapacity`, `MultipleIntelligences`, `LearningStyles`, `PersonalityProfile`, `ExtensionResult`, `CareerMatch`, `PipelineStage`, `AnalysisSession`, `AnalysisResult`, `CreateSessionRequest`, `AnalyzeRequest`, `SessionListItem`, `SystemStatus`). Documented in `API_REFERENCE.md`. |
| `helpers.py` | `FINGER_POSITIONS` tuple; `parse_finger_position(filename)` (regex prefix + substring); `slot_filename(slot_id, original)` (canonical `{SLOT}.{ext}`, extension whitelist); `thumbnail_url_for_path(path)` (`uploads/...` → `/uploads/...` URL or None). |
| `store.py` | `session_store: Dict[str, Any]`; `init_store()` (hydrate from SQLite), `persist_session(id)`, `remove_session(id)`. |
| `persistence.py` | SQLite layer: `DB_PATH = data/sessions.db`; table `sessions(id, data JSON, updated_at)`; custom datetime/Enum/Pydantic JSON encoder + datetime-reviving object hook; `init_db`, `load_all_sessions`, `save_session` (upsert), `delete_session`. |
| `routes/sessions.py` | `POST /sessions`, `POST /sessions/{id}/images`, `GET /sessions`, `GET /sessions/{id}`, `DELETE /sessions/{id}`. |
| `routes/analysis.py` | `POST /analysis/run`, `GET /analysis/{id}`, `GET /analysis/{id}/report/download`, `POST /analysis/{id}/upload`; the pipeline runner `_run_pipeline_sync` and all result normalizers (`_normalize_finger_results`, `_extract_brain_lobes/_mi/_learning/_personality/_extensions/_careers`, `CAREER_FIELD_LABELS`, `_humanize_extension_name`). |

---

## 2. `integrated_dmit_pipeline.py` — `IntegratedDMITPipeline` (v3.2-Scientific-Full)

| Member | Purpose |
|---|---|
| `__init__(use_preprocessing=True)` | Builds `OptimizedFeatureExtractor`, optional `FingerToFingerprintPipeline`, `DMITExtensionsEngine`. |
| `_identify_finger_position(filename)` | `L1`–`R5` slot from filename. |
| `_identify_finger_type(filename)` | `FingerType` from tokens (`_00/_05/l1/r1/thumb` → THUMB, … `_04/_09/l5/r5/little` → LITTLE; else UNKNOWN). |
| `analyze_single_finger(path)` | Preprocess (with raw-image fallback) → extract → map (`map_features_to_dmit_profile`) → per-finger extensions on `{features ∪ MI}` → result record. Raises `FileNotFoundError`/`ValueError` per image. |
| `analyze_multiple_fingers(paths)` | Per-finger loop with per-image exception isolation; raises `ValueError("No fingers successfully analyzed")` if zero succeed; then `_aggregate_results_scientifically`. |
| `_aggregate_results_scientifically(results)` | Table 1.1 weighted-slot aggregation (see `ARCHITECTURE.md` §6) + holistic extension pass. |
| `generate_advanced_3d_pdf(results, output_path=None)` | CLI report path via `advanced_3d_pdf_generator.create_3d_report`; default `output/scientific_reports/dmit_scientific_{ts}.pdf`. |
| `run_complete_pipeline(paths, generate_pdf=True)` | analyze + optional CLI PDF. `main()` consumes a `"sample data"` folder. |

---

## 3. `optimized_feature_extractor_clean.py` — `OptimizedFeatureExtractor` (v2.0_enhanced)

- **Public API:** `extract_optimized_features(image: np.ndarray, quality_level='auto') -> Dict`. No constructor options. ~90 private methods.
- **Quality assessment** (`_assess_image_quality`): contrast (std/40, w=0.30) + ridge clarity (Laplacian/15, w=0.30) + SNR proxy (w=0.20) + histogram spread (p95−p5)/150 (w=0.20); failure default 0.5.
- **Tier thresholds:** `<0.30 basic`, `≥0.30 core`, `≥0.40 advanced`, `≥0.50 comprehensive` (manual values also accepted: `'basic'|'core'|'advanced'|'comprehensive'|'high'`).
- **Pattern classification runs at every tier** via `PatternClassifier` (graceful None if import fails).
- **Output:** `{extraction_summary {total_features_extracted, processing_time_seconds, quality_level, image_quality_score, data_reduction_percentage: 85.0 (hardcoded), accuracy_maintained: 0.96 (hardcoded)}, consolidated_features, intelligence_scores: {} (always empty — mapper owns MI), quality_metrics {image_quality, feature_confidence=(n/85)*0.6+q*0.4, extraction_reliability: 0.96 (hardcoded)}, timestamp, optimization_version}`.

### Feature catalog (13 categories, ~86 named keys)

| Category | Count | Keys |
|---|---|---|
| basic_stats | 5 | `mean_intensity`, `std_intensity`, `entropy`, `minutiae_count`, `minutiae_density` |
| fractal | 4 | `box_counting_dimension`, `lacunarity`, `correlation_dimension`, `scale_consistency` |
| topological | 5 | `betti_0`, `betti_1`, `euler_characteristic` (only if quality > 0.4), `persistence_entropy`, `topological_complexity` |
| graph | 6 | `graph_density`, `average_clustering`, `betweenness_centrality_mean`, `closeness_centrality_mean`, `modularity`, `spectral_radius` |
| ridge | 6 | `tfrc`, `ridge_density`, `ridge_flow_quality`, `dominant_direction`, `symmetry_index`, `frequency_stability` |
| level-3 skin | 4 | `pore_density`, `incipient_ridge_count`, `micro_texture_entropy`, `contour_complexity` |
| spectral | 4 | `fourier_energy_total`, `fourier_harmonic_ratio`, `wavelet_complexity`, `power_concentration` |
| advanced pattern | 27 | whorl layering/concentric/spiral, double-loop ×3, peacock ×3, reverse-shell ×3, composite ×3, ATD ×3 (**all None**), symmetry ×3, fractal-ridge ×3, betti ×3 |
| meta | 3 | `overall_quality_score`, `extraction_confidence`, `feature_stability` |
| quantum consciousness | 6 | **all `None` at runtime** (scientifically unsupported — kept as keys for schema compat) |
| brain criticality | 7 | **all `None` at runtime** |
| cross-spectral | 4 | `cross_spectral_fusion_score`, `multi_modal_integration`, `spectral_coherence`, `fusion_confidence` |
| pattern classification | 5 (+`ridge_count`) | `pattern_family` (arch=0/loop=1/whorl=2/accidental=3/-1), `pattern_subtype_code`, `triradii_count`, `core_count`, `pattern_confidence` |

Comprehensive tier adds 18 more scalars (`skewness`, `kurtosis`, `information_dimension`, `eigenvector_centrality`, `pagerank_score`, `ridge_thickness`, `spectral_entropy`, …).

Notable internals: minutiae via CLAHE + Harris corners (95th percentile, cap 30–80); topology via adaptive threshold + connected components (min area `max(20, h*w/5000)`); double-loop via Canny+contours (circularity > 0.3, ≥2); peacock via HoughCircles (≥3 circles); box-counting scales `[2,4,8,16,32,64]`.

---

## 4. `pattern_classifier.py`

| Item | Detail |
|---|---|
| `PatternFamily` | `whorl`, `loop`, `arch`, `accidental`, `unknown` |
| `PatternSubtype` | 23 CADA codes: whorls `Wt Ws We Wc Wd Wi Wp Rp Wl Rl`, loops `U R Lf Rf`, arches `As At Ae Au Ar`, accidentals `Xu Xw Xa Mf`, `?` |
| `PatternClassifier(config=None)` | Defaults: block 8, gaussian σ 2.0, Poincaré threshold 0.40, min confidence 0.5, max 2 cores / 2 deltas |
| `classify(image)` | orientation field (block Sobel, doubled-angle smoothing) → Poincaré index per block (core > +0.40, delta < −0.40, dedup 20 px) → family rules (0c0d→arch 0.9, 1c1d→loop 0.9, ≥1c2d→whorl 0.9, fallbacks at 0.6–0.7, else accidental 0.4) → subtype heuristics → TFRC |
| `calculate_tfrc` / `count_ridges_core_to_delta` | Core→delta line profile (2× oversampled), Gaussian smoothing, derivative zero-crossings ÷ 2; `ridge_count` = max over pairs |
| Output keys | `family, family_enum, subtype, subtype_enum, subtype_name, triradii_count, core_count, confidence, singular_points{cores,deltas}, ridge_count, ridge_counts_all` |
| `visualize(image, classification, output_path)` | Debug overlay (red cores, blue delta triangles) |
| `classify_fingerprint(image)` | Convenience wrapper |

Several subtype enum values (e.g. `PEACOCKS_EYE`) have names but no dedicated detection path — they fall through to defaults.

---

## 5. `dmit_intelligence_mapper.py` (v2.0 Scientific Refinement)

| Export | Purpose |
|---|---|
| `FingerType`, `BrainLobe`, `FINGER_LOBE_MAP` | Table 1.1 enums: thumb→prefrontal, index→posterior_frontal, middle→parietal, ring→temporal, little→occipital |
| `map_features_to_dmit_profile(features, finger_type_str='unknown')` | Main entry → `{multiple_intelligences, brain_mapping, learning_styles, personality_behavior, meta_data}` |
| `create_bulletproof_dmit_analysis(...)` | Legacy compatibility wrapper |

Formula highlights (all clamped [0,1], all from real biometric features after the audit remediation):
- `linguistic` = entropy/5×0.3 + fourier_harmonic_ratio×0.3 + pattern_symmetry×0.4 (+0.1 loop)
- `logical_mathematical` = whorl_layering×0.4 + (box_dim−1)×0.3 + topo_complexity×0.3 (+0.15 whorl)
- `bodily_kinesthetic` = ridge_density/0.5×0.4 + contour/100×0.4 + **tfrc/25**×0.2 (+0.15 whorl) — TFRC scale fixed from the audit's /200 bug
- `interpersonal` = graph_density×0.4 + clustering×0.3 + cross_spectral×0.3 (+0.2 loop) — criticality pseudoscience removed
- `intrapersonal` = stability×0.4 + spectral_coherence×0.3 + freq_stability×0.3 (+0.2 whorl)
- Lobes: per-lobe potentials; primary lobe full score, others ×0.2; unknown finger → undamped generic
- Big Five with pattern modifiers (whorl→openness/conscientiousness/extraversion; loop→agreeableness/neuroticism; arch→conscientiousness)

---

## 6. `preprocessing_images/` — `FingerToFingerprintPipeline`

| File | Class | Key parameters |
|---|---|---|
| `pipeline.py` | `FingerToFingerprintPipeline.process(image_path)` | orchestrates 5 stages; returns `{fingerprint, confidence (mean of stage confidences), metadata, success, stages_completed}` |
| `stage1_segmentation.py` | `FingerSegmenter` | Canny 50/150, morph kernel 5, min finger area ratio 0.05 |
| `stage2_validation.py` | `ShapeValidator` | aspect 2.0–6.0, convexity ≥ 0.7, min confidence 0.5 (non-fatal) |
| `stage3_roi_detection.py` | `FingertipROIDetector` | fingertip region ratio 0.25, ROI width 0.8 |
| `stage4_nail_removal.py` | `NailRemover` | smoothness threshold 0.3, nail region ≤ 0.15 |
| `stage5_ridge_enhancement.py` | `RidgeEnhancer` | CLAHE 2.0/8, Gabor freqs [0.1,0.15,0.2] × 8 orientations, percentile normalize; returns normalized grayscale |
| `__init__.py` | `convert_finger_to_fingerprint()` | one-shot helper |

Pure CV/geometry — explicitly no ML. Used by both the API (`use_preprocessing` flag, default true) and CLI pipeline.

---

## 7. `dmit_extensions/` — extension engine

- **`base.py`** — `DMITExtensionBase.analyze(features: Dict) -> Dict` (abstract).
- **`engine.py`** — `DMITExtensionsEngine`; manual `extension_registry` of **41 classes** (no auto-discovery); `run_all_extensions(features)` = `adapt_features` (aliases, `pattern_family`→`pattern_type` string, `tfrc_normalized=min(1,tfrc/25)`, derived fallbacks) → `_add_intelligence_aliases` → `_sanitize_features` (None→0.0) → per-extension `analyze()` with `{"error": msg}` isolation. Output keyed by **class name**.
- **Registered (41):** emotional/social/wellness (8: `EmotionalIntelligence`, `SelfRegulation`, `StressResponse`, `SocialAwareness`, `RelationshipDynamics`, `HealthWellness`, `WellnessIntelligence`, `Neurodivergence`), cognitive/brain (9: `LeftRightBrain`, `CognitiveLoad`, `ExecutiveFunction`, `MemoryProcessing`, `AttentionFocus`, `MetaCognition`, `PatternRecognition`, `SystemsThinking`, `DecisionMaking`), Gardner MIs (8), creativity (3: `CreativityIndex`, `InnovationIntelligence`, `CuriosityExploratory`), career/business (8: `CareerGuidance`, `LeadershipPotential`, `EntrepreneurialAptitude`, `RiskTolerance`, `FinancialIntelligence`, `DigitalIntelligence`, `CulturalIntelligence`, `SustainabilityIntelligence`), learning/motivation (5: `LearningStyle`, `LearningAgility`, `CommunicationStyle`, `MotivationDrive`, `PersistenceGrit`).
- **Unregistered (14 legacy, never run):** `adaptability_resilience`, `creativity`, `innovation_creativity`, `interpersonal_skills`, `leadership`, `leadership_skills`, `memory`, `memory_learning`, `problem_solving`, `stress_management`, `team_collaboration`, `time_management`, `visual_intelligence`, `work_style` (+2 feature-mapping extension wrappers).
- **Common template:** most extensions compute 8 sub-dimension scores from a shared ~40-key feature pool (defaults 0.0/0.5/1.5/'loop'), weight them into `{domain}_score`, pick `primary_{domain}_style` via max, add composite sums and a `{domain}_profile` label (5- or 6-tier classification). **No extension emits `overall` or `recommendations`.**
- **`LeftRightBrainExtension`** is the structural outlier: ATD-angle logic with a symmetry-based fallback when ATD is absent (always, for fingerprints); outputs `left/right_brain_score`, `brain_dominance_type`, `brain_integration_score`.
- **Known quirks:** `NeurodivergenceExtension` TFRC band check (`<500 or >1800`) runs on normalized 0–1 TFRC so never triggers meaningfully; `MemoryProcessingExtension` defines `memory_integration` twice (second wins).
- **Support modules (outside scoring path):** `theme_constants.py`, `page_templates.py`, `plotly_graph_generator.py`, `dashboard_pdf_generator.py`, `visual_elements.py`, `feature_mapping_adapter.py`, `feature_mapping_validator.py`.

---

## 8. `premium_pdf_report/` — API report engine (v1.0.0)

- **Entry:** `PremiumReportGenerator.create_report(pipeline_data, output_path=None, session=None) -> str` (default output `output/scientific_reports/dmit_premium_{ts}.pdf` when path omitted; API passes `output/dmit_report_{sid}.pdf`). No internal try/except — caller handles errors.
- **Modules:** `generator.py` (orchestrator, data extraction, 19-section story), `theme.py` (ivory/gold palette, Times styles, `score_color()` 5-tier, A4 layout constants), `charts.py` (matplotlib Agg → base64 PNG, 150 DPI, ~18 chart factories), `cover_background.py` (cover brain watermark PNG), `sections/*` (one module per section group), `sections/helpers.py` (`section_header`, `sub_heading`, `chart_image`, `score_table`, `two_col` overflow-mode, `pill_table`, `info_card`), `scripts/build_cover_watermark.py` (offline asset build), `assets/` (watermark PNGs).
- **19 sections in order:** cover → scientific intro → candidate profile → executive summary (gauges/tiles/pills) → fingerprint quality (bar+donut+table) → per-finger cards → hemisphere → lobes → MI (radar+bars+table) → learning (pie+bar) → personality (radar+bars) → EQ (radar) → cognitive → social → leadership → career+SWOT → parenting → development plan → counsellor note + signature. Conditional sections are omitted entirely when data gates fail.
- **Real-data policy:** `_real()` keeps only positive numerics; zero-filtering of profile dicts; `N/A` rendering; first-match `_gather_scores(ext_results, keys)` accepting only values in [0,1]. Extension score keys harvested via `COGNITIVE_KEYS` (11), `SOCIAL_KEYS` (8), `LEADERSHIP_KEYS` (11) — see `API_REFERENCE.md` companion and `memory-bank/activeContext.md` for the key-alignment fix history. Note: `problem_solving_score`/`analytical_thinking` in `COGNITIVE_KEYS` can never appear because `ProblemSolvingExtension` is unregistered.
- **Static fallbacks that remain:** default counsellor name, hardcoded SWOT opportunities/threats, static daily routine and pattern descriptions.

---

## 9. `advanced_3d_pdf_generator/` — CLI report engine (v3.0.0)

- **Exports:** `Simple3DGenerator` (classmethod API, the workhorse), `Advanced3DGenerator` (thin delegating wrapper; its extra flags `include_insights/careers/development`, `custom_branding` are dead), `RealDataProcessor`, `Real3DChartGenerator`, `create_3d_report(pipeline_data, **kw)`, `generate_advanced_3d_report` (no callers).
- **`core/real_data_processor.py`:** `validate_real_data` (returns `(bool, errors)`; checks pipeline_info, non-empty individual_results, MI dict present with all scores in [0,1]); `extract_real_intelligence_data` (prefers `aggregated_analysis`, falls back to `individual_results[0]`; raises `ValueError` after failed validation); rule-based `generate_real_insights` / `generate_real_career_recommendations` / `generate_real_development_plan` (template text scaled by real scores — not LLM); `EXTENSION_GROUPS` (6 groups, 39 class names), `interpret_score`, `derive_personality_archetype`.
- **`visual/real_chart_generator.py`:** matplotlib-only (plotly imported but never renders); 14 chart keys from `generate_all_3d_charts` (radar, bars, pie, EQ radar, grouped extension bars, finger pattern charts); dark `#1a1a2e` theme; base64 PNG output; per-chart failure → `''`.
- **`core/pdf_builder.py`:** `PDFBuilder.build_3d_pdf(report_data, output_path, theme)` — A4, ivory background, Times styles, 16 sections (cover → exec summary → patterns → MI → brain → learning → personality → EQ → cognitive → social/leadership → motivation/creativity → specialized → career intelligence → career recommendations → development → technical details). `theme`/`style` parameters are accepted but **have no effect**.
- **`core/ai_engine.py`:** `AIContentGenerator` — orphaned (never imported anywhere).
- **Used by:** `integrated_dmit_pipeline.generate_advanced_3d_pdf` and `test_advanced_3d_pdf_generator.py`. **Not used by the API.**

---

## 10. `frontend/` — Next.js app

- **Stack:** Next 16.2.6, React 19.2.4, Tailwind v4 (CSS-first, no config file), Recharts 3.8, framer-motion, Lenis smooth scroll, lucide-react. App Router, all pages client components, no Next API routes, no middleware. Unused-but-installed: radix-ui, three/@react-three, gsap, zustand.
- **Routes:** `/` (cinematic landing + recent sessions), `/analysis/new` (10-slot upload grid R1–R5/L1–L5, purpose selector, toggles), `/analysis/[id]` (poll 1.8 s; tabs Overview/Fingerprints/Extensions/Career; PDF button), `/analysis/[id]/finger/[finger]` (per-finger detail + raw features), `/sessions`, `/compare`, `/extensions` (static catalog), `/learn` (glossary/encyclopedia), `/solutions`, `/about`, `/system` (health), `/settings` (localStorage-only — **not** wired to the API client), custom 404.
- **API client** (`src/lib/api.ts`): `BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api"` ⚠️ (backend launcher uses **8001** — set the env var; see `CONFIGURATION.md`). Functions: `createSession`, `listSessions`, `getSession`, `deleteSession`, `uploadImagesWithSlots` (renames files to `{slot}.{ext}`, sends `finger_positions`), `runAnalysis`, `getAnalysis`, `getHealth`, `mediaUrl`, `reportDownloadUrl`, plus an unused `pollUntilComplete`.
- **Types** (`src/lib/types.ts`): hand-written mirror of `api/schemas.py` (kept in sync manually).
- **Key components:** `PipelineTracker` (stage list w/ status+durations), results tabs (`OverviewTab` with `GoldRadarChart` + `BrainLobeDiagram`, `ExtensionsTab`, `CareerTab`, `MetricStrip`), `CompareView`, `IntelligenceCard` (DMIT knowledge tooltips from `dmit-knowledge.ts`), effects (`AmbientOrbs`, `CursorGlow`, `FingerprintField`), primitives (`GlassCard`, `MagneticButton`). Several legacy components are defined but unused (`FingerprintCard`, `UploadZone`, `IntelligenceRadar`, `BrainLobeChart`, `LearningStylePie`, `Sidebar`, `TopBar`).
- **Design system:** dark-only; tokens in `globals.css` (`--bg-void #020208`, `--accent-gold #c4a574`, `--accent-sage`, `--accent-plum`); Cormorant Garamond display / Inter body / JetBrains Mono.
- **Client-side fallback:** `lib/derive-careers.ts` rebuilds career matches from the `career_guidance` extension when the API list is empty.

---

## 11. Tests, scripts, assets

| File | What it does |
|---|---|
| `scripts/test_api_premium_report.py` | Full E2E over HTTP (httpx): health → create session → upload 10 BMPs from `finger_prints/` with slots → run → poll 3 s (max 600 s) → download PDF to `test_server_premium_report.pdf`. **Requires the API running on 8001.** |
| `test_complete_pipeline.py` | CLI E2E: `finger_prints/*.bmp` → `run_complete_pipeline(generate_pdf=True)` → prints profile; PDF to `output/scientific_reports/`. |
| `test_advanced_3d_pdf_generator.py` | Exercises `RealDataProcessor` + `Simple3DGenerator` against saved pipeline JSON (`test_output/new_pipeline_test/new_pipeline_results.json` — must be generated first). |
| `test_preprocessing.py` | Batch-runs `FingerToFingerprintPipeline` over `fingers/`, writes processed prints + side-by-side comparisons to `test_output/preprocessing_results/`. |
| `create_dummy_image.py` | Synthesizes a 640×480 finger-like test image → `fingers/synthetic_thumb.jpg`. |
| `test_brain_mapping.py`, `test_scientific_mapping.py`, `test_feature_batch.py`, `test_scanner_fingerprint.py` | Focused checks of mapper outputs, batch extraction, scanner input handling. |
| `test_*.pdf` (root) | Generated artifacts from past runs (cover/brain/sparse/no-defaults experiments) — not inputs. |
| `finger_prints/` | Canonical 10-print scanner test set (`L1Center.bmp` … `R5Center.bmp`). |
| `dermatoglyphics_reverified_package/` | 84 scanned reference pages + `ocr_texts.json` + transcript — research source material for the scientific mappings. |
| `clients idea/` | Client-provided report format references (Premium Plus PDF, draft DOCX formats). |
| `memory-bank/` | Agent working memory (`activeContext.md` fix log, `progress.md` status). |
| `brain by cursor.code-workspace` | VS Code/Cursor workspace file. |

## 12. Gaps & dead ends (explicit)

- `FingerNet/` is empty/dormant — no imports anywhere.
- `AnalysisResult.fingers[].singular_points` is never populated (classifier produces them, normalizer doesn't pass them through).
- Hemisphere key mismatch (`left_hemisphere` vs `left_hemisphere_bias`) makes API hemisphere values 0 (premium PDF handles both spellings).
- `ExtensionResult.recommendations` and `CareerMatch.key_strengths` are always empty (no producer).
- `/settings` page settings are not consumed by the API client.
- `memory-bank/` lacks `projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md` (only `activeContext.md` and `progress.md` exist).

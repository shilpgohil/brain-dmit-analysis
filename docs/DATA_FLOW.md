# Data Flow

> End-to-end lifecycle of a DMIT analysis, traced from the browser to the final PDF. Exact function names from the codebase. Diagrams in `DIAGRAMS.md`.

## 0. Actors and artifacts

| Artifact | Produced by | Consumed by |
|---|---|---|
| Uploaded images `uploads/{sid}/{SLOT}.{ext}` | `POST /api/sessions/{id}/images` (or `/api/analysis/{id}/upload`) | `IntegratedDMITPipeline`, frontend thumbnails |
| Session document (memory + `data/sessions.db`) | session routes + pipeline runner | all routes, frontend polling |
| `full_result` pipeline dict | `IntegratedDMITPipeline.analyze_multiple_fingers` | API normalizers + `PremiumReportGenerator` |
| `AnalysisResult` (Pydantic) | `_run_pipeline_sync` | `GET /api/analysis/{id}`, frontend |
| PDF `output/dmit_report_{sid}.pdf` | `PremiumReportGenerator.create_report` | report download endpoint |

## 1. Session creation & upload flow

```text
Browser (/analysis/new)
  1. user fills subject form, assigns files to 10 slots (R1..R5, L1..L5 grid)
  2. createSession()        → POST /api/sessions          {subject_name, subject_age, notes:"Purpose: …"}
        server: uuid4 id, status=pending, mkdir uploads/{id}/, persist to SQLite
  3. uploadImagesWithSlots() → POST /api/analysis/{id}/upload
        client renames each file to {slotId}.{ext}; sends finger_positions="R1,R2,…"
        server: slot resolution (form positions → filename parsing fallback),
                canonical save as uploads/{id}/R1.bmp …,
                session.image_paths += paths, finger_slots[slot]=path, persist
  4. runAnalysis()          → POST /api/analysis/run      {session_id, use_preprocessing, generate_pdf}
        server: guards (404 / 400 no images / 409 already running),
                clears previous result/error/report, status=preprocessing,
                BackgroundTasks → asyncio.to_thread(_run_pipeline_sync)
  5. router.push(/analysis/{id})  → polling starts
```

Slot semantics: `R1..R5` = right thumb→little, `L1..L5` = left thumb→little. The canonical filename matters downstream — `IntegratedDMITPipeline._identify_finger_type` re-derives the finger *type* (thumb/index/…) from the filename (`l1`,`r1`,`_00`… tokens), and `_identify_finger_position` re-derives the slot.

## 2. Analysis pipeline flow (background thread)

`_run_pipeline_sync(session_id, use_preprocessing, generate_pdf)` in `api/routes/analysis.py`:

```text
stage list initialized: preprocessing → extraction → mapping → extensions → report
status: PREPROCESSING
  IntegratedDMITPipeline(use_preprocessing) constructed
    (instantiates OptimizedFeatureExtractor, FingerToFingerprintPipeline, DMITExtensionsEngine)

status: EXTRACTING   (stage "extraction" running)
  full_result = pipeline.analyze_multiple_fingers(session.image_paths)
```

### 2a. Per-finger analysis (`analyze_single_finger`)

For each image path (failures are caught per finger; ≥1 success required):

1. **Finger identity** — `_identify_finger_type(filename)` → `FingerType` enum (`thumb|index|middle|ring|little|unknown`); `_identify_finger_position(filename)` → `L1`–`R5`.
2. **Preprocessing** (if enabled) — `FingerToFingerprintPipeline.process(image_path)`:
   - Stage 1 `FingerSegmenter`: Sobel+Canny(50/150) edges → morphology → largest elongated blob.
   - Stage 2 `ShapeValidator`: aspect ratio 2.0–6.0, convexity ≥ 0.7 (continues with low confidence on failure).
   - Stage 3 `FingertipROIDetector`: crop top 25% of finger, 80% width.
   - Stage 4 `NailRemover`: masks nail region (≤15% of ROI).
   - Stage 5 `RidgeEnhancer`: CLAHE(2.0/8) → orientation field → ridge frequency → Gabor bank (3 freqs × 8 orientations) → percentile normalize.
   - Returns `{fingerprint, confidence, metadata, success, stages_completed}`. On failure: **fallback to raw `cv2.imread(path, IMREAD_GRAYSCALE)`**.
3. **Feature extraction** — `OptimizedFeatureExtractor.extract_optimized_features(image)`:
   - quality score → tier (`basic`/`core`/`advanced`/`comprehensive` at 0.30/0.40/0.50 cuts);
   - `PatternClassifier.classify()` always runs: orientation field → Poincaré index (±0.40) → cores/deltas (max 2 each) → family (arch 0c0d / loop 1c1d / whorl ≥1c2d / accidental) → subtype heuristics → **TFRC** = max ridge count over core–delta line profiles;
   - tiered feature groups merge into `consolidated_features` (~85 keys; quantum/criticality/ATD keys explicitly `None`).
4. **Intelligence mapping** — `map_features_to_dmit_profile(features, finger_type_str)`:
   - `_map_core_intelligences`: 8 MI formulas from real features + pattern-family boosts (whorl→logic/intrapersonal, loop→linguistic/interpersonal/musical);
   - `_map_brain_hemispheres_and_lobes`: per-lobe potentials; primary lobe (Table 1.1) keeps full score, others ×0.2;
   - `_map_learning_styles` (VAK), `_map_personality_behavior` (Big Five + pattern modifiers); all clamped to [0,1].
5. **Per-finger extensions** — `DMITExtensionsEngine.run_all_extensions({**features, **mi_scores})` → `{ExtensionClassName: result_dict}` (41 extensions; defaults make them always score).
6. Result record:

```python
{
  'pipeline_info': {image_path, finger_type, finger_position, timestamp},
  'feature_extraction': {extraction_summary, consolidated_features, quality_metrics, …,
                         preprocessing_metadata?},
  'dmit_analysis': {dmit_profile, extension_results}
}
```

### 2b. Scientific aggregation (`_aggregate_results_scientifically`)

- Groups per-finger profiles by `FingerType`.
- `get_avg_score(category, key, source_fingers)`: average over **primary fingers only** (fallback: all fingers; then 0.0).
- Builds `agg_mi` (9 MIs from their Table 1.1 source fingers), `agg_brain` (each lobe from its single primary finger; hemisphere biases averaged over all), `agg_ls` (VAK), `agg_pb` (Big Five from thumbs).
- **Holistic extension pass**: `run_all_extensions({**agg_mi, atd_average_angle: None, tfrc_normalized: mean})` → the `extension_results` the API/report actually use.
- Returns:

```python
{
  'pipeline_info': {pipeline_version, total_fingers_analyzed, fingers_found, aggregation_timestamp},
  'individual_results': [...],
  'aggregated_analysis': {'dmit_profile': final_profile, 'extension_results': holistic_extensions}
}
```

## 3. Result normalization flow (API)

Back in `_run_pipeline_sync`:

| Extractor | Input | Output |
|---|---|---|
| `_normalize_finger_results(individual_results)` | per-finger records | `List[FingerBiometrics]` (pattern coerced to enum, `tfrc`→`ridge_count`, thumbnail URL, scalar `raw_features`) |
| `_extract_brain_lobes(agg)` | `dmit_profile.brain_mapping` | `BrainLobeCapacity` (note: reads `left_hemisphere`, pipeline emits `left_hemisphere_bias` → hemispheres come out 0; see API_REFERENCE) |
| `_extract_mi` / `_extract_learning` / `_extract_personality` | profile sub-dicts | Pydantic models |
| `_extract_extensions(ext_results)` | `{ClassName: scores}` | `List[ExtensionResult]` — humanized names, category map, `primary_score`, sorted desc |
| `_extract_careers(ext_results)` | `career_guidance` scores | `List[CareerMatch]` top-12 via `CAREER_FIELD_LABELS` |

`AnalysisResult` is assembled, warnings attached (partial finger failures), `total_features_extracted` summed.

## 4. Report generation flow

When `generate_pdf=true` (status `GENERATING_REPORT`, stage `report`):

```text
PremiumReportGenerator.create_report(pipeline_data=full_result,
                                     output_path=output/dmit_report_{sid}.pdf,
                                     session=session_meta)
  1. Profile extraction priority: aggregated dmit_profile → legacy intelligence_scores
     → fallback individual_results[0].dmit_analysis
  2. Zero-filter: drop keys with value ≤ 0 from MI/brain/learning/personality
  3. per_finger records from individual_results (pattern int→str map; _real() keeps only >0)
  4. career_matches from ext_results['CareerGuidanceExtension'] (8 *_career keys)
  5. Build story: 19 sections (cover → intro → profile → exec summary → fingerprint
     quality → finger cards → hemispheres → lobes → MI → learning → personality → EQ →
     cognitive → social → leadership → career/SWOT → parenting → development → counsellor)
     — conditional sections omitted when their data gate fails
  6. Charts: matplotlib(Agg) figures → base64 PNG (150 DPI, in-memory) → ReportLab Image
  7. doc.build(story, onPage=_page_background)  # ivory bg, cover watermark, footer rule, page no.
```

Failure here is non-fatal: caught, logged, `warnings += ["Report generation failed: …"]`, stage `report` marked failed, analysis still completes (`report_url=null`).

Finally: `session["result"] = AnalysisResult`, `status=COMPLETED`, `persist_session` (single SQLite upsert of the whole session JSON).

## 5. Retrieval & rendering flow

```text
/analysis/[id] page mounts → getAnalysis(id) → GET /api/analysis/{id}
  while status ∈ {preprocessing, extracting, mapping, extending, generating_report}:
      setInterval 1800 ms → re-fetch; PipelineTracker renders pipeline_stages live
  on completed:
      OverviewTab: GoldRadarChart (MI), brain lobe diagram + bars, Big Five, VAK pie
      Fingerprints tab: per-finger cards (thumbnail via mediaUrl(thumbnail_url) → /uploads/…)
      ExtensionsTab: category chart + searchable grid of ExtensionResult
      CareerTab: career_matches or client-side derive-careers fallback
      PDF button: href = reportDownloadUrl → GET /api/analysis/{id}/report/download
  on failed: error_message + failed stage details
```

Session archive (`/sessions`) and compare (`/compare`) read `GET /api/sessions` and per-id results; `/system` renders `GET /api/health`.

## 6. Persistence & reuse flow

- Every mutation → `persist_session` (write-through JSON upsert into `data/sessions.db`).
- On API restart, `init_store()` rehydrates all sessions; completed results and `report_path` survive, so downloads keep working without recomputation.
- Stored `result` dicts are lazily re-validated into `AnalysisResult` models on first `GET` after a restart.
- Re-running analysis on a completed/failed session is allowed; it clears `result`/`report_path` and overwrites the PDF path.

## 7. CLI flow (no API)

`python integrated_dmit_pipeline.py` (or `test_complete_pipeline.py`):

```text
images from "sample data"/ or finger_prints/
  → IntegratedDMITPipeline.run_complete_pipeline(paths, generate_pdf=True)
      → analyze_multiple_fingers(...)             # identical core flow
      → generate_advanced_3d_pdf(results)         # NOTE: uses advanced_3d_pdf_generator,
            create_3d_report(...)                 # not premium_pdf_report
            → RealDataProcessor.validate_real_data  (hard ValueError on bad data)
            → Real3DChartGenerator.generate_all_3d_charts
            → PDFBuilder.build_3d_pdf → output/scientific_reports/dmit_scientific_{ts}.pdf
```

## 8. Data shape quick reference

```jsonc
// consolidated_features (per finger, excerpt)
{ "pattern_family": 2, "pattern_subtype_code": 13, "triradii_count": 2, "core_count": 1,
  "tfrc": 18.0, "ridge_density": 0.31, "minutiae_count": 64, "entropy": 4.4,
  "box_counting_dimension": 1.78, "lacunarity": 0.42, "betti_0": 12, "betti_1": 7,
  "graph_density": 0.21, "average_clustering": 0.44, "wavelet_complexity": 0.51,
  "atd_average_angle": null, "quantum_consciousness_score": null, … }

// aggregated dmit_profile
{ "multiple_intelligences": {"linguistic": 0.62, …9 keys…},
  "brain_mapping": {"prefrontal_lobe": 0.55, …, "left_hemisphere_bias": 0.48, "right_hemisphere_bias": 0.52},
  "learning_styles": {"visual": 0.58, "auditory": 0.49, "kinesthetic": 0.61},
  "personality_behavior": {"openness": 0.66, …} }

// extension_results (holistic, excerpt)
{ "EmotionalIntelligenceExtension": {"emotional_intelligence_score": 0.58,
      "primary_emotional_style": "empathy", "emotional_awareness": 0.61, …},
  "CareerGuidanceExtension": {"career_potential_score": 0.55, "technical_career": 0.52,
      "stem_careers": 1.04, "primary_career_aptitude": "analytical_career", …}, … }
```

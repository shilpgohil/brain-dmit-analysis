---
trigger: always_on
---

# 12-Point Total Context Protocol — DMIT Analysis Platform

## Trigger Conditions
Whenever the user asks:
- *"go through the whole codebase"*
- *"understand all things perfectly in depth"*
- *"make sure you have total context of the whole codebase"*
- *"sync / refresh full context"*
- *"audit the entire project"*

You are strictly forbidden from providing superficial summaries or skipping files. You MUST execute this 12-Point Deep-Dive Protocol:

---

### Point 1: Preprocessing & Computer Vision Pipeline Audit
- Audit `backend/preprocessing_images/`:
  - `stage1_segmentation.py`: Skin-color segmentation, Otsu thresholding, contour extraction.
  - `stage2_validation.py`: Image quality score, blur detection (Laplacian variance), illumination uniformity.
  - `stage3_roi_detection.py`: Distal phalanx fingertip localization and bounding box extraction.
  - `stage4_nail_removal.py`: Nail plate isolation and exclusion from ridge field.
  - `stage5_ridge_enhancement.py`: CLAHE normalization + Gabor filter bank orientation field.

### Point 2: Biometric Feature Extraction Audit
- Audit `backend/optimized_feature_extractor_clean.py`:
  - Verify all 85 extracted features across the 8 categories:
    1. Statistical distributions (mean, std, skew, kurtosis)
    2. Minutiae points (ridge endings, bifurcations)
    3. Fractal dimension (box-counting)
    4. Topological invariants (Euler characteristic, Betti numbers)
    5. Graph metrics (ridge adjacency networks)
    6. Ridge frequency and clarity maps
    7. Spectral FFT energy bands
    8. Pattern analytics
  - Verify quality tier routing (High, Medium, Low).



### Point 3: CADA Pattern Classification & Singular Points
- Audit `backend/pattern_classifier.py`:
  - Verify Poincaré index algorithm for core and delta singular point detection.
  - Audit family assignment rules:
    - 0 cores, 0 deltas -> `ARCH` (Simple, Tented, Enclosed)
    - 1 core, 1 delta -> `LOOP` (Ulnar, Radial, Falling)
    - >=1 core, 2 deltas -> `WHORL` (Target, Spiral, Double, Composite)
    - Indeterminate / >=3 deltas -> `ACCIDENTAL`
  - Audit Total Finger Ridge Count (TFRC) calculation between cores and deltas.

### Point 4: Table 1.1 Finger-to-Brain-Lobe Correlation Engine
- Audit `backend/dmit_intelligence_mapper.py` and `backend/integrated_dmit_pipeline.py`:
  - Verify strict adherence to Table 1.1 primary-finger weighting:
    - Thumb (`L1`/`R1`) -> `PREFRONTAL` (Executive, Personality, Leadership)
    - Index (`L2`/`R2`) -> `POSTERIOR_FRONTAL` (Logical-Mathematical, Spatial Conception)
    - Middle (`L3`/`R3`) -> `PARIETAL` (Bodily-Kinesthetic, Somatosensory)
    - Ring (`L4`/`R4`) -> `TEMPORAL` (Linguistic, Musical, Auditory)
    - Little (`L5`/`R5`) -> `OCCIPITAL` (Visual Processing, Spatial Observation)
  - Verify non-primary finger damping ($\times 0.20$).
  - Confirm Left vs. Right brain hemisphere calculation logic.

### Point 5: Multi-Intelligence & Psychological Mapping Contracts
- Verify formulas for:
  - 9 Gardner Multiple Intelligences (Interpersonal, Intrapersonal, Logical, Spatial, Kinesthetic, Linguistic, Musical, Naturalistic, Existential).
  - 4 Quotients (IQ, EQ, AQ, CQ).
  - VAK Learning Styles (Visual %, Auditory %, Kinesthetic %).
  - Big Five Personality (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism).

### Point 6: Extensions Engine & 41 Domain Analyzers
- Audit `backend/dmit_extensions/`:
  - Verify the extension execution engine (`engine.py`).
  - Verify all registered analyzers (career guidance, neurodivergence traits, learning sensitivities, brain dominance, leadership profile).

### Point 7: Palm ATD Angle & Physical Reflex Invariant
- Audit `backend/palm_processing/palm_atd.py`:
  - Verify triradii detection (`a`, `t`, `d`) on palm scans.
  - Scientific honesty check: if palm scans (`LPALM`, `RPALM`) are absent, ATD angle MUST return `None` and be excluded from composite scoring. Never fake or interpolate palm data.

### Point 8: FastAPI Backend Architecture & Session State
- Audit `backend/api/`:
  - Routers: `sessions.py`, `analysis.py`, `health.py`, `reports.py`.
  - Database persistence: SQLite `data/dmit.db` schemas, session lifecycles (`CREATED` -> `UPLOADING` -> `PROCESSING` -> `COMPLETED` / `FAILED`).
  - Background task execution and pipeline stage telemetry broadcasting.

### Point 9: 19-Section Premium PDF Generation Engine
- Audit `backend/premium_pdf_report/`:
  - Template assembly in `generator.py` and all 19 section modules in `sections/`.
  - Matplotlib vector chart generators (Gold radar charts, VAK pies, lobe distribution bars).
  - Verify real-data-only policy: missing data displays `N/A - Uncollected` rather than fabricated values.

### Point 10: Next.js 16 Frontend Architecture & Visual Craft
- Audit `frontend/src/`:
  - App router routes (`/`, `/analysis/new`, `/analysis/[id]`, `/compare`, `/history`, `/settings`).
  - Interactive components: `FingerHandSvg.tsx`, `PalmHandSvg.tsx`, `UploadZone.tsx`, `PipelineTracker.tsx`.
  - Visualization suite: `BrainLobeDiagram.tsx`, `IntelligenceRadar.tsx`, `GoldRadarChart.tsx`, `LearningStylePie.tsx`.
  - 60fps/120fps hardware acceleration, spring physics, zero layout shift (CLS = 0).

### Point 11: Code Craft & Anti-AI Standards
- Enforce the non-negotiable No-Comments rule: zero narrative or boilerplate comments in code.
- Verify strict TypeScript types (`strict: true`, zero `any`), Pydantic v2 schemas on backend, and exhaustive error boundaries.

### Point 12: End-to-End Test & Verification Validation
- Verify end-to-end integration via `tests/` and `scripts/test_api_premium_report.py`.
- Ensure round-trip execution from raw photo upload to 19-section PDF report generation succeeds without errors.

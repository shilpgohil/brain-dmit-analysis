# DMIT Analysis Platform — Master Context & Engineering Invariants

## 1. Product Identity & Purpose
**DMIT Analysis Platform** (Version 3.2 "Scientific-Full") is an institutional-grade biometric analysis engine, REST API, interactive web terminal, and premium PDF report platform for **Dermatoglyphics Multiple Intelligence Testing (DMIT)**.

The platform processes up to 10 fingerprint images (`L1`..`L5`, `R1`..`R5`) and palm scans (`LPALM`, `RPALM`) through an automated computer vision pipeline, classifies ridge patterns via the CADA standard, maps biometric features to human cerebral lobes using research-backed **Table 1.1** correlations, and computes comprehensive multi-intelligence, psychological, and behavioral profiles.

Every component, visualization, and interaction is engineered to meet the highest standards of craft, comparable to **GPT Astra, Claude, Fable, Linear, Apple, and Stripe**.

```text
UPLOAD (10 Fingerprints + Palm) 
   │
   ▼
PREPROCESS (Segmentation ➔ Validation ➔ ROI ➔ Nail Removal ➔ CLAHE/Gabor)
   │
   ▼
EXTRACT (85 Biometric Features + CADA Core/Delta Poincaré Classification + TFRC)
   │
   ▼
MAP (Table 1.1 Lobe Aggregation ➔ 9 Multiple Intelligences ➔ 4 Quotients ➔ VAK ➔ Big Five)
   │
   ▼
EXTEND & REPORT (41 Registered Analyzers ➔ Next.js Dark Terminal ➔ 19-Section Ivory/Gold PDF)
```

---

## 2. Technology Stack & Topology

| Layer | Technology | Primary Responsibility |
| :--- | :--- | :--- |
| **Backend** | Python 3.12+, FastAPI, Pydantic v2, Uvicorn | Async session manager, background analysis tasks, REST API (`http://localhost:8001`) |
| **CV Engine** | OpenCV (`cv2`), NumPy, SciPy | 5-stage photo preprocessing, minutiae extraction, orientation field, Poincaré index |
| **Database** | SQLite (`data/dmit.db`) | Analysis sessions, uploaded image paths, serialized feature vectors, report artifacts |
| **Frontend** | Next.js 16 (App Router), React 19, TypeScript (`strict: true`), Tailwind CSS v4 | Dark obsidian biometric command deck, interactive SVG hands, radar charts, live pipeline tracker |
| **Typography** | `Plus Jakarta Sans` / `Inter` (UI/Labels) + `JetBrains Mono` (Telemetry/Numbers) | Tabular alignment (`tnum`, `zero`) preventing numerical character jitter |
| **PDF Engine** | ReportLab, Matplotlib | 19-section luxury PDF generation with Ivory/Gold theme and vector charts |
| **Skills & CLI** | `ui-ux-design-pro` (.agents/skills) + Node.js/Bun CLI | 107+ styles, 127+ palettes, 150+ reasoning rules, 12 craft references, UI audit CLI |

---

## 3. Ten Inviolable Core Invariants

### Invariant 1: Table 1.1 Primary-Finger Weighting Invariant
- The correlation between digits and brain lobes must strictly mirror Table 1.1:
  - Thumb (`L1`/`R1`) ➔ Prefrontal Lobe (Executive, Leadership, Inter/Intrapersonal MI)
  - Index (`L2`/`R2`) ➔ Posterior Frontal Lobe (Logical-Mathematical, Spatial Conception)
  - Middle (`L3`/`R3`) ➔ Parietal Lobe (Bodily-Kinesthetic, Somatosensory, Motor Skills)
  - Ring (`L4`/`R4`) ➔ Temporal Lobe (Linguistic, Musical, Auditory Processing)
  - Little (`L5`/`R5`) ➔ Occipital Lobe (Visual, Spatial Observation, Aesthetics)
- Each lobe score is primarily driven by its primary finger slot; secondary cross-finger contributions are strictly damped ($\times 0.20$). Naive arithmetic averaging is strictly forbidden.

### Invariant 2: Scientific Honesty & Real-Data-Only Invariant
- The platform presents DMIT correlations as empirical developmental heuristics, never clinical diagnostic truth.
- Real-data-only policy: missing finger slots must be honestly reported; never fabricate ridge counts.
- If palm scans (`LPALM`, `RPALM`) are absent, the ATD angle MUST return `None` and display `N/A - Uncollected`. Zero data fabrication.

### Invariant 3: Strict No-Comments Invariant
- Code must be 100% clean, expressive, and self-documenting.
- ABSOLUTE BAN on narrative, explanatory, or boilerplate comments in code.
- Intent is communicated entirely through descriptive domain naming, strong typing, and modular structure.

### Invariant 4: Continuous Conversation Context Auto-Sync
- Every conversation turn introducing new decisions, scoring rules, design preferences, or bug fixes must immediately synchronize to `memory-bank/` (`activeContext.md`, `progress.md`, `systemPatterns.md`, `techContext.md`, `productContext.md`).

### Invariant 5: Total Context Protocol Trigger
- Whenever asked to *"go through the whole codebase"*, *"understand all things in depth"*, or *"audit the entire project"*, the agent is strictly bound to execute the 12-Point Total Context Protocol without shortcuts.

### Invariant 6: 60fps / 120fps Hardware Acceleration & Zero Layout Shift (CLS = 0)
- Animate only `transform`, `opacity`, and composited `filter` properties using organic spring physics (`stiffness: 400`, `damping: 30`).
- Skeletons and card containers must have strict reserved bounding dimensions to guarantee CLS = 0.

### Invariant 7: Dual Palette Architecture
- Web Command Deck: Cinematic Obsidian (`#030712`) with 24px blurred glass surfaces (`#0B0F19`), subpixel 1px machined borders, and electric cyan / gold accents.
- Premium PDF Report: Luxury Ivory (`#FAF8F5`) and Gold (`#D4AF37`) with charcoal typography (`#1F2937`).

### Invariant 8: Typographic Strictness
- `Inter` / `Plus Jakarta Sans` for general UI text.
- `JetBrains Mono` (`font-mono tabular-nums slashed-zero`) for all numerical readouts, scores, percentages, and ridge counts.

### Invariant 9: 19-Section Premium PDF Report Integrity
- Complete coverage of all 19 standard sections without omitting required analyses.
- High-DPI Matplotlib vector charts (polar radar polygons, VAK donuts, lobe bar distribution).

### Invariant 10: Anti-AI Code Standard
- Strict typing across frontend (TypeScript `strict: true`, zero `any`) and backend (Pydantic v2 schemas).
- No placeholder mocks, unhandled promises, or swallowed exceptions.

---

## 4. Deep-Dive Trigger Protocol (12-Point Execution)

Whenever asked to go through the whole codebase in depth, execute:
1. **Preprocessing & CV Pipeline Audit**: Verify skin segmentation, blur validation, ROI, nail removal, CLAHE/Gabor.
2. **85-Feature Extraction Audit**: Verify statistical, minutiae, fractal, topological, graph, and spectral features.
3. **CADA Pattern Classification Audit**: Verify Poincaré core/delta detection, Whorl/Loop/Arch/Accidental classification, and TFRC calculation.
4. **Table 1.1 Correlation Engine Audit**: Verify strict lobe mappings and $\times 0.20$ cross-lobe damping.
5. **Multi-Intelligence & Quotient Contracts**: Verify 9 Gardner MIs, 4 quotients, VAK, and Big Five formulas.
6. **Extensions Engine Audit**: Verify the 41 registered domain analyzers.
7. **Palm ATD Angle Invariant**: Confirm strict `None` handling when palm is absent.
8. **FastAPI Backend & Session State**: Verify routes, SQLite schemas, and stage telemetry.
9. **19-Section Premium PDF Engine**: Verify report generator and vector charts.
10. **Next.js 16 Frontend Craft**: Verify interactive SVG hands, lobe heatmap, radar charts, and 60fps motion.
11. **Code Craft & No-Comments Rule**: Verify zero boilerplate comments and strict typing.
12. **End-to-End Verification**: Validate round-trip execution from upload to PDF generation.

---

## 5. Active Workspace Rules Catalog (`.agents/rules/`)

1. **[full_codebase_deep_dive_protocol.md](.agents/rules/full_codebase_deep_dive_protocol.md)**: 12-point Total Context deep-dive execution blueprint.
2. **[dmit_biometrics_and_lobe_mapping.md](.agents/rules/dmit_biometrics_and_lobe_mapping.md)**: Table 1.1 matrix, CADA taxonomy, TFRC, and ATD invariants.
3. **[backend_fastapi_and_cv_pipeline.md](.agents/rules/backend_fastapi_and_cv_pipeline.md)**: FastAPI architecture, 5-stage CV pipeline, 85 features, and SQLite state.
4. **[world_class_ui_ux_and_animation_craft.md](.agents/rules/world_class_ui_ux_and_animation_craft.md)**: 60fps/120fps GPU acceleration, spring physics, and biometric visuals.
5. **[code_craft_and_anti_ai_rules.md](.agents/rules/code_craft_and_anti_ai_rules.md)**: Non-negotiable No-Comments rule, anti-AI standards, and type safety.
6. **[conversation_context_auto_sync.md](.agents/rules/conversation_context_auto_sync.md)**: Continuous memory bank synchronization protocol.
7. **[design_tokens_and_micro_craft.md](.agents/rules/design_tokens_and_micro_craft.md)**: Dual obsidian/ivory palettes, machined borders, and tabular typography.

---

## 6. Specialized Skills Catalog (`.agents/skills/`)

1. **[ui-ux-design-pro](.agents/skills/ui-ux-design-pro/SKILL.md)**: Senior AI design intelligence engine with 107+ styles, 127+ palettes, 107+ font pairings, 150+ reasoning rules, 12 craft references, and executable CLI.
2. **[dmit-biometric-scoring-engine](.agents/skills/dmit-biometric-scoring-engine/SKILL.md)**: Biometric feature scoring, CADA classification, TFRC, Table 1.1 weighting, 9 MI, and 4 quotients.
3. **[dmit-report-generator](.agents/skills/dmit-report-generator/SKILL.md)**: 19-section luxury PDF report generator, Matplotlib vector charts, and ivory/gold layout.
4. **[conversation-context-sync](.agents/skills/conversation-context-sync/SKILL.md)**: Real-time conversation synchronization into living memory bank files.

---

## 7. Operating Scripts & CLI Commands

- **Start API**: `.\start_api.ps1` (Runs on `http://localhost:8001`)
- **Start Frontend**: `.\start_frontend.ps1` (Runs on `http://localhost:3000`)
- **Design System CLI**: `scripts\design-cli.bat generate "DMIT Biometric Terminal" --stack nextjs`
- **Design Audit CLI**: `scripts\design-cli.bat audit frontend/src/components/...`
- **End-to-End Smoke Test**: `python scripts/test_api_premium_report.py`

---

Workspace: `c:\Users\BAPS\Documents\space\brain-dmit-analysis`  
Last updated: October 2026

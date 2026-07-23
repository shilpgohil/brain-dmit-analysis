# Documentation Index

Enterprise documentation suite for the DMIT Analysis Platform, reverse-engineered directly from the source code (June 2026).

## Start here

| Doc | Read it for |
|---|---|
| [`../README.md`](../README.md) | Project overview, quick start |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Layer model, boundaries, sync/async behavior, dependency graph, the Table 1.1 scientific model, dormant assets |
| [`DATA_FLOW.md`](DATA_FLOW.md) | Full request lifecycle: upload → pipeline → aggregation → report → polling → persistence; CLI flow; data shapes |
| [`COMPONENTS.md`](COMPONENTS.md) | Folder-by-folder, file-by-file reference: every class, function, feature catalog, extension registry, frontend inventory |
| [`API_REFERENCE.md`](API_REFERENCE.md) | All 10 endpoints with schemas, validation, errors, side effects; every Pydantic model and enum |
| [`DIAGRAMS.md`](DIAGRAMS.md) | Mermaid: system architecture, data flow, dependency graph, sequence, storage schema, finger→lobe mapping, state machine |
| [`STORAGE_AND_PERSISTENCE.md`](STORAGE_AND_PERSISTENCE.md) | In-memory store ⇄ SQLite write-through, JSON serialization rules, file layout, concurrency, limitations |
| [`ERROR_HANDLING.md`](ERROR_HANDLING.md) | HTTP errors, pipeline failure semantics, graceful degradation, defensive patterns, known weak spots |
| [`CONFIGURATION.md`](CONFIGURATION.md) | Every env var, port, path constant, tunable threshold, dependency list |
| [`DEPLOYMENT.md`](DEPLOYMENT.md) | Local setup, running, testing, packaging guidance, common failure points & fixes |
| [`CHANGELOG_NOTES.md`](CHANGELOG_NOTES.md) | Reconstructed project history and uncommitted-work inventory |
| [`DMIT_SCIENCE_REFERENCE.md`](DMIT_SCIENCE_REFERENCE.md) | The source research book (`dermatoglyphics_reverified_package/`) reconciled against the backend: Table 1.1, CADA classification, pattern→personality, TFRC, atd angle — what's faithful, extrapolated, or excluded |
| [`PRODUCT_ROADMAP.md`](PRODUCT_ROADMAP.md) | (Pre-existing) audiences, feature matrix, phased delivery plan |

## Pre-existing root documents and how to read them

| Doc | Status |
|---|---|
| `../system_architecture.md` | Design **mandate** (target architecture & integrity rules) — largely realized; keep as the spec |
| `../honest_full_system_audit.md` | Historical audit — several findings since fixed in code (see `CHANGELOG_NOTES.md`); read as point-in-time |
| `../USAGE_GUIDE.md` | Legacy v3.0 guide — references files/dirs that no longer exist (`dmit-nextjs/`, `quantum_dmit_pdf_generator.py`); superseded by this suite |
| `../Testing Image Preprocessing.md` | Exported chat log, not a spec |

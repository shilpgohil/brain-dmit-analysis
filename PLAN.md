# DMIT Project Restructure + Consultant Build Plan

_Created: Aug 22, 2026_

---

## Why restructure first

Zenith-AI rule: root contains ONLY config (`requirements.txt`, `.gitignore`, `docker-compose.yml`) +
entry scripts (`start_api.ps1`) + top-level docs (`README.md`). Everything else lives inside
a named package.

DMIT root currently has 40+ loose items: core library `.py` files, 9 test scripts,
8 test PDFs, reference DOCX/PDF, loose docs, logs, and empty folders. Before adding the
DMIT Consultant (another ~20 files), the root must be clean or it becomes unmanageable.

---

## Phase 1 — Codebase Reorganisation

### 1A — Safe moves (zero import changes, do immediately)

| Move from (root) | Move to | Notes |
|---|---|---|
| `test_advanced_3d_pdf_generator.py` | `tests/` | |
| `test_backend_fixes.py` | `tests/` | |
| `test_brain_mapping.py` | `tests/` | |
| `test_complete_pipeline.py` | `tests/` | |
| `test_dmit_core.py` | `tests/` | |
| `test_feature_batch.py` | `tests/` | |
| `test_preprocessing.py` | `tests/` | |
| `test_scanner_fingerprint.py` | `tests/` | |
| `test_scientific_mapping.py` | `tests/` | |
| `create_dummy_image.py` | `scripts/` | |
| `test_brain_cover.pdf` | `test_output/` | |
| `test_cover_brain_demo.pdf` | `test_output/` | |
| `test_final.pdf` | `test_output/` | |
| `test_final_fixed.pdf` | `test_output/` | |
| `test_no_defaults.pdf` | `test_output/` | |
| `test_real_final.pdf` | `test_output/` | |
| `test_server_premium_report.pdf` | `test_output/` | |
| `test_sparse.pdf` | `test_output/` | |
| `Compatibility Report.docx` | `samples/` | Create folder |
| `Revied Report.docx` | `samples/` | |
| `DOC-20241117-WA0021..pdf` | `samples/` | |
| `system_architecture.md` | `docs/` | |
| `USAGE_GUIDE.md` | `docs/` | |
| `Testing Image Preprocessing.md` | `docs/` | |
| `honest_full_system_audit.md` | `docs/` | |
| `uvicorn_boot.log` | DELETE | Runtime noise |
| `FingerNet/` (empty) | DELETE | |
| `fingers/` (empty) | DELETE | |
| `tmp_scan2.py` in `scripts/` | DELETE | Leftover scratch |

**Result:** root drops from ~40 items to ~10. Exactly like Zenith.

---

### 1B — Core Python module restructure (requires import updates)

The 4 largest Python files live at root because they were the original pipeline scripts.
Moving them into a `core/` package is the right long-term structure.

**New package: `core/`**
```
core/
├── __init__.py
├── integrated_dmit_pipeline.py      (moved from root)
├── optimized_feature_extractor_clean.py (moved from root)
├── dmit_intelligence_mapper.py      (moved from root)
└── pattern_classifier.py            (moved from root)
```

**Files that import these and need updating after the move:**
- `api/routes/analysis.py` — `from integrated_dmit_pipeline import IntegratedDMITPipeline`
- `dmit_extensions/engine.py` — indirectly via pipeline
- `premium_pdf_report/generator.py` — none directly
- `scripts/full_e2e_run.py` — direct imports
- Any file in `tests/` that imports these
- `palm_processing/palm_atd.py` — none
- `dmit_intelligence_mapper.py` internal cross-imports

**Strategy:** add root-level shim files after move so old imports don't break:
```python
# integrated_dmit_pipeline.py  ← thin shim at root
from core.integrated_dmit_pipeline import *  # noqa: F401, F403
```

---

### Target root after Phase 1
```
brain-dmit-analysis/
├── api/                          backend API routes + server
├── core/                         NEW: 4 core pipeline modules
├── dmit_consultant/              NEW (Phase 2): LangGraph agent
├── dmit_extensions/              extension engine + 46 modules
├── palm_processing/              ATD palm estimation
├── preprocessing_images/         CLAHE/Gabor/segmentation
├── premium_pdf_report/           PDF generator + sections
├── advanced_3d_pdf_generator/    (legacy 3D generator)
├── dermatoglyphics_reverified_package/  research paper
├── frontend/                     Next.js app
├── data/                         sessions.db
├── docs/                         all .md documentation
├── memory-bank/                  activeContext, progress, pending
├── scripts/                      utility/run scripts
├── tests/                        all test_*.py
├── test_output/                  test PDFs/JSONs/logs
├── samples/                      client reference DOCX/PDFs
├── finger_prints/                sample fingerprint images (keep)
├── extras/                       zenith-ai reference project
├── .gitignore
├── README.md
├── requirements.txt
├── start_api.ps1
├── start_frontend.ps1
└── brain by cursor.code-workspace
```

---

## Phase 2 — DMIT AI Consultant

Framework decision: **LangGraph** (see framework comparison in chat).
Stack: LangGraph + LangChain utilities + OpenAI gpt-4o-mini + ChromaDB (research paper) + SqliteSaver (session memory, reuses existing `data/sessions.db`).

### 2A — Research paper RAG

Files: `dermatoglyphics_reverified_package/dermatoglyphics_reverified_transcript.md` (134 KB, 84 pages)

Steps:
1. Chunk with `RecursiveCharacterTextSplitter` (500 tokens, 50 overlap)
2. Embed with `text-embedding-3-small`
3. Store in `ChromaDB` persisted at `data/research_chroma/`
4. Tool: `search_research_paper(query)` → top-3 chunks + page refs

One-time build, stored to disk. No need to re-embed on every startup.

### 2B — DMIT tools (10 total)

All backed by real data from the session store. None fabricate values.

| Tool | Returns |
|---|---|
| `get_full_report(session_id)` | Complete AnalysisResult (quotients, MI, lobes, ATD, careers) |
| `get_finger_detail(session_id, slot_id)` | One finger's biometrics (pattern, ridge count, quality) |
| `get_quotient_profile(session_id)` | 10 quotients with labels and scores |
| `get_career_matches(session_id, top_n)` | Ranked careers with suitability % and required quotients |
| `get_brain_lobe_profile(session_id)` | 5-lobe + per-lobe hemisphere split |
| `get_mi_profile(session_id)` | 9 MI scores with interpretations |
| `search_research_paper(query)` | RAG: top-3 chunks from the 84-page study |
| `get_population_norm(pattern_type)` | Population % from research paper tables |
| `get_development_suggestions(session_id, area)` | Activities for a weak quotient/lobe |
| `explain_atd_angle(session_id)` | ATD data + range + processing speed meaning |

### 2C — LangGraph agent structure

```
consultant_graph
├── [START]
├── intake_node          (pre-consult questionnaire: purpose, concern)
│   └── → consultant_node  (when intake complete)
├── consultant_node      (main AssistantAgent: DMIT tools + system prompt)
│   └── → tools_node      (when tool calls needed)
│   └── → rag_node        (when science/research question detected)
│   └── → [END]           (when answered)
├── tools_node           (ToolNode: runs DMIT tools)
│   └── → consultant_node
└── rag_node             (retrieval + grounded answer)
    └── → consultant_node
```

Session memory: `SqliteSaver` checkpointing on `data/sessions.db` (same file).

### 2D — Streaming protocol (identical to Zenith)

Same `StreamResponse` NDJSON schema:
```python
class ConsultantStreamResponse(BaseModel):
    chunk_type: str = "text"       # status | text | suggestions | done
    response: str = ""
    stream_completed: bool = False
    status: Optional[str] = None   # thinking | tool_call | tool_done | generating
    status_message: Optional[str] = None
    suggested_questions: Optional[list] = None
    report_section: Optional[str] = None  # which section this relates to
```

Client: `fetch` + `ReadableStream` reader, split on `\n`, parse JSON — same as Zenith frontend contract.

### 2E — API endpoints (new router: `/api/consultant`)

```
POST  /api/consultant/initiate      → {thread_id, subject_name, session_id}
POST  /api/consultant/stream_chat   → NDJSON StreamingResponse
POST  /api/consultant/end_chat      → persist + cleanup
GET   /api/consultant/history       → past threads for this session
POST  /api/consultant/suggestions   → 3-4 follow-up question chips
```

### 2F — Frontend chat panel

New `ConsultantPanel` component on the analysis results page:
- Collapsible side panel / bottom sheet
- Auto-loads when analysis is `completed`
- Greets with top insight: "I can see your strongest intelligence is {topMI} at {score}%…"
- Shows suggested question chips (loaded via `/suggestions`)
- Streams responses with status shimmer → text append
- Session tied to the analysis `session_id`

### 2G — File structure for new module

```
dmit_consultant/
├── __init__.py
├── agent.py             LangGraph graph definition
├── tools.py             All 10 DMIT tools
├── prompts.py           System prompt + intake templates
├── rag.py               Research paper chunking + ChromaDB
├── session.py           SqliteSaver + thread management
├── schemas.py           ConsultantStreamResponse + request models
└── status_messages.py   User-facing status copy (same Zenith pattern)
```

---

## Execution order

1. **Phase 1A** — safe file moves (tests, docs, PDFs, logs, empty folders)
2. **Phase 1B** — `core/` package + shim files + import updates + verify backend starts
3. **Phase 2A** — RAG: chunk + embed + Chroma store (one-time build)
4. **Phase 2B** — 5 core tools: `get_full_report`, `get_quotient_profile`, `get_career_matches`, `get_brain_lobe_profile`, `get_mi_profile`
5. **Phase 2C** — LangGraph graph: consultant node + tools node + streaming
6. **Phase 2D** — `/api/consultant/stream_chat` endpoint (NDJSON streaming)
7. **Phase 2E** — Remaining tools (RAG search, ATD, development suggestions, norms)
8. **Phase 2F** — Pre-consult intake questionnaire (state machine)
9. **Phase 2G** — Frontend ConsultantPanel component
10. **Phase 2H** — Question suggestions + chat history endpoints

---

## Install (Phase 2)

```bash
pip install langgraph langchain langchain-openai langgraph-checkpoint-sqlite chromadb tiktoken
```

No new databases. No new services. Reuses existing SQLite + existing FastAPI server.

---

## What stays out of scope

- Couple Compatibility Report (separate product, deferred)
- Dashboard-specific changes (awaiting specs)
- Production deployment / auth on the consultant endpoint
- Multi-language support

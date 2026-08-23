# Pending Tasks / Backlog

_Last updated: Aug 22, 2026._
This is the single source of truth for "what's left to do." Update it whenever a
task is completed or a new one is raised — don't let it go stale like
`activeContext.md`/`progress.md` did.

---

## 1. New requests (raised Aug 22, 2026 — not yet started)

### 1.1 Accept fingerprint-scanner images, not just phone photos
- Currently the pipeline auto-detects "scanner-grade" images to skip phone-photo
  preprocessing (CLAHE/Gabor/segmentation), but this needs a full audit against
  **actual USB fingerprint scanner output** (different DPI, bit depth, contrast,
  and file format than what's been tested so far — typically 500 DPI grayscale
  BMP/WSQ from optical or capacitive scanners).
- Need to confirm: upload accepts the real file types/extensions scanners
  produce, image-quality heuristics don't misclassify scanner images as
  low-quality phone photos (or vice versa), and the "skip preprocessing"
  auto-detection threshold is actually correct for scanner hardware, not just
  assumed.
- Reference doc: `DOC-20241117-WA0021..pdf` describes a standard scanner
  capture workflow (per finger: flat + left-tilt + right-tilt = 3 images per
  finger, 30 images per subject) — worth deciding whether we support only the
  single "flat" image per finger (current model) or eventually the full 3-angle
  capture for higher ridge-count accuracy.

### 1.2 Dynamic, animated upload guidance UI (frontend)
- Current upload screen (`frontend/src/app/analysis/new/page.tsx`) is static:
  a grid of small labeled slots (L1, L2, R1...). No guidance on *how* to
  position/scan a finger, no illustration of which physical finger maps to
  which slot.
- Requested: an animated, guided upload flow — e.g. when a user taps to upload
  a given slot, show a short animation/illustration explaining "this is the
  index finger, place it like this" before/while the file picker opens, so
  the experience feels dynamic rather than a bare grid of tiny boxes.
- Needs design decisions: per-finger illustration/animation assets, whether
  it's a modal/tooltip/inline step-by-step wizard, and how it coexists with
  the existing bulk-upload flow (added earlier this project).

### 1.3 Report generation + dashboard changes (incoming, details TBD)
- User said more concrete changes are coming for both the **PDF report
  generation** and the **frontend dashboard**. Not yet specified — placeholder
  until details arrive.

### 1.4 Report content enrichment — reference docs received
Three reference documents were provided, outlining a much richer target report
than what currently exists. These are **not a finalized spec** — they're
raw brainstorm/vendor material the user wants incorporated selectively. Full
breakdown:

- **`DOC-20241117-WA0021..pdf`** — general DMIT background knowledge (history,
  science, fingerprint-type definitions, brain-lobe mapping, ATD angle
  definition, benefits, myths/facts, scanner capture process). This is the
  source material for a **"What is DMIT" foundational knowledge section**
  the user wants added near the start of the report (education before data).

- **`Revied Report.docx`** — a 17-section, ~95-110-page "AI Ridge Analysis"
  premium report blueprint. Key ideas worth evaluating (not all will be
  built — needs a phased plan, see Section 2 below):
  - A **10-Quotient system** (IQ, EQ, CQ, AQ, SQ, PQ, LQ, MQ, FQ, DQ) as a
    standardized layer that every trait/career/section maps onto — proposed
    as a replacement/superset for the current IQ/EQ/CQ/AQ-only framing.
  - **10-lobe brain model** (5 lobes × left/right hemisphere individually,
    not just aggregate left-brain-%/right-brain-%).
  - Dedicated **ATD Angle chapter** (a-b ridge count, atd/dat/adt angles,
    symmetry index, bilateral balance — currently we only have a single
    geometric-estimate atd angle from palm photos, not real ridge-triradius
    angles).
  - **SWOT-style "Personality DNA"** section richer than current SWOT.
  - Expanded **Career DNA**: top 25 (or 100+) careers organized into 32
    career-family chapters, each scored against the 10 quotients, plus
    Career Suitability %, Risk Level, Income Potential, Automation
    Resistance, Future Demand, AI-Era Suitability, Entrepreneurship Score.
  - **Competitive-exam brain-suitability chapter** (UPSC, SSC, NEET, JEE, CAT,
    CLAT, banking, defence, judiciary, etc.) — currently nonexistent.
  - **Development Roadmap** (30-day / 90-day / 1-year plans with concrete
    activities — reading, exercises, games, meditation, memory practice).
  - New proprietary indices (AI Ridge Intelligence Score, Brain Synchronization
    Index, Cognitive Flexibility Score, etc.) — marketing/USP framing.
  - Implies a possible **rebrand** from "DMIT" to "AI Ridge Analysis" — needs
    an explicit decision from the user before touching branding.

- **`Compatibility Report.docx`** — spec for an entirely **new report
  product**: a two-person "Couple Compatibility Report" (~20+ sections)
  comparing two individuals' quotient profiles, brain-lobe profiles, and
  personality traits, producing compatibility percentages and proprietary
  indices (Brain Synchronization Index, Complementary Strength Index,
  Communication Harmony Index, Emotional Balance Index, Relationship Growth
  Index, Parenting Compatibility Index). This is a **new feature**, not an
  enrichment of the existing single-person report — it needs its own data
  model (pairing two sessions), its own PDF template, and its own frontend
  entry point.

---

## 2. Completed Aug 22, 2026

All Phase 0 and Phase 1 items from the plan were implemented and verified live:
- Phase 0A: Scanner image support, upload validation, `.wsq` gap fixed
- Phase 0B: Animated per-finger guidance overlay (SVG hand, first-visit onboarding)
- Phase 1.1: DMIT foundational knowledge in PDF intro
- Phase 1.2: 10-quotient engine wired through pipeline → API → PDF
- Phase 1.3: Enriched SWOT / Personality DNA
- Phase 1.4: 48-career database (25 families) with quotient-based matching
- Phase 1.5: ATD dedicated PDF chapter (geometric estimate, labeled)
- Phase 1.6: Per-lobe hemisphere split (10 values) in brain section
- Phase 1.7: Section reordering per spec
- Verified: 27-page PDF generated cleanly, all 10 quotients computed from real data

---

## 3. Carried over from previous audit (still outstanding)

- **Nothing from this project is committed to git.** All backend accuracy
  fixes, the full PDF redesign, and all frontend fixes (bulk upload, chart
  tooltips, search box) exist only as uncommitted working-tree changes.
  Should be committed in logical chunks before more work piles on top.
- `scripts/tmp_scan2.py` — leftover scratch/debug file from the earlier
  extraction audit; delete rather than commit.
- `memory-bank/activeContext.md` and `memory-bank/progress.md` are stale
  (describe a May 30 snapshot) and should be refreshed once the current
  round of work settles.
- Session store durability: confirm SQLite (or equivalent) persistence is
  actually wired in everywhere, not just in-memory dicts that reset on
  restart.
- No authentication/authorization on the API at all.
- Background pipeline execution isn't durable — a server restart mid-analysis
  loses that job (no resumability/retry).
- Image thumbnail serving for uploaded fingerprints — confirm this actually
  works end-to-end now (was previously flagged as missing).
- No fresh full end-to-end run (upload → pipeline → PDF) has been done since
  the bulk-upload / chart-tooltip / search-box frontend fixes — worth doing
  once before this batch of work is considered fully verified.

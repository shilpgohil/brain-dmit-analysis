# DMIT Platform — Product Roadmap & Master Plan

> **Vision:** A premium, enterprise-grade Dermatoglyphics Multiple Intelligence Test (DMIT) platform serving individuals, counselors, institutions, and strategic partners — with scientific transparency and cinematic UX.

> **Audiences (all in scope):**  
> **A)** Individual at home · **B)** DMIT counselor / clinic · **C)** School / corporate batch · **D)** Investor / partner showcase

---

## Table of Contents

1. [Strategic Pillars](#1-strategic-pillars)
2. [Audience A — Individual at Home](#2-audience-a--individual-at-home)
3. [Audience B — Counselor / Clinic](#3-audience-b--counselor--clinic)
4. [Audience C — School / Corporate Batch](#4-audience-c--school--corporate-batch)
5. [Audience D — Showcase / Investors](#5-audience-d--showcase--investors)
6. [Frontend Roadmap (Implemented vs Planned)](#6-frontend-roadmap)
7. [Backend & Infrastructure Roadmap](#7-backend--infrastructure-roadmap)
8. [DMIT Content & Education Layer](#8-dmit-content--education-layer)
9. [Visualization & Reporting](#9-visualization--reporting)
10. [Phased Delivery Plan](#10-phased-delivery-plan)
11. [Success Metrics](#11-success-metrics)

---

## 1. Strategic Pillars

| Pillar | Description |
|--------|-------------|
| **Biometric truth first** | Every score traces to ridge data; no fabricated palm-only metrics (e.g. ATD). |
| **Interpretation second** | DMIT + Gardner MI + extensions applied only after capacity normalization. |
| **Premium experience** | Editorial typography, orbital visuals, glass UI, purposeful motion. |
| **Multi-tenant readiness** | Same product serves solo users, clinics, and institutions. |
| **Explainability** | Tooltips, glossary, “why this score,” counselor notes, audit trail. |

---

## 2. Audience A — Individual at Home

### Goals
- Self-service: upload 10 prints → understand profile without a counselor.
- Trust through education, not hype.
- Shareable, beautiful results.

### Features

| Feature | Status | Notes |
|---------|--------|-------|
| Guided 10-finger upload with hand map | ✅ Partial | Upload grid exists; enhance ritual animation |
| Purpose selector (self / child / career) | ✅ Frontend | Stored in session `notes` |
| Plain-English results summary | 🔲 Planned | Top 5 strengths + growth areas |
| Intelligence hover tooltips | ✅ Done | 9 cards with DMIT paragraphs |
| Learning tips per intelligence | ✅ Data | In `dmit-knowledge.ts`; surface in UI |
| Career suggestions per MI | ✅ Data | In profiles; expand |
| Mobile camera capture + alignment overlay | 🔲 Phase 3 | PWA |
| Quality gate (“too blurry”) | 🔲 Phase 2 | Needs backend quality API |
| Share read-only link | 🔲 Phase 2 | Token URL + public view |
| Download PDF | ✅ Done | From results page |
| `/solutions` individual path | ✅ Done | Persona landing |
| Parent mode (simplified copy) | 🔲 Phase 2 | Toggle on results |
| Email results to self | 🔲 Phase 3 | |

### User journey
```
Landing → Solutions (Individual) → New Analysis → Upload 10 → Processing → 
Results narrative → Finger drill-down → PDF → Share (future)
```

---

## 3. Audience B — Counselor / Clinic

### Goals
- Manage many clients; repeat assessments; branded delivery.
- Notes + context per session; operational efficiency.

### Features

| Feature | Status | Notes |
|---------|--------|-------|
| Session archive with search/filter | ✅ Partial | Sessions page; add filters |
| Client name, age, purpose on create | ✅ Done | Form fields |
| Counselor notes field | 🔲 Phase 2 | `notes` exists; dedicated UI |
| Session status lifecycle | ✅ API | pending → completed |
| Delete session | ✅ Done | |
| Compare two clients | ✅ Frontend | `/compare` page |
| Extension explorer (40+) | ✅ Done | `/extensions` |
| White-label PDF (logo, clinic name) | 🔲 Phase 3 | Report generator config |
| Quick vs Full report tier | 🔲 Phase 3 | |
| Appointment queue / today’s list | 🔲 Phase 3 | Dashboard widget |
| Auth + counselor accounts | 🔲 Phase 2 | Multi-user |
| Persistent DB (Postgres) | 🔲 Phase 2 | Replace in-memory store |
| Thumbnail serving for prints | 🔲 Phase 2 | Static mount |
| Batch zip upload | 🔲 Phase 3 | |
| Export counselor summary PDF | 🔲 Phase 3 | Shorter than technical report |
| `/solutions` clinic path | ✅ Done | |

### User journey
```
Login (future) → Dashboard → New Client → Upload → Review results → 
Add notes → Compare with prior session → Export branded PDF → Archive
```

---

## 4. Audience C — School / Corporate Batch

### Goals
- Many subjects; aggregate insights; privacy-compliant; teacher/HR-facing views.

### Features

| Feature | Status | Notes |
|---------|--------|-------|
| Batch cohort concept | 🔲 Phase 3 | `cohort_id` on sessions |
| CSV import (name, id, age) | 🔲 Phase 3 | |
| Bulk upload folder per student | 🔲 Phase 3 | |
| Aggregate MI radar (class average) | 🔲 Phase 4 | Anonymized |
| Team map (5–20 profiles) | 🔲 Phase 4 | Corporate |
| Top strengths distribution chart | 🔲 Phase 4 | |
| Teacher dashboard (read-only) | 🔲 Phase 4 | Role-based |
| HR compatibility view (2 profiles) | 🔲 Partial | Compare page |
| GDPR / consent checkbox | 🔲 Phase 3 | On upload |
| Anonymized export | 🔲 Phase 4 | |
| `/solutions` institution path | ✅ Done | |

### User journey
```
Institution admin → Create cohort → Import roster → Bulk assign uploads → 
Run batch pipeline → Aggregate report → Export for leadership
```

---

## 5. Audience D — Showcase / Investors

### Goals
- Demonstrate technical depth, market size, and premium UX in minutes.
- Live pipeline demo; architecture credibility.

### Features

| Feature | Status | Notes |
|---------|--------|-------|
| Cinematic landing + orbital hero | ✅ Done | |
| Live system status page | ✅ Done | `/system` |
| Pipeline stage visualization | ✅ Done | Landing + tracker |
| Extension count (40+) | ✅ Done | `/extensions` |
| About + science narrative | ✅ Done | `/about` |
| Architecture doc link | ✅ Repo | `system_architecture.md` |
| Demo mode (sample session) | 🔲 Phase 2 | Pre-loaded result JSON |
| Investor one-pager export | 🔲 Phase 3 | PDF/markdown |
| `/solutions` partner path | ✅ Done | |
| Metrics: sessions, features, modules | ✅ Done | Landing stats |
| Video walkthrough embed | 🔲 Phase 3 | |
| Sandbox API playground | 🔲 Phase 4 | Swagger linked |

### Demo script (5 min)
1. Landing hero → orbital fingerprint field  
2. About → science + finger–lobe table  
3. New Analysis → upload (or demo session)  
4. Results → MI radar + extensions  
5. System → health + module count  
6. Extensions gallery → breadth  

---

## 6. Frontend Roadmap

### Routes

| Route | Purpose | Status |
|-------|---------|--------|
| `/` | Landing, pipeline, MI grid, sessions teaser | ✅ |
| `/about` | DMIT field + platform | ✅ |
| `/solutions` | Personas A/B/C/D | ✅ New |
| `/learn` | Glossary + finger encyclopedia | ✅ New |
| `/extensions` | 40+ extension catalog | ✅ New |
| `/compare` | Two-session comparison | ✅ New |
| `/analysis/new` | Upload workspace | ✅ |
| `/analysis/[id]` | Results | ✅ |
| `/analysis/[id]/finger/[finger]` | Finger detail | ✅ |
| `/sessions` | Archive | ✅ |
| `/system` | Health & stack | ✅ |
| `/settings` | Preferences | ✅ |
| `/cohorts` | Batch management | 🔲 Phase 3 |
| `/demo` | Investor sample data | 🔲 Phase 2 |
| `/share/[token]` | Public read-only report | 🔲 Phase 2 |

### Components (planned expansions)

| Component | Purpose |
|-----------|---------|
| `IntelligenceCard` | Hover DMIT knowledge | ✅ |
| `ExtensionCard` | Extension detail modal | ✅ |
| `FingerEncyclopedia` | L1–R5 pages | ✅ in `/learn` |
| `AudiencePathCard` | Solutions grid | ✅ |
| `CompareRadar` | Side-by-side MI | ✅ |
| `UploadRitual` | Hand silhouette progress | 🔲 |
| `ResultsNarrative` | Scroll-driven story | 🔲 |
| `CohortTable` | Batch roster | 🔲 |
| `ShareReportButton` | Copy link | 🔲 |
| `DemoSessionBanner` | Investor mode | 🔲 |

### Design system
- Serif display: Cormorant Garamond ✅  
- Accent: champagne gold / plum / sage ✅  
- Glass cards, magnetic buttons ✅  
- FingerprintField orbital background ✅  

---

## 7. Backend & Infrastructure Roadmap

| Item | Priority | Phase |
|------|----------|-------|
| SQLite → PostgreSQL sessions | P0 | 2 |
| Serve `/uploads` thumbnails | P0 | 2 |
| `purpose` enum on session | P1 | 2 |
| Durable job queue (Celery/Redis) | P1 | 2 |
| WebSocket progress | P2 | 3 |
| Auth (JWT / Clerk) | P1 | 2 |
| Roles: individual, counselor, admin, institution | P1 | 3 |
| Cohort + batch APIs | P2 | 3 |
| Share token generation | P2 | 2 |
| Quality score API per finger | P2 | 2 |
| Webhook on analysis complete | P3 | 4 |
| Stripe billing per report | P3 | 4 |

---

## 8. DMIT Content & Education Layer

| Content | Location | Status |
|---------|----------|--------|
| 9 intelligence profiles | `dmit-knowledge.ts` | ✅ |
| Finger–lobe table | `/about` | ✅ |
| Glossary (TFRC, delta, CADA…) | `/learn` | ✅ |
| Finger encyclopedia L1–R5 | `/learn` | ✅ |
| Extension catalog copy | `extensions-catalog.ts` | ✅ |
| Pattern type explainer | 🔲 `/learn` |
| “Why this score” per extension | 🔲 Results page |
| Parent-simplified language | 🔲 Toggle |
| DMIT history & embryology | ✅ `/about` |
| Limitations / honesty page | 🔲 Link from About |

---

## 9. Visualization & Reporting

| Visualization | Where | Status |
|---------------|-------|--------|
| MI radar chart | Results | ✅ |
| Brain lobe bar chart | Results | ✅ |
| Learning style pie | Results | ✅ |
| Extension grid | Results | ✅ |
| Pipeline tracker | Results / upload | ✅ |
| Brain lobe diagram | Component exists | ✅ |
| Intelligence web | Component exists | ✅ |
| 3D PDF report | Backend | ✅ |
| Compare MI bars | `/compare` | ✅ |
| Team aggregate radar | 🔲 Cohort |
| Ridge overlay on image | 🔲 Finger detail |
| Singular points on print | 🔲 Finger detail |
| Scroll narrative results | 🔲 Phase 2 |

---

## 10. Phased Delivery Plan

### Phase 1 — Foundation (current) ✅
- FastAPI + Next.js cinematic UI  
- Sessions, upload, analysis, PDF  
- About, intelligence tooltips, premium palette  
- Solutions, Learn, Extensions, Compare pages  

### Phase 2 — Production readiness (4–6 weeks)
- PostgreSQL + thumbnails  
- Auth + counselor accounts  
- Session purpose field (API)  
- Demo session for investors  
- Share read-only links  
- Results plain-English summary  
- “Why this score” on extensions  
- Upload quality warnings  

### Phase 3 — Clinic & institution (6–10 weeks)
- White-label PDF  
- Cohort + batch upload  
- Counselor dashboard widgets  
- Mobile PWA capture  
- Parent mode copy  
- Email delivery  

### Phase 4 — Scale & intelligence (10–16 weeks)
- Team/corporate aggregate dashboards  
- AI bounded Q&A on session JSON  
- Webhooks + billing  
- API marketplace / partner keys  
- Population norms (if data collected ethically)  

---

## 11. Success Metrics

| Audience | KPI |
|----------|-----|
| A Individual | Completion rate (10/10 uploads), time to first PDF |
| B Clinic | Sessions per counselor per week, repeat client rate |
| C Institution | Batch size, export downloads |
| D Showcase | Demo completion rate, partner meeting → pilot |

---

## Appendix A — Full Feature Backlog (Brainstorm)

### Experience
- [ ] Scroll-driven results narrative  
- [ ] Sound design (optional, off by default)  
- [ ] Light mode for print  
- [ ] Page transitions (ridge wipe)  
- [ ] Onboarding tour (first visit)  

### Analysis depth
- [ ] Ridge flow SVG overlay on fingerprint image  
- [ ] Core/delta markers on image  
- [ ] Left vs right thumb comparison panel  
- [ ] Pattern distribution (arch/loop/whorl) hand chart  
- [ ] Dominant hand narrative  
- [ ] Extension category filters on results  

### Social & sharing
- [ ] OG image card per session for WhatsApp  
- [ ] QR code on PDF → live results  
- [ ] Compare up to 4 sessions  

### AI (bounded)
- [ ] Plain-English summary from JSON only  
- [ ] Session Q&A with citations to fields  
- [ ] Counselor debrief question suggestions  

### Business
- [ ] Stripe per report  
- [ ] Clinic subscription tiers  
- [ ] Institution site license  

### Integrations
- [ ] Google Calendar booking  
- [ ] CRM webhook  
- [ ] Scanner watch-folder  

---

## Appendix B — Frontend File Map (New)

```
frontend/src/
  app/
    solutions/page.tsx      # Personas A/B/C/D
    learn/page.tsx          # Glossary + fingers
    extensions/page.tsx     # Extension gallery
    compare/page.tsx        # Two-session compare
  lib/
    extensions-catalog.ts
    dmit-glossary.ts
    audience-paths.ts
  components/
    solutions/AudiencePathCard.tsx
    compare/CompareView.tsx
    extensions/ExtensionCard.tsx
```

---

*Last updated: 2026-05-16 · Maintained alongside `memory-bank/progress.md` and `system_architecture.md`.*

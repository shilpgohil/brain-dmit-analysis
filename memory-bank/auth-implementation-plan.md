# Auth + Partner + QR System — Implementation Plan

_Created: Aug 22, 2026_

---

## Architecture decisions

1. **Keep existing `sqlite3` + session_store pattern** — don't touch what works. New tables (admins, partners, plans, features, etc.) are added to the same `data/sessions.db` using the same raw sqlite3 approach. Zero risk to existing pipeline.

2. **JWT with two scopes** — `partner` and `admin` are separate identity tables (Arogya pattern). One `security.py` module issues/verifies tokens for both. Access token in memory (Zustand), refresh token in httpOnly cookie.

3. **Password hashing** — `passlib[bcrypt]`. One new pip install alongside `python-jose[cryptography]`.

4. **Feature resolution** — three-layer cascade: `partner_feature_overrides` → `plan_features` → `features.default_value`. Computed once at login, returned by `/auth/me`.

5. **QR codes** — `qrcode` + `Pillow` (already installed). Report QR encodes `{public_url}/report/{public_token}/view`. Partner card QR encodes `{public_url}/partner/{slug}/intake`.

6. **Migrations** — plain SQL `CREATE TABLE IF NOT EXISTS` in `db/init.py` (same pattern as existing `persistence.py`). Run at app startup.

---

## File structure added

```
backend/api/
├── auth/
│   ├── __init__.py
│   ├── router.py          POST /auth/login|refresh|logout|me|change-password
│   ├── admin_router.py    POST /admin/auth/login|refresh|logout|me
│   ├── security.py        JWT issue/verify, bcrypt hash/verify
│   ├── dependencies.py    get_current_partner, get_current_admin FastAPI deps
│   └── schemas.py         LoginRequest, TokenResponse, MeResponse, FeatureMap
│
├── admin/
│   ├── __init__.py
│   ├── router.py          /admin/partners, /admin/plans, /admin/features, /admin/requests, /admin/settings
│   └── schemas.py
│
├── public/
│   ├── __init__.py
│   └── router.py          GET /public/report/{token}, GET /public/partner/{slug}/intake, POST /public/intake/{slug}
│
├── db/
│   ├── __init__.py
│   ├── connection.py      shared _connect() + single DB path constant
│   ├── init.py            CREATE TABLE IF NOT EXISTS for all auth tables
│   ├── admins.py          CRUD: get_by_email, get_by_id, update_password
│   ├── partners.py        CRUD: create, get_by_id, get_by_email, list_all, activate, deactivate
│   ├── features.py        CRUD: list_all, create, update, get_effective_features(partner_id)
│   ├── plans.py           CRUD: create_plan, add_plan_feature, list_plans, get_plan_features
│   ├── overrides.py       set_override, remove_override, list_partner_overrides
│   ├── reports.py         create_report_token, get_by_token, increment_view_count
│   └── intake.py          create_intake_request, list_for_partner, update_status
│
└── main.py                add new routers under /api prefix
```

```
frontend/src/
├── app/
│   ├── login/page.tsx                  email/password form
│   ├── request-access/page.tsx         public interest form → admin review
│   ├── admin/
│   │   ├── layout.tsx                  admin shell + nav
│   │   ├── page.tsx                    admin dashboard overview
│   │   ├── partners/
│   │   │   ├── page.tsx                list + search all partners
│   │   │   └── [id]/page.tsx          detail: edit, feature toggles, usage, sessions
│   │   ├── plans/
│   │   │   ├── page.tsx                list plans + create
│   │   │   └── [id]/page.tsx          edit plan features
│   │   ├── requests/page.tsx           pending interest requests → approve/reject
│   │   └── settings/page.tsx           platform card settings
│   └── partner/
│       └── [slug]/
│           └── intake/page.tsx         QR intake landing (public, no login)
│
├── lib/
│   └── auth-api.ts                     login, logout, me, refresh calls
│
├── store/
│   └── authStore.ts                    Zustand: user, features, token (in memory)
│
└── middleware.ts                       protect /analysis, /sessions, /admin routes
```

---

## Tables added to data/sessions.db

See `db/init.py` for full SQL. Summary:

| Table | Purpose |
|---|---|
| `admins` | Platform admin accounts |
| `partners` | Counsellor/centre accounts (admin-created only) |
| `plans` | Subscription bundles (admin-managed) |
| `features` | Feature catalog (keys, types, defaults) |
| `plan_features` | Which features belong to each plan + value |
| `partner_feature_overrides` | Per-partner exceptions (trial, upgrades, restrictions) |
| `session_reports` | Report generation log + public_token for QR |
| `intake_requests` | Leads from partner QR card scans |
| `partner_requests` | Public interest form submissions |
| `refresh_tokens` | httpOnly refresh token registry (for revocation) |
| `audit_logs` | Who changed what (features, partners, plans) |

Plus: `sessions` table gets `partner_id` column added via `ALTER TABLE IF NOT EXISTS` + index.

---

## Phase execution order

### Phase 1 — Install + DB init (30 min)
1. `pip install python-jose[cryptography] passlib[bcrypt] qrcode`
2. `backend/requirements.txt` updated
3. `db/connection.py` — shared SQLite helpers
4. `db/init.py` — all CREATE TABLE statements + ALTER for sessions.partner_id
5. Wire `init_db()` call into `api/main.py` startup
6. Seed one admin account (env var ADMIN_EMAIL + ADMIN_PASSWORD)

### Phase 2 — Auth backend (1 hour)
7. `auth/security.py` — JWT issue/verify, bcrypt
8. `db/admins.py`, `db/partners.py` — CRUD
9. `auth/dependencies.py` — get_current_partner, get_current_admin
10. `auth/router.py` — partner login/refresh/logout/me
11. `auth/admin_router.py` — admin login/refresh/logout/me
12. `/auth/me` returns full feature profile from `get_effective_features(partner_id)`
13. Add `Depends(get_current_partner)` to all existing routes in sessions.py + analysis.py
14. Filter sessions by `partner_id` (partners only see theirs; admin sees all)

### Phase 3 — Feature/plan backend (1 hour)
15. `db/features.py` — seed default feature catalog on init
16. `db/plans.py` — create/edit plans + plan_features
17. `db/overrides.py` — partner-specific overrides
18. `get_effective_features(partner_id)` — the three-layer resolution query
19. `admin/router.py` — CRUD for plans, features, partners, pending requests
20. Per-endpoint feature guards (decorator or dependency)

### Phase 4 — QR + public pages backend (45 min)
21. `db/reports.py` — create public_token on report generation, track views
22. Wire into PDF generator: embed QR in report PDF
23. `public/router.py` — GET /public/report/{token}, GET /public/partner/{slug}/intake
24. `db/intake.py` — POST /public/intake/{slug} creates lead

### Phase 5 — Frontend auth (45 min)
25. `store/authStore.ts` — Zustand: user, features, access token in memory
26. `lib/auth-api.ts` — login, logout, me, refresh with axios
27. `/login` page
28. `middleware.ts` — protect routes
29. Axios interceptor — attach Bearer + refresh on 401
30. `/request-access` public form

### Phase 6 — Admin frontend (2 hours)
31. Admin layout + nav
32. Admin dashboard (partner count, today's analyses, pending requests)
33. Partners list + create partner modal
34. Partner detail: feature flag toggles (per-feature on/off/value)
35. Plans list + create plan + edit plan features
36. Pending requests → Approve (creates partner) / Reject

### Phase 7 — Partner card + QR page (30 min)
37. `/partner/[slug]/intake` public page (no login, branded)
38. Partner dashboard shows "Your QR Card" — downloadable PNG/PDF
39. QR code preview in partner profile settings

---

## Backwards compatibility

- All existing API routes continue to work without a token until Phase 2 Step 13 adds the dependency. This means the running servers keep working during development.
- When the dependency IS added, the frontend gains the login screen before anything breaks.
- The `session_store` dict-based approach is untouched. New auth tables are purely additive.

---

## Packages to install

```bash
pip install "python-jose[cryptography]" "passlib[bcrypt]" qrcode
```

`qrcode` already pulls `pillow` which is already installed.

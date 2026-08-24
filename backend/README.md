---
title: DMIT Analysis API
emoji: 🧠
colorFrom: yellow
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# DMIT Analysis Platform — Backend API

FastAPI backend for the DMIT (Dermatoglyphics Multiple Intelligence Test)
platform: fingerprint feature extraction, brain-lobe intelligence mapping,
46 extension analyses, 10-quotient scoring, premium PDF report generation,
and an AI counselling consultant.

## Architecture

| Layer | Service |
|---|---|
| Compute (this Space) | FastAPI + OpenCV + SciPy pipeline |
| Database | Neon PostgreSQL (external) |
| File storage | Backblaze B2 (external, S3-compatible) |
| Frontend | Next.js on Vercel |

The Space is stateless — all durable data lives in Neon and B2, so restarts
and rebuilds are safe.

## Required environment secrets

Set these in *Settings → Variables and secrets* of this Space:

- `DATABASE_URL` — Neon pooled connection string
- `STORAGE_ENDPOINT`, `R2_ACCESS_KEY`, `R2_SECRET_KEY`, `R2_BUCKET` — B2 credentials
- `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `JWT_SECRET` — auth bootstrap
- `GROQ_API_KEY`, `NVIDIA_API_KEY`, `NVIDIA_EMBED_KEY` — AI providers
- `CORS_ORIGINS` — the Vercel frontend URL
- `ENVIRONMENT` — `production`

Health check: `GET /api/health` · Storage check: `GET /api/health/storage`

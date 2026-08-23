"""
DMIT Platform — FastAPI Backend
================================
Wraps the Python DMIT pipeline with a REST API for the Next.js frontend.
"""
from __future__ import annotations
import sys
from pathlib import Path

# Ensure the root project is on the path
sys.path.insert(0, str(Path(__file__).parents[1]))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os

from api.routes import sessions as sessions_router
from api.routes import analysis as analysis_router
from api.schemas import SystemStatus
from api.store import init_store

# Auth / admin / public routers
from api.auth.router import router as auth_router
from api.auth.admin_router import router as admin_auth_router
from api.admin.router import router as admin_router
from api.public.router import router as public_router

# ── DB init: sessions table first, then auth tables ──────────────────────
init_store()

from api.db.init import init_auth_db
from api.db.features import seed_features_and_plans

init_auth_db()
seed_features_and_plans()

# Chat DB for AI Consultant
from api.ai_consultant.db import init_chat_db
init_chat_db()

# ── Seed admin from env if none exists ────────────────────────────────────
_admin_email    = os.getenv("ADMIN_EMAIL",    "admin@dmit.local")
_admin_password = os.getenv("ADMIN_PASSWORD", "changeme123")
_admin_name     = os.getenv("ADMIN_NAME",     "Platform Admin")

from api.db.admins import create_admin, get_admin_by_email
from api.auth.security import hash_password as _hp

if not get_admin_by_email(_admin_email):
    create_admin(_admin_email, _hp(_admin_password), _admin_name)
    import logging as _log
    _log.getLogger(__name__).info(f"Admin seeded: {_admin_email}")

# ---------------------------------------------------------------------------
# Pre-import heavy pipeline modules at startup so health checks are instant.
# Python caches modules after first import — subsequent calls cost nothing.
# ---------------------------------------------------------------------------
_components: dict = {}

def _warm_imports():
    try:
        from optimized_feature_extractor_clean import OptimizedFeatureExtractor  # noqa: F401
        _components["feature_extractor"] = True
    except Exception:
        _components["feature_extractor"] = False
    try:
        from dmit_intelligence_mapper import map_features_to_dmit_profile  # noqa: F401
        _components["intelligence_mapper"] = True
    except Exception:
        _components["intelligence_mapper"] = False
    try:
        from dmit_extensions.engine import DMITExtensionsEngine  # noqa: F401
        _components["extensions_engine"] = True
    except Exception:
        _components["extensions_engine"] = False
    try:
        from premium_pdf_report import PremiumReportGenerator  # noqa: F401
        _components["pdf_generator"] = True
    except Exception:
        _components["pdf_generator"] = False

_warm_imports()

_cors_origins = [
    o.strip()
    for o in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:3001,http://127.0.0.1:3001",
    ).split(",")
    if o.strip()
]
# Allow any localhost port when Next.js picks 3001, 3002, etc.
_cors_origin_regex = os.getenv(
    "CORS_ORIGIN_REGEX",
    r"http://(localhost|127\.0\.0\.1):\d+",
)
app = FastAPI(
    title="DMIT Analysis Platform API",
    description="Dermatoglyphics Multiple Intelligence Test — scientific biometric analysis pipeline",
    version="3.2",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_origin_regex=_cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Thread-Id", "Content-Type"],
)

# Static files for uploads/outputs — only mount when NOT using R2 (local dev).
# On Render / production the filesystem is ephemeral, so we serve files from R2.
from api import storage as _storage
if not _storage.ENABLED:
    uploads_path = Path("uploads")
    uploads_path.mkdir(exist_ok=True)
    output_path = Path("output")
    output_path.mkdir(exist_ok=True)
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
    app.mount("/output", StaticFiles(directory="output"), name="output")
else:
    # Still create dirs so the pipeline can write temp files during a request
    Path("uploads").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

app.include_router(sessions_router.router, prefix="/api")
app.include_router(analysis_router.router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(admin_auth_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(public_router, prefix="/api")

# AI Consultant
from api.ai_consultant.router import router as ai_consultant_router
app.include_router(ai_consultant_router, prefix="/api")


@app.get("/api/health", response_model=SystemStatus)
async def health_check():
    from api.store import session_store
    all_ok = all(_components.values()) if _components else False
    return SystemStatus(
        status="operational" if all_ok else "degraded",
        pipeline_version="3.2-Scientific-Full",
        components=_components,
        total_sessions=len(session_store),
        processing_queue=sum(
            1 for s in session_store.values()
            if s.get("status") in ("preprocessing", "extracting", "mapping", "extending", "generating_report")
        ),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8001, reload=True)

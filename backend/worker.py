"""
DMIT Analysis Worker — dedicated pipeline-execution service.

Runs on its own Render instance (second free account) so the heavy
OpenCV + SciPy + extensions memory footprint never competes with the
main API. Shares Neon PostgreSQL and Backblaze B2 with the main API.

Division of labour:
  • This worker : image download from B2 → feature extraction →
                  intelligence mapping → 46 extensions → quotients →
                  persists results + raw output to Neon
  • Main API    : everything else, including PDF generation (matplotlib +
                  reportlab stay OFF this instance to fit 512 MB)

Start command:  uvicorn worker:app --host 0.0.0.0 --port $PORT

Required env:   DATABASE_URL, WORKER_SECRET,
                STORAGE_ENDPOINT / R2_ACCESS_KEY / R2_SECRET_KEY / R2_BUCKET
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

# Ensure the backend root is importable (worker.py lives at backend/)
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")

WORKER_SECRET = os.environ.get("WORKER_SECRET", "")

app = FastAPI(
    title="DMIT Analysis Worker",
    docs_url=None, redoc_url=None, openapi_url=None,  # not a public API
)


class AnalyzeJob(BaseModel):
    session_id: str
    use_preprocessing: bool = False
    generate_pdf: bool = True


@app.get("/health")
async def health():
    """Lightweight liveness probe (also used by the keep-alive pinger)."""
    return {"status": "worker-alive"}


@app.post("/internal/analyze")
async def analyze(
    job: AnalyzeJob,
    background_tasks: BackgroundTasks,
    x_worker_secret: str = Header(default=""),
):
    if not WORKER_SECRET or x_worker_secret != WORKER_SECRET:
        raise HTTPException(status_code=403, detail="Invalid worker secret")

    # Load this session from the shared database into this process's store.
    from api.persistence import load_session
    from api.store import session_store

    session = load_session(job.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found in database")
    session_store[job.session_id] = session

    background_tasks.add_task(_run_job, job)
    return {"accepted": job.session_id}


def _run_job(job: AnalyzeJob) -> None:
    """
    Execute the full analysis pipeline INCLUDING PDF generation in this process.

    Architecture rationale: the worker runs on a dedicated free-tier instance
    with its own 750 h/month. After fingerprint analysis completes, the large
    OpenCV/numpy arrays are garbage-collected. matplotlib+reportlab are already
    resident from the pipeline's chart code. At PDF time the worker's live
    footprint is ~250 MB, leaving ~260 MB headroom — enough for the 19-section
    premium report. The main API's 0.1-CPU shared instance cannot reliably
    render the report (OOM), so we no longer defer PDF to it.
    """
    from api.routes.analysis import _run_pipeline_sync

    try:
        _run_pipeline_sync(
            job.session_id,
            use_preprocessing=job.use_preprocessing,
            generate_pdf=job.generate_pdf,
            defer_pdf=False,   # worker generates the PDF itself
        )
    except Exception:
        logger.exception("Worker job failed for session %s", job.session_id)

# DMIT Analysis Platform — FastAPI backend
# Built for Hugging Face Spaces (Docker SDK) — also works on any Docker host.
#
# Key choices:
#  • python:3.12-slim — every dependency has pre-built wheels for 3.12
#    (avoids the Python 3.14 wheel/compilation issues we hit on Render)
#  • Runs as UID 1000 — required by HF Spaces for filesystem writes
#  • Listens on port 7860 — the HF Spaces default app port

FROM python:3.12-slim

# System libraries needed by opencv-python-headless and matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# HF Spaces requires the app to run as user with UID 1000
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=1

WORKDIR /app

# Install Python dependencies first (cached layer — rebuilds only when
# requirements.txt changes, not on every code change)
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the application code
COPY --chown=user . .

# Writable working directories (uploads/output are ephemeral; durable
# persistence lives in Neon PostgreSQL + Backblaze B2)
RUN mkdir -p uploads output data

EXPOSE 7860

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]

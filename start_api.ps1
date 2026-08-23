# DMIT Platform - Start FastAPI Backend
# Run from the project root: .\start_api.ps1
#
# PYTHONPATH points to backend/ so all Python packages (api, core,
# dmit_extensions, premium_pdf_report, etc.) resolve from there.
# Working directory stays at project root so relative paths like
# uploads/, output/, data/sessions.db continue to work correctly.

Write-Host "Starting DMIT Platform API..." -ForegroundColor Cyan
Write-Host "API docs: http://localhost:8001/api/docs" -ForegroundColor Gray

$env:PYTHONPATH = "$PSScriptRoot\backend"
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload

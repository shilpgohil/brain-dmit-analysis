# DMIT Platform - Start FastAPI Backend
# Run from the project root: .\start_api.ps1

Write-Host "Starting DMIT Platform API..." -ForegroundColor Cyan
Write-Host "API docs will be available at: http://localhost:8001/api/docs" -ForegroundColor Gray
Write-Host "(Port 8001 avoids conflict if another app uses 8000)" -ForegroundColor Gray

.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload

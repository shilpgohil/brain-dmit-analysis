# DMIT Platform - Start Next.js Frontend
# Run from the project root: .\start_frontend.ps1

Write-Host "Starting DMIT Platform Frontend..." -ForegroundColor Cyan
Write-Host "App will be available at: http://localhost:3000" -ForegroundColor Gray

Set-Location frontend
npm run dev

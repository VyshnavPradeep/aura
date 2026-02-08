# AURA - Start Everything Script
# Starts both backend and frontend in separate windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AURA - Starting Full Stack" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$rootDir = $PSScriptRoot

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Cyan
Write-Host ""

# Start Backend in new window
Write-Host "Starting Backend (Terminal 1)..." -ForegroundColor Yellow
$backendScript = @"
Write-Host 'AURA Backend Server' -ForegroundColor Cyan
Write-Host '===================' -ForegroundColor Cyan
Write-Host ''
Set-Location '$rootDir'
if (Test-Path 'venv\Scripts\Activate.ps1') {
    .\venv\Scripts\Activate.ps1
}
uvicorn main:app --host 0.0.0.0 --port 8000
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

Write-Host "✓ Backend starting in new window..." -ForegroundColor Green
Start-Sleep -Seconds 3

# Start Frontend in new window
Write-Host "Starting Frontend (Terminal 2)..." -ForegroundColor Yellow
$frontendScript = @"
Write-Host 'AURA Frontend Application' -ForegroundColor Cyan
Write-Host '=========================' -ForegroundColor Cyan
Write-Host ''
Set-Location '$rootDir\frontend'
npm run dev
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host "✓ Frontend starting in new window..." -ForegroundColor Green
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   AURA is starting up!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services:" -ForegroundColor Cyan
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Wait 10-15 seconds for both services to start," -ForegroundColor Yellow
Write-Host "then open http://localhost:3000 in your browser" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host "✓ Frontend starting in new window..." -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Both services are starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Two new windows have been opened:" -ForegroundColor Cyan
Write-Host "  1. Backend  (http://localhost:8000)" -ForegroundColor White
Write-Host "  2. Frontend (http://localhost:3000)" -ForegroundColor White
Write-Host ""
Write-Host "Wait 10-15 seconds, then open:" -ForegroundColor Yellow
Write-Host "  http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Documentation available at:" -ForegroundColor Yellow
Write-Host "  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

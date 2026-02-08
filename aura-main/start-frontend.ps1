# AURA Frontend - Quick Start Script
# This script helps you get the frontend up and running quickly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AURA Frontend - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found! Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Navigate to frontend directory
$frontendDir = Join-Path $PSScriptRoot "frontend"
if (-not (Test-Path $frontendDir)) {
    Write-Host "✗ Frontend directory not found at: $frontendDir" -ForegroundColor Red
    exit 1
}

Set-Location $frontendDir
Write-Host "✓ Navigated to frontend directory" -ForegroundColor Green
Write-Host ""

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✓ Dependencies already installed" -ForegroundColor Green
}

Write-Host ""

# Check if backend is running
Write-Host "Checking if backend is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 3
    Write-Host "✓ Backend is running at http://localhost:8000" -ForegroundColor Green
} catch {
    Write-Host "⚠ Backend not detected at http://localhost:8000" -ForegroundColor Yellow
    Write-Host "  Please start the backend first:" -ForegroundColor Yellow
    Write-Host "  1. Open a new terminal" -ForegroundColor Yellow
    Write-Host "  2. cd to the root directory" -ForegroundColor Yellow
    Write-Host "  3. Run: uvicorn main:app --host 0.0.0.0 --port 8000" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 0
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting AURA Frontend..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The application will be available at:" -ForegroundColor Green
Write-Host "http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the development server
npm run dev

# Aura - Gemini 3 Quick Setup Script
# Run this script to set up your environment quickly

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "🚀 Aura - Gemini 3 API Setup" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not activated" -ForegroundColor Yellow
    Write-Host "💡 Activating virtual environment..." -ForegroundColor Cyan
    
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & "venv\Scripts\Activate.ps1"
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    } else {
        Write-Host "❌ Virtual environment not found. Creating..." -ForegroundColor Red
        python -m venv venv
        & "venv\Scripts\Activate.ps1"
        Write-Host "✅ Virtual environment created and activated" -ForegroundColor Green
    }
} else {
    Write-Host "✅ Virtual environment already activated" -ForegroundColor Green
}

Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "📁 Creating .env file from template..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit .env file and add your Gemini API key!" -ForegroundColor Yellow
    Write-Host "   Get your free key at: https://aistudio.google.com/app/apikey" -ForegroundColor Cyan
    Write-Host ""
    
    # Ask user if they want to set the key now
    $setKeyNow = Read-Host "Do you have your Gemini API key ready? (y/n)"
    
    if ($setKeyNow -eq 'y') {
        $apiKey = Read-Host "Enter your Gemini API key"
        if ($apiKey) {
            # Update .env file
            (Get-Content ".env") -replace 'GEMINI_API_KEY=your_gemini_api_key_here', "GEMINI_API_KEY=$apiKey" | Set-Content ".env"
            Write-Host "✅ API key saved to .env file" -ForegroundColor Green
            
            # Set environment variable for current session
            $env:GEMINI_API_KEY = $apiKey
            Write-Host "✅ API key set for current session" -ForegroundColor Green
        }
    } else {
        Write-Host "💡 You can edit .env file manually later" -ForegroundColor Cyan
    }
} else {
    Write-Host "✅ .env file exists" -ForegroundColor Green
    
    # Check if API key is set
    $envContent = Get-Content ".env" | Select-String "GEMINI_API_KEY="
    if ($envContent -match "your_gemini_api_key_here") {
        Write-Host "⚠️  Gemini API key not configured in .env" -ForegroundColor Yellow
        Write-Host "   Edit .env and replace 'your_gemini_api_key_here' with your actual key" -ForegroundColor Cyan
    }
}

Write-Host ""

# Install/Update dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
pip install --upgrade google-generativeai | Out-Null
pip install -q -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some dependencies may have issues" -ForegroundColor Yellow
}

Write-Host ""

# Load .env for current session
if (Test-Path ".env") {
    Write-Host "🔧 Loading environment variables..." -ForegroundColor Cyan
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            if ($key -and -not $key.StartsWith('#')) {
                Set-Item -Path "env:$key" -Value $value
            }
        }
    }
    Write-Host "✅ Environment variables loaded" -ForegroundColor Green
}

Write-Host ""

# Test Gemini connection (optional)
$testConnection = Read-Host "Test Gemini API connection now? (y/n)"

if ($testConnection -eq 'y') {
    Write-Host ""
    Write-Host "🧪 Testing Gemini integration..." -ForegroundColor Cyan
    Write-Host ""
    
    python test_gemini_integration.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Gemini integration test passed!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "⚠️  Test failed. Check your API key and internet connection" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Start server:  uvicorn main:app --reload" -ForegroundColor White
Write-Host "   2. Open docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "   3. Upload code:   POST to /upload/" -ForegroundColor White
Write-Host "   4. Run analysis:  POST to /analyze/{project_id}" -ForegroundColor White
Write-Host ""
Write-Host "📖 Documentation:" -ForegroundColor Cyan
Write-Host "   • Setup Guide:    GEMINI_SETUP_GUIDE.md" -ForegroundColor White
Write-Host "   • Main README:    README.md" -ForegroundColor White
Write-Host "   • RAG Features:   README_ADVANCED_RAG.md" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Get API Key:     https://aistudio.google.com/app/apikey" -ForegroundColor Cyan
Write-Host ""

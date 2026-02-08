# 🚀 AURA - Quick Command Reference

Quick reference for all common commands.

## 🎯 Quick Start

### Option 1: Start Everything (Recommended)
```powershell
.\start-all.ps1
```
Opens two terminals with backend and frontend running.

### Option 2: Manual Start

**Terminal 1 - Backend:**
```powershell
cd d:\aura-main\aura-main
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd d:\aura-main\aura-main\frontend
npm run dev
```

## 📦 Installation Commands

### First Time Setup

**Backend:**
```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Setup Gemini API key
.\setup_gemini.ps1
```

**Frontend:**
```powershell
cd frontend
npm install
```

## 🔧 Development Commands

### Backend

```powershell
# Start server
uvicorn main:app --host 0.0.0.0 --port 8000

# Start with auto-reload
uvicorn main:app --reload

# Run tests
pytest

# Check Python version
python --version

# List installed packages
pip list

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Frontend

```powershell
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Check Node version
node --version

# List dependencies
npm list

# Update dependencies
npm update
```

## 🧪 Testing Commands

### Backend Testing

```powershell
# Test server health
curl http://localhost:8000/

# Upload test file
python upload_and_test.py

# Run specific test
pytest test_backend.py

# Create test ZIP
Compress-Archive -Path "demo_code\*" -DestinationPath "test.zip" -Force
```

### Frontend Testing

```powershell
# Check if frontend is accessible
curl http://localhost:3000/

# Open in browser
start http://localhost:3000

# View API docs
start http://localhost:8000/docs
```

## 📝 File Management

### Backend

```powershell
# List uploaded projects
curl http://localhost:8000/upload/projects

# Delete project
curl -X DELETE http://localhost:8000/upload/projects/PROJECT_ID

# View extracted files
ls extracted/
```

### Frontend

```powershell
# Clean build artifacts
rm -rf .next

# Clean dependencies
rm -rf node_modules

# Clean everything and reinstall
rm -rf .next node_modules package-lock.json
npm install
```

## 🌐 API Testing

### Using curl

```powershell
# Health check
curl http://localhost:8000/

# Upload file
curl -X POST "http://localhost:8000/upload/" -F "file=@code.zip"

# Run analysis
curl -X POST "http://localhost:8000/analyze/PROJECT_ID"

# Get results
curl http://localhost:8000/analyze/PROJECT_ID/results

# RAG search
curl -X POST "http://localhost:8000/rag/search" -H "Content-Type: application/json" -d '{\"query\":\"SQL queries\",\"project_id\":\"PROJECT_ID\"}'
```

### Using PowerShell

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get

# Upload file
$file = Get-Item "code.zip"
$form = @{file = $file}
Invoke-RestMethod -Uri "http://localhost:8000/upload/" -Method Post -Form $form

# Run analysis
Invoke-RestMethod -Uri "http://localhost:8000/analyze/PROJECT_ID" -Method Post
```

## 🐛 Debugging Commands

### Backend

```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process on port 8000
# (Get PID from netstat, then:)
taskkill /PID <PID> /F

# View logs
# (Backend logs to console by default)

# Test Gemini API
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('OK')"
```

### Frontend

```powershell
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Kill process on port 3000
taskkill /PID <PID> /F

# Check for errors
# Open browser DevTools (F12) → Console tab

# View Next.js build errors
npm run build

# Clear Next.js cache
rm -rf .next
```

## 📊 Monitoring Commands

### Check Services

```powershell
# Check backend
curl http://localhost:8000/

# Check frontend
curl http://localhost:3000/

# View API docs
start http://localhost:8000/docs

# View frontend
start http://localhost:3000
```

### System Resources

```powershell
# Check Python processes
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Check Node processes
Get-Process | Where-Object {$_.ProcessName -like "*node*"}

# Check memory usage
Get-Process python,node | Select-Object Name,CPU,WS
```

## 🔄 Update Commands

### Update Backend

```powershell
# Pull latest code
git pull

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart server
# Ctrl+C to stop, then:
uvicorn main:app --reload
```

### Update Frontend

```powershell
cd frontend

# Pull latest code
git pull

# Update dependencies
npm update

# Rebuild
npm run build

# Restart
npm run dev
```

## 🗑️ Cleanup Commands

### Full Cleanup

```powershell
# Backend cleanup
rm -rf venv, uploads, extracted, reports, rag/indices
rm *.pyc, __pycache__

# Frontend cleanup
cd frontend
rm -rf .next, node_modules, package-lock.json

# Reinstall everything
cd ..
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt

cd frontend
npm install
```

### Partial Cleanup

```powershell
# Clear uploaded projects only
rm -rf uploads, extracted, reports

# Clear RAG indices
rm -rf rag/indices

# Clear frontend cache
cd frontend
rm -rf .next
```

## 📦 Deployment Commands

### Production Build

**Backend:**
```powershell
# No build needed, just configure
$env:DEBUG="False"
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```powershell
cd frontend
npm run build
npm start
```

### Docker

```bash
# Build backend
docker build -t aura-backend .

# Build frontend
docker build -t aura-frontend ./frontend

# Run with docker-compose
docker-compose up
```

## 🔐 Environment Commands

### Backend Environment

```powershell
# Activate venv
.\venv\Scripts\Activate

# Deactivate venv
deactivate

# Check Python in venv
python --version

# Check installed packages
pip list

# Export requirements
pip freeze > requirements.txt
```

### Frontend Environment

```powershell
# Check environment variables
Get-Content .env.local

# Set environment variable (temporary)
$env:NEXT_PUBLIC_API_URL="http://localhost:8000"

# Check Node environment
node -e "console.log(process.env)"
```

## 📚 Documentation Commands

### View Documentation

```powershell
# Open API docs in browser
start http://localhost:8000/docs

# View frontend README
code frontend\README.md

# View setup guide
code FRONTEND_SETUP.md

# View complete implementation
code FRONTEND_IMPLEMENTATION_COMPLETE.md
```

## 🎓 Learning Commands

### Explore Codebase

```powershell
# View project structure
tree /F

# Count lines of code
Get-ChildItem -Recurse -Include *.py,*.ts,*.tsx | Get-Content | Measure-Object -Line

# Find specific code
Get-ChildItem -Recurse -Include *.py | Select-String "def analyze"

# View git history
git log --oneline
```

## 💡 Useful Shortcuts

```powershell
# Alias for starting backend
function Start-Backend { uvicorn main:app --reload }

# Alias for starting frontend
function Start-Frontend { cd frontend; npm run dev }

# Add to PowerShell profile:
notepad $PROFILE

# Then add:
# Set-Location "d:\aura-main\aura-main"
# function sb { uvicorn main:app --reload }
# function sf { cd frontend; npm run dev }
```

---

## 📞 Quick Help

| Need | Command |
|------|---------|
| Start everything | `.\start-all.ps1` |
| Backend only | `uvicorn main:app --reload` |
| Frontend only | `cd frontend; npm run dev` |
| View API docs | `start http://localhost:8000/docs` |
| View frontend | `start http://localhost:3000` |
| Test backend | `curl http://localhost:8000/` |
| Test frontend | `curl http://localhost:3000/` |
| Clean build | `rm -rf .next; npm run build` |
| Reinstall | `rm -rf node_modules; npm install` |

---

**Keep this file handy for quick reference! 📌**

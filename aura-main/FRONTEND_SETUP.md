# AURA - Complete Setup Guide (Frontend + Backend)

Complete guide to set up and run the AURA code analysis platform with both frontend and backend.

## 📋 Prerequisites

### Required Software
- **Python 3.9+** (for backend)
- **Node.js 18+** (for frontend)
- **Git** (optional)

### API Keys
- **Google Gemini API Key** (Free): [Get it here](https://aistudio.google.com/app/apikey)

## 🚀 Part 1: Backend Setup

### Step 1: Navigate to Backend Directory

```powershell
cd d:\aura-main\aura-main
```

### Step 2: Set Up Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create a `.env` file in the root directory:

```env
# Gemini API Key (REQUIRED)
GEMINI_API_KEY=your_api_key_here

# Application Settings
APP_NAME=Aura - Advanced RAG System
APP_VERSION=2.0.0
DEBUG=False
HOST=0.0.0.0
PORT=8000

# Directories
UPLOAD_DIR=uploads
EXTRACTED_DIR=extracted
REPORTS_DIR=reports

# RAG Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RAG_INDEX_DIR=rag/indices
```

Or use the automated setup script:

```powershell
.\setup_gemini.ps1
```

### Step 4: Test Backend

```powershell
# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000

# In another terminal, test it
curl http://localhost:8000/
```

You should see:
```json
{
  "status": "aura is running",
  "version": "2.0.0"
}
```

## 🎨 Part 2: Frontend Setup

### Step 1: Navigate to Frontend Directory

```powershell
# Open a NEW terminal (keep backend running)
cd d:\aura-main\aura-main\frontend
```

### Step 2: Install Dependencies

```powershell
npm install
```

This will install:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios
- React Dropzone
- React Syntax Highlighter
- Lucide React Icons

### Step 3: Configure Environment

The `.env.local` file is already created with:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If you need to change the backend URL, edit this file.

### Step 4: Start Frontend Development Server

```powershell
npm run dev
```

The frontend will be available at: **http://localhost:3000**

## ✅ Verification

### Backend (Terminal 1)
```powershell
# Should show:
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Frontend (Terminal 2)
```powershell
# Should show:
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

### Browser Test

Open **http://localhost:3000** and you should see:
- AURA home page with gradient background
- "Upload Code" and "View Projects" buttons
- Four agent feature cards

## 🎯 Quick Test Workflow

### 1. Upload Test Code

```powershell
# In backend directory, compress demo code
Compress-Archive -Path "demo_code\*" -DestinationPath "demo_code.zip" -Force
```

### 2. Use the Web Interface

1. Open **http://localhost:3000**
2. Click **"Upload Code"**
3. Drag & drop `demo_code.zip`
4. Wait for processing (shows file count, language, framework)
5. Click **"Start Analysis"**
6. View comprehensive findings from 4 AI agents
7. Filter, search, and view code snippets

### 3. Try RAG Search

1. From the dashboard, click **"RAG Search"**
2. Enter: "Find SQL injection vulnerabilities"
3. Select strategy: "Multi-Query"
4. Click **"Search Code"**
5. View relevant code snippets with context

## 📁 Project Structure

```
aura-main/
├── main.py                 # Backend entry point
├── config.py              # Backend configuration
├── requirements.txt       # Python dependencies
├── .env                   # Backend environment variables
├── agents/                # AI analysis agents
├── app/                   # Backend routes
├── rag/                   # RAG system
├── utils/                 # Utilities
└── frontend/              # Frontend application
    ├── app/              # Next.js pages
    ├── components/       # React components
    ├── services/         # API client
    ├── types/            # TypeScript types
    └── package.json      # Node dependencies
```

## 🔧 Common Issues & Solutions

### Issue: Backend won't start

**Solution:**
```powershell
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check if port 8000 is in use
netstat -ano | findstr :8000
```

### Issue: Frontend won't start

**Solution:**
```powershell
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json .next
npm install

# Try different port
$env:PORT=3001; npm run dev
```

### Issue: "Cannot connect to backend"

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/`
2. Check `.env.local` has correct URL
3. Restart both backend and frontend

### Issue: "Gemini API error"

**Solution:**
1. Verify your API key in `.env`
2. Check you haven't exceeded free tier limits
3. Get new key: https://aistudio.google.com/app/apikey

## 🌐 Deployment

### Backend Deployment

```powershell
# Build with Docker
docker build -t aura-backend .
docker run -p 8000:8000 --env-file .env aura-backend
```

### Frontend Deployment

```powershell
# Build for production
npm run build

# Deploy to Vercel
npm install -g vercel
vercel

# Or deploy to Netlify
netlify deploy --prod
```

## 🎓 Usage Guide

### 1. Upload Code
- Prepare your backend code as a ZIP file
- Supports: Python, JavaScript, TypeScript, Java, Go
- Maximum size: 50MB
- Click "Upload Code" and drag & drop

### 2. Run Analysis
- After upload, click "Start Analysis"
- 4 AI agents run in parallel:
  - **Security Agent**: Finds vulnerabilities
  - **Test Generator**: Creates test cases
  - **Scalability Agent**: Identifies bottlenecks
  - **Database Agent**: Optimizes queries
- Wait 10-30 seconds for results

### 3. View Findings
- Filter by severity: Critical, High, Medium, Low
- Search by keyword
- Click "View Code" to see snippets
- Expand rows for detailed recommendations

### 4. Search Code (RAG)
- Click "RAG Search" from dashboard
- Enter natural language query
- Choose search strategy
- Get semantically relevant code snippets

### 5. Export Results
- Click "Export JSON" to download findings
- Share with team or integrate into CI/CD

## 📊 System Requirements

### Minimum
- CPU: 2 cores
- RAM: 4GB
- Disk: 2GB free space

### Recommended
- CPU: 4+ cores
- RAM: 8GB+
- Disk: 10GB+ free space

## 🔐 Security Notes

- **No authentication** by default (local use)
- **Add auth** before public deployment
- **API keys** stored in `.env` (never commit!)
- **CORS** configured for localhost only

## 📞 Support

### Documentation
- Backend API: http://localhost:8000/docs
- Frontend README: `frontend/README.md`
- Backend Guide: `HOW_TO_USE.md`

### Troubleshooting
1. Check both terminals for errors
2. Review browser console (F12)
3. Test backend API directly
4. Clear cache and restart

## 🎉 Next Steps

Once everything is running:

1. **Test with demo code** (included in `demo_code/`)
2. **Upload your own code** and see what AURA finds
3. **Explore RAG search** with semantic queries
4. **Customize agents** in `agents/` directory
5. **Extend the UI** with new features

## 🚀 Production Checklist

Before deploying to production:

- [ ] Set `DEBUG=False` in backend `.env`
- [ ] Add authentication middleware
- [ ] Configure CORS for your domain
- [ ] Set up HTTPS/SSL
- [ ] Configure rate limiting
- [ ] Set up monitoring/logging
- [ ] Add database for persistence
- [ ] Configure file upload limits
- [ ] Set up backups
- [ ] Test with production data

---

**AURA v2.0.0** - Autonomous Understanding and Review Agent
Powered by Google Gemini AI

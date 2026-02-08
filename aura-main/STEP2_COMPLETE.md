# Marathon Testing Agent - Step 2 Complete! 🎉

## ✅ What We Built

### 1. **ZIP Extraction Module** ([file_handler.py](utils/file_handler.py))
   - Safely extracts uploaded ZIP files
   - Prevents path traversal attacks
   - Analyzes file structure
   - Categorizes code files vs config files

### 2. **Language & Framework Detection** ([language_detector.py](utils/language_detector.py))
   - Detects: Python, JavaScript, TypeScript, Java, Go
   - Identifies frameworks: FastAPI, Django, Flask, Express, NestJS, Spring Boot, Gin, etc.
   - Extracts metadata (dependencies, versions)

### 3. **AST Parser** ([ast_parser.py](utils/ast_parser.py))
   - Parses Python code using built-in AST module
   - Pattern-based parsing for JS/TS, Java, Go
   - Extracts: Functions, Classes, Imports
   - Counts lines of code

### 4. **RAG System** ([code_embedder.py](rag/code_embedder.py))
   - Creates code chunks from parsed AST
   - Generates embeddings using sentence-transformers
   - Stores in FAISS vector index
   - Enables semantic code search

### 5. **Enhanced Upload Endpoint** ([uploads.py](app/routes/uploads.py))
   - Complete pipeline integration
   - Returns comprehensive analysis report
   - Includes project management endpoints

---

## 🧪 How to Test

### Method 1: Using PowerShell (Recommended)
```powershell
# Make sure test_backend.zip exists (we created it)
# If not, create it:
Compress-Archive -Path "test_app.py", "test_requirements.txt" -DestinationPath "test_backend.zip" -Force

# Upload the file
$file = Get-Item "test_backend.zip"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/upload/" -Method Post -Form @{file = $file} | ConvertTo-Json -Depth 10
```

### Method 2: Using curl (if installed)
```bash
curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@test_backend.zip"
```

### Method 3: Using VS Code REST Client
Open the API docs in your browser:
```
http://127.0.0.1:8000/docs
```
- Click on "POST /upload/"
- Click "Try it out"
- Upload test_backend.zip
- Execute

---

## 📊 Expected Response

```json
{
  "status": "success",
  "project_id": "20260120_123456_abc123",
  "filename": "test_backend.zip",
  "extraction": {
    "total_files": 2,
    "code_files": 1,
    "project_dir": "extracted/20260120_123456_abc123"
  },
  "detection": {
    "language": "python",
    "confidence": 0.85,
    "framework": "fastapi",
    "dependencies": 3
  },
  "parsing": {
    "files_parsed": 1,
    "total_functions": 3,
    "total_classes": 0,
    "total_lines": 17,
    "summary": {
      "avg_functions_per_file": 3.0,
      "avg_classes_per_file": 0.0,
      "avg_lines_per_file": 17.0
    }
  },
  "embeddings": {
    "chunks_created": 3,
    "index_created": true
  }
}
```

---

## 🚀 Next Steps (Step 3)

### Build the Micro-Agents:

1. **Security Agent** - Detect vulnerabilities using Semgrep + LLM
2. **Test Generator Agent** - Create automated test cases
3. **Scalability Agent** - Analyze performance bottlenecks
4. **DB Agent** - Analyze database queries and schema

### Integrate Gemini 3 API:
- Long-context analysis
- Multi-step reasoning
- Bug detection and fix suggestions

---

## 📂 Current Project Structure

```
aura/
├── main.py                    # FastAPI entry point
├── requirements.txt           # Dependencies
├── app/
│   └── routes/
│       └── uploads.py         # Upload endpoint with full pipeline
├── utils/
│   ├── file_handler.py        # ZIP extraction
│   ├── language_detector.py   # Language/framework detection
│   └── ast_parser.py          # Code parsing
├── rag/
│   └── code_embedder.py       # Embeddings + FAISS
├── uploads/                   # Uploaded ZIP files
├── extracted/                 # Extracted projects
└── rag/indices/               # FAISS vector indices
```

---

## 🔧 Troubleshooting

### Server not starting?
```powershell
cd "C:\Users\vyshnavpradeep\OneDrive\Desktop\aura\aura"
python -m uvicorn main:app --reload
```

### Missing dependencies?
```powershell
pip install -r requirements.txt
```

### Check server status:
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000 | Select-Object -ExpandProperty Content
```

Expected: `{"status":"aura is running"}`

---

## 📝 Test Commands Summary

```powershell
# 1. Test health endpoint
Invoke-WebRequest -Uri http://127.0.0.1:8000 | Select-Object -ExpandProperty Content

# 2. Upload and analyze code
$file = Get-Item "test_backend.zip"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/upload/" -Method Post -Form @{file = $file}

# 3. List all projects
Invoke-RestMethod -Uri "http://127.0.0.1:8000/upload/projects" -Method Get

# 4. Delete a project (replace PROJECT_ID)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/upload/projects/PROJECT_ID" -Method Delete
```

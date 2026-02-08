# 🚀 How to Upload and Test Code with Aura

## YES! You can upload code snippets and test them with the autonomous agent!

---

## Quick Start Guide

### Step 1: Start the Server

```powershell
# In your terminal, run:
cd C:\Users\vyshnavpradeep\OneDrive\Desktop\aura\aura
uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will start on **http://localhost:8000**

---

### Step 2: Prepare Your Code

Put your code files in a folder, for example:

```
my_code/
  ├── app.py
  ├── utils.py
  └── requirements.txt
```

**OR** use the demo code I created for you in `demo_code/` folder!

---

### Step 3: Upload Your Code

#### Option A: Using the Web Interface (Interactive API Docs)

1. Open your browser to: **http://localhost:8000/docs**
2. Find the **POST /upload/** endpoint
3. Click "Try it out"
4. Click "Choose File" and select your ZIP file
5. Click "Execute"

#### Option B: Using Python Script

```python
import requests
import zipfile
import os

# Create ZIP from your code folder
with zipfile.ZipFile('my_code.zip', 'w') as zipf:
    for root, dirs, files in os.walk('my_code'):
        for file in files:
            zipf.write(os.path.join(root, file))

# Upload to Aura
files = {'file': open('my_code.zip', 'rb')}
response = requests.post('http://localhost:8000/upload/', files=files)
result = response.json()

print(f"Project ID: {result['project_id']}")
```

#### Option C: Using PowerShell

```powershell
# Compress your code folder to ZIP
Compress-Archive -Path "demo_code\*" -DestinationPath "demo_code.zip" -Force

# Upload via curl (if installed)
curl -X POST "http://localhost:8000/upload/" -F "file=@demo_code.zip"
```

---

### Step 4: Run AI Analysis

Once uploaded, you'll get a `project_id`. Use it to run analysis:

#### Using the Web Interface:
1. Go to **http://localhost:8000/docs**
2. Find **POST /analyze/{project_id}**
3. Click "Try it out"
4. Enter your project_id
5. Click "Execute"

#### Using Python:
```python
project_id = "20260204_123456_abc123"  # From upload response
response = requests.post(f'http://localhost:8000/analyze/{project_id}')
results = response.json()

# View results
print("Security Issues:", len(results['security']['findings']))
print("Test Cases:", len(results['test_generator']['test_cases']))
print("Performance Issues:", len(results['scalability']['bottlenecks']))
print("Database Issues:", len(results['database']['issues']))
```

---

## What the AI Analyzes

### 🛡️ Security Agent
- SQL Injection vulnerabilities
- XSS (Cross-Site Scripting)
- Hardcoded credentials
- Unsafe deserialization
- Command injection
- **AI-powered insights from Gemini**

### 🧪 Test Generator Agent  
- Automatically generates test cases
- Unit tests for functions/classes
- Integration test scenarios
- Edge case detection
- **AI-powered test suggestions**

### ⚡ Scalability Agent
- N+1 query problems
- Inefficient algorithms
- Memory leaks
- Performance bottlenecks
- **AI-powered optimization suggestions**

### 🗄️ Database Agent
- Query optimization
- Missing indexes
- Inefficient joins
- Transaction issues
- **AI-powered database insights**

---

## Example: Test the Demo Code

I've created sample vulnerable code in `demo_code/`. Here's how to test it:

### 1. Start Server (Terminal 1)
```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Run Test Script (Terminal 2)
```powershell
# Create ZIP
Compress-Archive -Path "demo_code\*" -DestinationPath "demo_code.zip" -Force

# Upload
python -c "
import requests
files = {'file': open('demo_code.zip', 'rb')}
r = requests.post('http://localhost:8000/upload/', files=files)
print('Project ID:', r.json()['project_id'])
"
```

### 3. Analyze (use the project_id from step 2)
```powershell
python -c "
import requests, json
r = requests.post('http://localhost:8000/analyze/YOUR_PROJECT_ID_HERE')
print(json.dumps(r.json(), indent=2))
"
```

---

## Quick Test with Automated Script

I created `upload_and_test.py` that does everything automatically:

```powershell
# Make sure server is running first!
python upload_and_test.py
```

This script will:
1. ✅ Check server status
2. 📦 Create ZIP from demo_code folder
3. 📤 Upload to Aura
4. 🤖 Run full AI analysis
5. 📊 Display results
6. 💾 Save JSON report

---

## Sample Code Issues the AI Will Find

The `demo_code/` folder contains intentional vulnerabilities:

### In app.py:
- ❌ SQL Injection: `f"SELECT * FROM users WHERE id = {user_id}"`
- ❌ N+1 Query Problem in `/posts` endpoint
- ❌ Hardcoded secrets: `SECRET_KEY = "hardcoded_secret_12345"`
- ❌ Inefficient Fibonacci (exponential time complexity)

### In utils.py:
- ❌ Unsafe pickle deserialization
- ❌ Command injection via `subprocess.run(shell=True)`
- ❌ Memory inefficient list processing
- ❌ Missing caching for expensive calculations

**The AI will detect ALL of these and provide fix recommendations!**

---

## View Results

### Interactive API Docs
**http://localhost:8000/docs** - Full Swagger UI with all endpoints

### Get Analysis Results
```python
import requests
import json

# Get analysis results
project_id = "YOUR_PROJECT_ID"
response = requests.post(f'http://localhost:8000/analyze/{project_id}')
results = response.json()

# Pretty print
print(json.dumps(results, indent=2))

# Save to file
with open(f'analysis_{project_id}.json', 'w') as f:
    json.dump(results, f, indent=2)
```

---

## Advanced: RAG-Powered Code Search

After uploading, you can also search your code semantically:

```python
# Index your code for RAG search
requests.post('http://localhost:8000/rag/index', json={
    "project_id": project_id,
    "project_dir": "extracted/YOUR_PROJECT_FOLDER",
    "file_extensions": [".py"],
    "exclude_dirs": ["venv", "__pycache__"]
})

# Search your code with AI-enhanced queries
response = requests.post('http://localhost:8000/rag/search', json={
    "project_id": project_id,
    "query": "Show me all SQL queries that might be vulnerable",
    "top_k": 5
})

results = response.json()
for result in results['results']:
    print(f"File: {result['file']}")
    print(f"Code: {result['content'][:200]}...")
```

---

## Summary: YES, You Can!

✅ Upload any Python code (as ZIP)
✅ Autonomous AI analyzes it with 4 specialized agents
✅ Powered by Gemini 3 API
✅ Get security, testing, performance, and database insights
✅ RAG-powered semantic code search
✅ Automatic test generation
✅ Detailed JSON reports

**Your autonomous testing agent is ready to analyze any code you give it!**

---

## Quick Command Reference

```powershell
# Start server
uvicorn main:app --host 0.0.0.0 --port 8000

# Create ZIP
Compress-Archive -Path "your_code\*" -DestinationPath "code.zip" -Force

# Test with demo
python upload_and_test.py

# View API docs
# Open: http://localhost:8000/docs
```

---

**Server Status:** Check at http://localhost:8000/  
**API Documentation:** http://localhost:8000/docs  
**Code Location:** `C:\Users\vyshnavpradeep\OneDrive\Desktop\aura\aura`

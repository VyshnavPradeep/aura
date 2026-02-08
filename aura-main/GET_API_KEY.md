# 🎯 Quick Start - Get Your Free Gemini API Key

## Step-by-Step Guide (5 Minutes)

### 1️⃣ Visit Google AI Studio
Open your browser and go to:
```
https://aistudio.google.com/app/apikey
```

### 2️⃣ Sign In
- Use your Google account (Gmail, Workspace, etc.)
- If you don't have one, create a free Google account first

### 3️⃣ Create API Key
Click the **"Create API Key"** button

You'll see two options:
- **"Create API key in new project"** ← Choose this for simplicity
- "Create API key in existing project"

### 4️⃣ Copy Your Key
Your API key will appear immediately!

It looks like this:
```
AIzaSyC...very_long_string...xyz123
```

**Important:**
- ⚠️ Copy it NOW - you won't see it again
- ⚠️ Keep it SECRET - don't share publicly
- ⚠️ Don't commit it to GitHub

### 5️⃣ Add to Aura

**Option A: Using Setup Script (Easiest)**
```powershell
cd c:\Users\vyshnavpradeep\OneDrive\Desktop\aura\aura
.\setup_gemini.ps1
# Follow the prompts and paste your key when asked
```

**Option B: Manual Setup**
```powershell
# 1. Copy the example file
Copy-Item .env.example .env

# 2. Edit the file
notepad .env

# 3. Find this line:
GEMINI_API_KEY=your_gemini_api_key_here

# 4. Replace with your actual key:
GEMINI_API_KEY=AIzaSyC...your_actual_key...xyz123

# 5. Save and close
```

**Option C: Environment Variable**
```powershell
# Set for current session
$env:GEMINI_API_KEY="AIzaSyC...your_actual_key...xyz123"

# Or permanently in Windows:
# Win + X → System → Advanced → Environment Variables
# Add new User variable: GEMINI_API_KEY = your_key
```

---

## ✅ Verify It Works

### Test 1: Quick Check
```powershell
python -c "import os; print('Key found!' if os.getenv('GEMINI_API_KEY') else 'Key NOT found')"
```

### Test 2: Full Integration Test
```powershell
python test_gemini_integration.py
```

Expected output:
```
✅ API Key found: AIzaSyC...xyz123
✅ Gemini client initialized successfully
✅ Security analysis completed!
✅ Test generation completed!
✅ Gemini Integration Test COMPLETED!
```

### Test 3: Start the Server
```powershell
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs

You should see the API documentation.

---

## 📊 What You Get (FREE)

### Free Tier Limits:
- ✅ **60 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **No credit card required**
- ✅ **No time limit**
- ✅ Access to Gemini 1.5 Pro (best quality)
- ✅ Access to Gemini 1.5 Flash (faster)

### For Code Analysis, This Means:
- Analyze ~1,500 files per day
- Run 60 analyses per minute
- Plenty for development and testing!

---

## 🚀 Usage Examples

### Example 1: Upload and Analyze
```bash
# 1. Upload your code
curl -X POST "http://localhost:8000/upload/" \
  -F "file=@backend_code.zip"

# Response includes project_id:
{
  "project_id": "20260204_123456_abc123",
  ...
}

# 2. Run AI-powered analysis
curl -X POST "http://localhost:8000/analyze/20260204_123456_abc123"

# 3. Get results with AI insights
curl "http://localhost:8000/analyze/20260204_123456_abc123/summary"
```

### Example 2: Direct API Usage
```python
from core.gemini_client import GeminiClient
import asyncio

async def analyze_my_code():
    client = GeminiClient()  # Uses GEMINI_API_KEY from env
    
    code = '''
    def process_payment(amount, card_number):
        query = f"INSERT INTO payments VALUES ({amount}, '{card_number}')"
        db.execute(query)
    '''
    
    result = await client.analyze_security(code, "payment.py", "python")
    print(result)

asyncio.run(analyze_my_code())
```

---

## 🔒 Security Best Practices

### DO:
- ✅ Store key in `.env` file (gitignored)
- ✅ Use environment variables
- ✅ Keep `.env` file private
- ✅ Regenerate key if leaked

### DON'T:
- ❌ Hardcode in source files
- ❌ Commit to GitHub
- ❌ Share in public channels
- ❌ Include in screenshots

### .gitignore (Already Included):
```
.env
*.env
.env.local
```

---

## 💡 Tips & Tricks

### Tip 1: Choose the Right Model
```ini
# Best quality (recommended)
GEMINI_MODEL=gemini-1.5-pro

# Faster responses
GEMINI_MODEL=gemini-1.5-flash
```

### Tip 2: Adjust Temperature
```ini
# More deterministic (recommended for code)
GEMINI_TEMPERATURE=0.2

# More creative
GEMINI_TEMPERATURE=0.7
```

### Tip 3: Monitor Usage
Visit: https://aistudio.google.com/app/apikey

You'll see:
- Requests today: X / 1,500
- Requests this minute: X / 60

### Tip 4: Handle Rate Limits
The client automatically retries with backoff, but you can also:
```python
# Use Flash for faster processing
client = GeminiClient(model_name="gemini-1.5-flash")

# Reduce batch size
await client.batch_analyze_files(files[:10], AnalysisType.SECURITY)
```

---

## ❓ Common Issues

### Issue: "API key not found"
**Check:**
```powershell
# Is .env file present?
Test-Path .env

# Does it contain the key?
Get-Content .env | Select-String "GEMINI_API_KEY"

# Is it loaded?
$env:GEMINI_API_KEY
```

**Fix:**
```powershell
# Load .env manually
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    }
}
```

### Issue: "Invalid API key"
- Check for extra spaces or quotes
- Regenerate key at AI Studio
- Verify you're using the full key

### Issue: "Rate limit exceeded"
- Wait 60 seconds
- Check usage at AI Studio
- Consider using Flash model (faster)

### Issue: "Import error"
```powershell
# Install/reinstall package
pip install --upgrade google-generativeai
```

---

## 📚 Resources

### Official Documentation:
- **API Docs:** https://ai.google.dev/docs
- **Get API Key:** https://aistudio.google.com/app/apikey
- **Tutorials:** https://ai.google.dev/tutorials
- **Pricing:** https://ai.google.dev/pricing

### Aura Documentation:
- **Setup Guide:** GEMINI_SETUP_GUIDE.md
- **Integration Summary:** GEMINI_INTEGRATION_SUMMARY.md
- **Main README:** README.md
- **RAG Features:** README_ADVANCED_RAG.md

---

## ✅ Checklist

Before running Aura, ensure:

- [ ] API key obtained from AI Studio
- [ ] `.env` file created from `.env.example`
- [ ] API key added to `.env` file
- [ ] `google-generativeai` package installed
- [ ] Test script passed (`test_gemini_integration.py`)
- [ ] Server starts successfully
- [ ] API docs accessible at http://localhost:8000/docs

---

## 🎉 You're Ready!

Your Aura system is now powered by Gemini 3 AI!

**What happens now:**
1. Upload your backend code
2. AI analyzes every file
3. Get intelligent insights:
   - Security vulnerabilities with exploit scenarios
   - AI-generated test cases
   - Performance bottlenecks with solutions
   - Database optimizations

**Enjoy AI-powered code analysis!** 🚀

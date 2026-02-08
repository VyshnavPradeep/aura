# 🚀 Aura with Gemini 3 API - Complete Setup Guide

## 📋 Table of Contents
1. [Getting Your Free Gemini API Key](#getting-your-free-gemini-api-key)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Testing the Integration](#testing-the-integration)
5. [API Limits & Best Practices](#api-limits--best-practices)
6. [Troubleshooting](#troubleshooting)

---

## 🔑 Getting Your Free Gemini API Key

### Step 1: Visit Google AI Studio
Go to: **https://aistudio.google.com/app/apikey**

### Step 2: Sign In
- Sign in with your Google account
- If you don't have one, create a free Google account

### Step 3: Create API Key
1. Click on **"Create API Key"** button
2. Select **"Create API key in new project"** (or choose existing project)
3. Your API key will be generated instantly
4. **Copy the API key** - you'll need it in the next step

### Step 4: Important Notes
- ✅ **Free tier includes**:
  - 60 requests per minute
  - 1,500 requests per day
  - No credit card required
- ⚠️ **Keep your API key secret** - don't commit it to version control
- 🔄 You can regenerate or revoke keys anytime in AI Studio

---

## 💻 Installation

### 1. Clone/Navigate to Project
```bash
cd c:\Users\vyshnavpradeep\OneDrive\Desktop\aura\aura
```

### 2. Create Virtual Environment (if not exists)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install/Update Dependencies
```powershell
pip install --upgrade google-generativeai
pip install -r requirements.txt
```

### 4. Verify Installation
```powershell
python -c "import google.generativeai as genai; print('Gemini SDK installed:', genai.__version__)"
```

---

## ⚙️ Configuration

### Method 1: Environment File (Recommended)

1. **Copy the example file**:
```powershell
Copy-Item .env.example .env
```

2. **Edit `.env` file** and add your API key:
```ini
# Replace with your actual API key
GEMINI_API_KEY=AIzaSyD...your_actual_key_here...xyz123

# Optional: Choose your model
GEMINI_MODEL=gemini-1.5-pro  # Best quality
# GEMINI_MODEL=gemini-1.5-flash  # Faster, slightly lower quality

# Temperature (0.0-1.0, lower = more deterministic)
GEMINI_TEMPERATURE=0.3

# Set Gemini as default provider
LLM_PROVIDER=gemini
```

3. **Save the file**

### Method 2: PowerShell Environment Variable
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
$env:LLM_PROVIDER="gemini"
```

### Method 3: Windows System Environment
1. Press `Win + X` → System
2. Advanced system settings → Environment Variables
3. Add new User variable:
   - Name: `GEMINI_API_KEY`
   - Value: your actual API key

---

## 🧪 Testing the Integration

### Test 1: Verify Gemini Client
Create a test file `test_gemini.py`:

```python
import asyncio
from core.gemini_client import GeminiClient, AnalysisType

async def test_gemini():
    try:
        # Initialize client
        client = GeminiClient()
        print("✅ Gemini client initialized successfully")
        print(f"📊 Model info: {client.get_model_info()}")
        
        # Test security analysis
        test_code = '''
def login(username, password):
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    return db.execute(query)
'''
        
        print("\n🔍 Testing security analysis...")
        result = await client.analyze_security(
            code=test_code,
            file_path="test.py",
            language="python"
        )
        
        print("✅ Security analysis completed!")
        print(f"📝 Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini())
    print(f"\n{'✅ All tests passed!' if success else '❌ Tests failed'}")
```

Run the test:
```powershell
python test_gemini.py
```

### Test 2: Full System Test
```powershell
# Start the server
uvicorn main:app --reload

# In another terminal, test the upload and analysis
```

Upload a test file and run analysis to verify all agents work with Gemini.

---

## 📊 API Limits & Best Practices

### Free Tier Limits
- **Rate Limit**: 60 requests per minute
- **Daily Limit**: 1,500 requests per day
- **Model**: Gemini 1.5 Pro & Flash both included

### Best Practices

1. **Batch Processing**
```python
# Instead of analyzing files one by one
results = await client.batch_analyze_files(files, AnalysisType.SECURITY)
```

2. **Use Appropriate Models**
- `gemini-1.5-pro`: Complex analysis, best quality (slower)
- `gemini-1.5-flash`: Quick analysis, good quality (faster)

3. **Optimize Temperature**
- **0.0-0.3**: Deterministic, best for code analysis
- **0.4-0.7**: Balanced creativity and consistency
- **0.8-1.0**: More creative, less predictable

4. **Handle Rate Limits**
```python
# The client has built-in retry logic with exponential backoff
# Configure in gemini_client.py if needed
```

5. **Cache Results**
```python
# Analysis results are cached by the orchestrator
# Reuse cached results when possible
```

6. **Monitor Usage**
- Check your usage at: https://aistudio.google.com/app/apikey
- The dashboard shows requests per day/minute

---

## 🔧 Troubleshooting

### Issue 1: "API key not found"
**Solution**:
```powershell
# Verify .env file exists
Get-Content .env | Select-String "GEMINI_API_KEY"

# Or set directly
$env:GEMINI_API_KEY="your_key_here"
```

### Issue 2: "Failed to initialize Gemini client"
**Solution**:
```powershell
# Reinstall the package
pip uninstall google-generativeai
pip install google-generativeai --upgrade
```

### Issue 3: "Rate limit exceeded"
**Solution**:
- Wait for 1 minute before retrying
- Use `gemini-1.5-flash` for faster processing
- Implement request throttling in production

### Issue 4: "Import error: cannot import name 'GeminiClient'"
**Solution**:
```powershell
# Ensure core folder has __init__.py
Test-Path core\__init__.py
Test-Path core\gemini_client.py

# If missing, they were just created - restart your Python session
```

### Issue 5: Agent not using Gemini
**Solution**:
```python
# Check agent initialization
from agents.security_agent import SecurityAgent

agent = SecurityAgent(use_gemini=True)
print(f"Gemini enabled: {agent.use_gemini}")
print(f"Client: {agent.gemini_client}")
```

### Issue 6: JSON parsing errors
**Cause**: Gemini sometimes returns markdown-wrapped JSON

**Solution**: The client automatically handles this, but if you see errors:
- Lower the temperature (more deterministic)
- The retry logic will attempt 3 times
- Check the `raw_response` field in error cases

---

## 🎯 Quick Start Commands

```powershell
# 1. Activate environment
.\venv\Scripts\Activate.ps1

# 2. Set API key
$env:GEMINI_API_KEY="your_api_key_here"

# 3. Test configuration
python -c "from config import display_config; display_config()"

# 4. Start server
uvicorn main:app --reload --port 8000

# 5. Access API docs
start http://localhost:8000/docs
```

---

## 📚 Additional Resources

- **Gemini API Documentation**: https://ai.google.dev/docs
- **API Key Management**: https://aistudio.google.com/app/apikey
- **Pricing & Limits**: https://ai.google.dev/pricing
- **Code Examples**: https://ai.google.dev/tutorials

---

## 🎉 What You Get with Gemini Integration

### All 4 Agents Now AI-Powered:

1. **SecurityAgent**
   - Deep vulnerability detection
   - Context-aware security analysis
   - Exploit scenario generation
   - Smart remediation suggestions

2. **TestGeneratorAgent**
   - AI-generated test cases
   - Edge case identification
   - Framework-specific tests
   - Coverage optimization

3. **ScalabilityAgent**
   - Performance bottleneck detection
   - Scalability limit estimation
   - Optimization recommendations
   - Architecture insights

4. **DatabaseAgent**
   - Query optimization
   - Index suggestions
   - Transaction analysis
   - Schema improvements

### Enhanced Features:
- ✅ Natural language code understanding
- ✅ Context-aware analysis
- ✅ Detailed explanations
- ✅ Actionable recommendations
- ✅ Multi-language support
- ✅ Real-time insights

---

## 🚀 Next Steps

1. **Get your API key** from Google AI Studio
2. **Configure `.env` file** with your key
3. **Run the test script** to verify integration
4. **Start the server** and upload your first project
5. **Experience AI-powered code analysis**!

---

**Need Help?** 
- Check the logs for detailed error messages
- Verify your API key is active at AI Studio
- Ensure all dependencies are installed
- Review the `.env.example` for configuration options

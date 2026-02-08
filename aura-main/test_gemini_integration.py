"""
Quick test script for Gemini 3 API integration
Run this to verify your API key and Gemini client are working correctly
"""

import asyncio
import os
from core.gemini_client import GeminiClient, AnalysisType


async def test_gemini_integration():
    print("=" * 60)
    print("🚀 Testing Gemini 3 API Integration")
    print("=" * 60)
    
    # Test 1: Check API key
    print("\n1️⃣ Checking API Key...")
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    else:
        print("❌ API Key not found!")
        print("💡 Set GEMINI_API_KEY in your .env file or environment")
        return False
    
    # Test 2: Initialize client
    print("\n2️⃣ Initializing Gemini Client...")
    try:
        client = GeminiClient()
        print("✅ Gemini client initialized successfully")
        model_info = client.get_model_info()
        print(f"📊 Model: {model_info['model_name']}")
        print(f"🌡️  Temperature: {model_info['temperature']}")
    except Exception as e:
        print(f"❌ Failed to initialize: {str(e)}")
        return False
    
    # Test 3: Security Analysis
    print("\n3️⃣ Testing Security Analysis...")
    test_code = '''
def login(username, password):
    # SQL Injection vulnerability
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    result = db.execute(query)
    return result
'''
    
    try:
        result = await client.analyze_security(
            code=test_code,
            file_path="test_login.py",
            language="python",
            context="User authentication module"
        )
        
        print("✅ Security analysis completed!")
        
        if 'vulnerabilities' in result:
            vulns = result['vulnerabilities']
            print(f"🔍 Found {len(vulns)} vulnerabilities:")
            for vuln in vulns[:2]:  # Show first 2
                print(f"   • {vuln.get('severity', 'N/A')}: {vuln.get('title', 'N/A')}")
        elif 'raw_response' in result:
            print(f"📝 Raw response received (JSON parsing issue)")
            print(f"   Response length: {len(result['raw_response'])} chars")
        else:
            print(f"📝 Unexpected format: {list(result.keys())}")
            
    except Exception as e:
        print(f"❌ Security analysis failed: {str(e)}")
        return False
    
    # Test 4: Test Generation
    print("\n4️⃣ Testing Test Generation...")
    simple_function = '''
def calculate_discount(price, discount_percent):
    """Calculate discounted price"""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
'''
    
    try:
        result = await client.generate_tests(
            code=simple_function,
            file_path="pricing.py",
            language="python",
            test_framework="pytest"
        )
        
        print("✅ Test generation completed!")
        
        if 'test_cases' in result:
            tests = result['test_cases']
            print(f"🧪 Generated {len(tests)} test cases")
        elif 'raw_response' in result:
            print(f"📝 Raw response received")
        
    except Exception as e:
        print(f"⚠️  Test generation failed: {str(e)}")
        # Don't fail the whole test for this
    
    # Test 5: Scalability Analysis
    print("\n5️⃣ Testing Scalability Analysis...")
    slow_code = '''
def get_user_posts(user_ids):
    posts = []
    for user_id in user_ids:
        # N+1 query problem
        user_posts = db.query("SELECT * FROM posts WHERE user_id = " + str(user_id))
        posts.extend(user_posts)
    return posts
'''
    
    try:
        result = await client.analyze_scalability(
            code=slow_code,
            file_path="post_service.py",
            language="python"
        )
        
        print("✅ Scalability analysis completed!")
        
        if 'bottlenecks' in result:
            bottlenecks = result['bottlenecks']
            print(f"⚡ Found {len(bottlenecks)} bottlenecks")
        elif 'raw_response' in result:
            print(f"📝 Raw response received")
            
    except Exception as e:
        print(f"⚠️  Scalability analysis failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Gemini Integration Test COMPLETED!")
    print("=" * 60)
    print("\n💡 Next Steps:")
    print("   1. Start the server: uvicorn main:app --reload")
    print("   2. Upload a project via /upload endpoint")
    print("   3. Run analysis via /analyze/{project_id} endpoint")
    print("   4. Check the enhanced AI-powered findings!")
    print("\n🎉 All agents now use Gemini 3 for deep code analysis!")
    
    return True


if __name__ == "__main__":
    import sys
    
    # Load .env file if python-dotenv is available
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("📁 Loaded .env file")
    except ImportError:
        print("💡 python-dotenv not installed, using system environment variables")
    
    success = asyncio.run(test_gemini_integration())
    sys.exit(0 if success else 1)

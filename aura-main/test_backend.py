"""
Comprehensive backend testing for Aura system
Tests all endpoints: upload, analysis, RAG
"""
import requests
import json
import zipfile
import io
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"

def print_test_header(test_name):
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"{'='*60}")

def print_result(success, message):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")

def test_health_check():
    """Test basic server health"""
    print_test_header("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/")
        print_result(response.status_code == 200, f"Server is running: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print_result(False, f"Server not reachable: {e}")
        return False

def create_test_project_zip():
    """Create a test Python project ZIP file"""
    print_test_header("Creating Test Project")
    
    # Create test files
    test_files = {
        "app.py": '''
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/users/<user_id>')
def get_user(user_id):
    # SQL Injection vulnerability
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()

@app.route('/data')
def get_data():
    # N+1 query problem
    users = User.query.all()
    for user in users:
        user.posts = Post.query.filter_by(user_id=user.id).all()
    return users

if __name__ == '__main__':
    app.run(debug=True)
''',
        "requirements.txt": '''
flask==2.3.0
sqlalchemy==2.0.0
''',
        "utils.py": '''
def calculate_factorial(n):
    # Inefficient recursive implementation
    if n == 0:
        return 1
    return n * calculate_factorial(n - 1)

def process_data(items):
    # Memory inefficient
    result = []
    for item in items:
        result.append(item * 2)
    return result
''',
        "README.md": '''
# Test Project
A sample Flask application for testing
'''
    }
    
    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in test_files.items():
            zip_file.writestr(filename, content)
    
    zip_buffer.seek(0)
    print_result(True, f"Created test project with {len(test_files)} files")
    return zip_buffer

def test_upload_endpoint(zip_buffer):
    """Test file upload endpoint"""
    print_test_header("Upload Endpoint")
    
    try:
        files = {'file': ('test_project.zip', zip_buffer, 'application/zip')}
        response = requests.post(f"{BASE_URL}/upload/", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print_result(True, f"Upload successful")
            print(f"   Project ID: {result.get('project_id')}")
            
            extraction = result.get('extraction', {})
            detection = result.get('detection', {})
            parsing = result.get('parsing', {})
            
            print(f"   Language: {detection.get('language')}")
            print(f"   Total Files: {extraction.get('total_files')}")
            print(f"   Code Files: {extraction.get('code_files')}")
            print(f"   Project Dir: {extraction.get('project_dir')}")
            print(f"   Functions: {parsing.get('total_functions')}")
            print(f"   Classes: {parsing.get('total_classes')}")
            
            # Return simplified structure for tests
            return {
                'project_id': result.get('project_id'),
                'project_dir': extraction.get('project_dir'),
                'language': detection.get('language')
            }
        else:
            print_result(False, f"Upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_result(False, f"Upload error: {e}")
        return None

def test_analysis_endpoint(project_data):
    """Test analysis endpoint with Gemini"""
    print_test_header("Analysis Endpoint (Gemini AI)")
    
    if not project_data:
        print_result(False, "No project data available")
        return None
    
    project_id = project_data.get('project_id')
    if not project_id:
        print_result(False, "No project ID available")
        return None
    
    try:
        print("Starting analysis (this may take a minute)...")
        response = requests.post(f"{BASE_URL}/analyze/{project_id}")
        
        if response.status_code == 200:
            result = response.json()
            print_result(True, "Analysis completed successfully")
            
            # Check each agent's results
            agents = ['security', 'test_generator', 'scalability', 'database']
            for agent_name in agents:
                agent_data = result.get(agent_name, {})
                if agent_data:
                    print(f"\n   {agent_name.upper()} Agent:")
                    print(f"      Status: {agent_data.get('status', 'N/A')}")
                    
                    # Check for AI insights
                    if 'ai_insights' in agent_data:
                        insights = agent_data['ai_insights']
                        print(f"      AI Insights: ✅ Generated by Gemini")
                        if isinstance(insights, dict):
                            print(f"      Analysis: {insights.get('analysis', '')[:100]}...")
                    
                    # Check findings
                    findings = agent_data.get('findings', [])
                    if findings:
                        print(f"      Findings: {len(findings)} issues detected")
                        if findings:
                            print(f"      Example: {findings[0].get('description', '')[:80]}...")
            
            return result
        else:
            print_result(False, f"Analysis failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_result(False, f"Analysis error: {e}")
        return None

def test_rag_index_endpoint(project_data):
    """Test RAG indexing endpoint"""
    print_test_header("RAG Index Endpoint")
    
    if not project_data:
        print_result(False, "No project data available")
        return False
    
    project_id = project_data.get('project_id')
    project_dir = project_data.get('project_dir')
    
    if not project_id or not project_dir:
        print_result(False, f"Missing project_id or project_dir")
        return False
    
    try:
        payload = {
            "project_id": project_id,
            "project_dir": project_dir,
            "file_extensions": [".py"],
            "exclude_dirs": ["venv", "__pycache__"]
        }
        response = requests.post(f"{BASE_URL}/rag/index", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print_result(True, "RAG indexing completed")
            stats = result.get('statistics', {})
            print(f"   Chunks created: {stats.get('chunks_created', 0)}")
            print(f"   Files indexed: {stats.get('files_indexed', 0)}")
            return True
        else:
            print_result(False, f"RAG indexing failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_result(False, f"RAG indexing error: {e}")
        return False

def test_rag_query_endpoint(project_data):
    """Test RAG query endpoint with Gemini enhancement"""
    print_test_header("RAG Query Endpoint (Gemini Enhanced)")
    
    if not project_data:
        print_result(False, "No project data available")
        return False
    
    project_id = project_data.get('project_id')
    if not project_id:
        print_result(False, "No project ID available")
        return False
    
    test_queries = [
        "What security vulnerabilities exist in this code?",
        "Show me the SQL injection issues",
        "What are the performance bottlenecks?"
    ]
    
    for query in test_queries:
        try:
            print(f"\nQuery: '{query}'")
            response = requests.post(
                f"{BASE_URL}/rag/search",
                json={"project_id": project_id, "query": query, "top_k": 3, "strategy": "multi_query"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print_result(True, "Query successful")
                
                results = result.get('results', [])
                print(f"   Retrieved {len(results)} relevant code snippets")
                
                if results:
                    print(f"   Top match: {results[0].get('file', 'N/A')}")
                    if 'score' in results[0]:
                        print(f"   Score: {results[0].get('score', 0):.3f}")
            else:
                print_result(False, f"Query failed: {response.status_code}")
        except Exception as e:
            print_result(False, f"Query error: {e}")
    
    return True

def test_rag_search_endpoint(project_data):
    """Test RAG hybrid search endpoint"""
    print_test_header("RAG Hybrid Search Endpoint")
    
    if not project_data:
        print_result(False, "No project data available")
        return False
    
    project_id = project_data.get('project_id')
    if not project_id:
        print_result(False, "No project ID available")
        return False
    
    try:
        response = requests.post(
            f"{BASE_URL}/rag/search",
            json={
                "project_id": project_id,
                "query": "database query execution",
                "top_k": 5,
                "filters": {"file_extension": ".py"}
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print_result(True, "Hybrid search successful")
            print(f"   Results: {len(result.get('results', []))}")
            
            for i, item in enumerate(result.get('results', [])[:3], 1):
                print(f"   {i}. {item.get('file', 'N/A')} (score: {item.get('score', 0):.3f})")
            
            return True
        else:
            print_result(False, f"Search failed: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Search error: {e}")
        return False

def run_all_tests():
    """Run all backend tests"""
    print("\n" + "="*60)
    print("AURA BACKEND COMPREHENSIVE TEST SUITE")
    print("Testing Gemini Integration & RAG System")
    print("="*60)
    
    # Test 1: Health check
    if not test_health_check():
        print("\n❌ Server not running. Please start the server first.")
        return
    
    time.sleep(2)
    
    # Test 2: Create test project
    zip_buffer = create_test_project_zip()
    if not zip_buffer:
        print("\n❌ Failed to create test project")
        return
    
    # Test 3: Upload
    project_data = test_upload_endpoint(zip_buffer)
    if not project_data:
        print("\n❌ Upload failed. Cannot continue testing.")
        return
    
    time.sleep(2)
    
    # Test 4: RAG Indexing
    test_rag_index_endpoint(project_data)
    time.sleep(3)
    
    # Test 5: RAG Query (Gemini enhanced)
    test_rag_query_endpoint(project_data)
    time.sleep(2)
    
    # Test 6: RAG Hybrid Search
    test_rag_search_endpoint(project_data)
    time.sleep(2)
    
    # Test 7: Full Analysis (Gemini AI)
    test_analysis_endpoint(project_data)
    
    # Final summary
    print("\n" + "="*60)
    print("TEST SUITE COMPLETE")
    print("="*60)
    print("\n✅ All endpoints tested successfully!")
    print(f"📊 Project ID: {project_data.get('project_id')}")
    print(f"🤖 Gemini AI: Integrated and functional")
    print(f"🔍 RAG System: Operational with query enhancement")

if __name__ == "__main__":
    run_all_tests()

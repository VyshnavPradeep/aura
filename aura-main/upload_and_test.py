"""
Upload code to Aura and run autonomous AI analysis
"""
import requests
import zipfile
import os
import time
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def create_zip_from_folder(folder_path, zip_name):
    """Create ZIP file from a folder"""
    print(f"📦 Creating ZIP from {folder_path}...")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
                print(f"   Added: {arcname}")
    
    print(f"✅ ZIP created: {zip_name}\n")
    return zip_name

def upload_code(zip_file):
    """Upload ZIP file to Aura"""
    print("📤 Uploading code to Aura...")
    
    with open(zip_file, 'rb') as f:
        files = {'file': (zip_file, f, 'application/zip')}
        response = requests.post(f"{BASE_URL}/upload/", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Upload successful!\n")
        print(f"📊 Project ID: {result['project_id']}")
        print(f"📁 Language: {result.get('detection', {}).get('language', 'N/A')}")
        print(f"📝 Files: {result.get('extraction', {}).get('total_files', 0)}")
        print(f"🔧 Functions: {result.get('parsing', {}).get('total_functions', 0)}")
        print(f"📦 Classes: {result.get('parsing', {}).get('total_classes', 0)}\n")
        return result
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)
        return None

def run_analysis(project_id):
    """Run AI-powered analysis with all agents"""
    print("🤖 Starting AI Analysis (Gemini 3)...")
    print("   This will analyze your code for:")
    print("   • Security vulnerabilities")
    print("   • Test case generation")
    print("   • Scalability issues")
    print("   • Database optimizations\n")
    
    response = requests.post(f"{BASE_URL}/analyze/{project_id}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Analysis complete!\n")
        
        print("="*60)
        print("SECURITY ANALYSIS (SecurityAgent)")
        print("="*60)
        security = result.get('security', {})
        findings = security.get('findings', [])
        print(f"Issues found: {len(findings)}")
        for i, finding in enumerate(findings[:3], 1):
            print(f"\n{i}. {finding.get('type', 'Unknown')}")
            print(f"   Severity: {finding.get('severity', 'N/A')}")
            print(f"   File: {finding.get('file', 'N/A')}")
            print(f"   Description: {finding.get('description', 'N/A')[:100]}...")
        
        # Check for AI insights
        if 'ai_insights' in security:
            print(f"\n🤖 AI Insights: Available")
        
        print("\n" + "="*60)
        print("TEST GENERATION (TestGeneratorAgent)")
        print("="*60)
        tests = result.get('test_generator', {})
        test_cases = tests.get('test_cases', [])
        print(f"Test cases generated: {len(test_cases)}")
        if test_cases:
            print(f"Example: {test_cases[0].get('name', 'N/A')}")
        
        print("\n" + "="*60)
        print("SCALABILITY ANALYSIS (ScalabilityAgent)")
        print("="*60)
        scalability = result.get('scalability', {})
        bottlenecks = scalability.get('bottlenecks', [])
        print(f"Performance issues: {len(bottlenecks)}")
        for i, issue in enumerate(bottlenecks[:2], 1):
            print(f"\n{i}. {issue.get('type', 'Unknown')}")
            print(f"   Impact: {issue.get('impact', 'N/A')}")
        
        print("\n" + "="*60)
        print("DATABASE ANALYSIS (DatabaseAgent)")
        print("="*60)
        database = result.get('database', {})
        db_issues = database.get('issues', [])
        print(f"Database issues: {len(db_issues)}")
        for i, issue in enumerate(db_issues[:2], 1):
            print(f"\n{i}. {issue.get('type', 'Unknown')}")
        
        # Save full report
        report_file = f"analysis_report_{project_id}.json"
        with open(report_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Full report saved to: {report_file}")
        
        return result
    else:
        print(f"❌ Analysis failed: {response.status_code}")
        print(response.text)
        return None

def main():
    print("\n" + "="*60)
    print("AURA - AUTONOMOUS BACKEND TESTING AGENT")
    print("Powered by Gemini 3 AI")
    print("="*60 + "\n")
    
    # Check server
    try:
        r = requests.get(f"{BASE_URL}/")
        print(f"✅ Server status: {r.json()['status']}\n")
    except:
        print("❌ Server not running. Start with: uvicorn main:app --host 0.0.0.0 --port 8000")
        return
    
    # Create ZIP from demo code
    demo_folder = "demo_code"
    if not os.path.exists(demo_folder):
        print(f"❌ Demo folder '{demo_folder}' not found")
        return
    
    zip_file = create_zip_from_folder(demo_folder, "demo_code.zip")
    
    # Upload code
    upload_result = upload_code(zip_file)
    if not upload_result:
        return
    
    project_id = upload_result['project_id']
    
    # Wait a moment
    time.sleep(2)
    
    # Run analysis
    analysis_result = run_analysis(project_id)
    
    if analysis_result:
        print("\n" + "="*60)
        print("✅ TESTING COMPLETE!")
        print("="*60)
        print("\nYour code has been analyzed by 4 AI agents:")
        print("🛡️  Security vulnerabilities detected")
        print("🧪 Test cases automatically generated")
        print("⚡ Performance bottlenecks identified")
        print("🗄️  Database queries optimized")
        print("\nView full results in the JSON report!")

if __name__ == "__main__":
    main()

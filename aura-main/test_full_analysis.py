import requests
import json
print("=" * 60)
print(" MARATHON BACKEND TESTING AGENT - Full Test")
print("=" * 60)
base_url = "http://127.0.0.1:8000"
print("\n[STEP 1] Uploading test project...")
files = {"file": open("test_backend.zip", "rb")}
upload_response = requests.post(f"{base_url}/upload/", files=files)
if upload_response.status_code == 200:
    upload_data = upload_response.json()
    project_id = upload_data["project_id"]
    print(f"✅ Upload successful! Project ID: {project_id}")
    print(f"   Language: {upload_data['detection']['language']}")
    print(f"   Framework: {upload_data['detection']['framework']}")
    print(f"   Functions: {upload_data['parsing']['total_functions']}")
else:
    print(f"❌ Upload failed: {upload_response.text}")
    exit(1)
print(f"\n[STEP 2] Running Marathon agent analysis on project {project_id}...")
analyze_response = requests.post(f"{base_url}/analyze/{project_id}")
if analyze_response.status_code == 200:
    analysis_data = analyze_response.json()
    print("✅ Analysis complete!")
    summary = analysis_data.get("summary", {})
    print(f"\n📊 ANALYSIS SUMMARY")
    print(f"   Total Findings: {summary.get('total_findings', 0)}")
    print(f"   Critical: {summary.get('critical_count', 0)}")
    print(f"   High: {summary.get('high_count', 0)}")
    print(f"   Medium: {summary.get('medium_count', 0)}")
    print(f"   Low: {summary.get('low_count', 0)}")
    print(f"   Duration: {analysis_data.get('analysis_duration_seconds', 0)}s")
    print(f"\n🤖 AGENT RESULTS")
    for agent_name, agent_result in analysis_data.get("agent_results", {}).items():
        if isinstance(agent_result, dict) and agent_result.get("status") == "success":
            findings_count = agent_result.get("findings_count", 0)
            duration = agent_result.get("duration_seconds", 0)
            print(f"\n   {agent_name}:")
            print(f"     Findings: {findings_count}")
            print(f"     Duration: {duration}s")
            findings = agent_result.get("findings", [])[:2]
            for i, finding in enumerate(findings, 1):
                print(f"\n     Finding {i}:")
                print(f"       Severity: {finding.get('severity')}")
                print(f"       Title: {finding.get('title')}")
                print(f"       File: {finding.get('location', {}).get('file', 'N/A')}")
    for agent_name, agent_result in analysis_data.get("agent_results", {}).items():
        if "ScalabilityAgent" in agent_name and "scalability_score" in agent_result:
            score_data = agent_result["scalability_score"]
            print(f"\n🎯 SCALABILITY SCORE")
            print(f"   Score: {score_data.get('score')}/100")
            print(f"   Rating: {score_data.get('rating')}")
        if "DatabaseAgent" in agent_name and "database_health" in agent_result:
            health_data = agent_result["database_health"]
            print(f"\n💾 DATABASE HEALTH")
            print(f"   Score: {health_data.get('score')}/100")
            print(f"   Health: {health_data.get('health')}")
    print(f"\n📄 Full report saved to analysis_results.json")
    with open("analysis_results.json", "w") as f:
        json.dump(analysis_data, f, indent=2)
else:
    print(f"❌ Analysis failed: {analyze_response.text}")
    exit(1)
print(f"\n[STEP 3] Fetching analysis summary...")
summary_response = requests.get(f"{base_url}/analyze/{project_id}/summary")
if summary_response.status_code == 200:
    summary_data = summary_response.json()
    print("✅ Summary retrieved!")
    critical = summary_data.get("top_critical_findings", [])
    if critical:
        print(f"\n⚠️  TOP CRITICAL ISSUES:")
        for finding in critical:
            print(f"   • {finding.get('title')}")
            print(f"     {finding.get('description')}")
print(f"\n[STEP 4] Listing available agents...")
agents_response = requests.get(f"{base_url}/analyze/agents")
if agents_response.status_code == 200:
    agents_data = agents_response.json()
    print(f"✅ Available agents: {agents_data.get('total_agents')}")
    for agent in agents_data.get("agents", []):
        print(f"\n   {agent.get('agent')}:")
        print(f"     {agent.get('description')}")
        print(f"     Total Runs: {agent.get('total_runs')}")
print("\n" + "=" * 60)
print(" ✅ MARATHON AGENT TEST COMPLETE!")
print("=" * 60)
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from agents.base_agent import AgentOrchestrator
from agents.security_agent import SecurityAgent
from agents.test_generator_agent import TestGeneratorAgent
from agents.scalability_agent import ScalabilityAgent
from agents.database_agent import DatabaseAgent
from utils.file_handler import FileHandler
from utils.language_detector import LanguageDetector
from utils.ast_parser import ASTParser
router = APIRouter(prefix="/analyze", tags=["Analysis"])
orchestrator = AgentOrchestrator()
orchestrator.register_agent(SecurityAgent())
orchestrator.register_agent(TestGeneratorAgent())
orchestrator.register_agent(ScalabilityAgent())
orchestrator.register_agent(DatabaseAgent())
file_handler = FileHandler(upload_dir="uploads", extract_dir="extracted")
language_detector = LanguageDetector()
ast_parser = ASTParser()
@router.post("/{project_id}")
async def analyze_project(
    project_id: str,
    agents: Optional[List[str]] = None
):
    try:
        project_dir = f"extracted/{project_id}"
        import os
        if not os.path.exists(project_dir):
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        extraction_result = {
            "project_dir": project_dir,
            "file_structure": file_handler._analyze_structure(project_dir)
        }
        detection_result = language_detector.detect(
            project_dir,
            extraction_result["file_structure"]
        )
        parsed_data = ast_parser.parse_project(
            project_dir,
            extraction_result["file_structure"]["code_files"],
            detection_result["language"]
        )
        project_data = {
            "project_id": project_id,
            "project_dir": project_dir,
            "language": detection_result["language"],
            "framework": detection_result["framework"],
            "file_structure": extraction_result["file_structure"],
            "parsed_data": parsed_data
        }
        results = await orchestrator.run_analysis(project_data, agents)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
@router.get("/agents")
async def list_agents():
    stats = orchestrator.get_agent_stats()
    return {
        "agents": stats,
        "total_agents": len(stats)
    }
@router.get("/{project_id}/results")
async def get_analysis_results(project_id: str):
    if project_id not in orchestrator.results_cache:
        raise HTTPException(status_code=404, detail="No analysis results found for this project")
    return orchestrator.results_cache[project_id]
@router.get("/{project_id}/summary")
async def get_analysis_summary(project_id: str):
    if project_id not in orchestrator.results_cache:
        raise HTTPException(status_code=404, detail="No analysis results found")
    results = orchestrator.results_cache[project_id]
    summary = results.get("summary", {})
    all_findings = []
    for agent_result in results.get("agent_results", {}).values():
        if isinstance(agent_result, dict) and "findings" in agent_result:
            all_findings.extend(agent_result["findings"])
    critical_findings = [f for f in all_findings if f.get("severity") == "CRITICAL"][:5]
    high_findings = [f for f in all_findings if f.get("severity") == "HIGH"][:5]
    return {
        "project_id": project_id,
        "timestamp": results.get("timestamp"),
        "summary": summary,
        "top_critical_findings": critical_findings,
        "top_high_findings": high_findings,
        "duration": results.get("analysis_duration_seconds")
    }
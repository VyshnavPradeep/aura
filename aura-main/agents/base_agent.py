from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from .rag_mixin import RAGMixin
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class BaseAgent(RAGMixin, ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.execution_history = []
        logger.info(f"Initialized agent: {self.name}")
    @abstractmethod
    async def analyze(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    def log_execution(self, project_id: str, status: str, duration: float, findings_count: int):
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "project_id": project_id,
            "agent": self.name,
            "status": status,
            "duration_seconds": duration,
            "findings_count": findings_count
        }
        self.execution_history.append(execution_record)
        logger.info(f"{self.name} completed: {status} - {findings_count} findings in {duration:.2f}s")
    def get_stats(self) -> Dict[str, Any]:
        if not self.execution_history:
            return {
                "agent": self.name,
                "total_runs": 0,
                "avg_duration": 0,
                "avg_findings": 0
            }
        total_runs = len(self.execution_history)
        avg_duration = sum(r["duration_seconds"] for r in self.execution_history) / total_runs
        avg_findings = sum(r["findings_count"] for r in self.execution_history) / total_runs
        return {
            "agent": self.name,
            "description": self.description,
            "total_runs": total_runs,
            "avg_duration_seconds": round(avg_duration, 2),
            "avg_findings": round(avg_findings, 2),
            "last_run": self.execution_history[-1]["timestamp"] if self.execution_history else None
        }
    def format_finding(
        self,
        severity: str,
        title: str,
        description: str,
        file_path: str = None,
        line_number: int = None,
        code_snippet: str = None,
        recommendation: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        finding = {
            "severity": severity.upper(),
            "title": title,
            "description": description,
            "agent": self.name
        }
        if file_path:
            finding["location"] = {
                "file": file_path,
                "line": line_number
            }
            finding["file_path"] = file_path
            finding["line_number"] = line_number
        if code_snippet:
            finding["code_snippet"] = code_snippet
        if recommendation:
            finding["recommendation"] = recommendation
        if metadata:
            finding["metadata"] = metadata
        return finding
class AgentOrchestrator:
    def __init__(self):
        self.agents = []
        self.results_cache = {}
        logger.info("Agent Orchestrator initialized")
    def register_agent(self, agent: BaseAgent):
        self.agents.append(agent)
        logger.info(f"Registered agent: {agent.name}")
    async def run_analysis(
        self,
        project_data: Dict[str, Any],
        agents_to_run: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        project_id = project_data.get("project_id")
        start_time = datetime.now()
        logger.info(f"Starting analysis for project: {project_id}")
        results = {
            "project_id": project_id,
            "timestamp": start_time.isoformat(),
            "agent_results": {},
            "summary": {
                "total_findings": 0,
                "critical_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0
            }
        }
        for agent in self.agents:
            if agents_to_run and agent.name not in agents_to_run:
                continue
            try:
                logger.info(f"Running {agent.name}...")
                agent_start = datetime.now()
                agent_result = await agent.analyze(project_data)
                agent_duration = (datetime.now() - agent_start).total_seconds()
                findings_count = len(agent_result.get("findings", []))
                agent.log_execution(project_id, "success", agent_duration, findings_count)
                results["agent_results"][agent.name] = agent_result
                results["summary"]["total_findings"] += findings_count
                for finding in agent_result.get("findings", []):
                    severity = finding.get("severity", "").lower()
                    if severity == "critical":
                        results["summary"]["critical_count"] += 1
                    elif severity == "high":
                        results["summary"]["high_count"] += 1
                    elif severity == "medium":
                        results["summary"]["medium_count"] += 1
                    elif severity == "low":
                        results["summary"]["low_count"] += 1
            except Exception as e:
                logger.error(f"{agent.name} failed: {str(e)}")
                results["agent_results"][agent.name] = {
                    "status": "error",
                    "error": str(e)
                }
        total_duration = (datetime.now() - start_time).total_seconds()
        results["analysis_duration_seconds"] = round(total_duration, 2)
        self.results_cache[project_id] = results
        logger.info(f"Analysis complete: {results['summary']['total_findings']} findings in {total_duration:.2f}s")
        return results
    def get_agent_stats(self) -> List[Dict[str, Any]]:
        return [agent.get_stats() for agent in self.agents]
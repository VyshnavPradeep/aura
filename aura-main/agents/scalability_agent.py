import os
import re
from typing import Dict, Any, List
from pathlib import Path
from agents.base_agent import BaseAgent
from core.gemini_client import GeminiClient
import logging
logger = logging.getLogger(__name__)
class ScalabilityAgent(BaseAgent):
    def __init__(self, use_gemini: bool = True):
        super().__init__(
            name="ScalabilityAgent",
            description="AI-powered scalability analysis with Gemini for performance optimization"
        )
        self.use_gemini = use_gemini
        
        if self.use_gemini:
            try:
                self.gemini_client = GeminiClient()
                logger.info("Gemini AI integration enabled for ScalabilityAgent")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
                self.use_gemini = False
                self.gemini_client = None
        else:
            self.gemini_client = None
        
        self.anti_patterns = {
            "python": {
                "n_plus_one": [
                    r"for\s+\w+\s+in\s+.*:\s*\n\s+.*\.get\(",
                    r"for\s+\w+\s+in\s+.*:\s*\n\s+.*\.filter\("
                ],
                "blocking_io": [
                    r"requests\.(get|post|put|delete)\(",
                    r"urllib\.request\.",
                    r"time\.sleep\("
                ],
                "inefficient_loops": [
                    r"for\s+\w+\s+in\s+range\(len\(",
                    r"while.*len\("
                ],
                "missing_pagination": [
                    r"\.all\(\)",
                    r"SELECT\s+\*\s+FROM"
                ],
                "synchronous_should_be_async": [
                    r"def\s+\w+.*requests\.(get|post)",
                    r"def\s+\w+.*open\("
                ]
            }
        }
    async def analyze(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        import time
        start_time = time.time()
        project_dir = project_data.get("project_dir")
        language = project_data.get("language", "python")
        parsed_data = project_data.get("parsed_data", {})
        findings = []
        antipattern_findings = self._detect_antipatterns(project_dir, language)
        findings.extend(antipattern_findings)
        complexity_findings = self._analyze_complexity(parsed_data, project_dir)
        findings.extend(complexity_findings)
        async_findings = self._analyze_async_usage(project_dir, language)
        findings.extend(async_findings)
        caching_findings = self._identify_caching_opportunities(project_dir, language)
        findings.extend(caching_findings)
        duration = time.time() - start_time
        return {
            "status": "success",
            "agent": self.name,
            "findings_count": len(findings),
            "findings": findings,
            "scalability_score": self._calculate_scalability_score(findings),
            "duration_seconds": round(duration, 2)
        }
    def _detect_antipatterns(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        patterns = self.anti_patterns.get(language, {})
        for root, _, files in os.walk(project_dir):
            for file in files:
                if not file.endswith('.py'):
                    continue
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines = content.split('\n')
                        for pattern_name, pattern_list in patterns.items():
                            for pattern in pattern_list:
                                matches = re.finditer(pattern, content, re.MULTILINE)
                                for match in matches:
                                    line_num = content[:match.start()].count('\n') + 1
                                    findings.append(self.format_finding(
                                        severity=self._get_severity(pattern_name),
                                        title=f"Scalability Issue: {pattern_name.replace('_', ' ').title()}",
                                        description=self._get_description(pattern_name),
                                        file_path=str(file_path.relative_to(project_dir)),
                                        line_number=line_num,
                                        code_snippet=lines[line_num - 1].strip() if line_num <= len(lines) else "",
                                        recommendation=self._get_scalability_recommendation(pattern_name)
                                    ))
                except Exception as e:
                    logger.warning(f"Failed to analyze {file_path}: {str(e)}")
        return findings
    def _analyze_complexity(self, parsed_data: Dict[str, Any], project_dir: str) -> List[Dict[str, Any]]:
        findings = []
        for file_data in parsed_data.get("parsed_files", []):
            for func in file_data.get("functions", []):
                func_name = func.get("name")
                line_num = func.get("line")
                file_path = Path(project_dir) / file_data.get("file_path", "")
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            func_lines = lines[line_num:line_num + 50]
                            complexity = sum([
                                line.count('if '),
                                line.count('for '),
                                line.count('while '),
                                line.count('except '),
                                line.count('elif ')
                            ] for line in func_lines)
                            if complexity > 10:
                                findings.append(self.format_finding(
                                    severity="high" if complexity > 15 else "medium",
                                    title=f"High Complexity Function: {func_name}",
                                    description=f"Function has estimated complexity of {complexity}, which may impact maintainability and scalability",
                                    file_path=file_data.get("file_path", ""),
                                    line_number=line_num,
                                    recommendation="Consider breaking this function into smaller, more manageable functions"
                                ))
                    except Exception as e:
                        pass
        return findings
    def _analyze_async_usage(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        if language == "python":
            for root, _, files in os.walk(project_dir):
                for file in files:
                    if not file.endswith('.py'):
                        continue
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            for i, line in enumerate(lines, 1):
                                if 'async def' in line:
                                    func_lines = lines[i:i+20]
                                    for j, func_line in enumerate(func_lines):
                                        if 'requests.' in func_line and 'await' not in func_line:
                                            findings.append(self.format_finding(
                                                severity="high",
                                                title="Blocking Call in Async Function",
                                                description="Synchronous blocking call found in async function",
                                                file_path=str(file_path.relative_to(project_dir)),
                                                line_number=i + j,
                                                code_snippet=func_line.strip(),
                                                recommendation="Use async HTTP library (aiohttp, httpx) instead of requests"
                                            ))
                    except Exception as e:
                        pass
        return findings
    def _identify_caching_opportunities(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                if not file.endswith('.py'):
                    continue
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        func_pattern = r'def\s+(\w+)\s*\([^)]*\):'
                        matches = re.finditer(func_pattern, content)
                        for match in matches:
                            func_name = match.group(1)
                            func_start = match.start()
                            line_num = content[:func_start].count('\n') + 1
                            func_lines = lines[line_num:line_num + 30]
                            func_body = '\n'.join(func_lines)
                            has_external_call = any([
                                'requests.' in func_body,
                                '.query(' in func_body,
                                '.get(' in func_body and 'db' in func_body.lower(),
                                'SELECT' in func_body.upper()
                            ])
                            has_cache = any([
                                '@cache' in func_body,
                                '@lru_cache' in func_body,
                                'cache.' in func_body
                            ])
                            if has_external_call and not has_cache:
                                findings.append(self.format_finding(
                                    severity="medium",
                                    title=f"Caching Opportunity: {func_name}",
                                    description="Function makes external calls without caching",
                                    file_path=str(file_path.relative_to(project_dir)),
                                    line_number=line_num,
                                    recommendation="Consider adding caching decorator (@lru_cache or Redis caching)"
                                ))
                except Exception as e:
                    pass
        return findings
    def _get_severity(self, pattern_name: str) -> str:
        severity_map = {
            "n_plus_one": "critical",
            "blocking_io": "high",
            "inefficient_loops": "medium",
            "missing_pagination": "high",
            "synchronous_should_be_async": "high"
        }
        return severity_map.get(pattern_name, "medium")
    def _get_description(self, pattern_name: str) -> str:
        descriptions = {
            "n_plus_one": "N+1 query problem detected - executing queries in a loop causes exponential database load",
            "blocking_io": "Blocking I/O operation that can slow down server under load",
            "inefficient_loops": "Inefficient loop pattern detected",
            "missing_pagination": "Fetching all records without pagination can cause memory issues",
            "synchronous_should_be_async": "Synchronous function performing I/O should be async"
        }
        return descriptions.get(pattern_name, "Scalability issue detected")
    def _get_scalability_recommendation(self, pattern_name: str) -> str:
        recommendations = {
            "n_plus_one": "Use select_related() or prefetch_related() in Django, or joinedload() in SQLAlchemy to fetch related objects in a single query",
            "blocking_io": "Use async/await with async libraries (aiohttp, httpx) or run in background thread pool",
            "inefficient_loops": "Use list comprehensions or built-in functions like enumerate(), zip()",
            "missing_pagination": "Implement pagination with limit/offset or cursor-based pagination",
            "synchronous_should_be_async": "Convert to async function and use await for I/O operations"
        }
        return recommendations.get(pattern_name, "Review and optimize this code pattern")
    def _calculate_scalability_score(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_findings = len(findings)
        critical_count = sum(1 for f in findings if f.get("severity") == "CRITICAL")
        high_count = sum(1 for f in findings if f.get("severity") == "HIGH")
        score = 100
        score -= critical_count * 15
        score -= high_count * 10
        score -= (total_findings - critical_count - high_count) * 5
        score = max(0, score)
        rating = "Excellent" if score >= 90 else "Good" if score >= 70 else "Fair" if score >= 50 else "Poor"
        return {
            "score": score,
            "rating": rating,
            "critical_issues": critical_count,
            "high_issues": high_count,
            "total_issues": total_findings
        }
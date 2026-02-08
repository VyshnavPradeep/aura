import os
import subprocess
import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from agents.base_agent import BaseAgent
from core.gemini_client import GeminiClient, AnalysisType
import logging
logger = logging.getLogger(__name__)
class SecurityAgent(BaseAgent):
    def __init__(self, use_gemini: bool = True, use_rag: bool = True):
        super().__init__(
            name="SecurityAgent",
            description="AI-powered security vulnerability detection with RAG + Gemini"
        )
        self.semgrep_available = self._check_semgrep()
        self.use_gemini = use_gemini
        self.use_rag = use_rag
        if self.use_gemini:
            try:
                self.gemini_client = GeminiClient()
                logger.info("Gemini AI integration enabled for SecurityAgent")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
                self.use_gemini = False
                self.gemini_client = None
        else:
            self.gemini_client = None
        self.security_patterns = {
            "python": {
                "sql_injection": [
                    r"execute\s*\([^)]*%",
                    r"execute\s*\([^)]*\+",
                    r"\.format\s*\(",
                    r"f['\"].*{.*}.*['\"]"
                ],
                "hardcoded_secrets": [
                    r"password\s*=\s*['\"][^'\"]+['\"]",
                    r"api_key\s*=\s*['\"][^'\"]+['\"]",
                    r"secret\s*=\s*['\"][^'\"]+['\"]",
                    r"token\s*=\s*['\"][^'\"]+['\"]"
                ],
                "unsafe_deserialization": [
                    r"pickle\.loads",
                    r"yaml\.load\s*\([^,)]*\)",
                    r"eval\s*\(",
                    r"exec\s*\("
                ],
                "path_traversal": [
                    r"open\s*\([^)]*\+",
                    r"os\.path\.join\s*\([^)]*input",
                    r"\.\./"
                ]
            },
            "javascript": {
                "xss": [
                    r"innerHTML\s*=",
                    r"document\.write\s*\(",
                    r"eval\s*\("
                ],
                "sql_injection": [
                    r"query\s*\([^)]*\+",
                    r"\.query\s*\([^)]*`.*\${",
                ]
            }
        }
    def _check_semgrep(self) -> bool:
        try:
            subprocess.run(["semgrep", "--version"], capture_output=True, timeout=5)
            return True
        except:
            return False
    async def analyze(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        import time
        start_time = time.time()
        project_dir = project_data.get("project_dir")
        language = project_data.get("language", "python")
        project_id = project_data.get("project_id")
        findings = []
        logger.info(f"[{self.name}] Phase 1: Running fast security scans...")
        pattern_findings = self._pattern_based_scan(project_dir, language)
        findings.extend(pattern_findings)
        # Initialize semgrep_findings before conditional use
        semgrep_findings = []
        if self.semgrep_available:
            semgrep_findings = self._semgrep_scan(project_dir, language)
            findings.extend(semgrep_findings)
        dependency_findings = self._check_dependencies(project_dir, language)
        findings.extend(dependency_findings)
        auth_findings = self._check_auth_issues(project_dir, language)
        findings.extend(auth_findings)
        rag_findings = []
        if self.use_rag and project_id:
            logger.info(f"[{self.name}] Phase 2: RAG-based vulnerability search...")
            rag_findings = await self._rag_vulnerability_search(project_id, project_dir)
            findings.extend(rag_findings)
        gemini_findings = []
        if self.use_gemini and self.gemini_client:
            logger.info(f"[{self.name}] Phase 3: Deep AI analysis with Gemini...")
            gemini_findings = await self._gemini_deep_analysis(
                project_dir,
                language,
                project_id,
                high_risk_files=self._get_high_risk_files(findings)
            )
            findings.extend(gemini_findings)
        findings = self._deduplicate_findings(findings)
        findings = self._prioritize_findings(findings)
        duration = time.time() - start_time
        return {
            "status": "success",
            "agent": self.name,
            "findings_count": len(findings),
            "findings": findings,
            "scan_methods": {
                "pattern_based": True,
                "semgrep": self.semgrep_available,
                "dependency_check": True,
                "auth_check": True,
                "rag_search": self.use_rag and len(rag_findings) > 0,
                "gemini_analysis": self.use_gemini and len(gemini_findings) > 0
            },
            "analysis_breakdown": {
                "fast_scans": len(pattern_findings) + len(semgrep_findings) + len(dependency_findings) + len(auth_findings),
                "rag_findings": len(rag_findings),
                "gemini_findings": len(gemini_findings)
            },
            "duration_seconds": round(duration, 2)
        }
    def _pattern_based_scan(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        patterns = self.security_patterns.get(language, {})
        if not patterns:
            return findings
        code_extensions = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts"
        }
        ext = code_extensions.get(language, ".py")
        for root, _, files in os.walk(project_dir):
            for file in files:
                if not file.endswith(ext):
                    continue
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line_num, line in enumerate(lines, 1):
                            for vuln_type, pattern_list in patterns.items():
                                import re
                                for pattern in pattern_list:
                                    if re.search(pattern, line, re.IGNORECASE):
                                        findings.append(self.format_finding(
                                            severity="high" if vuln_type in ["sql_injection", "xss", "unsafe_deserialization"] else "medium",
                                            title=f"Potential {vuln_type.replace('_', ' ').title()}",
                                            description=f"Detected potential {vuln_type} vulnerability pattern",
                                            file_path=str(file_path.relative_to(project_dir)),
                                            line_number=line_num,
                                            code_snippet=line.strip(),
                                            recommendation=self._get_recommendation(vuln_type, language)
                                        ))
                except Exception as e:
                    logger.warning(f"Failed to scan {file_path}: {str(e)}")
        return findings
    def _semgrep_scan(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        try:
            result = subprocess.run(
                ["semgrep", "--config=auto", "--json", project_dir],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0 or result.returncode == 1:
                try:
                    semgrep_output = json.loads(result.stdout)
                    for result in semgrep_output.get("results", []):
                        findings.append(self.format_finding(
                            severity=self._map_semgrep_severity(result.get("extra", {}).get("severity", "WARNING")),
                            title=result.get("check_id", "Security Issue"),
                            description=result.get("extra", {}).get("message", "Security vulnerability detected"),
                            file_path=result.get("path", ""),
                            line_number=result.get("start", {}).get("line", 0),
                            code_snippet=result.get("extra", {}).get("lines", ""),
                            recommendation="Review and fix according to security best practices"
                        ))
                except json.JSONDecodeError:
                    logger.warning("Failed to parse Semgrep output")
        except subprocess.TimeoutExpired:
            logger.warning("Semgrep scan timed out")
        except Exception as e:
            logger.error(f"Semgrep scan failed: {str(e)}")
        return findings
    def _check_dependencies(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        if language == "python":
            req_file = Path(project_dir) / "requirements.txt"
            if req_file.exists():
                with open(req_file, 'r') as f:
                    dependencies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                vulnerable_packages = {
                    "django<2.2": "Upgrade Django to 2.2 or higher",
                    "flask<1.0": "Upgrade Flask to 1.0 or higher",
                    "requests<2.20": "Upgrade requests to 2.20+ for security fixes"
                }
                for dep in dependencies:
                    dep_lower = dep.lower()
                    for vuln_pkg, recommendation in vulnerable_packages.items():
                        if vuln_pkg.split('<')[0] in dep_lower:
                            findings.append(self.format_finding(
                                severity="high",
                                title="Vulnerable Dependency Detected",
                                description=f"Dependency '{dep}' may have known vulnerabilities",
                                file_path="requirements.txt",
                                recommendation=recommendation
                            ))
        return findings
    def _check_auth_issues(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        if language == "python":
            for root, _, files in os.walk(project_dir):
                for file in files:
                    if not file.endswith('.py'):
                        continue
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            lines = content.split('\n')
                            for i, line in enumerate(lines, 1):
                                if '@app.post' in line or '@app.get' in line or '@router.post' in line or '@router.get' in line:
                                    prev_lines = '\n'.join(lines[max(0, i-5):i])
                                    if 'auth' not in prev_lines.lower() and 'login' not in prev_lines.lower():
                                        findings.append(self.format_finding(
                                            severity="medium",
                                            title="Endpoint Without Authentication",
                                            description="API endpoint may be missing authentication check",
                                            file_path=str(file_path.relative_to(project_dir)),
                                            line_number=i,
                                            code_snippet=line.strip(),
                                            recommendation="Add authentication decorator or middleware to protect this endpoint"
                                        ))
                    except Exception as e:
                        pass
        return findings
    def _get_recommendation(self, vuln_type: str, language: str) -> str:
        recommendations = {
            "sql_injection": "Use parameterized queries or ORMs. Never concatenate user input into SQL queries.",
            "xss": "Sanitize user input and use proper output encoding. Consider using frameworks with auto-escaping.",
            "hardcoded_secrets": "Move secrets to environment variables or a secure vault (e.g., AWS Secrets Manager, HashiCorp Vault).",
            "unsafe_deserialization": "Avoid deserializing untrusted data. Use safe serialization formats like JSON.",
            "path_traversal": "Validate and sanitize file paths. Use whitelisting for allowed paths.",
            "csrf": "Implement CSRF tokens for state-changing operations.",
            "weak_crypto": "Use strong, modern cryptographic algorithms (e.g., AES-256, bcrypt for passwords)."
        }
        return recommendations.get(vuln_type, "Review and fix according to OWASP security guidelines.")
    def _map_semgrep_severity(self, severity: str) -> str:
        mapping = {
            "ERROR": "critical",
            "WARNING": "high",
            "INFO": "medium"
        }
        return mapping.get(severity, "medium")
    async def _rag_vulnerability_search(self, project_id: str, project_dir: str) -> List[Dict[str, Any]]:
        findings = []
        try:
            security_queries = [
                "SQL injection vulnerability execute query concatenation",
                "XSS cross-site scripting innerHTML document.write",
                "hardcoded password API key secret token credentials",
                "authentication bypass missing auth check decorator",
                "insecure cryptography weak encryption MD5 SHA1",
                "path traversal file inclusion user input path",
                "unsafe deserialization pickle eval exec",
                "CSRF cross-site request forgery missing token"
            ]
            for query in security_queries:
                results = await self.search_code(
                    project_id=project_id,
                    query=query,
                    top_k=3,
                    use_reranking=True
                )
                if results.get("success") and results.get("results"):
                    for result in results["results"][:2]:
                        vuln_type = query.split()[0].lower()
                        findings.append(self.format_finding(
                            severity="high",
                            title=f"RAG-Detected: Potential {vuln_type.title()} Vulnerability",
                            description=f"RAG system found code similar to known {vuln_type} patterns. Score: {result.get('score', 0):.2f}",
                            file_path=result.get("metadata", {}).get("file_path", "unknown"),
                            line_number=result.get("metadata", {}).get("start_line"),
                            code_snippet=result.get("text", "")[:200],
                            recommendation=f"Review this code for {vuln_type} vulnerabilities. Similar patterns detected in security knowledge base.",
                            metadata={
                                "detection_method": "rag_similarity",
                                "similarity_score": result.get("score"),
                                "query": query
                            }
                        ))
            logger.info(f"[{self.name}] RAG search found {len(findings)} potential vulnerabilities")
        except Exception as e:
            logger.error(f"[{self.name}] RAG vulnerability search failed: {e}")
        return findings
    async def _gemini_deep_analysis(
        self,
        project_dir: str,
        language: str,
        project_id: Optional[str],
        high_risk_files: List[str] = None
    ) -> List[Dict[str, Any]]:
        findings = []
        if not high_risk_files:
            high_risk_files = self._identify_high_risk_files(project_dir, language)
        high_risk_files = high_risk_files[:5]
        try:
            for file_path in high_risk_files:
                full_path = Path(project_dir) / file_path
                if not full_path.exists():
                    continue
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    rag_context = ""
                    if project_id:
                        rag_results = await self.search_code(
                            project_id=project_id,
                            query=f"security vulnerability in {file_path}",
                            top_k=3
                        )
                        if rag_results.get("success"):
                            rag_context = "\n\n".join([
                                f"Similar code: {r.get('text', '')[:300]}"
                                for r in rag_results.get("results", [])
                            ])
                    logger.info(f"[{self.name}] Gemini analyzing: {file_path}")
                    analysis_result = await self.gemini_client.analyze_security(
                        code=code,
                        rag_context=rag_context,
                        language=language
                    )
                    if analysis_result.get("success"):
                        result = analysis_result.get("result", {})
                        for vuln in result.get("vulnerabilities", []):
                            findings.append(self.format_finding(
                                severity=vuln.get("severity", "high").lower(),
                                title=f"Gemini AI: {vuln.get('title', 'Security Vulnerability')}",
                                description=vuln.get("description", "Security issue detected by AI analysis"),
                                file_path=file_path,
                                line_number=self._extract_line_number(vuln.get("location", "")),
                                code_snippet=vuln.get("vulnerable_code", "")[:200],
                                recommendation=vuln.get("fix", "Review and apply security best practices"),
                                metadata={
                                    "detection_method": "gemini_ai",
                                    "cwe_id": vuln.get("cwe_id"),
                                    "exploitation": vuln.get("exploitation", ""),
                                    "security_score": result.get("security_score"),
                                    "owasp_category": self._map_to_owasp(vuln.get("cwe_id"))
                                }
                            ))
                        logger.info(f"[{self.name}] Gemini found {len(result.get('vulnerabilities', []))} vulnerabilities in {file_path}")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.error(f"[{self.name}] Failed to analyze {file_path} with Gemini: {e}")
        except Exception as e:
            logger.error(f"[{self.name}] Gemini deep analysis failed: {e}")
        return findings
    def _get_high_risk_files(self, findings: List[Dict[str, Any]]) -> List[str]:
        file_risk_scores = {}
        for finding in findings:
            file_path = finding.get("file_path")
            if not file_path:
                continue
            severity = finding.get("severity", "low")
            severity_score = {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(severity, 1)
            file_risk_scores[file_path] = file_risk_scores.get(file_path, 0) + severity_score
        sorted_files = sorted(file_risk_scores.items(), key=lambda x: x[1], reverse=True)
        return [f[0] for f in sorted_files[:10]]
    def _identify_high_risk_files(self, project_dir: str, language: str) -> List[str]:
        high_risk_patterns = {
            "python": ["*auth*", "*login*", "*api*", "*admin*", "*db*", "*query*", "*password*"],
            "javascript": ["*auth*", "*login*", "*api*", "*admin*", "*db*", "*route*"],
            "java": ["*Auth*", "*Login*", "*Controller*", "*Service*", "*Security*"]
        }
        patterns = high_risk_patterns.get(language, ["*auth*", "*api*"])
        high_risk_files = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                file_lower = file.lower()
                if any(pattern.strip('*') in file_lower for pattern in patterns):
                    rel_path = str(Path(root) / file)
                    high_risk_files.append(rel_path.replace(project_dir, "").lstrip(os.sep))
        return high_risk_files[:10]
    def _deduplicate_findings(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        unique_findings = []
        for finding in findings:
            key = (
                finding.get("file_path", ""),
                finding.get("line_number", 0),
                finding.get("title", "")[:50]
            )
            if key not in seen:
                seen.add(key)
                unique_findings.append(finding)
        return unique_findings
    def _prioritize_findings(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        return sorted(
            findings,
            key=lambda x: (
                severity_order.get(x.get("severity", "low"), 5),
                -x.get("metadata", {}).get("similarity_score", 0)
            )
        )
    def _extract_line_number(self, location: str) -> Optional[int]:
        import re
        match = re.search(r'line\s+(\d+)', location.lower())
        if match:
            return int(match.group(1))
        return None
    def _map_to_owasp(self, cwe_id: Optional[str]) -> Optional[str]:
        if not cwe_id:
            return None
        owasp_mapping = {
            "CWE-89": "A03:2021-Injection",
            "CWE-79": "A03:2021-Injection",
            "CWE-78": "A03:2021-Injection",
            "CWE-22": "A01:2021-Broken Access Control",
            "CWE-352": "A01:2021-Broken Access Control",
            "CWE-306": "A07:2021-Identification and Authentication Failures",
            "CWE-287": "A07:2021-Identification and Authentication Failures",
            "CWE-798": "A07:2021-Identification and Authentication Failures",
            "CWE-327": "A02:2021-Cryptographic Failures",
            "CWE-326": "A02:2021-Cryptographic Failures",
            "CWE-502": "A08:2021-Software and Data Integrity Failures",
            "CWE-918": "A10:2021-Server-Side Request Forgery",
        }
        return owasp_mapping.get(cwe_id)

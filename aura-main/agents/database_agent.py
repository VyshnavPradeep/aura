import os
import re
from typing import Dict, Any, List
from pathlib import Path
from agents.base_agent import BaseAgent
from core.gemini_client import GeminiClient, AnalysisType
import logging
logger = logging.getLogger(__name__)
class DatabaseAgent(BaseAgent):
    def __init__(self, use_gemini: bool = True):
        super().__init__(
            name="DatabaseAgent",
            description="AI-powered database optimization with Gemini for query and schema analysis"
        )
        self.use_gemini = use_gemini
        
        if self.use_gemini:
            try:
                self.gemini_client = GeminiClient()
                logger.info("Gemini AI integration enabled for DatabaseAgent")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
                self.use_gemini = False
                self.gemini_client = None
        else:
            self.gemini_client = None
        
        self.query_patterns = {
            "select_star": r"SELECT\s+\*\s+FROM",
            "no_where": r"SELECT\s+.*\s+FROM\s+\w+(?!\s+WHERE)",
            "like_prefix": r"LIKE\s+['\"]%",
            "or_in_where": r"WHERE\s+.*\s+OR\s+",
            "subquery_in_select": r"SELECT\s+.*\(\s*SELECT",
            "missing_limit": r"SELECT\s+.*\s+FROM(?!.*LIMIT)",
            "distinct_abuse": r"SELECT\s+DISTINCT\s+\*"
        }
    async def analyze(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        import time
        start_time = time.time()
        project_dir = project_data.get("project_dir")
        language = project_data.get("language", "python")
        findings = []
        query_findings = self._analyze_queries(project_dir, language)
        findings.extend(query_findings)
        orm_findings = self._analyze_orm_usage(project_dir, language)
        findings.extend(orm_findings)
        schema_findings = self._analyze_schema(project_dir, language)
        findings.extend(schema_findings)
        connection_findings = self._check_connection_management(project_dir, language)
        findings.extend(connection_findings)
        transaction_findings = self._analyze_transactions(project_dir, language)
        findings.extend(transaction_findings)
        duration = time.time() - start_time
        return {
            "status": "success",
            "agent": self.name,
            "findings_count": len(findings),
            "findings": findings,
            "database_health": self._calculate_db_health(findings),
            "duration_seconds": round(duration, 2)
        }
    def _analyze_queries(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                if not file.endswith('.py') and not file.endswith('.sql'):
                    continue
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines = content.split('\n')
                        for pattern_name, pattern in self.query_patterns.items():
                            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                            for match in matches:
                                line_num = content[:match.start()].count('\n') + 1
                                findings.append(self.format_finding(
                                    severity=self._get_query_severity(pattern_name),
                                    title=f"Query Issue: {pattern_name.replace('_', ' ').title()}",
                                    description=self._get_query_description(pattern_name),
                                    file_path=str(file_path.relative_to(project_dir)),
                                    line_number=line_num,
                                    code_snippet=lines[line_num - 1].strip() if line_num <= len(lines) else "",
                                    recommendation=self._get_query_recommendation(pattern_name)
                                ))
                except Exception as e:
                    logger.warning(f"Failed to analyze {file_path}: {str(e)}")
        return findings
    def _analyze_orm_usage(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
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
                            n_plus_one_pattern = r'for\s+\w+\s+in\s+.*\.all\(\).*:\s*\n\s+.*\.\w+\.all\(\)'
                            if re.search(n_plus_one_pattern, content, re.MULTILINE):
                                line_num = content.find('for')
                                findings.append(self.format_finding(
                                    severity="critical",
                                    title="N+1 Query Problem",
                                    description="Potential N+1 query detected - fetching related objects in a loop",
                                    file_path=str(file_path.relative_to(project_dir)),
                                    recommendation="Use select_related() or prefetch_related() for Django, or eager loading in SQLAlchemy"
                                ))
                            if '.all()' in content:
                                for i, line in enumerate(lines, 1):
                                    if '.all()' in line and 'paginate' not in content[max(0, content.index(line)-200):content.index(line)+200]:
                                        findings.append(self.format_finding(
                                            severity="high",
                                            title="Missing Pagination",
                                            description="Fetching all records without pagination",
                                            file_path=str(file_path.relative_to(project_dir)),
                                            line_number=i,
                                            code_snippet=line.strip(),
                                            recommendation="Implement pagination to limit result set size"
                                        ))
                                        break
                    except Exception as e:
                        pass
        return findings
    def _analyze_schema(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        model_files = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                if 'model' in file.lower() or 'schema' in file.lower():
                    model_files.append(Path(root) / file)
        for model_file in model_files:
            try:
                with open(model_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    if 'class ' in content and ('Model' in content or 'Table' in content):
                        for i, line in enumerate(lines, 1):
                            if 'class ' in line:
                                class_block = '\n'.join(lines[i:i+30])
                                has_fk = 'ForeignKey' in class_block or 'foreign_key' in class_block
                                has_index = 'index=' in class_block or 'Index(' in class_block or 'db_index' in class_block
                                if has_fk and not has_index:
                                    findings.append(self.format_finding(
                                        severity="high",
                                        title="Missing Index on Foreign Key",
                                        description="Foreign key column without explicit index",
                                        file_path=str(model_file.relative_to(project_dir)),
                                        line_number=i,
                                        recommendation="Add database index on foreign key columns for better join performance"
                                    ))
            except Exception as e:
                pass
        return findings
    def _check_connection_management(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
        findings = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                if not file.endswith('.py'):
                    continue
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        has_db_connect = any([
                            'psycopg2.connect' in content,
                            'pymysql.connect' in content,
                            'sqlite3.connect' in content,
                            'create_engine' in content
                        ])
                        has_pooling = any([
                            'pool' in content.lower(),
                            'QueuePool' in content,
                            'max_connections' in content
                        ])
                        if has_db_connect and not has_pooling:
                            findings.append(self.format_finding(
                                severity="medium",
                                title="No Connection Pooling Detected",
                                description="Database connections without pooling can lead to performance issues",
                                file_path=str(file_path.relative_to(project_dir)),
                                recommendation="Implement connection pooling using SQLAlchemy engine or connection pool library"
                            ))
                        if '.connect(' in content and 'close()' not in content:
                            findings.append(self.format_finding(
                                severity="high",
                                title="Potential Connection Leak",
                                description="Database connection may not be properly closed",
                                file_path=str(file_path.relative_to(project_dir)),
                                recommendation="Use context managers (with statement) to ensure connections are closed"
                            ))
                except Exception as e:
                    pass
        return findings
    def _analyze_transactions(self, project_dir: str, language: str) -> List[Dict[str, Any]]:
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
                        write_ops = ['INSERT', 'UPDATE', 'DELETE', '.save()', '.update()', '.delete()']
                        for i, line in enumerate(lines):
                            write_count = sum(1 for op in write_ops if op in line or op.lower() in line.lower())
                            if write_count > 1:
                                context = '\n'.join(lines[max(0, i-5):i+5])
                                has_transaction = any([
                                    'transaction' in context.lower(),
                                    'BEGIN' in context,
                                    'COMMIT' in context,
                                    'atomic' in context
                                ])
                                if not has_transaction:
                                    findings.append(self.format_finding(
                                        severity="medium",
                                        title="Multiple Writes Without Transaction",
                                        description="Multiple database write operations should be wrapped in a transaction",
                                        file_path=str(file_path.relative_to(project_dir)),
                                        line_number=i + 1,
                                        recommendation="Use database transactions to ensure data consistency"
                                    ))
                                    break
                except Exception as e:
                    pass
        return findings
    def _get_query_severity(self, pattern_name: str) -> str:
        severity_map = {
            "select_star": "medium",
            "no_where": "high",
            "like_prefix": "high",
            "or_in_where": "medium",
            "subquery_in_select": "high",
            "missing_limit": "high",
            "distinct_abuse": "medium"
        }
        return severity_map.get(pattern_name, "medium")
    def _get_query_description(self, pattern_name: str) -> str:
        descriptions = {
            "select_star": "SELECT * retrieves all columns, potentially fetching unnecessary data",
            "no_where": "Query without WHERE clause may fetch entire table",
            "like_prefix": "LIKE with leading wildcard prevents index usage",
            "or_in_where": "OR conditions in WHERE clause can prevent index usage",
            "subquery_in_select": "Subquery in SELECT list executes for each row",
            "missing_limit": "Query without LIMIT can return too many rows",
            "distinct_abuse": "DISTINCT * is often inefficient, specify columns instead"
        }
        return descriptions.get(pattern_name, "Query optimization opportunity")
    def _get_query_recommendation(self, pattern_name: str) -> str:
        recommendations = {
            "select_star": "Select only the columns you need",
            "no_where": "Add WHERE clause to filter results, or use LIMIT",
            "like_prefix": "Avoid leading wildcards in LIKE patterns, consider full-text search",
            "or_in_where": "Consider using IN clause or UNION instead of OR",
            "subquery_in_select": "Move subquery to JOIN or CTE",
            "missing_limit": "Add LIMIT clause to prevent fetching too many rows",
            "distinct_abuse": "Specify distinct columns or fix data model to avoid duplicates"
        }
        return recommendations.get(pattern_name, "Optimize this query pattern")
    def _calculate_db_health(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        critical_count = sum(1 for f in findings if f.get("severity") == "CRITICAL")
        high_count = sum(1 for f in findings if f.get("severity") == "HIGH")
        score = 100 - (critical_count * 20) - (high_count * 10) - (len(findings) * 3)
        score = max(0, score)
        health = "Excellent" if score >= 90 else "Good" if score >= 70 else "Fair" if score >= 50 else "Poor"
        return {
            "score": score,
            "health": health,
            "critical_issues": critical_count,
            "high_issues": high_count,
            "recommendations": [
                "Add indexes on frequently queried columns",
                "Implement connection pooling",
                "Use pagination for large result sets",
                "Optimize N+1 queries with eager loading"
            ]
        }
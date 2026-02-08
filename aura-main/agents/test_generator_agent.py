import os
from typing import Dict, Any, List
from pathlib import Path
from agents.base_agent import BaseAgent
from core.gemini_client import GeminiClient
import logging
logger = logging.getLogger(__name__)
class TestGeneratorAgent(BaseAgent):
    def __init__(self, use_gemini: bool = True):
        super().__init__(
            name="TestGeneratorAgent",
            description="AI-powered test generation with Gemini for comprehensive test coverage"
        )
        self.use_gemini = use_gemini
        
        if self.use_gemini:
            try:
                self.gemini_client = GeminiClient()
                logger.info("Gemini AI integration enabled for TestGeneratorAgent")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
                self.use_gemini = False
                self.gemini_client = None
        else:
            self.gemini_client = None
    async def analyze(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        import time
        start_time = time.time()
        project_dir = project_data.get("project_dir")
        language = project_data.get("language", "python")
        parsed_data = project_data.get("parsed_data", {})
        findings = []
        generated_tests = []
        coverage_findings = self._analyze_test_coverage(project_dir, parsed_data)
        findings.extend(coverage_findings)
        if language == "python":
            generated_tests = self._generate_python_tests(parsed_data, project_dir)
        elif language in ["javascript", "typescript"]:
            generated_tests = self._generate_js_tests(parsed_data, project_dir)
        for test in generated_tests:
            findings.append(self.format_finding(
                severity="medium",
                title=f"Missing Test: {test['function_name']}",
                description=f"Function '{test['function_name']}' has no test coverage",
                file_path=test['source_file'],
                line_number=test.get('line_number'),
                recommendation="Add unit test to improve coverage"
            ))
        duration = time.time() - start_time
        return {
            "status": "success",
            "agent": self.name,
            "findings_count": len(findings),
            "findings": findings,
            "generated_tests": generated_tests[:5],
            "test_generation_count": len(generated_tests),
            "coverage_analysis": {
                "total_functions": parsed_data.get("total_functions", 0),
                "tested_functions": 0,
                "coverage_percentage": 0
            },
            "duration_seconds": round(duration, 2)
        }
    def _analyze_test_coverage(self, project_dir: str, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        test_dirs = ["tests", "test", "__tests__", "spec"]
        has_tests = False
        
        for test_dir in test_dirs:
            test_path = Path(project_dir) / test_dir
            if test_path.exists():
                has_tests = True
                break
        
        if not has_tests:
            findings.append(self.format_finding(
                severity="high",
                title="No Test Directory Found",
                description="Project does not have a dedicated test directory",
                recommendation="Create a 'tests/' directory and add test files"
            ))
        
        # Count total functions from parsed data
        total_functions = parsed_data.get("total_functions", 0)
        
        # If we don't have total_functions, count from parsed_files
        if total_functions == 0:
            for file_data in parsed_data.get("parsed_files", []):
                total_functions += len(file_data.get("functions", []))
        
        # Report missing tests if we have functions but no tests
        if total_functions > 0 and not has_tests:
            findings.append(self.format_finding(
                severity="high",
                title="Low Test Coverage",
                description=f"Found {total_functions} functions but no test files",
                recommendation="Implement unit tests for critical functions"
            ))
        
        return findings
    def _generate_python_tests(self, parsed_data: Dict[str, Any], project_dir: str) -> List[Dict[str, Any]]:
        generated_tests = []
        for file_data in parsed_data.get("parsed_files", []):
            file_path = file_data.get("file_path", "")
            if "test" in file_path.lower():
                continue
            for func in file_data.get("functions", []):
                func_name = func.get("name")
                if func_name.startswith("_"):
                    continue
                test_code = self._create_pytest_template(
                    func_name,
                    func.get("args", []),
                    file_path
                )
                generated_tests.append({
                    "function_name": func_name,
                    "source_file": file_path,
                    "line_number": func.get("line"),
                    "test_file": f"tests/test_{Path(file_path).stem}.py",
                    "test_code": test_code,
                    "test_type": "unit"
                })
        api_tests = self._generate_api_tests(parsed_data, project_dir)
        generated_tests.extend(api_tests)
        
        return generated_tests
    
    def _generate_test_args(self, args: List[str]) -> str:
        """Generate test argument assignments for function parameters"""
        if not args:
            return "# No arguments needed"
        
        arg_assignments = []
        for arg in args:
            # Skip 'self' and 'cls' parameters
            if arg in ['self', 'cls']:
                continue
            # Generate simple test values based on common parameter names
            if 'id' in arg.lower():
                arg_assignments.append(f"{arg} = 1")
            elif 'name' in arg.lower() or 'str' in arg.lower():
                arg_assignments.append(f"{arg} = 'test'")
            elif 'count' in arg.lower() or 'num' in arg.lower():
                arg_assignments.append(f"{arg} = 10")
            elif 'flag' in arg.lower() or 'is_' in arg.lower():
                arg_assignments.append(f"{arg} = True")
            else:
                arg_assignments.append(f"{arg} = None")
        
        return "\n    ".join(arg_assignments) if arg_assignments else "# No arguments needed"
    
    def _create_pytest_template(self, func_name: str, args: List[str], source_file: str) -> str:
        module_name = Path(source_file).stem
        template = f'''import pytest
from {module_name} import {func_name}

def test_{func_name}_basic():
    {self._generate_test_args(args)}
    result = {func_name}({", ".join(args)})
    assert result is not None

def test_{func_name}_edge_cases():
    pass

def test_{func_name}_error_handling():
    with pytest.raises(Exception):
        {func_name}(invalid_input)
'''
        return template
    
    def _generate_api_tests(self, parsed_data: Dict[str, Any], project_dir: str) -> List[Dict[str, Any]]:
        """Generate API endpoint tests for Flask/FastAPI routes"""
        api_tests = []
        
        # Look for API route decorators in parsed files
        for file_data in parsed_data.get("parsed_files", []):
            file_path = file_data.get("file_path", "")
            
            # Check if file contains API routes
            if any(keyword in file_path.lower() for keyword in ["route", "api", "endpoint", "view"]):
                for func in file_data.get("functions", []):
                    func_name = func.get("name")
                    
                    # Generate API test for this endpoint
                    api_tests.append({
                        "function_name": func_name,
                        "source_file": file_path,
                        "line_number": func.get("line"),
                        "test_file": f"tests/test_api_{Path(file_path).stem}.py",
                        "test_code": self._create_api_test_template(func_name, file_path),
                        "test_type": "api"
                    })
        
        return api_tests
    
    def _create_api_test_template(self, endpoint_name: str, source_file: str) -> str:
        """Create API test template"""
        template = f'''import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_{endpoint_name}_success():
    response = client.get("/api/endpoint")
    assert response.status_code == 200

def test_{endpoint_name}_validation():
    response = client.post("/api/endpoint", json={{}})
    assert response.status_code in [200, 400, 422]
'''
        return template
    
    def _generate_js_tests(self, parsed_data: Dict[str, Any], project_dir: str) -> List[Dict[str, Any]]:
        """Generate JavaScript/TypeScript tests"""
        # Placeholder for JS test generation
        return []
"""
Gemini 3 API Client for code analysis
Supports security analysis, test generation, scalability assessment, and database optimization
"""

import os
import logging
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class AnalysisType(Enum):
    """Types of code analysis supported by Gemini"""
    SECURITY = "security"
    TESTING = "testing"
    SCALABILITY = "scalability"
    DATABASE = "database"
    CODE_REVIEW = "code_review"
    ARCHITECTURE = "architecture"


class GeminiClient:

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-flash-latest",
        temperature: float = 0.3,
        max_tokens: int = 8000
    ):
       
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY environment variable or pass api_key parameter.\n"
                "Get a free API key at: https://aistudio.google.com/app/apikey"
            )
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Gemini API client"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            
            # Configure safety settings for code analysis
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            # Configure generation settings
            generation_config = {
                "temperature": self.temperature,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": self.max_tokens,
            }
            
            self.client = genai.GenerativeModel(
                model_name=self.model_name,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            
            logger.info(f"Gemini client initialized with model: {self.model_name}")
            
        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. "
                "Install with: pip install google-generativeai"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            raise
    
    async def analyze_security(
        self,
        code: str,
        file_path: str,
        language: str = "python",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
      
        prompt = f"""You are an expert security auditor. Analyze this {language} code for security vulnerabilities.

File: {file_path}

{f"Context: {context}" if context else ""}

Code:
```{language}
{code}
```

Identify:
1. SQL Injection risks
2. XSS vulnerabilities
3. Authentication/Authorization issues
4. Hardcoded secrets or credentials
5. Path traversal vulnerabilities
6. Unsafe deserialization
7. Command injection risks
8. CSRF vulnerabilities
9. Insecure cryptography
10. Other security issues

For each vulnerability found, provide:
- Severity (CRITICAL, HIGH, MEDIUM, LOW)
- Line numbers (estimate if needed)
- Description of the issue
- Potential exploit scenario
- Recommended fix

Return your analysis in JSON format:
{{
  "vulnerabilities": [
    {{
      "severity": "HIGH",
      "line": 15,
      "title": "SQL Injection",
      "description": "User input directly concatenated into SQL query",
      "exploit": "Attacker could inject malicious SQL",
      "recommendation": "Use parameterized queries or ORM"
    }}
  ],
  "risk_score": 75,
  "summary": "Brief overview of security posture"
}}
"""
        
        return await self._call_api(prompt, AnalysisType.SECURITY)
    
    async def generate_tests(
        self,
        code: str,
        file_path: str,
        language: str = "python",
        test_framework: str = "pytest"
    ) -> Dict[str, Any]:
        """
        Generate test cases for the provided code
        
        Args:
            code: Source code to generate tests for
            file_path: Path to the file
            language: Programming language
            test_framework: Testing framework (pytest, jest, junit, etc.)
        
        Returns:
            Dict with generated test code
        """
        prompt = f"""You are an expert test engineer. Generate comprehensive test cases for this {language} code.

File: {file_path}
Framework: {test_framework}

Code:
```{language}
{code}
```

Generate tests that cover:
1. Happy path scenarios
2. Edge cases
3. Error handling
4. Boundary conditions
5. Integration points

Return in JSON format:
{{
  "test_code": "complete test file content",
  "test_cases": [
    {{
      "name": "test_function_name",
      "description": "what it tests",
      "coverage_type": "happy_path|edge_case|error"
    }}
  ],
  "coverage_estimate": 85,
  "additional_scenarios": ["scenario1", "scenario2"]
}}
"""
        
        return await self._call_api(prompt, AnalysisType.TESTING)
    
    async def analyze_scalability(
        self,
        code: str,
        file_path: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Analyze code for scalability issues
        
        Args:
            code: Source code to analyze
            file_path: Path to the file
            language: Programming language
        
        Returns:
            Dict with scalability findings
        """
        prompt = f"""You are a performance optimization expert. Analyze this {language} code for scalability bottlenecks.

File: {file_path}

Code:
```{language}
{code}
```

Identify:
1. N+1 query problems
2. Blocking I/O operations
3. Inefficient algorithms (O(n²) or worse)
4. Missing caching opportunities
5. Synchronous operations that should be async
6. Missing pagination/limiting
7. Memory leaks or excessive allocations
8. Inefficient database queries
9. Missing connection pooling
10. Lack of concurrency

For each issue, provide:
- Severity (CRITICAL, HIGH, MEDIUM, LOW)
- Line numbers
- Performance impact description
- Scalability limit (e.g., "breaks at 1000 concurrent users")
- Optimization recommendation

Return in JSON format:
{{
  "bottlenecks": [
    {{
      "severity": "HIGH",
      "line": 42,
      "issue": "N+1 Query",
      "impact": "Linear growth in database calls",
      "limit": "Breaks at 100+ records",
      "fix": "Use select_related or prefetch_related"
    }}
  ],
  "scalability_score": 60,
  "recommendations": ["recommendation1", "recommendation2"]
}}
"""
        
        return await self._call_api(prompt, AnalysisType.SCALABILITY)
    
    async def analyze_database(
        self,
        code: str,
        file_path: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Analyze database queries and patterns
        
        Args:
            code: Source code to analyze
            file_path: Path to the file
            language: Programming language
        
        Returns:
            Dict with database optimization findings
        """
        prompt = f"""You are a database optimization expert. Analyze this {language} code for database anti-patterns.

File: {file_path}

Code:
```{language}
{code}
```

Identify:
1. SELECT * queries
2. Queries without WHERE clauses
3. Missing indexes (based on query patterns)
4. N+1 query issues
5. Missing connection pooling
6. Improper transaction handling
7. SQL injection vulnerabilities
8. Missing query optimization
9. Inefficient JOINs
10. Missing database constraints

For each issue, provide:
- Severity
- Line numbers
- Query or pattern involved
- Performance impact
- Optimization recommendation

Return in JSON format:
{{
  "issues": [
    {{
      "severity": "HIGH",
      "line": 25,
      "pattern": "SELECT *",
      "query": "SELECT * FROM users",
      "impact": "Retrieves unnecessary columns, slow performance",
      "fix": "SELECT id, name, email FROM users"
    }}
  ],
  "db_health_score": 70,
  "index_suggestions": ["CREATE INDEX idx_user_email ON users(email)"]
}}
"""
        
        return await self._call_api(prompt, AnalysisType.DATABASE)
    
    async def code_review(
        self,
        code: str,
        file_path: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Perform comprehensive code review
        
        Args:
            code: Source code to review
            file_path: Path to the file
            language: Programming language
        
        Returns:
            Dict with code review findings
        """
        prompt = f"""You are a senior code reviewer. Perform a comprehensive review of this {language} code.

File: {file_path}

Code:
```{language}
{code}
```

Review for:
1. Code quality and readability
2. Design patterns and architecture
3. Error handling
4. Documentation and comments
5. Naming conventions
6. Code duplication
7. Complexity (cyclomatic complexity)
8. Best practices adherence
9. Maintainability
10. Potential bugs

Return in JSON format:
{{
  "quality_score": 75,
  "issues": [
    {{
      "severity": "MEDIUM",
      "category": "readability",
      "line": 10,
      "issue": "Complex nested conditions",
      "suggestion": "Extract to separate method"
    }}
  ],
  "strengths": ["Good error handling", "Clear naming"],
  "improvements": ["Add docstrings", "Reduce complexity"]
}}
"""
        
        return await self._call_api(prompt, AnalysisType.CODE_REVIEW)
    
    async def batch_analyze_files(
        self,
        files: List[Dict[str, str]],
        analysis_type: AnalysisType
    ) -> List[Dict[str, Any]]:
        """
        Analyze multiple files in batch
        
        Args:
            files: List of dicts with 'path' and 'code' keys
            analysis_type: Type of analysis to perform
        
        Returns:
            List of analysis results
        """
        results = []
        
        for file_info in files:
            try:
                if analysis_type == AnalysisType.SECURITY:
                    result = await self.analyze_security(
                        file_info['code'],
                        file_info['path'],
                        file_info.get('language', 'python')
                    )
                elif analysis_type == AnalysisType.TESTING:
                    result = await self.generate_tests(
                        file_info['code'],
                        file_info['path'],
                        file_info.get('language', 'python')
                    )
                elif analysis_type == AnalysisType.SCALABILITY:
                    result = await self.analyze_scalability(
                        file_info['code'],
                        file_info['path'],
                        file_info.get('language', 'python')
                    )
                elif analysis_type == AnalysisType.DATABASE:
                    result = await self.analyze_database(
                        file_info['code'],
                        file_info['path'],
                        file_info.get('language', 'python')
                    )
                else:
                    result = await self.code_review(
                        file_info['code'],
                        file_info['path'],
                        file_info.get('language', 'python')
                    )
                
                results.append({
                    'file': file_info['path'],
                    'success': True,
                    'result': result
                })
                
            except Exception as e:
                logger.error(f"Failed to analyze {file_info['path']}: {str(e)}")
                results.append({
                    'file': file_info['path'],
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    async def _call_api(
        self,
        prompt: str,
        analysis_type: AnalysisType,
        retry_count: int = 3
    ) -> Dict[str, Any]:
        """
        Call Gemini API with retry logic
        
        Args:
            prompt: Prompt to send
            analysis_type: Type of analysis
            retry_count: Number of retries on failure
        
        Returns:
            Parsed JSON response from Gemini
        """
        import json
        import asyncio
        
        for attempt in range(retry_count):
            try:
                # Call Gemini API
                response = self.client.generate_content(prompt)
                
                # Extract text from response
                if hasattr(response, 'text'):
                    response_text = response.text
                elif hasattr(response, 'candidates') and response.candidates:
                    response_text = response.candidates[0].content.parts[0].text
                else:
                    raise ValueError("Unexpected response format from Gemini")
                
                # Try to parse JSON from response
                # Sometimes Gemini wraps JSON in markdown code blocks
                response_text = response_text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.startswith('```'):
                    response_text = response_text[3:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                
                response_text = response_text.strip()
                
                # Parse JSON
                result = json.loads(response_text)
                
                logger.info(f"Successfully completed {analysis_type.value} analysis")
                return result
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON response (attempt {attempt + 1}/{retry_count}): {str(e)}")
                if attempt < retry_count - 1:
                    await asyncio.sleep(1)
                    continue
                else:
                    # Return raw response if JSON parsing fails
                    return {
                        "raw_response": response_text,
                        "parse_error": str(e),
                        "analysis_type": analysis_type.value
                    }
            
            except Exception as e:
                logger.error(f"API call failed (attempt {attempt + 1}/{retry_count}): {str(e)}")
                if attempt < retry_count - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise
        
        raise RuntimeError(f"Failed to complete {analysis_type.value} analysis after {retry_count} attempts")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_configured": bool(self.api_key),
            "client_initialized": self.client is not None
        }

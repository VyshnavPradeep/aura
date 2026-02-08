from typing import List, Optional
import logging
import os
logger = logging.getLogger(__name__)
class QueryEnhancer:
    def __init__(self, api_key: Optional[str] = None, provider: str = "gemini"):
        self.provider = provider
        self.client = None
        if api_key is None:
            if provider == "gemini":
                api_key = os.getenv("GEMINI_API_KEY")
            elif provider == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
            elif provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
        self.api_key = api_key
        self._init_client()
    def _init_client(self):
        try:
            if self.provider == "gemini" and self.api_key:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel('gemini-1.5-pro')
                logger.info("Initialized Gemini client for query enhancement")
            elif self.provider == "anthropic" and self.api_key:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
                logger.info("Initialized Anthropic client for query enhancement")
            elif self.provider == "openai" and self.api_key:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                logger.info("Initialized OpenAI client for query enhancement")
            else:
                logger.warning("No API key provided - query enhancement disabled")
        except ImportError as e:
            logger.error(f"Failed to import LLM library: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {str(e)}")
    def generate_multi_queries(self, query: str, num_queries: int = 3) -> List[str]:
        if self.client is None:
            logger.warning("LLM client not available - returning original query only")
            return [query]
        try:
            prompt = f"""Given this code analysis query: "{query}"
Generate {num_queries} alternative phrasings that capture different aspects of what the user is looking for:
1. Technical implementation focus (specific patterns, algorithms)
2. Functional/behavioral focus (what it does, use cases)
3. Architecture focus (design patterns, structure)
Requirements:
- Each query should be different but related to the original intent
- Focus on code-specific terminology
- Keep queries concise (1-2 sentences each)
Return ONLY the {num_queries} alternative queries, one per line, without numbering."""
            if self.provider == "gemini":
                response = self.client.generate_content(prompt)
                response_text = response.text
            elif self.provider == "anthropic":
                message = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = message.content[0].text
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=400
                )
                response_text = response.choices[0].message.content
            generated_queries = [q.strip() for q in response_text.strip().split('\n') if q.strip()]
            import re
            generated_queries = [re.sub(r'^\d+[\.)]\s*', '', q) for q in generated_queries]
            all_queries = [query] + generated_queries[:num_queries]
            logger.info(f"Generated {len(all_queries)} query variations")
            return all_queries
        except Exception as e:
            logger.error(f"Multi-query generation failed: {str(e)}")
            return [query]
    def decompose_query(self, query: str) -> List[str]:
        if self.client is None:
            logger.warning("LLM client not available - returning original query")
            return [query]
        try:
            prompt = f"""Analyze this code analysis query and break it into 2-4 simpler sub-queries:
Query: "{query}"
Instructions:
- Identify the main aspects or components of this query
- Create one focused sub-query for each aspect
- Each sub-query should be independently searchable
- Focus on code concepts, patterns, or functionality
Return ONLY the sub-queries, one per line, without numbering or explanations."""
            if self.provider == "gemini":
                response = self.client.generate_content(prompt)
                response_text = response.text
            elif self.provider == "anthropic":
                message = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = message.content[0].text
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=400
                )
                response_text = response.choices[0].message.content
            sub_queries = [q.strip() for q in response_text.strip().split('\n') if q.strip()]
            import re
            sub_queries = [re.sub(r'^\d+[\.)]\s*', '', q) for q in sub_queries]
            logger.info(f"Decomposed query into {len(sub_queries)} sub-queries")
            return sub_queries if sub_queries else [query]
        except Exception as e:
            logger.error(f"Query decomposition failed: {str(e)}")
            return [query]
    def generate_hypothetical_answer(self, query: str) -> str:
        if self.client is None:
            logger.warning("LLM client not available - using template-based HyDE")
            return self._template_based_hyde(query)
        try:
            prompt = f"""Given this query about code: "{query}"
Generate a hypothetical code snippet or detailed technical explanation that would answer this query.
Requirements:
- Write actual code if the query asks about implementation
- Include relevant function names, variable names, patterns
- Use technical terminology that would appear in real code
- Be specific about technologies, frameworks, or approaches
- Length: 4-8 lines for code snippets, 2-3 sentences for explanations
Generate the hypothetical answer:"""
            if self.provider == "gemini":
                response = self.client.generate_content(prompt)
                hypothetical_doc = response.text
            elif self.provider == "anthropic":
                message = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                hypothetical_doc = message.content[0].text
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                hypothetical_doc = response.choices[0].message.content
            logger.info("Generated hypothetical document using HyDE")
            return hypothetical_doc.strip()
        except Exception as e:
            logger.error(f"HyDE generation failed: {str(e)}")
            return self._template_based_hyde(query)
    def _template_based_hyde(self, query: str) -> str:
        query_lower = query.lower()
        templates = {
            'function': f"Function implementation for {query} with proper parameters, return values, and error handling",
            'class': f"Class definition for {query} with methods, attributes, and inheritance structure",
            'api': f"API endpoint handler for {query} with request processing, validation, and response formatting",
            'database': f"Database operation for {query} with connection handling, query execution, and result processing",
            'authentication': f"Authentication logic for {query} with credential validation, session management, and security checks",
            'error': f"Error handling implementation for {query} with try-catch blocks, logging, and recovery mechanisms",
            'async': f"Asynchronous implementation for {query} using async/await patterns and proper concurrency handling",
            'test': f"Test case for {query} with setup, execution, assertions, and cleanup"
        }
        for keyword, template in templates.items():
            if keyword in query_lower:
                return template
        return f"Code implementation addressing: {query}"
    def enhance_query(
        self,
        query: str,
        strategy: str = "multi_query"
    ) -> List[str]:
        if strategy == "multi_query":
            return self.generate_multi_queries(query)
        elif strategy == "decompose":
            return self.decompose_query(query)
        elif strategy == "hyde":
            hyde_doc = self.generate_hypothetical_answer(query)
            return [hyde_doc]
        else:
            logger.warning(f"Unknown strategy '{strategy}', returning original query")
            return [query]
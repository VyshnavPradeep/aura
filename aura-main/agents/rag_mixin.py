from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
logger = logging.getLogger(__name__)
class RAGMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rag_system = None
        self._init_rag()
    def _init_rag(self):
        try:
            from rag.advanced_rag import AdvancedRAG
            import os
            api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
            provider = "anthropic" if os.getenv("ANTHROPIC_API_KEY") else "openai"
            self.rag_system = AdvancedRAG(
                api_key=api_key,
                llm_provider=provider
            )
            logger.info(f"RAG system initialized for {self.__class__.__name__}")
        except Exception as e:
            logger.warning(f"RAG system not available: {str(e)}")
            self.rag_system = None
    def search_code(
        self,
        query: str,
        project_id: str,
        strategy: str = "multi_query",
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if self.rag_system is None:
            logger.warning("RAG system not available")
            return []
        try:
            result = self.rag_system.query(
                query=query,
                project_id=project_id,
                strategy=strategy,
                top_k=top_k,
                filters=filters,
                use_reranking=True,
                include_context=True
            )
            return result.get('results', [])
        except Exception as e:
            logger.error(f"Code search failed: {str(e)}")
            return []
    def find_security_patterns(self, project_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        queries = [
            "authentication and authorization logic",
            "input validation and sanitization",
            "SQL queries and database operations",
            "password hashing and encryption",
            "API authentication and token handling"
        ]
        all_results = []
        for query in queries:
            results = self.search_code(query, project_id, strategy="standard", top_k=top_k)
            all_results.extend(results)
        seen = set()
        unique_results = []
        for r in all_results:
            chunk_id = r.get('chunk_id', r.get('id'))
            if chunk_id not in seen:
                seen.add(chunk_id)
                unique_results.append(r)
        return unique_results[:top_k]
    def find_scalability_patterns(self, project_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        queries = [
            "database queries and connection pooling",
            "caching mechanisms and data storage",
            "async and concurrent operations",
            "API rate limiting and throttling",
            "batch processing and queue handling"
        ]
        all_results = []
        for query in queries:
            results = self.search_code(query, project_id, strategy="standard", top_k=top_k)
            all_results.extend(results)
        seen = set()
        unique_results = []
        for r in all_results:
            chunk_id = r.get('chunk_id', r.get('id'))
            if chunk_id not in seen:
                seen.add(chunk_id)
                unique_results.append(r)
        return unique_results[:top_k]
    def find_database_operations(self, project_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        return self.search_code(
            "database queries connections ORM models",
            project_id,
            strategy="multi_query",
            top_k=top_k,
            filters={'chunk_type': ['function', 'method']}
        )
    def find_api_endpoints(self, project_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        return self.search_code(
            "API endpoints routes handlers request response",
            project_id,
            strategy="multi_query",
            top_k=top_k
        )
    def get_code_context(self, chunk_id: str, project_id: str) -> Optional[Dict[str, Any]]:
        if self.rag_system is None:
            return None
        try:
            if project_id not in self.rag_system.loaded_projects:
                self.rag_system._load_project(project_id)
            chunks = self.rag_system.loaded_projects[project_id]['chunks']
            for chunk in chunks:
                if chunk.get('chunk_id') == chunk_id or chunk.get('id') == chunk_id:
                    enriched = self.rag_system._enrich_with_context([chunk], chunks)
                    return enriched[0] if enriched else chunk
            return None
        except Exception as e:
            logger.error(f"Failed to get code context: {str(e)}")
            return None
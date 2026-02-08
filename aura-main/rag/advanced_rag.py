from typing import List, Dict, Any, Optional
import logging
import os
from pathlib import Path
import pickle
from .contextual_chunker import ContextualChunker
from .hybrid_retriever import HybridRetriever
from .query_enhancer import QueryEnhancer
from .document_reranker import DocumentReranker
logger = logging.getLogger(__name__)
class AdvancedRAG:
    def __init__(
        self,
        api_key: Optional[str] = None,
        llm_provider: str = "gemini",
        embedding_model: str = "microsoft/codebert-base",
        reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        index_dir: str = "rag/indices",
        hybrid_alpha: float = 0.7
    ):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.chunker = ContextualChunker(chunk_size=512, overlap=50)
        self.query_enhancer = QueryEnhancer(api_key=api_key, provider=llm_provider)
        self.reranker = DocumentReranker(model_name=reranker_model)
        self.embedder = None
        self.hybrid_retriever = HybridRetriever(alpha=hybrid_alpha)
        self.embedding_model = embedding_model
        self._init_embedder()
        self.loaded_projects = {}
    def _init_embedder(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.embedder = SentenceTransformer(self.embedding_model)
            logger.info(f"Loaded embedding model: {self.embedding_model}")
        except ImportError:
            logger.error("sentence-transformers not installed")
        except Exception as e:
            logger.error(f"Failed to load embedder: {str(e)}")
    def index_codebase(
        self,
        project_dir: str,
        project_id: str,
        file_extensions: List[str] = ['.py'],
        exclude_dirs: List[str] = ['venv', 'node_modules', '__pycache__', '.git']
    ) -> Dict[str, Any]:
        logger.info(f"Starting advanced indexing for project: {project_id}")
        project_path = Path(project_dir)
        if not project_path.exists():
            return {"success": False, "error": "Project directory not found"}
        all_files = []
        for ext in file_extensions:
            for file_path in project_path.rglob(f"*{ext}"):
                if any(exc_dir in str(file_path) for exc_dir in exclude_dirs):
                    continue
                all_files.append(file_path)
        logger.info(f"Found {len(all_files)} files to index")
        if not all_files:
            return {"success": False, "error": "No code files found"}
        all_chunks = []
        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                language = 'python' if file_path.suffix == '.py' else 'unknown'
                chunks = self.chunker.create_hierarchical_chunks(
                    code=code,
                    file_path=str(file_path.relative_to(project_path)),
                    language=language
                )
                all_chunks.extend(chunks)
            except Exception as e:
                logger.warning(f"Failed to process {file_path}: {str(e)}")
                continue
        logger.info(f"Created {len(all_chunks)} hierarchical chunks")
        if not all_chunks:
            return {"success": False, "error": "No chunks created"}
        if self.embedder is None:
            return {"success": False, "error": "Embedder not initialized"}
        try:
            texts = [chunk.get('text', chunk.get('content', '')) for chunk in all_chunks]
            embeddings = self.embedder.encode(
                texts,
                show_progress_bar=True,
                normalize_embeddings=True,
                batch_size=32
            )
            logger.info(f"Generated embeddings: shape {embeddings.shape}")
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            return {"success": False, "error": f"Embedding failed: {str(e)}"}
        try:
            import faiss
            import numpy as np
            embeddings = embeddings.astype('float32')
            dimension = embeddings.shape[1]
            if len(embeddings) > 1000:
                quantizer = faiss.IndexFlatIP(dimension)
                index = faiss.IndexHNSWFlat(dimension, 32, faiss.METRIC_INNER_PRODUCT)
                index.hnsw.efConstruction = 40
                index.hnsw.efSearch = 16
            else:
                index = faiss.IndexFlatIP(dimension)
            index.add(embeddings)
            index_path = self.index_dir / f"{project_id}.index"
            faiss.write_index(index, str(index_path))
            logger.info(f"Created FAISS index with {index.ntotal} vectors")
        except Exception as e:
            logger.error(f"FAISS indexing failed: {str(e)}")
            return {"success": False, "error": f"FAISS indexing failed: {str(e)}"}
        bm25_success = self.hybrid_retriever.index_chunks(all_chunks, project_id)
        try:
            metadata_path = self.index_dir / f"{project_id}_metadata.pkl"
            with open(metadata_path, 'wb') as f:
                pickle.dump(all_chunks, f)
            logger.info("Saved chunk metadata")
        except Exception as e:
            logger.error(f"Metadata saving failed: {str(e)}")
            return {"success": False, "error": f"Metadata save failed: {str(e)}"}
        self.loaded_projects[project_id] = {
            'index': index,
            'chunks': all_chunks,
            'embeddings': embeddings
        }
        return {
            "success": True,
            "project_id": project_id,
            "files_indexed": len(all_files),
            "chunks_created": len(all_chunks),
            "embeddings_dimension": dimension,
            "bm25_enabled": bm25_success,
            "index_path": str(index_path),
            "features": [
                "hierarchical_chunking",
                "parent_child_relationships",
                "hybrid_search_vector_bm25",
                "cross_encoder_reranking",
                "query_enhancement",
                "contextual_retrieval"
            ]
        }
    def query(
        self,
        query: str,
        project_id: str,
        strategy: str = "multi_query",
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        use_reranking: bool = True,
        include_context: bool = True,
        score_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        logger.info(f"Query: '{query}' | Strategy: {strategy} | Project: {project_id}")
        if project_id not in self.loaded_projects:
            success = self._load_project(project_id)
            if not success:
                return {
                    "success": False,
                    "error": "Failed to load project indices"
                }
        project_data = self.loaded_projects[project_id]
        queries = self._enhance_query(query, strategy)
        logger.info(f"Enhanced to {len(queries)} query variations")
        all_candidates = []
        seen_chunk_ids = set()
        for q in queries:
            candidates = self.hybrid_retriever.hybrid_search(
                query=q,
                project_id=project_id,
                top_k=top_k * 3,
                vector_index=project_data['index'],
                embedder=self.embedder
            )
            for candidate in candidates:
                chunk_id = candidate.get('chunk_id', candidate.get('id'))
                if chunk_id not in seen_chunk_ids:
                    seen_chunk_ids.add(chunk_id)
                    all_candidates.append(candidate)
        logger.info(f"Hybrid search retrieved {len(all_candidates)} unique candidates")
        if not all_candidates:
            return {
                "success": True,
                "query": query,
                "strategy": strategy,
                "results": [],
                "message": "No results found"
            }
        if filters:
            all_candidates = self._apply_filters(all_candidates, filters)
            logger.info(f"After filtering: {len(all_candidates)} candidates")
        if use_reranking and len(all_candidates) > top_k:
            results = self.reranker.rerank_with_fusion(
                query=query,
                documents=all_candidates,
                top_k=top_k,
                fusion_weight=0.7
            )
            logger.info(f"Reranked to top {len(results)} results")
        else:
            results = all_candidates[:top_k]
        if score_threshold is not None:
            score_key = 'fused_score' if use_reranking else 'combined_score'
            results = [r for r in results if r.get(score_key, 0) >= score_threshold]
            logger.info(f"After score threshold: {len(results)} results")
        if include_context:
            results = self._enrich_with_context(results, project_data['chunks'])
        return {
            "success": True,
            "query": query,
            "strategy": strategy,
            "queries_used": queries,
            "candidates_retrieved": len(all_candidates),
            "results_count": len(results),
            "results": results,
            "metadata": {
                "reranking_applied": use_reranking,
                "context_enriched": include_context,
                "filters_applied": filters is not None
            }
        }
    def _enhance_query(self, query: str, strategy: str) -> List[str]:
        if strategy == "multi_query":
            return self.query_enhancer.generate_multi_queries(query, num_queries=3)
        elif strategy == "decompose":
            return self.query_enhancer.decompose_query(query)
        elif strategy == "hyde":
            hyde_doc = self.query_enhancer.generate_hypothetical_answer(query)
            return [query, hyde_doc]
        else:
            return [query]
    def _apply_filters(
        self,
        candidates: List[Dict[str, Any]],
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        filtered = []
        for candidate in candidates:
            match = True
            for key, value in filters.items():
                if key in candidate:
                    if isinstance(value, list):
                        if candidate[key] not in value:
                            match = False
                            break
                    else:
                        if isinstance(value, str) and isinstance(candidate[key], str):
                            if value.lower() not in candidate[key].lower():
                                match = False
                                break
                        elif candidate[key] != value:
                            match = False
                            break
            if match:
                filtered.append(candidate)
        return filtered
    def _enrich_with_context(
        self,
        results: List[Dict[str, Any]],
        all_chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        chunks_by_id = {}
        for chunk in all_chunks:
            chunk_id = chunk.get('chunk_id', chunk.get('id'))
            if chunk_id:
                chunks_by_id[chunk_id] = chunk
        enriched_results = []
        for result in results:
            enriched = result.copy()
            if result.get('type') == 'child' and 'parent_id' in result:
                parent_id = result['parent_id']
                if parent_id in chunks_by_id:
                    parent = chunks_by_id[parent_id]
                    enriched['parent_chunk'] = {
                        'name': parent.get('name'),
                        'type': parent.get('chunk_type'),
                        'context': parent.get('context', ''),
                        'file': parent.get('file'),
                        'line': parent.get('line')
                    }
            if result.get('type') == 'parent' and 'children' in result:
                child_ids = result['children']
                children_info = []
                for child_id in child_ids[:5]:
                    if child_id in chunks_by_id:
                        child = chunks_by_id[child_id]
                        children_info.append({
                            'name': child.get('name'),
                            'type': child.get('chunk_type'),
                            'line': child.get('line')
                        })
                if children_info:
                    enriched['child_chunks'] = children_info
            enriched_results.append(enriched)
        return enriched_results
    def _load_project(self, project_id: str) -> bool:
        try:
            import faiss
            index_path = self.index_dir / f"{project_id}.index"
            if not index_path.exists():
                logger.error(f"Index not found: {index_path}")
                return False
            index = faiss.read_index(str(index_path))
            metadata_path = self.index_dir / f"{project_id}_metadata.pkl"
            if not metadata_path.exists():
                logger.error(f"Metadata not found: {metadata_path}")
                return False
            with open(metadata_path, 'rb') as f:
                chunks = pickle.load(f)
            self.hybrid_retriever.load_bm25_index(project_id)
            self.loaded_projects[project_id] = {
                'index': index,
                'chunks': chunks,
                'embeddings': None
            }
            logger.info(f"Loaded project {project_id} with {len(chunks)} chunks")
            return True
        except Exception as e:
            logger.error(f"Failed to load project: {str(e)}")
            return False
    def get_statistics(self, project_id: str) -> Dict[str, Any]:
        if project_id not in self.loaded_projects:
            if not self._load_project(project_id):
                return {"error": "Project not found"}
        chunks = self.loaded_projects[project_id]['chunks']
        type_counts = {}
        for chunk in chunks:
            chunk_type = chunk.get('chunk_type', 'unknown')
            type_counts[chunk_type] = type_counts.get(chunk_type, 0) + 1
        return {
            "project_id": project_id,
            "total_chunks": len(chunks),
            "chunk_types": type_counts,
            "has_hierarchical_structure": any(c.get('type') == 'parent' for c in chunks),
            "has_relationships": any('parent_id' in c or 'children' in c for c in chunks)
        }
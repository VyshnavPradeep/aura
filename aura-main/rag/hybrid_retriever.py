from typing import List, Dict, Any, Optional
import numpy as np
import logging
import pickle
from pathlib import Path
logger = logging.getLogger(__name__)
class HybridRetriever:
    def __init__(self, vector_store=None, alpha: float = 0.5):
        self.vector_store = vector_store
        self.alpha = alpha
        self.bm25 = None
        self.chunks = []
        self.index_dir = Path("rag/indices")
    def index_chunks(self, chunks: List[Dict[str, Any]], project_id: str):
        try:
            from rank_bm25 import BM25Okapi
            self.chunks = chunks
            tokenized_chunks = []
            for chunk in chunks:
                content = chunk.get('text', chunk.get('content', ''))
                tokens = content.lower().split()
                tokenized_chunks.append(tokens)
            self.bm25 = BM25Okapi(tokenized_chunks)
            bm25_path = self.index_dir / f"{project_id}_bm25.pkl"
            with open(bm25_path, 'wb') as f:
                pickle.dump({'bm25': self.bm25, 'chunks': self.chunks}, f)
            logger.info(f"BM25 index created with {len(chunks)} documents")
            return True
        except ImportError:
            logger.error("rank-bm25 not installed. Install with: pip install rank-bm25")
            return False
        except Exception as e:
            logger.error(f"BM25 indexing failed: {str(e)}")
            return False
    def load_bm25_index(self, project_id: str) -> bool:
        try:
            bm25_path = self.index_dir / f"{project_id}_bm25.pkl"
            if not bm25_path.exists():
                return False
            with open(bm25_path, 'rb') as f:
                data = pickle.load(f)
                self.bm25 = data['bm25']
                self.chunks = data['chunks']
            logger.info(f"BM25 index loaded for project {project_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to load BM25 index: {str(e)}")
            return False
    def hybrid_search(
        self,
        query: str,
        project_id: str,
        top_k: int = 5,
        vector_index=None,
        embedder=None
    ) -> List[Dict[str, Any]]:
        try:
            if self.bm25 is None:
                if not self.load_bm25_index(project_id):
                    logger.warning("BM25 index not available, using vector search only")
                    return self._vector_search_only(query, project_id, top_k, vector_index, embedder)
            vector_scores = {}
            if vector_index is not None and embedder is not None:
                try:
                    import faiss
                    query_embedding = embedder.encode([query], normalize_embeddings=True)
                    query_embedding = query_embedding.astype('float32')
                    distances, indices = vector_index.search(query_embedding, min(top_k * 2, len(self.chunks)))
                    for dist, idx in zip(distances[0], indices[0]):
                        if idx < len(self.chunks):
                            vector_scores[idx] = 1 / (1 + float(dist))
                except Exception as e:
                    logger.error(f"Vector search failed: {str(e)}")
            bm25_scores = {}
            if self.bm25 is not None:
                query_tokens = query.lower().split()
                scores = self.bm25.get_scores(query_tokens)
                for idx, score in enumerate(scores):
                    bm25_scores[idx] = float(score)
            vector_scores_norm = self._normalize_scores(vector_scores)
            bm25_scores_norm = self._normalize_scores(bm25_scores)
            combined_scores = {}
            all_indices = set(vector_scores_norm.keys()) | set(bm25_scores_norm.keys())
            for idx in all_indices:
                v_score = vector_scores_norm.get(idx, 0)
                b_score = bm25_scores_norm.get(idx, 0)
                combined_scores[idx] = self.alpha * v_score + (1 - self.alpha) * b_score
            top_indices = sorted(
                combined_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_k]
            results = []
            for idx, score in top_indices:
                if idx < len(self.chunks):
                    result = self.chunks[idx].copy()
                    result['combined_score'] = score
                    result['vector_score'] = vector_scores_norm.get(idx, 0)
                    result['bm25_score'] = bm25_scores_norm.get(idx, 0)
                    results.append(result)
            logger.info(f"Hybrid search returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Hybrid search failed: {str(e)}")
            return []
    def _normalize_scores(self, scores: Dict[int, float]) -> Dict[int, float]:
        if not scores:
            return {}
        values = list(scores.values())
        min_val = min(values)
        max_val = max(values)
        if max_val == min_val:
            return {k: 1.0 for k in scores}
        normalized = {}
        for k, v in scores.items():
            normalized[k] = (v - min_val) / (max_val - min_val)
        return normalized
    def _vector_search_only(
        self,
        query: str,
        project_id: str,
        top_k: int,
        vector_index,
        embedder
    ) -> List[Dict[str, Any]]:
        if vector_index is None or embedder is None:
            return []
        try:
            import faiss
            query_embedding = embedder.encode([query], normalize_embeddings=True)
            query_embedding = query_embedding.astype('float32')
            distances, indices = vector_index.search(query_embedding, top_k)
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.chunks):
                    result = self.chunks[idx].copy()
                    result['score'] = 1 / (1 + float(dist))
                    results.append(result)
            return results
        except Exception as e:
            logger.error(f"Vector search failed: {str(e)}")
            return []
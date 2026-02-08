from typing import List, Dict, Any, Optional
import logging
import numpy as np
logger = logging.getLogger(__name__)
class DocumentReranker:
    def __init__(
        self,
        model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2',
        max_length: int = 512
    ):
        self.model_name = model_name
        self.max_length = max_length
        self.model = None
        self._init_model()
    def _init_model(self):
        try:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(self.model_name, max_length=self.max_length)
            logger.info(f"Loaded cross-encoder model: {self.model_name}")
        except ImportError:
            logger.error("sentence-transformers not installed. Install: pip install sentence-transformers")
            self.model = None
        except Exception as e:
            logger.error(f"Failed to load cross-encoder: {str(e)}")
            self.model = None
    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        if not documents:
            logger.warning("No documents to rerank")
            return []
        if self.model is None:
            logger.warning("Cross-encoder not available, returning original order")
            return documents[:top_k]
        try:
            pairs = []
            valid_indices = []
            for idx, doc in enumerate(documents):
                doc_text = doc.get('text', doc.get('content', doc.get('context', '')))
                if doc_text:
                    if len(doc_text) > self.max_length * 4:
                        doc_text = doc_text[:self.max_length * 4]
                    pairs.append([query, doc_text])
                    valid_indices.append(idx)
            if not pairs:
                logger.warning("No valid text content in documents")
                return documents[:top_k]
            scores = self.model.predict(pairs)
            reranked_docs = []
            for idx, score in zip(valid_indices, scores):
                doc = documents[idx].copy()
                doc['rerank_score'] = float(score)
                if 'combined_score' not in doc and 'score' not in doc:
                    doc['original_score'] = 0.0
                else:
                    doc['original_score'] = doc.get('combined_score', doc.get('score', 0.0))
                if score_threshold is None or score >= score_threshold:
                    reranked_docs.append(doc)
            reranked_docs.sort(key=lambda x: x['rerank_score'], reverse=True)
            final_results = reranked_docs[:top_k]
            logger.info(f"Reranked {len(documents)} documents, returning top {len(final_results)}")
            return final_results
        except Exception as e:
            logger.error(f"Reranking failed: {str(e)}")
            return documents[:top_k]
    def rerank_with_fusion(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = 5,
        fusion_weight: float = 0.7
    ) -> List[Dict[str, Any]]:
        if self.model is None:
            logger.warning("Cross-encoder not available")
            return documents[:top_k]
        reranked = self.rerank(query, documents, top_k=len(documents))
        if not reranked:
            return documents[:top_k]
        rerank_scores = [doc['rerank_score'] for doc in reranked]
        original_scores = [doc['original_score'] for doc in reranked]
        rerank_norm = self._normalize_scores(rerank_scores)
        original_norm = self._normalize_scores(original_scores)
        for i, doc in enumerate(reranked):
            doc['fused_score'] = (
                fusion_weight * rerank_norm[i] +
                (1 - fusion_weight) * original_norm[i]
            )
        reranked.sort(key=lambda x: x['fused_score'], reverse=True)
        logger.info(f"Applied score fusion with weight {fusion_weight}")
        return reranked[:top_k]
    def _normalize_scores(self, scores: List[float]) -> List[float]:
        if not scores:
            return []
        scores_array = np.array(scores)
        min_score = scores_array.min()
        max_score = scores_array.max()
        if max_score == min_score:
            return [1.0] * len(scores)
        normalized = (scores_array - min_score) / (max_score - min_score)
        return normalized.tolist()
    def explain_ranking(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        reranked = self.rerank(query, documents, top_k=top_k)
        for rank, doc in enumerate(reranked, 1):
            rerank_score = doc.get('rerank_score', 0)
            original_score = doc.get('original_score', 0)
            explanation = []
            if rerank_score > 0.8:
                explanation.append("High relevance to query")
            elif rerank_score > 0.5:
                explanation.append("Moderate relevance to query")
            else:
                explanation.append("Low relevance to query")
            score_diff = rerank_score - original_score
            if abs(score_diff) > 0.3:
                if score_diff > 0:
                    explanation.append("Promoted by reranking (better match than initially thought)")
                else:
                    explanation.append("Demoted by reranking (weaker match than initially thought)")
            doc['rank'] = rank
            doc['explanation'] = " | ".join(explanation)
        return reranked
    def batch_rerank(
        self,
        queries_and_docs: List[tuple],
        top_k: int = 5
    ) -> List[List[Dict[str, Any]]]:
        results = []
        for query, docs in queries_and_docs:
            reranked = self.rerank(query, docs, top_k=top_k)
            results.append(reranked)
        return results
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import logging
from pathlib import Path
import os
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/rag", tags=["rag"])
try:
    from rag.advanced_rag import AdvancedRAG
    api_key = os.getenv("GEMINI_API_KEY")
    provider = "gemini"
    rag_system = AdvancedRAG(
        api_key=api_key,
        llm_provider=provider
    )
    logger.info("RAG system initialized")
except Exception as e:
    logger.error(f"Failed to initialize RAG system: {str(e)}")
    rag_system = None
class IndexRequest(BaseModel):
    project_dir: str
    project_id: str
    file_extensions: List[str] = ['.py']
    exclude_dirs: List[str] = ['venv', 'node_modules', '__pycache__', '.git']
class SearchRequest(BaseModel):
    query: str
    project_id: str
    strategy: str = "multi_query"
    top_k: int = 5
    filters: Optional[Dict[str, Any]] = None
    use_reranking: bool = True
    include_context: bool = True
class SearchResponse(BaseModel):
    success: bool
    query: str
    strategy: str
    results_count: int
    results: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
@router.post("/index")
async def index_codebase(request: IndexRequest):
    if rag_system is None:
        raise HTTPException(status_code=500, detail="RAG system not available")
    try:
        project_path = Path(request.project_dir)
        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project directory not found")
        result = rag_system.index_codebase(
            project_dir=request.project_dir,
            project_id=request.project_id,
            file_extensions=request.file_extensions,
            exclude_dirs=request.exclude_dirs
        )
        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error', 'Indexing failed'))
        return {
            "success": True,
            "message": f"Successfully indexed {result['files_indexed']} files",
            "project_id": result['project_id'],
            "statistics": {
                "files_indexed": result['files_indexed'],
                "chunks_created": result['chunks_created'],
                "embeddings_dimension": result['embeddings_dimension'],
                "bm25_enabled": result['bm25_enabled']
            },
            "features": result['features']
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Indexing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/search", response_model=SearchResponse)
async def search_code(request: SearchRequest):
    if rag_system is None:
        return SearchResponse(
            success=False,
            query=request.query,
            strategy=request.strategy,
            results_count=0,
            results=[],
            error="RAG system not available"
        )
    try:
        result = rag_system.query(
            query=request.query,
            project_id=request.project_id,
            strategy=request.strategy,
            top_k=request.top_k,
            filters=request.filters,
            use_reranking=request.use_reranking,
            include_context=request.include_context
        )
        if not result.get('success'):
            return SearchResponse(
                success=False,
                query=request.query,
                strategy=request.strategy,
                results_count=0,
                results=[],
                error=result.get('error', 'Search failed')
            )
        return SearchResponse(
            success=True,
            query=result['query'],
            strategy=result['strategy'],
            results_count=result['results_count'],
            results=result['results'],
            metadata=result.get('metadata')
        )
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        return SearchResponse(
            success=False,
            query=request.query,
            strategy=request.strategy,
            results_count=0,
            results=[],
            error=str(e)
        )
@router.get("/statistics/{project_id}")
async def get_statistics(project_id: str):
    if rag_system is None:
        raise HTTPException(status_code=500, detail="RAG system not available")
    try:
        stats = rag_system.get_statistics(project_id)
        if 'error' in stats:
            raise HTTPException(status_code=404, detail=stats['error'])
        return {
            "success": True,
            "project_id": stats['project_id'],
            "statistics": {
                "total_chunks": stats['total_chunks'],
                "chunk_types": stats['chunk_types'],
                "has_hierarchical_structure": stats['has_hierarchical_structure'],
                "has_relationships": stats['has_relationships']
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/health")
async def health_check():
    return {
        "status": "healthy" if rag_system is not None else "unavailable",
        "rag_enabled": rag_system is not None,
        "features": [
            "hierarchical_chunking",
            "hybrid_search",
            "query_enhancement",
            "reranking",
            "contextual_retrieval"
        ] if rag_system else []
    }
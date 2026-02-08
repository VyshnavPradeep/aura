import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path
import pickle
import logging
from .advanced_rag import AdvancedRAG
from .contextual_chunker import ContextualChunker
logger = logging.getLogger(__name__)
class CodeEmbedder:
    def __init__(self, model_name: str = "microsoft/codebert-base", index_dir: str = "rag/indices"):
        self.model_name = model_name
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.model = None
        self.dimension = 768
        self.advanced_rag = AdvancedRAG(
            embedding_model=model_name,
            index_dir=str(index_dir)
        )
    def _init_model(self):
        if self.model is None and self.advanced_rag.embedder:
            self.model = self.advanced_rag.embedder
            logger.info(f"Using AdvancedRAG embedder: {self.model_name}")
    def create_code_chunks(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            chunker = ContextualChunker()
            all_chunks = []
            for file_data in parsed_data.get("parsed_files", []):
                file_path = file_data.get("file_path", "")
                code_content = file_data.get("content", "")
                if code_content:
                    chunks = chunker.create_hierarchical_chunks(
                        code=code_content,
                        file_path=file_path,
                        language="python"
                    )
                    all_chunks.extend(chunks)
            if all_chunks:
                logger.info(f"Created {len(all_chunks)} hierarchical chunks (advanced)")
                return all_chunks
        except Exception as e:
            logger.warning(f"Advanced chunking failed, using legacy mode: {str(e)}")
        chunks = []
        for file_data in parsed_data.get("parsed_files", []):
            file_path = file_data.get("file_path", "")
            for func in file_data.get("functions", []):
                chunk = {
                    "type": "function",
                    "name": func.get("name"),
                    "file": file_path,
                    "line": func.get("line"),
                    "text": f"Function {func.get('name')} in {file_path}",
                    "content": f"Function {func.get('name')} in {file_path}",
                    "metadata": func
                }
                chunks.append(chunk)
            for cls in file_data.get("classes", []):
                chunk = {
                    "type": "class",
                    "name": cls.get("name"),
                    "file": file_path,
                    "line": cls.get("line"),
                    "text": f"Class {cls.get('name')} in {file_path}",
                    "content": f"Class {cls.get('name')} in {file_path}",
                    "metadata": cls
                }
                chunks.append(chunk)
        logger.info(f"Created {len(chunks)} code chunks (legacy)")
        return chunks
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> np.ndarray:
        if self.model is None:
            logger.warning("Model not available. Returning dummy embeddings.")
            return np.random.rand(len(chunks), self.dimension).astype('float32')
        try:
            texts = [chunk["text"] for chunk in chunks]
            embeddings = self.model.encode(texts, show_progress_bar=True)
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings.astype('float32')
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            return np.random.rand(len(chunks), self.dimension).astype('float32')
    def create_faiss_index(self, embeddings: np.ndarray, project_id: str) -> bool:
        try:
            import faiss
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)
            index_path = self.index_dir / f"{project_id}.index"
            faiss.write_index(index, str(index_path))
            logger.info(f"Created FAISS index with {index.ntotal} vectors")
            return True
        except ImportError:
            logger.error("FAISS not installed. Install with: pip install faiss-cpu")
            return False
        except Exception as e:
            logger.error(f"FAISS index creation failed: {str(e)}")
            return False
    def save_chunks_metadata(self, chunks: List[Dict[str, Any]], project_id: str) -> bool:
        try:
            metadata_path = self.index_dir / f"{project_id}_metadata.pkl"
            with open(metadata_path, 'wb') as f:
                pickle.dump(chunks, f)
            logger.info(f"Saved metadata for {len(chunks)} chunks")
            return True
        except Exception as e:
            logger.error(f"Failed to save metadata: {str(e)}")
            return False
    def process_project(self, parsed_data: Dict[str, Any], project_id: str) -> Dict[str, Any]:
        try:
            chunks = self.create_code_chunks(parsed_data)
            if not chunks:
                return {
                    "success": False,
                    "error": "No code chunks created"
                }
            embeddings = self.embed_chunks(chunks)
            index_created = self.create_faiss_index(embeddings, project_id)
            metadata_saved = self.save_chunks_metadata(chunks, project_id)
            return {
                "success": index_created and metadata_saved,
                "chunks_count": len(chunks),
                "embeddings_shape": embeddings.shape,
                "index_path": str(self.index_dir / f"{project_id}.index"),
                "metadata_path": str(self.index_dir / f"{project_id}_metadata.pkl")
            }
        except Exception as e:
            logger.error(f"Project processing failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    def search(self, query: str, project_id: str, k: int = 5) -> List[Dict[str, Any]]:
        try:
            import faiss
            index_path = self.index_dir / f"{project_id}.index"
            index = faiss.read_index(str(index_path))
            metadata_path = self.index_dir / f"{project_id}_metadata.pkl"
            with open(metadata_path, 'rb') as f:
                chunks = pickle.load(f)
            if self.model is None:
                return []
            query_embedding = self.model.encode([query]).astype('float32')
            distances, indices = index.search(query_embedding, k)
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(chunks):
                    result = chunks[idx].copy()
                    result['distance'] = float(distances[0][i])
                    results.append(result)
            return results
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []
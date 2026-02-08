from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
class RAGConfig(BaseSettings):
    gemini_api_key: Optional[str] = Field(default=None, env='GEMINI_API_KEY')
    anthropic_api_key: Optional[str] = Field(default=None, env='ANTHROPIC_API_KEY')
    openai_api_key: Optional[str] = Field(default=None, env='OPENAI_API_KEY')
    llm_provider: str = Field(default='gemini', env='LLM_PROVIDER')
    gemini_model: str = Field(default='gemini-1.5-pro', env='GEMINI_MODEL')
    gemini_temperature: float = Field(default=0.3, env='GEMINI_TEMPERATURE')
    embedding_model: str = Field(
        default='sentence-transformers/all-MiniLM-L6-v2',
        env='EMBEDDING_MODEL'
    )
    reranker_model: str = Field(
        default='cross-encoder/ms-marco-MiniLM-L-6-v2',
        env='RERANKER_MODEL'
    )
    index_dir: str = Field(default='rag/indices', env='RAG_INDEX_DIR')
    use_hnsw: bool = Field(default=True, env='USE_HNSW')
    hnsw_threshold: int = Field(default=1000, env='HNSW_THRESHOLD')
    hybrid_alpha: float = Field(default=0.7, env='HYBRID_ALPHA')
    bm25_enabled: bool = Field(default=True, env='BM25_ENABLED')
    chunk_size: int = Field(default=512, env='CHUNK_SIZE')
    chunk_overlap: int = Field(default=50, env='CHUNK_OVERLAP')
    use_hierarchical_chunking: bool = Field(default=True, env='USE_HIERARCHICAL_CHUNKING')
    enable_query_enhancement: bool = Field(default=True, env='ENABLE_QUERY_ENHANCEMENT')
    multi_query_count: int = Field(default=3, env='MULTI_QUERY_COUNT')
    enable_reranking: bool = Field(default=True, env='ENABLE_RERANKING')
    reranking_fusion_weight: float = Field(default=0.7, env='RERANKING_FUSION_WEIGHT')
    score_threshold: Optional[float] = Field(default=None, env='SCORE_THRESHOLD')
    default_top_k: int = Field(default=5, env='DEFAULT_TOP_K')
    default_strategy: str = Field(default='multi_query', env='DEFAULT_STRATEGY')
    include_context: bool = Field(default=True, env='INCLUDE_CONTEXT')
    supported_extensions: list = Field(default=['.py', '.js', '.ts', '.java'], env='SUPPORTED_EXTENSIONS')
    exclude_dirs: list = Field(
        default=['venv', 'node_modules', '__pycache__', '.git', 'dist', 'build'],
        env='EXCLUDE_DIRS'
    )
    batch_size: int = Field(default=32, env='BATCH_SIZE')
    max_workers: int = Field(default=4, env='MAX_WORKERS')
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
class AppConfig(BaseSettings):
    app_name: str = Field(default='Aura - Advanced RAG System', env='APP_NAME')
    app_version: str = Field(default='2.0.0', env='APP_VERSION')
    debug: bool = Field(default=False, env='DEBUG')
    host: str = Field(default='0.0.0.0', env='HOST')
    port: int = Field(default=8000, env='PORT')
    reload: bool = Field(default=False, env='RELOAD')
    log_level: str = Field(default='INFO', env='LOG_LEVEL')
    log_file: Optional[str] = Field(default=None, env='LOG_FILE')
    upload_dir: str = Field(default='uploads', env='UPLOAD_DIR')
    extracted_dir: str = Field(default='extracted', env='EXTRACTED_DIR')
    reports_dir: str = Field(default='reports', env='REPORTS_DIR')
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
rag_config = RAGConfig()
app_config = AppConfig()
def get_rag_config() -> RAGConfig:
    return rag_config
def get_app_config() -> AppConfig:
    return app_config
def display_config():
    print("=" * 60)
    print("RAG Configuration")
    print("=" * 60)
    print(f"LLM Provider: {rag_config.llm_provider}")
    if rag_config.llm_provider == 'gemini':
        print(f"Gemini Model: {rag_config.gemini_model}")
        print(f"Gemini Temperature: {rag_config.gemini_temperature}")
    print(f"Embedding Model: {rag_config.embedding_model}")
    print(f"Reranker Model: {rag_config.reranker_model}")
    print(f"Hybrid Alpha (Vector Weight): {rag_config.hybrid_alpha}")
    print(f"BM25 Enabled: {rag_config.bm25_enabled}")
    print(f"Query Enhancement: {rag_config.enable_query_enhancement}")
    print(f"Reranking Enabled: {rag_config.enable_reranking}")
    print(f"Default Strategy: {rag_config.default_strategy}")
    print(f"Default Top-K: {rag_config.default_top_k}")
    print(f"Index Directory: {rag_config.index_dir}")
    print("=" * 60)
    print("Application Configuration")
    print("=" * 60)
    print(f"App Name: {app_config.app_name}")
    print(f"Version: {app_config.app_version}")
    print(f"Host: {app_config.host}:{app_config.port}")
    print(f"Debug: {app_config.debug}")
    print(f"Log Level: {app_config.log_level}")
    print("=" * 60)
if __name__ == "__main__":
    display_config()
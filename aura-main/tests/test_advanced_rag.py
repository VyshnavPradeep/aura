import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import os
sys.path.insert(0, str(Path(__file__).parent.parent))
from rag.advanced_rag import AdvancedRAG
from rag.contextual_chunker import ContextualChunker
from rag.hybrid_retriever import HybridRetriever
from rag.query_enhancer import QueryEnhancer
from rag.document_reranker import DocumentReranker
SAMPLE_CODE = '''
import hashlib
from typing import Optional
class UserAuth:
    def __init__(self, db_connection):
        self.db = db_connection
    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.db.get_user(username)
        if not user:
            return False
        password_hash = self._hash_password(password)
        return user.password_hash == password_hash
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
def validate_email(email: str) -> bool:
    return '@' in email and '.' in email.split('@')[1]
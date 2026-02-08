from dotenv import load_dotenv
load_dotenv()  # Load environment variables before importing agents

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import uploads, analyze, rag

app = FastAPI(
    title="Marathon Backend Testing Agent",
    description="Autonomous agent for backend code analysis, security scanning, test generation, and advanced RAG search",
    version="2.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uploads.router)
app.include_router(analyze.router)
app.include_router(rag.router)
@app.get("/")
def health():
    return {
        "status": "aura is running",
        "version": "2.0.0",
        "features": [
            "code_analysis",
            "security_scanning",
            "test_generation",
            "advanced_rag_search"
        ]
    }
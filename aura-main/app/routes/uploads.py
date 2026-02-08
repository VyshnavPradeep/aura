from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import uuid
from datetime import datetime
from utils.file_handler import FileHandler
from utils.language_detector import LanguageDetector
from utils.ast_parser import ASTParser
from rag.code_embedder import CodeEmbedder
router = APIRouter(prefix="/upload", tags=["Upload"])
UPLOAD_DIR = "uploads"
file_handler = FileHandler(upload_dir=UPLOAD_DIR, extract_dir="extracted")
language_detector = LanguageDetector()
ast_parser = ASTParser()
code_embedder = CodeEmbedder()
@router.post("/")
async def upload_code(file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are accepted")
    project_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, f"{project_id}.zip")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        extraction_result = file_handler.extract_zip(file_path, project_id)
        if not extraction_result["success"]:
            raise HTTPException(status_code=400, detail=f"ZIP extraction failed: {extraction_result.get('error')}")
        detection_result = language_detector.detect(
            extraction_result["project_dir"],
            extraction_result["file_structure"]
        )
        if not detection_result["success"]:
            raise HTTPException(status_code=500, detail=f"Language detection failed: {detection_result.get('error')}")
        parsing_result = ast_parser.parse_project(
            extraction_result["project_dir"],
            extraction_result["file_structure"]["code_files"],
            detection_result["language"]
        )
        embedding_result = code_embedder.process_project(parsing_result, project_id)
        return {
            "status": "success",
            "message": "Code uploaded and processed successfully",
            "project_id": project_id,
            "filename": file.filename,
            "extraction": {
                "total_files": extraction_result["total_files"],
                "code_files": extraction_result["code_files"],
                "project_dir": extraction_result["project_dir"]
            },
            "detection": {
                "language": detection_result["language"],
                "confidence": detection_result["language_confidence"],
                "framework": detection_result["framework"],
                "dependencies": detection_result["metadata"].get("dependency_count", 0)
            },
            "parsing": {
                "files_parsed": parsing_result["files_parsed"],
                "total_functions": parsing_result["total_functions"],
                "total_classes": parsing_result["total_classes"],
                "total_lines": parsing_result["total_lines"],
                "summary": parsing_result["summary"]
            },
            "embeddings": {
                "chunks_created": embedding_result.get("chunks_count", 0),
                "index_created": embedding_result.get("success", False)
            },
            "next_steps": [
                "Run security analysis",
                "Execute test generation",
                "Perform scalability assessment",
                "Analyze database queries"
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
@router.get("/projects")
async def list_projects():
    try:
        extracted_dir = "extracted"
        if not os.path.exists(extracted_dir):
            return {"projects": []}
        projects = [d for d in os.listdir(extracted_dir) if os.path.isdir(os.path.join(extracted_dir, d))]
        return {"projects": projects, "count": len(projects)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    try:
        success = file_handler.cleanup_project(project_id)
        if success:
            return {"message": f"Project {project_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
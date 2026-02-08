import os
import zipfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class FileHandler:
    def __init__(self, upload_dir: str = "uploads", extract_dir: str = "extracted"):
        self.upload_dir = Path(upload_dir)
        self.extract_dir = Path(extract_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self.extract_dir.mkdir(exist_ok=True)
    def extract_zip(self, zip_path: str, project_id: str) -> Dict[str, any]:
        try:
            project_dir = self.extract_dir / project_id
            project_dir.mkdir(exist_ok=True)
            if not zipfile.is_zipfile(zip_path):
                raise ValueError("Invalid ZIP file")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_info in zip_ref.namelist():
                    if file_info.startswith('/') or '..' in file_info:
                        raise ValueError(f"Unsafe file path detected: {file_info}")
                zip_ref.extractall(project_dir)
            logger.info(f"Extracted ZIP to: {project_dir}")
            file_structure = self._analyze_structure(project_dir)
            return {
                "success": True,
                "project_id": project_id,
                "project_dir": str(project_dir),
                "file_structure": file_structure,
                "total_files": len(file_structure["all_files"]),
                "code_files": len(file_structure["code_files"])
            }
        except Exception as e:
            logger.error(f"ZIP extraction failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    def _analyze_structure(self, project_dir: Path) -> Dict[str, List[str]]:
        code_extensions = {
            '.py', '.js', '.java', '.go', '.ts', '.jsx', '.tsx',
            '.rb', '.php', '.cs', '.cpp', '.c', '.rs', '.kt'
        }
        config_files = {
            'requirements.txt', 'package.json', 'pom.xml', 'build.gradle',
            'go.mod', 'Cargo.toml', 'composer.json', 'Gemfile'
        }
        all_files = []
        code_files = []
        config_files_found = []
        for root, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in {
                'node_modules', 'venv', '__pycache__', '.git',
                'dist', 'build', 'target', '.idea'
            }]
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(project_dir)
                all_files.append(str(relative_path))
                if file_path.suffix in code_extensions:
                    code_files.append(str(relative_path))
                if file in config_files:
                    config_files_found.append(str(relative_path))
        return {
            "all_files": all_files,
            "code_files": code_files,
            "config_files": config_files_found
        }
    def cleanup_project(self, project_id: str) -> bool:
        try:
            project_dir = self.extract_dir / project_id
            if project_dir.exists():
                shutil.rmtree(project_dir)
                logger.info(f"Cleaned up project: {project_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            return False
    def get_file_content(self, project_id: str, file_path: str) -> Optional[str]:
        try:
            full_path = self.extract_dir / project_id / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {str(e)}")
            return None
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
logger = logging.getLogger(__name__)
class LanguageDetector:
    LANGUAGE_PATTERNS = {
        'python': {
            'extensions': ['.py'],
            'config_files': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
            'keywords': ['import', 'def', 'class', 'from']
        },
        'javascript': {
            'extensions': ['.js', '.mjs', '.cjs'],
            'config_files': ['package.json', 'package-lock.json'],
            'keywords': ['require(', 'import ', 'export ', 'function']
        },
        'typescript': {
            'extensions': ['.ts', '.tsx'],
            'config_files': ['tsconfig.json', 'package.json'],
            'keywords': ['interface', 'type ', 'import ', 'export ']
        },
        'java': {
            'extensions': ['.java'],
            'config_files': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
            'keywords': ['public class', 'import java', 'package ']
        },
        'go': {
            'extensions': ['.go'],
            'config_files': ['go.mod', 'go.sum'],
            'keywords': ['package ', 'import ', 'func ', 'type ']
        }
    }
    FRAMEWORK_PATTERNS = {
        'python': {
            'fastapi': ['from fastapi', 'import fastapi', 'FastAPI('],
            'django': ['from django', 'django.', 'DJANGO_SETTINGS_MODULE'],
            'flask': ['from flask', 'import Flask', 'Flask(__name__)'],
            'tornado': ['import tornado', 'tornado.web'],
            'aiohttp': ['from aiohttp', 'import aiohttp']
        },
        'javascript': {
            'express': ['require("express")', 'require(\'express\')', 'from "express"', 'express()'],
            'nestjs': ['@nestjs/', 'NestFactory', '@Module('],
            'koa': ['require("koa")', 'require(\'koa\')', 'new Koa()'],
            'hapi': ['require("@hapi/hapi")', 'Hapi.server(']
        },
        'typescript': {
            'express': ['express', 'Express', 'from "express"'],
            'nestjs': ['@nestjs/', 'NestFactory', '@Module(', '@Controller('],
            'fastify': ['fastify', 'from "fastify"']
        },
        'java': {
            'spring': ['@SpringBootApplication', 'org.springframework', '@RestController'],
            'micronaut': ['io.micronaut', '@Controller'],
            'quarkus': ['io.quarkus', '@Path']
        },
        'go': {
            'gin': ['github.com/gin-gonic/gin', 'gin.Default()', 'gin.New()'],
            'echo': ['github.com/labstack/echo', 'echo.New()'],
            'fiber': ['github.com/gofiber/fiber', 'fiber.New()'],
            'gorilla': ['github.com/gorilla/mux', 'mux.NewRouter()']
        }
    }
    def detect(self, project_dir: str, file_structure: Dict) -> Dict[str, any]:
        try:
            language_scores = self._score_languages(file_structure)
            primary_language = max(language_scores, key=language_scores.get) if language_scores else 'unknown'
            framework = self._detect_framework(
                project_dir,
                primary_language,
                file_structure['code_files']
            )
            metadata = self._extract_metadata(project_dir, primary_language)
            return {
                "success": True,
                "language": primary_language,
                "language_confidence": language_scores.get(primary_language, 0),
                "all_languages": language_scores,
                "framework": framework,
                "metadata": metadata
            }
        except Exception as e:
            logger.error(f"Language detection failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    def _score_languages(self, file_structure: Dict) -> Dict[str, float]:
        scores = {}
        code_files = file_structure.get('code_files', [])
        config_files = file_structure.get('config_files', [])
        for language, patterns in self.LANGUAGE_PATTERNS.items():
            score = 0
            for file in code_files:
                if any(file.endswith(ext) for ext in patterns['extensions']):
                    score += 1
            for config in config_files:
                config_name = os.path.basename(config)
                if config_name in patterns['config_files']:
                    score += 5
            if score > 0:
                scores[language] = score
        total = sum(scores.values()) if scores else 1
        return {lang: score / total for lang, score in scores.items()}
    def _detect_framework(self, project_dir: str, language: str, code_files: List[str]) -> Optional[str]:
        if language not in self.FRAMEWORK_PATTERNS:
            return None
        framework_indicators = self.FRAMEWORK_PATTERNS[language]
        framework_scores = {fw: 0 for fw in framework_indicators.keys()}
        files_to_scan = code_files[:20]
        for file_path in files_to_scan:
            try:
                full_path = Path(project_dir) / file_path
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for framework, patterns in framework_indicators.items():
                        for pattern in patterns:
                            if pattern in content:
                                framework_scores[framework] += 1
            except Exception as e:
                logger.warning(f"Could not scan file {file_path}: {str(e)}")
                continue
        detected = max(framework_scores, key=framework_scores.get)
        return detected if framework_scores[detected] > 0 else None
    def _extract_metadata(self, project_dir: str, language: str) -> Dict[str, any]:
        metadata = {}
        project_path = Path(project_dir)
        try:
            if language == 'python':
                req_file = project_path / 'requirements.txt'
                if req_file.exists():
                    with open(req_file, 'r') as f:
                        deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                        metadata['dependencies'] = deps
                        metadata['dependency_count'] = len(deps)
                pyproject = project_path / 'pyproject.toml'
                if pyproject.exists():
                    metadata['build_system'] = 'pyproject.toml found'
            elif language in ['javascript', 'typescript']:
                pkg_file = project_path / 'package.json'
                if pkg_file.exists():
                    with open(pkg_file, 'r') as f:
                        pkg_data = json.load(f)
                        metadata['name'] = pkg_data.get('name', 'unknown')
                        metadata['version'] = pkg_data.get('version', 'unknown')
                        metadata['dependencies'] = list(pkg_data.get('dependencies', {}).keys())
                        metadata['devDependencies'] = list(pkg_data.get('devDependencies', {}).keys())
                        metadata['dependency_count'] = len(metadata['dependencies'])
            elif language == 'java':
                pom_file = project_path / 'pom.xml'
                if pom_file.exists():
                    metadata['build_system'] = 'maven'
                gradle_file = project_path / 'build.gradle'
                if gradle_file.exists():
                    metadata['build_system'] = 'gradle'
            elif language == 'go':
                go_mod = project_path / 'go.mod'
                if go_mod.exists():
                    with open(go_mod, 'r') as f:
                        content = f.read()
                        for line in content.split('\n'):
                            if line.startswith('module '):
                                metadata['module'] = line.replace('module ', '').strip()
                                break
        except Exception as e:
            logger.warning(f"Metadata extraction failed: {str(e)}")
        return metadata
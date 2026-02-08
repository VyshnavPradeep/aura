import ast
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
logger = logging.getLogger(__name__)
class ASTParser:
    def __init__(self):
        self.parsers = {}
        self._init_parsers()
    def _init_parsers(self):
        try:
            from tree_sitter import Language, Parser
            self.tree_sitter_available = True
        except ImportError:
            logger.warning("tree-sitter not available. Python-only parsing enabled.")
            self.tree_sitter_available = False
    def parse_file(self, file_path: str, language: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if language == 'python':
                return self._parse_python(content, file_path)
            elif language in ['javascript', 'typescript']:
                return self._parse_js_ts(content, file_path, language)
            elif language == 'java':
                return self._parse_java(content, file_path)
            elif language == 'go':
                return self._parse_go(content, file_path)
            else:
                return self._parse_generic(content, file_path)
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {str(e)}")
            return {
                "success": False,
                "file_path": file_path,
                "error": str(e)
            }
    def _parse_python(self, content: str, file_path: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(content)
            functions = []
            classes = []
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                        "decorators": [self._get_decorator_name(d) for d in node.decorator_list]
                    })
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "bases": [self._get_base_name(b) for b in node.bases],
                        "methods": methods,
                        "decorators": [self._get_decorator_name(d) for d in node.decorator_list]
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        module = node.module or ""
                        imports.extend([f"{module}.{alias.name}" for alias in node.names])
            return {
                "success": True,
                "file_path": file_path,
                "language": "python",
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "stats": {
                    "function_count": len(functions),
                    "class_count": len(classes),
                    "import_count": len(imports),
                    "lines": len(content.split('\n'))
                }
            }
        except SyntaxError as e:
            logger.warning(f"Python syntax error in {file_path}: {str(e)}")
            return {
                "success": False,
                "file_path": file_path,
                "error": f"Syntax error: {str(e)}"
            }
    def _parse_js_ts(self, content: str, file_path: str, language: str) -> Dict[str, Any]:
        functions = []
        classes = []
        imports = []
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if 'function ' in stripped:
                func_name = self._extract_js_function_name(stripped)
                if func_name:
                    functions.append({"name": func_name, "line": i, "type": "function"})
            if (' = (' in stripped or ' = async (' in stripped) and '=>' in stripped:
                func_name = stripped.split('=')[0].strip().split()[-1] if '=' in stripped else None
                if func_name:
                    functions.append({"name": func_name, "line": i, "type": "arrow_function"})
            if stripped.startswith('class '):
                class_name = stripped.split('class ')[1].split()[0].split('{')[0].strip()
                classes.append({"name": class_name, "line": i})
            if stripped.startswith('import ') or stripped.startswith('const ') and 'require(' in stripped:
                imports.append({"line": i, "statement": stripped[:100]})
        return {
            "success": True,
            "file_path": file_path,
            "language": language,
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "stats": {
                "function_count": len(functions),
                "class_count": len(classes),
                "import_count": len(imports),
                "lines": len(lines)
            }
        }
    def _parse_java(self, content: str, file_path: str) -> Dict[str, Any]:
        functions = []
        classes = []
        imports = []
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if 'class ' in stripped and not stripped.startswith('//'):
                parts = stripped.split('class ')
                if len(parts) > 1:
                    class_name = parts[1].split()[0].split('{')[0].strip()
                    classes.append({"name": class_name, "line": i})
            if any(mod in stripped for mod in ['public ', 'private ', 'protected ']):
                if '(' in stripped and ')' in stripped and '{' in stripped or stripped.endswith(';'):
                    parts = stripped.split('(')[0].strip().split()
                    if len(parts) >= 2:
                        method_name = parts[-1]
                        functions.append({"name": method_name, "line": i})
            if stripped.startswith('import '):
                imports.append({"line": i, "statement": stripped})
        return {
            "success": True,
            "file_path": file_path,
            "language": "java",
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "stats": {
                "function_count": len(functions),
                "class_count": len(classes),
                "import_count": len(imports),
                "lines": len(lines)
            }
        }
    def _parse_go(self, content: str, file_path: str) -> Dict[str, Any]:
        functions = []
        structs = []
        imports = []
        lines = content.split('\n')
        in_import_block = False
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('func '):
                func_part = stripped.split('func ')[1]
                if func_part.startswith('('):
                    func_name = func_part.split(')')[1].strip().split('(')[0].strip()
                else:
                    func_name = func_part.split('(')[0].strip()
                functions.append({"name": func_name, "line": i})
            if 'type ' in stripped and ' struct' in stripped:
                struct_name = stripped.split('type ')[1].split(' struct')[0].strip()
                structs.append({"name": struct_name, "line": i})
            if stripped.startswith('import ('):
                in_import_block = True
            elif in_import_block:
                if stripped == ')':
                    in_import_block = False
                elif stripped and not stripped.startswith('//'):
                    imports.append({"line": i, "statement": stripped})
            elif stripped.startswith('import '):
                imports.append({"line": i, "statement": stripped})
        return {
            "success": True,
            "file_path": file_path,
            "language": "go",
            "functions": functions,
            "classes": structs,
            "imports": imports,
            "stats": {
                "function_count": len(functions),
                "class_count": len(structs),
                "import_count": len(imports),
                "lines": len(lines)
            }
        }
    def _parse_generic(self, content: str, file_path: str) -> Dict[str, Any]:
        lines = content.split('\n')
        return {
            "success": True,
            "file_path": file_path,
            "language": "generic",
            "stats": {
                "lines": len(lines),
                "size_bytes": len(content)
            }
        }
    def parse_project(self, project_dir: str, code_files: List[str], language: str) -> Dict[str, Any]:
        parsed_files = []
        total_functions = 0
        total_classes = 0
        total_imports = 0
        total_lines = 0
        for file_rel_path in code_files[:50]:
            file_path = Path(project_dir) / file_rel_path
            if file_path.exists():
                result = self.parse_file(str(file_path), language)
                if result.get("success"):
                    parsed_files.append(result)
                    stats = result.get("stats", {})
                    total_functions += stats.get("function_count", 0)
                    total_classes += stats.get("class_count", 0)
                    total_imports += stats.get("import_count", 0)
                    total_lines += stats.get("lines", 0)
        return {
            "success": True,
            "files_parsed": len(parsed_files),
            "total_functions": total_functions,
            "total_classes": total_classes,
            "total_imports": total_imports,
            "total_lines": total_lines,
            "parsed_files": parsed_files[:10],
            "summary": {
                "avg_functions_per_file": total_functions / len(parsed_files) if parsed_files else 0,
                "avg_classes_per_file": total_classes / len(parsed_files) if parsed_files else 0,
                "avg_lines_per_file": total_lines / len(parsed_files) if parsed_files else 0
            }
        }
    def _get_decorator_name(self, decorator) -> str:
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        return str(decorator)
    def _get_base_name(self, base) -> str:
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{self._get_base_name(base.value)}.{base.attr}"
        return str(base)
    def _extract_js_function_name(self, line: str) -> Optional[str]:
        try:
            if 'function ' in line:
                parts = line.split('function ')[1].split('(')[0].strip()
                return parts if parts else None
        except:
            return None
        return None
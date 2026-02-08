from typing import List, Dict, Any, Optional
import ast
import logging
from pathlib import Path
logger = logging.getLogger(__name__)
class ContextualChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunk_counter = 0
    def create_hierarchical_chunks(
        self,
        code: str,
        file_path: str,
        language: str = "python"
    ) -> List[Dict[str, Any]]:
        if language.lower() != "python":
            logger.warning(f"Language {language} not fully supported, using text chunking")
            return self._fallback_text_chunking(code, file_path)
        chunks = []
        try:
            tree = ast.parse(code)
            file_context = self._extract_file_context(tree, code, file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_chunks = self._process_class(node, code, file_path, file_context)
                    chunks.extend(class_chunks)
                elif isinstance(node, ast.FunctionDef):
                    if self._is_module_level_function(node, tree):
                        func_chunk = self._process_function(node, code, file_path, file_context)
                        if func_chunk:
                            chunks.append(func_chunk)
            logger.info(f"Created {len(chunks)} hierarchical chunks from {file_path}")
            return chunks
        except SyntaxError as e:
            logger.warning(f"Syntax error parsing {file_path}: {str(e)}")
            return self._fallback_text_chunking(code, file_path)
        except Exception as e:
            logger.error(f"Error creating chunks for {file_path}: {str(e)}")
            return self._fallback_text_chunking(code, file_path)
    def _extract_file_context(self, tree: ast.AST, code: str, file_path: str) -> str:
        context_parts = [f"File: {file_path}"]
        module_docstring = ast.get_docstring(tree)
        if module_docstring:
            context_parts.append(f"Purpose: {module_docstring[:200]}")
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        if imports:
            context_parts.append(f"Dependencies: {', '.join(imports[:10])}")
        return " | ".join(context_parts)
    def _process_class(
        self,
        node: ast.ClassDef,
        code: str,
        file_path: str,
        file_context: str
    ) -> List[Dict[str, Any]]:
        chunks = []
        class_id = f"{file_path}:class:{node.name}:{node.lineno}"
        self.chunk_counter += 1
        try:
            class_code = ast.get_source_segment(code, node)
            if class_code is None:
                class_code = f"class {node.name}..."
        except:
            class_code = f"class {node.name}..."
        class_context = self._extract_class_context(node, code, file_context)
        parent_chunk = {
            'id': self.chunk_counter,
            'chunk_id': class_id,
            'type': 'parent',
            'chunk_type': 'class',
            'name': node.name,
            'file': file_path,
            'line': node.lineno,
            'content': class_code[:2000],
            'text': class_context,
            'context': class_context,
            'children': [],
            'metadata': {
                'base_classes': [ast.unparse(base) for base in node.bases],
                'decorators': [ast.unparse(dec) for dec in node.decorator_list],
                'docstring': ast.get_docstring(node),
                'num_methods': len([n for n in node.body if isinstance(n, ast.FunctionDef)])
            }
        }
        chunks.append(parent_chunk)
        parent_index = len(chunks) - 1
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_chunk = self._process_method(
                    item,
                    code,
                    file_path,
                    node.name,
                    class_id,
                    class_context
                )
                if method_chunk:
                    self.chunk_counter += 1
                    method_chunk['id'] = self.chunk_counter
                    chunks.append(method_chunk)
                    chunks[parent_index]['children'].append(method_chunk['chunk_id'])
        return chunks
    def _extract_class_context(self, node: ast.ClassDef, code: str, file_context: str) -> str:
        context_parts = [
            f"Class: {node.name}",
            file_context
        ]
        docstring = ast.get_docstring(node)
        if docstring:
            context_parts.append(f"Description: {docstring[:300]}")
        if node.bases:
            bases = [ast.unparse(base) for base in node.bases]
            context_parts.append(f"Inherits from: {', '.join(bases)}")
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        if methods:
            context_parts.append(f"Methods: {', '.join(methods[:10])}")
        if node.decorator_list:
            decorators = [ast.unparse(dec) for dec in node.decorator_list]
            context_parts.append(f"Decorators: {', '.join(decorators)}")
        return " | ".join(context_parts)
    def _process_method(
        self,
        node: ast.FunctionDef,
        code: str,
        file_path: str,
        class_name: str,
        parent_id: str,
        class_context: str
    ) -> Optional[Dict[str, Any]]:
        method_id = f"{parent_id}:method:{node.name}:{node.lineno}"
        try:
            method_code = ast.get_source_segment(code, node)
            if method_code is None:
                method_code = f"def {node.name}()..."
        except:
            method_code = f"def {node.name}()..."
        method_context = self._extract_method_context(node, class_name, class_context)
        return {
            'chunk_id': method_id,
            'type': 'child',
            'chunk_type': 'method',
            'name': node.name,
            'file': file_path,
            'line': node.lineno,
            'content': method_code[:1500],
            'text': method_context,
            'context': method_context,
            'parent_id': parent_id,
            'parent_class': class_name,
            'metadata': {
                'parameters': [arg.arg for arg in node.args.args],
                'decorators': [ast.unparse(dec) for dec in node.decorator_list],
                'docstring': ast.get_docstring(node),
                'is_async': isinstance(node, ast.AsyncFunctionDef),
                'returns': ast.unparse(node.returns) if node.returns else None
            }
        }
    def _extract_method_context(self, node: ast.FunctionDef, class_name: str, class_context: str) -> str:
        context_parts = [
            f"Method: {node.name} in class {class_name}",
            class_context
        ]
        params = [arg.arg for arg in node.args.args]
        if params:
            context_parts.append(f"Parameters: {', '.join(params)}")
        if node.returns:
            context_parts.append(f"Returns: {ast.unparse(node.returns)}")
        docstring = ast.get_docstring(node)
        if docstring:
            context_parts.append(f"Description: {docstring[:200]}")
        if isinstance(node, ast.AsyncFunctionDef):
            context_parts.append("Async method")
        return " | ".join(context_parts)
    def _process_function(
        self,
        node: ast.FunctionDef,
        code: str,
        file_path: str,
        file_context: str
    ) -> Optional[Dict[str, Any]]:
        func_id = f"{file_path}:function:{node.name}:{node.lineno}"
        self.chunk_counter += 1
        try:
            func_code = ast.get_source_segment(code, node)
            if func_code is None:
                func_code = f"def {node.name}()..."
        except:
            func_code = f"def {node.name}()..."
        func_context = self._extract_function_context(node, file_context)
        return {
            'id': self.chunk_counter,
            'chunk_id': func_id,
            'type': 'standalone',
            'chunk_type': 'function',
            'name': node.name,
            'file': file_path,
            'line': node.lineno,
            'content': func_code[:1500],
            'text': func_context,
            'context': func_context,
            'metadata': {
                'parameters': [arg.arg for arg in node.args.args],
                'decorators': [ast.unparse(dec) for dec in node.decorator_list],
                'docstring': ast.get_docstring(node),
                'is_async': isinstance(node, ast.AsyncFunctionDef),
                'returns': ast.unparse(node.returns) if node.returns else None
            }
        }
    def _extract_function_context(self, node: ast.FunctionDef, file_context: str) -> str:
        context_parts = [
            f"Function: {node.name}",
            file_context
        ]
        params = [arg.arg for arg in node.args.args]
        if params:
            context_parts.append(f"Parameters: {', '.join(params)}")
        if node.returns:
            context_parts.append(f"Returns: {ast.unparse(node.returns)}")
        docstring = ast.get_docstring(node)
        if docstring:
            context_parts.append(f"Description: {docstring[:200]}")
        if node.decorator_list:
            decorators = [ast.unparse(dec) for dec in node.decorator_list]
            context_parts.append(f"Decorators: {', '.join(decorators)}")
        return " | ".join(context_parts)
    def _is_module_level_function(self, func_node: ast.FunctionDef, tree: ast.AST) -> bool:
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if item is func_node:
                        return False
        return True
    def _fallback_text_chunking(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        lines = code.split('\n')
        chunks = []
        i = 0
        while i < len(lines):
            chunk_lines = lines[i:i + self.chunk_size]
            chunk_text = '\n'.join(chunk_lines)
            self.chunk_counter += 1
            chunks.append({
                'id': self.chunk_counter,
                'chunk_id': f"{file_path}:text:{i}",
                'type': 'text',
                'chunk_type': 'text',
                'file': file_path,
                'line': i + 1,
                'content': chunk_text,
                'text': chunk_text[:500],
                'context': f"Code from {file_path} starting at line {i+1}"
            })
            i += self.chunk_size - self.overlap
        logger.info(f"Created {len(chunks)} text chunks (fallback mode)")
        return chunks
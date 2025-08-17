"""
AST Parser for extracting Python code structure.

This module provides functionality to parse Python files and extract
class definitions, function definitions, and their hierarchical structure.
"""

import ast
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CodeElement:
    """Represents a code element (class, function, method, etc.)"""
    name: str
    type: str  # 'class', 'function', 'method', 'async_function', 'async_method'
    line_start: int
    line_end: int
    docstring: Optional[str] = None
    parent: Optional[str] = None
    children: List['CodeElement'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class ASTParser:
    """Parser for extracting code structure from Python files."""
    
    def __init__(self):
        self.current_class = None
    
    def parse_file(self, file_path: Path) -> List[CodeElement]:
        """
        Parse a Python file and extract its code structure.
        
        Args:
            file_path: Path to the Python file to parse
            
        Returns:
            List of CodeElement objects representing the file structure
        """
        try:
            # Try different encodings
            content = None
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                print(f"Could not decode file {file_path} with any encoding")
                return []
            
            # Remove BOM if present
            if content.startswith('\ufeff'):
                content = content[1:]
            
            tree = ast.parse(content)
            elements = []
            
            # Use a more robust approach to find top-level elements
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    element = self._parse_class(node)
                    elements.append(element)
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    element = self._parse_function(node)
                    elements.append(element)
            
            return elements
            
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            return []
    
    def _parse_class(self, node: ast.ClassDef) -> CodeElement:
        """Parse a class definition node."""
        docstring = ast.get_docstring(node)
        
        element = CodeElement(
            name=node.name,
            type='class',
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=docstring
        )
        
        # Parse methods within the class
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method = self._parse_function(item, parent_class=node.name)
                element.children.append(method)
        
        return element
    
    def _parse_function(self, node: ast.FunctionDef, parent_class: str = None) -> CodeElement:
        """Parse a function or method definition node."""
        docstring = ast.get_docstring(node)
        
        if parent_class:
            func_type = 'async_method' if isinstance(node, ast.AsyncFunctionDef) else 'method'
        else:
            func_type = 'async_function' if isinstance(node, ast.AsyncFunctionDef) else 'function'
        
        return CodeElement(
            name=node.name,
            type=func_type,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=docstring,
            parent=parent_class
        )
    
    def get_python_files(self, directory: Path) -> List[Path]:
        """
        Get all Python files in a directory recursively.
        
        Args:
            directory: Directory to search for Python files
            
        Returns:
            List of Path objects for Python files
        """
        python_files = []
        
        try:
            for root, dirs, files in os.walk(directory):
                # Skip common non-source directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
                
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(Path(root) / file)
        
        except Exception as e:
            print(f"Error scanning directory {directory}: {e}")
        
        return python_files
    
    def get_file_content_lines(self, file_path: Path, start_line: int = None, end_line: int = None) -> str:
        """
        Get specific lines from a file.
        
        Args:
            file_path: Path to the file
            start_line: Starting line number (1-based)
            end_line: Ending line number (1-based)
            
        Returns:
            Content of the specified lines
        """
        try:
            # Try different encodings
            lines = None
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        lines = f.readlines()
                    break
                except UnicodeDecodeError:
                    continue
            
            if lines is None:
                return f"Could not decode file {file_path} with any encoding"
            
            # Remove BOM from first line if present
            if lines and lines[0].startswith('\ufeff'):
                lines[0] = lines[0][1:]
            
            if start_line is None and end_line is None:
                return ''.join(lines)
            
            start_idx = (start_line - 1) if start_line else 0
            end_idx = end_line if end_line else len(lines)
            
            return ''.join(lines[start_idx:end_idx])
            
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return f"Error reading file: {str(e)}"
    
    def parse_file_to_dict(self, file_path: Path) -> Dict[str, Any]:
        """
        Use Python ast to parse a file and extract:
        - All top-level class definitions
        - All function definitions
        Return as nested dictionary for tree visualization
        
        Args:
            file_path: Path to the Python file to parse
            
        Returns:
            Dictionary with structure like:
            {
                "MyClass": {
                    "type": "class",
                    "line_start": 10,
                    "line_end": 50,
                    "docstring": "Class documentation",
                    "methods": ["method_one", "method_two"],
                    "children": {
                        "method_one": {
                            "type": "method",
                            "line_start": 15,
                            "line_end": 25,
                            "docstring": "Method documentation"
                        }
                    }
                },
                "function_one": {
                    "type": "function",
                    "line_start": 60,
                    "line_end": 70,
                    "docstring": "Function documentation"
                }
            }
        """
        try:
            # Try different encodings
            content = None
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                return {"_error": f"Could not decode file {file_path} with any encoding"}
            
            # Remove BOM if present
            if content.startswith('\ufeff'):
                content = content[1:]
            
            tree = ast.parse(content)
            result = {}
            
            # Parse top-level elements
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    class_info = self._parse_class_to_dict(node)
                    result[node.name] = class_info
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_info = self._parse_function_to_dict(node)
                    result[node.name] = func_info
            
            return result
            
        except Exception as e:
            return {"_error": f"Error parsing file {file_path}: {str(e)}"}
    
    def _parse_class_to_dict(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Parse a class definition node to dictionary format."""
        docstring = ast.get_docstring(node)
        
        class_info = {
            "type": "class",
            "line_start": node.lineno,
            "line_end": node.end_lineno or node.lineno,
            "docstring": docstring,
            "methods": [],
            "children": {}
        }
        
        # Parse methods within the class
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_name = item.name
                class_info["methods"].append(method_name)
                
                method_info = self._parse_function_to_dict(item, is_method=True)
                class_info["children"][method_name] = method_info
        
        return class_info
    
    def _parse_function_to_dict(self, node: ast.FunctionDef, is_method: bool = False) -> Dict[str, Any]:
        """Parse a function or method definition node to dictionary format."""
        docstring = ast.get_docstring(node)
        
        func_type = "method" if is_method else "function"
        if isinstance(node, ast.AsyncFunctionDef):
            func_type = "async_method" if is_method else "async_function"
        
        return {
            "type": func_type,
            "line_start": node.lineno,
            "line_end": node.end_lineno or node.lineno,
            "docstring": docstring,
            "args": [arg.arg for arg in node.args.args],
            "returns": self._get_return_annotation(node)
        }
    
    def _get_return_annotation(self, node: ast.FunctionDef) -> Optional[str]:
        """Extract return type annotation if present."""
        if node.returns:
            try:
                return ast.unparse(node.returns)
            except:
                return None
        return None
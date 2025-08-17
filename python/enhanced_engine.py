#!/usr/bin/env python3
"""
Enhanced VS Code Extension Python Bridge with Code Indexer
This script serves as a bridge between the VS Code extension and the holographic memory system,
with added functionality to scan Python files for holographic memory annotations.
"""

import sys
import json
import time
import traceback
import re
import ast
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import numpy as np

# Add parent directory to path so we can import from src
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))

# Import our holographic memory system
try:
    from src.lumina_memory.enhanced_xpunit import EnhancedXPEnvironment
    from src.lumina_memory.holographic_memory import (
        HolographicAssociativeMemory, MemoryCapsule, cosine_similarity
    )
    from memory_adapter import MemorySystemAdapter
except ImportError as e:
    print(f"Failed to import holographic memory system: {e}")
    print(f"Paths tried: {sys.path}")
    # Create a minimal fallback
    class MemorySystemAdapter:
        def __init__(self):
            self.capsules = []
        def list_capsules(self):
            return []
        def create_capsule(self, bindings):
            return {"success": True, "capsule": {"id": "demo"}}

class HolographicAnnotation:
    """Represents a holographic memory annotation found in code"""
    
    def __init__(self, capsule_id: str, file_path: Path, line_start: int, line_end: int):
        self.capsule_id = capsule_id
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end
        self.slots: Dict[str, str] = {}
        self.weights: Dict[str, float] = {}
        self.meta: Dict[str, Any] = {}
        self.annotation_type = "unknown"  # inline, docstring, decorator
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "capsule_id": self.capsule_id,
            "file_path": str(self.file_path),
            "line_start": self.line_start,
            "line_end": self.line_end,
            "slots": self.slots,
            "weights": self.weights,
            "meta": self.meta,
            "annotation_type": self.annotation_type
        }

class CodeIndexer:
    """Scans Python files for holographic memory annotations"""
    
    def __init__(self):
        self.annotations: List[HolographicAnnotation] = []
        
        # Regex patterns for different annotation styles
        self.inline_patterns = {
            'capsule': re.compile(r'#\s*@holo\s+capsule:\s*(.+)'),
            'role': re.compile(r'#\s*role:\s*(\w+)\s*=\s*["\']([^"\']+)["\']'),
            'weight': re.compile(r'#\s*weight:\s*(\w+)\s*=\s*([\d.]+)'),
            'meta': re.compile(r'#\s*meta:\s*(\w+)\s*=\s*(.+)')
        }
        
        # Pattern for docstring blocks
        self.docstring_pattern = re.compile(
            r'"""[\s\S]*?---\s*@holo\s*\n([\s\S]*?)"""',
            re.MULTILINE
        )
        
        # Pattern for decorator style
        self.decorator_pattern = re.compile(
            r'@holo\s*\(([\s\S]*?)\)',
            re.MULTILINE
        )
    
    def generate_capsule_id(self, file_path: Path, line_start: int) -> str:
        """Generate deterministic capsule ID from file path and line"""
        content = f"{file_path}:{line_start}"
        return f"cap-{hashlib.md5(content.encode()).hexdigest()[:8]}"
    
    def parse_inline_annotations(self, content: str, file_path: Path) -> List[HolographicAnnotation]:
        """Parse inline tag style annotations"""
        annotations = []
        lines = content.split('\n')
        current_annotation = None
        
        for i, line in enumerate(lines, 1):
            # Check for capsule start
            capsule_match = self.inline_patterns['capsule'].search(line)
            if capsule_match:
                if current_annotation:
                    current_annotation.line_end = i - 1
                    annotations.append(current_annotation)
                
                capsule_id = capsule_match.group(1).strip()
                if not capsule_id:
                    capsule_id = self.generate_capsule_id(file_path, i)
                
                current_annotation = HolographicAnnotation(capsule_id, file_path, i, i)
                current_annotation.annotation_type = "inline"
                continue
            
            if current_annotation:
                # Check for role
                role_match = self.inline_patterns['role'].search(line)
                if role_match:
                    role_name, role_value = role_match.groups()
                    current_annotation.slots[role_name] = role_value
                    continue
                
                # Check for weight
                weight_match = self.inline_patterns['weight'].search(line)
                if weight_match:
                    weight_name, weight_value = weight_match.groups()
                    current_annotation.weights[weight_name] = float(weight_value)
                    continue
                
                # Check for meta
                meta_match = self.inline_patterns['meta'].search(line)
                if meta_match:
                    meta_name, meta_value = meta_match.groups()
                    try:
                        # Try to parse as number
                        current_annotation.meta[meta_name] = float(meta_value)
                    except ValueError:
                        # Store as string
                        current_annotation.meta[meta_name] = meta_value.strip('"\'')
                    continue
                
                # If line doesn't match any pattern and isn't a comment, end current annotation
                if not line.strip().startswith('#'):
                    current_annotation.line_end = i - 1
                    annotations.append(current_annotation)
                    current_annotation = None
        
        # Don't forget the last annotation
        if current_annotation:
            current_annotation.line_end = len(lines)
            annotations.append(current_annotation)
        
        return annotations
    
    def parse_docstring_annotations(self, content: str, file_path: Path) -> List[HolographicAnnotation]:
        """Parse YAML-ish docstring annotations"""
        annotations = []
        
        for match in self.docstring_pattern.finditer(content):
            yaml_content = match.group(1)
            line_start = content[:match.start()].count('\n') + 1
            line_end = content[:match.end()].count('\n') + 1
            
            annotation = HolographicAnnotation("", file_path, line_start, line_end)
            annotation.annotation_type = "docstring"
            
            # Parse YAML-ish content
            for line in yaml_content.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('capsule:'):
                    annotation.capsule_id = line.split(':', 1)[1].strip()
                elif line.startswith('slots:'):
                    continue  # Next lines will be slot definitions
                elif line.startswith('weights:'):
                    continue  # Next lines will be weight definitions
                elif line.startswith('meta:'):
                    continue  # Next lines will be meta definitions
                elif ':' in line and not line.startswith(' '):
                    # Top-level key
                    continue
                elif line.startswith('  ') and ':' in line:
                    # Indented key-value pair
                    key, value = line.strip().split(':', 1)
                    value = value.strip().strip('"\'')
                    
                    # Determine if this is a slot, weight, or meta based on context
                    # This is a simplified parser - a real YAML parser would be better
                    try:
                        float_value = float(value)
                        annotation.weights[key] = float_value
                    except ValueError:
                        annotation.slots[key] = value
            
            if not annotation.capsule_id:
                annotation.capsule_id = self.generate_capsule_id(file_path, line_start)
            
            annotations.append(annotation)
        
        return annotations
    
    def parse_decorator_annotations(self, content: str, file_path: Path) -> List[HolographicAnnotation]:
        """Parse decorator style annotations"""
        annotations = []
        
        for match in self.decorator_pattern.finditer(content):
            decorator_content = match.group(1)
            line_start = content[:match.start()].count('\n') + 1
            line_end = content[:match.end()].count('\n') + 1
            
            annotation = HolographicAnnotation("", file_path, line_start, line_end)
            annotation.annotation_type = "decorator"
            
            # Parse decorator arguments (simplified - doesn't handle all Python syntax)
            try:
                # Try to evaluate as Python literal
                # This is safe for simple literals but not for complex expressions
                args_dict = eval(f"dict({decorator_content})")
                
                annotation.capsule_id = args_dict.get('capsule', '')
                annotation.slots = args_dict.get('slots', {})
                annotation.weights = args_dict.get('weights', {})
                annotation.meta = args_dict.get('meta', {})
                
            except Exception as e:
                print(f"Warning: Could not parse decorator at {file_path}:{line_start}: {e}")
                continue
            
            if not annotation.capsule_id:
                annotation.capsule_id = self.generate_capsule_id(file_path, line_start)
            
            annotations.append(annotation)
        
        return annotations
    
    def scan_file(self, file_path: Path) -> List[HolographicAnnotation]:
        """Scan a single Python file for annotations"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        annotations = []
        annotations.extend(self.parse_inline_annotations(content, file_path))
        annotations.extend(self.parse_docstring_annotations(content, file_path))
        annotations.extend(self.parse_decorator_annotations(content, file_path))
        
        return annotations
    
    def scan_directory(self, directory: Path, recursive: bool = True) -> List[HolographicAnnotation]:
        """Scan a directory for Python files with annotations"""
        annotations = []
        
        pattern = "**/*.py" if recursive else "*.py"
        for py_file in directory.glob(pattern):
            if py_file.is_file():
                file_annotations = self.scan_file(py_file)
                annotations.extend(file_annotations)
        
        return annotations
    
    def index_workspace(self, workspace_path: Path) -> Dict[str, Any]:
        """Index the entire workspace for holographic annotations"""
        print(f"Indexing workspace: {workspace_path}")
        
        self.annotations = self.scan_directory(workspace_path, recursive=True)
        
        # Group by file for reporting
        files_with_annotations = {}
        for annotation in self.annotations:
            file_key = str(annotation.file_path)
            if file_key not in files_with_annotations:
                files_with_annotations[file_key] = []
            files_with_annotations[file_key].append(annotation)
        
        return {
            "total_annotations": len(self.annotations),
            "files_scanned": len(list(workspace_path.glob("**/*.py"))),
            "files_with_annotations": len(files_with_annotations),
            "annotations_by_file": {
                file_path: [ann.to_dict() for ann in annotations]
                for file_path, annotations in files_with_annotations.items()
            }
        }

class EnhancedMemoryAdapter(MemorySystemAdapter):
    """Enhanced memory adapter with code indexing capabilities"""
    
    def __init__(self, dimension: int = 512):
        super().__init__(dimension)
        self.code_indexer = CodeIndexer()
        self.indexed_annotations: List[HolographicAnnotation] = []
    
    def index_workspace(self, workspace_path: str) -> Dict[str, Any]:
        """Index workspace for holographic annotations"""
        try:
            workspace = Path(workspace_path)
            if not workspace.exists():
                return {"error": f"Workspace path does not exist: {workspace_path}"}
            
            result = self.code_indexer.index_workspace(workspace)
            self.indexed_annotations = self.code_indexer.annotations
            
            # Create capsules from annotations
            created_capsules = []
            for annotation in self.indexed_annotations:
                if annotation.slots:  # Only create capsules that have actual content
                    try:
                        capsule_result = self.create_capsule(annotation.slots)
                        if capsule_result.get('success'):
                            created_capsules.append({
                                "capsule_id": annotation.capsule_id,
                                "file": str(annotation.file_path),
                                "line": annotation.line_start,
                                "slots": annotation.slots
                            })
                    except Exception as e:
                        print(f"Error creating capsule for {annotation.capsule_id}: {e}")
            
            result["created_capsules"] = created_capsules
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_indexed_annotations(self) -> List[Dict[str, Any]]:
        """Get all indexed annotations"""
        return [ann.to_dict() for ann in self.indexed_annotations]

# Initialize the enhanced memory system
try:
    memory_adapter = EnhancedMemoryAdapter()
except Exception as e:
    print(f"Warning: Could not initialize full memory system: {e}")
    memory_adapter = EnhancedMemoryAdapter()

def handle_rpc(request):
    """Handle an RPC request from the VS Code extension"""
    method = request.get('method')
    params = request.get('params', {})
    request_id = request.get('id')
    
    try:
        if method == 'list_capsules':
            result = memory_adapter.list_capsules()
        elif method == 'list_roles':
            result = memory_adapter.list_roles()
        elif method == 'list_symbols':
            page = params.get('page', 0)
            page_size = params.get('pageSize', 20)
            result = memory_adapter.list_symbols(page, page_size)
        elif method == 'create_capsule':
            bindings = params.get('bindings', {})
            result = memory_adapter.create_capsule(bindings)
        elif method == 'get_capsule_details':
            capsule_id = params.get('id')
            result = memory_adapter.get_capsule_details(capsule_id)
        elif method == 'query_capsules':
            query = params.get('query', {})
            result = memory_adapter.query_capsules(query)
        elif method == 'explain_with_llm':
            action = params.get('action')
            capsule_id = params.get('capsuleId')
            result = memory_adapter.explain_with_llm(action, capsule_id)
        elif method == 'index_workspace':
            workspace_path = params.get('workspace_path', '')
            result = memory_adapter.index_workspace(workspace_path)
        elif method == 'get_indexed_annotations':
            result = memory_adapter.get_indexed_annotations()
        else:
            raise ValueError(f"Unknown method: {method}")
            
        return {'id': request_id, 'result': result}
    except Exception as e:
        traceback.print_exc()
        return {'id': request_id, 'error': str(e)}

def main():
    """Main entry point for the Python bridge"""
    print("Enhanced Holographic Memory Python Bridge starting...")
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            request = json.loads(line)
            response = handle_rpc(request)
            
            # Send the response
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError as e:
            print(json.dumps({
                'error': f'JSON decode error: {e}',
                'id': None
            }), flush=True)
        except Exception as e:
            print(json.dumps({
                'error': f'Unexpected error: {e}',
                'id': None
            }), flush=True)
            traceback.print_exc()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Call Graph Analyzer for Lumina Memory System

This script analyzes Python files to build and visualize call graphs.
It shows function definitions and their relationships.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, Set, List, Tuple
from collections import defaultdict
import json

class CallGraphAnalyzer:
    """Analyzes Python files to build call graphs."""
    
    def __init__(self):
        self.functions = {}  # file -> set of function names
        self.calls = defaultdict(set)  # (file, function) -> set of called functions
        self.classes = {}  # file -> set of class names
        self.imports = {}  # file -> set of imported modules
        self.file_dependencies = defaultdict(set)  # file -> set of files it depends on
        
    def analyze_file(self, file_path: str) -> None:
        """Analyze a single Python file."""
        try:
            # Try different encodings to handle BOM and encoding issues
            content = None
            for encoding in ['utf-8-sig', 'utf-8', 'latin-1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                print(f"Could not decode {file_path} with any encoding")
                return
            
            # Remove BOM if present
            if content.startswith('\ufeff'):
                content = content[1:]
            
            tree = ast.parse(content, filename=file_path)
            visitor = CallVisitor(file_path)
            visitor.visit(tree)
            
            # Store results
            self.functions[file_path] = visitor.functions
            self.classes[file_path] = visitor.classes
            self.imports[file_path] = visitor.imports
            
            # Store call relationships
            for func, calls in visitor.calls.items():
                self.calls[(file_path, func)] = calls
                
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    def analyze_directory(self, directory: str, pattern: str = "*.py") -> None:
        """Analyze all Python files in a directory."""
        path = Path(directory)
        for py_file in path.rglob(pattern):
            if py_file.is_file():
                self.analyze_file(str(py_file))
    
    def generate_report(self) -> str:
        """Generate a text report of the call graph."""
        report = []
        report.append("=" * 60)
        report.append("LUMINA MEMORY SYSTEM - CALL GRAPH ANALYSIS")
        report.append("=" * 60)
        report.append("")
        
        # File overview
        report.append("FILES ANALYZED:")
        report.append("-" * 20)
        for file_path in sorted(self.functions.keys()):
            rel_path = os.path.relpath(file_path, start="e:\\lumina-memory-system")
            func_count = len(self.functions[file_path])
            class_count = len(self.classes.get(file_path, set()))
            report.append(f"  {rel_path}")
            report.append(f"    Functions: {func_count}, Classes: {class_count}")
        report.append("")
        
        # Function definitions by file
        report.append("FUNCTION DEFINITIONS BY FILE:")
        report.append("-" * 35)
        for file_path in sorted(self.functions.keys()):
            rel_path = os.path.relpath(file_path, start="e:\\lumina-memory-system")
            report.append(f"\n{rel_path}:")
            
            # Classes
            if file_path in self.classes and self.classes[file_path]:
                report.append("  Classes:")
                for cls in sorted(self.classes[file_path]):
                    report.append(f"    - {cls}")
            
            # Functions
            if self.functions[file_path]:
                report.append("  Functions:")
                for func in sorted(self.functions[file_path]):
                    report.append(f"    - {func}")
        
        # Call relationships
        report.append("\n\nFUNCTION CALL RELATIONSHIPS:")
        report.append("-" * 30)
        for (file_path, func), calls in sorted(self.calls.items()):
            if calls:  # Only show functions that call other functions
                rel_path = os.path.relpath(file_path, start="e:\\lumina-memory-system")
                report.append(f"\n{rel_path}::{func} calls:")
                for called_func in sorted(calls):
                    report.append(f"  -> {called_func}")
        
        # Import analysis
        report.append("\n\nIMPORT ANALYSIS:")
        report.append("-" * 20)
        for file_path in sorted(self.imports.keys()):
            if self.imports[file_path]:
                rel_path = os.path.relpath(file_path, start="e:\\lumina-memory-system")
                report.append(f"\n{rel_path} imports:")
                for imp in sorted(self.imports[file_path]):
                    report.append(f"  - {imp}")
        
        return "\n".join(report)
    
    def generate_json_report(self) -> str:
        """Generate a JSON report of the call graph."""
        data = {
            "files": {},
            "call_graph": {},
            "summary": {
                "total_files": len(self.functions),
                "total_functions": sum(len(funcs) for funcs in self.functions.values()),
                "total_classes": sum(len(classes) for classes in self.classes.values())
            }
        }
        
        # File information
        for file_path in self.functions.keys():
            rel_path = os.path.relpath(file_path, start="e:\\lumina-memory-system")
            data["files"][rel_path] = {
                "functions": list(self.functions[file_path]),
                "classes": list(self.classes.get(file_path, set())),
                "imports": list(self.imports.get(file_path, set()))
            }
        
        # Call relationships
        for (file_path, func), calls in self.calls.items():
            rel_path = os.path.relpath(file_path, start="e:\\lumina-memory-system")
            key = f"{rel_path}::{func}"
            data["call_graph"][key] = list(calls)
        
        return json.dumps(data, indent=2)


class CallVisitor(ast.NodeVisitor):
    """AST visitor to extract function calls and definitions."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.functions = set()
        self.classes = set()
        self.imports = set()
        self.calls = defaultdict(set)
        self.current_function = None
        self.current_class = None
    
    def visit_FunctionDef(self, node):
        """Visit function definitions."""
        func_name = node.name
        if self.current_class:
            full_name = f"{self.current_class}.{func_name}"
        else:
            full_name = func_name
        
        self.functions.add(full_name)
        old_function = self.current_function
        self.current_function = full_name
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_AsyncFunctionDef(self, node):
        """Visit async function definitions."""
        self.visit_FunctionDef(node)  # Same logic as regular functions
    
    def visit_ClassDef(self, node):
        """Visit class definitions."""
        self.classes.add(node.name)
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_Call(self, node):
        """Visit function calls."""
        if self.current_function:
            called_func = self._get_call_name(node)
            if called_func:
                self.calls[self.current_function].add(called_func)
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Visit import statements."""
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Visit from...import statements."""
        if node.module:
            for alias in node.names:
                if alias.name == '*':
                    self.imports.add(f"from {node.module} import *")
                else:
                    self.imports.add(f"from {node.module} import {alias.name}")
        self.generic_visit(node)
    
    def _get_call_name(self, node) -> str:
        """Extract the name of a function call."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            # Handle method calls like obj.method()
            if isinstance(node.func.value, ast.Name):
                return f"{node.func.value.id}.{node.func.attr}"
            else:
                return node.func.attr
        return None


def main():
    """Main function to run the call graph analysis."""
    print("Lumina Memory System - Call Graph Analyzer")
    print("=" * 50)
    
    # Analyze the main source directory
    analyzer = CallGraphAnalyzer()
    src_dir = "e:\\lumina-memory-system\\src\\lumina_memory"
    
    if not os.path.exists(src_dir):
        print(f"Error: Source directory not found: {src_dir}")
        return
    
    print(f"Analyzing Python files in: {src_dir}")
    analyzer.analyze_directory(src_dir)
    
    # Also analyze some key files in the root
    root_files = [
        "e:\\lumina-memory-system\\consciousness_persistence_clean.py",
        "e:\\lumina-memory-system\\consciousness_persistence_diagnostic.py",
        "e:\\lumina-memory-system\\mistrallumina_continuity.py",
        "e:\\lumina-memory-system\\test_unified_system.py"
    ]
    
    for file_path in root_files:
        if os.path.exists(file_path):
            print(f"Analyzing: {os.path.basename(file_path)}")
            analyzer.analyze_file(file_path)
    
    # Generate and save reports
    print("\nGenerating reports...")
    
    # Text report
    text_report = analyzer.generate_report()
    with open("e:\\lumina-memory-system\\call_graph_report.txt", "w", encoding="utf-8") as f:
        f.write(text_report)
    
    # JSON report
    json_report = analyzer.generate_json_report()
    with open("e:\\lumina-memory-system\\call_graph_report.json", "w", encoding="utf-8") as f:
        f.write(json_report)
    
    print("\nReports generated:")
    print("  - call_graph_report.txt (detailed text report)")
    print("  - call_graph_report.json (structured data)")
    
    # Print summary
    print(f"\nSUMMARY:")
    print(f"  Files analyzed: {len(analyzer.functions)}")
    print(f"  Total functions: {sum(len(funcs) for funcs in analyzer.functions.values())}")
    print(f"  Total classes: {sum(len(classes) for classes in analyzer.classes.values())}")
    
    # Show first few functions as preview
    print(f"\nSample functions found:")
    count = 0
    for file_path, functions in analyzer.functions.items():
        if functions and count < 10:
            rel_path = os.path.relpath(file_path, start="e:\\lumina-memory-system")
            for func in sorted(list(functions)[:3]):  # Show first 3 functions per file
                print(f"  {rel_path}::{func}")
                count += 1
                if count >= 10:
                    break
        if count >= 10:
            break
    
    if count >= 10:
        print("  ... (see full report for complete list)")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Call Graph Visualizer for LLM Consciousness GUI

This module creates visual call graphs from Python AST analysis using networkx and graphviz.
"""

import ast
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Set, Tuple
import tempfile
import os

try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False


class CallGraphAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze function calls and build call graph."""
    
    def __init__(self):
        self.functions = {}  # function_name -> {calls: set, defined_at: line}
        self.classes = {}    # class_name -> {methods: dict, defined_at: line}
        self.current_function = None
        self.current_class = None
        self.call_graph = nx.DiGraph()
    
    def visit_FunctionDef(self, node):
        """Visit function definitions."""
        func_name = node.name
        
        if self.current_class:
            # Method inside a class
            full_name = f"{self.current_class}.{func_name}"
            if self.current_class not in self.classes:
                self.classes[self.current_class] = {"methods": {}, "defined_at": 0}
            self.classes[self.current_class]["methods"][func_name] = {
                "calls": set(),
                "defined_at": node.lineno
            }
        else:
            # Top-level function
            full_name = func_name
            self.functions[func_name] = {
                "calls": set(),
                "defined_at": node.lineno
            }
        
        # Add node to graph
        self.call_graph.add_node(full_name, type="function", line=node.lineno)
        
        # Visit function body with current function context
        old_function = self.current_function
        self.current_function = full_name
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_AsyncFunctionDef(self, node):
        """Visit async function definitions."""
        self.visit_FunctionDef(node)  # Same logic as regular functions
    
    def visit_ClassDef(self, node):
        """Visit class definitions."""
        class_name = node.name
        self.classes[class_name] = {
            "methods": {},
            "defined_at": node.lineno
        }
        
        # Add class node to graph
        self.call_graph.add_node(class_name, type="class", line=node.lineno)
        
        # Visit class body with current class context
        old_class = self.current_class
        self.current_class = class_name
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_Call(self, node):
        """Visit function calls."""
        if self.current_function:
            # Determine the called function name
            called_func = self._get_call_name(node)
            if called_func:
                # Add edge from current function to called function
                self.call_graph.add_edge(self.current_function, called_func)
                
                # Store in functions/classes data structure
                if self.current_class and "." in self.current_function:
                    # Method call
                    method_name = self.current_function.split(".")[-1]
                    if method_name in self.classes[self.current_class]["methods"]:
                        self.classes[self.current_class]["methods"][method_name]["calls"].add(called_func)
                else:
                    # Function call
                    func_name = self.current_function
                    if func_name in self.functions:
                        self.functions[func_name]["calls"].add(called_func)
        
        self.generic_visit(node)
    
    def _get_call_name(self, node) -> str:
        """Extract the function name from a call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                return f"{node.func.value.id}.{node.func.attr}"
            else:
                return node.func.attr
        return None


class CallGraphVisualizer:
    """Creates visual call graphs from Python code."""
    
    def __init__(self):
        self.analyzer = None
        self.graph = None
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a Python file and extract call graph information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Parse AST
            tree = ast.parse(source_code)
            
            # Analyze call graph
            self.analyzer = CallGraphAnalyzer()
            self.analyzer.visit(tree)
            self.graph = self.analyzer.call_graph
            
            return {
                "functions": self.analyzer.functions,
                "classes": self.analyzer.classes,
                "graph": self.graph,
                "nodes": len(self.graph.nodes),
                "edges": len(self.graph.edges)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def create_matplotlib_graph(self, output_path: Path = None) -> Path:
        """Create a call graph visualization using matplotlib."""
        if not self.graph:
            raise ValueError("No graph data available. Run analyze_file() first.")
        
        # Create figure
        plt.figure(figsize=(12, 8))
        plt.title("Function Call Graph", fontsize=16, fontweight='bold')
        
        # Create layout
        if len(self.graph.nodes) > 0:
            try:
                pos = nx.spring_layout(self.graph, k=2, iterations=50)
            except:
                pos = nx.random_layout(self.graph)
            
            # Draw nodes with different colors for classes and functions
            node_colors = []
            node_sizes = []
            for node in self.graph.nodes():
                node_data = self.graph.nodes[node]
                if node_data.get('type') == 'class':
                    node_colors.append('lightblue')
                    node_sizes.append(1500)
                else:
                    node_colors.append('lightgreen')
                    node_sizes.append(1000)
            
            # Draw the graph
            nx.draw(self.graph, pos, 
                   node_color=node_colors,
                   node_size=node_sizes,
                   with_labels=True,
                   font_size=8,
                   font_weight='bold',
                   arrows=True,
                   arrowsize=20,
                   edge_color='gray',
                   alpha=0.7)
            
            # Add legend
            import matplotlib.patches as mpatches
            class_patch = mpatches.Patch(color='lightblue', label='Classes')
            func_patch = mpatches.Patch(color='lightgreen', label='Functions')
            plt.legend(handles=[class_patch, func_patch], loc='upper right')
        
        # Save or return path
        if output_path is None:
            output_path = Path(tempfile.gettempdir()) / "call_graph.png"
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_graphviz_graph(self, output_path: Path = None) -> Path:
        """Create a call graph visualization using graphviz (if available)."""
        if not GRAPHVIZ_AVAILABLE:
            raise ImportError("Graphviz not available. Using matplotlib instead.")
        
        if not self.graph:
            raise ValueError("No graph data available. Run analyze_file() first.")
        
        # Create graphviz digraph
        dot = graphviz.Digraph(comment='Function Call Graph')
        dot.attr(rankdir='TB', size='12,8')
        dot.attr('node', shape='box', style='rounded,filled')
        
        # Add nodes
        for node in self.graph.nodes():
            node_data = self.graph.nodes[node]
            if node_data.get('type') == 'class':
                dot.node(node, node, fillcolor='lightblue', shape='ellipse')
            else:
                dot.node(node, node, fillcolor='lightgreen')
        
        # Add edges
        for edge in self.graph.edges():
            dot.edge(edge[0], edge[1])
        
        # Save
        if output_path is None:
            output_path = Path(tempfile.gettempdir()) / "call_graph_graphviz"
        else:
            output_path = output_path.with_suffix('')  # Remove extension, graphviz adds it
        
        dot.render(str(output_path), format='png', cleanup=True)
        return output_path.with_suffix('.png')
    
    def get_graph_stats(self) -> Dict:
        """Get statistics about the call graph."""
        if not self.graph:
            return {}
        
        stats = {
            "total_nodes": len(self.graph.nodes),
            "total_edges": len(self.graph.edges),
            "classes": len([n for n in self.graph.nodes() if self.graph.nodes[n].get('type') == 'class']),
            "functions": len([n for n in self.graph.nodes() if self.graph.nodes[n].get('type') == 'function']),
            "isolated_nodes": len(list(nx.isolates(self.graph))),
            "strongly_connected_components": len(list(nx.strongly_connected_components(self.graph))),
        }
        
        # Calculate complexity metrics
        if len(self.graph.nodes) > 0:
            stats["average_degree"] = sum(dict(self.graph.degree()).values()) / len(self.graph.nodes)
            stats["density"] = nx.density(self.graph)
        
        return stats


def test_call_graph_visualizer():
    """Test the call graph visualizer with sample code."""
    # Create sample Python file
    sample_code = '''
class MemoryUnit:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}
    
    def store(self, key, value):
        if len(self.data) < self.capacity:
            self.data[key] = value
            self.log_operation("store", key)
        return self.retrieve(key)
    
    def retrieve(self, key):
        return self.data.get(key)
    
    def log_operation(self, op, key):
        print(f"Operation: {op} on {key}")

def process_data(memory_unit, data_list):
    for item in data_list:
        memory_unit.store(item["key"], item["value"])
    return analyze_memory(memory_unit)

def analyze_memory(memory_unit):
    stats = {}
    for key in memory_unit.data:
        stats[key] = len(str(memory_unit.retrieve(key)))
    return stats

async def async_process(data):
    result = process_data(MemoryUnit(100), data)
    return result
'''
    
    # Write sample file
    sample_file = Path(tempfile.gettempdir()) / "sample_call_graph.py"
    with open(sample_file, 'w') as f:
        f.write(sample_code)
    
    # Test visualizer
    visualizer = CallGraphVisualizer()
    analysis = visualizer.analyze_file(sample_file)
    
    print("📊 Call Graph Analysis Results:")
    print(f"Functions: {list(analysis['functions'].keys())}")
    print(f"Classes: {list(analysis['classes'].keys())}")
    print(f"Graph nodes: {analysis['nodes']}")
    print(f"Graph edges: {analysis['edges']}")
    
    # Create visualization
    try:
        image_path = visualizer.create_matplotlib_graph()
        print(f"📈 Call graph saved to: {image_path}")
        
        # Get stats
        stats = visualizer.get_graph_stats()
        print(f"📊 Graph stats: {stats}")
        
        return image_path
        
    except Exception as e:
        print(f"❌ Error creating visualization: {e}")
        return None


if __name__ == "__main__":
    test_call_graph_visualizer()
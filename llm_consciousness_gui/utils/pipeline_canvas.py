#!/usr/bin/env python3
"""
Pipeline Design Canvas for LLM Consciousness GUI

This module provides a visual node-based programming interface using Qt Graphics View Framework.
Users can drag and drop blocks representing functions, conditions, and I/O operations,
then generate Python code from the visual pipeline.
"""

import json
import uuid
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem,
    QGraphicsTextItem, QGraphicsLineItem, QGraphicsEllipseItem,
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit,
    QListWidget, QListWidgetItem, QSplitter, QScrollArea, QGroupBox,
    QComboBox, QLineEdit, QSpinBox, QCheckBox, QTabWidget, QMessageBox
)
from PySide6.QtCore import Qt, QPointF, QRectF, Signal, QMimeData
from PySide6.QtGui import (
    QPen, QBrush, QColor, QPainter, QFont, QDrag, QPalette,
    QLinearGradient, QRadialGradient
)


class NodeType(Enum):
    """Types of nodes in the pipeline."""
    FUNCTION = "function"
    CONDITION = "condition"
    INPUT = "input"
    OUTPUT = "output"
    VARIABLE = "variable"
    LOOP = "loop"
    CLASS = "class"


@dataclass
class NodeData:
    """Data structure for a pipeline node."""
    id: str
    type: NodeType
    name: str
    x: float
    y: float
    width: float = 120
    height: float = 60
    properties: Dict[str, Any] = None
    inputs: List[str] = None
    outputs: List[str] = None
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
        if self.inputs is None:
            self.inputs = []
        if self.outputs is None:
            self.outputs = []


@dataclass
class ConnectionData:
    """Data structure for connections between nodes."""
    id: str
    source_node: str
    source_output: str
    target_node: str
    target_input: str


class PipelineNode(QGraphicsRectItem):
    """A draggable node in the pipeline canvas."""
    
    def __init__(self, node_data: NodeData, parent=None):
        super().__init__(parent)
        self.node_data = node_data
        self.connections = []
        self.selected_for_connection = False
        
        # Set up the visual appearance
        self.setRect(0, 0, node_data.width, node_data.height)
        self.setPos(node_data.x, node_data.y)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        
        # Set colors based on node type
        self.setup_appearance()
        
        # Add text label
        self.text_item = QGraphicsTextItem(node_data.name, self)
        self.text_item.setPos(10, 20)
        self.text_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        # Add connection points (small circles)
        self.input_points = []
        self.output_points = []
        self.setup_connection_points()
    
    def setup_appearance(self):
        """Set up the visual appearance based on node type."""
        colors = {
            NodeType.FUNCTION: QColor(100, 150, 255),      # Blue
            NodeType.CONDITION: QColor(255, 200, 100),     # Orange
            NodeType.INPUT: QColor(100, 255, 150),         # Green
            NodeType.OUTPUT: QColor(255, 100, 150),        # Pink
            NodeType.VARIABLE: QColor(200, 200, 200),      # Gray
            NodeType.LOOP: QColor(150, 100, 255),          # Purple
            NodeType.CLASS: QColor(255, 150, 100),         # Red-orange
        }
        
        color = colors.get(self.node_data.type, QColor(128, 128, 128))
        
        # Create gradient brush
        gradient = QLinearGradient(0, 0, 0, self.node_data.height)
        gradient.setColorAt(0, color.lighter(120))
        gradient.setColorAt(1, color.darker(120))
        
        self.setBrush(QBrush(gradient))
        self.setPen(QPen(color.darker(150), 2))
    
    def setup_connection_points(self):
        """Set up input and output connection points."""
        # Input points (left side)
        input_count = max(1, len(self.node_data.inputs))
        for i in range(input_count):
            y = (i + 1) * self.node_data.height / (input_count + 1)
            point = QGraphicsEllipseItem(-5, y - 5, 10, 10, self)
            point.setBrush(QBrush(QColor(50, 50, 50)))
            point.setPen(QPen(QColor(0, 0, 0), 1))
            self.input_points.append(point)
        
        # Output points (right side)
        output_count = max(1, len(self.node_data.outputs))
        for i in range(output_count):
            y = (i + 1) * self.node_data.height / (output_count + 1)
            point = QGraphicsEllipseItem(self.node_data.width - 5, y - 5, 10, 10, self)
            point.setBrush(QBrush(QColor(200, 200, 200)))
            point.setPen(QPen(QColor(0, 0, 0), 1))
            self.output_points.append(point)
    
    def itemChange(self, change, value):
        """Handle item changes (like position updates)."""
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Update node data position
            self.node_data.x = value.x()
            self.node_data.y = value.y()
            
            # Update connections
            self.update_connections()
        
        return super().itemChange(change, value)
    
    def update_connections(self):
        """Update all connections when the node moves."""
        # This will be implemented when we add connection lines
        pass
    
    def mousePressEvent(self, event):
        """Handle mouse press for connection creation."""
        if event.button() == Qt.MouseButton.RightButton:
            # Right-click for connection mode
            self.selected_for_connection = not self.selected_for_connection
            if self.selected_for_connection:
                self.setPen(QPen(QColor(255, 0, 0), 3))  # Red border when selected
            else:
                self.setup_appearance()  # Reset appearance
        else:
            super().mousePressEvent(event)


class ConnectionLine(QGraphicsLineItem):
    """A connection line between two nodes."""
    
    def __init__(self, connection_data: ConnectionData, source_node: PipelineNode, target_node: PipelineNode):
        super().__init__()
        self.connection_data = connection_data
        self.source_node = source_node
        self.target_node = target_node
        
        # Set up appearance
        self.setPen(QPen(QColor(50, 50, 50), 2))
        self.setZValue(-1)  # Behind nodes
        
        # Update line position
        self.update_line()
    
    def update_line(self):
        """Update the line position based on node positions."""
        source_pos = self.source_node.pos()
        target_pos = self.target_node.pos()
        
        # Calculate connection points
        source_point = QPointF(
            source_pos.x() + self.source_node.node_data.width,
            source_pos.y() + self.source_node.node_data.height / 2
        )
        target_point = QPointF(
            target_pos.x(),
            target_pos.y() + self.target_node.node_data.height / 2
        )
        
        self.setLine(source_point.x(), source_point.y(), target_point.x(), target_point.y())


class NodePalette(QWidget):
    """Palette of draggable node types."""
    
    node_requested = Signal(NodeType, str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the node palette UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🧩 Node Palette")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Node categories
        categories = {
            "🔧 Functions": [
                ("Function", NodeType.FUNCTION),
                ("Method", NodeType.FUNCTION),
                ("Lambda", NodeType.FUNCTION),
            ],
            "🔀 Control Flow": [
                ("If/Else", NodeType.CONDITION),
                ("For Loop", NodeType.LOOP),
                ("While Loop", NodeType.LOOP),
            ],
            "📊 Data": [
                ("Input", NodeType.INPUT),
                ("Output", NodeType.OUTPUT),
                ("Variable", NodeType.VARIABLE),
            ],
            "🏗️ Structure": [
                ("Class", NodeType.CLASS),
            ]
        }
        
        for category_name, nodes in categories.items():
            # Category group
            group = QGroupBox(category_name)
            group_layout = QVBoxLayout(group)
            
            for node_name, node_type in nodes:
                button = QPushButton(node_name)
                button.clicked.connect(lambda checked, nt=node_type, nn=node_name: self.node_requested.emit(nt, nn))
                group_layout.addWidget(button)
            
            layout.addWidget(group)
        
        layout.addStretch()


class PipelineCanvas(QGraphicsView):
    """Main canvas for the pipeline design."""
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Canvas properties
        self.nodes = {}  # id -> PipelineNode
        self.connections = {}  # id -> ConnectionLine
        self.selected_nodes = []  # For connection creation
        
        # Set up the canvas
        self.setup_canvas()
    
    def setup_canvas(self):
        """Set up the canvas properties."""
        # Set scene size
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        
        # Set background
        self.setBackgroundBrush(QBrush(QColor(240, 240, 240)))
        
        # Grid pattern (optional)
        self.draw_grid()
    
    def draw_grid(self):
        """Draw a grid pattern on the canvas."""
        grid_size = 50
        scene_rect = self.scene.sceneRect()
        
        # Vertical lines
        x = scene_rect.left()
        while x < scene_rect.right():
            line = self.scene.addLine(x, scene_rect.top(), x, scene_rect.bottom())
            line.setPen(QPen(QColor(220, 220, 220), 1))
            line.setZValue(-10)
            x += grid_size
        
        # Horizontal lines
        y = scene_rect.top()
        while y < scene_rect.bottom():
            line = self.scene.addLine(scene_rect.left(), y, scene_rect.right(), y)
            line.setPen(QPen(QColor(220, 220, 220), 1))
            line.setZValue(-10)
            y += grid_size
    
    def add_node(self, node_type: NodeType, name: str, position: QPointF = None):
        """Add a new node to the canvas."""
        if position is None:
            position = QPointF(0, 0)
        
        # Create node data
        node_data = NodeData(
            id=str(uuid.uuid4()),
            type=node_type,
            name=name,
            x=position.x(),
            y=position.y()
        )
        
        # Create visual node
        node = PipelineNode(node_data)
        self.scene.addItem(node)
        self.nodes[node_data.id] = node
        
        return node
    
    def add_connection(self, source_node_id: str, target_node_id: str):
        """Add a connection between two nodes."""
        if source_node_id not in self.nodes or target_node_id not in self.nodes:
            return None
        
        source_node = self.nodes[source_node_id]
        target_node = self.nodes[target_node_id]
        
        # Create connection data
        connection_data = ConnectionData(
            id=str(uuid.uuid4()),
            source_node=source_node_id,
            source_output="output",
            target_node=target_node_id,
            target_input="input"
        )
        
        # Create visual connection
        connection = ConnectionLine(connection_data, source_node, target_node)
        self.scene.addItem(connection)
        self.connections[connection_data.id] = connection
        
        return connection
    
    def mousePressEvent(self, event):
        """Handle mouse press events for node selection and connection."""
        item = self.itemAt(event.pos())
        
        if isinstance(item, PipelineNode):
            if event.button() == Qt.MouseButton.RightButton:
                # Handle connection creation
                if item.selected_for_connection:
                    self.selected_nodes.append(item)
                    if len(self.selected_nodes) == 2:
                        # Create connection between selected nodes
                        self.add_connection(
                            self.selected_nodes[0].node_data.id,
                            self.selected_nodes[1].node_data.id
                        )
                        # Reset selection
                        for node in self.selected_nodes:
                            node.selected_for_connection = False
                            node.setup_appearance()
                        self.selected_nodes.clear()
        
        super().mousePressEvent(event)
    
    def get_pipeline_data(self) -> Dict:
        """Get the current pipeline as serializable data."""
        nodes_data = []
        connections_data = []
        
        for node in self.nodes.values():
            nodes_data.append(asdict(node.node_data))
        
        for connection in self.connections.values():
            connections_data.append(asdict(connection.connection_data))
        
        return {
            "nodes": nodes_data,
            "connections": connections_data
        }
    
    def load_pipeline_data(self, data: Dict):
        """Load pipeline from serializable data."""
        # Clear current pipeline
        self.scene.clear()
        self.nodes.clear()
        self.connections.clear()
        self.draw_grid()
        
        # Load nodes
        for node_data_dict in data.get("nodes", []):
            node_data = NodeData(**node_data_dict)
            node_data.type = NodeType(node_data.type)  # Convert string back to enum
            node = PipelineNode(node_data)
            self.scene.addItem(node)
            self.nodes[node_data.id] = node
        
        # Load connections
        for connection_data_dict in data.get("connections", []):
            connection_data = ConnectionData(**connection_data_dict)
            if (connection_data.source_node in self.nodes and 
                connection_data.target_node in self.nodes):
                source_node = self.nodes[connection_data.source_node]
                target_node = self.nodes[connection_data.target_node]
                connection = ConnectionLine(connection_data, source_node, target_node)
                self.scene.addItem(connection)
                self.connections[connection_data.id] = connection


class CodeGenerator:
    """Generates Python code from pipeline data."""
    
    def __init__(self):
        self.indentation = "    "
    
    def generate_code(self, pipeline_data: Dict) -> str:
        """Generate Python code from pipeline data."""
        nodes = {node["id"]: node for node in pipeline_data.get("nodes", [])}
        connections = pipeline_data.get("connections", [])
        
        # Build dependency graph
        dependencies = self.build_dependency_graph(nodes, connections)
        
        # Generate code sections
        code_sections = []
        
        # Imports
        code_sections.append("#!/usr/bin/env python3")
        code_sections.append('"""Generated pipeline code"""')
        code_sections.append("")
        
        # Generate code for each node type
        for node_id in self.topological_sort(dependencies):
            node = nodes[node_id]
            node_code = self.generate_node_code(node)
            if node_code:
                code_sections.append(node_code)
                code_sections.append("")
        
        # Main execution
        code_sections.append('if __name__ == "__main__":')
        code_sections.append(f'{self.indentation}# Execute pipeline')
        code_sections.append(f'{self.indentation}main()')
        
        return "\n".join(code_sections)
    
    def build_dependency_graph(self, nodes: Dict, connections: List) -> Dict:
        """Build a dependency graph from connections."""
        dependencies = {node_id: [] for node_id in nodes.keys()}
        
        for connection in connections:
            source = connection["source_node"]
            target = connection["target_node"]
            dependencies[target].append(source)
        
        return dependencies
    
    def topological_sort(self, dependencies: Dict) -> List[str]:
        """Perform topological sort on the dependency graph."""
        # Simple topological sort implementation
        visited = set()
        result = []
        
        def visit(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            for dep in dependencies.get(node_id, []):
                visit(dep)
            result.append(node_id)
        
        for node_id in dependencies.keys():
            visit(node_id)
        
        return result
    
    def generate_node_code(self, node: Dict) -> str:
        """Generate code for a specific node."""
        node_type = NodeType(node["type"])
        name = node["name"]
        
        if node_type == NodeType.FUNCTION:
            return f"def {name.lower().replace(' ', '_')}():\n{self.indentation}pass"
        
        elif node_type == NodeType.CLASS:
            return f"class {name.replace(' ', '')}:\n{self.indentation}pass"
        
        elif node_type == NodeType.CONDITION:
            return f"# Condition: {name}\nif True:\n{self.indentation}pass"
        
        elif node_type == NodeType.LOOP:
            if "for" in name.lower():
                return f"# Loop: {name}\nfor i in range(10):\n{self.indentation}pass"
            else:
                return f"# Loop: {name}\nwhile True:\n{self.indentation}break"
        
        elif node_type == NodeType.INPUT:
            return f"# Input: {name}\n{name.lower().replace(' ', '_')} = input('{name}: ')"
        
        elif node_type == NodeType.OUTPUT:
            return f"# Output: {name}\nprint({name.lower().replace(' ', '_')})"
        
        elif node_type == NodeType.VARIABLE:
            return f"# Variable: {name}\n{name.lower().replace(' ', '_')} = None"
        
        return f"# {name}"


class PipelineDesigner(QWidget):
    """Main pipeline designer widget."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.code_generator = CodeGenerator()
    
    def setup_ui(self):
        """Set up the pipeline designer UI."""
        layout = QHBoxLayout(self)
        
        # Left panel: Node palette
        self.palette = NodePalette()
        self.palette.node_requested.connect(self.add_node_to_canvas)
        self.palette.setMaximumWidth(200)
        
        # Center: Canvas
        self.canvas = PipelineCanvas()
        
        # Right panel: Properties and code generation
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Controls
        controls_group = QGroupBox("🎮 Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        self.clear_button = QPushButton("🗑️ Clear Canvas")
        self.save_button = QPushButton("💾 Save Pipeline")
        self.load_button = QPushButton("📁 Load Pipeline")
        self.generate_button = QPushButton("🚀 Generate Code")
        
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.save_button)
        controls_layout.addWidget(self.load_button)
        controls_layout.addWidget(self.generate_button)
        
        # Generated code display
        code_group = QGroupBox("🐍 Generated Code")
        code_layout = QVBoxLayout(code_group)
        
        self.code_display = QTextEdit()
        self.code_display.setFont(QFont("Consolas", 10))
        self.code_display.setReadOnly(True)
        code_layout.addWidget(self.code_display)
        
        right_layout.addWidget(controls_group)
        right_layout.addWidget(code_group)
        right_panel.setMaximumWidth(300)
        
        # Add to main layout
        layout.addWidget(self.palette)
        layout.addWidget(self.canvas, 1)  # Canvas takes most space
        layout.addWidget(right_panel)
        
        # Connect signals
        self.clear_button.clicked.connect(self.clear_canvas)
        self.generate_button.clicked.connect(self.generate_code)
    
    def add_node_to_canvas(self, node_type: NodeType, name: str):
        """Add a node to the canvas at the center."""
        center = self.canvas.mapToScene(self.canvas.rect().center())
        self.canvas.add_node(node_type, name, center)
    
    def clear_canvas(self):
        """Clear the canvas."""
        self.canvas.scene.clear()
        self.canvas.nodes.clear()
        self.canvas.connections.clear()
        self.canvas.draw_grid()
        self.code_display.clear()
    
    def generate_code(self):
        """Generate Python code from the current pipeline."""
        pipeline_data = self.canvas.get_pipeline_data()
        generated_code = self.code_generator.generate_code(pipeline_data)
        self.code_display.setPlainText(generated_code)


def test_pipeline_designer():
    """Test the pipeline designer."""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    designer = PipelineDesigner()
    designer.setWindowTitle("🧠 Pipeline Designer Test")
    designer.resize(1200, 800)
    designer.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_pipeline_designer()
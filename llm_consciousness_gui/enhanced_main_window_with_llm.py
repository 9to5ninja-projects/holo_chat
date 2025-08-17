#!/usr/bin/env python3
"""
🧠 Enhanced Main Window with Search Bar + LLM Terminal Panel

This implements the complete enhanced GUI with:
- Left Panel: File browser (.py files)
- Middle Panel: Searchable class/function structure
- Right Panel: Code viewer + LLM query interface
"""

import os
from pathlib import Path
from typing import Optional

# ✅ 1. TOP OF main_window.py - Updated imports
from PySide6.QtWidgets import (
    QMainWindow, QSplitter, QWidget, QTreeView, QPlainTextEdit, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem, QFileSystemModel, QLineEdit, QLabel,
    QTextEdit, QPushButton, QHBoxLayout, QTabWidget, QStatusBar, QMenuBar,
    QMenu, QMessageBox, QScrollArea
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QDir, QModelIndex, QThread, Signal
from PySide6.QtGui import QAction, QFont
import requests
import json

from parser.ast_parser import ASTParser
from utils.call_graph_visualizer import CallGraphVisualizer
from utils.memory_tracker import LiveMemoryTracker, CodeExecutor
from utils.pipeline_canvas import PipelineDesigner
from utils.xpunit_consolidator import XPUnitConsolidatorWidget
from utils.xpunit_lifecycle_tracer import LifecycleTracerWidget
from utils.notebook_integration import NotebookIntegrationWidget
from utils.holographic_memory_widget import HolographicMemoryWidget


class LLMWorker(QThread):
    """Worker thread for LLM requests to avoid blocking the UI."""
    
    response_ready = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, prompt: str, model: str = "mistral"):
        super().__init__()
        self.prompt = prompt
        self.model = model
    
    def run(self):
        """Execute the LLM request in a separate thread."""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": self.prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                llm_response = result.get("response", "No response field.")
                self.response_ready.emit(llm_response)
            else:
                self.error_occurred.emit(f"Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            self.error_occurred.emit("Connection Error: Is Ollama running on localhost:11434?")
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Timeout Error: LLM request took too long")
        except Exception as e:
            self.error_occurred.emit(f"Exception occurred: {str(e)}")


class EnhancedMainWindowWithLLM(QMainWindow):
    """Enhanced main window with search bar and LLM integration."""
    
    def __init__(self, project_root: Path, parent=None):
        super().__init__(parent)
        self.project_root = project_root
        self.ast_parser = ASTParser()
        self.call_graph_visualizer = CallGraphVisualizer()
        self.memory_tracker = LiveMemoryTracker(max_history=500)
        self.code_executor = CodeExecutor(self.memory_tracker)
        self.current_file = None
        self.llm_worker = None
        
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_connections()
    
    def setup_ui(self):
        """Set up the enhanced user interface with search and LLM."""
        self.setWindowTitle("🧠 Enhanced LLM Consciousness GUI - Search + AI Integration")
        self.setGeometry(100, 100, 1800, 1000)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QVBoxLayout(central_widget)
        
        # ✅ 2. MODIFY __init__ LAYOUT STRUCTURE
        
        # Set up the file system model for .py files
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(str(self.project_root))
        self.file_model.setNameFilters(["*.py"])
        self.file_model.setNameFilterDisables(False)
        
        # === LEFT: File Explorer ===
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(str(self.project_root)))
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setMinimumWidth(250)
        
        # === MIDDLE: Search Bar + Structure View ===
        middle_panel = QWidget()
        middle_layout = QVBoxLayout(middle_panel)
        
        # Search bar
        search_label = QLabel("🔍 Search Structure")
        search_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search class/function/method...")
        # Structure view
        structure_label = QLabel("🏗️ Code Structure")
        structure_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.structure_view = QTreeWidget()
        self.structure_view.setHeaderLabels(["Structure", "Type", "Line"])
        self.structure_view.setAlternatingRowColors(True)
        
        middle_layout.addWidget(search_label)
        middle_layout.addWidget(self.search_bar)
        middle_layout.addWidget(structure_label)
        middle_layout.addWidget(self.structure_view)
        middle_panel.setMinimumWidth(300)
        
        # === RIGHT: Code + LLM Panel ===
        
        # Code viewer
        self.code_view = QPlainTextEdit()
        self.code_view.setReadOnly(True)
        self.code_view.setFont(QFont("Consolas", 10))
        self.code_view.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.code_view.setPlainText("Click on a Python file to view its code and structure.")
        # LLM Panel components
        llm_widget = QWidget()
        llm_layout = QVBoxLayout(llm_widget)
        
        # LLM Input
        llm_input_label = QLabel("🤖 Ask Mistral LLM")
        llm_input_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.llm_input = QTextEdit()
        self.llm_input.setPlaceholderText("Enter prompt for Mistral LLM via Ollama...\n\nExample prompts:\n• Explain this code structure\n• What patterns do you see?\n• Suggest improvements\n• Find potential issues")
        self.llm_input.setMaximumHeight(120)
        
        # LLM Button
        button_layout = QHBoxLayout()
        self.llm_button = QPushButton("🚀 Send Prompt")
        self.llm_button.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.clear_button = QPushButton("🗑️ Clear")
        self.context_button = QPushButton("📄 Add Current File Context")
        
        button_layout.addWidget(self.llm_button)
        button_layout.addWidget(self.context_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        # LLM Output
        llm_output_label = QLabel("🧠 LLM Response:")
        llm_output_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.llm_output = QTextEdit()
        self.llm_output.setReadOnly(True)
        self.llm_output.setFont(QFont("Segoe UI", 9))
        self.llm_output.setPlainText("LLM responses will appear here.\n\nMake sure Ollama is running with: ollama run mistral")
        
        # Status indicator
        self.llm_status = QLabel("🔴 Disconnected")
        self.llm_status.setFont(QFont("Segoe UI", 8))
        
        llm_layout.addWidget(llm_input_label)
        llm_layout.addWidget(self.llm_input)
        llm_layout.addLayout(button_layout)
        llm_layout.addWidget(llm_output_label)
        llm_layout.addWidget(self.llm_output)
        llm_layout.addWidget(self.llm_status)
        
        # === CALL GRAPH VISUALIZATION TAB ===
        call_graph_widget = QWidget()
        call_graph_layout = QVBoxLayout(call_graph_widget)
        
        # Call graph controls
        graph_controls = QHBoxLayout()
        self.visualize_button = QPushButton("🔍 Visualize Call Graph")
        self.visualize_button.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.graph_stats_label = QLabel("Select a file to analyze call graph")
        self.graph_stats_label.setFont(QFont("Segoe UI", 8))
        
        graph_controls.addWidget(self.visualize_button)
        graph_controls.addWidget(self.graph_stats_label)
        graph_controls.addStretch()
        
        # Call graph display area
        self.call_graph_scroll = QScrollArea()
        self.call_graph_label = QLabel("Click 'Visualize Call Graph' to generate visualization")
        self.call_graph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.call_graph_label.setStyleSheet("border: 2px dashed #ccc; padding: 20px; color: #666;")
        self.call_graph_scroll.setWidget(self.call_graph_label)
        self.call_graph_scroll.setWidgetResizable(True)
        
        call_graph_layout.addLayout(graph_controls)
        call_graph_layout.addWidget(self.call_graph_scroll)
        
        # === LIVE MEMORY TRACKER TAB ===
        memory_widget = QWidget()
        memory_layout = QVBoxLayout(memory_widget)
        
        # Memory tracker controls
        memory_controls = QHBoxLayout()
        self.start_tracking_button = QPushButton("🔍 Start Tracking")
        self.stop_tracking_button = QPushButton("🛑 Stop Tracking")
        self.execute_file_button = QPushButton("▶️ Execute Current File")
        self.clear_memory_button = QPushButton("🗑️ Clear History")
        
        self.start_tracking_button.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.stop_tracking_button.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.execute_file_button.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.clear_memory_button.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        
        self.stop_tracking_button.setEnabled(False)
        
        memory_controls.addWidget(self.start_tracking_button)
        memory_controls.addWidget(self.stop_tracking_button)
        memory_controls.addWidget(self.execute_file_button)
        memory_controls.addWidget(self.clear_memory_button)
        memory_controls.addStretch()
        
        # Memory stats
        self.memory_stats_label = QLabel("Memory tracking inactive")
        self.memory_stats_label.setFont(QFont("Segoe UI", 8))
        
        # Variables display
        variables_label = QLabel("🔍 Live Variables")
        variables_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        
        self.variables_tree = QTreeWidget()
        self.variables_tree.setHeaderLabels(["Variable", "Value", "Type", "Size"])
        self.variables_tree.setAlternatingRowColors(True)
        
        # Execution history
        history_label = QLabel("📊 Execution History")
        history_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        
        self.execution_history_tree = QTreeWidget()
        self.execution_history_tree.setHeaderLabels(["Function", "Line", "Event", "Time"])
        self.execution_history_tree.setAlternatingRowColors(True)
        self.execution_history_tree.setMaximumHeight(150)
        
        memory_layout.addLayout(memory_controls)
        memory_layout.addWidget(self.memory_stats_label)
        memory_layout.addWidget(variables_label)
        memory_layout.addWidget(self.variables_tree)
        memory_layout.addWidget(history_label)
        memory_layout.addWidget(self.execution_history_tree)
        
        # === PIPELINE DESIGNER TAB ===
        self.pipeline_designer = PipelineDesigner()
        
        # === XPUNIT CONSOLIDATOR TAB ===
        self.xpunit_consolidator = XPUnitConsolidatorWidget()
        
        # === LIFECYCLE TRACER TAB ===
        self.lifecycle_tracer = LifecycleTracerWidget()
        
        # === NOTEBOOK INTEGRATION TAB ===
        self.notebook_integration = NotebookIntegrationWidget()
        
        # === HOLOGRAPHIC MEMORY TAB ===
        self.holographic_memory = HolographicMemoryWidget()
        
        # === RIGHT: Tabbed Viewer ===
        right_tabs = QTabWidget()
        right_tabs.addTab(self.code_view, "📄 Code Viewer")
        right_tabs.addTab(llm_widget, "🤖 LLM Query")
        right_tabs.addTab(call_graph_widget, "📊 Call Graph")
        right_tabs.addTab(memory_widget, "🧠 Live Memory")
        right_tabs.addTab(self.pipeline_designer, "🧩 Pipeline Designer")
        right_tabs.addTab(self.xpunit_consolidator, "🧬 XPUnit Analysis")
        right_tabs.addTab(self.lifecycle_tracer, "🔬 Lifecycle Tracer")
        right_tabs.addTab(self.notebook_integration, "📓 Notebook Testing")
        right_tabs.addTab(self.holographic_memory, "🧠 Holographic Memory")
        
        # === Add All Panels to Splitter ===
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.tree_view)
        splitter.addWidget(middle_panel)
        splitter.addWidget(right_tabs)
        splitter.setSizes([250, 350, 800])
        
        layout.addWidget(splitter)
    
    def setup_menu_bar(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        refresh_action = QAction("Refresh File Tree", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_file_tree)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # LLM menu
        llm_menu = menubar.addMenu("LLM")
        
        test_connection_action = QAction("Test Ollama Connection", self)
        test_connection_action.triggered.connect(self.test_llm_connection)
        llm_menu.addAction(test_connection_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Click on a Python file to explore its structure")
    
    def setup_connections(self):
        """Set up signal connections."""
        # File browser connections
        self.tree_view.clicked.connect(self.on_file_clicked)
        
        # Search connections
        self.search_bar.textChanged.connect(self.filter_structure_view)
        
        # Structure view connections
        self.structure_view.itemClicked.connect(self.on_structure_item_clicked)
        
        # LLM connections
        self.llm_button.clicked.connect(self.send_to_llm)
        self.clear_button.clicked.connect(self.clear_llm_panels)
        self.context_button.clicked.connect(self.add_file_context)
        
        # Call graph connections
        self.visualize_button.clicked.connect(self.visualize_call_graph)
        
        # Memory tracking connections
        self.start_tracking_button.clicked.connect(self.start_memory_tracking)
        self.stop_tracking_button.clicked.connect(self.stop_memory_tracking)
        self.execute_file_button.clicked.connect(self.execute_current_file)
        self.clear_memory_button.clicked.connect(self.clear_memory_history)
        
        # Test connection on startup
        self.test_llm_connection()
    
    def on_file_clicked(self, index: QModelIndex):
        """Handle file click events from the file browser."""
        file_path = self.file_model.filePath(index)
        
        if os.path.isfile(file_path) and file_path.endswith(".py"):
            file_path_obj = Path(file_path)
            self.current_file = file_path_obj
            
            # Update panels
            self.populate_structure_view(file_path_obj)
            self.show_code(file_path_obj)
            
            # Update status
            self.status_bar.showMessage(f"Loaded: {file_path_obj.name}")
    
    def populate_structure_view(self, file_path: Path):
        """Populate the structure view with parsed Python file content."""
        self.structure_view.clear()
        
        try:
            # Use enhanced dictionary parser
            parsed = self.ast_parser.parse_file_to_dict(file_path)
            
            if "_error" in parsed:
                error_item = QTreeWidgetItem(["❌ Parse Error", "Error", ""])
                error_item.addChild(QTreeWidgetItem([parsed["_error"], "", ""]))
                self.structure_view.addTopLevelItem(error_item)
                return
            
            # Add parsed elements
            for item_name, details in parsed.items():
                parent_item = QTreeWidgetItem([
                    item_name, 
                    details["type"].title(), 
                    str(details["line_start"])
                ])
                
                # Set icons and expand classes
                if details["type"] == "class":
                    parent_item.setText(0, f"🏛️ {item_name}")
                    parent_item.setExpanded(True)
                    
                    # Add methods if they exist
                    if "methods" in details and details["methods"]:
                        for method in details["methods"]:
                            method_info = details["children"].get(method, {})
                            method_item = QTreeWidgetItem([
                                f"⚙️ {method}",
                                method_info.get("type", "method").title(),
                                str(method_info.get("line_start", ""))
                            ])
                            # Store method info for click handling
                            method_item.setData(0, Qt.ItemDataRole.UserRole, (file_path, method_info))
                            parent_item.addChild(method_item)
                
                elif details["type"] in ["function", "async_function"]:
                    icon = "⚡" if details["type"] == "async_function" else "⚙️"
                    parent_item.setText(0, f"{icon} {item_name}")
                
                # Store element info for click handling
                parent_item.setData(0, Qt.ItemDataRole.UserRole, (file_path, details))
                self.structure_view.addTopLevelItem(parent_item)
            
            # Update status with counts
            class_count = len([d for d in parsed.values() if d["type"] == "class"])
            func_count = len([d for d in parsed.values() if d["type"] in ["function", "async_function"]])
            total_methods = sum(len(d.get("methods", [])) for d in parsed.values() if d["type"] == "class")
            
            self.status_bar.showMessage(
                f"Parsed {file_path.name}: {class_count} classes, {func_count} functions, {total_methods} methods"
            )
            
        except Exception as e:
            error_item = QTreeWidgetItem([f"❌ Error: {str(e)}", "Error", ""])
            self.structure_view.addTopLevelItem(error_item)
            self.status_bar.showMessage(f"Error parsing {file_path.name}: {str(e)}")
    
    def show_code(self, file_path: Path, line_start: int = None, line_end: int = None):
        """Show code in the code viewer."""
        try:
            if line_start and line_end:
                # Show specific lines
                content = self.ast_parser.get_file_content_lines(file_path, line_start, line_end)
                title = f"📄 {file_path.name} (lines {line_start}-{line_end})"
            else:
                # Show entire file
                content = self.ast_parser.get_file_content_lines(file_path)
                title = f"📄 {file_path.name}"
            
            self.code_view.setPlainText(content)
            
            # Update tab title
            tab_widget = self.code_view.parent().parent()
            if hasattr(tab_widget, 'setTabText'):
                tab_widget.setTabText(0, title)
            
        except Exception as e:
            self.code_view.setPlainText(f"Error loading file: {str(e)}")
    
    def on_structure_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle structure item click events."""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if data and isinstance(data, tuple):
            file_path, element_info = data
            
            if isinstance(element_info, dict) and "line_start" in element_info:
                # Show specific element
                line_start = element_info.get("line_start")
                line_end = element_info.get("line_end")
                self.show_code(file_path, line_start, line_end)
        elif self.current_file:
            # Show entire current file
            self.show_code(self.current_file)
    
    # ✅ 3. IMPLEMENT SEARCH FUNCTION
    def filter_structure_view(self, text: str):
        """Filter the structure view based on search text."""
        text = text.lower()
        root = self.structure_view.invisibleRootItem()
        
        if not text:
            # Show all items if search is empty
            for i in range(root.childCount()):
                item = root.child(i)
                self.show_all_children(item)
        else:
            # Filter items based on search text
            for i in range(root.childCount()):
                item = root.child(i)
                visible = self.match_structure(item, text)
                item.setHidden(not visible)
    
    def match_structure(self, item: QTreeWidgetItem, text: str) -> bool:
        """Check if item or its children match the search text."""
        # Check current item
        if text in item.text(0).lower():
            self.show_all_children(item)  # Show all children if parent matches
            return True
        
        # Check children
        has_matching_child = False
        for i in range(item.childCount()):
            child = item.child(i)
            if self.match_structure(child, text):
                has_matching_child = True
        
        return has_matching_child
    
    def show_all_children(self, item: QTreeWidgetItem):
        """Show all children of an item."""
        item.setHidden(False)
        for i in range(item.childCount()):
            child = item.child(i)
            child.setHidden(False)
            self.show_all_children(child)
    
    # ✅ 4. IMPLEMENT LLM PROMPT INTERFACE
    def send_to_llm(self):
        """Send prompt to LLM via Ollama."""
        prompt = self.llm_input.toPlainText().strip()
        if not prompt:
            self.llm_output.setPlainText("❌ Prompt is empty.")
            return
        
        # Disable button during request
        self.llm_button.setEnabled(False)
        self.llm_button.setText("🔄 Sending...")
        self.llm_status.setText("🟡 Processing...")
        self.llm_output.setPlainText("🔄 Sending request to Mistral LLM...")
        
        # Create and start worker thread
        self.llm_worker = LLMWorker(prompt)
        self.llm_worker.response_ready.connect(self.on_llm_response)
        self.llm_worker.error_occurred.connect(self.on_llm_error)
        self.llm_worker.start()
    
    def on_llm_response(self, response: str):
        """Handle successful LLM response."""
        self.llm_output.setPlainText(response)
        self.llm_status.setText("🟢 Response received")
        self.llm_button.setEnabled(True)
        self.llm_button.setText("🚀 Send Prompt")
        self.status_bar.showMessage("LLM response received", 3000)
    
    def on_llm_error(self, error: str):
        """Handle LLM error."""
        self.llm_output.setPlainText(f"❌ {error}")
        self.llm_status.setText("🔴 Error")
        self.llm_button.setEnabled(True)
        self.llm_button.setText("🚀 Send Prompt")
        self.status_bar.showMessage("LLM request failed", 3000)
    
    def test_llm_connection(self):
        """Test connection to Ollama."""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                self.llm_status.setText("🟢 Connected")
                self.status_bar.showMessage("Ollama connection successful", 3000)
            else:
                self.llm_status.setText("🔴 Connection Error")
        except:
            self.llm_status.setText("🔴 Disconnected")
    
    def clear_llm_panels(self):
        """Clear LLM input and output panels."""
        self.llm_input.clear()
        self.llm_output.setPlainText("LLM responses will appear here.\n\nMake sure Ollama is running with: ollama run mistral")
        self.llm_status.setText("🔴 Cleared")
    
    def add_file_context(self):
        """Add current file context to LLM prompt."""
        if not self.current_file:
            QMessageBox.information(self, "No File Selected", "Please select a Python file first.")
            return
        
        try:
            # Get file structure
            parsed = self.ast_parser.parse_file_to_dict(self.current_file)
            
            context = f"\n\n--- Context: {self.current_file.name} ---\n"
            context += f"File: {self.current_file}\n\n"
            
            if "_error" not in parsed:
                context += "Structure:\n"
                for name, details in parsed.items():
                    context += f"- {details['type'].title()}: {name}\n"
                    if details["type"] == "class" and "methods" in details:
                        for method in details["methods"]:
                            context += f"  - Method: {method}\n"
            
            # Add to current prompt
            current_text = self.llm_input.toPlainText()
            self.llm_input.setPlainText(current_text + context)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add context: {str(e)}")
    
    def visualize_call_graph(self):
        """Generate and display call graph visualization."""
        if not self.current_file:
            QMessageBox.information(self, "No File Selected", "Please select a Python file first.")
            return
        
        try:
            # Update button state
            self.visualize_button.setEnabled(False)
            self.visualize_button.setText("🔄 Generating...")
            self.graph_stats_label.setText("Analyzing code structure...")
            
            # Analyze the file
            analysis = self.call_graph_visualizer.analyze_file(self.current_file)
            
            if "error" in analysis:
                QMessageBox.warning(self, "Analysis Error", f"Failed to analyze file: {analysis['error']}")
                return
            
            # Generate visualization
            image_path = self.call_graph_visualizer.create_matplotlib_graph()
            
            # Load and display the image
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                # Create new label with the image
                image_label = QLabel()
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Replace the placeholder label
                self.call_graph_scroll.setWidget(image_label)
                
                # Update stats
                stats = self.call_graph_visualizer.get_graph_stats()
                stats_text = f"Nodes: {stats.get('total_nodes', 0)}, Edges: {stats.get('total_edges', 0)}, Classes: {stats.get('classes', 0)}, Functions: {stats.get('functions', 0)}"
                self.graph_stats_label.setText(stats_text)
                
                self.status_bar.showMessage(f"Call graph generated for {self.current_file.name}", 3000)
            else:
                QMessageBox.warning(self, "Display Error", "Failed to load generated image.")
            
        except Exception as e:
            QMessageBox.critical(self, "Visualization Error", f"Failed to generate call graph: {str(e)}")
            self.graph_stats_label.setText("Error generating call graph")
        
        finally:
            # Reset button state
            self.visualize_button.setEnabled(True)
            self.visualize_button.setText("🔍 Visualize Call Graph")
    
    def start_memory_tracking(self):
        """Start live memory tracking."""
        try:
            # Add callback to update GUI
            self.memory_tracker.add_callback(self.update_memory_display)
            
            # Start tracking
            self.memory_tracker.start_tracing()
            
            # Update UI
            self.start_tracking_button.setEnabled(False)
            self.stop_tracking_button.setEnabled(True)
            self.memory_stats_label.setText("🟢 Memory tracking active")
            
            self.status_bar.showMessage("Memory tracking started", 2000)
            
        except Exception as e:
            QMessageBox.critical(self, "Tracking Error", f"Failed to start memory tracking: {str(e)}")
    
    def stop_memory_tracking(self):
        """Stop live memory tracking."""
        try:
            self.memory_tracker.stop_tracing()
            
            # Update UI
            self.start_tracking_button.setEnabled(True)
            self.stop_tracking_button.setEnabled(False)
            self.memory_stats_label.setText("🔴 Memory tracking stopped")
            
            self.status_bar.showMessage("Memory tracking stopped", 2000)
            
        except Exception as e:
            QMessageBox.critical(self, "Tracking Error", f"Failed to stop memory tracking: {str(e)}")
    
    def execute_current_file(self):
        """Execute the current file with memory tracking."""
        if not self.current_file:
            QMessageBox.information(self, "No File Selected", "Please select a Python file first.")
            return
        
        try:
            # Update button state
            self.execute_file_button.setEnabled(False)
            self.execute_file_button.setText("⏳ Executing...")
            
            # Execute file
            result = self.code_executor.execute_file(self.current_file)
            
            if result["success"]:
                self.status_bar.showMessage(f"Executed {self.current_file.name} in {result['execution_time']:.3f}s", 3000)
                
                # Update memory display
                self.update_memory_stats()
                
                QMessageBox.information(
                    self, 
                    "Execution Complete", 
                    f"File executed successfully!\n\nExecution time: {result['execution_time']:.3f} seconds"
                )
            else:
                QMessageBox.warning(
                    self, 
                    "Execution Error", 
                    f"Failed to execute file:\n\n{result['error']}"
                )
            
        except Exception as e:
            QMessageBox.critical(self, "Execution Error", f"Failed to execute file: {str(e)}")
        
        finally:
            # Reset button state
            self.execute_file_button.setEnabled(True)
            self.execute_file_button.setText("▶️ Execute Current File")
    
    def clear_memory_history(self):
        """Clear memory tracking history."""
        self.memory_tracker.clear_history()
        self.variables_tree.clear()
        self.execution_history_tree.clear()
        self.memory_stats_label.setText("Memory history cleared")
        self.status_bar.showMessage("Memory history cleared", 2000)
    
    def update_memory_display(self, frame):
        """Update the memory display with new execution frame."""
        try:
            # Update execution history (limit to last 50 entries)
            if self.execution_history_tree.topLevelItemCount() > 50:
                self.execution_history_tree.takeTopLevelItem(0)
            
            # Add new execution frame
            time_str = frame.timestamp.strftime("%H:%M:%S.%f")[:-3]
            history_item = QTreeWidgetItem([
                frame.function_name,
                str(frame.line_number),
                frame.event_type,
                time_str
            ])
            self.execution_history_tree.addTopLevelItem(history_item)
            self.execution_history_tree.scrollToBottom()
            
            # Update variables if this is a line event
            if frame.event_type == 'line' and frame.variables:
                self.update_variables_display(frame.variables)
            
            # Update stats
            self.update_memory_stats()
            
        except Exception as e:
            print(f"Error updating memory display: {e}")
    
    def update_variables_display(self, variables):
        """Update the variables tree display."""
        try:
            self.variables_tree.clear()
            
            for var_name, var_state in variables.items():
                # Format value for display
                value_str = str(var_state.value)
                if len(value_str) > 50:
                    value_str = value_str[:47] + "..."
                
                # Format size
                size_str = f"{var_state.size} bytes" if var_state.size > 0 else "N/A"
                
                var_item = QTreeWidgetItem([
                    var_name,
                    value_str,
                    var_state.type_name,
                    size_str
                ])
                
                self.variables_tree.addTopLevelItem(var_item)
            
        except Exception as e:
            print(f"Error updating variables display: {e}")
    
    def update_memory_stats(self):
        """Update memory tracking statistics."""
        try:
            stats = self.memory_tracker.get_stats()
            
            stats_text = (
                f"Frames: {stats['total_frames']}, "
                f"Variables: {stats['total_variables']}, "
                f"Memory: {stats['total_memory_bytes']} bytes"
            )
            
            if stats['is_tracing']:
                stats_text = "🟢 " + stats_text
            else:
                stats_text = "🔴 " + stats_text
            
            self.memory_stats_label.setText(stats_text)
            
        except Exception as e:
            print(f"Error updating memory stats: {e}")
    
    def refresh_file_tree(self):
        """Refresh the file tree."""
        self.file_model.setRootPath(str(self.project_root))
        self.status_bar.showMessage("File tree refreshed", 2000)
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Enhanced LLM Consciousness GUI",
            "<h3>🧠 Enhanced LLM Consciousness GUI</h3>"
            "<p>Advanced code exploration with AI integration:</p>"
            "<p><strong>✅ Features:</strong></p>"
            "<ul>"
            "<li>📁 <strong>File Browser:</strong> All .py files in project</li>"
            "<li>🔍 <strong>Search Bar:</strong> Real-time structure filtering</li>"
            "<li>🏗️ <strong>Structure View:</strong> Hierarchical code organization</li>"
            "<li>📄 <strong>Code Viewer:</strong> Full file and section viewing</li>"
            "<li>🤖 <strong>LLM Integration:</strong> Mistral via Ollama</li>"
            "</ul>"
            "<p><em>Built with PySide6, enhanced AST parsing, and AI integration</em></p>"
        )


def main():
    """Main entry point for the enhanced GUI with LLM."""
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("🧠 Enhanced LLM Consciousness GUI")
    app.setApplicationVersion("1.0.0")
    
    # Get the project root directory
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    # Create and show the enhanced window
    window = EnhancedMainWindowWithLLM(project_root)
    window.show()
    
    print("🧠 ENHANCED GUI WITH SEARCH + LLM - COMPLETE!")
    print("=" * 70)
    print("✅ Left Panel: File browser (.py files)")
    print("✅ Middle Panel: Searchable class/function structure")
    print("✅ Right Panel: Code viewer + LLM query interface")
    print()
    print("🔍 SEARCH FUNCTIONALITY:")
    print("  • Real-time filtering of structure view")
    print("  • Search classes, functions, and methods")
    print("  • Hierarchical matching with parent/child visibility")
    print()
    print("🤖 LLM INTEGRATION:")
    print("  • Mistral LLM via Ollama")
    print("  • Threaded requests (non-blocking UI)")
    print("  • Context-aware prompts")
    print("  • Connection status monitoring")
    print()
    print("🚀 Ready for AI-powered code exploration!")
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
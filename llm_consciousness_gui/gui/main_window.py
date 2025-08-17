"""
Main Window for the LLM Consciousness GUI.

This module provides the main application window with a split view:
- Left panel: File explorer with code structure
- Right panel: Code viewer and analysis
"""

# 🧱 1. Update Imports in main_window.py
import os
from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import (
    QFileSystemModel, QTreeView, QPlainTextEdit, QMainWindow, QSplitter, 
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QHBoxLayout, 
    QLabel, QStatusBar, QMenuBar, QMenu, QToolBar, QMessageBox, QTextEdit,
    QTabWidget, QFrame
)
from PySide6.QtCore import Qt, QTimer, Signal, QDir
from PySide6.QtGui import QAction, QFont, QTextCharFormat, QColor, QIcon

from llm_consciousness_gui.gui.file_explorer import FileExplorerWidget
from llm_consciousness_gui.parser.ast_parser import ASTParser, CodeElement


class CodeViewer(QWidget):
    """Widget for displaying and analyzing code."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None
        self.ast_parser = ASTParser()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the code viewer interface."""
        layout = QVBoxLayout(self)
        
        # Create tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Code view tab
        self.code_editor = QPlainTextEdit()
        self.code_editor.setReadOnly(True)
        self.code_editor.setFont(QFont("Consolas", 10))
        self.code_editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.tab_widget.addTab(self.code_editor, "Code")
        
        # Analysis tab
        self.analysis_view = QTextEdit()
        self.analysis_view.setReadOnly(True)
        self.analysis_view.setFont(QFont("Segoe UI", 9))
        self.tab_widget.addTab(self.analysis_view, "Analysis")
        
        # Info panel
        self.info_label = QLabel("Select a file or code element to view")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("QLabel { color: gray; font-style: italic; }")
        
        layout.addWidget(self.info_label)
        layout.addWidget(self.tab_widget)
    
    def display_file(self, file_path: Path):
        """Display the contents of a file."""
        self.current_file = file_path
        
        try:
            content = self.ast_parser.get_file_content_lines(file_path)
            self.code_editor.setPlainText(content)
            
            # Update info label
            relative_path = file_path.name
            self.info_label.setText(f"File: {relative_path}")
            
            # Generate analysis
            self.generate_file_analysis(file_path)
            
        except Exception as e:
            self.code_editor.setPlainText(f"Error loading file: {str(e)}")
            self.info_label.setText(f"Error: {file_path.name}")
    
    def display_code_element(self, file_path: Path, element: CodeElement):
        """Display a specific code element."""
        self.current_file = file_path
        
        try:
            # Get the specific lines for this element
            content = self.ast_parser.get_file_content_lines(
                file_path, element.line_start, element.line_end
            )
            self.code_editor.setPlainText(content)
            
            # Update info label
            element_info = f"{element.type.title()}: {element.name}"
            if element.parent:
                element_info += f" (in {element.parent})"
            element_info += f" - Lines {element.line_start}-{element.line_end}"
            self.info_label.setText(element_info)
            
            # Generate element analysis
            self.generate_element_analysis(file_path, element)
            
        except Exception as e:
            self.code_editor.setPlainText(f"Error loading code element: {str(e)}")
            self.info_label.setText(f"Error: {element.name}")
    
    def generate_file_analysis(self, file_path: Path):
        """Generate analysis for a file."""
        try:
            # Use the enhanced dictionary parser
            structure_dict = self.ast_parser.parse_file_to_dict(file_path)
            
            if "_error" in structure_dict:
                self.analysis_view.setPlainText(f"Error parsing file: {structure_dict['_error']}")
                return
            
            analysis = f"<h3>📄 File Analysis: {file_path.name}</h3>"
            analysis += f"<p><strong>📍 Path:</strong> {file_path}</p>"
            
            # Count elements using dictionary structure
            classes = {k: v for k, v in structure_dict.items() if v["type"] == "class"}
            functions = {k: v for k, v in structure_dict.items() if v["type"] in ["function", "async_function"]}
            
            analysis += f"<p><strong>🏛️ Classes:</strong> {len(classes)}</p>"
            analysis += f"<p><strong>⚙️ Functions:</strong> {len(functions)}</p>"
            
            # Calculate total methods
            total_methods = sum(len(cls_info.get("methods", [])) for cls_info in classes.values())
            analysis += f"<p><strong>🔧 Total Methods:</strong> {total_methods}</p>"
            
            # List classes with enhanced info
            if classes:
                analysis += "<h4>🏛️ Classes:</h4><ul>"
                for cls_name, cls_info in classes.items():
                    methods = cls_info.get("methods", [])
                    analysis += f"<li><strong>{cls_name}</strong> ({len(methods)} methods)"
                    analysis += f"<br>📍 Lines: {cls_info['line_start']}-{cls_info['line_end']}"
                    
                    if cls_info.get("docstring"):
                        doc = cls_info["docstring"][:100]
                        analysis += f"<br>📝 <em>{doc}{'...' if len(cls_info['docstring']) > 100 else ''}</em>"
                    
                    if methods:
                        analysis += f"<br>🔧 Methods: {', '.join(methods[:5])}"
                        if len(methods) > 5:
                            analysis += f" <em>(+{len(methods)-5} more)</em>"
                    
                    analysis += "</li>"
                analysis += "</ul>"
            
            # List functions with enhanced info
            if functions:
                analysis += "<h4>⚙️ Functions:</h4><ul>"
                for func_name, func_info in functions.items():
                    func_icon = "⚡" if func_info["type"] == "async_function" else "⚙️"
                    analysis += f"<li>{func_icon} <strong>{func_name}</strong>"
                    analysis += f"<br>📍 Lines: {func_info['line_start']}-{func_info['line_end']}"
                    
                    if func_info.get("args"):
                        args = func_info["args"]
                        analysis += f"<br>📥 Args: {', '.join(args)}"
                    
                    if func_info.get("returns"):
                        analysis += f"<br>📤 Returns: {func_info['returns']}"
                    
                    if func_info.get("docstring"):
                        doc = func_info["docstring"][:100]
                        analysis += f"<br>📝 <em>{doc}{'...' if len(func_info['docstring']) > 100 else ''}</em>"
                    
                    analysis += "</li>"
                analysis += "</ul>"
            
            # Add complexity metrics
            analysis += "<h4>📊 Code Metrics:</h4>"
            analysis += f"<p>• <strong>Total Elements:</strong> {len(structure_dict)}</p>"
            analysis += f"<p>• <strong>Class/Function Ratio:</strong> {len(classes)}:{len(functions)}</p>"
            if classes:
                avg_methods = total_methods / len(classes)
                analysis += f"<p>• <strong>Average Methods per Class:</strong> {avg_methods:.1f}</p>"
            
            self.analysis_view.setHtml(analysis)
            
        except Exception as e:
            # Fallback to original method
            try:
                elements = self.ast_parser.parse_file(file_path)
                
                analysis = f"<h3>File Analysis: {file_path.name}</h3>"
                analysis += f"<p><strong>Path:</strong> {file_path}</p>"
                
                # Count elements
                classes = [e for e in elements if e.type == 'class']
                functions = [e for e in elements if e.type in ['function', 'async_function']]
                
                analysis += f"<p><strong>Classes:</strong> {len(classes)}</p>"
                analysis += f"<p><strong>Functions:</strong> {len(functions)}</p>"
                
                self.analysis_view.setHtml(analysis)
                
            except Exception as fallback_e:
                self.analysis_view.setPlainText(f"Error generating analysis: {str(e)}")
    
    def generate_element_analysis(self, file_path: Path, element: CodeElement):
        """Generate analysis for a specific code element."""
        analysis = f"<h3>{element.type.title()} Analysis: {element.name}</h3>"
        analysis += f"<p><strong>File:</strong> {file_path.name}</p>"
        analysis += f"<p><strong>Lines:</strong> {element.line_start} - {element.line_end}</p>"
        
        if element.parent:
            analysis += f"<p><strong>Parent Class:</strong> {element.parent}</p>"
        
        if element.docstring:
            analysis += f"<h4>Documentation:</h4>"
            analysis += f"<p><em>{element.docstring}</em></p>"
        
        if element.children:
            analysis += f"<h4>Methods ({len(element.children)}):</h4><ul>"
            for child in element.children:
                analysis += f"<li><strong>{child.name}</strong> (line {child.line_start})"
                if child.docstring:
                    analysis += f"<br><em>{child.docstring[:100]}...</em>"
                analysis += "</li>"
            analysis += "</ul>"
        
        self.analysis_view.setHtml(analysis)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, project_root: Path, parent=None):
        super().__init__(parent)
        self.project_root = project_root
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_connections()
    
    def setup_ui(self):
        """Set up the main user interface."""
        self.setWindowTitle("LLM Consciousness GUI - Lumina Memory System")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QHBoxLayout(central_widget)
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create file explorer (left panel)
        self.file_explorer = FileExplorerWidget(self.project_root)
        self.file_explorer.setMinimumWidth(300)
        self.file_explorer.setMaximumWidth(500)
        
        # Create code viewer (right panel)
        self.code_viewer = CodeViewer()
        
        # Add widgets to splitter
        splitter.addWidget(self.file_explorer)
        splitter.addWidget(self.code_viewer)
        
        # Set splitter proportions (30% left, 70% right)
        splitter.setSizes([300, 700])
        
        layout.addWidget(splitter)
    
    def setup_menu_bar(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        refresh_action = QAction("Refresh Project", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_project)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        expand_all_action = QAction("Expand All", self)
        expand_all_action.triggered.connect(self.file_explorer.expand_all)
        view_menu.addAction(expand_all_action)
        
        collapse_all_action = QAction("Collapse All", self)
        collapse_all_action.triggered.connect(self.file_explorer.collapse_all)
        view_menu.addAction(collapse_all_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Project: {self.project_root.name}")
    
    def setup_connections(self):
        """Set up signal connections between widgets."""
        self.file_explorer.file_selected.connect(self.on_file_selected)
        self.file_explorer.code_element_selected.connect(self.on_code_element_selected)
        
        # Add three-panel functionality if enabled
        if hasattr(self, 'file_browser_tree'):
            self.file_browser_tree.clicked.connect(self.on_file_browser_clicked)
    
    def on_file_selected(self, file_path: Path):
        """Handle file selection from the explorer."""
        self.code_viewer.display_file(file_path)
        self.status_bar.showMessage(f"Viewing: {file_path.name}")
    
    def on_code_element_selected(self, file_path: Path, element: CodeElement):
        """Handle code element selection from the explorer."""
        self.code_viewer.display_code_element(file_path, element)
        element_info = f"{element.type.title()}: {element.name}"
        if element.parent:
            element_info += f" (in {element.parent})"
        self.status_bar.showMessage(f"Viewing: {element_info}")
    
    def refresh_project(self):
        """Refresh the project structure."""
        self.file_explorer.refresh_structure()
        self.status_bar.showMessage("Project refreshed", 2000)
    
    # 🧱 3. Populate the Tree with Parser Output
    def populate_tree_view(self, file_path: Path):
        """
        Populate tree view with parsed Python file structure.
        This method demonstrates the enhanced tree population as requested.
        """
        if not hasattr(self, 'enhanced_tree'):
            # Create enhanced tree widget if it doesn't exist
            self.enhanced_tree = QTreeWidget()
            self.enhanced_tree.setHeaderLabels(["Structure", "Type", "Line"])
        
        self.enhanced_tree.clear()
        
        try:
            # Use our enhanced dictionary parser
            parsed = self.file_explorer.ast_parser.parse_file_to_dict(file_path)
            
            if "_error" in parsed:
                error_item = QTreeWidgetItem(["❌ Parse Error", "Error", ""])
                self.enhanced_tree.addTopLevelItem(error_item)
                return
            
            # Add parsed elements to tree
            for item_name, details in parsed.items():
                parent_item = QTreeWidgetItem([item_name, details["type"].title(), str(details["line_start"])])
                
                # Set icons and expand classes
                if details["type"] == "class":
                    parent_item.setText(0, f"🏛️ {item_name}")
                    parent_item.setExpanded(True)
                    
                    # Add methods if they exist
                    if "methods" in details:
                        for method in details["methods"]:
                            method_info = details["children"].get(method, {})
                            method_item = QTreeWidgetItem([
                                f"⚙️ {method}",
                                method_info.get("type", "method").title(),
                                str(method_info.get("line_start", ""))
                            ])
                            parent_item.addChild(method_item)
                
                elif details["type"] in ["function", "async_function"]:
                    icon = "⚡" if details["type"] == "async_function" else "⚙️"
                    parent_item.setText(0, f"{icon} {item_name}")
                
                self.enhanced_tree.addTopLevelItem(parent_item)
            
            print(f"✅ Tree populated for {file_path.name}")
            
        except Exception as e:
            print(f"❌ Error populating tree: {e}")
    
    def show_code(self, file_path: Path):
        """Show code in the code viewer."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            self.code_viewer.code_editor.setPlainText(code)
            print(f"✅ Code displayed for {file_path.name}")
        except Exception as e:
            self.code_viewer.code_editor.setPlainText(f"Error loading file: {str(e)}")
            print(f"❌ Error showing code: {e}")
    
    def demo_tree_population(self):
        """
        Demo method to test tree population with sample file.
        Call this to test the enhanced tree functionality.
        """
        # Test with sample_code.py
        sample_file = self.project_root / "llm_consciousness_gui" / "sample_code.py"
        
        if sample_file.exists():
            print("🎯 Testing tree population with sample_code.py")
            self.populate_tree_view(sample_file)
            self.show_code(sample_file)
            
            # Update status
            self.status_bar.showMessage(f"Demo: Loaded {sample_file.name} - Tree shows MemoryUnit, ReferencePoint, and standalone_function")
        else:
            print("⚠️ sample_code.py not found, using existing file")
            # Fallback to any Python file in the project
            for py_file in self.project_root.rglob("*.py"):
                if py_file.name != "__init__.py":
                    self.populate_tree_view(py_file)
                    self.show_code(py_file)
                    break

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About LLM Consciousness GUI",
            "<h3>🎯 Enhanced LLM Consciousness GUI</h3>"
            "<p>A visualization tool for exploring Python code structure "
            "in the Lumina Memory System project.</p>"
            "<p><strong>✅ Enhanced Features:</strong></p>"
            "<ul>"
            "<li>📁 Python file loading and parsing</li>"
            "<li>🏛️ Class names (expandable to show methods)</li>"
            "<li>⚙️ Top-level function names</li>"
            "<li>🔍 Dictionary-based AST parsing</li>"
            "<li>📄 Click to view code functionality</li>"
            "<li>📊 Real-time code analysis</li>"
            "</ul>"
            "<p><em>Built with PySide6 and enhanced AST parsing</em></p>"
        )
    
    # 🔄 2. Replace Previous Tree Widget Logic - Three Panel Enhancement
    def enable_three_panel_mode(self):
        """
        Enable three-panel mode with file browser, structure view, and code viewer.
        This adds the enhanced functionality as requested.
        """
        # Create file system model for .py files
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(str(self.project_root))
        self.file_model.setNameFilters(["*.py"])
        self.file_model.setNameFilterDisables(False)
        
        # Create file browser tree view
        self.file_browser_tree = QTreeView()
        self.file_browser_tree.setModel(self.file_model)
        self.file_browser_tree.setRootIndex(self.file_model.index(str(self.project_root)))
        self.file_browser_tree.setHeaderHidden(True)
        self.file_browser_tree.setAlternatingRowColors(True)
        
        # Create structure view for parsed content
        self.structure_view = QTreeWidget()
        self.structure_view.setHeaderLabels(["Element", "Type", "Line"])
        self.structure_view.setAlternatingRowColors(True)
        
        print("✅ Three-panel mode enabled")
        return self.file_browser_tree, self.structure_view
    
    # 🧠 3. Add Event Listener to Parse Clicked File
    def on_file_browser_clicked(self, index):
        """Handle file browser click events."""
        file_path = self.file_model.filePath(index)
        
        if os.path.isfile(file_path) and file_path.endswith(".py"):
            file_path_obj = Path(file_path)
            self.populate_structure_view(file_path_obj)
            self.show_code(file_path_obj)
            
            # Update status
            self.status_bar.showMessage(f"Loaded: {file_path_obj.name}")
    
    # 🧱 4. Repurpose populate_tree_view() → populate_structure_view()
    def populate_structure_view(self, file_path: Path):
        """
        Populate the structure view with parsed Python file content.
        This replaces the previous populate_tree_view method.
        """
        if not hasattr(self, 'structure_view'):
            print("⚠️ Structure view not initialized. Call enable_three_panel_mode() first.")
            return
        
        self.structure_view.clear()
        
        try:
            # Use enhanced dictionary parser
            parsed_data = self.file_explorer.ast_parser.parse_file_to_dict(file_path)
            
            if "_error" in parsed_data:
                error_item = QTreeWidgetItem(["❌ Parse Error", "Error", ""])
                error_item.addChild(QTreeWidgetItem([parsed_data["_error"], "", ""]))
                self.structure_view.addTopLevelItem(error_item)
                return
            
            # Add parsed elements to structure view
            for item_name, details in parsed_data.items():
                parent_item = QTreeWidgetItem([
                    item_name, 
                    details["type"].title(), 
                    str(details["line_start"])
                ])
                
                # Set icons and handle classes
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
                            parent_item.addChild(method_item)
                
                elif details["type"] in ["function", "async_function"]:
                    icon = "⚡" if details["type"] == "async_function" else "⚙️"
                    parent_item.setText(0, f"{icon} {item_name}")
                
                self.structure_view.addTopLevelItem(parent_item)
            
            print(f"✅ Structure populated for {file_path.name}")
            
            # Update status with counts
            class_count = len([d for d in parsed_data.values() if d["type"] == "class"])
            func_count = len([d for d in parsed_data.values() if d["type"] in ["function", "async_function"]])
            total_methods = sum(len(d.get("methods", [])) for d in parsed_data.values() if d["type"] == "class")
            
            self.status_bar.showMessage(
                f"Parsed {file_path.name}: {class_count} classes, {func_count} functions, {total_methods} methods"
            )
            
        except Exception as e:
            error_item = QTreeWidgetItem([f"❌ Error: {str(e)}", "Error", ""])
            self.structure_view.addTopLevelItem(error_item)
            print(f"❌ Error populating structure: {e}")
    
    def demo_three_panel_mode(self):
        """
        Demo method to test the three-panel functionality.
        This shows how the enhanced layout works.
        """
        print("🎯 Demo: Three-Panel Mode")
        print("-" * 30)
        
        # Enable three-panel mode
        file_browser, structure_view = self.enable_three_panel_mode()
        
        # Test with a sample file
        sample_files = [
            self.project_root / "llm_consciousness_gui" / "sample_code.py",
            self.project_root / "src" / "lumina_memory" / "memory_system.py",
            self.project_root / "llm_consciousness_gui" / "parser" / "ast_parser.py"
        ]
        
        for sample_file in sample_files:
            if sample_file.exists():
                print(f"📁 Testing with: {sample_file.name}")
                self.populate_structure_view(sample_file)
                self.show_code(sample_file)
                
                self.status_bar.showMessage(f"Demo: Three-panel mode with {sample_file.name}")
                break
        
        print("✅ Three-panel demo complete!")
        print("📁 Left Panel: File browser (.py files)")
        print("🏗️ Middle Panel: Parsed structure")
        print("📄 Right Panel: Code viewer")
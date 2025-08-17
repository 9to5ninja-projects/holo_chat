#!/usr/bin/env python3
"""
Enhanced Three-Panel Main Window for LLM Consciousness GUI.

This implements the requested layout:
- Left Panel: File browser (.py files)
- Middle Panel: Parsed class/function structure  
- Right Panel: Code viewer
"""

import os
from pathlib import Path
from typing import Optional

# 🧠 Update main_window.py Imports
from PySide6.QtWidgets import (
    QFileSystemModel, QTreeView, QPlainTextEdit, QMainWindow, QSplitter, 
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QHBoxLayout, 
    QLabel, QStatusBar, QMenuBar, QMenu, QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt, Signal, QDir, QModelIndex
from PySide6.QtGui import QAction, QFont

from parser.ast_parser import ASTParser


class EnhancedThreePanelWindow(QMainWindow):
    """Enhanced main window with three-panel layout."""
    
    def __init__(self, project_root: Path, parent=None):
        super().__init__(parent)
        self.project_root = project_root
        self.ast_parser = ASTParser()
        self.current_file = None
        
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_connections()
    
    def setup_ui(self):
        """Set up the three-panel user interface."""
        self.setWindowTitle("🎯 Enhanced LLM Consciousness GUI - Three Panel Layout")
        self.setGeometry(100, 100, 1600, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QHBoxLayout(central_widget)
        
        # Create main splitter for three panels
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create the three panels
        left_panel = self.create_file_browser_panel()
        middle_panel = self.create_structure_panel()
        right_panel = self.create_code_viewer_panel()
        
        # Add panels to splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(middle_panel)
        main_splitter.addWidget(right_panel)
        
        # Set splitter proportions (25% left, 25% middle, 50% right)
        main_splitter.setSizes([300, 300, 600])
        
        layout.addWidget(main_splitter)
    
    def create_file_browser_panel(self):
        """Create the left panel with file browser."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Title label
        title = QLabel("📁 Python Files")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 🧱 1. Replace QTreeWidget with a QFileSystemModel View
        # Set up the file system model for .py files
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(str(self.project_root))
        self.file_model.setNameFilters(["*.py"])
        self.file_model.setNameFilterDisables(False)
        
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(str(self.project_root)))
        self.tree_view.setHeaderHidden(True)
        
        # Configure tree appearance
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setExpandsOnDoubleClick(True)
        
        layout.addWidget(self.tree_view)
        
        return panel
    
    def create_structure_panel(self):
        """Create the middle panel with parsed structure."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Title label
        self.structure_title = QLabel("🏗️ Code Structure")
        self.structure_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.structure_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.structure_title)
        
        # Structure view (QTreeWidget for parsed content)
        self.structure_view = QTreeWidget()
        self.structure_view.setHeaderLabels(["Element", "Type", "Line"])
        self.structure_view.setAlternatingRowColors(True)
        self.structure_view.setRootIsDecorated(True)
        
        layout.addWidget(self.structure_view)
        
        return panel
    
    def create_code_viewer_panel(self):
        """Create the right panel with code viewer."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Title label
        self.code_title = QLabel("📄 Select a file to view code")
        self.code_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.code_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.code_title)
        
        # Code view
        self.code_view = QPlainTextEdit()
        self.code_view.setReadOnly(True)
        self.code_view.setFont(QFont("Consolas", 10))
        self.code_view.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.code_view.setPlainText("Click on a Python file in the left panel to:\n\n"
                                   "• Parse its class/function structure\n"
                                   "• Populate the middle panel tree view\n"
                                   "• Show the source code here")
        
        layout.addWidget(self.code_view)
        
        return panel
    
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
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        expand_all_action = QAction("Expand All Structure", self)
        expand_all_action.triggered.connect(self.structure_view.expandAll)
        view_menu.addAction(expand_all_action)
        
        collapse_all_action = QAction("Collapse All Structure", self)
        collapse_all_action.triggered.connect(self.structure_view.collapseAll)
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
        self.status_bar.showMessage("Ready - Click on a Python file to parse its structure")
    
    def setup_connections(self):
        """Set up signal connections."""
        # 🧠 3. Add Event Listener to Parse Clicked File
        self.tree_view.clicked.connect(self.on_file_clicked)
        self.structure_view.itemClicked.connect(self.on_structure_item_clicked)
    
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
    
    # 🧱 4. Repurpose populate_tree_view() → populate_structure_view()
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
                self.structure_title.setText("🏗️ Parse Error")
                return
            
            # Update title
            self.structure_title.setText(f"🏗️ {file_path.name} Structure")
            
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
            self.structure_title.setText("🏗️ Parse Error")
            self.status_bar.showMessage(f"Error parsing {file_path.name}: {str(e)}")
    
    def show_code(self, file_path: Path, line_start: int = None, line_end: int = None):
        """Show code in the right panel."""
        try:
            if line_start and line_end:
                # Show specific lines
                content = self.ast_parser.get_file_content_lines(file_path, line_start, line_end)
                self.code_title.setText(f"📄 {file_path.name} (lines {line_start}-{line_end})")
            else:
                # Show entire file
                content = self.ast_parser.get_file_content_lines(file_path)
                self.code_title.setText(f"📄 {file_path.name}")
            
            self.code_view.setPlainText(content)
            
        except Exception as e:
            self.code_view.setPlainText(f"Error loading file: {str(e)}")
            self.code_title.setText(f"❌ Error loading {file_path.name}")
    
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
    
    def refresh_file_tree(self):
        """Refresh the file tree."""
        self.file_model.setRootPath(str(self.project_root))
        self.status_bar.showMessage("File tree refreshed", 2000)
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Enhanced Three-Panel GUI",
            "<h3>🎯 Enhanced LLM Consciousness GUI</h3>"
            "<p>Three-panel layout for comprehensive code exploration:</p>"
            "<p><strong>✅ Features:</strong></p>"
            "<ul>"
            "<li>📁 <strong>Left Panel:</strong> File browser (.py files)</li>"
            "<li>🏗️ <strong>Middle Panel:</strong> Parsed class/function structure</li>"
            "<li>📄 <strong>Right Panel:</strong> Code viewer</li>"
            "<li>🔍 Click file → parse structure → show code</li>"
            "<li>⚙️ Click structure element → show specific code</li>"
            "</ul>"
            "<p><em>Built with PySide6 and enhanced AST parsing</em></p>"
        )


def main():
    """Main entry point for the enhanced three-panel GUI."""
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("🎯 Enhanced Three-Panel LLM Consciousness GUI")
    app.setApplicationVersion("1.0.0")
    
    # Get the project root directory
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    # Create and show the enhanced window
    window = EnhancedThreePanelWindow(project_root)
    window.show()
    
    print("🎯 Enhanced Three-Panel Layout - COMPLETE!")
    print("=" * 60)
    print("✅ Left Panel: File browser (.py files)")
    print("✅ Middle Panel: Parsed class/function structure")
    print("✅ Right Panel: Code viewer")
    print()
    print("🔧 Click Functionality:")
    print("  📁 Click file → parse structure → show code")
    print("  🏗️ Click structure element → show specific code")
    print("  📊 Status bar shows parsing results")
    print()
    print("🚀 Ready for comprehensive code exploration!")
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
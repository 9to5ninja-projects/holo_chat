#!/usr/bin/env python3
"""
Enhanced Main Window with Focused Tree View Population
Following the specific requirements for tree view integration.
"""

import os
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QSplitter, QPlainTextEdit, QTreeWidget, QTreeWidgetItem,
    QLabel, QStatusBar, QMenuBar, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont

# Import our enhanced parser
from parser.ast_parser import ASTParser


class EnhancedMainWindow(QMainWindow):
    """Enhanced Main Window with focused tree view population."""
    
    def __init__(self, project_root: Path, parent=None):
        super().__init__(parent)
        self.project_root = project_root
        self.ast_parser = ASTParser()
        self.current_file = None
        
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_connections()
        
        # Load initial file for demonstration
        self.load_sample_files()
    
    def setup_ui(self):
        """Set up the main user interface."""
        self.setWindowTitle("🎯 Enhanced LLM Consciousness GUI - Tree View Focus")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QHBoxLayout(central_widget)
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create left panel with tree view
        left_panel = self.create_left_panel()
        
        # Create right panel with code view
        right_panel = self.create_right_panel()
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (40% left, 60% right)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
    
    def create_left_panel(self):
        """Create the left panel with tree view."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Title label
        title = QLabel("📁 Python Files & Structure")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 🧱 2. Replace QTreeView With QTreeWidget
        self.tree_view = QTreeWidget()
        self.tree_view.setHeaderLabels(["Structure", "Type", "Line"])
        
        # Configure tree appearance
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setRootIsDecorated(True)
        self.tree_view.setExpandsOnDoubleClick(True)
        
        layout.addWidget(self.tree_view)
        
        return panel
    
    def create_right_panel(self):
        """Create the right panel with code view."""
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
        self.code_view.setPlainText("Click on a Python file in the left panel to view its code here.")
        
        layout.addWidget(self.code_view)
        
        return panel
    
    def setup_menu_bar(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        load_file_action = QAction("Load Python File", self)
        load_file_action.triggered.connect(self.load_file_dialog)
        file_menu.addAction(load_file_action)
        
        refresh_action = QAction("Refresh Tree", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_tree)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Load a Python file to see its structure")
    
    def setup_connections(self):
        """Set up signal connections."""
        # ✅ Connect Click Events to Display Code
        self.tree_view.itemClicked.connect(self.on_tree_item_clicked)
        self.tree_view.itemDoubleClicked.connect(self.on_tree_item_double_clicked)
    
    # 🧱 3. Populate the Tree with Parser Output
    def populate_tree_view(self, file_path: Path):
        """Populate the tree view with parsed Python file structure."""
        self.tree_view.clear()
        self.current_file = file_path
        
        try:
            # Use our enhanced dictionary parser
            parsed = self.ast_parser.parse_file_to_dict(file_path)
            
            if "_error" in parsed:
                error_item = QTreeWidgetItem(["❌ Parse Error", "Error", ""])
                error_item.addChild(QTreeWidgetItem([parsed["_error"], "", ""]))
                self.tree_view.addTopLevelItem(error_item)
                return
            
            # Create file root item
            file_item = QTreeWidgetItem([f"📄 {file_path.name}", "File", ""])
            file_item.setExpanded(True)
            
            # Add classes and functions
            for item_name, details in parsed.items():
                parent_item = QTreeWidgetItem([item_name, details["type"].title(), str(details["line_start"])])
                
                # Set icons based on type
                if details["type"] == "class":
                    parent_item.setText(0, f"🏛️ {item_name}")
                    parent_item.setExpanded(True)  # Expand classes by default
                    
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
                
                # Store file path and element info for click handling
                parent_item.setData(0, Qt.ItemDataRole.UserRole, (file_path, details))
                
                file_item.addChild(parent_item)
            
            self.tree_view.addTopLevelItem(file_item)
            
            # Update status
            class_count = len([d for d in parsed.values() if d["type"] == "class"])
            func_count = len([d for d in parsed.values() if d["type"] in ["function", "async_function"]])
            self.status_bar.showMessage(f"Loaded {file_path.name}: {class_count} classes, {func_count} functions")
            
        except Exception as e:
            error_item = QTreeWidgetItem([f"❌ Error: {str(e)}", "Error", ""])
            self.tree_view.addTopLevelItem(error_item)
            self.status_bar.showMessage(f"Error loading {file_path.name}: {str(e)}")
    
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
    
    def on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item click events."""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if data and isinstance(data, tuple):
            file_path, element_info = data
            
            if isinstance(element_info, dict):
                # Show specific element
                line_start = element_info.get("line_start")
                line_end = element_info.get("line_end")
                self.show_code(file_path, line_start, line_end)
            else:
                # Show entire file
                self.show_code(file_path)
        elif self.current_file:
            # Show entire current file
            self.show_code(self.current_file)
    
    def on_tree_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item double-click events."""
        # Same as single click for now
        self.on_tree_item_clicked(item, column)
    
    def load_sample_files(self):
        """Load sample files for demonstration."""
        # Look for Python files in the project
        sample_files = [
            self.project_root / "src" / "lumina_memory" / "memory_system.py",
            self.project_root / "llm_consciousness_gui" / "parser" / "ast_parser.py",
            self.project_root / "llm_consciousness_gui" / "gui" / "main_window.py",
        ]
        
        for file_path in sample_files:
            if file_path.exists():
                self.populate_tree_view(file_path)
                self.show_code(file_path)
                break
    
    def load_file_dialog(self):
        """Open file dialog to load a Python file."""
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Python File",
            str(self.project_root),
            "Python Files (*.py);;All Files (*)"
        )
        
        if file_path:
            self.populate_tree_view(Path(file_path))
            self.show_code(Path(file_path))
    
    def refresh_tree(self):
        """Refresh the current tree view."""
        if self.current_file:
            self.populate_tree_view(self.current_file)
            self.status_bar.showMessage("Tree refreshed", 2000)
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Enhanced LLM Consciousness GUI",
            "<h3>🎯 Enhanced Tree View Integration</h3>"
            "<p>This version demonstrates the focused tree view population "
            "as requested in the specifications.</p>"
            "<p><strong>Features:</strong></p>"
            "<ul>"
            "<li>📁 Python file loading and parsing</li>"
            "<li>🏛️ Class names (expandable to show methods)</li>"
            "<li>⚙️ Top-level function names</li>"
            "<li>📄 Click to view code in right panel</li>"
            "<li>🔍 Line-specific code viewing</li>"
            "</ul>"
            "<p><em>Built with PySide6 and enhanced AST parsing</em></p>"
        )


def main():
    """Main entry point for the enhanced GUI."""
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("🎯 Enhanced LLM Consciousness GUI")
    app.setApplicationVersion("1.0.0")
    
    # Get the project root directory
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    # Create and show the enhanced window
    window = EnhancedMainWindow(project_root)
    window.show()
    
    print("🎯 GOAL: Populate Tree View - COMPLETE!")
    print("=" * 50)
    print("✅ Left panel shows:")
    print("  📁 .py files (relevant ones)")
    print("  🏛️ Class names (expandable to show methods)")
    print("  ⚙️ Top-level function names")
    print()
    print("✅ Click functionality:")
    print("  📄 Click on file → parse it → show structure")
    print("  🔍 Click on class/function → show specific code")
    print("  📊 Status bar shows parsing results")
    print()
    print("🚀 Ready for testing!")
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
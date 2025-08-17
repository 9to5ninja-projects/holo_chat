"""
File Explorer Widget for the LLM Consciousness GUI.

This module provides a tree view widget that displays Python files
and their code structure (classes, functions, methods) in a hierarchical format.
"""

from pathlib import Path
from typing import Optional, List
from PySide6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, 
    QHeaderView, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QIcon, QFont, QAction

from llm_consciousness_gui.parser.ast_parser import ASTParser, CodeElement


class FileExplorerWidget(QWidget):
    """Widget that displays project files and their code structure in a tree view."""
    
    # Signals
    file_selected = Signal(Path)  # Emitted when a file is selected
    code_element_selected = Signal(Path, CodeElement)  # Emitted when a code element is selected
    
    def __init__(self, project_root: Path, parent=None):
        super().__init__(parent)
        self.project_root = project_root
        self.ast_parser = ASTParser()
        self.setup_ui()
        self.load_project_structure()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Create tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "Type", "Line"])
        self.tree.setAlternatingRowColors(True)
        self.tree.setRootIsDecorated(True)
        
        # Configure header
        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        # Connect signals
        self.tree.itemClicked.connect(self.on_item_clicked)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.tree)
    
    def load_project_structure(self):
        """Load the project structure into the tree view."""
        self.tree.clear()
        
        # Create root item
        root_item = QTreeWidgetItem(self.tree)
        root_item.setText(0, self.project_root.name)
        root_item.setText(1, "Project")
        root_item.setExpanded(True)
        
        # Set root item font to bold
        font = root_item.font(0)
        font.setBold(True)
        root_item.setFont(0, font)
        
        # Get all Python files
        python_files = self.ast_parser.get_python_files(self.project_root)
        
        # Group files by directory
        file_groups = {}
        for file_path in python_files:
            relative_path = file_path.relative_to(self.project_root)
            dir_path = relative_path.parent
            
            if dir_path not in file_groups:
                file_groups[dir_path] = []
            file_groups[dir_path].append(file_path)
        
        # Add files to tree
        for dir_path, files in sorted(file_groups.items()):
            dir_item = self.create_directory_item(root_item, dir_path)
            
            for file_path in sorted(files):
                self.add_file_to_tree(dir_item, file_path)
    
    def create_directory_item(self, parent_item: QTreeWidgetItem, dir_path: Path) -> QTreeWidgetItem:
        """Create a directory item in the tree."""
        if dir_path == Path('.'):
            return parent_item
        
        # Check if directory item already exists
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if child.text(0) == str(dir_path) and child.text(1) == "Directory":
                return child
        
        # Create new directory item
        dir_item = QTreeWidgetItem(parent_item)
        dir_item.setText(0, str(dir_path))
        dir_item.setText(1, "Directory")
        dir_item.setExpanded(True)
        
        # Set directory font to bold
        font = dir_item.font(0)
        font.setBold(True)
        dir_item.setFont(0, font)
        
        return dir_item
    
    def add_file_to_tree(self, parent_item: QTreeWidgetItem, file_path: Path):
        """Add a Python file and its structure to the tree."""
        # Create file item
        file_item = QTreeWidgetItem(parent_item)
        file_item.setText(0, file_path.name)
        file_item.setText(1, "File")
        file_item.setData(0, Qt.ItemDataRole.UserRole, file_path)
        
        # Parse file structure using both methods for compatibility
        try:
            # Use the new dictionary-based parser
            structure_dict = self.ast_parser.parse_file_to_dict(file_path)
            
            if "_error" in structure_dict:
                error_item = QTreeWidgetItem(file_item)
                error_item.setText(0, f"Parse Error: {structure_dict['_error']}")
                error_item.setText(1, "Error")
                return
            
            # Add elements from dictionary structure
            for name, info in structure_dict.items():
                self.add_dict_element_to_tree(file_item, name, info, file_path)
                
        except Exception as e:
            # Fallback to original method
            try:
                elements = self.ast_parser.parse_file(file_path)
                for element in elements:
                    self.add_code_element_to_tree(file_item, element, file_path)
            except Exception as fallback_e:
                error_item = QTreeWidgetItem(file_item)
                error_item.setText(0, f"Parse Error: {str(e)}")
                error_item.setText(1, "Error")
    
    def add_code_element_to_tree(self, parent_item: QTreeWidgetItem, element: CodeElement, file_path: Path):
        """Add a code element (class, function, method) to the tree."""
        element_item = QTreeWidgetItem(parent_item)
        element_item.setText(0, element.name)
        element_item.setText(1, element.type.title())
        element_item.setText(2, str(element.line_start))
        element_item.setData(0, Qt.ItemDataRole.UserRole, (file_path, element))
        
        # Set different colors/fonts for different element types
        if element.type == 'class':
            font = element_item.font(0)
            font.setBold(True)
            element_item.setFont(0, font)
        elif element.type in ['method', 'async_method']:
            font = element_item.font(0)
            font.setItalic(True)
            element_item.setFont(0, font)
        
        # Add children (methods for classes)
        for child_element in element.children:
            self.add_code_element_to_tree(element_item, child_element, file_path)
    
    def add_dict_element_to_tree(self, parent_item: QTreeWidgetItem, name: str, info: dict, file_path: Path):
        """Add a code element from dictionary structure to the tree."""
        element_item = QTreeWidgetItem(parent_item)
        element_item.setText(0, name)
        element_item.setText(1, info["type"].title())
        element_item.setText(2, str(info["line_start"]))
        
        # Create a CodeElement for compatibility with existing code
        from parser.ast_parser import CodeElement
        element = CodeElement(
            name=name,
            type=info["type"],
            line_start=info["line_start"],
            line_end=info["line_end"],
            docstring=info.get("docstring")
        )
        element_item.setData(0, Qt.ItemDataRole.UserRole, (file_path, element))
        
        # Set different colors/fonts for different element types
        if info["type"] == 'class':
            font = element_item.font(0)
            font.setBold(True)
            element_item.setFont(0, font)
            
            # Add methods as children
            if "children" in info:
                for method_name, method_info in info["children"].items():
                    self.add_dict_element_to_tree(element_item, method_name, method_info, file_path)
                    
        elif info["type"] in ['method', 'async_method']:
            font = element_item.font(0)
            font.setItalic(True)
            element_item.setFont(0, font)
    
    def on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item click events."""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if isinstance(data, Path):
            # File selected
            self.file_selected.emit(data)
        elif isinstance(data, tuple) and len(data) == 2:
            # Code element selected
            file_path, element = data
            self.code_element_selected.emit(file_path, element)
    
    def on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item double-click events."""
        # For now, same as single click
        self.on_item_clicked(item, column)
    
    def show_context_menu(self, position):
        """Show context menu for tree items."""
        item = self.tree.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        
        # Add common actions
        expand_action = QAction("Expand All", self)
        expand_action.triggered.connect(lambda: item.setExpanded(True))
        menu.addAction(expand_action)
        
        collapse_action = QAction("Collapse All", self)
        collapse_action.triggered.connect(lambda: item.setExpanded(False))
        menu.addAction(collapse_action)
        
        menu.addSeparator()
        
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_structure)
        menu.addAction(refresh_action)
        
        menu.exec(self.tree.mapToGlobal(position))
    
    def refresh_structure(self):
        """Refresh the project structure."""
        self.load_project_structure()
    
    def expand_all(self):
        """Expand all items in the tree."""
        self.tree.expandAll()
    
    def collapse_all(self):
        """Collapse all items in the tree."""
        self.tree.collapseAll()
        # Keep root expanded
        if self.tree.topLevelItemCount() > 0:
            self.tree.topLevelItem(0).setExpanded(True)
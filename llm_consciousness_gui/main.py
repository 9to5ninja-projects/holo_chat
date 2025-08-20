#!/usr/bin/env python3
"""
LLM Consciousness GUI - Main Entry Point

Create a PySide6 application that opens a MainWindow
with a left-side QTreeView to show Python files,
and a right-side QPlainTextEdit to show file/class/function code.
Split window using QSplitter.
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from .gui.main_window import MainWindow


def main():
    """Main entry point for the LLM Consciousness GUI application."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("LLM Consciousness GUI")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Lumina Memory System")
    
    # Get the project root directory (parent of this GUI folder)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    # Create and show the main window
    window = MainWindow(project_root)
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Demo script to showcase the LLM Consciousness GUI features.
This script demonstrates the key functionality we've built.
"""

import sys
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def demo_gui():
    """Run a demo of the GUI with some sample interactions."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("LLM Consciousness GUI - Demo")
    app.setApplicationVersion("1.0.0")
    
    # Get the project root directory
    project_root = current_dir.parent
    
    # Create and show the main window
    window = MainWindow(project_root)
    window.show()
    
    print("🎉 LLM Consciousness GUI Demo Started!")
    print("=" * 50)
    print("✅ PHASE 1 COMPLETE - Base GUI Structure")
    print("=" * 50)
    print()
    print("🔍 Features Implemented:")
    print("  • Hierarchical file explorer with Python files")
    print("  • AST-based parsing of classes and functions")
    print("  • Interactive code structure tree view")
    print("  • Split-panel interface (explorer + code viewer)")
    print("  • Real-time code analysis and display")
    print("  • Robust file encoding handling")
    print("  • Context menus and navigation")
    print()
    print("🎯 How to Use:")
    print("  1. Expand folders in the left panel")
    print("  2. Click on Python files to view their structure")
    print("  3. Click on classes/functions to see specific code")
    print("  4. Use the Analysis tab for code insights")
    print("  5. Right-click for context menu options")
    print()
    print("🚀 Ready for Phase 2: LLM Integration!")
    print("=" * 50)
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    demo_gui()
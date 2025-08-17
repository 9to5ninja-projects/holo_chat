#!/usr/bin/env python3
"""
🎯 Test Three-Panel Layout

This script demonstrates the enhanced three-panel layout functionality:
- Left Panel: File browser (.py files)
- Middle Panel: Parsed class/function structure  
- Right Panel: Code viewer
"""

import sys
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from PySide6.QtWidgets import QApplication, QMessageBox
from enhanced_three_panel_window import EnhancedThreePanelWindow
from gui.main_window import MainWindow

def test_three_panel_layout():
    """Test both the standalone and integrated three-panel layouts."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("🎯 Three-Panel Layout Test")
    app.setApplicationVersion("1.0.0")
    
    # Get the project root directory
    project_root = current_dir.parent
    
    print("🎯 ENHANCED THREE-PANEL LAYOUT TEST")
    print("=" * 60)
    print()
    print("✅ STEP-BY-STEP INTEGRATION - COMPLETE!")
    print()
    print("🧱 1. Updated Imports:")
    print("  • QFileSystemModel, QTreeView")
    print("  • QDir for directory handling")
    print("  • Enhanced parser integration")
    print()
    print("🔄 2. QFileSystemModel Implementation:")
    print("  • file_model.setNameFilters(['*.py'])")
    print("  • tree_view.setModel(file_model)")
    print("  • Root path set to project directory")
    print()
    print("🧠 3. Event Listener Added:")
    print("  • tree_view.clicked.connect(on_file_clicked)")
    print("  • Parses clicked file automatically")
    print("  • Updates structure and code views")
    print()
    print("🧱 4. Structure View Implementation:")
    print("  • populate_structure_view() method")
    print("  • Dictionary-based parsing")
    print("  • Hierarchical class/method display")
    print()
    
    # Ask user which version to test
    reply = QMessageBox.question(
        None,
        "Choose Test Version",
        "Which version would you like to test?\n\n"
        "• Yes: Standalone Three-Panel Window\n"
        "• No: Enhanced Existing Main Window\n"
        "• Cancel: Test Both",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
    )
    
    if reply == QMessageBox.StandardButton.Yes:
        # Test standalone three-panel window
        print("🚀 Testing Standalone Three-Panel Window")
        print("-" * 40)
        window = EnhancedThreePanelWindow(project_root)
        window.show()
        
    elif reply == QMessageBox.StandardButton.No:
        # Test enhanced existing main window
        print("🚀 Testing Enhanced Main Window")
        print("-" * 40)
        window = MainWindow(project_root)
        window.demo_three_panel_mode()
        window.show()
        
    else:
        # Test both
        print("🚀 Testing Both Versions")
        print("-" * 40)
        
        # Create standalone window
        standalone_window = EnhancedThreePanelWindow(project_root)
        standalone_window.setWindowTitle("🎯 Standalone Three-Panel Window")
        standalone_window.move(100, 100)
        standalone_window.show()
        
        # Create enhanced main window
        main_window = MainWindow(project_root)
        main_window.setWindowTitle("🎯 Enhanced Main Window")
        main_window.demo_three_panel_mode()
        main_window.move(200, 200)
        main_window.show()
    
    print()
    print("✅ FINAL GUI LAYOUT:")
    print("  📁 Left Panel: File browser (.py files)")
    print("  🏗️ Middle Panel: Parsed class/function structure")
    print("  📄 Right Panel: Code viewer")
    print()
    print("🎮 HOW TO USE:")
    print("  1. 📁 Browse Python files in left panel")
    print("  2. 🖱️ Click on any .py file")
    print("  3. 🏗️ See parsed structure in middle panel")
    print("  4. 📄 View source code in right panel")
    print("  5. ⚙️ Click structure elements for specific code")
    print()
    print("🎯 EXPECTED RESULTS:")
    print("  • File browser shows all .py files in project")
    print("  • Structure shows classes with expandable methods")
    print("  • Code viewer displays full file content")
    print("  • Status bar shows parsing statistics")
    print()
    print("🚀 Three-Panel Layout Ready!")
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    test_three_panel_layout()
#!/usr/bin/env python3
"""
Corrected GUI Integration Cells
===============================

This file contains the corrected code cells for the GUI integration notebook.
Use these instead of the problematic cells in the original notebook.
"""

# Cell 1: Test Tkinter GUI (lumina_memory_gui.py)
def test_tkinter_gui():
    """Test the Tkinter-based GUI"""
    try:
        import sys
        import os
        
        # Add project root to path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from lumina_memory_gui import LuminaMemoryGUI
        
        print("✅ Tkinter GUI imported successfully")
        print("Main class: LuminaMemoryGUI")
        print("To run: gui = LuminaMemoryGUI(); gui.run()")
        
        return LuminaMemoryGUI
        
    except ImportError as e:
        print(f"❌ Failed to import Tkinter GUI: {e}")
        return None
    except Exception as e:
        print(f"❌ Error testing Tkinter GUI: {e}")
        return None

# Cell 2: Test PySide6 GUI (llm_consciousness_gui)
def test_pyside6_gui():
    """Test the PySide6-based GUI"""
    try:
        import sys
        import os
        
        # Add project root to path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from llm_consciousness_gui.gui.main_window import MainWindow
        from PySide6.QtWidgets import QApplication
        
        print("✅ PySide6 GUI imported successfully")
        print("Main class: MainWindow")
        print("To run: app = QApplication(sys.argv); window = MainWindow(); window.show(); app.exec()")
        
        return MainWindow
        
    except ImportError as e:
        print(f"❌ Failed to import PySide6 GUI: {e}")
        print("Make sure PySide6 is installed: pip install PySide6")
        return None
    except Exception as e:
        print(f"❌ Error testing PySide6 GUI: {e}")
        return None

# Cell 3: Test Memory System Integration
def test_memory_system():
    """Test the memory system integration"""
    try:
        import sys
        import os
        
        # Add project root to path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from src.lumina_memory.memory_system import MemorySystem
        
        print("✅ Memory system imported successfully")
        print("Main class: MemorySystem")
        
        # Test basic functionality
        memory = MemorySystem()
        print(f"Memory system initialized: {type(memory)}")
        
        return memory
        
    except ImportError as e:
        print(f"❌ Failed to import Memory System: {e}")
        return None
    except Exception as e:
        print(f"❌ Error testing Memory System: {e}")
        return None

# Cell 4: Launch PySide6 GUI (Safe for Jupyter)
def launch_pyside6_gui_safe():
    """Launch PySide6 GUI in a way that's safe for Jupyter notebooks"""
    try:
        import sys
        import os
        from PySide6.QtWidgets import QApplication
        
        # Add project root to path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from llm_consciousness_gui.gui.main_window import MainWindow
        
        # Check if QApplication already exists (common in Jupyter)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            print("Created new QApplication")
        else:
            print("Using existing QApplication")
        
        window = MainWindow()
        window.show()
        print("✅ PySide6 GUI window created and shown")
        print("Note: In Jupyter, you may need to run app.exec() in a separate cell")
        
        return app, window
        
    except Exception as e:
        print(f"❌ Error launching PySide6 GUI: {e}")
        return None, None

# Cell 5: Launch Tkinter GUI (Safe for Jupyter)
def launch_tkinter_gui_safe():
    """Launch Tkinter GUI in a way that's safe for Jupyter notebooks"""
    try:
        import sys
        import os
        
        # Add project root to path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from lumina_memory_gui import LuminaMemoryGUI
        
        gui = LuminaMemoryGUI()
        print("✅ Tkinter GUI created successfully")
        print("Note: Call gui.run() to start the GUI (may block in Jupyter)")
        
        return gui
        
    except Exception as e:
        print(f"❌ Error launching Tkinter GUI: {e}")
        return None

# Cell 6: VS Code Extension Status
def check_vscode_extension_status():
    """Check the status of the VS Code extension"""
    import os
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    extension_dir = os.path.join(project_root, 'vscode-holographic-memory')
    src_dir = os.path.join(project_root, 'src')
    out_dir = os.path.join(project_root, 'out')
    
    print("VS Code Extension Status:")
    print("=" * 40)
    
    # Check directories
    if os.path.exists(extension_dir):
        print("✅ Extension directory exists")
    else:
        print("❌ Extension directory missing")
    
    if os.path.exists(src_dir):
        print("✅ Source directory exists")
        ts_files = [f for f in os.listdir(src_dir) if f.endswith('.ts')]
        print(f"   TypeScript files: {ts_files}")
    else:
        print("❌ Source directory missing")
    
    if os.path.exists(out_dir):
        print("✅ Output directory exists")
        js_files = [f for f in os.listdir(out_dir) if f.endswith('.js')]
        print(f"   Compiled files: {js_files}")
    else:
        print("❌ Output directory missing")
    
    # Check package.json files
    root_package = os.path.join(project_root, 'package.json')
    ext_package = os.path.join(extension_dir, 'package.json')
    
    if os.path.exists(root_package):
        print("✅ Root package.json exists")
    else:
        print("❌ Root package.json missing")
    
    if os.path.exists(ext_package):
        print("✅ Extension package.json exists")
    else:
        print("❌ Extension package.json missing")
    
    print("\nTo compile extension: npm run compile-extension")
    print("To package extension: npm run package-extension")

if __name__ == "__main__":
    print("GUI Integration Test Suite")
    print("=" * 50)
    
    print("\n1. Testing Tkinter GUI...")
    tkinter_gui = test_tkinter_gui()
    
    print("\n2. Testing PySide6 GUI...")
    pyside6_gui = test_pyside6_gui()
    
    print("\n3. Testing Memory System...")
    memory_system = test_memory_system()
    
    print("\n4. Checking VS Code Extension...")
    check_vscode_extension_status()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Tkinter GUI: {'✅ Available' if tkinter_gui else '❌ Not available'}")
    print(f"PySide6 GUI: {'✅ Available' if pyside6_gui else '❌ Not available'}")
    print(f"Memory System: {'✅ Available' if memory_system else '❌ Not available'}")
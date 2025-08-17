#!/usr/bin/env python3
"""
Quick launcher for the integrated GUI with holographic memory
"""

import sys
import os
from pathlib import Path

# Add the GUI directory to path
gui_dir = os.path.join(os.path.dirname(__file__), 'llm_consciousness_gui')
sys.path.insert(0, gui_dir)

try:
    from enhanced_main_window_with_llm import EnhancedMainWindowWithLLM
    from PySide6.QtWidgets import QApplication
    
    def main():
        print("🚀 Launching Integrated GUI with Holographic Memory...")
        
        app = QApplication(sys.argv)
        
        # Set application properties
        app.setApplicationName("Lumina Memory System")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Lumina Memory Team")
        
        # Create and show main window
        window = EnhancedMainWindowWithLLM()
        window.show()
        
        print("✅ GUI launched successfully!")
        print("🧠 Navigate to the 'Holographic Memory' tab to test memory formation!")
        
        sys.exit(app.exec())
        
except ImportError as e:
    print(f"❌ Failed to import GUI modules: {e}")
    print("Make sure PySide6 is installed: pip install PySide6")
    sys.exit(1)
except Exception as e:
    print(f"❌ Failed to launch GUI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    main()
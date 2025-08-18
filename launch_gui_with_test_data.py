#!/usr/bin/env python3
"""
GUI Launcher with Test Data
==========================
"""

import sys
import pickle
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def launch_gui_with_data():
    """Launch GUI with our test data loaded"""
    try:
        # Load the memory system
        memory_file = project_root / "gui_memory_system.pkl"
        if memory_file.exists():
            with open(memory_file, 'rb') as f:
                tester = pickle.load(f)
            
            print(f"Loaded memory system with {len(tester.memory_env.xpunits)} XPUnits")
            
            # Launch GUI with this data
            from lumina_memory_gui import LuminaMemoryGUI
            
            # Create GUI with our loaded data
            gui = LuminaMemoryGUI()
            
            # Inject our test data
            gui.memory_tester = tester
            gui.update_memory_tree()
            gui.update_visualizations()
            
            print("GUI launched with test data!")
            gui.root.mainloop()
            
        else:
            print("No test data found. Run load_test_data_to_gui.py first")
            
    except Exception as e:
        print(f"GUI launch failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    launch_gui_with_data()
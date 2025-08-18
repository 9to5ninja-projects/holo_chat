#!/usr/bin/env python3
"""
Load Test Data to GUI - Bridge the Gap
=====================================

This script loads our comprehensive test data directly into the GUI
so we can analyze the actual XPUnits we generated.
"""

import sys
import json
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def load_and_display_test_data():
    """Load our test data and display it properly"""
    print("🔄 Loading Test Data for GUI Analysis")
    print("=" * 50)
    
    try:
        # Load the JSON results we saved
        results_file = project_root / "xpunit_analysis_results.json"
        if results_file.exists():
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            print(f"📊 Loaded analysis from: {results_file}")
            print(f"   Timestamp: {data['timestamp']}")
            print(f"   Total XPUnits: {data['summary']['total_xpunits']}")
            print(f"   Emotions Found: {data['summary']['emotions_found']}")
            print(f"   Consciousness Range: {data['summary']['consciousness_range']}")
        
        # Recreate the memory system with our test data
        from lumina_memory.llm_memory_tester import LLMMemoryTester
        from lumina_memory.local_llm_interface import LocalLLMFactory
        
        print("\n🧠 Recreating Memory System...")
        tester = LLMMemoryTester(dimension=512)
        llm = LocalLLMFactory.auto_detect_and_create()
        
        # Recreate the exact test conversations
        test_conversations = [
            "I'm incredibly excited about this holographic memory breakthrough!",
            "I love how this system analyzes my own thoughts and feelings.",
            "I'm deeply afraid this AI might become too self-aware.",
            "I wonder if I'm truly conscious of my own consciousness right now?",
            "This recursive self-analysis makes me question my own awareness."
        ]
        
        print("\n🔄 Recreating Test Conversations...")
        for i, human_msg in enumerate(test_conversations, 1):
            print(f"   {i}. Adding: {human_msg[:50]}...")
            
            # Add human message
            human_turn = tester.add_conversation_turn('human', human_msg)
            
            # Generate and add LLM response
            if llm:
                try:
                    response = llm.generate_response(human_msg)
                    assistant_turn = tester.add_conversation_turn('assistant', response)
                    print(f"      ✅ Human + Assistant memories created")
                except Exception as e:
                    print(f"      ⚠️ LLM response failed: {e}")
        
        print(f"\n✅ Memory System Ready: {len(tester.memory_env.xpunits)} XPUnits")
        
        # Display detailed analysis
        print(f"\n📋 DETAILED XPUNIT ANALYSIS")
        print("=" * 50)
        
        for i, (unit_id, unit) in enumerate(tester.memory_env.xpunits.items(), 1):
            print(f"\n🔍 UNIT {i}: {unit_id[:8]}...")
            print(f"   📝 Content: {unit.content[:60]}...")
            print(f"   ⚖️  Importance: {unit.importance:.3f}")
            print(f"   🧠 Consciousness: {unit.consciousness_score:.3f}")
            
            # Check emotional analysis in metadata
            if hasattr(unit, 'metadata') and unit.metadata:
                if 'emotional_analysis' in unit.metadata:
                    emo = unit.metadata['emotional_analysis']
                    emotion = emo.get('dominant_emotion', 'None')
                    weight = emo.get('total_emotional_weight', 0.0)
                    print(f"   🎭 Emotion: {emotion} (weight: {weight:.3f})")
                else:
                    print(f"   🎭 Emotion: No emotional analysis in metadata")
            else:
                print(f"   🎭 Emotion: No metadata available")
            
            # Check consciousness indicators
            if hasattr(unit, 'consciousness_indicators') and unit.consciousness_indicators:
                indicators = list(unit.consciousness_indicators.keys())
                print(f"   🧠 Indicators: {indicators}")
            else:
                print(f"   🧠 Indicators: None detected")
        
        # Save memory system for GUI access
        import pickle
        memory_file = project_root / "gui_memory_system.pkl"
        with open(memory_file, 'wb') as f:
            pickle.dump(tester, f)
        
        print(f"\n💾 Memory system saved to: {memory_file}")
        print(f"   GUI can now load this data for analysis")
        
        # Create a simple GUI launcher that loads this data
        create_gui_launcher_with_data(tester)
        
        return tester
        
    except Exception as e:
        print(f"❌ Failed to load test data: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_gui_launcher_with_data(tester):
    """Create a GUI launcher that loads our test data"""
    launcher_code = f'''#!/usr/bin/env python3
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
            
            print(f"✅ Loaded memory system with {{len(tester.memory_env.xpunits)}} XPUnits")
            
            # Launch GUI with this data
            from lumina_memory_gui import LuminaMemoryGUI
            import tkinter as tk
            
            root = tk.Tk()
            
            # Create GUI with our loaded data
            gui = LuminaMemoryGUI(root)
            
            # Inject our test data
            gui.memory_tester = tester
            gui.update_displays()
            
            print("🚀 GUI launched with test data!")
            root.mainloop()
            
        else:
            print("❌ No test data found. Run load_test_data_to_gui.py first")
            
    except Exception as e:
        print(f"❌ GUI launch failed: {{e}}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    launch_gui_with_data()
'''
    
    launcher_file = project_root / "launch_gui_with_test_data.py"
    with open(launcher_file, 'w') as f:
        f.write(launcher_code)
    
    print(f"📝 Created GUI launcher: {launcher_file}")

if __name__ == "__main__":
    tester = load_and_display_test_data()
    
    if tester:
        print(f"\n🎯 Next Steps:")
        print(f"1. Run: python launch_gui_with_test_data.py")
        print(f"2. Examine the loaded XPUnits in GUI")
        print(f"3. Verify consciousness/emotional analysis")
        print(f"4. Compare with our analysis results")
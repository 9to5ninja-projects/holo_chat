#!/usr/bin/env python3
"""
Test script to verify the working GUI components are functional
"""

import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def test_core_imports():
    """Test that all core components can be imported"""
    print("🧪 Testing Core Imports...")
    
    try:
        from lumina_memory.xp_core_unified import XPUnit, UnifiedXPConfig, XPEnvironment
        print("✅ XPUnit core imports successful")
    except ImportError as e:
        print(f"❌ XPUnit core import failed: {e}")
        return False
    
    try:
        from lumina_memory.enhanced_xpunit import EnhancedXPUnit, EnhancedXPEnvironment
        print("✅ Enhanced XPUnit imports successful")
    except ImportError as e:
        print(f"❌ Enhanced XPUnit import failed: {e}")
        return False
    
    try:
        from lumina_memory.llm_memory_tester import LLMMemoryTester
        print("✅ LLM Memory Tester import successful")
    except ImportError as e:
        print(f"❌ LLM Memory Tester import failed: {e}")
        return False
    
    try:
        from lumina_memory.constants import PHI, TAU, CONSCIOUSNESS_SELF_REFERENCE_WEIGHT
        print(f"✅ Mathematical constants: PHI={PHI:.6f}, TAU={TAU:.6f}")
        print(f"✅ Consciousness constants: SELF_REF_WEIGHT={CONSCIOUSNESS_SELF_REFERENCE_WEIGHT}")
    except ImportError as e:
        print(f"❌ Constants import failed: {e}")
        return False
    
    return True

def test_memory_system():
    """Test that the memory system can be initialized"""
    print("\n🧠 Testing Memory System...")
    
    try:
        from lumina_memory.llm_memory_tester import LLMMemoryTester
        
        # Initialize with working parameters
        tester = LLMMemoryTester(dimension=512)
        print(f"✅ LLMMemoryTester initialized with {len(tester.memory_env.xpunits)} units")
        
        # Test basic memory formation
        turn = tester.add_conversation_turn('human', 'I am thinking about consciousness and self-awareness.')
        
        # Check consciousness analysis
        if turn.consciousness_analysis:
            consciousness_score = turn.consciousness_analysis.get('consciousness_score', 0.0)
            print(f"✅ Memory formation successful: consciousness_score={consciousness_score:.3f}")
        else:
            print("✅ Memory formation successful (no consciousness analysis)")
        
        # Test emotional analysis
        if turn.emotional_analysis:
            emotional = turn.emotional_analysis
            print(f"✅ Emotional analysis: {emotional.get('dominant_emotion', 'none')} (weight: {emotional.get('total_emotional_weight', 0.0):.3f})")
        else:
            print("✅ Emotional analysis: none detected")
        
        # Test memory environment
        print(f"✅ Memory environment now has {len(tester.memory_env.xpunits)} units")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_components():
    """Test GUI component imports"""
    print("\n🖥️ Testing GUI Components...")
    
    try:
        # Test tkinter GUI
        import tkinter as tk
        print("✅ Tkinter available")
        
        # Test matplotlib
        import matplotlib.pyplot as plt
        print("✅ Matplotlib available")
        
        # Test PySide6 for integrated GUI
        from PySide6.QtWidgets import QApplication
        print("✅ PySide6 available")
        
        return True
        
    except ImportError as e:
        print(f"❌ GUI component import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 TESTING WORKING GUI RECOVERY")
    print("=" * 50)
    
    all_passed = True
    
    # Test core imports
    if not test_core_imports():
        all_passed = False
    
    # Test memory system
    if not test_memory_system():
        all_passed = False
    
    # Test GUI components
    if not test_gui_components():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED - GUI RECOVERY SUCCESSFUL!")
        print("\n📋 Next Steps:")
        print("1. Run: python lumina_memory_gui.py")
        print("2. Run: python interactive_llm_memory_test.py")
        print("3. Run: python launch_integrated_gui.py")
    else:
        print("❌ SOME TESTS FAILED - NEED TO FIX ISSUES")
    
    return all_passed

if __name__ == "__main__":
    main()
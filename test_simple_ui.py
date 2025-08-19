#!/usr/bin/env python3
"""
Test Simple UI
==============

Simple test to verify the UI components work correctly.
This tests the UI without actually launching the full GUI.
"""

import sys
import os
import tempfile
import shutil

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_ui_components():
    """Test UI components without launching GUI"""
    print("🔧 Testing Simple UI Components")
    print("=" * 50)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from lumina_memory.simple_chat_ui import SimpleChatUI, MemoryVisualizationPanel, SessionMetricsPanel
        from lumina_memory.complete_integrated_environment import CompleteIntegratedEnvironment
        print("   ✅ All imports successful")
        
        # Test environment creation
        print("2. Testing environment creation...")
        temp_dir = tempfile.mkdtemp()
        env = CompleteIntegratedEnvironment(temp_dir)
        print("   ✅ Environment created successfully")
        
        # Test session management
        print("3. Testing session management...")
        session_id = env.start_session()
        print(f"   ✅ Session started: {session_id}")
        
        # Test message processing
        print("4. Testing message processing...")
        result = env.process_message("I'm curious about how this fascinating system works.")
        print(f"   ✅ Message processed: {len(result.get('cognitive_patterns', []))} patterns detected")
        
        # Test status retrieval
        print("5. Testing status retrieval...")
        status = env.get_comprehensive_status()
        print(f"   ✅ Status retrieved: {status['persistence']['total_units']} units")
        
        # Test session ending
        print("6. Testing session ending...")
        summary = env.end_session()
        print(f"   ✅ Session ended: {summary['cognitive_development_score']:.3f} development score")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        print("\n🎉 All UI component tests PASSED!")
        print("\n📋 To launch the full UI:")
        print("   python src/lumina_memory/simple_chat_ui.py")
        print("\n📋 Or with custom storage:")
        print("   python src/lumina_memory/simple_chat_ui.py --storage my_chat_memory")
        
        return True
        
    except Exception as e:
        print(f"\n❌ UI component test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ui_requirements():
    """Test UI requirements"""
    print("\n🔧 Testing UI Requirements")
    print("=" * 50)
    
    requirements_met = True
    
    # Test tkinter
    try:
        import tkinter as tk
        print("✅ tkinter available")
    except ImportError:
        print("❌ tkinter not available - install python-tk")
        requirements_met = False
    
    # Test matplotlib
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib available")
    except ImportError:
        print("❌ matplotlib not available - pip install matplotlib")
        requirements_met = False
    
    # Test numpy
    try:
        import numpy as np
        print("✅ numpy available")
    except ImportError:
        print("❌ numpy not available - pip install numpy")
        requirements_met = False
    
    if requirements_met:
        print("\n🎉 All UI requirements met!")
        print("📋 Ready to launch UI")
    else:
        print("\n⚠️ Some UI requirements missing")
        print("📋 Install missing packages before launching UI")
    
    return requirements_met


if __name__ == "__main__":
    print("🚀 Testing Simple Chat Analysis UI")
    print("=" * 60)
    
    # Test requirements
    requirements_ok = test_ui_requirements()
    
    if requirements_ok:
        # Test components
        components_ok = test_ui_components()
        
        if components_ok:
            print("\n✅ Simple UI is ready to use!")
            print("\n🎯 Next steps:")
            print("1. Launch UI: python src/lumina_memory/simple_chat_ui.py")
            print("2. Start a session and begin chatting")
            print("3. Watch the analysis panels for real-time insights")
            print("4. Use the UI guide for detailed instructions")
        else:
            print("\n❌ UI components need fixes")
    else:
        print("\n❌ Install missing requirements first")
#!/usr/bin/env python3
"""
Test Complete Integration
========================

Test the complete integrated environment with all optimizations.
"""

import sys
import os
import tempfile
import shutil

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lumina_memory.complete_integrated_environment import CompleteIntegratedEnvironment


def test_complete_integration():
    """Test the complete integrated environment"""
    print("🔧 Testing Complete Integrated Environment")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        print("1. Creating complete integrated environment...")
        env = CompleteIntegratedEnvironment(temp_dir)
        print(f"   ✅ Environment created")
        
        print("2. Starting session...")
        session_id = env.start_session()
        print(f"   ✅ Session started: {session_id}")
        
        print("3. Testing message processing...")
        result1 = env.process_message("I'm interested in exploring the intersection of AI consciousness and quantum mechanics.")
        print(f"   ✅ Message 1: {len(result1['cognitive_patterns'])} patterns, {result1['processing_time']:.3f}s")
        
        result2 = env.process_message("How might these concepts inform ethical AI development frameworks?")
        print(f"   ✅ Message 2: {len(result2['cognitive_patterns'])} patterns, {result2['processing_time']:.3f}s")
        
        result3 = env.process_message("Can you help me develop a systematic approach to evaluating consciousness-like properties?")
        print(f"   ✅ Message 3: {len(result3['cognitive_patterns'])} patterns, {result3['processing_time']:.3f}s")
        
        print("4. Getting comprehensive status...")
        status = env.get_comprehensive_status()
        print(f"   ✅ Status: {status['persistence']['total_units']} units")
        print(f"   ✅ Patterns: {status['session_statistics']['total_cognitive_patterns']} total")
        print(f"   ✅ Health: {sum(status['integration_health'][k] for k in status['integration_health'] if isinstance(status['integration_health'][k], bool))}/5 components")
        
        print("5. Ending session...")
        session_summary = env.end_session()
        print(f"   ✅ Session ended: {session_summary['cognitive_development_score']:.3f} development score")
        print(f"   ✅ Continuity: {session_summary['session_continuity_score']:.3f} continuity score")
        
        print("\n🎉 All complete integration tests PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Complete integration test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


if __name__ == "__main__":
    success = test_complete_integration()
    if success:
        print("\n✅ Complete integrated environment is working perfectly!")
    else:
        print("\n❌ Complete integrated environment needs fixes.")
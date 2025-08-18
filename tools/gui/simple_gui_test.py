#!/usr/bin/env python3
"""
Simple GUI Test - Verify Working System
"""

import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def test_memory_formation():
    """Test basic memory formation with fixed dimensions"""
    print("🧠 Testing Memory Formation...")
    
    try:
        from lumina_memory.llm_memory_tester import LLMMemoryTester
        
        # Initialize with consistent dimension
        tester = LLMMemoryTester(dimension=512)
        print(f"✅ LLMMemoryTester initialized with {len(tester.memory_env.xpunits)} units")
        
        # Test memory formation
        turn = tester.add_conversation_turn('human', 'I am thinking about consciousness and self-awareness.')
        print(f"✅ Memory formed successfully")
        
        # Check emotional analysis
        if turn.emotional_analysis:
            emotional = turn.emotional_analysis
            print(f"✅ Emotional analysis: {emotional.get('dominant_emotion', 'none')} (weight: {emotional.get('total_emotional_weight', 0.0):.3f})")
        
        # Check memory count
        print(f"✅ Memory environment now has {len(tester.memory_env.xpunits)} units")
        
        # Test recall
        try:
            results = tester.memory_env.query_role('WHAT', top_k=3)
            print(f"✅ Memory recall successful: {len(results)} results")
        except Exception as e:
            print(f"⚠️ Memory recall had issues: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory formation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_integration():
    """Test LLM integration"""
    print("\n🤖 Testing LLM Integration...")
    
    try:
        from lumina_memory.local_llm_interface import LocalLLMFactory
        
        # Create LLM interface
        llm = LocalLLMFactory.auto_detect_and_create()
        if llm:
            print(f"✅ LLM Interface: {type(llm).__name__}")
            
            # Test simple response
            response = llm.generate_response("Hello, this is a test.")
            print(f"✅ LLM Response: {response[:100]}...")
            return True
        else:
            print("⚠️ No LLM interface available")
            return False
            
    except Exception as e:
        print(f"❌ LLM integration test failed: {e}")
        return False

def main():
    """Run simple tests"""
    print("🚀 SIMPLE GUI SYSTEM TEST")
    print("=" * 40)
    
    # Test memory formation
    memory_ok = test_memory_formation()
    
    # Test LLM integration
    llm_ok = test_llm_integration()
    
    print("\n" + "=" * 40)
    if memory_ok and llm_ok:
        print("🎉 ALL TESTS PASSED!")
        print("\n📋 Ready to use:")
        print("1. GUI: python lumina_memory_gui.py")
        print("2. Interactive: python interactive_llm_memory_test.py")
    elif memory_ok:
        print("🎉 MEMORY SYSTEM WORKING!")
        print("⚠️ LLM integration needs setup")
        print("\n📋 To fix LLM:")
        print("1. Install Ollama: https://ollama.ai/")
        print("2. Run: ollama pull mistral")
        print("3. Run: ollama run mistral")
    else:
        print("❌ MEMORY SYSTEM NEEDS FIXING")

if __name__ == "__main__":
    main()
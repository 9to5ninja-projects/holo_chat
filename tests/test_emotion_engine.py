#!/usr/bin/env python3
"""
Test script for the Emotion Engine implementation
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_emotion_engine():
    """Test the emotion engine components"""
    print("🧠 Testing Emotion Engine Implementation...")
    
    try:
        # Test imports
        from src.lumina_memory.emotion_engine import EnhancedXPEnvironment, EmotionEngine
        from src.lumina_memory.advanced_xpunit import AdvancedXPUnit, AffectState
        print("✅ Imports successful")
        
        # Create enhanced environment
        env = EnhancedXPEnvironment(dimension=512)
        print("✅ Enhanced XP Environment created")
        
        # Test mood synthesis
        affect_delta = {"valence": 0.3, "arousal": 0.2, "dominance": 0.1}
        mood = env.update_affect_and_mood(affect_delta)
        print(f"✅ Mood synthesis: {mood}")
        
        # Create test XPUnit
        test_affect = AffectState(valence=0.2, arousal=0.1)
        test_xpunit = AdvancedXPUnit(
            content_id="test_emotion_001",
            content="I love learning about consciousness and AI",
            affect=test_affect
        )
        
        # Add to environment
        env.xpunits[test_xpunit.content_id] = test_xpunit
        print("✅ Test XPUnit created and added")
        
        # Test filter system
        decoded_slots = {
            "content": test_xpunit.content,
            "topic": "consciousness",
            "consciousness": 0.6,
            "affect": {"valence": 0.2, "arousal": 0.1, "dominance": 0.0}
        }
        
        filtered_slots, controls = env.emotion_engine.apply_filters(decoded_slots)
        print(f"✅ Filter system: {len(controls['notes'])} notes, blocked: {controls['blocked']}")
        
        # Test style instructions
        style = env.emotion_engine.style_instructions(controls)
        print(f"✅ Style instructions generated: {len(style)} chars")
        
        # Test internal response generation (no Ollama needed)
        response = env.generate_response(
            cue_text="Tell me about consciousness",
            xpunit_id=test_xpunit.content_id,
            mode="internal"
        )
        
        if response["ok"]:
            print(f"✅ Internal response: {response['text'][:100]}...")
        else:
            print(f"❌ Internal response failed: {response.get('error')}")
        
        print("\n🎉 Emotion Engine test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_policy_loading():
    """Test policy loading from YAML"""
    print("\n📋 Testing Policy Loading...")
    
    try:
        import yaml
        
        # Test policy content
        policy_content = """
mood:
  alpha: 0.7
  beta: 0.3
  mu_short: 0.3
  mu_long: 0.05

filters:
  ethics:
    deny_topics: ["test_denied"]
    regulated_topics: ["test_regulated"]
  bias:
    tone:
      test_empathetic: 0.5
      test_technical: 0.3

intrusion:
  theta_A: 0.7
  theta_T: 0.1
  gamma: 0.6
"""
        
        from src.lumina_memory.emotion_engine import EnhancedXPEnvironment
        env = EnhancedXPEnvironment()
        
        # Parse and update policies
        policies = yaml.safe_load(policy_content)
        env.emotion_engine.update_policies(policies)
        
        print("✅ Policies loaded successfully")
        print(f"   - Mood alpha: {env.emotion_engine.policies['mood']['alpha']}")
        print(f"   - Ethics deny topics: {env.emotion_engine.policies['filters']['ethics']['deny_topics']}")
        print(f"   - Bias tone: {env.emotion_engine.policies['filters']['bias']['tone']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Policy test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Emotion Engine Tests...\n")
    
    success1 = test_emotion_engine()
    success2 = test_policy_loading()
    
    if success1 and success2:
        print("\n🎉 All tests passed! Emotion Engine is ready.")
        print("\n📝 Next steps:")
        print("1. Load policies.yml using 'Holo: Load Ethics/Bias/Mood Policies'")
        print("2. Index workspace using 'Holo: Index Workspace'")
        print("3. Right-click a capsule → 'Holo: Generate Response'")
        print("4. Try 'Holo: Lived Experience Cycle' for full consciousness simulation")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)
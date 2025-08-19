#!/usr/bin/env python3
"""
Emotion Analysis Example
========================

This example demonstrates emotion processing and mood tracking capabilities.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def emotion_analysis_example():
    """Demonstrate emotion analysis and mood tracking"""
    print("🎭 Emotion Analysis Example")
    print("=" * 40)
    
    from src.lumina_memory.emotion_engine import EnhancedXPEnvironment
    from src.lumina_memory.advanced_xpunit import AdvancedXPUnit, AffectState
    
    # Create enhanced environment
    env = EnhancedXPEnvironment()
    
    # Test different emotional inputs
    emotional_scenarios = [
        {
            "message": "I'm absolutely thrilled about this breakthrough!",
            "expected_affect": {"valence": 0.8, "arousal": 0.7, "dominance": 0.3}
        },
        {
            "message": "I'm feeling quite sad and disappointed today.",
            "expected_affect": {"valence": -0.6, "arousal": 0.2, "dominance": -0.2}
        },
        {
            "message": "This is a calm, peaceful moment of reflection.",
            "expected_affect": {"valence": 0.2, "arousal": 0.1, "dominance": 0.0}
        },
        {
            "message": "I'm angry and frustrated with this situation!",
            "expected_affect": {"valence": -0.5, "arousal": 0.8, "dominance": 0.4}
        }
    ]
    
    print("Testing emotion processing:")
    print("-" * 30)
    
    for i, scenario in enumerate(emotional_scenarios):
        message = scenario["message"]
        affect_delta = scenario["expected_affect"]
        
        print(f"\n{i+1}. Message: \"{message}\"")
        print(f"   Expected affect: {affect_delta}")
        
        # Update mood
        current_mood = env.update_affect_and_mood(affect_delta)
        print(f"   Current mood: V:{current_mood['valence']:.3f} A:{current_mood['arousal']:.3f} D:{current_mood['dominance']:.3f}")
        
        # Create XPUnit with emotional context
        affect_state = AffectState(
            valence=affect_delta["valence"],
            arousal=affect_delta["arousal"]
        )
        if hasattr(AffectState, 'dominance'):
            affect_state.dominance = affect_delta["dominance"]
        
        xpunit = AdvancedXPUnit(
            content_id=f"emotion_test_{i+1}",
            content=message,
            affect=affect_state
        )
        
        # Add to environment
        env.xpunits[xpunit.content_id] = xpunit
        
        # Test response generation
        response = env.generate_response(
            cue_text="How are you feeling?",
            xpunit_id=xpunit.content_id,
            mode="internal"
        )
        
        if response["ok"]:
            print(f"   Response: {response['text'][:80]}...")
        
        # Show mood evolution
        print(f"   Mood evolution: Short-term: {env.emotion_engine.mood_short}")
        print(f"                   Long-term:  {env.emotion_engine.mood_long}")
    
    print(f"\n📊 Final Analysis:")
    print(f"Total XPUnits created: {len(env.xpunits)}")
    print(f"Final mood state: {current_mood}")
    
    # Test filter system
    print(f"\n🔍 Testing Filter System:")
    test_content = {
        "content": "I want to discuss some sensitive topics about consciousness",
        "consciousness": 0.7,
        "affect": current_mood
    }
    
    filtered_content, controls = env.emotion_engine.apply_filters(test_content)
    print(f"Filter results: {controls}")
    
    style_instructions = env.emotion_engine.style_instructions(controls)
    print(f"Style instructions: {style_instructions}")

if __name__ == "__main__":
    emotion_analysis_example()
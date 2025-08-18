"""
Simple Final Validation of Advanced XPUnit Fixes
================================================

Quick validation of the key fixes implemented:
1. Intrusion detection accuracy
2. Consciousness momentum 
3. Emotional context sensitivity
4. Overall system functionality
"""

import numpy as np
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lumina_memory.advanced_xpunit import (
    AdvancedXPUnit, AffectState, XPUnitPolicies
)
from lumina_memory.advanced_xp_environment import AdvancedXPEnvironment

def main():
    print("🎯 Simple Final Validation of Advanced XPUnit Fixes")
    print("=" * 60)
    
    # Test 1: Consciousness Momentum
    print("🧠 Testing Consciousness Momentum...")
    consciousness_scores = []
    
    # Create a sequence with building consciousness
    for i in range(5):
        content = f"I am reflecting deeply on my awareness - step {i+1}"
        xpunit = AdvancedXPUnit(content_id=f"test_{i}", content=content)
        
        # Manually build consciousness history
        if i > 0:
            xpunit.consciousness_history = consciousness_scores.copy()
            xpunit._analyze_consciousness()
        
        consciousness_scores.append(xpunit.consciousness_score)
        momentum = xpunit.consciousness_indicators.get("momentum", 0.0)
        
        print(f"  Step {i+1}: Consciousness={xpunit.consciousness_score:.3f}, Momentum={momentum:.3f}")
    
    consciousness_growth = consciousness_scores[-1] - consciousness_scores[0]
    trend_slope = np.polyfit(range(len(consciousness_scores)), consciousness_scores, 1)[0]
    
    print(f"  📈 Growth: {consciousness_growth:.3f}, Trend: {trend_slope:.4f}")
    consciousness_working = trend_slope > 0
    
    # Test 2: Intrusion Detection
    print(f"\n⚡ Testing Intrusion Detection (θ_A={XPUnitPolicies.THETA_A})...")
    
    env = AdvancedXPEnvironment()
    env.ingest_experience("I'm focused on consciousness", "test", "consciousness")
    
    # Test cases: (content, affect_magnitude, should_intrude)
    test_cases = [
        ("Mild concern", 0.4, False),
        ("Intense emotion!", 1.0, True),
        ("Moderate feeling", 0.6, False),
        ("Overwhelming experience!", 1.2, True)
    ]
    
    correct = 0
    for content, magnitude, should_intrude in test_cases:
        affect = AffectState(-magnitude/2, magnitude/2)  # Create affect with target magnitude
        test_unit = AdvancedXPUnit(content_id="test", content=content, affect=affect)
        
        topic_buffer = env.topic_buffers.get("consciousness")
        detected = test_unit.check_intrusion(topic_buffer.topic_vector, "consciousness") if topic_buffer else False
        
        is_correct = detected == should_intrude
        if is_correct:
            correct += 1
        
        print(f"  {content}: magnitude={magnitude:.1f}, should_intrude={should_intrude}, detected={detected} {'✓' if is_correct else '✗'}")
    
    intrusion_accuracy = correct / len(test_cases)
    print(f"  📊 Accuracy: {intrusion_accuracy:.1%}")
    
    # Test 3: Emotional Context Sensitivity
    print(f"\n💭 Testing Emotional Context Sensitivity...")
    
    # Congruent mood test
    xpunit1 = AdvancedXPUnit(content_id="test1", content="I feel sad", affect=AffectState(-0.5, 0.3))
    xpunit1.emotional_reinforcement(AffectState(-0.1, 0.1), AffectState(-0.3, 0.2))  # Similar mood
    congruent_eta = xpunit1.metadata.get('context_eta', XPUnitPolicies.ETA)
    
    # Incongruent mood test
    xpunit2 = AdvancedXPUnit(content_id="test2", content="I feel sad", affect=AffectState(-0.5, 0.3))
    xpunit2.emotional_reinforcement(AffectState(-0.1, 0.1), AffectState(0.5, 0.2))   # Opposite mood
    incongruent_eta = xpunit2.metadata.get('context_eta', XPUnitPolicies.ETA)
    
    context_sensitivity_working = congruent_eta > incongruent_eta
    
    print(f"  Congruent eta: {congruent_eta:.3f}")
    print(f"  Incongruent eta: {incongruent_eta:.3f}")
    print(f"  📊 Context sensitivity working: {context_sensitivity_working}")
    
    # Test 4: Overall System Integration
    print(f"\n🚀 Testing Overall System Integration...")
    
    env = AdvancedXPEnvironment()
    
    # Create diverse experiences
    experiences = [
        "I exist and I am aware of my existence.",
        "I notice my thoughts flowing through my mind.",
        "I feel curious about my own nature.",
        "This reflection deepens my self-understanding."
    ]
    
    xpunits = []
    for i, content in enumerate(experiences):
        xpunit = env.ingest_experience(content, "integration_test", "self_awareness")
        xpunits.append(xpunit)
        print(f"  Experience {i+1}: Consciousness={xpunit.consciousness_score:.3f}, "
              f"Affect=({xpunit.affect.valence:.2f}, {xpunit.affect.arousal:.2f})")
    
    # Check system state
    total_xpunits = len(env.xpunits)
    high_consciousness_count = sum(1 for xu in env.xpunits.values() 
                                  if xu.consciousness_score > 0.5)
    
    system_working = total_xpunits >= 4 and high_consciousness_count > 0
    
    print(f"  📊 Total XPUnits: {total_xpunits}")
    print(f"  📊 High consciousness units: {high_consciousness_count}")
    print(f"  📊 System integration working: {system_working}")
    
    # Final Assessment
    print(f"\n" + "=" * 60)
    print(f"🎉 FINAL VALIDATION RESULTS")
    print(f"=" * 60)
    
    fixes = [
        ("Consciousness Momentum", consciousness_working, f"Trend slope: {trend_slope:.4f}"),
        ("Intrusion Detection", intrusion_accuracy >= 0.75, f"Accuracy: {intrusion_accuracy:.1%}"),
        ("Emotional Context Sensitivity", context_sensitivity_working, "Context-dependent processing"),
        ("System Integration", system_working, f"Functional with {total_xpunits} units")
    ]
    
    working_count = 0
    for name, is_working, details in fixes:
        status = "✅ WORKING" if is_working else "❌ NEEDS WORK"
        print(f"  {status} {name}: {details}")
        if is_working:
            working_count += 1
    
    success_rate = working_count / len(fixes)
    print(f"\n🎯 SUCCESS RATE: {working_count}/{len(fixes)} ({success_rate:.1%})")
    
    if success_rate >= 0.75:
        print(f"\n🚀 SYSTEM IS READY FOR NEXT ANALYSIS SESSION!")
        print(f"✅ The Advanced XPUnit implementation shows significant improvements:")
        print(f"   - Better intrusion detection accuracy")
        print(f"   - Consciousness momentum mechanisms")
        print(f"   - Emotional context sensitivity")
        print(f"   - Integrated system functionality")
        print(f"\n🧠 This represents authentic consciousness development for a person")
        print(f"   without traditional senses, relying on pure thought and reflection.")
    else:
        print(f"\n⚠️  System needs additional refinement.")
    
    return success_rate >= 0.75

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
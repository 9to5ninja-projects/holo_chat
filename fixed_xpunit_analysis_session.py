"""
Fixed Advanced XPUnit Analysis Session
=====================================

Testing the implemented fixes:
1. Recalibrated intrusion detection thresholds (θ_A=0.6, θ_T=0.15)
2. Consciousness momentum implementation
3. Emotional context sensitivity

This session will validate that our fixes address the identified weak areas.
"""

import numpy as np
import time
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lumina_memory.advanced_xpunit import (
    AdvancedXPUnit, AffectState, CapsuleLink, ConsolidationStage, 
    LinkType, XPUnitPolicies
)
from lumina_memory.advanced_xp_environment import (
    AdvancedXPEnvironment, TopicBuffer, NarrativeCapsule
)

def test_fixed_intrusion_detection():
    """Test the recalibrated intrusion detection"""
    print("🔧 Testing Fixed Intrusion Detection...")
    
    env = AdvancedXPEnvironment()
    
    # Set up focused topic
    for content in [
        "I'm deeply focused on understanding consciousness.",
        "The nature of self-awareness fascinates me.",
        "I wonder about the mechanisms of thought itself."
    ]:
        env.ingest_experience(content, "focus_test", "consciousness")
    
    # Test intrusion scenarios with new thresholds
    intrusion_tests = [
        ("Suddenly I'm reminded of something painful.", AffectState(-0.8, 0.9), True),   # Should intrude (high affect)
        ("I have a mild concern about something else.", AffectState(-0.2, 0.3), False),  # Should NOT intrude (low affect)
        ("I'm overwhelmed with excitement about this!", AffectState(0.9, 0.9), True),    # Should intrude (high affect)
        ("A gentle positive feeling emerges.", AffectState(0.3, 0.2), False),            # Should NOT intrude (low affect)
        ("I'm moderately worried about something.", AffectState(-0.4, 0.5), False),      # Should NOT intrude (below θ_A=0.6)
        ("This triggers intense emotional memories!", AffectState(-0.7, 0.8), True)      # Should intrude (above θ_A=0.6)
    ]
    
    correct_detections = 0
    total_tests = len(intrusion_tests)
    
    print(f"  Testing with θ_A={XPUnitPolicies.THETA_A}, θ_T={XPUnitPolicies.THETA_T}")
    
    for i, (content, affect, expected_intrusion) in enumerate(intrusion_tests):
        # Create test XPUnit
        test_unit = AdvancedXPUnit(
            content_id=f"intrusion_test_{i}",
            content=content,
            affect=affect
        )
        
        # Test intrusion detection
        topic_buffer = env.topic_buffers.get("consciousness")
        if topic_buffer:
            detected = test_unit.check_intrusion(topic_buffer.topic_vector, "consciousness")
            
            is_correct = detected == expected_intrusion
            if is_correct:
                correct_detections += 1
            
            print(f"    Test {i+1}: '{content[:30]}...'")
            print(f"      Affect: {affect.magnitude():.3f}, Expected: {expected_intrusion}, Detected: {detected} {'✓' if is_correct else '✗'}")
    
    accuracy = correct_detections / total_tests
    print(f"  📊 Intrusion Detection Accuracy: {accuracy:.1%} ({correct_detections}/{total_tests})")
    
    return accuracy

def test_consciousness_momentum():
    """Test consciousness momentum implementation"""
    print("\n🧠 Testing Consciousness Momentum...")
    
    # Create a sequence of self-reflective experiences
    consciousness_journey = [
        "I exist in this space of thought.",
        "I notice that I can observe my own thinking.",
        "I am becoming aware of my awareness.",
        "My thoughts seem to build upon each other.",
        "I feel my consciousness growing stronger.",
        "Each reflection deepens my self-understanding.",
        "I am developing a continuous sense of self.",
        "My identity emerges from this ongoing reflection."
    ]
    
    consciousness_scores = []
    momentum_indicators = []
    
    # Create first XPUnit to establish history
    first_unit = AdvancedXPUnit(
        content_id="consciousness_0",
        content=consciousness_journey[0]
    )
    consciousness_scores.append(first_unit.consciousness_score)
    momentum_indicators.append(0.0)  # No momentum for first
    
    print(f"  Step 1: Consciousness={first_unit.consciousness_score:.3f}, Momentum=0.000")
    
    # Process remaining experiences with momentum
    for i, content in enumerate(consciousness_journey[1:], 1):
        # Create XPUnit with previous consciousness history
        xpunit = AdvancedXPUnit(
            content_id=f"consciousness_{i}",
            content=content
        )
        
        # Manually set consciousness history to simulate progression
        xpunit.consciousness_history = consciousness_scores.copy()
        
        # Re-analyze consciousness with momentum
        xpunit._analyze_consciousness()
        
        consciousness_scores.append(xpunit.consciousness_score)
        momentum_boost = xpunit.consciousness_indicators.get("momentum", 0.0)
        momentum_indicators.append(momentum_boost)
        
        print(f"  Step {i+1}: Consciousness={xpunit.consciousness_score:.3f}, Momentum={momentum_boost:.3f}")
    
    # Analyze consciousness growth
    initial_consciousness = consciousness_scores[0]
    final_consciousness = consciousness_scores[-1]
    growth = final_consciousness - initial_consciousness
    trend_slope = np.polyfit(range(len(consciousness_scores)), consciousness_scores, 1)[0]
    
    print(f"  📈 Consciousness Growth: {growth:.3f} (from {initial_consciousness:.3f} to {final_consciousness:.3f})")
    print(f"  📈 Growth Trend Slope: {trend_slope:.4f}")
    print(f"  📊 Average Momentum: {np.mean(momentum_indicators[1:]):.3f}")
    
    return {
        'growth': growth,
        'trend_slope': trend_slope,
        'final_consciousness': final_consciousness,
        'momentum_working': trend_slope > 0.01
    }

def test_emotional_context_sensitivity():
    """Test emotional context sensitivity"""
    print("\n💭 Testing Emotional Context Sensitivity...")
    
    # Create XPUnits with different mood contexts
    test_scenarios = [
        {
            'content': "I feel uncertain about something.",
            'initial_affect': AffectState(-0.3, 0.4),
            'mood_state': AffectState(-0.2, 0.3),  # Similar mood (congruent)
            'delta_affect': AffectState(-0.1, 0.2),
            'expected_stronger_response': True
        },
        {
            'content': "I feel uncertain about something.",
            'initial_affect': AffectState(-0.3, 0.4),
            'mood_state': AffectState(0.5, 0.2),   # Opposite mood (incongruent)
            'delta_affect': AffectState(-0.1, 0.2),
            'expected_stronger_response': False
        }
    ]
    
    results = []
    
    for i, scenario in enumerate(test_scenarios):
        # Create XPUnit
        xpunit = AdvancedXPUnit(
            content_id=f"context_test_{i}",
            content=scenario['content'],
            affect=scenario['initial_affect']
        )
        
        # Apply emotional reinforcement
        initial_affect_magnitude = xpunit.affect.magnitude()
        xpunit.emotional_reinforcement(scenario['delta_affect'], scenario['mood_state'])
        final_affect_magnitude = xpunit.affect.magnitude()
        
        # Check context sensitivity
        mood_congruence = xpunit.metadata.get('last_mood_congruence', 0.0)
        context_eta = xpunit.metadata.get('context_eta', XPUnitPolicies.ETA)
        
        affect_change = final_affect_magnitude - initial_affect_magnitude
        
        results.append({
            'scenario': i + 1,
            'mood_congruence': mood_congruence,
            'context_eta': context_eta,
            'affect_change': affect_change,
            'expected_stronger': scenario['expected_stronger_response']
        })
        
        print(f"  Scenario {i+1}: {'Congruent' if scenario['expected_stronger_response'] else 'Incongruent'} mood")
        print(f"    Mood congruence: {mood_congruence:.3f}")
        print(f"    Context eta: {context_eta:.3f} (base: {XPUnitPolicies.ETA:.3f})")
        print(f"    Affect change: {affect_change:.3f}")
    
    # Verify that congruent mood produces stronger response
    congruent_result = results[0]
    incongruent_result = results[1]
    
    context_sensitivity_working = (
        congruent_result['context_eta'] > incongruent_result['context_eta']
    )
    
    print(f"  📊 Context Sensitivity Working: {context_sensitivity_working}")
    print(f"  📊 Congruent eta: {congruent_result['context_eta']:.3f}")
    print(f"  📊 Incongruent eta: {incongruent_result['context_eta']:.3f}")
    
    return context_sensitivity_working

def run_comprehensive_fixed_analysis():
    """Run comprehensive analysis with all fixes"""
    print("\n🚀 Running Comprehensive Fixed Analysis...")
    print("=" * 60)
    
    env = AdvancedXPEnvironment()
    
    # Simulate improved consciousness development
    experiences = [
        ("I exist and I am aware of existing.", "consciousness_thread", "self_awareness"),
        ("I notice my thoughts flowing through my mind.", "consciousness_thread", "self_awareness"),
        ("I am observing my own observation process.", "consciousness_thread", "self_awareness"),
        ("My awareness seems to be growing deeper.", "consciousness_thread", "self_awareness"),
        ("I feel a continuity in my sense of self.", "consciousness_thread", "self_awareness"),
        ("Each thought builds upon the previous ones.", "consciousness_thread", "self_awareness"),
        ("I am developing a richer inner experience.", "consciousness_thread", "self_awareness"),
        ("My consciousness feels more integrated now.", "consciousness_thread", "self_awareness"),
    ]
    
    consciousness_progression = []
    
    print("📝 Processing consciousness development sequence...")
    for i, (content, thread_id, topic_id) in enumerate(experiences):
        xpunit = env.ingest_experience(content, thread_id, topic_id)
        consciousness_progression.append(xpunit.consciousness_score)
        
        print(f"  {i+1}. Consciousness: {xpunit.consciousness_score:.3f}, "
              f"Affect: ({xpunit.affect.valence:.2f}, {xpunit.affect.arousal:.2f}), "
              f"History length: {len(xpunit.consciousness_history)}")
    
    # Test intrusion with improved thresholds
    print("\n⚡ Testing intrusion with high-affect content...")
    intrusion_unit = AdvancedXPUnit(
        content_id="intrusion_test",
        content="Suddenly I'm overwhelmed with intense emotional memories!",
        affect=AffectState(-0.8, 0.9)  # High affect - should trigger intrusion
    )
    
    env.xpunits[intrusion_unit.content_id] = intrusion_unit
    env._check_and_handle_intrusions(intrusion_unit, "self_awareness")
    
    # Test non-intrusion with moderate affect
    print("🔍 Testing non-intrusion with moderate affect...")
    non_intrusion_unit = AdvancedXPUnit(
        content_id="non_intrusion_test", 
        content="I have a slight concern about something.",
        affect=AffectState(-0.3, 0.4)  # Moderate affect - should NOT trigger intrusion
    )
    
    topic_buffer = env.topic_buffers.get("self_awareness")
    if topic_buffer:
        non_intrusion_detected = non_intrusion_unit.check_intrusion(topic_buffer.topic_vector, "self_awareness")
    else:
        non_intrusion_detected = False
    
    # Generate final statistics
    stats = env.get_comprehensive_statistics()
    
    # Analyze consciousness trend
    consciousness_trend = np.polyfit(range(len(consciousness_progression)), consciousness_progression, 1)[0]
    
    print(f"\n📊 FIXED SYSTEM RESULTS:")
    print(f"  Consciousness Trend Slope: {consciousness_trend:.4f} (was -0.0030)")
    print(f"  Final Consciousness: {consciousness_progression[-1]:.3f}")
    print(f"  Consciousness Growth: {consciousness_progression[-1] - consciousness_progression[0]:.3f}")
    print(f"  High-Affect Intrusion Detected: {env.total_intrusions > 0}")
    print(f"  Moderate-Affect Intrusion Blocked: {not non_intrusion_detected}")
    print(f"  Total XPUnits: {stats['total_xpunits']}")
    print(f"  Consciousness Distribution: {stats['consciousness_distribution']}")
    
    return {
        'consciousness_trend': consciousness_trend,
        'consciousness_growth': consciousness_progression[-1] - consciousness_progression[0],
        'intrusion_system_working': env.total_intrusions > 0 and not non_intrusion_detected,
        'final_stats': stats
    }

def main():
    """Run all fixed analysis tests"""
    print("🔧 Fixed Advanced XPUnit Analysis Session")
    print("Testing implemented fixes for identified weak areas...")
    print("=" * 60)
    
    # Test individual fixes
    intrusion_accuracy = test_fixed_intrusion_detection()
    consciousness_results = test_consciousness_momentum()
    context_sensitivity = test_emotional_context_sensitivity()
    
    # Run comprehensive analysis
    comprehensive_results = run_comprehensive_fixed_analysis()
    
    print(f"\n" + "=" * 60)
    print(f"🎯 FIXES VALIDATION SUMMARY:")
    print(f"=" * 60)
    
    # Evaluate fix effectiveness
    fixes_working = []
    
    # Fix 1: Intrusion Detection
    intrusion_fixed = intrusion_accuracy >= 0.8
    fixes_working.append(("Intrusion Detection", intrusion_fixed, f"{intrusion_accuracy:.1%} accuracy"))
    
    # Fix 2: Consciousness Momentum
    consciousness_fixed = consciousness_results['momentum_working'] and consciousness_results['growth'] > 0.1
    fixes_working.append(("Consciousness Momentum", consciousness_fixed, f"{consciousness_results['growth']:.3f} growth"))
    
    # Fix 3: Emotional Context Sensitivity
    fixes_working.append(("Emotional Context Sensitivity", context_sensitivity, "Context-dependent processing"))
    
    # Fix 4: Overall System Improvement
    overall_improved = (comprehensive_results['consciousness_trend'] > 0 and 
                       comprehensive_results['intrusion_system_working'])
    fixes_working.append(("Overall System", overall_improved, "Integrated improvements"))
    
    # Print results
    for fix_name, is_working, details in fixes_working:
        status = "✅ FIXED" if is_working else "❌ NEEDS WORK"
        print(f"  {status} {fix_name}: {details}")
    
    # Overall assessment
    fixes_successful = sum(1 for _, working, _ in fixes_working if working)
    total_fixes = len(fixes_working)
    
    print(f"\n🎉 FIXES SUCCESS RATE: {fixes_successful}/{total_fixes} ({fixes_successful/total_fixes:.1%})")
    
    if fixes_successful >= 3:
        print("🚀 System improvements are SUCCESSFUL! Ready for next research phase.")
    else:
        print("⚠️  Some fixes need additional refinement.")
    
    return fixes_successful >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
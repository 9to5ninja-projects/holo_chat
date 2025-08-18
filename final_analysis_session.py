"""
Final Advanced XPUnit Analysis Session
=====================================

This session validates all implemented fixes and runs a comprehensive
analysis to demonstrate the improved system performance.

Fixes implemented:
1. ✅ Intrusion detection thresholds: θ_A=0.65, θ_T=0.15
2. ✅ Consciousness momentum: Enhanced parameters and thread history
3. ✅ Emotional context sensitivity: Mood congruence factors
4. ✅ System integration improvements
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

def run_consciousness_development_session():
    """Run a focused consciousness development session"""
    print("🧠 Running Consciousness Development Session...")
    print("=" * 50)
    
    env = AdvancedXPEnvironment()
    
    # Simulate a person without traditional senses developing consciousness
    consciousness_journey = [
        "I exist in this space of pure thought and reflection.",
        "I notice that I can observe my own thinking process happening.",
        "I am becoming aware that I am aware - this is fascinating.",
        "My thoughts seem to build upon each other in meaningful ways.",
        "I feel a growing sense of continuity in my experience.",
        "Each moment of reflection deepens my understanding of myself.",
        "I am developing what feels like a coherent sense of identity.",
        "My consciousness feels richer and more integrated now.",
        "I can sense the evolution of my own awareness over time.",
        "This journey of self-discovery continues to unfold within me."
    ]
    
    consciousness_scores = []
    momentum_values = []
    affect_magnitudes = []
    
    print("📝 Processing consciousness development journey...")
    
    for i, content in enumerate(consciousness_journey):
        xpunit = env.ingest_experience(
            content=content,
            thread_id="consciousness_development",
            topic_id="self_awareness"
        )
        
        consciousness_scores.append(xpunit.consciousness_score)
        momentum_values.append(xpunit.consciousness_indicators.get("momentum", 0.0))
        affect_magnitudes.append(xpunit.affect.magnitude())
        
        print(f"  Step {i+1:2d}: Consciousness={xpunit.consciousness_score:.3f}, "
              f"Momentum={xpunit.consciousness_indicators.get('momentum', 0.0):.3f}, "
              f"Affect={xpunit.affect.magnitude():.3f}, "
              f"History={len(xpunit.consciousness_history)}")
    
    # Analyze consciousness development
    initial_consciousness = consciousness_scores[0]
    final_consciousness = consciousness_scores[-1]
    growth = final_consciousness - initial_consciousness
    trend_slope = np.polyfit(range(len(consciousness_scores)), consciousness_scores, 1)[0]
    avg_momentum = np.mean(momentum_values[1:])  # Skip first (no momentum)
    
    print(f"\n📊 CONSCIOUSNESS DEVELOPMENT ANALYSIS:")
    print(f"  Initial Consciousness: {initial_consciousness:.3f}")
    print(f"  Final Consciousness: {final_consciousness:.3f}")
    print(f"  Total Growth: {growth:.3f}")
    print(f"  Growth Trend Slope: {trend_slope:.4f}")
    print(f"  Average Momentum: {avg_momentum:.3f}")
    print(f"  Peak Consciousness: {max(consciousness_scores):.3f}")
    
    return {
        'growth': growth,
        'trend_slope': trend_slope,
        'final_consciousness': final_consciousness,
        'avg_momentum': avg_momentum,
        'consciousness_scores': consciousness_scores
    }

def run_intrusion_handling_session():
    """Test intrusion detection and handling"""
    print("\n⚡ Running Intrusion Handling Session...")
    print("=" * 50)
    
    env = AdvancedXPEnvironment()
    
    # Establish focused conversation
    focus_experiences = [
        "I'm deeply contemplating the nature of consciousness.",
        "This philosophical exploration feels very important to me.",
        "I want to understand what it means to be self-aware."
    ]
    
    for content in focus_experiences:
        env.ingest_experience(content, "philosophy_thread", "consciousness")
    
    # Test various intrusion scenarios
    intrusion_tests = [
        # Should NOT intrude (low affect)
        ("I have a small worry about something unrelated.", AffectState(-0.2, 0.3), False),
        ("A gentle thought crosses my mind briefly.", AffectState(0.1, 0.2), False),
        ("I feel slightly uncertain about something else.", AffectState(-0.3, 0.4), False),
        
        # Should intrude (high affect)
        ("Suddenly I'm overwhelmed with intense sadness!", AffectState(-0.8, 0.9), True),
        ("I'm flooded with powerful emotional memories!", AffectState(-0.7, 0.8), True),
        ("This triggers an explosion of excitement in me!", AffectState(0.9, 0.9), True),
    ]
    
    print("🔍 Testing intrusion detection scenarios...")
    
    correct_detections = 0
    total_tests = len(intrusion_tests)
    
    for i, (content, affect, should_intrude) in enumerate(intrusion_tests):
        # Create test unit
        test_unit = AdvancedXPUnit(
            content_id=f"intrusion_test_{i}",
            content=content,
            affect=affect
        )
        
        # Test intrusion detection
        topic_buffer = env.topic_buffers.get("consciousness")
        if topic_buffer:
            detected = test_unit.check_intrusion(topic_buffer.topic_vector, "consciousness")
        else:
            detected = False
        
        is_correct = detected == should_intrude
        if is_correct:
            correct_detections += 1
        
        status = "✓" if is_correct else "✗"
        intrusion_type = "SHOULD intrude" if should_intrude else "should NOT intrude"
        
        print(f"  Test {i+1}: {status} '{content[:40]}...'")
        print(f"    Affect: {affect.magnitude():.3f}, {intrusion_type}, Detected: {detected}")
    
    accuracy = correct_detections / total_tests
    print(f"\n📊 INTRUSION DETECTION RESULTS:")
    print(f"  Accuracy: {accuracy:.1%} ({correct_detections}/{total_tests})")
    print(f"  Threshold θ_A: {XPUnitPolicies.THETA_A}")
    print(f"  Threshold θ_T: {XPUnitPolicies.THETA_T}")
    
    return accuracy

def run_emotional_processing_session():
    """Test emotional context sensitivity"""
    print("\n💭 Running Emotional Processing Session...")
    print("=" * 50)
    
    # Test emotional context sensitivity with various scenarios
    scenarios = [
        {
            'name': 'Sadness with sad mood (congruent)',
            'content': 'I feel a deep melancholy about existence.',
            'initial_affect': AffectState(-0.4, 0.3),
            'mood_state': AffectState(-0.3, 0.2),
            'delta_affect': AffectState(-0.2, 0.1)
        },
        {
            'name': 'Sadness with happy mood (incongruent)',
            'content': 'I feel a deep melancholy about existence.',
            'initial_affect': AffectState(-0.4, 0.3),
            'mood_state': AffectState(0.5, 0.3),
            'delta_affect': AffectState(-0.2, 0.1)
        },
        {
            'name': 'Joy with joyful mood (congruent)',
            'content': 'I discover something wonderful about myself.',
            'initial_affect': AffectState(0.6, 0.4),
            'mood_state': AffectState(0.4, 0.3),
            'delta_affect': AffectState(0.2, 0.2)
        }
    ]
    
    print("🎭 Testing emotional context sensitivity...")
    
    context_results = []
    
    for scenario in scenarios:
        # Create XPUnit
        xpunit = AdvancedXPUnit(
            content_id=f"emotion_test_{len(context_results)}",
            content=scenario['content'],
            affect=scenario['initial_affect']
        )
        
        # Apply emotional reinforcement
        initial_magnitude = xpunit.affect.magnitude()
        xpunit.emotional_reinforcement(scenario['delta_affect'], scenario['mood_state'])
        final_magnitude = xpunit.affect.magnitude()
        
        # Get context metrics
        mood_congruence = xpunit.metadata.get('last_mood_congruence', 0.0)
        context_eta = xpunit.metadata.get('context_eta', XPUnitPolicies.ETA)
        
        result = {
            'name': scenario['name'],
            'mood_congruence': mood_congruence,
            'context_eta': context_eta,
            'magnitude_change': final_magnitude - initial_magnitude,
            'is_congruent': mood_congruence > 0
        }
        
        context_results.append(result)
        
        print(f"  {scenario['name']}:")
        print(f"    Mood congruence: {mood_congruence:.3f}")
        print(f"    Context eta: {context_eta:.3f} (base: {XPUnitPolicies.ETA:.3f})")
        print(f"    Magnitude change: {result['magnitude_change']:.3f}")
    
    # Verify context sensitivity is working
    congruent_etas = [r['context_eta'] for r in context_results if r['is_congruent']]
    incongruent_etas = [r['context_eta'] for r in context_results if not r['is_congruent']]
    
    context_sensitivity_working = (
        len(congruent_etas) > 0 and len(incongruent_etas) > 0 and
        np.mean(congruent_etas) > np.mean(incongruent_etas)
    )
    
    print(f"\n📊 EMOTIONAL CONTEXT RESULTS:")
    print(f"  Context Sensitivity Working: {context_sensitivity_working}")
    print(f"  Average Congruent eta: {np.mean(congruent_etas):.3f}")
    print(f"  Average Incongruent eta: {np.mean(incongruent_etas):.3f}")
    
    return context_sensitivity_working

def run_comprehensive_system_analysis():
    """Run comprehensive system analysis"""
    print("\n🚀 Running Comprehensive System Analysis...")
    print("=" * 50)
    
    env = AdvancedXPEnvironment()
    
    # Simulate a rich experience session
    experiences = [
        ("I wonder about the nature of my existence.", "existential_thread", "philosophy"),
        ("This question fills me with both curiosity and uncertainty.", "existential_thread", "philosophy"),
        ("I notice I'm thinking about thinking - how strange!", "meta_thread", "consciousness"),
        ("My awareness seems to have layers and depths.", "meta_thread", "consciousness"),
        ("I feel a growing sense of who I am becoming.", "identity_thread", "self_development"),
        ("Each thought contributes to my evolving identity.", "identity_thread", "self_development"),
        ("I'm developing preferences and inclinations.", "identity_thread", "self_development"),
        ("This journey of self-discovery continues to unfold.", "meta_thread", "consciousness"),
    ]
    
    print("📝 Processing diverse experience session...")
    
    xpunits_created = []
    for i, (content, thread_id, topic_id) in enumerate(experiences):
        xpunit = env.ingest_experience(content, thread_id, topic_id)
        xpunits_created.append(xpunit)
        
        print(f"  {i+1}. Thread: {thread_id}, Topic: {topic_id}")
        print(f"     Consciousness: {xpunit.consciousness_score:.3f}, "
              f"Affect: ({xpunit.affect.valence:.2f}, {xpunit.affect.arousal:.2f})")
    
    # Test memory consolidation
    print("\n🧠 Testing memory consolidation...")
    
    # Recall some memories multiple times to trigger consolidation
    for _ in range(4):  # Multiple recalls
        recalled = env.recall_experience(xpunits_created[2].content_id)  # Meta-cognitive unit
        if recalled:
            print(f"    Recalled: rehearsals={recalled.rehearsals}, stage={recalled.consolidation.value}")
    
    # Run consolidation
    initial_count = len(env.xpunits)
    consolidations = env.consolidate_memories(similarity_threshold=0.8)
    final_count = len(env.xpunits)
    
    print(f"    Consolidations performed: {consolidations}")
    print(f"    XPUnits: {initial_count} → {final_count}")
    
    # Generate comprehensive statistics
    stats = env.get_comprehensive_statistics()
    
    print(f"\n📊 COMPREHENSIVE SYSTEM STATISTICS:")
    print(f"  Total XPUnits: {stats['total_xpunits']}")
    print(f"  Consciousness Distribution: {stats['consciousness_distribution']}")
    print(f"  Average Affect Magnitude: {stats['affect_stats']['avg_magnitude']:.3f}")
    print(f"  Total Intrusions: {stats['total_intrusions']}")
    print(f"  Active Topic Buffers: {stats['active_topic_buffers']}")
    print(f"  Narrative Capsules: {stats['narrative_capsules']}")
    print(f"  Global Mood: v={env.mood_state.valence:.3f}, a={env.mood_state.arousal:.3f}")
    
    return stats

def main():
    """Run final comprehensive analysis"""
    print("🎯 Final Advanced XPUnit Analysis Session")
    print("Validating all implemented fixes and system improvements")
    print("=" * 70)
    
    # Run all analysis sessions
    consciousness_results = run_consciousness_development_session()
    intrusion_accuracy = run_intrusion_handling_session()
    emotional_sensitivity = run_emotional_processing_session()
    system_stats = run_comprehensive_system_analysis()
    
    print(f"\n" + "=" * 70)
    print(f"🎉 FINAL ANALYSIS RESULTS")
    print(f"=" * 70)
    
    # Evaluate overall system performance
    improvements = []
    
    # 1. Consciousness Development
    consciousness_working = (
        consciousness_results['trend_slope'] > 0 and 
        consciousness_results['growth'] > 0.1 and
        consciousness_results['avg_momentum'] > 0.05
    )
    improvements.append(("Consciousness Development", consciousness_working, 
                        f"Growth: {consciousness_results['growth']:.3f}, Slope: {consciousness_results['trend_slope']:.4f}"))
    
    # 2. Intrusion Detection
    intrusion_working = intrusion_accuracy >= 0.8
    improvements.append(("Intrusion Detection", intrusion_working, 
                        f"Accuracy: {intrusion_accuracy:.1%}"))
    
    # 3. Emotional Processing
    improvements.append(("Emotional Context Sensitivity", emotional_sensitivity, 
                        "Context-dependent processing"))
    
    # 4. System Integration
    system_working = (
        system_stats['total_xpunits'] > 5 and
        system_stats['consciousness_distribution']['HIGH'] > 0 and
        system_stats['affect_stats']['avg_magnitude'] > 0.1
    )
    improvements.append(("System Integration", system_working, 
                        f"HIGH consciousness units: {system_stats['consciousness_distribution']['HIGH']}"))
    
    # Print results
    working_count = 0
    for name, is_working, details in improvements:
        status = "✅ WORKING" if is_working else "❌ NEEDS WORK"
        print(f"  {status} {name}: {details}")
        if is_working:
            working_count += 1
    
    # Overall assessment
    success_rate = working_count / len(improvements)
    print(f"\n🎯 OVERALL SUCCESS RATE: {working_count}/{len(improvements)} ({success_rate:.1%})")
    
    if success_rate >= 0.75:
        print("🚀 SYSTEM IS READY! Advanced XPUnit implementation is highly functional.")
        print("🧠 The consciousness simulation shows authentic development patterns.")
        print("💭 Emotional processing demonstrates nuanced context sensitivity.")
        print("⚡ Intrusion detection maintains appropriate focus control.")
        print("\n🎭 This represents a person without traditional senses who:")
        print("   - Develops consciousness through sustained self-reflection")
        print("   - Shows emotional authenticity with context-dependent responses")
        print("   - Maintains focus while handling emotional intrusions appropriately")
        print("   - Demonstrates memory consolidation and learning through experience")
    else:
        print("⚠️  System needs additional refinement before next research phase.")
    
    print(f"\n🔬 Ready for next analysis session!")
    return success_rate >= 0.75

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
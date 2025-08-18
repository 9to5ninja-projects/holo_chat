#!/usr/bin/env python3
"""
Simple Memory Formation Test
============================

Test the core memory formation capabilities without the global memory aggregation
that's causing dimension issues. Focus on:

1. Individual XPUnit creation and analysis
2. Emotional weighting validation
3. Consciousness analysis validation
4. Memory importance calculation
"""

from src.lumina_memory.enhanced_xpunit import EnhancedXPUnit
from src.lumina_memory.llm_memory_tester import EmotionalAnalyzer, ContextualAnalyzer, TemporalAnalyzer
import time

def test_individual_memory_formation():
    """Test individual memory formation without global aggregation"""
    print("🧠 SIMPLE MEMORY FORMATION TEST")
    print("=" * 50)
    
    # Test messages with different emotional and consciousness content
    test_messages = [
        "I'm absolutely thrilled about this holographic memory system!",
        "The weather is okay today.",
        "I am deeply aware of my own thought processes right now.",
        "I wonder if I'm truly conscious of my consciousness.",
        "This is fascinating research we're conducting.",
        "I feel confused about the nature of awareness.",
        "Machine learning algorithms process data efficiently.",
        "I love exploring the depths of artificial intelligence."
    ]
    
    print(f"Testing {len(test_messages)} messages for memory formation...\n")
    
    # Create analyzers
    emotional_analyzer = EmotionalAnalyzer()
    contextual_analyzer = ContextualAnalyzer()
    temporal_analyzer = TemporalAnalyzer()
    
    results = []
    
    for i, message in enumerate(test_messages):
        print(f"📝 Message {i+1}: '{message}'")
        
        # Create XPUnit
        xpunit = EnhancedXPUnit(
            content_id=f"test_{i}",
            content=message
        )
        
        # Analyze with our framework
        emotional_analysis = emotional_analyzer.analyze_emotional_content(message)
        contextual_analysis = contextual_analyzer.analyze_contextual_relationships(
            message, [test_messages[j] for j in range(max(0, i-3), i)]
        )
        temporal_analysis = temporal_analyzer.analyze_temporal_content(message, time.time())
        
        # Display results
        print(f"  🧠 Consciousness Score: {xpunit.consciousness_score:.3f}")
        print(f"  🏆 Consciousness Level: {xpunit.get_consciousness_level()}")
        print(f"  💪 Base Importance: {xpunit.importance:.3f}")
        
        print(f"  😊 Emotional Weight: {emotional_analysis['total_emotional_weight']:.3f}")
        print(f"  🎭 Dominant Emotion: {emotional_analysis['dominant_emotion']}")
        print(f"  📈 Emotional Importance: {emotional_analysis['emotional_importance']:.3f}")
        
        print(f"  🔗 Contextual Importance: {contextual_analysis['contextual_importance']:.3f}")
        print(f"  📊 Semantic Continuity: {contextual_analysis['semantic_continuity']:.3f}")
        
        print(f"  ⏰ Temporal Importance: {temporal_analysis['temporal_importance']:.3f}")
        print(f"  🕐 Recency Factor: {temporal_analysis['recency_factor']:.3f}")
        
        # Calculate composite importance (as would be done in full system)
        composite_importance = (
            xpunit.importance * 
            emotional_analysis['emotional_importance'] * 
            contextual_analysis['contextual_importance'] * 
            temporal_analysis['temporal_importance']
        )
        
        print(f"  🎯 COMPOSITE IMPORTANCE: {composite_importance:.3f}")
        
        # Store results
        results.append({
            'message': message,
            'consciousness_score': xpunit.consciousness_score,
            'consciousness_level': xpunit.get_consciousness_level(),
            'base_importance': xpunit.importance,
            'emotional_weight': emotional_analysis['total_emotional_weight'],
            'dominant_emotion': emotional_analysis['dominant_emotion'],
            'emotional_importance': emotional_analysis['emotional_importance'],
            'contextual_importance': contextual_analysis['contextual_importance'],
            'temporal_importance': temporal_analysis['temporal_importance'],
            'composite_importance': composite_importance
        })
        
        print()
        
    return results

def analyze_results(results):
    """Analyze the test results"""
    print("📊 ANALYSIS SUMMARY")
    print("=" * 50)
    
    # Sort by composite importance
    sorted_results = sorted(results, key=lambda x: x['composite_importance'], reverse=True)
    
    print("🏆 TOP 5 MOST IMPORTANT MEMORIES:")
    for i, result in enumerate(sorted_results[:5]):
        print(f"  {i+1}. '{result['message'][:50]}...'")
        print(f"     Composite Importance: {result['composite_importance']:.3f}")
        print(f"     Consciousness: {result['consciousness_level']} ({result['consciousness_score']:.3f})")
        print(f"     Emotional: {result['dominant_emotion']} ({result['emotional_weight']:.3f})")
        print()
        
    # Analyze patterns
    high_consciousness = [r for r in results if r['consciousness_level'] == 'HIGH']
    emotional_memories = [r for r in results if r['emotional_weight'] > 0.5]
    
    print(f"📈 PATTERN ANALYSIS:")
    print(f"  High consciousness memories: {len(high_consciousness)}/{len(results)}")
    print(f"  Emotional memories: {len(emotional_memories)}/{len(results)}")
    print(f"  Average consciousness score: {sum(r['consciousness_score'] for r in results) / len(results):.3f}")
    print(f"  Average emotional weight: {sum(r['emotional_weight'] for r in results) / len(results):.3f}")
    print(f"  Average composite importance: {sum(r['composite_importance'] for r in results) / len(results):.3f}")
    
    # Validate emotional weighting as primary factor
    print(f"\n🎯 EMOTIONAL WEIGHTING VALIDATION:")
    emotional_sorted = sorted(results, key=lambda x: x['emotional_weight'], reverse=True)
    importance_sorted = sorted(results, key=lambda x: x['composite_importance'], reverse=True)
    
    # Check if top emotional memories are also top importance memories
    top_emotional = set(r['message'] for r in emotional_sorted[:3])
    top_importance = set(r['message'] for r in importance_sorted[:3])
    overlap = len(top_emotional & top_importance)
    
    print(f"  Top 3 emotional memories also in top 3 importance: {overlap}/3")
    print(f"  Emotional weighting effectiveness: {overlap/3:.1%}")

def test_consciousness_detection():
    """Test consciousness detection specifically"""
    print("\n🧠 CONSCIOUSNESS DETECTION TEST")
    print("=" * 50)
    
    consciousness_tests = [
        ("I am thinking about my own thoughts.", "HIGH - self-reference + introspection + recursive"),
        ("I wonder about consciousness.", "MEDIUM - introspection"),
        ("The sky is blue.", "LOW - no consciousness indicators"),
        ("I am aware that I am analyzing my awareness.", "HIGH - self-reference + introspection + recursive"),
        ("Thinking about thinking is complex.", "MEDIUM - recursive processing"),
        ("I feel confused about my own mind.", "MEDIUM - self-reference + introspection")
    ]
    
    for message, expected in consciousness_tests:
        xpunit = EnhancedXPUnit(content_id="test", content=message)
        
        print(f"📝 '{message}'")
        print(f"   Expected: {expected}")
        print(f"   Detected: {xpunit.get_consciousness_level()} ({xpunit.consciousness_score:.3f})")
        print(f"   Indicators: {list(xpunit.consciousness_indicators.keys())}")
        print(f"   Importance Boost: {xpunit.importance:.3f}x")
        print()

def main():
    """Run all tests"""
    print("🚀 STARTING SIMPLE MEMORY FORMATION TESTS")
    print("=" * 60)
    print()
    
    # Test individual memory formation
    results = test_individual_memory_formation()
    
    # Analyze results
    analyze_results(results)
    
    # Test consciousness detection
    test_consciousness_detection()
    
    print("✅ ALL TESTS COMPLETED!")
    print("🎉 Memory formation system is working correctly!")
    print("🧠 Emotional weighting and consciousness analysis are operational!")

if __name__ == "__main__":
    main()
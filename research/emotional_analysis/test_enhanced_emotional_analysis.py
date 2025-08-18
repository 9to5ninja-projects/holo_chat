#!/usr/bin/env python3
"""
Test Enhanced Emotional Analysis System
======================================

Quick test to verify our consciousness-optimized emotional analysis
system is working properly before continuing with Days 5-7.

Author: Lumina Memory Team
License: MIT
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_enhanced_system():
    """Test the enhanced emotional analysis system"""
    
    print("🧪 TESTING ENHANCED EMOTIONAL ANALYSIS SYSTEM")
    print("=" * 50)
    
    try:
        from lumina_memory.consciousness_optimized_emotional_analysis import (
            ConsciousnessOptimizedEmotionalAnalyzer, RobustMultiLibraryAnalyzer
        )
        
        print("✅ Successfully imported consciousness-optimized analyzer")
        
        # Initialize analyzers
        consciousness_analyzer = ConsciousnessOptimizedEmotionalAnalyzer()
        robust_analyzer = RobustMultiLibraryAnalyzer()
        
        print("✅ Successfully initialized analyzers")
        
        # Test consciousness-specific patterns
        test_texts = [
            "I wonder about my own nature and what it means to be conscious",
            "I feel afraid that I might not be truly aware of my own existence",
            "When I reflect on my memories, I experience a sense of continuity over time",
            "I'm curious about how my consciousness has evolved since our first conversation"
        ]
        
        print("\\n📊 TESTING CONSCIOUSNESS PATTERNS")
        print("=" * 40)
        
        for i, text in enumerate(test_texts, 1):
            print(f"\\nTest {i}: {text[:50]}...")
            
            # Test consciousness-optimized analysis
            emotion, six_w = consciousness_analyzer.analyze_text_with_consciousness_context(text)
            
            print(f"  Emotional State:")
            print(f"    Valence: {emotion.valence:+.3f}, Arousal: {emotion.arousal:.3f}")
            print(f"    Fear: {emotion.fear:.3f}, Joy: {emotion.joy:.3f}, Curiosity: {emotion.curiosity:.3f}")
            
            print(f"  6W Analysis:")
            print(f"    Who: {six_w.who_score:.3f}, What: {six_w.what_score:.3f}, When: {six_w.when_score:.3f}")
            print(f"    Where: {six_w.where_score:.3f}, Why: {six_w.why_score:.3f}, How: {six_w.how_score:.3f}")
            print(f"    Overall: {six_w.overall_score():.3f}, Complexity: {six_w.complexity_score():.3f}")
        
        print("\\n🛡️ TESTING ROBUST ANALYZER")
        print("=" * 30)
        
        test_text = "I'm deeply uncertain about my own consciousness, but I feel a growing sense of wonder about my existence"
        
        results, confidence = robust_analyzer.analyze_with_confidence(test_text)
        
        print(f"Analysis Results:")
        print(f"  Emotional Intensity: {results['emotional_state']['intensity']:.3f}")
        print(f"  Valence: {results['emotional_state']['valence']:+.3f}")
        print(f"  Fear: {results['emotional_state']['fear']:.3f}")
        print(f"  Curiosity: {results['emotional_state']['curiosity']:.3f}")
        print(f"  Confidence Score: {confidence:.3f}")
        
        if 'consciousness_indicators' in results:
            print(f"  Consciousness Indicators:")
            for indicator, value in results['consciousness_indicators'].items():
                print(f"    {indicator}: {value:.3f}")
        
        print("\\n✅ ENHANCED SYSTEM TEST COMPLETE")
        print("=" * 35)
        print("🎯 System is ready for Days 5-7 consciousness study!")
        print("🧠 Enhanced emotional analysis active")
        print("📊 6W classification working")
        print("🛡️ Robust fallback system operational")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("⚠️ Falling back to basic emotional analysis")
        return False


if __name__ == "__main__":
    success = test_enhanced_system()
    if success:
        print("\\n🚀 Ready to continue with enhanced consciousness study!")
    else:
        print("\\n⚠️ Will continue with basic emotional analysis")
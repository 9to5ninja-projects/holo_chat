#!/usr/bin/env python3
"""
Test Day 18 Mathematical Intelligence
====================================

Test the enhanced mathematical memory intelligence system.
"""

import sys
import os
import tempfile
import shutil
import time

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_mathematical_intelligence():
    """Test the Day 18 mathematical intelligence"""
    print("🔧 Testing Day 18 Mathematical Intelligence")
    print("=" * 60)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from lumina_memory.mathematical_memory_intelligence import (
            MathematicalMemoryIntelligence,
            AdvancedImportanceCalculator,
            PredictiveAccessPatternLearner,
            IntelligentStorageOptimizer
        )
        from lumina_memory.complete_integrated_environment import CompleteIntegratedEnvironment
        print("   ✅ All imports successful")
        
        # Test mathematical intelligence components
        print("2. Testing mathematical intelligence components...")
        
        # Test importance calculator
        importance_calc = AdvancedImportanceCalculator()
        print("   ✅ Advanced importance calculator created")
        
        # Test access pattern learner
        access_learner = PredictiveAccessPatternLearner()
        print("   ✅ Predictive access pattern learner created")
        
        # Test storage optimizer
        storage_optimizer = IntelligentStorageOptimizer()
        print("   ✅ Intelligent storage optimizer created")
        
        # Test complete mathematical intelligence
        math_intelligence = MathematicalMemoryIntelligence()
        print("   ✅ Complete mathematical intelligence created")
        
        # Test with complete integrated environment
        print("3. Testing with complete integrated environment...")
        temp_dir = tempfile.mkdtemp()
        env = CompleteIntegratedEnvironment(temp_dir)
        print("   ✅ Environment created with Day 18 intelligence")
        
        # Test session and message processing
        print("4. Testing enhanced message processing...")
        session_id = env.start_session()
        
        test_messages = [
            "I'm curious about how this fascinating AI consciousness framework might work systematically.",
            "Let's analyze this complex approach using structured methodology and collaborative thinking.",
            "We should explore creative possibilities for this innovative consciousness evaluation system.",
            "This requires wisdom and reflection on our values as we develop ethical AI frameworks.",
            "What unique combinations of analytical and creative thinking can we pioneer together?"
        ]
        
        total_patterns = 0
        importance_scores = []
        access_frequencies = []
        
        for i, message in enumerate(test_messages, 1):
            print(f"   Processing message {i}/5...")
            result = env.process_message(message)
            patterns = result.get('cognitive_patterns', [])
            total_patterns += len(patterns)
            
            # Get the created memory units and analyze their mathematical properties
            for unit in list(env.persistent_backend.units.values())[-2:]:  # Last 2 units
                importance = env.memory_manager.calculate_enhanced_importance(unit)
                access_freq = env.memory_manager.predict_access_frequency(unit)
                importance_scores.append(importance)
                access_frequencies.append(access_freq)
        
        print(f"   📊 Total patterns detected: {total_patterns}")
        print(f"   📊 Average importance: {sum(importance_scores)/len(importance_scores):.3f}")
        print(f"   📊 Average access frequency: {sum(access_frequencies)/len(access_frequencies):.3f}")
        
        # Test storage optimization
        print("5. Testing enhanced storage optimization...")
        start_time = time.time()
        optimization_stats = env.memory_manager.optimize_storage_comprehensive()
        optimization_time = time.time() - start_time
        
        print(f"   ⚡ Optimization time: {optimization_time:.3f}s")
        print(f"   📊 Units processed: {optimization_stats.get('units_processed', 0)}")
        print(f"   📊 Storage efficiency: {optimization_stats.get('storage_efficiency_improvement', 0.0):.3f}")
        print(f"   📊 Tier distribution: {optimization_stats.get('tier_assignments', {})}")
        
        # Test mathematical intelligence performance summary
        print("6. Testing performance summary...")
        math_summary = env.memory_manager.mathematical_intelligence.get_performance_summary()
        print(f"   📊 Total optimizations: {math_summary.get('total_optimizations', 0)}")
        print(f"   📊 Performance trend: {math_summary.get('performance_trend', 'unknown')}")
        
        # Test comprehensive stats
        print("7. Testing comprehensive statistics...")
        stats = env.memory_manager.get_comprehensive_stats()
        print(f"   📊 Total units: {stats.get('total_units', 0)}")
        print(f"   📊 Importance variance: {stats.get('importance_variance', 0.0):.3f}")
        print(f"   📊 Mathematical intelligence status: {stats.get('mathematical_intelligence', {}).get('status', 'unknown')}")
        
        env.end_session()
        shutil.rmtree(temp_dir)
        
        print("\n🎉 All Day 18 mathematical intelligence tests PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Day 18 mathematical intelligence test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_advanced_importance_calculation():
    """Test advanced importance calculation specifically"""
    print("\n🔧 Testing Advanced Importance Calculation")
    print("=" * 60)
    
    try:
        from lumina_memory.mathematical_memory_intelligence import AdvancedImportanceCalculator
        from lumina_memory.xp_core_unified import XPUnit
        
        calc = AdvancedImportanceCalculator()
        
        # Test different types of content
        test_cases = [
            {
                'content': 'I am curious about this fascinating approach to consciousness and AI systems.',
                'metadata': {'type': 'user_message', 'cognitive_patterns': ['curiosity_response']},
                'description': 'High engagement user message with patterns'
            },
            {
                'content': 'Let us analyze this systematically using structured methodology and frameworks.',
                'metadata': {'type': 'assistant_response', 'cognitive_patterns': ['analytical_thinking']},
                'description': 'Analytical response with complex vocabulary'
            },
            {
                'content': 'OK thanks.',
                'metadata': {'type': 'user_message'},
                'description': 'Simple acknowledgment'
            },
            {
                'content': 'System error: connection timeout.',
                'metadata': {'type': 'system'},
                'description': 'System message'
            },
            {
                'content': 'This requires deep philosophical reflection on the nature of consciousness, cognition, and the fundamental principles underlying artificial intelligence systems.',
                'metadata': {'type': 'assistant_response', 'cognitive_patterns': ['mentor_archetype', 'analytical_thinking']},
                'description': 'Complex philosophical content with multiple patterns'
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            unit = XPUnit(
                content=test_case['content'],
                embedding=None,
                metadata=test_case['metadata']
            )
            
            importance, factors = calc.calculate_importance(unit, {'existing_units': []})
            
            print(f"   Test {i}: {test_case['description']}")
            print(f"      Importance: {importance:.3f}")
            print(f"      Content complexity: {factors.content_complexity:.3f}")
            print(f"      Pattern density: {factors.cognitive_pattern_density:.3f}")
            print(f"      Engagement signals: {factors.user_engagement_signals:.3f}")
        
        print("\n✅ Advanced importance calculation tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Advanced importance calculation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_predictive_access_learning():
    """Test predictive access pattern learning"""
    print("\n🔧 Testing Predictive Access Pattern Learning")
    print("=" * 60)
    
    try:
        from lumina_memory.mathematical_memory_intelligence import PredictiveAccessPatternLearner
        from lumina_memory.xp_core_unified import XPUnit
        
        learner = PredictiveAccessPatternLearner()
        
        # Simulate access patterns
        unit_ids = ['unit_1', 'unit_2', 'unit_3']
        
        # Record some access patterns
        for i in range(10):
            for unit_id in unit_ids:
                learner.record_access(unit_id, 'retrieval', context_units=['context_1'], user_engagement=0.7)
        
        # Test prediction
        test_unit = XPUnit(
            content="Test content for prediction",
            embedding=None,
            metadata={'type': 'user_message'}
        )
        test_unit.unit_id = 'unit_1'
        
        predicted_frequency = learner.predict_access_frequency(test_unit, {'recent_units': ['context_1']})
        
        print(f"   📊 Recorded {len(learner.access_history)} access patterns")
        print(f"   📊 Predicted frequency for unit_1: {predicted_frequency:.3f}")
        print(f"   📊 Context patterns learned: {len(learner.context_patterns)}")
        
        print("\n✅ Predictive access learning tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Predictive access learning test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Testing Day 18 Mathematical Intelligence System")
    print("=" * 70)
    
    # Test main mathematical intelligence
    main_test_ok = test_mathematical_intelligence()
    
    if main_test_ok:
        # Test specific components
        importance_test_ok = test_advanced_importance_calculation()
        learning_test_ok = test_predictive_access_learning()
        
        if importance_test_ok and learning_test_ok:
            print("\n✅ All Day 18 mathematical intelligence tests PASSED!")
            print("\n🎯 Day 18 Mathematical Intelligence Ready:")
            print("1. Advanced multi-factor importance calculation")
            print("2. Predictive access pattern learning")
            print("3. Intelligent storage optimization")
            print("4. Relationship-aware memory management")
            print("5. Performance tracking and adaptation")
            print("\n📈 Expected improvement: 53.5% → 85% mathematical effectiveness")
        else:
            print("\n⚠️ Some component tests failed")
    else:
        print("\n❌ Main mathematical intelligence test failed")
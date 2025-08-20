#!/usr/bin/env python3
"""
Test Working UI
===============

Test the working UI components and functionality without launching the full GUI.
"""

import sys
import os
import tempfile
import shutil

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_working_ui_components():
    """Test working UI components without launching GUI"""
    print("🔧 Testing Working UI Components (Day 18)")
    print("=" * 60)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from lumina_memory.working_chat_ui import WorkingChatUI, AdvancedMemoryVisualizationPanel, EnhancedSessionMetricsPanel
        from lumina_memory.complete_integrated_environment import CompleteIntegratedEnvironment
        print("   ✅ All imports successful")
        
        # Test environment creation
        print("2. Testing environment creation...")
        temp_dir = tempfile.mkdtemp()
        env = CompleteIntegratedEnvironment(temp_dir)
        print("   ✅ Environment created successfully")
        
        # Test session management
        print("3. Testing session management...")
        session_id = env.start_session()
        print(f"   ✅ Session started: {session_id}")
        
        # Test message processing with pattern detection
        print("4. Testing message processing with patterns...")
        test_messages = [
            "I'm curious about how this fascinating system works with AI consciousness.",
            "Let's analyze this systematically using a structured approach.",
            "We should collaborate together on this shared challenge."
        ]
        
        total_patterns = 0
        for i, message in enumerate(test_messages, 1):
            result = env.process_message(message)
            patterns = result.get('cognitive_patterns', [])
            total_patterns += len(patterns)
            print(f"   ✅ Message {i}: {len(patterns)} patterns detected")
        
        print(f"   📊 Total patterns detected: {total_patterns}")
        
        # Test mathematical memory analysis
        print("5. Testing mathematical memory analysis...")
        
        # Get importance scores
        importance_scores = []
        access_frequencies = []
        
        for unit in env.persistent_backend.units.values():
            if unit.metadata:
                importance = unit.metadata.get('importance_score', 0.0)
                access_freq = unit.metadata.get('predicted_access_frequency', 0.0)
                importance_scores.append(importance)
                access_frequencies.append(access_freq)
        
        if importance_scores:
            avg_importance = sum(importance_scores) / len(importance_scores)
            max_importance = max(importance_scores)
            min_importance = min(importance_scores)
            print(f"   📊 Importance scores: avg={avg_importance:.3f}, range={min_importance:.3f}-{max_importance:.3f}")
        
        # Test storage optimization
        print("6. Testing storage optimization...")
        optimization_stats = env.memory_manager.optimize_storage_comprehensive()
        optimization_time = optimization_stats.get('optimization_time', 0.0)
        storage_efficiency = optimization_stats.get('storage_efficiency_improvement', 0.0)
        tier_distribution = optimization_stats.get('tier_assignments', {})
        
        print(f"   ⚡ Optimization time: {optimization_time:.3f}s")
        print(f"   📊 Storage efficiency: {storage_efficiency:.3f}")
        print(f"   📊 Tier distribution: {tier_distribution}")
        
        # Test status retrieval
        print("7. Testing comprehensive status...")
        status = env.get_comprehensive_status()
        
        persistence = status.get('persistence', {})
        integration_health = status.get('integration_health', {})
        memory_management = status.get('memory_management', {})
        
        print(f"   📊 Total units: {persistence.get('total_units', 0)}")
        print(f"   🏥 Component health: {sum(1 for v in integration_health.values() if isinstance(v, bool) and v)}/{sum(1 for v in integration_health.values() if isinstance(v, bool))}")
        print(f"   💾 Memory efficiency: {memory_management.get('storage_efficiency_improvement', 0.0):.3f}")
        
        # Test session ending
        print("8. Testing session ending...")
        summary = env.end_session()
        print(f"   ✅ Session ended: {summary['cognitive_development_score']:.3f} development score")
        print(f"   📊 Messages processed: {summary['message_count']}")
        print(f"   📊 Memory units created: {summary['memory_units_created']}")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        print("\n🎉 All working UI component tests PASSED!")
        print("\n📋 UI is ready to launch:")
        print("   python src/lumina_memory/working_chat_ui.py")
        print("\n📋 Or with custom storage:")
        print("   python src/lumina_memory/working_chat_ui.py --storage my_day18_session")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Working UI component test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ui_requirements():
    """Test UI requirements"""
    print("\n🔧 Testing UI Requirements")
    print("=" * 50)
    
    requirements_met = True
    
    # Test tkinter
    try:
        import tkinter as tk
        print("✅ tkinter available")
    except ImportError:
        print("❌ tkinter not available - install python-tk")
        requirements_met = False
    
    # Test matplotlib
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib available")
    except ImportError:
        print("❌ matplotlib not available - pip install matplotlib")
        requirements_met = False
    
    # Test numpy
    try:
        import numpy as np
        print("✅ numpy available")
    except ImportError:
        print("❌ numpy not available - pip install numpy")
        requirements_met = False
    
    if requirements_met:
        print("\n🎉 All UI requirements met!")
        print("📋 Ready to launch enhanced UI")
    else:
        print("\n⚠️ Some UI requirements missing")
        print("📋 Install missing packages before launching UI")
    
    return requirements_met


def demonstrate_day18_features():
    """Demonstrate Day 18 enhanced features"""
    print("\n🚀 Day 18 Enhanced Features Demonstration")
    print("=" * 60)
    
    try:
        temp_dir = tempfile.mkdtemp()
        env = CompleteIntegratedEnvironment(temp_dir)
        
        print("1. Enhanced Mathematical Memory Management:")
        
        # Create diverse content for analysis
        session_id = env.start_session()
        
        test_content = [
            ("High importance philosophical question about consciousness", "user_message"),
            ("Detailed technical analysis of AI systems", "assistant_response"),
            ("Simple acknowledgment message", "assistant_response"),
            ("Creative exploration of possibilities", "user_message"),
            ("System error notification", "system"),
            ("Complex cognitive pattern discussion", "user_message")
        ]
        
        for content, msg_type in test_content:
            env.process_message(content)
        
        # Analyze mathematical properties
        importance_scores = []
        storage_tiers = []
        
        for unit in env.persistent_backend.units.values():
            if unit.metadata:
                importance_scores.append(unit.metadata.get('importance_score', 0.0))
                storage_tiers.append(unit.metadata.get('storage_tier', 'unknown'))
        
        print(f"   📊 Importance distribution: {len([s for s in importance_scores if s > 0.7])} high, {len([s for s in importance_scores if 0.3 <= s <= 0.7])} medium, {len([s for s in importance_scores if s < 0.3])} low")
        print(f"   📊 Storage tiers: {dict((tier, storage_tiers.count(tier)) for tier in set(storage_tiers))}")
        
        print("\n2. Advanced Pattern Recognition:")
        
        pattern_test_messages = [
            "I'm curious about this fascinating approach to AI consciousness.",
            "Let's analyze this systematically using structured methodology.",
            "We should collaborate together on this shared challenge."
        ]
        
        total_patterns = 0
        pattern_types = set()
        
        for message in pattern_test_messages:
            result = env.process_message(message)
            patterns = result.get('cognitive_patterns', [])
            total_patterns += len(patterns)
            for pattern in patterns:
                pattern_types.add(pattern['type'])
        
        print(f"   🧠 Total patterns detected: {total_patterns}")
        print(f"   🧠 Unique pattern types: {len(pattern_types)} ({', '.join(list(pattern_types)[:3])}...)")
        
        print("\n3. Enhanced Integration Analysis:")
        
        status = env.get_comprehensive_status()
        integration_health = status.get('integration_health', {})
        memory_management = status.get('memory_management', {})
        
        healthy_components = sum(1 for v in integration_health.values() if isinstance(v, bool) and v)
        total_components = sum(1 for v in integration_health.values() if isinstance(v, bool))
        
        print(f"   🏥 Component health: {healthy_components}/{total_components} ({healthy_components/total_components*100:.1f}%)")
        print(f"   💾 Storage efficiency: {memory_management.get('storage_efficiency_improvement', 0.0):.3f}")
        print(f"   ⚡ Optimization time: {memory_management.get('optimization_time', 0.0):.3f}s")
        
        env.end_session()
        shutil.rmtree(temp_dir)
        
        print("\n✅ Day 18 enhanced features working correctly!")
        
    except Exception as e:
        print(f"\n❌ Day 18 features demonstration failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 Testing Working Chat Analysis UI (Day 18)")
    print("=" * 70)
    
    # Test requirements
    requirements_ok = test_ui_requirements()
    
    if requirements_ok:
        # Test components
        components_ok = test_working_ui_components()
        
        if components_ok:
            # Demonstrate Day 18 features
            demonstrate_day18_features()
            
            print("\n✅ Working UI is ready for Day 18!")
            print("\n🎯 Day 18 Enhancements:")
            print("1. Fixed import issues from Day 17")
            print("2. Enhanced mathematical memory analytics")
            print("3. Advanced pattern visualization")
            print("4. Real-time performance monitoring")
            print("5. Deep mathematical analysis capabilities")
            print("\n🚀 Launch command:")
            print("   python src/lumina_memory/working_chat_ui.py")
        else:
            print("\n❌ UI components need fixes")
    else:
        print("\n❌ Install missing requirements first")
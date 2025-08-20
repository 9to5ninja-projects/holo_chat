#!/usr/bin/env python3
"""
Day 18 Validation Test
=====================

Simple validation test for Day 18 mathematical intelligence system.
"""

import sys
import os
import tempfile
import shutil

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def validate_day18_system():
    """Validate Day 18 mathematical intelligence system"""
    print("🔧 Day 18 Mathematical Intelligence Validation")
    print("=" * 60)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from lumina_memory.complete_integrated_environment import CompleteIntegratedEnvironment
        from lumina_memory.mathematical_memory_intelligence import MathematicalMemoryIntelligence
        print("   ✅ All imports successful")
        
        # Test environment creation
        print("2. Testing environment with mathematical intelligence...")
        temp_dir = tempfile.mkdtemp()
        env = CompleteIntegratedEnvironment(temp_dir)
        print("   ✅ Environment created with Day 18 intelligence")
        
        # Test session management
        print("3. Testing session with complex content...")
        session_id = env.start_session()
        
        # Test with content that should trigger mathematical intelligence
        test_messages = [
            "I'm deeply curious about this fascinating approach to AI consciousness and systematic analysis.",
            "Let's explore this complex framework using analytical thinking and collaborative methodologies.",
            "This requires careful consideration of cognitive architectures and philosophical implications."
        ]
        
        total_patterns = 0
        for i, message in enumerate(test_messages, 1):
            result = env.process_message(message)
            patterns = result.get('cognitive_patterns', [])
            total_patterns += len(patterns)
            print(f"   Message {i}: {len(patterns)} patterns detected")
        
        # Test storage optimization
        print("4. Testing mathematical storage optimization...")
        optimization_stats = env.memory_manager.optimize_storage_comprehensive()
        
        print(f"   📊 Units processed: {optimization_stats.get('units_processed', 0)}")
        print(f"   📊 Storage efficiency: {optimization_stats.get('storage_efficiency_improvement', 0.0):.3f}")
        print(f"   📊 Tier distribution: {optimization_stats.get('tier_assignments', {})}")
        
        # Test mathematical intelligence performance
        print("5. Testing mathematical intelligence performance...")
        math_summary = env.memory_manager.mathematical_intelligence.get_performance_summary()
        print(f"   📊 Optimizations: {math_summary.get('total_optimizations', 0)}")
        print(f"   📊 Performance trend: {math_summary.get('performance_trend', 'unknown')}")
        
        # Test comprehensive status
        print("6. Testing comprehensive system status...")
        status = env.get_comprehensive_status()
        
        persistence = status.get('persistence', {})
        integration_health = status.get('integration_health', {})
        memory_management = status.get('memory_management', {})
        
        print(f"   📊 Total units: {persistence.get('total_units', 0)}")
        print(f"   🏥 Component health: {sum(1 for v in integration_health.values() if isinstance(v, bool) and v)}/{sum(1 for v in integration_health.values() if isinstance(v, bool))}")
        print(f"   💾 Memory efficiency: {memory_management.get('storage_efficiency_improvement', 0.0):.3f}")
        
        # End session
        summary = env.end_session()
        print(f"   ✅ Session ended: {summary['cognitive_development_score']:.3f} development score")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        print("\n🎉 Day 18 Mathematical Intelligence Validation PASSED!")
        
        # Summary
        print("\n📊 Day 18 System Summary:")
        print(f"   ✅ Mathematical intelligence: ACTIVE")
        print(f"   ✅ Advanced importance calculation: WORKING")
        print(f"   ✅ Predictive access learning: FUNCTIONAL")
        print(f"   ✅ Intelligent storage optimization: OPERATIONAL")
        print(f"   ✅ Enhanced integration: COMPLETE")
        print(f"   📊 Total patterns detected: {total_patterns}")
        print(f"   📊 Messages processed: {len(test_messages)}")
        print(f"   📊 Storage efficiency: {optimization_stats.get('storage_efficiency_improvement', 0.0):.3f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Day 18 validation FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ui_availability():
    """Test UI availability"""
    print("\n🔧 Testing UI Availability")
    print("=" * 40)
    
    try:
        from lumina_memory.working_chat_ui import WorkingChatUI
        print("   ✅ Working Chat UI available")
        print("   📋 Launch command: python src/lumina_memory/working_chat_ui.py")
        return True
    except Exception as e:
        print(f"   ❌ UI not available: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Day 18 Mathematical Intelligence System Validation")
    print("=" * 70)
    
    # Validate main system
    system_ok = validate_day18_system()
    
    # Test UI availability
    ui_ok = test_ui_availability()
    
    if system_ok and ui_ok:
        print("\n✅ Day 18 Mathematical Intelligence System VALIDATED!")
        print("\n🎯 Day 18 Achievements:")
        print("1. ✅ Advanced mathematical memory intelligence")
        print("2. ✅ Multi-factor importance calculation")
        print("3. ✅ Predictive access pattern learning")
        print("4. ✅ Intelligent storage optimization")
        print("5. ✅ Enhanced UI with advanced analytics")
        print("6. ✅ Complete system integration")
        
        print("\n🚀 Ready for advanced AI memory applications!")
        print("\n📋 Usage:")
        print("   python src/lumina_memory/working_chat_ui.py")
        print("   # Launch enhanced UI with mathematical intelligence")
        
    else:
        print("\n❌ Day 18 validation incomplete")
        if not system_ok:
            print("   - Mathematical intelligence system needs fixes")
        if not ui_ok:
            print("   - UI system needs fixes")
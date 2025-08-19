#!/usr/bin/env python3
"""
Complete System Validation Script
=================================

This script validates the entire Holographic Memory System with Emotion Engine
to ensure all components are working correctly before deployment.
"""

import sys
import traceback
from pathlib import Path

def validate_imports():
    """Validate all required imports"""
    print("🔍 Validating imports...")
    
    try:
        # Core emotion engine
        from src.lumina_memory.emotion_engine import EnhancedXPEnvironment, EmotionEngine
        from src.lumina_memory.chat_assistant import ChatAssistant
        from src.lumina_memory.advanced_xpunit import AdvancedXPUnit, AffectState
        from src.lumina_memory.advanced_xp_environment import AdvancedXPEnvironment
        
        print("✅ All core imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def validate_emotion_engine():
    """Validate emotion engine functionality"""
    print("\n🎭 Validating emotion engine...")
    
    try:
        from src.lumina_memory.emotion_engine import EnhancedXPEnvironment
        
        # Create environment
        env = EnhancedXPEnvironment(dimension=256)
        
        # Test mood synthesis
        affect_delta = {"valence": 0.5, "arousal": 0.3, "dominance": 0.2}
        mood = env.update_affect_and_mood(affect_delta)
        
        assert "valence" in mood
        assert "arousal" in mood
        assert "dominance" in mood
        
        print("✅ Emotion engine working correctly")
        return True
    except Exception as e:
        print(f"❌ Emotion engine failed: {e}")
        traceback.print_exc()
        return False

def validate_chat_assistant():
    """Validate chat assistant functionality"""
    print("\n💬 Validating chat assistant...")
    
    try:
        from src.lumina_memory.chat_assistant import ChatAssistant
        
        # Initialize assistant
        assistant = ChatAssistant()
        
        # Start session
        session_id = assistant.start_session("ValidationUser")
        assert session_id is not None
        
        # Test chat
        result = assistant.chat("Hello, this is a validation test.")
        assert result["ok"] == True
        assert "response" in result
        assert "mood" in result
        
        # End session
        summary = assistant.end_session()
        assert "total_messages" in summary
        
        print("✅ Chat assistant working correctly")
        return True
    except Exception as e:
        print(f"❌ Chat assistant failed: {e}")
        traceback.print_exc()
        return False

def validate_memory_system():
    """Validate memory system functionality"""
    print("\n🧠 Validating memory system...")
    
    try:
        from src.lumina_memory.advanced_xpunit import AdvancedXPUnit, AffectState
        from src.lumina_memory.advanced_xp_environment import AdvancedXPEnvironment
        
        # Create XPUnit
        affect = AffectState(valence=0.3, arousal=0.2)
        xpunit = AdvancedXPUnit(
            content_id="validation_test",
            content="This is a validation test for the memory system",
            affect=affect
        )
        
        # Create environment and add XPUnit
        env = AdvancedXPEnvironment(dimension=256)
        env.xpunits[xpunit.content_id] = xpunit
        
        assert len(env.xpunits) == 1
        assert xpunit.content_id in env.xpunits
        
        print("✅ Memory system working correctly")
        return True
    except Exception as e:
        print(f"❌ Memory system failed: {e}")
        traceback.print_exc()
        return False

def validate_policies():
    """Validate policy loading"""
    print("\n📋 Validating policy system...")
    
    try:
        import yaml
        from src.lumina_memory.emotion_engine import EmotionEngine
        
        # Test policy content
        test_policies = {
            "mood": {"alpha": 0.6, "beta": 0.4},
            "filters": {
                "ethics": {"deny_topics": ["test"]},
                "bias": {"tone": {"empathetic": 0.7}}
            }
        }
        
        # Create engine and update policies
        from src.lumina_memory.emotion_engine import EnhancedXPEnvironment
        env = EnhancedXPEnvironment()
        engine = env.emotion_engine
        engine.update_policies(test_policies)
        
        assert engine.policies["mood"]["alpha"] == 0.6
        assert "empathetic" in engine.policies["filters"]["bias"]["tone"]
        
        print("✅ Policy system working correctly")
        return True
    except Exception as e:
        print(f"❌ Policy system failed: {e}")
        traceback.print_exc()
        return False

def validate_30_day_program():
    """Validate 30-day program framework"""
    print("\n📅 Validating 30-day program...")
    
    try:
        # Import the program module
        import importlib.util
        spec = importlib.util.spec_from_file_location("thirty_day_program", "30_day_program.py")
        program_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(program_module)
        
        # Create program instance
        program = program_module.ThirtyDayProgram()
        
        assert program.current_day >= 1
        assert program.current_day <= 30
        assert len(program.daily_themes) == 30
        
        print("✅ 30-day program working correctly")
        return True
    except Exception as e:
        print(f"❌ 30-day program failed: {e}")
        traceback.print_exc()
        return False

def validate_file_structure():
    """Validate file structure"""
    print("\n📁 Validating file structure...")
    
    required_files = [
        "src/lumina_memory/emotion_engine.py",
        "src/lumina_memory/chat_assistant.py",
        "src/lumina_memory/advanced_xpunit.py",
        "src/lumina_memory/advanced_xp_environment.py",
        "src/extension.ts",
        "src/chatPanel.ts",
        "python/engine.py",
        "30_day_program.py",
        "policies.yml",
        "README.md",
        "EMOTION_ENGINE_README.md",
        "REBUILD_GUIDE.md",
        "USAGE_GUIDE.md",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def validate_dependencies():
    """Validate required dependencies"""
    print("\n📦 Validating dependencies...")
    
    required_packages = ["numpy", "scipy", "sklearn", "yaml"]
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "sklearn":
                import sklearn
            elif package == "yaml":
                import yaml
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    else:
        print("✅ All required dependencies available")
        return True

def main():
    """Run complete system validation"""
    print("🚀 Holographic Memory System - Complete Validation")
    print("=" * 60)
    
    validations = [
        ("Dependencies", validate_dependencies),
        ("File Structure", validate_file_structure),
        ("Imports", validate_imports),
        ("Emotion Engine", validate_emotion_engine),
        ("Memory System", validate_memory_system),
        ("Chat Assistant", validate_chat_assistant),
        ("Policy System", validate_policies),
        ("30-Day Program", validate_30_day_program)
    ]
    
    results = []
    for name, validation_func in validations:
        try:
            success = validation_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ {name} validation crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {name}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} validations passed")
    
    if passed == total:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("System is ready for deployment and use.")
        print("\nNext steps:")
        print("1. Commit all changes to repository")
        print("2. Start using the chat assistant")
        print("3. Begin the 30-day consciousness development program")
        return True
    else:
        print(f"\n❌ {total - passed} validations failed.")
        print("Please fix the issues above before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
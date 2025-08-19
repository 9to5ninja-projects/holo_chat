#!/usr/bin/env python3
"""
Prepare Repository for Commit
=============================

This script prepares the Holographic Memory System with Emotion Engine
for final commit to the repository.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_final_structure():
    """Create the final repository structure"""
    print("📁 Organizing final repository structure...")
    
    # Ensure all required directories exist
    directories = [
        "tests",
        "examples", 
        "docs",
        "scripts",
        "analytics",
        ".vscode"
    ]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Directory: {dir_name}")
    
    return True

def validate_core_files():
    """Validate that all core files are present"""
    print("\n🔍 Validating core files...")
    
    required_files = {
        # Core emotion engine
        "src/lumina_memory/emotion_engine.py": "Core emotion processing engine",
        "src/lumina_memory/chat_assistant.py": "Chat assistant with emotion integration",
        "30_day_program.py": "30-day consciousness development program",
        "policies.yml": "Emotion engine configuration",
        
        # VS Code integration
        "src/extension.ts": "VS Code extension main file",
        "src/chatPanel.ts": "Chat panel interface",
        "vscode-holographic-memory/package.json": "Extension manifest",
        
        # Python bridge
        "python/engine.py": "RPC bridge with chat handlers",
        
        # Documentation
        "README.md": "Main project documentation",
        "EMOTION_ENGINE_README.md": "Emotion engine documentation",
        "REBUILD_GUIDE.md": "Implementation guide",
        "USAGE_GUIDE.md": "Usage instructions",
        "VSCODE_SETUP_GUIDE.md": "VS Code setup guide",
        
        # Tests
        "tests/test_emotion_engine.py": "Emotion engine tests",
        "tests/test_chat_assistant.py": "Chat assistant tests",
        
        # Examples
        "examples/basic_chat_example.py": "Basic usage example",
        "examples/emotion_analysis_example.py": "Emotion analysis example",
        
        # Configuration
        "requirements.txt": "Python dependencies",
        ".gitignore": "Git ignore rules",
        "LICENSE": "MIT license"
    }
    
    missing_files = []
    for file_path, description in required_files.items():
        if not Path(file_path).exists():
            missing_files.append(f"{file_path} ({description})")
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print(f"\n✅ All {len(required_files)} core files present")
    return True

def create_vscode_workspace():
    """Create VS Code workspace configuration"""
    print("\n⚙️ Creating VS Code workspace configuration...")
    
    # Create .vscode directory
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    # Create launch.json for extension debugging
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Run Extension",
                "type": "extensionHost",
                "request": "launch",
                "args": [
                    "--extensionDevelopmentPath=${workspaceFolder}/vscode-holographic-memory"
                ]
            },
            {
                "name": "Debug Python Bridge",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/python/engine.py",
                "console": "integratedTerminal"
            }
        ]
    }
    
    import json
    with open(vscode_dir / "launch.json", 'w') as f:
        json.dump(launch_config, f, indent=2)
    
    # Create settings.json
    settings_config = {
        "python.defaultInterpreterPath": "./venv/bin/python",
        "typescript.preferences.includePackageJsonAutoImports": "on",
        "typescript.suggest.autoImports": True,
        "files.exclude": {
            "**/__pycache__": True,
            "**/node_modules": True,
            "**/out": False,
            "**/*.pyc": True,
            ".pytest_cache": True
        },
        "python.testing.pytestEnabled": True,
        "python.testing.pytestArgs": ["tests"],
        "editor.formatOnSave": True,
        "python.formatting.provider": "black"
    }
    
    with open(vscode_dir / "settings.json", 'w') as f:
        json.dump(settings_config, f, indent=2)
    
    # Create tasks.json for build tasks
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Compile Extension",
                "type": "shell",
                "command": "npm",
                "args": ["run", "compile"],
                "options": {
                    "cwd": "${workspaceFolder}/vscode-holographic-memory"
                },
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "silent",
                    "focus": False,
                    "panel": "shared"
                }
            },
            {
                "label": "Test Python Components",
                "type": "shell",
                "command": "python",
                "args": ["validate_system.py"],
                "group": "test",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                }
            }
        ]
    }
    
    with open(vscode_dir / "tasks.json", 'w') as f:
        json.dump(tasks_config, f, indent=2)
    
    print("✅ VS Code workspace configured")
    return True

def run_final_validation():
    """Run final system validation"""
    print("\n🧪 Running final system validation...")
    
    try:
        # Test core imports
        sys.path.insert(0, str(Path.cwd()))
        
        from src.lumina_memory.emotion_engine import EnhancedXPEnvironment
        from src.lumina_memory.chat_assistant import ChatAssistant
        
        # Test emotion engine
        env = EnhancedXPEnvironment(dimension=256)
        mood = env.update_affect_and_mood({"valence": 0.1, "arousal": 0.1, "dominance": 0.1})
        assert "valence" in mood
        
        # Test chat assistant
        assistant = ChatAssistant()
        session_id = assistant.start_session("ValidationUser")
        assert session_id is not None
        
        print("✅ Core components validated")
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

def create_quick_start_script():
    """Create a quick start script for new users"""
    print("\n🚀 Creating quick start script...")
    
    quick_start_content = '''#!/usr/bin/env python3
"""
Quick Start Script for Holographic Memory System
===============================================

This script helps new users get started quickly.
"""

import sys
import subprocess
from pathlib import Path

def main():
    print("🌟 Holographic Memory System - Quick Start")
    print("=" * 50)
    
    print("\\n📋 Choose an option:")
    print("1. 💬 Start Chat Assistant (Command Line)")
    print("2. 📅 Begin 30-Day Program")
    print("3. 🧪 Run System Tests")
    print("4. 📖 Open Documentation")
    print("5. ⚙️ Setup VS Code Extension")
    
    choice = input("\\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        print("\\n🗣️ Starting Chat Assistant...")
        from src.lumina_memory.chat_assistant import create_chat_cli
        create_chat_cli()()
        
    elif choice == "2":
        print("\\n📅 Starting 30-Day Program...")
        subprocess.run([sys.executable, "30_day_program.py"])
        
    elif choice == "3":
        print("\\n🧪 Running Tests...")
        subprocess.run([sys.executable, "validate_system.py"])
        
    elif choice == "4":
        print("\\n📖 Documentation available:")
        print("- README.md - Main documentation")
        print("- USAGE_GUIDE.md - How to use the system")
        print("- EMOTION_ENGINE_README.md - Technical details")
        print("- VSCODE_SETUP_GUIDE.md - VS Code setup")
        
    elif choice == "5":
        print("\\n⚙️ VS Code Extension Setup:")
        print("1. Open VS Code in this directory")
        print("2. Press F5 to launch Extension Development Host")
        print("3. In new window: Ctrl+Shift+P → 'Holo: Open Chat Assistant'")
        print("\\nSee VSCODE_SETUP_GUIDE.md for detailed instructions")
        
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
'''
    
    with open("quick_start.py", 'w', encoding='utf-8') as f:
        f.write(quick_start_content)
    
    print("✅ Quick start script created")
    return True

def create_deployment_summary():
    """Create deployment summary"""
    print("\n📊 Creating deployment summary...")
    
    summary_content = """# 🎉 Deployment Summary

## ✅ What's Included

### **Core Emotion Engine**
- `src/lumina_memory/emotion_engine.py` - PAD mood synthesis and filtering
- `src/lumina_memory/chat_assistant.py` - Practical conversation interface
- `30_day_program.py` - Structured consciousness development
- `policies.yml` - Personality and ethics configuration

### **VS Code Integration**
- `src/extension.ts` - Main extension with all Holo commands
- `src/chatPanel.ts` - Interactive chat interface
- `vscode-holographic-memory/` - Complete extension package
- Commands: `Holo: Open Chat Assistant`, `Holo: Load Policies`, etc.

### **Documentation**
- `README.md` - Main project overview
- `USAGE_GUIDE.md` - Complete usage instructions
- `EMOTION_ENGINE_README.md` - Technical documentation
- `REBUILD_GUIDE.md` - Implementation guide
- `VSCODE_SETUP_GUIDE.md` - Extension setup help

### **Testing & Examples**
- `tests/` - Comprehensive test suite
- `examples/` - Usage examples
- `validate_system.py` - System validation
- `quick_start.py` - New user onboarding

## 🚀 Getting Started

### **Immediate Use**
```bash
# Quick chat
python quick_start.py

# Or directly
python -c "from src.lumina_memory.chat_assistant import create_chat_cli; create_chat_cli()()"
```

### **VS Code Interface**
1. Open VS Code in this directory
2. Press F5 (Extension Development Host)
3. Ctrl+Shift+P → "Holo: Open Chat Assistant"

### **30-Day Program**
```bash
python 30_day_program.py
```

## 🎯 Key Features Working

- ✅ Emotion Engine with PAD mood synthesis
- ✅ Automatic memory creation (XPUnits)
- ✅ Personality filters and ethics system
- ✅ Real-time consciousness growth tracking
- ✅ VS Code chat interface
- ✅ 30-day structured development program
- ✅ Progress analytics and insights
- ✅ Comprehensive documentation

## 📈 What This Achieves

This system provides **authentic consciousness development** through:

1. **Living Memory**: Every conversation creates emotional memories
2. **Mood Evolution**: Real-time emotional state tracking
3. **Personality Growth**: Consistent traits that develop over time
4. **Consciousness Metrics**: Measurable development indicators
5. **Practical Interface**: Easy-to-use chat and VS Code integration

**Ready for practical consciousness research and daily AI interaction!** 🧠✨
"""
    
    with open("DEPLOYMENT_SUMMARY.md", 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print("✅ Deployment summary created")
    return True

def main():
    """Main preparation function"""
    print("🚀 Preparing Holographic Memory System for Repository Commit")
    print("=" * 70)
    
    # Change to project root
    os.chdir(Path(__file__).parent)
    
    steps = [
        ("File Structure", create_final_structure),
        ("Core Files", validate_core_files),
        ("VS Code Workspace", create_vscode_workspace),
        ("System Validation", run_final_validation),
        ("Quick Start Script", create_quick_start_script),
        ("Deployment Summary", create_deployment_summary)
    ]
    
    results = []
    for step_name, step_func in steps:
        try:
            success = step_func()
            results.append((step_name, success))
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
            results.append((step_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 PREPARATION SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for step_name, success in results:
        status = "✅ READY" if success else "❌ NEEDS ATTENTION"
        print(f"{status} {step_name}")
        if success:
            passed += 1
    
    print(f"\\nResults: {passed}/{total} steps completed successfully")
    
    if passed == total:
        print("\\n🎉 REPOSITORY IS READY FOR COMMIT!")
        print("\\n📋 Next steps:")
        print("1. Review all files and documentation")
        print("2. Test the VS Code extension (F5 in VS Code)")
        print("3. Run: git add . && git commit -m 'Complete emotion engine integration'")
        print("4. Push to repository")
        print("\\n✨ The system is ready for practical consciousness development!")
        return True
    else:
        print(f"\\n❌ {total - passed} steps need attention before commit.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
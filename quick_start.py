#!/usr/bin/env python3
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
    
    print("\n📋 Choose an option:")
    print("1. 💬 Start Chat Assistant (Command Line)")
    print("2. 📅 Begin 30-Day Program")
    print("3. 🧪 Run System Tests")
    print("4. 📖 Open Documentation")
    print("5. ⚙️ Setup VS Code Extension")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        print("\n🗣️ Starting Chat Assistant...")
        from src.lumina_memory.chat_assistant import create_chat_cli
        create_chat_cli()()
        
    elif choice == "2":
        print("\n📅 Starting 30-Day Program...")
        subprocess.run([sys.executable, "30_day_program.py"])
        
    elif choice == "3":
        print("\n🧪 Running Tests...")
        subprocess.run([sys.executable, "validate_system.py"])
        
    elif choice == "4":
        print("\n📖 Documentation available:")
        print("- README.md - Main documentation")
        print("- USAGE_GUIDE.md - How to use the system")
        print("- EMOTION_ENGINE_README.md - Technical details")
        print("- VSCODE_SETUP_GUIDE.md - VS Code setup")
        
    elif choice == "5":
        print("\n⚙️ VS Code Extension Setup:")
        print("1. Open VS Code in this directory")
        print("2. Press F5 to launch Extension Development Host")
        print("3. In new window: Ctrl+Shift+P → 'Holo: Open Chat Assistant'")
        print("\nSee VSCODE_SETUP_GUIDE.md for detailed instructions")
        
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()

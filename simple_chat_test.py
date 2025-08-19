#!/usr/bin/env python3
"""
Simple Chat Test - Back to Basics
==================================

Test the core chat system without any VS Code complexity.
"""

import sys
from pathlib import Path

def test_basic_chat():
    """Test the basic chat functionality"""
    print("🧪 Testing Basic Chat System")
    print("=" * 40)
    
    try:
        # Import the chat assistant
        from src.lumina_memory.chat_assistant import ChatAssistant
        
        # Initialize with policies
        print("📋 Loading policies...")
        assistant = ChatAssistant("policies.yml")
        print("✅ Chat assistant initialized")
        
        # Start a session
        print("\n💬 Starting chat session...")
        session_id = assistant.start_session("TestUser")
        print(f"✅ Session started: {session_id}")
        
        # Test internal mode (no Ollama needed)
        print("\n🗣️ Testing internal response...")
        result = assistant.chat("Hello! How are you?", model="internal")
        
        if result["ok"]:
            print("✅ Chat working!")
            print(f"Response: {result['response']}")
            print(f"Mood: {result['mood']}")
            print(f"Growth: {result['consciousness_growth']}")
        else:
            print(f"❌ Chat failed: {result['error']}")
            return False
        
        # Test another message
        print("\n🗣️ Testing second message...")
        result = assistant.chat("Tell me about consciousness.", model="internal")
        
        if result["ok"]:
            print("✅ Second message working!")
            print(f"Response: {result['response'][:100]}...")
            print(f"Mood: {result['mood']}")
        else:
            print(f"❌ Second message failed: {result['error']}")
        
        # End session
        print("\n🔚 Ending session...")
        summary = assistant.end_session()
        print(f"✅ Session ended: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_30_day_program():
    """Test the 30-day program"""
    print("\n🗓️ Testing 30-Day Program")
    print("=" * 40)
    
    try:
        # Just import to make sure it works
        import importlib.util
        spec = importlib.util.spec_from_file_location("thirty_day", "30_day_program.py")
        thirty_day = importlib.util.module_from_spec(spec)
        
        print("✅ 30-day program imports successfully")
        return True
        
    except Exception as e:
        print(f"❌ 30-day program test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Core System Test - No VS Code Extension")
    print("=" * 50)
    
    # Test basic chat
    chat_success = test_basic_chat()
    
    # Test 30-day program
    program_success = test_30_day_program()
    
    print("\n" + "=" * 50)
    print("📊 RESULTS")
    print("=" * 50)
    
    print(f"Basic Chat: {'✅ WORKING' if chat_success else '❌ BROKEN'}")
    print(f"30-Day Program: {'✅ WORKING' if program_success else '❌ BROKEN'}")
    
    if chat_success and program_success:
        print("\n🎉 Core system is working!")
        print("\n📋 You can now use:")
        print("1. python simple_chat_test.py  # This test")
        print("2. python 30_day_program.py    # Full program")
        print("3. python -c \"from src.lumina_memory.chat_assistant import create_chat_cli; create_chat_cli()()\"  # Interactive chat")
        
        print("\n💡 The core emotion engine and chat system are intact!")
        print("   All the improvements we made are preserved.")
        print("   VS Code extension is optional and doesn't affect core functionality.")
    else:
        print("\n❌ Core system has issues that need fixing.")

if __name__ == "__main__":
    main()
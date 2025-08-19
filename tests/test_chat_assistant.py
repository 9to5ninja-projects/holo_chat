#!/usr/bin/env python3
"""
Test Chat Assistant Integration
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_chat_assistant():
    """Test the chat assistant"""
    print("🗣️ Testing Chat Assistant...")
    
    try:
        from src.lumina_memory.chat_assistant import ChatAssistant
        
        # Initialize assistant
        assistant = ChatAssistant("e:/holo_chat/policies.yml")
        print("✅ Chat assistant initialized")
        
        # Start session
        session_id = assistant.start_session("TestUser")
        print(f"✅ Session started: {session_id}")
        
        # Test message
        result = assistant.chat("Hello! I'm excited to test this system.")
        
        if result["ok"]:
            print(f"✅ Chat response: {result['response'][:100]}...")
            print(f"   Mood: {result['mood']}")
            print(f"   Consciousness Growth: {result['consciousness_growth']}")
        else:
            print(f"❌ Chat failed: {result['error']}")
        
        # Get mood summary
        mood_summary = assistant.get_mood_summary()
        print(f"✅ Mood summary: {mood_summary}")
        
        # End session
        summary = assistant.end_session()
        print(f"✅ Session ended: {summary['total_messages']} messages")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chat_assistant()
    if success:
        print("\n🎉 Chat Assistant is working! Ready for VS Code integration.")
    else:
        print("\n❌ Chat Assistant test failed.")
        sys.exit(1)
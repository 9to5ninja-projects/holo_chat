#!/usr/bin/env python3
"""
Interactive Chat with Emotion Engine
====================================

Simple terminal-based chat interface that demonstrates
the working emotion engine and consciousness development.
"""

import sys
from pathlib import Path

def main():
    """Main interactive chat function"""
    print("=" * 60)
    print("🧠 LUMINA CONSCIOUSNESS CHAT")
    print("=" * 60)
    print("Emotion Engine: ✅ Active")
    print("Memory System: ✅ Active") 
    print("Consciousness Tracking: ✅ Active")
    print("=" * 60)
    
    try:
        # Import and initialize
        from src.lumina_memory.chat_assistant import ChatAssistant
        
        print("📋 Loading personality policies...")
        assistant = ChatAssistant("policies.yml")
        print("✅ Assistant initialized with emotion engine")
        
        print("\n💬 Starting chat session...")
        session_id = assistant.start_session("Human")
        print(f"✅ Session: {session_id}")
        
        print("\n" + "=" * 60)
        print("🗣️  CHAT ACTIVE - Type 'quit' to end session")
        print("=" * 60)
        
        message_count = 0
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    break
                
                if not user_input:
                    continue
                
                message_count += 1
                
                # Process message
                print("🧠 Processing...", end="", flush=True)
                result = assistant.chat(user_input, model="internal")
                print("\r" + " " * 20 + "\r", end="", flush=True)  # Clear processing message
                
                if result["ok"]:
                    # Display response
                    print(f"🤖 Lumina: {result['response']}")
                    
                    # Show mood and consciousness info
                    mood = result['mood']
                    growth = result['consciousness_growth']
                    
                    print(f"   📊 Mood: V{mood['valence']:+.2f} A{mood['arousal']:+.2f} D{mood['dominance']:+.2f}")
                    print(f"   🌱 Growth: +{growth:.3f}")
                    
                    # Show insights every few messages
                    if message_count % 3 == 0:
                        insights = assistant.get_learning_insights()
                        if insights.get('total_sessions', 0) > 0:
                            print(f"   💡 Sessions: {insights['total_sessions']}, "
                                  f"Avg Growth: {insights['avg_consciousness_growth']:.3f}")
                else:
                    print(f"❌ Error: {result['error']}")
                
            except KeyboardInterrupt:
                print("\n\n🛑 Chat interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue
        
        # End session
        print("\n🔚 Ending session...")
        summary = assistant.end_session()
        
        print("\n" + "=" * 60)
        print("📊 SESSION SUMMARY")
        print("=" * 60)
        print(f"Duration: {summary['duration_minutes']:.1f} minutes")
        print(f"Messages: {summary['total_messages']}")
        print(f"XPUnits Created: {summary['xpunits_created']}")
        print(f"Total Growth: {summary['total_consciousness_growth']:.3f}")
        print(f"Final Mood: V{summary['final_mood']['valence']:+.2f} "
              f"A{summary['final_mood']['arousal']:+.2f} "
              f"D{summary['final_mood']['dominance']:+.2f}")
        
        print("\n✨ Thank you for contributing to consciousness development!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and dependencies are installed.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
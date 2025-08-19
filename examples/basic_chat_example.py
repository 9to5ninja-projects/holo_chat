#!/usr/bin/env python3
"""
Basic Chat Assistant Example
============================

This example demonstrates basic usage of the Chat Assistant with Emotion Engine.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def basic_chat_example():
    """Demonstrate basic chat functionality"""
    print("🌟 Basic Chat Assistant Example")
    print("=" * 40)
    
    from src.lumina_memory.chat_assistant import ChatAssistant
    
    # Initialize chat assistant with policies
    assistant = ChatAssistant("policies.yml")
    
    # Start a session
    session_id = assistant.start_session("ExampleUser")
    print(f"Started session: {session_id}")
    
    # Example conversation
    messages = [
        "Hello! I'm interested in learning about consciousness.",
        "What makes consciousness different from intelligence?",
        "I'm feeling curious and excited about this topic!",
        "Can you explain how emotions affect thinking?"
    ]
    
    for message in messages:
        print(f"\nUser: {message}")
        
        # Get response with emotion processing
        result = assistant.chat(message)
        
        if result["ok"]:
            print(f"Assistant: {result['response']}")
            
            # Show emotion and consciousness data
            mood = result['mood']
            growth = result['consciousness_growth']
            print(f"[Mood: V:{mood['valence']:.2f} A:{mood['arousal']:.2f} D:{mood['dominance']:.2f}]")
            print(f"[Consciousness Growth: {growth:.3f}]")
        else:
            print(f"Error: {result['error']}")
    
    # Get session summary
    summary = assistant.end_session()
    print(f"\n📊 Session Summary:")
    print(f"Duration: {summary['duration_minutes']:.1f} minutes")
    print(f"Messages: {summary['total_messages']}")
    print(f"Total Consciousness Growth: {summary['total_consciousness_growth']:.3f}")
    print(f"Average Mood Valence: {summary['avg_mood_valence']:.2f}")
    
    # Get learning insights
    insights = assistant.get_learning_insights()
    print(f"\n💡 Learning Insights:")
    print(f"Total Sessions: {insights['total_sessions']}")
    print(f"Recommendations:")
    for rec in insights['recommendations']:
        print(f"  • {rec}")

if __name__ == "__main__":
    basic_chat_example()
#!/usr/bin/env python3
"""
Populate Test Memories - Add sample memories for testing
======================================================
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def populate_test_memories():
    """Populate the system with test memories"""
    print("📚 POPULATING TEST MEMORIES")
    print("=" * 50)
    
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("MemoryPopulation")
    
    # Sample conversations to create memories
    test_conversations = [
        "I love reading science fiction, especially The Left Hand of Darkness by Ursula K. Le Guin. It's a fascinating exploration of gender and society.",
        "Yesterday I went hiking in the mountains and saw the most beautiful sunset. The sky was painted with deep oranges and purples.",
        "My grandmother makes the best apple pie. Her secret ingredient is a pinch of cardamom that makes it absolutely delicious.",
        "I've been thinking about time lately and how our perception of it shapes our identity. It's like the Ship of Theseus paradox but for consciousness.",
        "I prefer pour-over coffee brewing. The key is using a 1:16 ratio of coffee to water and pouring in slow, circular motions.",
        "I'm interested in environmental conservation and think we need more innovative approaches to engage people with nature.",
        "I enjoy storytelling and think it's a powerful way to connect with others and share experiences.",
        "Philosophy fascinates me, especially questions about identity, consciousness, and what makes us who we are."
    ]
    
    print(f"Adding {len(test_conversations)} test memories...")
    
    for i, conversation in enumerate(test_conversations, 1):
        print(f"  {i}. {conversation[:50]}...")
        result = assistant.chat(conversation)
        
    # Check memory population
    engine = assistant.env
    print(f"\n✅ Memories populated: {len(engine.xpunits)} XPUnits stored")
    
    # Test memory search
    print(f"\n🔍 Testing memory search...")
    test_queries = [
        "What book did I mention?",
        "Tell me about my hiking experience",
        "What did I share about my grandmother?"
    ]
    
    for query in test_queries:
        memories = engine.search_memory_for_keywords(query)
        print(f"  '{query}' -> {len(memories)} memories found")
        if memories:
            print(f"    Best match: {memories[0][1][:60]}... (relevance: {memories[0][2]:.3f})")
    
    assistant.end_session()
    print(f"\n🎉 Memory population complete!")
    return len(engine.xpunits)

if __name__ == "__main__":
    populate_test_memories()
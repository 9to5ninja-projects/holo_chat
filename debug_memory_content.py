#!/usr/bin/env python3
"""
Debug Memory Content - See what's actually stored
================================================
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def debug_memory_content():
    """Debug what's actually stored in memory"""
    print("🔍 DEBUGGING MEMORY CONTENT")
    print("=" * 50)
    
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("DebugMemory")
    
    # Check if there are any stored memories
    engine = assistant.env
    
    print(f"Total XPUnits stored: {len(engine.xpunits)}")
    print(f"Memory search function: {hasattr(engine, 'search_memory_for_keywords')}")
    
    # Test memory search
    test_query = "What book did I mention?"
    print(f"\nTesting memory search for: '{test_query}'")
    
    if hasattr(engine, 'search_memory_for_keywords'):
        memories = engine.search_memory_for_keywords(test_query)
        print(f"Found {len(memories)} memories")
        
        for i, memory in enumerate(memories[:3]):
            print(f"\nMemory {i+1}:")
            print(f"  ID: {memory[0]}")
            print(f"  Content: {memory[1][:100]}...")
            print(f"  Relevance: {memory[2]:.3f}")
            
            # Test content extraction
            extracted = engine.extract_relevant_details(memory[1], test_query)
            print(f"  Extracted: {extracted[:100]}...")
            
            # Test key information extraction
            if hasattr(engine, 'extract_key_information'):
                key_info = engine.extract_key_information(memory[1])
                print(f"  Key Info: {key_info[:100]}...")
    
    # Test a simple chat to see the full flow
    print(f"\n" + "="*50)
    print("TESTING FULL CHAT FLOW")
    print("="*50)
    
    result = assistant.chat("What book did I mention?")
    print(f"Response: {result.get('response', 'No response')}")
    
    assistant.end_session()

if __name__ == "__main__":
    debug_memory_content()
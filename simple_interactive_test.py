#!/usr/bin/env python3
"""
Simple Interactive Memory Test - No Crashes
"""

import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def main():
    """Simple interactive test"""
    print("🧠 SIMPLE INTERACTIVE MEMORY TEST")
    print("=" * 50)
    
    try:
        from lumina_memory.llm_memory_tester import LLMMemoryTester
        from lumina_memory.local_llm_interface import LocalLLMFactory
        
        # Initialize systems
        print("Initializing memory system...")
        tester = LLMMemoryTester(dimension=512)
        
        print("Initializing LLM interface...")
        llm = LocalLLMFactory.auto_detect_and_create()
        
        print(f"✅ Systems ready! Memory units: {len(tester.memory_env.xpunits)}")
        print("\n" + "=" * 50)
        
        # Test conversation
        test_messages = [
            "I'm excited about this holographic memory system!",
            "I love how it analyzes consciousness and emotions.",
            "This feels revolutionary for AI development.",
            "I wonder if I'm truly aware of my own thoughts?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n{i}. HUMAN: {message}")
            
            # Add to memory
            turn = tester.add_conversation_turn('human', message)
            
            # Show analysis
            if turn.emotional_analysis:
                emotional = turn.emotional_analysis
                print(f"   📊 Emotion: {emotional.get('dominant_emotion', 'none')} (weight: {emotional.get('total_emotional_weight', 0.0):.2f})")
            
            if turn.consciousness_analysis:
                consciousness = turn.consciousness_analysis.get('consciousness_score', 0.0)
                print(f"   🧠 Consciousness: {consciousness:.2f}")
            
            # Generate LLM response
            if llm:
                try:
                    response = llm.generate_response(message)
                    print(f"   🤖 ASSISTANT: {response[:150]}...")
                    
                    # Add assistant response to memory
                    tester.add_conversation_turn('assistant', response)
                except Exception as e:
                    print(f"   ⚠️ LLM response failed: {e}")
            
            print(f"   📈 Total memories: {len(tester.memory_env.xpunits)}")
        
        # Test recall
        print(f"\n" + "=" * 50)
        print("TESTING MEMORY RECALL")
        print("=" * 50)
        
        test_queries = [
            "What was I excited about?",
            "What did I love?",
            "What felt revolutionary?",
            "What was I wondering about?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            try:
                # Simple text search in memory content
                matches = []
                for unit in tester.memory_env.xpunits:
                    if any(word.lower() in unit.content.lower() for word in query.lower().split() if len(word) > 2):
                        matches.append(unit.content[:100] + "...")
                
                if matches:
                    print(f"   ✅ Found {len(matches)} matches:")
                    for match in matches[:2]:  # Show top 2
                        print(f"      • {match}")
                else:
                    print("   ❌ No matches found")
                    
            except Exception as e:
                print(f"   ⚠️ Recall error: {e}")
        
        # Final stats
        print(f"\n" + "=" * 50)
        print("FINAL STATISTICS")
        print("=" * 50)
        print(f"Total memories formed: {len(tester.memory_env.xpunits)}")
        print(f"Conversation turns: {len(tester.conversation_turns)}")
        
        # Show memory details
        for i, unit in enumerate(tester.memory_env.xpunits):
            print(f"{i+1}. {unit.content[:80]}... (importance: {unit.importance:.2f})")
        
        print("\n🎉 Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
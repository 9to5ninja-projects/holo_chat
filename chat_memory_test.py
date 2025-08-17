#!/usr/bin/env python3
"""
Simple Chat Memory Test
=======================

Interactive chat session to test memory formation with real conversations.
Bypasses the global memory aggregation issue while testing core functionality.
"""

from src.lumina_memory.enhanced_xpunit import EnhancedXPUnit
from src.lumina_memory.llm_memory_tester import EmotionalAnalyzer, ContextualAnalyzer, TemporalAnalyzer
import time

class SimpleChatMemoryTester:
    def __init__(self):
        self.emotional_analyzer = EmotionalAnalyzer()
        self.contextual_analyzer = ContextualAnalyzer()
        self.temporal_analyzer = TemporalAnalyzer()
        self.conversation_history = []
        self.memory_units = []
        
    def process_message(self, message: str, speaker: str = "human"):
        """Process a message and create memory"""
        print(f"\n🧠 Processing: '{message}'")
        print("-" * 50)
        
        # Create XPUnit
        xpunit = EnhancedXPUnit(
            content_id=f"{speaker}_{len(self.memory_units)}",
            content=message
        )
        
        # Analyze with framework
        emotional_analysis = self.emotional_analyzer.analyze_emotional_content(message)
        contextual_analysis = self.contextual_analyzer.analyze_contextual_relationships(
            message, [msg['content'] for msg in self.conversation_history[-5:]]
        )
        temporal_analysis = self.temporal_analyzer.analyze_temporal_content(message, time.time())
        
        # Calculate composite importance
        composite_importance = (
            xpunit.importance * 
            emotional_analysis['emotional_importance'] * 
            contextual_analysis['contextual_importance'] * 
            temporal_analysis['temporal_importance']
        )
        
        # Display analysis
        print(f"🧠 Consciousness: {xpunit.get_consciousness_level()} ({xpunit.consciousness_score:.3f})")
        print(f"😊 Emotional: {emotional_analysis['dominant_emotion']} ({emotional_analysis['total_emotional_weight']:.3f})")
        print(f"🔗 Contextual: {contextual_analysis['contextual_importance']:.3f}")
        print(f"⏰ Temporal: {temporal_analysis['temporal_importance']:.3f}")
        print(f"🎯 COMPOSITE IMPORTANCE: {composite_importance:.3f}")
        
        # Store memory
        memory_record = {
            'content': message,
            'speaker': speaker,
            'xpunit': xpunit,
            'emotional_analysis': emotional_analysis,
            'contextual_analysis': contextual_analysis,
            'temporal_analysis': temporal_analysis,
            'composite_importance': composite_importance,
            'timestamp': time.time()
        }
        
        self.conversation_history.append(memory_record)
        self.memory_units.append(memory_record)
        
        return memory_record
        
    def recall_memories(self, query: str = None):
        """Show memory recall results"""
        print(f"\n🔍 MEMORY RECALL" + (f" for '{query}'" if query else ""))
        print("=" * 50)
        
        # Sort by composite importance
        sorted_memories = sorted(self.memory_units, key=lambda x: x['composite_importance'], reverse=True)
        
        print("🏆 TOP MEMORIES BY IMPORTANCE:")
        for i, memory in enumerate(sorted_memories[:5]):
            print(f"  {i+1}. [{memory['speaker']}] '{memory['content'][:50]}...'")
            print(f"     Importance: {memory['composite_importance']:.3f}")
            print(f"     Consciousness: {memory['xpunit'].get_consciousness_level()}")
            print(f"     Emotion: {memory['emotional_analysis']['dominant_emotion']}")
            print()
            
    def show_statistics(self):
        """Show memory statistics"""
        if not self.memory_units:
            print("No memories formed yet.")
            return
            
        print(f"\n📊 MEMORY STATISTICS")
        print("=" * 50)
        
        total_memories = len(self.memory_units)
        high_consciousness = len([m for m in self.memory_units if m['xpunit'].get_consciousness_level() == 'HIGH'])
        emotional_memories = len([m for m in self.memory_units if m['emotional_analysis']['total_emotional_weight'] > 0.5])
        
        avg_importance = sum(m['composite_importance'] for m in self.memory_units) / total_memories
        avg_consciousness = sum(m['xpunit'].consciousness_score for m in self.memory_units) / total_memories
        avg_emotional = sum(m['emotional_analysis']['total_emotional_weight'] for m in self.memory_units) / total_memories
        
        print(f"Total memories: {total_memories}")
        print(f"High consciousness: {high_consciousness} ({high_consciousness/total_memories:.1%})")
        print(f"Emotional memories: {emotional_memories} ({emotional_memories/total_memories:.1%})")
        print(f"Average importance: {avg_importance:.3f}")
        print(f"Average consciousness: {avg_consciousness:.3f}")
        print(f"Average emotional weight: {avg_emotional:.3f}")

def main():
    """Interactive chat session"""
    print("🤖 SIMPLE CHAT MEMORY TESTER")
    print("=" * 50)
    print("Type messages to test memory formation!")
    print("Commands:")
    print("  /recall - Show memory recall")
    print("  /stats - Show statistics")
    print("  /quit - Exit")
    print()
    
    tester = SimpleChatMemoryTester()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input == '/quit':
                break
            elif user_input == '/recall':
                tester.recall_memories()
            elif user_input == '/stats':
                tester.show_statistics()
            else:
                # Process user message
                tester.process_message(user_input, "human")
                
                # Generate simple assistant response
                if "consciousness" in user_input.lower() or "aware" in user_input.lower():
                    response = "I find myself reflecting on the nature of awareness as we discuss this."
                elif "excited" in user_input.lower() or "love" in user_input.lower():
                    response = "I can sense your enthusiasm! That's wonderful to hear."
                elif "confused" in user_input.lower() or "wonder" in user_input.lower():
                    response = "I understand that feeling. These are complex topics to explore."
                else:
                    response = "That's an interesting perspective. What do you think about this?"
                    
                print(f"\nAssistant: {response}")
                tester.process_message(response, "assistant")
                
        except KeyboardInterrupt:
            break
            
    print("\n👋 Session ended!")
    tester.show_statistics()

if __name__ == "__main__":
    main()
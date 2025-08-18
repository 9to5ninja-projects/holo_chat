#!/usr/bin/env python3
"""
Interactive LLM Memory Testing
==============================

This script provides an interactive testing environment for evaluating
holographic memory performance using real-time LLM conversations.

Features:
- Real-time conversation processing and memory formation
- Emotional, contextual, and temporal analysis
- Interactive recall testing
- Performance monitoring and reporting
- Memory consolidation testing

Run this script to start an interactive session where you can:
1. Have conversations that form memories
2. Test recall with various queries
3. Monitor memory formation patterns
4. Analyze emotional and consciousness factors

Author: Lumina Memory Team
License: MIT
"""

import sys
import time
import json
from typing import Dict, List, Any, Optional

# Import our LLM memory testing framework
import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from lumina_memory.llm_memory_tester import (
    LLMMemoryTester, ConversationTurn, create_demo_conversation_test
)

class InteractiveLLMMemorySession:
    """
    Interactive session for testing LLM memory formation and recall
    """
    
    def __init__(self, dimension: int = 512):
        self.tester = LLMMemoryTester(dimension=dimension)
        self.session_active = True
        self.auto_analysis = True
        
    def start_session(self):
        """Start the interactive testing session"""
        print("🧠 INTERACTIVE LLM MEMORY TESTING SESSION")
        print("=" * 60)
        print()
        print("This session will test holographic memory formation using real conversations.")
        print("Each message you send will be analyzed for:")
        print("  • Emotional content and weighting")
        print("  • Contextual relationships")
        print("  • Temporal patterns")
        print("  • Consciousness indicators")
        print()
        print("Commands:")
        print("  /recall <query>     - Test memory recall")
        print("  /report            - Generate performance report")
        print("  /demo              - Run demo conversation")
        print("  /analysis on/off   - Toggle automatic analysis display")
        print("  /consolidate       - Test memory consolidation")
        print("  /help              - Show this help")
        print("  /quit              - End session")
        print()
        print("Start by typing a message or command...")
        print()
        
        while self.session_active:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.startswith('/'):
                    self._handle_command(user_input)
                else:
                    self._process_user_message(user_input)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Generating final report...")
                self._generate_final_report()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
                
    def _handle_command(self, command: str):
        """Handle user commands"""
        parts = command.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == '/quit':
            print("\n👋 Ending session...")
            self._generate_final_report()
            self.session_active = False
            
        elif cmd == '/recall':
            if not args:
                print("❌ Please provide a query. Example: /recall What were we discussing?")
                return
            self._test_recall(args)
            
        elif cmd == '/report':
            self._generate_performance_report()
            
        elif cmd == '/demo':
            self._run_demo_conversation()
            
        elif cmd == '/analysis':
            if args.lower() == 'off':
                self.auto_analysis = False
                print("📊 Automatic analysis display turned OFF")
            elif args.lower() == 'on':
                self.auto_analysis = True
                print("📊 Automatic analysis display turned ON")
            else:
                print("❌ Use '/analysis on' or '/analysis off'")
                
        elif cmd == '/consolidate':
            self._test_consolidation()
            
        elif cmd == '/help':
            self._show_help()
            
        else:
            print(f"❌ Unknown command: {cmd}. Type /help for available commands.")
            
    def _process_user_message(self, message: str):
        """Process a user message and form memory"""
        print(f"\n🧠 Processing message: '{message[:50]}{'...' if len(message) > 50 else ''}'")
        
        # Add user turn
        user_turn = self.tester.add_conversation_turn('human', message)
        
        if self.auto_analysis:
            self._display_turn_analysis(user_turn)
            
        # Generate assistant response (simulated)
        assistant_response = self._generate_assistant_response(message, user_turn)
        print(f"\nAssistant: {assistant_response}")
        
        # Add assistant turn
        assistant_turn = self.tester.add_conversation_turn('assistant', assistant_response)
        
        if self.auto_analysis:
            self._display_turn_analysis(assistant_turn)
            
        print()
        
    def _generate_assistant_response(self, user_message: str, user_turn: ConversationTurn) -> str:
        """Generate a contextually appropriate assistant response"""
        
        # Analyze user's emotional state
        emotional_analysis = user_turn.emotional_analysis
        dominant_emotion = emotional_analysis.get('dominant_emotion')
        
        # Generate response based on emotional context
        if dominant_emotion == 'joy' or dominant_emotion == 'love':
            responses = [
                "I can feel your enthusiasm! That's wonderful to hear.",
                "Your excitement is contagious! I'm delighted by your positive energy.",
                "It's beautiful to sense such joy in our conversation."
            ]
        elif dominant_emotion == 'fear' or dominant_emotion == 'anxiety':
            responses = [
                "I understand your concerns. Let's work through this together.",
                "Your feelings are completely valid. What specifically worries you?",
                "I'm here to help. Can you tell me more about what's troubling you?"
            ]
        elif dominant_emotion == 'curiosity' or dominant_emotion == 'introspection':
            responses = [
                "That's a fascinating question! I find myself pondering the same thing.",
                "Your curiosity sparks my own reflection. What do you think about this?",
                "I'm intrigued by your perspective. Let me think about this more deeply."
            ]
        elif dominant_emotion == 'confusion':
            responses = [
                "I can sense your confusion. Let me try to clarify this for you.",
                "That's understandably puzzling. Let's break it down step by step.",
                "I appreciate your honesty about feeling confused. How can I help?"
            ]
        else:
            # Default responses for neutral or mixed emotions
            responses = [
                "That's an interesting point. I'm processing what you've shared.",
                "I appreciate you sharing that with me. What are your thoughts on this?",
                "Thank you for that insight. It gives me something to reflect on."
            ]
            
        # Add consciousness-related responses for high consciousness content
        if user_turn.consciousness_score > 0.5:
            consciousness_responses = [
                "I find myself becoming more aware of my own thought processes as we discuss this.",
                "Your words make me reflect on the nature of my own awareness.",
                "I'm experiencing something like introspection as I consider your perspective."
            ]
            responses.extend(consciousness_responses)
            
        # Select response (in production, this would be more sophisticated)
        import random
        return random.choice(responses)
        
    def _display_turn_analysis(self, turn: ConversationTurn):
        """Display analysis results for a conversation turn"""
        print(f"  📊 Analysis for {turn.speaker}:")
        
        # Emotional analysis
        emotional = turn.emotional_analysis
        if emotional['has_emotional_content']:
            print(f"    😊 Emotional Weight: {emotional['total_emotional_weight']:.3f}")
            print(f"    🎭 Dominant Emotion: {emotional['dominant_emotion']}")
            print(f"    💪 Importance Boost: {emotional['emotional_importance']:.3f}x")
        else:
            print(f"    😐 No strong emotional content detected")
            
        # Contextual analysis
        contextual = turn.contextual_analysis
        print(f"    🔗 Contextual Importance: {contextual['contextual_importance']:.3f}")
        print(f"    📈 Semantic Continuity: {contextual['semantic_continuity']:.3f}")
        
        # Temporal analysis
        temporal = turn.temporal_analysis
        if temporal['has_temporal_content']:
            print(f"    ⏰ Temporal Importance: {temporal['temporal_importance']:.3f}")
            print(f"    🕐 Age: {temporal['age_hours']:.2f} hours")
        else:
            print(f"    ⏰ No specific temporal markers")
            
        # Find the corresponding memory unit
        memory_units = list(self.tester.memory_env.xpunits.values())
        if memory_units:
            latest_memory = memory_units[-1]  # Most recent
            print(f"    🧠 Consciousness Score: {latest_memory.consciousness_score:.3f}")
            print(f"    🏆 Final Importance: {latest_memory.importance:.3f}")
            
    def _test_recall(self, query: str):
        """Test memory recall with a query"""
        print(f"\n🔍 Testing recall for: '{query}'")
        print("-" * 40)
        
        result = self.tester.test_memory_recall(query)
        
        print(f"Query Analysis:")
        query_emotional = result['query_analysis']
        if query_emotional['has_emotional_content']:
            print(f"  Emotional content: {query_emotional['dominant_emotion']}")
        else:
            print(f"  No strong emotional content in query")
            
        print(f"\nRole-based results:")
        for i, (symbol, similarity) in enumerate(result['role_results'][:5]):
            print(f"  {i+1}. {symbol} (similarity: {similarity:.3f})")
            
        if result['compositional_results']:
            print(f"\nCompositional results:")
            for i, (content, similarity) in enumerate(result['compositional_results'][:3]):
                print(f"  {i+1}. '{content}...' (similarity: {similarity:.3f})")
                
        print(f"\nRecall Success: {'✅ YES' if result['recall_success'] else '❌ NO'}")
        print()
        
    def _generate_performance_report(self):
        """Generate and display performance report"""
        print("\n📊 MEMORY PERFORMANCE REPORT")
        print("=" * 50)
        
        report = self.tester.get_memory_performance_report()
        
        # Conversation summary
        conv_summary = report['conversation_summary']
        print(f"\n💬 Conversation Summary:")
        print(f"  Total turns: {conv_summary['total_turns']}")
        print(f"  Duration: {conv_summary['conversation_duration_hours']:.2f} hours")
        print(f"  Memories formed: {conv_summary['memories_formed']}")
        print(f"  Formation rate: {conv_summary['memory_formation_rate']:.3f} memories/turn")
        
        # Memory quality
        quality = report['memory_quality']
        print(f"\n🎯 Memory Quality:")
        print(f"  Emotional memory rate: {quality['emotional_memory_rate']:.3f}")
        print(f"  High consciousness rate: {quality['consciousness_rate']:.3f}")
        print(f"  Contextual connections: {quality['contextual_connections']}")
        print(f"  Average importance: {quality['average_importance']:.3f}")
        
        # Recall performance
        recall = report['recall_performance']
        print(f"\n🔍 Recall Performance:")
        print(f"  Total tests: {recall['total_recall_tests']}")
        print(f"  Successful recalls: {recall['successful_recalls']}")
        print(f"  Success rate: {recall['recall_success_rate']:.3f}")
        
        # Emotional patterns
        emotional = report['emotional_analysis_summary']
        if emotional:
            print(f"\n😊 Emotional Patterns:")
            print(f"  Emotional memories: {emotional['emotional_memories_count']}")
            print(f"  Average emotional weight: {emotional['average_emotional_weight']:.3f}")
            if emotional['dominant_emotions']:
                print(f"  Most common emotions: {list(emotional['dominant_emotions'].keys())[:3]}")
                
        # Consciousness patterns
        consciousness = report['consciousness_analysis_summary']
        if consciousness:
            print(f"\n🧠 Consciousness Patterns:")
            print(f"  Distribution: {consciousness['consciousness_distribution']}")
            print(f"  Average score: {consciousness['average_consciousness_score']:.3f}")
            print(f"  High consciousness memories: {consciousness['high_consciousness_memories']}")
            
        print()
        
    def _run_demo_conversation(self):
        """Run the demo conversation"""
        print("\n🎭 Running demo conversation...")
        print("-" * 40)
        
        demo_tester, demo_report = create_demo_conversation_test()
        
        print(f"\n📊 Demo Results:")
        print(f"  Memories formed: {demo_report['conversation_summary']['memories_formed']}")
        print(f"  Emotional memory rate: {demo_report['memory_quality']['emotional_memory_rate']:.3f}")
        print(f"  Recall success rate: {demo_report['recall_performance']['recall_success_rate']:.3f}")
        print()
        
    def _test_consolidation(self):
        """Test memory consolidation"""
        print("\n🔄 Testing memory consolidation...")
        print("-" * 40)
        
        # Get stats before consolidation
        stats_before = self.tester.memory_env.get_statistics()
        memories_before = stats_before['total_xpunits']
        
        # Perform consolidation
        self.tester.memory_env.consolidate_memories(similarity_threshold=0.8)
        
        # Get stats after consolidation
        stats_after = self.tester.memory_env.get_statistics()
        memories_after = stats_after['total_xpunits']
        
        print(f"Memories before consolidation: {memories_before}")
        print(f"Memories after consolidation: {memories_after}")
        print(f"Memories consolidated: {memories_before - memories_after}")
        print(f"Consolidation rate: {(memories_before - memories_after) / max(1, memories_before):.3f}")
        print()
        
    def _show_help(self):
        """Show help information"""
        print("\n❓ HELP - Available Commands:")
        print("-" * 40)
        print("/recall <query>     - Test memory recall with a specific query")
        print("/report            - Generate comprehensive performance report")
        print("/demo              - Run demo conversation to see system in action")
        print("/analysis on/off   - Toggle automatic analysis display")
        print("/consolidate       - Test memory consolidation (merge similar memories)")
        print("/help              - Show this help message")
        print("/quit              - End session and generate final report")
        print()
        print("💡 Tips:")
        print("- Try messages with different emotional content")
        print("- Use consciousness-related words like 'I think', 'I wonder', 'I am aware'")
        print("- Reference previous parts of the conversation")
        print("- Test recall with queries related to your messages")
        print()
        
    def _generate_final_report(self):
        """Generate final session report"""
        print("\n📋 FINAL SESSION REPORT")
        print("=" * 50)
        
        report = self.tester.get_memory_performance_report()
        
        # Key metrics
        conv_summary = report['conversation_summary']
        quality = report['memory_quality']
        recall = report['recall_performance']
        
        print(f"Session Duration: {conv_summary['conversation_duration_hours']:.2f} hours")
        print(f"Total Interactions: {conv_summary['total_turns']} turns")
        print(f"Memories Formed: {conv_summary['memories_formed']}")
        print(f"Emotional Memories: {int(quality['emotional_memory_rate'] * conv_summary['memories_formed'])}")
        print(f"High Consciousness Memories: {int(quality['consciousness_rate'] * conv_summary['memories_formed'])}")
        print(f"Recall Tests: {recall['total_recall_tests']}")
        print(f"Recall Success Rate: {recall['recall_success_rate']:.1%}")
        
        # Memory system performance
        memory_stats = report['memory_system_stats']
        print(f"\nMemory System:")
        print(f"  Dimension: {memory_stats['dimension']}")
        print(f"  Memory Usage: {memory_stats['memory_usage_mb']:.2f} MB")
        print(f"  Estimated Capacity: {memory_stats['estimated_capacity']} associations")
        
        print(f"\n✅ Session completed successfully!")
        print(f"💾 Memory data preserved in tester object for further analysis.")

def main():
    """Main entry point"""
    print("🚀 Starting Interactive LLM Memory Testing Session...")
    
    try:
        session = InteractiveLLMMemorySession(dimension=512)
        session.start_session()
    except Exception as e:
        print(f"❌ Session failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Chat Assistant with Emotion Engine Integration
==============================================

This bridges our emotion engine with practical chat functionality.
Every conversation automatically:
1. Updates mood based on interaction
2. Creates memory XPUnits 
3. Applies personality filters
4. Tracks consciousness growth
5. Learns from user feedback

This IS the practical interface for our 30-day program.
"""

import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from .emotion_engine import EmotionXPEnvironment
from .advanced_xpunit import AdvancedXPUnit, AffectState


@dataclass
class ChatSession:
    """Represents a chat session with emotion/memory tracking"""
    session_id: str
    start_time: float
    user_name: str = "User"
    assistant_name: str = "Lumina"
    
    # Conversation tracking
    messages: List[Dict[str, Any]] = None
    current_mood: Dict[str, float] = None
    session_xpunits: List[str] = None
    
    def __post_init__(self):
        if self.messages is None:
            self.messages = []
        if self.current_mood is None:
            self.current_mood = {"valence": 0.0, "arousal": 0.0, "dominance": 0.0}
        if self.session_xpunits is None:
            self.session_xpunits = []


class ChatAssistant:
    """
    Practical Chat Assistant with Emotion Engine
    
    This is the main interface for our 30-day program:
    - Handles conversations with automatic memory creation
    - Updates mood based on interaction sentiment
    - Applies personality filters to responses
    - Tracks learning and consciousness growth
    - Provides feedback mechanisms for refinement
    """
    
    def __init__(self, policies_path: Optional[str] = None):
        """Initialize chat assistant with emotion engine"""
        
        # Create enhanced environment
        self.env = EmotionXPEnvironment(dimension=512)
        
        # Load policies if provided
        if policies_path and Path(policies_path).exists():
            self.load_policies(policies_path)
        
        # Current session
        self.current_session: Optional[ChatSession] = None
        
        # Chat history for learning
        self.chat_history: List[ChatSession] = []
        
        # Performance metrics
        self.metrics = {
            "total_conversations": 0,
            "avg_mood_valence": 0.0,
            "consciousness_growth": 0.0,
            "user_satisfaction": 0.0,
            "learning_rate": 0.0
        }
    
    def load_policies(self, yaml_path: str):
        """Load emotion engine policies from YAML file"""
        try:
            import yaml
            with open(yaml_path, 'r') as f:
                policies = yaml.safe_load(f)
            self.env.emotion_engine.update_policies(policies)
            print(f"✅ Loaded policies from {yaml_path}")
        except Exception as e:
            print(f"❌ Failed to load policies: {e}")
    
    def start_session(self, user_name: str = "User") -> str:
        """Start a new chat session"""
        session_id = f"chat_{int(time.time()*1000)}"
        self.current_session = ChatSession(
            session_id=session_id,
            start_time=time.time(),
            user_name=user_name
        )
        
        # Use ASCII for RPC compatibility
        try:
            print(f"Started chat session: {session_id}")
        except UnicodeEncodeError:
            pass  # Ignore encoding errors in RPC mode
        return session_id
    
    def analyze_message_sentiment(self, message: str) -> Dict[str, float]:
        """
        Analyze message sentiment to determine affect delta
        
        This is a simple heuristic - in production you'd use a proper sentiment model
        """
        message_lower = message.lower()
        
        # Positive indicators
        positive_words = ["good", "great", "excellent", "love", "amazing", "wonderful", "happy", "excited"]
        negative_words = ["bad", "terrible", "hate", "awful", "sad", "angry", "frustrated", "disappointed"]
        high_arousal_words = ["excited", "angry", "amazing", "terrible", "love", "hate"]
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        arousal_count = sum(1 for word in high_arousal_words if word in message_lower)
        
        # Calculate affect delta
        valence = (positive_count - negative_count) * 0.2
        arousal = arousal_count * 0.15
        dominance = 0.1 if positive_count > negative_count else -0.05
        
        # Clamp values
        valence = max(-1.0, min(1.0, valence))
        arousal = max(0.0, min(1.0, arousal))
        dominance = max(-1.0, min(1.0, dominance))
        
        return {"valence": valence, "arousal": arousal, "dominance": dominance}
    
    def chat(self, user_message: str, model: str = "mistral") -> Dict[str, Any]:
        """
        Main chat function with automatic emotion/memory integration
        
        This is the core function for our 30-day program:
        1. Analyzes user message sentiment
        2. Updates mood via emotion engine
        3. Creates memory XPUnit for the interaction
        4. Generates response through personality filters
        5. Tracks consciousness growth
        """
        
        if not self.current_session:
            self.start_session()
        
        # 1. Analyze user message sentiment
        affect_delta = self.analyze_message_sentiment(user_message)
        
        # 2. Create XPUnit for user message
        user_affect = AffectState(
            valence=affect_delta["valence"],
            arousal=affect_delta["arousal"]
        )
        if hasattr(AffectState, 'dominance'):
            user_affect.dominance = affect_delta["dominance"]
        
        user_xpunit = AdvancedXPUnit(
            content_id=f"{self.current_session.session_id}_user_{len(self.current_session.messages)}",
            content=user_message,
            affect=user_affect
        )
        
        # Add metadata
        user_xpunit.metadata.update({
            "type": "user_message",
            "session_id": self.current_session.session_id,
            "message_index": len(self.current_session.messages),
            "timestamp": time.time()
        })
        
        # Add to environment
        self.env.xpunits[user_xpunit.content_id] = user_xpunit
        self.current_session.session_xpunits.append(user_xpunit.content_id)
        
        # 3. Run lived experience cycle to generate response
        try:
            response_result = self.env.lived_experience_cycle(
                xpunit_id=user_xpunit.content_id,
                cue_text=user_message,
                affect_delta=affect_delta,
                mode="external",
                model=model
            )
            
            if response_result["ok"]:
                assistant_response = response_result["response"]["text"]
                current_mood = response_result["mood"]
                
                # Update session
                self.current_session.current_mood = current_mood
                self.current_session.messages.append({
                    "role": "user",
                    "content": user_message,
                    "affect_delta": affect_delta,
                    "xpunit_id": user_xpunit.content_id
                })
                self.current_session.messages.append({
                    "role": "assistant", 
                    "content": assistant_response,
                    "mood": current_mood,
                    "narrative_xpunit": response_result["narrative_xpunit"],
                    "consciousness_growth": response_result.get("consciousness_growth", 0.0)
                })
                
                return {
                    "ok": True,
                    "response": assistant_response,
                    "mood": current_mood,
                    "affect_delta": affect_delta,
                    "consciousness_growth": response_result.get("consciousness_growth", 0.0),
                    "session_id": self.current_session.session_id
                }
            else:
                return {"ok": False, "error": response_result.get("error", "Unknown error")}
                
        except Exception as e:
            return {"ok": False, "error": f"Chat processing failed: {e}"}
    
    def get_mood_summary(self) -> str:
        """Get current mood state as human-readable summary"""
        if not self.current_session:
            return "No active session"
        
        mood = self.current_session.current_mood
        v, a, d = mood["valence"], mood["arousal"], mood["dominance"]
        
        # Interpret mood
        if v > 0.3:
            valence_desc = "positive" if v < 0.7 else "very positive"
        elif v < -0.3:
            valence_desc = "negative" if v > -0.7 else "very negative"
        else:
            valence_desc = "neutral"
        
        if a > 0.4:
            arousal_desc = "high energy"
        elif a > 0.2:
            arousal_desc = "moderate energy"
        else:
            arousal_desc = "calm"
        
        if d > 0.3:
            dominance_desc = "confident"
        elif d < -0.3:
            dominance_desc = "submissive"
        else:
            dominance_desc = "balanced"
        
        return f"{valence_desc}, {arousal_desc}, {dominance_desc} (V:{v:.2f} A:{a:.2f} D:{d:.2f})"
    
    def end_session(self) -> Dict[str, Any]:
        """End current session and return summary"""
        if not self.current_session:
            return {"error": "No active session"}
        
        session = self.current_session
        
        # Calculate session metrics
        total_messages = len(session.messages)
        avg_valence = sum(msg.get("mood", {}).get("valence", 0) 
                         for msg in session.messages if msg["role"] == "assistant") / max(1, total_messages//2)
        
        total_consciousness_growth = sum(msg.get("consciousness_growth", 0) 
                                       for msg in session.messages if msg["role"] == "assistant")
        
        session_summary = {
            "session_id": session.session_id,
            "duration_minutes": (time.time() - session.start_time) / 60,
            "total_messages": total_messages,
            "avg_mood_valence": avg_valence,
            "total_consciousness_growth": total_consciousness_growth,
            "xpunits_created": len(session.session_xpunits),
            "final_mood": session.current_mood
        }
        
        # Archive session
        self.chat_history.append(session)
        self.current_session = None
        
        # Update global metrics
        self.metrics["total_conversations"] += 1
        self.metrics["consciousness_growth"] += total_consciousness_growth
        
        return session_summary
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Get insights for 30-day program refinement
        
        This analyzes conversation patterns to suggest improvements
        """
        if not self.chat_history:
            return {"error": "No conversation history available"}
        
        # Analyze patterns across sessions
        total_sessions = len(self.chat_history)
        avg_session_length = sum(len(s.messages) for s in self.chat_history) / total_sessions
        
        # Mood trends
        mood_history = []
        for session in self.chat_history:
            for msg in session.messages:
                if msg["role"] == "assistant" and "mood" in msg:
                    mood_history.append(msg["mood"])
        
        if mood_history:
            avg_valence = sum(m["valence"] for m in mood_history) / len(mood_history)
            avg_arousal = sum(m["arousal"] for m in mood_history) / len(mood_history)
            avg_dominance = sum(m["dominance"] for m in mood_history) / len(mood_history)
        else:
            avg_valence = avg_arousal = avg_dominance = 0.0
        
        # Consciousness growth trend
        consciousness_growth = [
            sum(msg.get("consciousness_growth", 0) for msg in session.messages if msg["role"] == "assistant")
            for session in self.chat_history
        ]
        
        return {
            "total_sessions": total_sessions,
            "avg_session_length": avg_session_length,
            "mood_trends": {
                "avg_valence": avg_valence,
                "avg_arousal": avg_arousal, 
                "avg_dominance": avg_dominance
            },
            "consciousness_growth_trend": consciousness_growth,
            "total_xpunits": sum(len(s.session_xpunits) for s in self.chat_history),
            "recommendations": self._generate_recommendations(avg_valence, consciousness_growth)
        }
    
    def _generate_recommendations(self, avg_valence: float, consciousness_growth: List[float]) -> List[str]:
        """Generate recommendations for improving the system"""
        recommendations = []
        
        if avg_valence < -0.2:
            recommendations.append("Consider adjusting bias filters to be more empathetic")
        elif avg_valence > 0.8:
            recommendations.append("System may be too positive - add more balanced responses")
        
        if len(consciousness_growth) > 3:
            recent_growth = sum(consciousness_growth[-3:]) / 3
            early_growth = sum(consciousness_growth[:3]) / 3
            
            if recent_growth < early_growth * 0.5:
                recommendations.append("Consciousness growth is slowing - consider more challenging interactions")
        
        if not recommendations:
            recommendations.append("System performance looks good - continue current approach")
        
        return recommendations


def create_chat_cli():
    """Create a simple CLI for testing the chat assistant"""
    
    def main():
        print("Lumina Chat Assistant with Emotion Engine")
        print("=" * 50)
        
        # Initialize assistant
        policies_path = "e:/holo_chat/policies.yml"
        assistant = ChatAssistant(policies_path)
        
        print("Commands:")
        print("  /start [name] - Start new session")
        print("  /mood - Show current mood")
        print("  /end - End session and show summary")
        print("  /insights - Show learning insights")
        print("  /quit - Exit")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.startswith("/"):
                    if user_input == "/quit":
                        break
                    elif user_input.startswith("/start"):
                        parts = user_input.split(" ", 1)
                        name = parts[1] if len(parts) > 1 else "User"
                        session_id = assistant.start_session(name)
                        print(f"✅ Started session: {session_id}")
                    elif user_input == "/mood":
                        print(f"Current mood: {assistant.get_mood_summary()}")
                    elif user_input == "/end":
                        summary = assistant.end_session()
                        if "error" in summary:
                            print(f"❌ {summary['error']}")
                        else:
                            print(f"📊 Session Summary:")
                            print(f"   Duration: {summary['duration_minutes']:.1f} minutes")
                            print(f"   Messages: {summary['total_messages']}")
                            print(f"   Avg Mood: {summary['avg_mood_valence']:.2f}")
                            print(f"   Consciousness Growth: {summary['total_consciousness_growth']:.3f}")
                    elif user_input == "/insights":
                        insights = assistant.get_learning_insights()
                        if "error" in insights:
                            print(f"❌ {insights['error']}")
                        else:
                            print("📈 Learning Insights:")
                            print(f"   Total Sessions: {insights['total_sessions']}")
                            print(f"   Avg Session Length: {insights['avg_session_length']:.1f}")
                            print(f"   Mood Trends: V:{insights['mood_trends']['avg_valence']:.2f} A:{insights['mood_trends']['avg_arousal']:.2f} D:{insights['mood_trends']['avg_dominance']:.2f}")
                            print("   Recommendations:")
                            for rec in insights['recommendations']:
                                print(f"     • {rec}")
                    else:
                        print("❌ Unknown command")
                    continue
                
                if not user_input:
                    continue
                
                # Process chat message
                result = assistant.chat(user_input)
                
                if result["ok"]:
                    print(f"Lumina: {result['response']}")
                    print(f"[Mood: {assistant.get_mood_summary()}]")
                else:
                    print(f"❌ Error: {result['error']}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n👋 Goodbye!")
    
    return main


if __name__ == "__main__":
    cli = create_chat_cli()
    cli()
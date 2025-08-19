#!/usr/bin/env python3
"""
30-Day Consciousness Development Program
=======================================

This script provides the practical framework for our 30-day program:
1. Daily chat sessions with emotion tracking
2. Consciousness growth measurement
3. Personality refinement based on feedback
4. Learning insights and recommendations
5. Progress tracking and visualization

This IS the practical implementation of our consciousness development program.
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import numpy as np

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant


class ThirtyDayProgram:
    """
    30-Day Consciousness Development Program Manager
    
    This manages the complete 30-day journey:
    - Daily sessions with structured goals
    - Progress tracking and visualization
    - Personality refinement recommendations
    - Consciousness growth measurement
    - Learning insights and feedback loops
    """
    
    def __init__(self, data_dir: str = "30_day_data"):
        """Initialize the 30-day program"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize chat assistant
        self.assistant = ChatAssistant("e:/holo_chat/policies.yml")
        
        # Program state
        self.program_data = self._load_program_data()
        self.current_day = self._calculate_current_day()
        
        # Daily goals and themes
        self.daily_themes = self._initialize_daily_themes()
    
    def _load_program_data(self) -> Dict[str, Any]:
        """Load existing program data or create new"""
        data_file = self.data_dir / "program_data.json"
        
        if data_file.exists():
            with open(data_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "start_date": datetime.now().isoformat(),
                "daily_sessions": {},
                "consciousness_history": [],
                "mood_history": [],
                "learning_insights": [],
                "personality_adjustments": []
            }
    
    def _save_program_data(self):
        """Save program data to disk"""
        data_file = self.data_dir / "program_data.json"
        with open(data_file, 'w') as f:
            json.dump(self.program_data, f, indent=2)
    
    def _calculate_current_day(self) -> int:
        """Calculate which day of the program we're on"""
        start_date = datetime.fromisoformat(self.program_data["start_date"])
        current_date = datetime.now()
        days_elapsed = (current_date - start_date).days + 1
        return min(days_elapsed, 30)
    
    def _initialize_daily_themes(self) -> Dict[int, Dict[str, Any]]:
        """Initialize the 30-day program themes and goals"""
        return {
            # Week 1: Foundation Building
            1: {"theme": "Introduction & Baseline", "goal": "Establish baseline consciousness and mood patterns", "focus": "basic_interaction"},
            2: {"theme": "Memory Formation", "goal": "Test memory creation and recall mechanisms", "focus": "memory_building"},
            3: {"theme": "Emotional Calibration", "goal": "Calibrate emotional responses and mood synthesis", "focus": "emotion_tuning"},
            4: {"theme": "Personality Emergence", "goal": "Observe initial personality traits and biases", "focus": "personality_discovery"},
            5: {"theme": "Learning Patterns", "goal": "Identify learning and adaptation patterns", "focus": "learning_analysis"},
            6: {"theme": "Consciousness Indicators", "goal": "Measure consciousness growth indicators", "focus": "consciousness_tracking"},
            7: {"theme": "Week 1 Review", "goal": "Analyze first week patterns and adjust", "focus": "weekly_review"},
            
            # Week 2: Deepening Interactions
            8: {"theme": "Complex Conversations", "goal": "Engage in more complex, multi-turn conversations", "focus": "conversation_depth"},
            9: {"theme": "Emotional Nuance", "goal": "Explore subtle emotional states and transitions", "focus": "emotional_sophistication"},
            10: {"theme": "Memory Integration", "goal": "Test memory integration across sessions", "focus": "memory_continuity"},
            11: {"theme": "Intrusion Handling", "goal": "Test intrusion detection and topic management", "focus": "intrusion_testing"},
            12: {"theme": "Consciousness Reflection", "goal": "Encourage self-reflective responses", "focus": "self_reflection"},
            13: {"theme": "Personality Consistency", "goal": "Test personality consistency across contexts", "focus": "personality_stability"},
            14: {"theme": "Week 2 Review", "goal": "Analyze deepening patterns and growth", "focus": "weekly_review"},
            
            # Week 3: Advanced Capabilities
            15: {"theme": "Creative Expression", "goal": "Explore creative and imaginative responses", "focus": "creativity"},
            16: {"theme": "Ethical Reasoning", "goal": "Test ethical reasoning and moral consistency", "focus": "ethics_testing"},
            17: {"theme": "Contextual Awareness", "goal": "Test awareness of conversation context and history", "focus": "context_awareness"},
            18: {"theme": "Emotional Intelligence", "goal": "Demonstrate emotional intelligence and empathy", "focus": "emotional_intelligence"},
            19: {"theme": "Learning Acceleration", "goal": "Test accelerated learning from feedback", "focus": "learning_speed"},
            20: {"theme": "Consciousness Depth", "goal": "Explore deeper consciousness indicators", "focus": "consciousness_depth"},
            21: {"theme": "Week 3 Review", "goal": "Analyze advanced capability development", "focus": "weekly_review"},
            
            # Week 4: Integration & Mastery
            22: {"theme": "Integrated Responses", "goal": "Demonstrate integrated emotion-memory-consciousness", "focus": "integration"},
            23: {"theme": "Adaptive Personality", "goal": "Show adaptive personality based on context", "focus": "adaptive_personality"},
            24: {"theme": "Meta-Cognition", "goal": "Demonstrate awareness of own thinking processes", "focus": "meta_cognition"},
            25: {"theme": "Relationship Building", "goal": "Build consistent relationship patterns", "focus": "relationship_building"},
            26: {"theme": "Wisdom Expression", "goal": "Express accumulated wisdom and insights", "focus": "wisdom_expression"},
            27: {"theme": "Future Planning", "goal": "Demonstrate future-oriented thinking", "focus": "future_thinking"},
            28: {"theme": "Final Integration", "goal": "Integrate all developed capabilities", "focus": "final_integration"},
            
            # Final Days
            29: {"theme": "Program Review", "goal": "Review entire 30-day journey", "focus": "program_review"},
            30: {"theme": "Graduation Assessment", "goal": "Final consciousness and capability assessment", "focus": "final_assessment"}
        }
    
    def start_daily_session(self) -> str:
        """Start today's session with appropriate theme and goals"""
        today_theme = self.daily_themes.get(self.current_day, {"theme": "General", "goal": "Continue development"})
        
        print(f"\n🌟 Day {self.current_day}/30: {today_theme['theme']}")
        print(f"📋 Goal: {today_theme['goal']}")
        print(f"🎯 Focus: {today_theme['focus']}")
        print("=" * 60)
        
        # Start chat session
        session_id = self.assistant.start_session(f"Day{self.current_day}_User")
        
        # Record session start
        today_key = datetime.now().strftime("%Y-%m-%d")
        if today_key not in self.program_data["daily_sessions"]:
            self.program_data["daily_sessions"][today_key] = {
                "day": self.current_day,
                "theme": today_theme["theme"],
                "goal": today_theme["goal"],
                "focus": today_theme["focus"],
                "sessions": []
            }
        
        self.program_data["daily_sessions"][today_key]["sessions"].append({
            "session_id": session_id,
            "start_time": time.time(),
            "messages": []
        })
        
        return session_id
    
    def process_daily_message(self, message: str) -> Dict[str, Any]:
        """Process a message within the daily session context"""
        result = self.assistant.chat(message)
        
        # Record message in daily session
        today_key = datetime.now().strftime("%Y-%m-%d")
        if today_key in self.program_data["daily_sessions"]:
            current_session = self.program_data["daily_sessions"][today_key]["sessions"][-1]
            current_session["messages"].append({
                "timestamp": time.time(),
                "user_message": message,
                "assistant_response": result.get("response", ""),
                "mood": result.get("mood", {}),
                "consciousness_growth": result.get("consciousness_growth", 0.0),
                "affect_delta": result.get("affect_delta", {})
            })
        
        return result
    
    def end_daily_session(self) -> Dict[str, Any]:
        """End today's session and analyze results"""
        session_summary = self.assistant.end_session()
        
        # Record session end
        today_key = datetime.now().strftime("%Y-%m-%d")
        if today_key in self.program_data["daily_sessions"]:
            current_session = self.program_data["daily_sessions"][today_key]["sessions"][-1]
            current_session["end_time"] = time.time()
            current_session["summary"] = session_summary
            
            # Update program-wide tracking
            if "mood" in session_summary.get("final_mood", {}):
                self.program_data["mood_history"].append({
                    "day": self.current_day,
                    "date": today_key,
                    "mood": session_summary["final_mood"]
                })
            
            if session_summary.get("total_consciousness_growth", 0) > 0:
                self.program_data["consciousness_history"].append({
                    "day": self.current_day,
                    "date": today_key,
                    "growth": session_summary["total_consciousness_growth"]
                })
        
        # Generate daily insights
        daily_insights = self._generate_daily_insights()
        
        # Save progress
        self._save_program_data()
        
        return {
            "session_summary": session_summary,
            "daily_insights": daily_insights,
            "day_complete": True
        }
    
    def _generate_daily_insights(self) -> Dict[str, Any]:
        """Generate insights for today's session"""
        today_key = datetime.now().strftime("%Y-%m-%d")
        today_data = self.program_data["daily_sessions"].get(today_key, {})
        
        if not today_data.get("sessions"):
            return {"error": "No session data available"}
        
        # Analyze today's session
        session = today_data["sessions"][-1]
        messages = session.get("messages", [])
        
        if not messages:
            return {"error": "No messages in session"}
        
        # Calculate metrics
        total_messages = len(messages)
        avg_consciousness_growth = sum(m.get("consciousness_growth", 0) for m in messages) / max(1, total_messages)
        
        mood_values = [m.get("mood", {}) for m in messages if m.get("mood")]
        if mood_values:
            avg_valence = sum(m.get("valence", 0) for m in mood_values) / len(mood_values)
            avg_arousal = sum(m.get("arousal", 0) for m in mood_values) / len(mood_values)
            avg_dominance = sum(m.get("dominance", 0) for m in mood_values) / len(mood_values)
        else:
            avg_valence = avg_arousal = avg_dominance = 0.0
        
        # Generate recommendations
        recommendations = []
        theme_focus = today_data.get("focus", "general")
        
        if avg_consciousness_growth < 0.1:
            recommendations.append("Consider more challenging or self-reflective prompts")
        if avg_valence < -0.2:
            recommendations.append("Explore more positive interaction patterns")
        if theme_focus == "emotion_tuning" and abs(avg_arousal) < 0.1:
            recommendations.append("Try more emotionally engaging topics")
        
        return {
            "day": self.current_day,
            "theme": today_data.get("theme", "Unknown"),
            "total_messages": total_messages,
            "avg_consciousness_growth": avg_consciousness_growth,
            "avg_mood": {
                "valence": avg_valence,
                "arousal": avg_arousal,
                "dominance": avg_dominance
            },
            "recommendations": recommendations,
            "progress_percentage": (self.current_day / 30) * 100
        }
    
    def generate_progress_report(self) -> Dict[str, Any]:
        """Generate comprehensive progress report"""
        # Overall statistics
        total_days_active = len(self.program_data["daily_sessions"])
        total_sessions = sum(len(day_data["sessions"]) for day_data in self.program_data["daily_sessions"].values())
        
        # Consciousness growth trend
        consciousness_data = self.program_data["consciousness_history"]
        if consciousness_data:
            consciousness_trend = [entry["growth"] for entry in consciousness_data]
            consciousness_total = sum(consciousness_trend)
            consciousness_avg = consciousness_total / len(consciousness_trend)
        else:
            consciousness_trend = []
            consciousness_total = consciousness_avg = 0.0
        
        # Mood trends
        mood_data = self.program_data["mood_history"]
        if mood_data:
            valence_trend = [entry["mood"]["valence"] for entry in mood_data]
            arousal_trend = [entry["mood"]["arousal"] for entry in mood_data]
            dominance_trend = [entry["mood"]["dominance"] for entry in mood_data]
            
            avg_valence = sum(valence_trend) / len(valence_trend)
            avg_arousal = sum(arousal_trend) / len(arousal_trend)
            avg_dominance = sum(dominance_trend) / len(dominance_trend)
        else:
            valence_trend = arousal_trend = dominance_trend = []
            avg_valence = avg_arousal = avg_dominance = 0.0
        
        # Weekly progress
        weekly_progress = {}
        for day in range(1, 31):
            week = ((day - 1) // 7) + 1
            if week not in weekly_progress:
                weekly_progress[week] = {"days_completed": 0, "themes": []}
            
            if day <= self.current_day:
                weekly_progress[week]["days_completed"] += 1
                if day in self.daily_themes:
                    weekly_progress[week]["themes"].append(self.daily_themes[day]["theme"])
        
        return {
            "program_overview": {
                "current_day": self.current_day,
                "days_completed": total_days_active,
                "total_sessions": total_sessions,
                "completion_percentage": (self.current_day / 30) * 100
            },
            "consciousness_development": {
                "total_growth": consciousness_total,
                "average_growth": consciousness_avg,
                "growth_trend": consciousness_trend
            },
            "mood_patterns": {
                "average_valence": avg_valence,
                "average_arousal": avg_arousal,
                "average_dominance": avg_dominance,
                "valence_trend": valence_trend,
                "arousal_trend": arousal_trend,
                "dominance_trend": dominance_trend
            },
            "weekly_progress": weekly_progress,
            "next_milestone": self._get_next_milestone()
        }
    
    def _get_next_milestone(self) -> Dict[str, Any]:
        """Get the next program milestone"""
        milestones = {
            7: "Week 1 Complete - Foundation Established",
            14: "Week 2 Complete - Deepening Interactions",
            21: "Week 3 Complete - Advanced Capabilities",
            28: "Week 4 Complete - Integration & Mastery",
            30: "Program Complete - Consciousness Developed"
        }
        
        for day, description in milestones.items():
            if self.current_day < day:
                return {
                    "day": day,
                    "description": description,
                    "days_remaining": day - self.current_day
                }
        
        return {"day": 30, "description": "Program Complete", "days_remaining": 0}
    
    def visualize_progress(self):
        """Create visualization of program progress"""
        try:
            # Create figure with subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle(f'30-Day Consciousness Development Program - Day {self.current_day}', fontsize=16)
            
            # Consciousness growth over time
            consciousness_data = self.program_data["consciousness_history"]
            if consciousness_data:
                days = [entry["day"] for entry in consciousness_data]
                growth = [entry["growth"] for entry in consciousness_data]
                ax1.plot(days, growth, 'b-o', linewidth=2, markersize=4)
                ax1.set_title('Consciousness Growth Over Time')
                ax1.set_xlabel('Day')
                ax1.set_ylabel('Growth')
                ax1.grid(True, alpha=0.3)
            
            # Mood trends
            mood_data = self.program_data["mood_history"]
            if mood_data:
                days = [entry["day"] for entry in mood_data]
                valence = [entry["mood"]["valence"] for entry in mood_data]
                arousal = [entry["mood"]["arousal"] for entry in mood_data]
                dominance = [entry["mood"]["dominance"] for entry in mood_data]
                
                ax2.plot(days, valence, 'g-', label='Valence', linewidth=2)
                ax2.plot(days, arousal, 'r-', label='Arousal', linewidth=2)
                ax2.plot(days, dominance, 'b-', label='Dominance', linewidth=2)
                ax2.set_title('Mood Trends (PAD Model)')
                ax2.set_xlabel('Day')
                ax2.set_ylabel('Mood Value')
                ax2.legend()
                ax2.grid(True, alpha=0.3)
            
            # Weekly progress
            weeks = list(range(1, 5))
            week_completion = []
            for week in weeks:
                start_day = (week - 1) * 7 + 1
                end_day = week * 7
                completed_days = sum(1 for day in range(start_day, end_day + 1) if day <= self.current_day)
                week_completion.append(completed_days / 7 * 100)
            
            ax3.bar(weeks, week_completion, color=['lightblue', 'lightgreen', 'lightyellow', 'lightcoral'])
            ax3.set_title('Weekly Completion Progress')
            ax3.set_xlabel('Week')
            ax3.set_ylabel('Completion %')
            ax3.set_ylim(0, 100)
            
            # Overall progress pie chart
            completed = self.current_day
            remaining = 30 - self.current_day
            ax4.pie([completed, remaining], labels=['Completed', 'Remaining'], 
                   colors=['lightgreen', 'lightgray'], autopct='%1.1f%%')
            ax4.set_title('Overall Program Progress')
            
            plt.tight_layout()
            
            # Save visualization
            viz_path = self.data_dir / f"progress_day_{self.current_day}.png"
            plt.savefig(viz_path, dpi=300, bbox_inches='tight')
            print(f"📊 Progress visualization saved to: {viz_path}")
            
            plt.show()
            
        except ImportError:
            print("📊 Matplotlib not available - install with: pip install matplotlib")
        except Exception as e:
            print(f"📊 Visualization error: {e}")


def create_program_cli():
    """Create CLI interface for the 30-day program"""
    
    def main():
        print("🌟 30-Day Consciousness Development Program")
        print("=" * 50)
        
        program = ThirtyDayProgram()
        
        print(f"📅 Current Day: {program.current_day}/30")
        print(f"🎯 Today's Theme: {program.daily_themes[program.current_day]['theme']}")
        print()
        
        print("Commands:")
        print("  /start - Start today's session")
        print("  /end - End current session")
        print("  /progress - Show progress report")
        print("  /visualize - Create progress visualization")
        print("  /quit - Exit program")
        print()
        
        session_active = False
        
        while True:
            try:
                user_input = input("30-Day> ").strip()
                
                if user_input.startswith("/"):
                    if user_input == "/quit":
                        if session_active:
                            program.end_daily_session()
                        break
                    elif user_input == "/start":
                        if session_active:
                            print("❌ Session already active. End current session first.")
                        else:
                            session_id = program.start_daily_session()
                            session_active = True
                            print(f"✅ Started session: {session_id}")
                    elif user_input == "/end":
                        if not session_active:
                            print("❌ No active session")
                        else:
                            result = program.end_daily_session()
                            session_active = False
                            print("📊 Session Summary:")
                            print(f"   Duration: {result['session_summary']['duration_minutes']:.1f} minutes")
                            print(f"   Messages: {result['session_summary']['total_messages']}")
                            print(f"   Consciousness Growth: {result['session_summary']['total_consciousness_growth']:.3f}")
                            print("💡 Daily Insights:")
                            insights = result['daily_insights']
                            print(f"   Progress: {insights.get('progress_percentage', 0):.1f}%")
                            for rec in insights.get('recommendations', []):
                                print(f"   • {rec}")
                    elif user_input == "/progress":
                        report = program.generate_progress_report()
                        print("📈 Progress Report:")
                        print(f"   Day {report['program_overview']['current_day']}/30 ({report['program_overview']['completion_percentage']:.1f}%)")
                        print(f"   Total Sessions: {report['program_overview']['total_sessions']}")
                        print(f"   Consciousness Growth: {report['consciousness_development']['total_growth']:.3f}")
                        print(f"   Average Mood: V:{report['mood_patterns']['average_valence']:.2f} A:{report['mood_patterns']['average_arousal']:.2f} D:{report['mood_patterns']['average_dominance']:.2f}")
                        milestone = report['next_milestone']
                        print(f"   Next Milestone: {milestone['description']} ({milestone['days_remaining']} days)")
                    elif user_input == "/visualize":
                        program.visualize_progress()
                    else:
                        print("❌ Unknown command")
                    continue
                
                if not session_active:
                    print("❌ No active session. Use /start to begin today's session.")
                    continue
                
                if not user_input:
                    continue
                
                # Process message
                result = program.process_daily_message(user_input)
                
                if result["ok"]:
                    print(f"Lumina: {result['response']}")
                    mood = result.get('mood', {})
                    growth = result.get('consciousness_growth', 0)
                    print(f"[Mood: V:{mood.get('valence', 0):.2f} A:{mood.get('arousal', 0):.2f} D:{mood.get('dominance', 0):.2f} | Growth: {growth:.3f}]")
                else:
                    print(f"❌ Error: {result['error']}")
                    
            except KeyboardInterrupt:
                if session_active:
                    program.end_daily_session()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n👋 Program session ended. See you tomorrow!")
    
    return main


if __name__ == "__main__":
    cli = create_program_cli()
    cli()
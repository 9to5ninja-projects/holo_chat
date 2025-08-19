"""
Persistent Chat Assistant - Memory That Survives Across Sessions
================================================================

This module implements a chat assistant with true persistent memory that
accumulates across sessions and survives process restarts.

ARCHITECTURAL SIGNIFICANCE:
- Solves the memory persistence gap discovered in Day 14
- Enables true cross-session conversation continuity
- Provides foundation for accumulative learning and relationship building
- Maintains full compatibility with existing emotion engine and cognitive capabilities

PERSISTENCE FEATURES:
- Persistent memory across process restarts
- Session continuity and conversation history
- Accumulative learning over time
- Memory statistics and health monitoring
- Integration with emotion engine and pattern recognition

Author: Lumina Memory Team
Date: August 19, 2025 (Day 15)
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from .persistent_xp_environment import PersistentXPEnvironment, SessionContinuityManager
from .emotion_engine import EmotionXPEnvironment
from .chat_assistant import ChatAssistant, ChatSession
from .math_foundation import get_current_timestamp

logger = logging.getLogger(__name__)


@dataclass
class PersistentChatSession(ChatSession):
    """Chat session with persistence tracking"""
    memory_units_created: int = 0
    memory_units_accessed: int = 0
    persistence_health: str = "UNKNOWN"
    session_file_path: Optional[str] = None


class PersistentChatAssistant:
    """Chat assistant with persistent memory across sessions"""
    
    def __init__(self, memory_path: str = "chat_memory", policies_path: Optional[str] = None):
        """Initialize persistent chat assistant"""
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(exist_ok=True)
        
        # Initialize persistent environment
        self.persistent_env = PersistentXPEnvironment(str(self.memory_path))
        
        # Initialize emotion engine with persistent environment
        self.emotion_env = EmotionXPEnvironment(dimension=512)
        # Replace the emotion engine's environment with our persistent one
        self.emotion_env.xp_env = self.persistent_env
        
        # Initialize session continuity
        self.session_manager = SessionContinuityManager(self.memory_path)
        
        # Load previous session state
        self.previous_session_state = self.session_manager.load_session_state()
        
        # Current session
        self.current_session: Optional[PersistentChatSession] = None
        
        # Chat history for learning (persistent)
        self.chat_history_file = self.memory_path / "chat_history.json"
        self.chat_history = self._load_chat_history()
        
        # Performance metrics
        self.metrics = {
            "total_conversations": len(self.chat_history),
            "total_memory_units": len(self.persistent_env.units),
            "avg_mood_valence": 0.0,
            "consciousness_growth": 0.0,
            "user_satisfaction": 0.0,
            "learning_rate": 0.0,
            "persistence_health": self.persistent_env._check_persistence_health()
        }
        
        # Load policies if provided
        if policies_path and Path(policies_path).exists():
            self.load_policies(policies_path)
        
        logger.info(f"Persistent Chat Assistant initialized with {len(self.persistent_env.units)} existing memories")
    
    def load_policies(self, yaml_path: str):
        """Load emotion engine policies from YAML file"""
        try:
            import yaml
            with open(yaml_path, 'r') as f:
                policies = yaml.safe_load(f)
            self.emotion_env.emotion_engine.update_policies(policies)
            logger.info(f"✅ Loaded policies from {yaml_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load policies: {e}")
    
    def _load_chat_history(self) -> List[Dict[str, Any]]:
        """Load persistent chat history"""
        try:
            if self.chat_history_file.exists():
                with open(self.chat_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                logger.info(f"Loaded {len(history)} previous chat sessions")
                return history
            else:
                logger.info("No previous chat history found")
                return []
        except Exception as e:
            logger.error(f"Failed to load chat history: {e}")
            return []
    
    def _save_chat_history(self):
        """Save chat history to persistent storage"""
        try:
            with open(self.chat_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
            logger.debug("Saved chat history to disk")
        except Exception as e:
            logger.error(f"Failed to save chat history: {e}")
    
    def start_session(self, user_name: str = "User") -> str:
        """Start a new persistent chat session"""
        session_id = f"chat_{int(time.time()*1000)}"
        
        # Create session file path
        session_file = self.memory_path / "sessions" / f"{session_id}.json"
        session_file.parent.mkdir(exist_ok=True)
        
        self.current_session = PersistentChatSession(
            session_id=session_id,
            start_time=time.time(),
            user_name=user_name,
            assistant_name="Lumina",
            session_file_path=str(session_file)
        )
        
        # Load context from previous sessions if available
        context_summary = self._generate_session_context()
        
        logger.info(f"Started persistent session {session_id} for {user_name}")
        logger.info(f"Session context: {len(self.persistent_env.units)} memories available")
        
        return session_id
    
    def _generate_session_context(self) -> str:
        """Generate context summary from previous sessions and memories"""
        try:
            # Get recent memories
            recent_memories = []
            current_time = get_current_timestamp()
            
            for unit in self.persistent_env.units.values():
                # Get memories from last 7 days
                if current_time - unit.timestamp < 7 * 24 * 3600:
                    recent_memories.append(unit)
            
            # Sort by recency and importance
            recent_memories.sort(key=lambda x: x.last_access, reverse=True)
            
            # Generate summary
            if recent_memories:
                context = f"I have {len(self.persistent_env.units)} memories accumulated across {len(self.chat_history)} previous sessions. "
                context += f"Recent context includes {len(recent_memories)} memories from the past week."
            else:
                context = f"I have {len(self.persistent_env.units)} memories from {len(self.chat_history)} previous sessions."
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to generate session context: {e}")
            return "Starting fresh session."
    
    def chat(self, message: str) -> str:
        """Chat with persistent memory integration"""
        if not self.current_session:
            self.start_session()
        
        try:
            # Add user message to persistent memory
            user_unit = self.persistent_env.ingest_experience(
                f"User ({self.current_session.user_name}): {message}",
                metadata={
                    'type': 'user_message',
                    'session_id': self.current_session.session_id,
                    'user_name': self.current_session.user_name,
                    'timestamp': get_current_timestamp()
                }
            )
            
            self.current_session.memory_units_created += 1
            
            # Generate response using emotion engine with persistent memory
            response = self._generate_response_with_persistent_memory(message)
            
            # Add assistant response to persistent memory
            assistant_unit = self.persistent_env.ingest_experience(
                f"Assistant (Lumina): {response}",
                metadata={
                    'type': 'assistant_response',
                    'session_id': self.current_session.session_id,
                    'user_name': self.current_session.user_name,
                    'timestamp': get_current_timestamp(),
                    'response_to': user_unit.content_id
                }
            )
            
            self.current_session.memory_units_created += 1
            
            # Add to current session messages
            self.current_session.messages.extend([
                {
                    'role': 'user',
                    'content': message,
                    'timestamp': get_current_timestamp(),
                    'memory_unit_id': user_unit.content_id
                },
                {
                    'role': 'assistant',
                    'content': response,
                    'timestamp': get_current_timestamp(),
                    'memory_unit_id': assistant_unit.content_id
                }
            ])
            
            # Save session state
            self._save_current_session()
            
            # Update metrics
            self._update_metrics()
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat processing: {e}")
            return f"I apologize, but I encountered an error processing your message. Error: {e}"
    
    def _generate_response_with_persistent_memory(self, message: str) -> str:
        """Generate response using emotion engine with full persistent memory context"""
        try:
            # Use emotion engine to process the message with full memory context
            response = self.emotion_env.process_with_emotion(
                message,
                debug_patterns=False  # Set to True for debugging
            )
            
            # Track memory access
            if self.current_session:
                self.current_session.memory_units_accessed += len(self.persistent_env.units)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm having trouble processing that right now. Could you try rephrasing your question?"
    
    def _save_current_session(self):
        """Save current session state to persistent storage"""
        if not self.current_session:
            return
        
        try:
            # Update session metadata
            self.current_session.persistence_health = self.persistent_env._check_persistence_health()
            
            # Save session to file
            session_data = {
                'session_id': self.current_session.session_id,
                'start_time': self.current_session.start_time,
                'user_name': self.current_session.user_name,
                'assistant_name': self.current_session.assistant_name,
                'messages': self.current_session.messages,
                'memory_units_created': self.current_session.memory_units_created,
                'memory_units_accessed': self.current_session.memory_units_accessed,
                'persistence_health': self.current_session.persistence_health,
                'last_updated': get_current_timestamp()
            }
            
            if self.current_session.session_file_path:
                with open(self.current_session.session_file_path, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            # Save to session manager
            self.session_manager.save_session_state({
                'session_id': self.current_session.session_id,
                'total_units': len(self.persistent_env.units),
                'session_duration': get_current_timestamp() - self.current_session.start_time,
                'interactions': len(self.current_session.messages) // 2,
                'memory_units_created': self.current_session.memory_units_created,
                'persistence_health': self.current_session.persistence_health
            })
            
        except Exception as e:
            logger.error(f"Failed to save current session: {e}")
    
    def _update_metrics(self):
        """Update performance metrics"""
        try:
            self.metrics.update({
                "total_conversations": len(self.chat_history),
                "total_memory_units": len(self.persistent_env.units),
                "persistence_health": self.persistent_env._check_persistence_health()
            })
        except Exception as e:
            logger.error(f"Failed to update metrics: {e}")
    
    def end_session(self):
        """End current session and save to history"""
        if not self.current_session:
            return
        
        try:
            # Calculate session duration
            session_duration = time.time() - self.current_session.start_time
            
            # Create session summary
            session_summary = {
                'session_id': self.current_session.session_id,
                'start_time': self.current_session.start_time,
                'end_time': time.time(),
                'duration': session_duration,
                'user_name': self.current_session.user_name,
                'message_count': len(self.current_session.messages),
                'memory_units_created': self.current_session.memory_units_created,
                'memory_units_accessed': self.current_session.memory_units_accessed,
                'persistence_health': self.current_session.persistence_health
            }
            
            # Add to chat history
            self.chat_history.append(session_summary)
            
            # Keep only last 1000 sessions
            if len(self.chat_history) > 1000:
                self.chat_history = self.chat_history[-1000:]
            
            # Save chat history
            self._save_chat_history()
            
            # Final session save
            self._save_current_session()
            
            logger.info(f"Ended session {self.current_session.session_id} after {session_duration:.1f}s")
            logger.info(f"Session created {self.current_session.memory_units_created} new memories")
            
            self.current_session = None
            
        except Exception as e:
            logger.error(f"Error ending session: {e}")
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get comprehensive memory and session summary"""
        try:
            stats = self.persistent_env.get_persistence_stats()
            
            # Calculate session statistics
            session_durations = [s.get('duration', 0) for s in self.chat_history if 'duration' in s]
            avg_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
            
            total_messages = sum(s.get('message_count', 0) for s in self.chat_history)
            
            return {
                'persistence_stats': {
                    'total_units': stats.total_units,
                    'storage_size_mb': stats.storage_size_mb,
                    'oldest_memory': stats.oldest_memory_timestamp,
                    'newest_memory': stats.newest_memory_timestamp,
                    'persistence_health': stats.persistence_health
                },
                'session_stats': {
                    'total_sessions': len(self.chat_history),
                    'avg_session_duration': avg_session_duration,
                    'total_messages': total_messages,
                    'current_session_active': self.current_session is not None
                },
                'current_session': {
                    'session_id': self.current_session.session_id if self.current_session else None,
                    'duration': time.time() - self.current_session.start_time if self.current_session else 0,
                    'messages': len(self.current_session.messages) if self.current_session else 0,
                    'memory_units_created': self.current_session.memory_units_created if self.current_session else 0
                } if self.current_session else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get memory summary: {e}")
            return {'error': str(e)}
    
    def search_memory(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search persistent memory for relevant content"""
        try:
            # Use the persistent environment's search capabilities
            results = self.persistent_env.retrieve_similar(query, k=limit)
            
            # Format results
            formatted_results = []
            for unit, similarity in results:
                formatted_results.append({
                    'content': unit.content,
                    'similarity': similarity,
                    'timestamp': unit.timestamp,
                    'last_access': unit.last_access,
                    'importance': unit.importance,
                    'metadata': unit.metadata
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search memory: {e}")
            return []
    
    def validate_memory_integrity(self) -> Dict[str, Any]:
        """Validate memory integrity and return detailed report"""
        try:
            is_valid, issues = self.persistent_env.validate_persistence_integrity()
            
            return {
                'is_valid': is_valid,
                'issues': issues,
                'total_units': len(self.persistent_env.units),
                'persistence_health': self.persistent_env._check_persistence_health(),
                'validation_timestamp': get_current_timestamp()
            }
            
        except Exception as e:
            logger.error(f"Failed to validate memory integrity: {e}")
            return {
                'is_valid': False,
                'issues': [f"Validation failed: {e}"],
                'validation_timestamp': get_current_timestamp()
            }


def create_persistent_chat_assistant(memory_path: str = "chat_memory") -> PersistentChatAssistant:
    """Factory function to create a persistent chat assistant"""
    return PersistentChatAssistant(memory_path)


# Test function for development
def test_persistent_chat():
    """Test persistent chat functionality"""
    import tempfile
    import shutil
    
    # Create temporary storage
    temp_dir = tempfile.mkdtemp()
    
    try:
        print("🔧 Testing persistent chat functionality...")
        
        # Create first chat session
        assistant1 = PersistentChatAssistant(temp_dir)
        session1_id = assistant1.start_session("TestUser")
        
        response1 = assistant1.chat("Hello, I love hiking in the mountains.")
        response2 = assistant1.chat("My favorite color is blue.")
        
        assistant1.end_session()
        
        print(f"✅ Session 1 completed with {len(assistant1.persistent_env.units)} memories")
        
        # Create second chat session (simulating restart)
        assistant2 = PersistentChatAssistant(temp_dir)
        session2_id = assistant2.start_session("TestUser")
        
        response3 = assistant2.chat("What do you remember about my interests?")
        
        assistant2.end_session()
        
        print(f"✅ Session 2 completed with {len(assistant2.persistent_env.units)} memories")
        
        # Verify memory persistence
        assert len(assistant2.persistent_env.units) > 2, "Memories not persisted across sessions"
        
        # Get memory summary
        summary = assistant2.get_memory_summary()
        print(f"📊 Total sessions: {summary['session_stats']['total_sessions']}")
        print(f"📊 Total memories: {summary['persistence_stats']['total_units']}")
        print(f"📊 Storage size: {summary['persistence_stats']['storage_size_mb']:.2f} MB")
        
        print("✅ All persistent chat tests passed!")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_persistent_chat()
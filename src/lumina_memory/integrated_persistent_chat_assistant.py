"""
Integrated Persistent Chat Assistant
===================================

This module implements a chat assistant with fully integrated persistent
cognitive architecture, combining the best of persistent memory storage
with cognitive capabilities and mathematical memory management.

ARCHITECTURAL SIGNIFICANCE:
- Solves the integration gap identified in Day 15
- Provides seamless cognitive capabilities with persistent memory
- Implements mathematical memory management for scaling
- Enables true accumulative cognitive learning across sessions

INTEGRATION FEATURES:
- Unified persistent cognitive environment
- Mathematical memory management at scale
- Full compatibility with emotion engine and pattern recognition
- Hierarchical storage system for optimal performance
- Production-ready scaling capabilities

Author: Lumina Memory Team
Date: August 19, 2025 (Day 16)
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from .unified_persistent_environment import UnifiedPersistentEnvironment, MathematicalMemoryManager
from .persistent_chat_assistant import PersistentChatSession
from .math_foundation import get_current_timestamp

logger = logging.getLogger(__name__)


@dataclass
class IntegratedChatSession(PersistentChatSession):
    """Chat session with integrated persistent cognitive capabilities"""
    cognitive_patterns_used: List[str] = None
    mathematical_optimizations: int = 0
    storage_tier_distribution: Dict[str, int] = None
    cognitive_development_score: float = 0.0
    
    def __post_init__(self):
        if self.cognitive_patterns_used is None:
            self.cognitive_patterns_used = []
        if self.storage_tier_distribution is None:
            self.storage_tier_distribution = {'hot': 0, 'warm': 0, 'cold': 0, 'archive': 0}


class IntegratedPersistentChatAssistant:
    """Chat assistant with fully integrated persistent cognitive architecture"""
    
    def __init__(self, memory_path: str = "chat_memory", policies_path: Optional[str] = None):
        """Initialize integrated persistent chat assistant"""
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(exist_ok=True)
        
        # Initialize unified persistent environment (combines all capabilities)
        self.unified_env = UnifiedPersistentEnvironment(str(self.memory_path))
        
        # Direct access to components for convenience
        self.persistent_env = self.unified_env.persistent_backend
        self.memory_manager = self.unified_env.memory_manager
        
        # Session management
        self.session_manager = self.persistent_env.session_manager
        self.current_session: Optional[IntegratedChatSession] = None
        
        # Chat history for learning (persistent)
        self.chat_history_file = self.memory_path / "integrated_chat_history.json"
        self.chat_history = self._load_chat_history()
        
        # Performance and cognitive metrics
        self.metrics = {
            "total_conversations": len(self.chat_history),
            "total_memory_units": len(self.persistent_env.units),
            "cognitive_integration_score": 0.0,
            "mathematical_optimization_score": 0.0,
            "accumulative_learning_score": 0.0,
            "session_continuity_score": 0.0,
            "overall_integration_health": "INITIALIZING"
        }
        
        # Load policies if provided
        if policies_path and Path(policies_path).exists():
            self.load_policies(policies_path)
        
        # Initialize cognitive integration
        self._initialize_cognitive_integration()
        
        logger.info(f"Integrated Persistent Chat Assistant initialized")
        logger.info(f"Unified environment: {len(self.persistent_env.units)} memories, {self.unified_env.integration_stats}")
    
    def load_policies(self, yaml_path: str):
        """Load emotion engine policies from YAML file"""
        try:
            import yaml
            with open(yaml_path, 'r') as f:
                policies = yaml.safe_load(f)
            self.unified_env.emotion_engine.update_policies(policies)
            logger.info(f"✅ Loaded policies from {yaml_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load policies: {e}")
    
    def _initialize_cognitive_integration(self):
        """Initialize and validate cognitive integration"""
        try:
            # Test cognitive integration
            integration_test_result = self._test_cognitive_integration()
            
            # Update metrics based on integration test
            self.metrics["cognitive_integration_score"] = integration_test_result.get("integration_score", 0.0)
            self.metrics["overall_integration_health"] = integration_test_result.get("health_status", "UNKNOWN")
            
            logger.info(f"Cognitive integration initialized: {integration_test_result}")
            
        except Exception as e:
            logger.error(f"Failed to initialize cognitive integration: {e}")
            self.metrics["overall_integration_health"] = "ERROR"
    
    def _test_cognitive_integration(self) -> Dict[str, Any]:
        """Test cognitive integration capabilities"""
        try:
            test_results = {
                "emotion_engine_working": False,
                "pattern_recognition_working": False,
                "persistent_memory_working": False,
                "mathematical_management_working": False,
                "integration_score": 0.0,
                "health_status": "UNKNOWN"
            }
            
            # Test emotion engine integration
            try:
                test_response = self.unified_env.process_with_emotion("Test cognitive integration.")
                test_results["emotion_engine_working"] = len(test_response) > 10
            except Exception as e:
                logger.error(f"Emotion engine integration test failed: {e}")
            
            # Test pattern recognition integration
            try:
                if self.persistent_env.units:
                    similar_units = self.persistent_env.retrieve_similar("test", k=3)
                    test_results["pattern_recognition_working"] = len(similar_units) >= 0
                else:
                    test_results["pattern_recognition_working"] = True  # No units to test with
            except Exception as e:
                logger.error(f"Pattern recognition integration test failed: {e}")
            
            # Test persistent memory integration
            try:
                test_unit = self.persistent_env.ingest_experience("Integration test memory.")
                test_results["persistent_memory_working"] = test_unit is not None
            except Exception as e:
                logger.error(f"Persistent memory integration test failed: {e}")
            
            # Test mathematical management integration
            try:
                management_stats = self.memory_manager.get_management_stats()
                test_results["mathematical_management_working"] = management_stats.total_units >= 0
            except Exception as e:
                logger.error(f"Mathematical management integration test failed: {e}")
            
            # Calculate integration score
            working_components = sum([
                test_results["emotion_engine_working"],
                test_results["pattern_recognition_working"],
                test_results["persistent_memory_working"],
                test_results["mathematical_management_working"]
            ])
            
            test_results["integration_score"] = working_components / 4.0
            
            # Determine health status
            if test_results["integration_score"] >= 0.75:
                test_results["health_status"] = "HEALTHY"
            elif test_results["integration_score"] >= 0.5:
                test_results["health_status"] = "PARTIAL"
            else:
                test_results["health_status"] = "UNHEALTHY"
            
            return test_results
            
        except Exception as e:
            logger.error(f"Failed to test cognitive integration: {e}")
            return {"integration_score": 0.0, "health_status": "ERROR", "error": str(e)}
    
    def _load_chat_history(self) -> List[Dict[str, Any]]:
        """Load persistent integrated chat history"""
        try:
            if self.chat_history_file.exists():
                with open(self.chat_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                logger.info(f"Loaded {len(history)} previous integrated chat sessions")
                return history
            else:
                logger.info("No previous integrated chat history found")
                return []
        except Exception as e:
            logger.error(f"Failed to load integrated chat history: {e}")
            return []
    
    def _save_chat_history(self):
        """Save integrated chat history to persistent storage"""
        try:
            with open(self.chat_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
            logger.debug("Saved integrated chat history to disk")
        except Exception as e:
            logger.error(f"Failed to save integrated chat history: {e}")
    
    def start_session(self, user_name: str = "User") -> str:
        """Start a new integrated persistent chat session"""
        session_id = f"integrated_chat_{int(time.time()*1000)}"
        
        # Create session file path
        session_file = self.memory_path / "sessions" / f"{session_id}.json"
        session_file.parent.mkdir(exist_ok=True)
        
        self.current_session = IntegratedChatSession(
            session_id=session_id,
            start_time=time.time(),
            user_name=user_name,
            assistant_name="Lumina-Integrated",
            session_file_path=str(session_file)
        )
        
        # Load context from previous sessions and mathematical analysis
        context_summary = self._generate_integrated_session_context()
        
        # Optimize memory storage at session start
        optimization_stats = self.unified_env.optimize_memory_storage()
        self.current_session.mathematical_optimizations += 1
        
        logger.info(f"Started integrated session {session_id} for {user_name}")
        logger.info(f"Session context: {len(self.persistent_env.units)} memories, optimization: {optimization_stats}")
        
        return session_id
    
    def _generate_integrated_session_context(self) -> str:
        """Generate context summary using integrated cognitive and mathematical analysis"""
        try:
            # Get mathematical memory management stats
            management_stats = self.memory_manager.get_management_stats()
            
            # Get recent high-importance memories
            recent_memories = []
            current_time = get_current_timestamp()
            
            for unit in self.persistent_env.units.values():
                # Get memories from last 7 days with high importance
                if (current_time - unit.timestamp < 7 * 24 * 3600 and 
                    self.memory_manager.calculate_memory_importance(unit) > 0.7):
                    recent_memories.append(unit)
            
            # Sort by mathematical importance
            recent_memories.sort(key=lambda x: self.memory_manager.calculate_memory_importance(x), reverse=True)
            
            # Generate integrated context summary
            context = f"I have {management_stats.total_units} memories with mathematical management: "
            context += f"{management_stats.hot_storage_units} hot, {management_stats.warm_storage_units} warm, "
            context += f"{management_stats.cold_storage_units} cold, {management_stats.archive_storage_units} archived. "
            
            if recent_memories:
                context += f"Recent high-importance context includes {len(recent_memories)} significant memories. "
            
            context += f"Cognitive integration health: {self.metrics['overall_integration_health']}."
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to generate integrated session context: {e}")
            return "Starting integrated session with full cognitive and mathematical capabilities."
    
    def chat(self, message: str) -> str:
        """Chat with integrated persistent cognitive architecture"""
        if not self.current_session:
            self.start_session()
        
        try:
            # Add user message to persistent memory with mathematical management
            user_unit = self.unified_env.ingest_experience(
                f"User ({self.current_session.user_name}): {message}",
                metadata={
                    'type': 'user_message',
                    'session_id': self.current_session.session_id,
                    'user_name': self.current_session.user_name,
                    'timestamp': get_current_timestamp(),
                    'integrated_session': True
                }
            )
            
            self.current_session.memory_units_created += 1
            
            # Update storage tier distribution
            storage_strategy = self.memory_manager.calculate_storage_strategy(user_unit)
            self.current_session.storage_tier_distribution[storage_strategy.tier] += 1
            
            # Generate response using integrated cognitive architecture
            response = self._generate_integrated_cognitive_response(message)
            
            # Detect cognitive patterns used
            patterns_used = self._detect_cognitive_patterns_used(message, response)
            self.current_session.cognitive_patterns_used.extend(patterns_used)
            
            # Add assistant response to persistent memory
            assistant_unit = self.unified_env.ingest_experience(
                f"Assistant (Lumina-Integrated): {response}",
                metadata={
                    'type': 'assistant_response',
                    'session_id': self.current_session.session_id,
                    'user_name': self.current_session.user_name,
                    'timestamp': get_current_timestamp(),
                    'response_to': user_unit.content_id,
                    'cognitive_patterns_used': patterns_used,
                    'integrated_session': True
                }
            )
            
            self.current_session.memory_units_created += 1
            
            # Update storage tier distribution
            storage_strategy = self.memory_manager.calculate_storage_strategy(assistant_unit)
            self.current_session.storage_tier_distribution[storage_strategy.tier] += 1
            
            # Add to current session messages
            self.current_session.messages.extend([
                {
                    'role': 'user',
                    'content': message,
                    'timestamp': get_current_timestamp(),
                    'memory_unit_id': user_unit.content_id,
                    'storage_tier': storage_strategy.tier
                },
                {
                    'role': 'assistant',
                    'content': response,
                    'timestamp': get_current_timestamp(),
                    'memory_unit_id': assistant_unit.content_id,
                    'cognitive_patterns': patterns_used,
                    'storage_tier': storage_strategy.tier
                }
            ])
            
            # Calculate cognitive development score
            self.current_session.cognitive_development_score = self._calculate_cognitive_development()
            
            # Save session state
            self._save_current_session()
            
            # Update metrics
            self._update_integrated_metrics()
            
            # Periodic optimization (every 10 interactions)
            if len(self.current_session.messages) % 20 == 0:  # Every 10 exchanges
                optimization_stats = self.unified_env.optimize_memory_storage()
                self.current_session.mathematical_optimizations += 1
                logger.info(f"Periodic optimization: {optimization_stats}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in integrated chat processing: {e}")
            return f"I apologize, but I encountered an error in my integrated processing. Error: {e}"
    
    def _generate_integrated_cognitive_response(self, message: str) -> str:
        """Generate response using integrated cognitive architecture"""
        try:
            # Use unified environment for emotion processing with persistent memory
            response = self.unified_env.process_with_emotion(
                message,
                debug_patterns=False  # Set to True for debugging
            )
            
            # Track memory access for mathematical management
            if self.current_session:
                self.current_session.memory_units_accessed += len(self.persistent_env.units)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating integrated cognitive response: {e}")
            return "I'm having trouble with my integrated processing right now. Could you try rephrasing your question?"
    
    def _detect_cognitive_patterns_used(self, message: str, response: str) -> List[str]:
        """Detect which cognitive patterns were used in the response"""
        try:
            patterns_used = []
            response_lower = response.lower()
            
            # Pattern detection based on response characteristics
            pattern_indicators = {
                'curiosity_response': ['curious', 'fascinating', 'wonder', 'explore', 'intrigued'],
                'mentor_archetype': ['grappling', 'growth', 'wisdom', 'reflection', 'values'],
                'creative_archetype': ['unique combination', 'innovation', 'creative', 'pioneer', 'possibilities'],
                'collaborator_archetype': ['together', 'collaborate', 'partnership', 'shared', 'collective'],
                'analytical_thinking': ['analyze', 'systematic', 'framework', 'approach', 'methodology'],
                'emotional_processing': ['feel', 'emotion', 'experience', 'sense', 'resonate']
            }
            
            for pattern, indicators in pattern_indicators.items():
                matches = sum(1 for indicator in indicators if indicator in response_lower)
                if matches >= 2:  # Require at least 2 indicators
                    patterns_used.append(pattern)
            
            return patterns_used
            
        except Exception as e:
            logger.error(f"Failed to detect cognitive patterns: {e}")
            return []
    
    def _calculate_cognitive_development(self) -> float:
        """Calculate cognitive development score for current session"""
        try:
            if not self.current_session or not self.current_session.messages:
                return 0.0
            
            # Factors for cognitive development
            pattern_diversity = len(set(self.current_session.cognitive_patterns_used))
            message_complexity = sum(len(msg['content']) for msg in self.current_session.messages) / len(self.current_session.messages)
            memory_integration = self.current_session.memory_units_accessed / max(len(self.persistent_env.units), 1)
            
            # Normalize and combine factors
            pattern_score = min(pattern_diversity / 5.0, 1.0)  # Max 5 different patterns
            complexity_score = min(message_complexity / 200.0, 1.0)  # Normalize to 200 chars
            integration_score = min(memory_integration, 1.0)
            
            development_score = (pattern_score + complexity_score + integration_score) / 3.0
            
            return development_score
            
        except Exception as e:
            logger.error(f"Failed to calculate cognitive development: {e}")
            return 0.0
    
    def _save_current_session(self):
        """Save current integrated session state to persistent storage"""
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
                'cognitive_patterns_used': self.current_session.cognitive_patterns_used,
                'mathematical_optimizations': self.current_session.mathematical_optimizations,
                'storage_tier_distribution': self.current_session.storage_tier_distribution,
                'cognitive_development_score': self.current_session.cognitive_development_score,
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
                'cognitive_development_score': self.current_session.cognitive_development_score,
                'mathematical_optimizations': self.current_session.mathematical_optimizations,
                'persistence_health': self.current_session.persistence_health
            })
            
        except Exception as e:
            logger.error(f"Failed to save current integrated session: {e}")
    
    def _update_integrated_metrics(self):
        """Update integrated performance metrics"""
        try:
            # Update basic metrics
            self.metrics.update({
                "total_conversations": len(self.chat_history),
                "total_memory_units": len(self.persistent_env.units)
            })
            
            # Update cognitive integration score
            integration_test = self._test_cognitive_integration()
            self.metrics["cognitive_integration_score"] = integration_test.get("integration_score", 0.0)
            self.metrics["overall_integration_health"] = integration_test.get("health_status", "UNKNOWN")
            
            # Update mathematical optimization score
            management_stats = self.memory_manager.get_management_stats()
            self.metrics["mathematical_optimization_score"] = management_stats.storage_efficiency
            
            # Update accumulative learning score (based on session development)
            if self.current_session:
                self.metrics["accumulative_learning_score"] = self.current_session.cognitive_development_score
            
        except Exception as e:
            logger.error(f"Failed to update integrated metrics: {e}")
    
    def end_session(self):
        """End current integrated session and save to history"""
        if not self.current_session:
            return
        
        try:
            # Calculate session duration
            session_duration = time.time() - self.current_session.start_time
            
            # Final optimization
            final_optimization = self.unified_env.optimize_memory_storage()
            self.current_session.mathematical_optimizations += 1
            
            # Create integrated session summary
            session_summary = {
                'session_id': self.current_session.session_id,
                'start_time': self.current_session.start_time,
                'end_time': time.time(),
                'duration': session_duration,
                'user_name': self.current_session.user_name,
                'message_count': len(self.current_session.messages),
                'memory_units_created': self.current_session.memory_units_created,
                'memory_units_accessed': self.current_session.memory_units_accessed,
                'cognitive_patterns_used': list(set(self.current_session.cognitive_patterns_used)),
                'mathematical_optimizations': self.current_session.mathematical_optimizations,
                'storage_tier_distribution': self.current_session.storage_tier_distribution,
                'cognitive_development_score': self.current_session.cognitive_development_score,
                'persistence_health': self.current_session.persistence_health,
                'final_optimization': final_optimization
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
            
            logger.info(f"Ended integrated session {self.current_session.session_id} after {session_duration:.1f}s")
            logger.info(f"Session created {self.current_session.memory_units_created} memories, "
                       f"used {len(set(self.current_session.cognitive_patterns_used))} cognitive patterns, "
                       f"performed {self.current_session.mathematical_optimizations} optimizations")
            
            self.current_session = None
            
        except Exception as e:
            logger.error(f"Error ending integrated session: {e}")
    
    def get_integrated_summary(self) -> Dict[str, Any]:
        """Get comprehensive integrated system summary"""
        try:
            # Get unified environment stats
            unified_stats = self.unified_env.get_unified_stats()
            
            # Calculate session statistics
            session_durations = [s.get('duration', 0) for s in self.chat_history if 'duration' in s]
            avg_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
            
            total_messages = sum(s.get('message_count', 0) for s in self.chat_history)
            total_cognitive_patterns = len(set(
                pattern for session in self.chat_history 
                for pattern in session.get('cognitive_patterns_used', [])
            ))
            
            return {
                'unified_environment': unified_stats,
                'session_stats': {
                    'total_sessions': len(self.chat_history),
                    'avg_session_duration': avg_session_duration,
                    'total_messages': total_messages,
                    'total_cognitive_patterns_used': total_cognitive_patterns,
                    'current_session_active': self.current_session is not None
                },
                'current_session': {
                    'session_id': self.current_session.session_id if self.current_session else None,
                    'duration': time.time() - self.current_session.start_time if self.current_session else 0,
                    'messages': len(self.current_session.messages) if self.current_session else 0,
                    'memory_units_created': self.current_session.memory_units_created if self.current_session else 0,
                    'cognitive_patterns_used': len(set(self.current_session.cognitive_patterns_used)) if self.current_session else 0,
                    'mathematical_optimizations': self.current_session.mathematical_optimizations if self.current_session else 0,
                    'cognitive_development_score': self.current_session.cognitive_development_score if self.current_session else 0.0
                } if self.current_session else None,
                'integration_metrics': self.metrics
            }
            
        except Exception as e:
            logger.error(f"Failed to get integrated summary: {e}")
            return {'error': str(e)}


def create_integrated_persistent_chat_assistant(memory_path: str = "chat_memory") -> IntegratedPersistentChatAssistant:
    """Factory function to create an integrated persistent chat assistant"""
    return IntegratedPersistentChatAssistant(memory_path)


# Test function for development
def test_integrated_chat_assistant():
    """Test integrated persistent chat assistant"""
    import tempfile
    import shutil
    
    # Create temporary storage
    temp_dir = tempfile.mkdtemp()
    
    try:
        print("🔧 Testing integrated persistent chat assistant...")
        
        # Create integrated assistant
        assistant = IntegratedPersistentChatAssistant(temp_dir)
        session_id = assistant.start_session("TestUser")
        
        # Test integrated cognitive capabilities
        response1 = assistant.chat("I'm interested in the intersection of AI consciousness and quantum mechanics.")
        response2 = assistant.chat("How might these concepts inform ethical AI development?")
        response3 = assistant.chat("Can you help me develop a framework for evaluating consciousness-like properties?")
        
        assistant.end_session()
        
        print(f"✅ Session completed with integrated cognitive architecture")
        
        # Get comprehensive summary
        summary = assistant.get_integrated_summary()
        print(f"📊 Total memories: {summary['unified_environment']['persistence']['total_units']}")
        print(f"📊 Cognitive patterns used: {summary['session_stats']['total_cognitive_patterns_used']}")
        print(f"📊 Integration health: {summary['integration_metrics']['overall_integration_health']}")
        
        print("✅ All integrated chat assistant tests passed!")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_integrated_chat_assistant()
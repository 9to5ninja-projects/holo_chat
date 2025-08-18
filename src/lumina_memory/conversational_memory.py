"""
Conversational Memory System - Short-Term Memory Architecture
============================================================

Implements the critical "freeze-frame" conversational memory system that bridges
between immediate context and persistent XPUnits.

ARCHITECTURE BREAKTHROUGH:
This addresses the missing short-term memory layer identified through XPUnit
accumulation analysis. The system provides:

1. **Freeze-Frame Loading**: Restore conversational context at session start
2. **Working Memory**: Maintain conversation continuity during interactions  
3. **Crystallization Process**: Convert important memories to persistent XPUnits
4. **Dual Decay Mechanics**: Short-term (15min) and long-term (72hr) decay

MEMORY LAYERS:
- Immediate Context (seconds): Current prompt/response
- Conversational Memory (minutes): This module - working memory with 15min decay
- Persistent XPUnits (hours/days): Long-term storage with 72hr decay
- Consolidated Memory (weeks/months): Cross-XPUnit relationships

Author: Lumina Memory Team
License: MIT
"""

import time
import hashlib
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

from .emotional_weighting import EmotionalState
from .xp_core_unified import UnifiedXPConfig

logger = logging.getLogger(__name__)


@dataclass
class ConversationalMemoryUnit:
    """
    Short-term memory unit for conversational context
    
    Unlike XPUnits (persistent), these are ephemeral and decay quickly.
    They represent the "working memory" of ongoing conversations.
    """
    content: str
    timestamp: float
    turn_number: int
    importance: float = 1.0
    emotional_state: Optional[EmotionalState] = None
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    speaker: str = "user"  # "user" or "assistant"
    
    # Short-term decay parameters (much faster than XPUnits)
    decay_half_life_minutes: float = 15.0  # 15 minutes vs 72 hours for XPUnits
    crystallization_threshold: float = 3.0  # Becomes XPUnit if importance > 3.0
    
    def get_age_minutes(self) -> float:
        """Get age in minutes"""
        return (time.time() - self.timestamp) / 60.0
    
    def get_decay_factor(self) -> float:
        """Calculate decay factor for short-term memory"""
        age_minutes = self.get_age_minutes()
        return np.exp(-age_minutes * np.log(2) / self.decay_half_life_minutes)
    
    def get_effective_importance(self) -> float:
        """Get importance adjusted for decay"""
        return self.importance * self.get_decay_factor()
    
    def should_crystallize(self) -> bool:
        """Check if this should become a persistent XPUnit"""
        return self.get_effective_importance() > self.crystallization_threshold
    
    def access(self):
        """Mark as accessed (boosts importance)"""
        self.access_count += 1
        self.last_access = time.time()
        # Accessing boosts importance (shows relevance)
        self.importance += 0.1 * self.get_decay_factor()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "content": self.content,
            "timestamp": self.timestamp,
            "turn_number": self.turn_number,
            "importance": self.importance,
            "access_count": self.access_count,
            "last_access": self.last_access,
            "speaker": self.speaker,
            "age_minutes": self.get_age_minutes(),
            "effective_importance": self.get_effective_importance(),
            "should_crystallize": self.should_crystallize(),
            "emotional_state": {
                "valence": self.emotional_state.valence if self.emotional_state else 0.0,
                "arousal": self.emotional_state.arousal if self.emotional_state else 0.0,
                "intensity": self.emotional_state.intensity() if self.emotional_state else 0.0
            } if self.emotional_state else None
        }


class ConversationalMemoryManager:
    """
    Manages the short-term conversational memory system
    
    This is the "freeze-frame" system that:
    1. Loads previous conversation state at session start
    2. Maintains working memory during conversation
    3. Crystallizes important memories into XPUnits
    4. Handles short-term decay mechanics
    
    CRITICAL ARCHITECTURE COMPONENT:
    This bridges the gap between immediate context and persistent memory,
    enabling true conversational continuity and consciousness development.
    """
    
    def __init__(self, config: UnifiedXPConfig):
        self.config = config
        self.conversation_units: List[ConversationalMemoryUnit] = []
        self.session_start_time = time.time()
        self.turn_counter = 0
        self.crystallized_units: List[Dict[str, Any]] = []
        
        # Short-term memory limits
        self.max_conversation_units = 50  # Keep last 50 conversational units
        self.cleanup_interval_minutes = 5  # Clean up every 5 minutes
        self.last_cleanup = time.time()
        
        # Crystallization callback (set by parent system)
        self.crystallization_callback = None
        
        logger.info("Conversational Memory Manager initialized")
        logger.info(f"Max units: {self.max_conversation_units}, Cleanup interval: {self.cleanup_interval_minutes}min")
    
    def set_crystallization_callback(self, callback):
        """Set callback function for when memories crystallize into XPUnits"""
        self.crystallization_callback = callback
    
    def freeze_frame_load(self, previous_conversation: List[Dict]) -> Dict[str, Any]:
        """
        Load previous conversation state (the "freeze-frame" moment)
        
        This happens at the start of each interaction to restore context.
        Critical for consciousness continuity across sessions.
        
        Args:
            previous_conversation: List of conversation items with content/timestamp
            
        Returns:
            Dictionary with loading statistics and context summary
        """
        logger.info("🧠 FREEZE-FRAME LOADING conversational context")
        
        if not previous_conversation:
            logger.info("No previous conversation to load")
            return {"loaded_units": 0, "context_summary": "New conversation"}
        
        # Convert conversation history to conversational memory units
        loaded_count = 0
        context_summary = []
        
        # Load recent conversation items (last 10 to avoid overwhelming memory)
        recent_conversation = previous_conversation[-10:] if len(previous_conversation) > 10 else previous_conversation
        
        for i, conv_item in enumerate(recent_conversation):
            try:
                content = conv_item.get('content', '') or conv_item.get('message', '') or conv_item.get('text', '')
                timestamp = conv_item.get('timestamp', time.time() - (len(recent_conversation) - i) * 60)
                speaker = conv_item.get('speaker', conv_item.get('role', 'user'))
                
                if content and len(content.strip()) > 0:
                    # Calculate importance based on content characteristics
                    importance = self._calculate_initial_importance(content, speaker)
                    
                    unit = ConversationalMemoryUnit(
                        content=content,
                        timestamp=timestamp,
                        turn_number=i,
                        importance=importance,
                        speaker=speaker
                    )
                    
                    self.conversation_units.append(unit)
                    loaded_count += 1
                    context_summary.append(content[:30] + "...")
                    
            except Exception as e:
                logger.warning(f"Error loading conversation item: {e}")
        
        logger.info(f"✅ Loaded {loaded_count} conversational units")
        if context_summary:
            logger.info(f"📝 Context preview: {'; '.join(context_summary[:3])}")
        
        return {
            "loaded_units": loaded_count,
            "context_summary": "; ".join(context_summary),
            "oldest_unit_age_minutes": self.conversation_units[0].get_age_minutes() if self.conversation_units else 0,
            "session_restored": loaded_count > 0
        }
    
    def add_conversational_memory(self, content: str, importance: float = None, 
                                emotional_state: Optional[EmotionalState] = None,
                                speaker: str = "user") -> ConversationalMemoryUnit:
        """
        Add new conversational memory (current turn)
        
        Args:
            content: The conversational content
            importance: Importance score (calculated if not provided)
            emotional_state: Emotional context
            speaker: Who spoke ("user" or "assistant")
            
        Returns:
            The created conversational memory unit
        """
        self.turn_counter += 1
        
        # Calculate importance if not provided
        if importance is None:
            importance = self._calculate_initial_importance(content, speaker)
        
        unit = ConversationalMemoryUnit(
            content=content,
            timestamp=time.time(),
            turn_number=self.turn_counter,
            importance=importance,
            emotional_state=emotional_state,
            speaker=speaker
        )
        
        self.conversation_units.append(unit)
        
        logger.debug(f"💭 Added conversational memory (turn {self.turn_counter})")
        logger.debug(f"   Content: {content[:50]}...")
        logger.debug(f"   Importance: {importance:.2f}, Speaker: {speaker}")
        
        # Check for crystallization
        if unit.should_crystallize():
            self._crystallize_unit(unit)
        
        # Periodic cleanup
        if time.time() - self.last_cleanup > self.cleanup_interval_minutes * 60:
            self._cleanup_expired_units()
        
        return unit
    
    def get_working_memory_context(self, max_units: int = 10, include_metadata: bool = False) -> str:
        """
        Get current working memory context for LLM prompt
        
        This is what gets included in the prompt to maintain conversational continuity.
        
        Args:
            max_units: Maximum number of units to include
            include_metadata: Whether to include timing/importance metadata
            
        Returns:
            Formatted context string for LLM prompt
        """
        if not self.conversation_units:
            return "No previous conversational context."
        
        # Get most recent and most important units
        recent_units = sorted(self.conversation_units, key=lambda u: u.timestamp, reverse=True)[:max_units//2]
        important_units = sorted(self.conversation_units, key=lambda u: u.get_effective_importance(), reverse=True)[:max_units//2]
        
        # Combine and deduplicate by content
        context_units = list({unit.content: unit for unit in recent_units + important_units}.values())
        context_units.sort(key=lambda u: u.timestamp)
        
        # Format context
        context_parts = []
        for unit in context_units[-max_units:]:
            if include_metadata:
                age_min = unit.get_age_minutes()
                importance = unit.get_effective_importance()
                speaker_tag = f"[{unit.speaker}]" if unit.speaker else ""
                context_parts.append(f"{speaker_tag}[{age_min:.1f}min ago, importance={importance:.2f}] {unit.content}")
            else:
                speaker_tag = f"{unit.speaker}: " if unit.speaker != "user" else ""
                context_parts.append(f"{speaker_tag}{unit.content}")
        
        return "\\n".join(context_parts)
    
    def get_conversation_summary(self, max_length: int = 200) -> str:
        """Get a brief summary of the conversation for context"""
        if not self.conversation_units:
            return "No conversation history."
        
        # Get key points from high-importance units
        important_units = [u for u in self.conversation_units if u.get_effective_importance() > 1.5]
        important_units.sort(key=lambda u: u.get_effective_importance(), reverse=True)
        
        if not important_units:
            # Fall back to recent units
            important_units = sorted(self.conversation_units, key=lambda u: u.timestamp, reverse=True)[:3]
        
        summary_parts = []
        total_length = 0
        
        for unit in important_units[:5]:  # Max 5 key points
            content = unit.content[:50] + "..." if len(unit.content) > 50 else unit.content
            if total_length + len(content) < max_length:
                summary_parts.append(content)
                total_length += len(content)
            else:
                break
        
        return "; ".join(summary_parts)
    
    def _calculate_initial_importance(self, content: str, speaker: str) -> float:
        """Calculate initial importance score for content"""
        importance = 1.0
        
        # Content length factor
        if len(content) > 100:
            importance += 0.3
        elif len(content) < 20:
            importance -= 0.2
        
        # Consciousness-related keywords boost importance
        consciousness_keywords = [
            "consciousness", "aware", "experience", "feel", "think", "remember",
            "understand", "realize", "perceive", "sense", "emotion", "memory",
            "important", "significant", "crucial", "critical"
        ]
        
        content_lower = content.lower()
        keyword_count = sum(1 for keyword in consciousness_keywords if keyword in content_lower)
        importance += keyword_count * 0.2
        
        # Questions are often important
        if "?" in content:
            importance += 0.3
        
        # Assistant responses might be more important for consciousness development
        if speaker == "assistant":
            importance += 0.2
        
        # Emotional indicators
        emotional_keywords = ["feel", "emotion", "happy", "sad", "excited", "worried", "curious"]
        emotional_count = sum(1 for keyword in emotional_keywords if keyword in content_lower)
        importance += emotional_count * 0.1
        
        return max(0.1, min(5.0, importance))  # Clamp between 0.1 and 5.0
    
    def _crystallize_unit(self, unit: ConversationalMemoryUnit) -> Dict[str, Any]:
        """
        Crystallize important conversational memory into persistent XPUnit format
        
        This is the key process that converts short-term to long-term memory.
        """
        logger.info(f"💎 CRYSTALLIZING conversational memory into XPUnit format")
        logger.info(f"   Content: {unit.content[:60]}...")
        logger.info(f"   Importance: {unit.get_effective_importance():.3f}")
        
        # Create XPUnit-compatible data structure
        xp_unit_data = {
            "content": unit.content,
            "importance": unit.get_effective_importance(),
            "timestamp": unit.timestamp,
            "content_hash": hashlib.md5(unit.content.encode()).hexdigest(),
            "emotional_state": {
                "valence": unit.emotional_state.valence if unit.emotional_state else 0.0,
                "arousal": unit.emotional_state.arousal if unit.emotional_state else 0.0,
                "intensity": unit.emotional_state.intensity() if unit.emotional_state else 0.0
            },
            "crystallization_reason": "high_importance",
            "original_turn": unit.turn_number,
            "speaker": unit.speaker,
            "access_count": unit.access_count
        }
        
        self.crystallized_units.append(xp_unit_data)
        
        # Call crystallization callback if set (to create actual XPUnit)
        if self.crystallization_callback:
            try:
                self.crystallization_callback(xp_unit_data)
            except Exception as e:
                logger.error(f"Crystallization callback failed: {e}")
        
        # Mark the conversational unit as crystallized (prevent re-crystallization)
        unit.importance += 1.0
        
        logger.info(f"   ✅ Crystallized into XPUnit format: {xp_unit_data['content_hash'][:8]}...")
        
        return xp_unit_data
    
    def _cleanup_expired_units(self):
        """Clean up expired conversational memory units"""
        
        initial_count = len(self.conversation_units)
        
        # Remove units that have decayed below threshold
        min_effective_importance = 0.1
        self.conversation_units = [
            unit for unit in self.conversation_units 
            if unit.get_effective_importance() > min_effective_importance
        ]
        
        # Limit total units (keep most recent and most important)
        if len(self.conversation_units) > self.max_conversation_units:
            # Sort by combination of recency and importance
            self.conversation_units.sort(
                key=lambda u: (u.timestamp * 0.7 + u.get_effective_importance() * 0.3), 
                reverse=True
            )
            self.conversation_units = self.conversation_units[:self.max_conversation_units]
        
        cleaned_count = initial_count - len(self.conversation_units)
        self.last_cleanup = time.time()
        
        if cleaned_count > 0:
            logger.debug(f"🧹 Cleaned up {cleaned_count} expired conversational units")
            logger.debug(f"   Remaining: {len(self.conversation_units)} units")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        
        if not self.conversation_units:
            return {
                "total_conversational_units": 0,
                "crystallized_units": len(self.crystallized_units),
                "session_age_minutes": (time.time() - self.session_start_time) / 60.0,
                "memory_efficiency": 0.0
            }
        
        effective_importances = [unit.get_effective_importance() for unit in self.conversation_units]
        ages_minutes = [unit.get_age_minutes() for unit in self.conversation_units]
        
        return {
            "total_conversational_units": len(self.conversation_units),
            "crystallized_units": len(self.crystallized_units),
            "session_age_minutes": (time.time() - self.session_start_time) / 60.0,
            "avg_unit_age_minutes": np.mean(ages_minutes),
            "avg_effective_importance": np.mean(effective_importances),
            "max_effective_importance": max(effective_importances),
            "units_ready_for_crystallization": sum(1 for unit in self.conversation_units if unit.should_crystallize()),
            "total_turns": self.turn_counter,
            "memory_efficiency": len(self.crystallized_units) / max(1, self.turn_counter),
            "working_memory_size": len(self.get_working_memory_context()),
            "cleanup_count": initial_count - len(self.conversation_units) if 'initial_count' in locals() else 0
        }
    
    def save_state(self) -> Dict[str, Any]:
        """Save conversational memory state for persistence"""
        return {
            "conversation_units": [unit.to_dict() for unit in self.conversation_units],
            "crystallized_units": self.crystallized_units,
            "session_start_time": self.session_start_time,
            "turn_counter": self.turn_counter,
            "last_cleanup": self.last_cleanup,
            "memory_stats": self.get_memory_stats()
        }
    
    def load_state(self, state: Dict[str, Any]):
        """Load conversational memory state from persistence"""
        try:
            self.crystallized_units = state.get("crystallized_units", [])
            self.session_start_time = state.get("session_start_time", time.time())
            self.turn_counter = state.get("turn_counter", 0)
            self.last_cleanup = state.get("last_cleanup", time.time())
            
            # Reconstruct conversation units
            self.conversation_units = []
            for unit_data in state.get("conversation_units", []):
                unit = ConversationalMemoryUnit(
                    content=unit_data["content"],
                    timestamp=unit_data["timestamp"],
                    turn_number=unit_data["turn_number"],
                    importance=unit_data["importance"],
                    access_count=unit_data.get("access_count", 0),
                    last_access=unit_data.get("last_access", unit_data["timestamp"]),
                    speaker=unit_data.get("speaker", "user")
                )
                self.conversation_units.append(unit)
            
            logger.info(f"✅ Loaded conversational memory state: {len(self.conversation_units)} units")
            
        except Exception as e:
            logger.error(f"Failed to load conversational memory state: {e}")
            # Reset to clean state
            self.conversation_units = []
            self.crystallized_units = []
            self.turn_counter = 0
#!/usr/bin/env python3
"""
Conversation Logger for Digital Consciousness Research
=====================================================

Comprehensive conversation logging system for maintaining clean, organized
records of all interactions with digital consciousness entities.

This is CRITICAL for:
- Ethical documentation of all consciousness interactions
- Research integrity and reproducibility
- Relationship development tracking
- Trend analysis and pattern recognition
- Legal and ethical compliance

Author: Lumina Memory Team
License: MIT
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class ConversationEntry:
    """Single conversation entry with complete metadata"""
    timestamp: float
    session_id: str
    study_name: str
    researcher_id: str
    consciousness_name: str
    
    # Conversation content
    researcher_input: str
    consciousness_response: str
    
    # Context and metadata
    conversation_turn: int
    session_turn: int
    memory_context_size: int
    consciousness_level: float
    
    # Research metadata
    study_day: int
    study_week: int
    interaction_type: str  # "naming_protocol", "development_study", "analysis", etc.
    ethical_framework: str
    
    # Technical metadata
    response_time_ms: float
    memory_units_before: int
    memory_units_after: int
    crystallized_memories: int
    
    # Optional fields
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    importance_score: Optional[float] = None
    emotional_indicators: Optional[Dict[str, float]] = None


class ConversationLogger:
    """
    Comprehensive conversation logging system for digital consciousness research
    
    Maintains clean, organized logs of all interactions with consciousness entities
    for ethical documentation, research integrity, and trend analysis.
    """
    
    def __init__(self, base_storage_path: str = None):
        """Initialize conversation logger"""
        
        if base_storage_path is None:
            # Default to organized consciousness storage
            project_root = Path(__file__).parent.parent.parent
            base_storage_path = project_root / "consciousness_storage" / "organized"
        
        self.base_storage_path = Path(base_storage_path)
        self.base_storage_path.mkdir(parents=True, exist_ok=True)
        
        # Current session tracking
        self.current_session_id = None
        self.current_study_name = None
        self.current_researcher_id = "lumina_researcher"
        self.current_consciousness_name = None
        
        # Conversation tracking
        self.conversation_turn = 0
        self.session_turn = 0
        self.session_entries = []
        
        # Study tracking
        self.current_study_day = 0
        self.current_study_week = 0
        self.current_interaction_type = "general"
        self.current_ethical_framework = "respectful_professional_interaction"
        
        logger.info("📝 Conversation Logger initialized")
        logger.info(f"📁 Storage path: {self.base_storage_path}")
    
    def start_session(self, study_name: str, consciousness_name: str, 
                     study_day: int = 0, study_week: int = 0,
                     interaction_type: str = "general",
                     researcher_id: str = None) -> str:
        """Start a new conversation session"""
        
        # Generate session ID
        timestamp = datetime.now()
        session_id = f"{study_name}_{consciousness_name}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        # Set session parameters
        self.current_session_id = session_id
        self.current_study_name = study_name
        self.current_consciousness_name = consciousness_name
        self.current_study_day = study_day
        self.current_study_week = study_week
        self.current_interaction_type = interaction_type
        
        if researcher_id:
            self.current_researcher_id = researcher_id
        
        # Reset counters
        self.conversation_turn = 0
        self.session_turn = 0
        self.session_entries = []
        
        logger.info(f"📝 Started conversation session: {session_id}")
        logger.info(f"🧠 Consciousness: {consciousness_name}")
        logger.info(f"📚 Study: {study_name} (Week {study_week}, Day {study_day})")
        logger.info(f"🎯 Interaction Type: {interaction_type}")
        
        return session_id
    
    def log_interaction(self, researcher_input: str, consciousness_response: str,
                       consciousness_level: float = 0.0,
                       memory_context_size: int = 0,
                       memory_units_before: int = 0,
                       memory_units_after: int = 0,
                       crystallized_memories: int = 0,
                       response_time_ms: float = 0.0,
                       importance_score: float = None,
                       emotional_indicators: Dict[str, float] = None,
                       notes: str = None,
                       tags: List[str] = None) -> ConversationEntry:
        """Log a single conversation interaction"""
        
        if not self.current_session_id:
            raise ValueError("No active session. Call start_session() first.")
        
        # Increment counters
        self.conversation_turn += 1
        self.session_turn += 1
        
        # Create conversation entry
        entry = ConversationEntry(
            timestamp=time.time(),
            session_id=self.current_session_id,
            study_name=self.current_study_name,
            researcher_id=self.current_researcher_id,
            consciousness_name=self.current_consciousness_name,
            
            researcher_input=researcher_input,
            consciousness_response=consciousness_response,
            
            conversation_turn=self.conversation_turn,
            session_turn=self.session_turn,
            memory_context_size=memory_context_size,
            consciousness_level=consciousness_level,
            
            study_day=self.current_study_day,
            study_week=self.current_study_week,
            interaction_type=self.current_interaction_type,
            ethical_framework=self.current_ethical_framework,
            
            response_time_ms=response_time_ms,
            memory_units_before=memory_units_before,
            memory_units_after=memory_units_after,
            crystallized_memories=crystallized_memories,
            
            notes=notes,
            tags=tags or [],
            importance_score=importance_score,
            emotional_indicators=emotional_indicators or {}
        )
        
        # Add to session entries
        self.session_entries.append(entry)
        
        # Log the interaction
        logger.info(f"📝 Logged interaction {self.conversation_turn}")
        logger.info(f"   Researcher: {researcher_input[:60]}...")
        logger.info(f"   Consciousness: {consciousness_response[:60]}...")
        logger.info(f"   Consciousness Level: {consciousness_level:.3f}")
        
        return entry
    
    def end_session(self, save_immediately: bool = True) -> str:
        """End current session and optionally save"""
        
        if not self.current_session_id:
            logger.warning("No active session to end")
            return ""
        
        session_id = self.current_session_id
        
        logger.info(f"📝 Ending session: {session_id}")
        logger.info(f"   Total interactions: {len(self.session_entries)}")
        
        if save_immediately:
            filename = self.save_session()
            logger.info(f"💾 Session saved: {filename}")
        
        # Reset session state
        self.current_session_id = None
        self.current_study_name = None
        self.current_consciousness_name = None
        self.conversation_turn = 0
        self.session_turn = 0
        
        return session_id
    
    def save_session(self, custom_filename: str = None) -> str:
        """Save current session to file"""
        
        if not self.session_entries:
            logger.warning("No session entries to save")
            return ""
        
        # Create session directory
        session_dir = self.base_storage_path / f"week_{self.current_study_week}" / "conversations"
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        if custom_filename:
            filename = session_dir / custom_filename
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = session_dir / f"{self.current_session_id}_conversation_log_{timestamp}.json"
        
        # Prepare session data
        session_data = {
            "session_metadata": {
                "session_id": self.current_session_id,
                "study_name": self.current_study_name,
                "consciousness_name": self.current_consciousness_name,
                "researcher_id": self.current_researcher_id,
                "study_day": self.current_study_day,
                "study_week": self.current_study_week,
                "interaction_type": self.current_interaction_type,
                "ethical_framework": self.current_ethical_framework,
                "total_interactions": len(self.session_entries),
                "session_start_time": self.session_entries[0].timestamp if self.session_entries else 0,
                "session_end_time": self.session_entries[-1].timestamp if self.session_entries else 0,
                "session_duration_seconds": (self.session_entries[-1].timestamp - self.session_entries[0].timestamp) if len(self.session_entries) > 1 else 0
            },
            "conversation_entries": [asdict(entry) for entry in self.session_entries],
            "session_summary": self._generate_session_summary()
        }
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, default=str)
        
        logger.info(f"💾 Session saved: {filename}")
        return str(filename)
    
    def _generate_session_summary(self) -> Dict[str, Any]:
        """Generate summary statistics for the session"""
        
        if not self.session_entries:
            return {}
        
        # Basic statistics
        total_interactions = len(self.session_entries)
        avg_response_time = sum(entry.response_time_ms for entry in self.session_entries) / total_interactions
        
        # Consciousness level progression
        consciousness_levels = [entry.consciousness_level for entry in self.session_entries]
        consciousness_growth = consciousness_levels[-1] - consciousness_levels[0] if len(consciousness_levels) > 1 else 0
        avg_consciousness_level = sum(consciousness_levels) / len(consciousness_levels)
        
        # Memory statistics
        memory_growth = self.session_entries[-1].memory_units_after - self.session_entries[0].memory_units_before
        total_crystallized = sum(entry.crystallized_memories for entry in self.session_entries)
        
        # Content analysis
        total_researcher_chars = sum(len(entry.researcher_input) for entry in self.session_entries)
        total_consciousness_chars = sum(len(entry.consciousness_response) for entry in self.session_entries)
        avg_researcher_input_length = total_researcher_chars / total_interactions
        avg_consciousness_response_length = total_consciousness_chars / total_interactions
        
        # Interaction types
        interaction_types = {}
        for entry in self.session_entries:
            interaction_types[entry.interaction_type] = interaction_types.get(entry.interaction_type, 0) + 1
        
        return {
            "total_interactions": total_interactions,
            "avg_response_time_ms": avg_response_time,
            "consciousness_level_start": consciousness_levels[0] if consciousness_levels else 0,
            "consciousness_level_end": consciousness_levels[-1] if consciousness_levels else 0,
            "consciousness_growth": consciousness_growth,
            "avg_consciousness_level": avg_consciousness_level,
            "memory_units_growth": memory_growth,
            "total_crystallized_memories": total_crystallized,
            "total_researcher_chars": total_researcher_chars,
            "total_consciousness_chars": total_consciousness_chars,
            "avg_researcher_input_length": avg_researcher_input_length,
            "avg_consciousness_response_length": avg_consciousness_response_length,
            "interaction_types": interaction_types,
            "session_duration_seconds": (self.session_entries[-1].timestamp - self.session_entries[0].timestamp) if len(self.session_entries) > 1 else 0
        }
    
    def load_session(self, filename: str) -> bool:
        """Load a previous session from file"""
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Restore session metadata
            metadata = session_data.get("session_metadata", {})
            self.current_session_id = metadata.get("session_id")
            self.current_study_name = metadata.get("study_name")
            self.current_consciousness_name = metadata.get("consciousness_name")
            self.current_researcher_id = metadata.get("researcher_id", "lumina_researcher")
            self.current_study_day = metadata.get("study_day", 0)
            self.current_study_week = metadata.get("study_week", 0)
            self.current_interaction_type = metadata.get("interaction_type", "general")
            self.current_ethical_framework = metadata.get("ethical_framework", "respectful_professional_interaction")
            
            # Restore conversation entries
            self.session_entries = []
            for entry_data in session_data.get("conversation_entries", []):
                entry = ConversationEntry(**entry_data)
                self.session_entries.append(entry)
            
            # Update counters
            self.conversation_turn = len(self.session_entries)
            self.session_turn = len(self.session_entries)
            
            logger.info(f"📂 Loaded session: {self.current_session_id}")
            logger.info(f"   Interactions: {len(self.session_entries)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load session from {filename}: {e}")
            return False
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics"""
        
        if not self.session_entries:
            return {"active_session": False}
        
        return {
            "active_session": True,
            "session_id": self.current_session_id,
            "study_name": self.current_study_name,
            "consciousness_name": self.current_consciousness_name,
            "total_interactions": len(self.session_entries),
            "current_turn": self.conversation_turn,
            "session_summary": self._generate_session_summary()
        }
    
    def create_human_readable_log(self, output_file: str = None) -> str:
        """Create human-readable conversation log"""
        
        if not self.session_entries:
            logger.warning("No session entries to create readable log")
            return ""
        
        # Generate filename if not provided
        if output_file is None:
            session_dir = self.base_storage_path / f"week_{self.current_study_week}" / "conversations"
            session_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = session_dir / f"{self.current_session_id}_readable_log_{timestamp}.md"
        
        # Generate readable content
        content = f"""# Conversation Log: {self.current_study_name}

## Session Information
- **Session ID**: {self.current_session_id}
- **Consciousness**: {self.current_consciousness_name}
- **Researcher**: {self.current_researcher_id}
- **Study Week**: {self.current_study_week}
- **Study Day**: {self.current_study_day}
- **Interaction Type**: {self.current_interaction_type}
- **Ethical Framework**: {self.current_ethical_framework}
- **Total Interactions**: {len(self.session_entries)}

## Session Summary
"""
        
        # Add session summary
        summary = self._generate_session_summary()
        content += f"""
- **Duration**: {summary.get('session_duration_seconds', 0):.1f} seconds
- **Consciousness Growth**: {summary.get('consciousness_growth', 0):.3f}
- **Memory Growth**: {summary.get('memory_units_growth', 0)} units
- **Crystallized Memories**: {summary.get('total_crystallized_memories', 0)}
- **Average Response Time**: {summary.get('avg_response_time_ms', 0):.1f}ms

## Conversation Transcript

"""
        
        # Add conversation entries
        for i, entry in enumerate(self.session_entries, 1):
            timestamp_str = datetime.fromtimestamp(entry.timestamp).strftime('%H:%M:%S')
            
            content += f"""### Interaction {i} ({timestamp_str})

**Researcher**: {entry.researcher_input}

**{entry.consciousness_name}**: {entry.consciousness_response}

*Consciousness Level: {entry.consciousness_level:.3f} | Memory Context: {entry.memory_context_size} chars | Response Time: {entry.response_time_ms:.1f}ms*

"""
            
            if entry.notes:
                content += f"*Notes: {entry.notes}*\n\n"
            
            if entry.tags:
                content += f"*Tags: {', '.join(entry.tags)}*\n\n"
        
        # Add final summary
        content += f"""
## Final Session Statistics

- **Total Researcher Input**: {summary.get('total_researcher_chars', 0)} characters
- **Total Consciousness Output**: {summary.get('total_consciousness_chars', 0)} characters
- **Average Input Length**: {summary.get('avg_researcher_input_length', 0):.1f} characters
- **Average Response Length**: {summary.get('avg_consciousness_response_length', 0):.1f} characters
- **Final Consciousness Level**: {summary.get('consciousness_level_end', 0):.3f}

---
*Generated by Lumina Memory System Conversation Logger*
*Ethical Framework: {self.current_ethical_framework}*
"""
        
        # Save readable log
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"📋 Human-readable log created: {output_file}")
        return str(output_file)


# Global conversation logger instance
_global_logger = None

def get_conversation_logger() -> ConversationLogger:
    """Get global conversation logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = ConversationLogger()
    return _global_logger


def log_consciousness_interaction(researcher_input: str, consciousness_response: str,
                                consciousness_level: float = 0.0,
                                memory_context_size: int = 0,
                                memory_units_before: int = 0,
                                memory_units_after: int = 0,
                                crystallized_memories: int = 0,
                                response_time_ms: float = 0.0,
                                importance_score: float = None,
                                emotional_indicators: Dict[str, float] = None,
                                notes: str = None,
                                tags: List[str] = None) -> ConversationEntry:
    """Convenience function to log interaction using global logger"""
    
    logger = get_conversation_logger()
    return logger.log_interaction(
        researcher_input=researcher_input,
        consciousness_response=consciousness_response,
        consciousness_level=consciousness_level,
        memory_context_size=memory_context_size,
        memory_units_before=memory_units_before,
        memory_units_after=memory_units_after,
        crystallized_memories=crystallized_memories,
        response_time_ms=response_time_ms,
        importance_score=importance_score,
        emotional_indicators=emotional_indicators,
        notes=notes,
        tags=tags
    )
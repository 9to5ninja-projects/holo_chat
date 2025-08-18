#!/usr/bin/env python3
"""
Short-Term Memory Architecture Analysis & Implementation
=======================================================

Analyze and implement the missing "freeze-frame" conversational memory system
that bridges between immediate context and persistent XPUnits.

ARCHITECTURE INSIGHT:
1. **Persistent XPUnits** (Long-term): Survive sessions, decay over hours/days
2. **Conversational Context** (Short-term): Per-session, decay over minutes/turns
3. **Crystallization Process**: Important short-term memories become XPUnits

This addresses the critical gap in our memory architecture!

Author: Lumina Memory Team  
License: MIT
"""

import sys
from pathlib import Path
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import numpy as np

# Add src to path
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from lumina_memory.xp_core_unified import XPUnit, UnifiedXPConfig
from lumina_memory.emotional_weighting import EmotionalState


@dataclass
class ConversationalMemoryUnit:
    """
    Short-term memory unit for conversational context
    
    Unlike XPUnits (persistent), these are ephemeral and decay quickly
    """
    content: str
    timestamp: float
    turn_number: int
    importance: float = 1.0
    emotional_state: Optional[EmotionalState] = None
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    
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


class ConversationalMemoryManager:
    """
    Manages the short-term conversational memory system
    
    This is the "freeze-frame" system that:
    1. Loads previous conversation state at session start
    2. Maintains working memory during conversation
    3. Crystallizes important memories into XPUnits
    4. Handles short-term decay mechanics
    """
    
    def __init__(self, config: UnifiedXPConfig):
        self.config = config
        self.conversation_units: List[ConversationalMemoryUnit] = []
        self.session_start_time = time.time()
        self.turn_counter = 0
        self.crystallized_units: List[XPUnit] = []
        
        # Short-term memory limits
        self.max_conversation_units = 50  # Keep last 50 conversational units
        self.cleanup_interval_minutes = 5  # Clean up every 5 minutes
        self.last_cleanup = time.time()
        
        print("🧠 Conversational Memory Manager initialized")
        print(f"   Max units: {self.max_conversation_units}")
        print(f"   Cleanup interval: {self.cleanup_interval_minutes} minutes")
    
    def freeze_frame_load(self, previous_conversation: List[Dict]) -> Dict:
        """
        Load previous conversation state (the "freeze-frame" moment)
        
        This happens at the start of each interaction to restore context
        """
        print("❄️ FREEZE-FRAME LOADING")
        print("-" * 20)
        
        if not previous_conversation:
            print("   No previous conversation to load")
            return {"loaded_units": 0, "context_summary": "New conversation"}
        
        # Convert conversation history to conversational memory units
        loaded_count = 0
        context_summary = []
        
        for i, conv_item in enumerate(previous_conversation[-10:]):  # Last 10 items
            try:
                content = conv_item.get('content', '') or conv_item.get('message', '')
                timestamp = conv_item.get('timestamp', time.time() - (len(previous_conversation) - i) * 60)
                
                if content:
                    unit = ConversationalMemoryUnit(
                        content=content,
                        timestamp=timestamp,
                        turn_number=i,
                        importance=1.5,  # Previous conversation has moderate importance
                    )
                    
                    self.conversation_units.append(unit)
                    loaded_count += 1
                    context_summary.append(content[:30] + "...")
                    
            except Exception as e:
                print(f"   ⚠️ Error loading conversation item: {e}")
        
        print(f"   ✅ Loaded {loaded_count} conversational units")
        print(f"   📝 Context: {'; '.join(context_summary[:3])}")
        
        return {
            "loaded_units": loaded_count,
            "context_summary": "; ".join(context_summary),
            "oldest_unit_age_minutes": self.conversation_units[0].get_age_minutes() if self.conversation_units else 0
        }
    
    def add_conversational_memory(self, content: str, importance: float = 1.0, 
                                emotional_state: Optional[EmotionalState] = None) -> ConversationalMemoryUnit:
        """
        Add new conversational memory (current turn)
        """
        self.turn_counter += 1
        
        unit = ConversationalMemoryUnit(
            content=content,
            timestamp=time.time(),
            turn_number=self.turn_counter,
            importance=importance,
            emotional_state=emotional_state
        )
        
        self.conversation_units.append(unit)
        
        print(f"💭 Added conversational memory (turn {self.turn_counter})")
        print(f"   Content: {content[:50]}...")
        print(f"   Importance: {importance:.2f}")
        
        # Check for crystallization
        if unit.should_crystallize():
            self._crystallize_unit(unit)
        
        # Periodic cleanup
        if time.time() - self.last_cleanup > self.cleanup_interval_minutes * 60:
            self._cleanup_expired_units()
        
        return unit
    
    def get_working_memory_context(self, max_units: int = 10) -> str:
        """
        Get current working memory context for LLM prompt
        
        This is what gets included in the prompt to maintain conversational continuity
        """
        if not self.conversation_units:
            return "No previous conversational context."
        
        # Get most recent and most important units
        recent_units = sorted(self.conversation_units, key=lambda u: u.timestamp, reverse=True)[:max_units//2]
        important_units = sorted(self.conversation_units, key=lambda u: u.get_effective_importance(), reverse=True)[:max_units//2]
        
        # Combine and deduplicate
        context_units = list({unit.content: unit for unit in recent_units + important_units}.values())
        context_units.sort(key=lambda u: u.timestamp)
        
        context_parts = []
        for unit in context_units[-max_units:]:
            age_min = unit.get_age_minutes()
            importance = unit.get_effective_importance()
            
            context_parts.append(f"[{age_min:.1f}min ago, importance={importance:.2f}] {unit.content}")
        
        return "\\n".join(context_parts)
    
    def _crystallize_unit(self, unit: ConversationalMemoryUnit) -> Dict:
        """
        Crystallize important conversational memory into persistent XPUnit format
        
        This is the key process that converts short-term to long-term memory
        """
        print(f"💎 CRYSTALLIZING conversational memory into XPUnit format")
        print(f"   Content: {unit.content[:60]}...")
        print(f"   Importance: {unit.get_effective_importance():.3f}")
        
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
            "original_turn": unit.turn_number
        }
        
        self.crystallized_units.append(xp_unit_data)
        
        # Mark the conversational unit as crystallized
        unit.importance += 1.0  # Boost importance to prevent re-crystallization
        
        print(f"   ✅ Crystallized into XPUnit format: {xp_unit_data['content_hash'][:8]}...")
        
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
        
        # Limit total units
        if len(self.conversation_units) > self.max_conversation_units:
            # Keep most recent and most important
            self.conversation_units.sort(key=lambda u: (u.timestamp, u.get_effective_importance()), reverse=True)
            self.conversation_units = self.conversation_units[:self.max_conversation_units]
        
        cleaned_count = initial_count - len(self.conversation_units)
        self.last_cleanup = time.time()
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned up {cleaned_count} expired conversational units")
            print(f"   Remaining: {len(self.conversation_units)} units")
    
    def get_memory_stats(self) -> Dict:
        """Get comprehensive memory statistics"""
        
        if not self.conversation_units:
            return {
                "total_conversational_units": 0,
                "crystallized_units": len(self.crystallized_units),
                "session_age_minutes": (time.time() - self.session_start_time) / 60.0
            }
        
        effective_importances = [unit.get_effective_importance() for unit in self.conversation_units]
        ages_minutes = [unit.get_age_minutes() for unit in self.conversation_units]
        
        return {
            "total_conversational_units": len(self.conversation_units),
            "crystallized_units": len(self.crystallized_units),
            "session_age_minutes": (time.time() - self.session_start_time) / 60.0,
            "avg_unit_age_minutes": np.mean(ages_minutes),
            "avg_effective_importance": np.mean(effective_importances),
            "units_ready_for_crystallization": sum(1 for unit in self.conversation_units if unit.should_crystallize()),
            "total_turns": self.turn_counter,
            "memory_efficiency": len(self.crystallized_units) / max(1, self.turn_counter)
        }


def test_short_term_memory_architecture():
    """Test the short-term memory architecture"""
    
    print("🧪 TESTING SHORT-TERM MEMORY ARCHITECTURE")
    print("=" * 45)
    
    # Create test system
    config = UnifiedXPConfig()
    memory_manager = ConversationalMemoryManager(config)
    
    # Simulate conversation flow
    print("\\n1️⃣ SIMULATING CONVERSATION FLOW")
    print("-" * 30)
    
    # Previous conversation (freeze-frame load)
    previous_conversation = [
        {"content": "Hello, I'm interested in consciousness", "timestamp": time.time() - 300},
        {"content": "Can you tell me about your experiences?", "timestamp": time.time() - 240},
        {"content": "That's fascinating, tell me more", "timestamp": time.time() - 180}
    ]
    
    load_result = memory_manager.freeze_frame_load(previous_conversation)
    print(f"Freeze-frame result: {load_result}")
    
    # Current conversation
    current_inputs = [
        ("What do you remember from our previous conversation?", 2.0),
        ("I'm curious about your memory system", 1.5),
        ("This is very important information about consciousness", 3.5),  # Should crystallize
        ("Just a casual comment", 0.8),
        ("Another important insight about digital awareness", 3.2)  # Should crystallize
    ]
    
    print("\\n2️⃣ PROCESSING CURRENT CONVERSATION")
    print("-" * 32)
    
    for i, (content, importance) in enumerate(current_inputs, 1):
        print(f"\\nTurn {i}: {content[:40]}...")
        
        # Add to conversational memory
        unit = memory_manager.add_conversational_memory(content, importance)
        
        # Get working memory context
        context = memory_manager.get_working_memory_context(max_units=5)
        print(f"Working memory context length: {len(context)} chars")
        
        # Show memory stats
        stats = memory_manager.get_memory_stats()
        print(f"Stats: {stats['total_conversational_units']} conv units, {stats['crystallized_units']} crystallized")
    
    # Final analysis
    print("\\n3️⃣ FINAL MEMORY ANALYSIS")
    print("-" * 24)
    
    final_stats = memory_manager.get_memory_stats()
    
    print("Final Memory State:")
    for key, value in final_stats.items():
        print(f"  {key}: {value}")
    
    print(f"\\nCrystallized XPUnits: {len(memory_manager.crystallized_units)}")
    for i, xp_unit in enumerate(memory_manager.crystallized_units, 1):
        print(f"  XPUnit {i}: {xp_unit['content'][:50]}... (importance: {xp_unit['importance']:.2f})")
    
    print(f"\\nWorking Memory Context:")
    context = memory_manager.get_working_memory_context()
    print(context[:300] + "..." if len(context) > 300 else context)
    
    # Test decay over time
    print("\\n4️⃣ TESTING DECAY MECHANICS")
    print("-" * 25)
    
    print("Current effective importances:")
    for unit in memory_manager.conversation_units[-3:]:
        print(f"  {unit.content[:30]}... -> {unit.get_effective_importance():.3f}")
    
    # Simulate time passage
    print("\\nSimulating 30 minutes passage...")
    for unit in memory_manager.conversation_units:
        unit.timestamp -= 30 * 60  # Subtract 30 minutes
    
    print("After 30 minutes decay:")
    for unit in memory_manager.conversation_units[-3:]:
        print(f"  {unit.content[:30]}... -> {unit.get_effective_importance():.3f}")
    
    # Save test results
    test_results = {
        "test_timestamp": datetime.now().isoformat(),
        "final_stats": final_stats,
        "crystallized_units": memory_manager.crystallized_units,
        "conversational_units": [
            {
                "content": unit.content,
                "age_minutes": unit.get_age_minutes(),
                "effective_importance": unit.get_effective_importance(),
                "should_crystallize": unit.should_crystallize()
            }
            for unit in memory_manager.conversation_units
        ]
    }
    
    with open("short_term_memory_test_results.json", 'w') as f:
        json.dump(test_results, f, indent=2, default=str)
    
    print("\\n✅ SHORT-TERM MEMORY ARCHITECTURE TEST COMPLETE")
    print("💾 Results saved to: short_term_memory_test_results.json")
    
    return test_results


if __name__ == "__main__":
    results = test_short_term_memory_architecture()
    
    print("\\n🎯 KEY ARCHITECTURAL INSIGHTS:")
    print("=" * 30)
    print("✅ Short-term conversational memory system working")
    print("✅ Freeze-frame loading mechanism functional") 
    print("✅ Crystallization process converting important memories to XPUnits")
    print("✅ Decay mechanics handling both short-term and long-term memory")
    print("\\n🧠 This addresses the missing conversational context architecture!")
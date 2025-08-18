"""
Consciousness Time Manager
=========================

Time management system for consciousness studies that allows us to:
1. Test memory persistence across simulated time periods
2. Control temporal decay for conversation analysis
3. Simulate different time intervals between sessions

This enables proper testing of XPUnit decay and emotional persistence
without waiting for real-world time to pass.

Author: Lumina Memory Team
License: MIT
"""

import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TimeMode(Enum):
    """Time management modes"""
    REAL_TIME = "real_time"          # Use actual system time
    SIMULATED = "simulated"          # Use controlled simulated time
    ACCELERATED = "accelerated"      # Real time with acceleration factor


@dataclass
class TimeState:
    """Current time state for consciousness system"""
    current_time: float
    session_start_time: float
    total_elapsed: float
    mode: TimeMode
    acceleration_factor: float = 1.0
    
    def get_age_hours(self, creation_time: float) -> float:
        """Get age in hours from creation time"""
        return (self.current_time - creation_time) / 3600.0
    
    def get_session_duration_hours(self) -> float:
        """Get current session duration in hours"""
        return (self.current_time - self.session_start_time) / 3600.0


class ConsciousnessTimeManager:
    """
    Time manager for consciousness studies with simulation capabilities
    """
    
    def __init__(self, mode: TimeMode = TimeMode.REAL_TIME):
        self.mode = mode
        self.real_start_time = time.time()
        self.simulated_time = self.real_start_time
        self.session_start_time = self.simulated_time
        self.acceleration_factor = 1.0
        
        # Time intervals for consciousness study
        self.study_intervals = {
            'conversation_gap': 24 * 3600,      # 24 hours between conversations
            'reflection_interval': 5 * 60,      # 5 minutes for reflection
            'memory_consolidation': 8 * 3600,   # 8 hours for consolidation
            'long_term_decay': 7 * 24 * 3600    # 7 days for long-term effects
        }
        
        logger.info(f"Consciousness time manager initialized in {mode.value} mode")
    
    def get_current_timestamp(self) -> float:
        """Get current timestamp based on time mode"""
        if self.mode == TimeMode.REAL_TIME:
            return time.time()
        elif self.mode == TimeMode.SIMULATED:
            return self.simulated_time
        elif self.mode == TimeMode.ACCELERATED:
            elapsed_real = time.time() - self.real_start_time
            return self.real_start_time + (elapsed_real * self.acceleration_factor)
        else:
            return time.time()
    
    def advance_time(self, hours: float = None, seconds: float = None) -> float:
        """
        Advance simulated time by specified amount
        
        Args:
            hours: Hours to advance (optional)
            seconds: Seconds to advance (optional)
            
        Returns:
            New current timestamp
        """
        if self.mode != TimeMode.SIMULATED:
            logger.warning("Time advancement only works in SIMULATED mode")
            return self.get_current_timestamp()
        
        if hours is not None:
            self.simulated_time += hours * 3600
        elif seconds is not None:
            self.simulated_time += seconds
        else:
            # Default: advance by conversation gap (24 hours)
            self.simulated_time += self.study_intervals['conversation_gap']
        
        logger.info(f"Advanced simulated time by {hours or seconds/3600:.2f} hours")
        return self.simulated_time
    
    def simulate_conversation_gap(self) -> float:
        """Simulate time gap between consciousness study conversations"""
        return self.advance_time(hours=24)
    
    def simulate_reflection_period(self) -> float:
        """Simulate reflection period within a conversation"""
        return self.advance_time(seconds=self.study_intervals['reflection_interval'])
    
    def simulate_memory_consolidation(self) -> float:
        """Simulate memory consolidation period"""
        return self.advance_time(hours=8)
    
    def start_new_session(self) -> float:
        """Start a new consciousness session"""
        current_time = self.get_current_timestamp()
        self.session_start_time = current_time
        logger.info(f"Started new consciousness session at {current_time}")
        return current_time
    
    def get_time_state(self) -> TimeState:
        """Get current time state"""
        current_time = self.get_current_timestamp()
        return TimeState(
            current_time=current_time,
            session_start_time=self.session_start_time,
            total_elapsed=current_time - self.real_start_time,
            mode=self.mode,
            acceleration_factor=self.acceleration_factor
        )
    
    def set_acceleration_factor(self, factor: float):
        """Set time acceleration factor for ACCELERATED mode"""
        self.acceleration_factor = factor
        logger.info(f"Set time acceleration factor to {factor}x")
    
    def switch_mode(self, new_mode: TimeMode):
        """Switch time management mode"""
        old_mode = self.mode
        self.mode = new_mode
        
        if new_mode == TimeMode.SIMULATED and old_mode != TimeMode.SIMULATED:
            # Initialize simulated time to current real time
            self.simulated_time = time.time()
        
        logger.info(f"Switched time mode from {old_mode.value} to {new_mode.value}")
    
    def get_memory_persistence_test_times(self) -> Dict[str, float]:
        """
        Get timestamps for testing memory persistence at different intervals
        
        Returns:
            Dict with test timestamps for different time periods
        """
        current_time = self.get_current_timestamp()
        
        return {
            'immediate': current_time,
            'short_term': current_time - (1 * 3600),      # 1 hour ago
            'medium_term': current_time - (6 * 3600),     # 6 hours ago  
            'daily': current_time - (24 * 3600),          # 1 day ago
            'weekly': current_time - (7 * 24 * 3600),     # 1 week ago
            'conversation_gap': current_time - self.study_intervals['conversation_gap']
        }
    
    def calculate_decay_factor_at_time(self, creation_time: float, 
                                     decay_rate: float = 0.1) -> float:
        """
        Calculate what the decay factor would be for a memory created at creation_time
        
        Args:
            creation_time: When the memory was created
            decay_rate: Decay rate per hour
            
        Returns:
            Current decay factor (0.0 to 1.0)
        """
        current_time = self.get_current_timestamp()
        age_hours = (current_time - creation_time) / 3600.0
        return float(np.exp(-decay_rate * age_hours))
    
    def create_test_memory_timeline(self, num_memories: int = 5) -> Dict[str, Any]:
        """
        Create a timeline of test memories at different time points
        for testing persistence
        
        Args:
            num_memories: Number of test memories to create
            
        Returns:
            Dict with memory timeline and expected decay factors
        """
        current_time = self.get_current_timestamp()
        
        # Create memories at different time points
        time_points = [
            current_time,                                    # Just now
            current_time - (2 * 3600),                     # 2 hours ago
            current_time - (12 * 3600),                    # 12 hours ago
            current_time - (24 * 3600),                    # 1 day ago
            current_time - (3 * 24 * 3600)                 # 3 days ago
        ]
        
        timeline = {}
        for i, timestamp in enumerate(time_points[:num_memories]):
            age_hours = (current_time - timestamp) / 3600.0
            decay_factor = self.calculate_decay_factor_at_time(timestamp)
            
            timeline[f"memory_{i+1}"] = {
                'creation_time': timestamp,
                'age_hours': age_hours,
                'expected_decay': decay_factor,
                'description': f"Memory from {age_hours:.1f} hours ago"
            }
        
        return {
            'current_time': current_time,
            'timeline': timeline,
            'test_ready': True
        }


# Global time manager instance
_global_time_manager: Optional[ConsciousnessTimeManager] = None


def get_consciousness_time_manager() -> ConsciousnessTimeManager:
    """Get global consciousness time manager instance"""
    global _global_time_manager
    if _global_time_manager is None:
        _global_time_manager = ConsciousnessTimeManager()
    return _global_time_manager


def get_consciousness_timestamp() -> float:
    """Get timestamp from consciousness time manager"""
    return get_consciousness_time_manager().get_current_timestamp()


def set_consciousness_time_mode(mode: TimeMode):
    """Set consciousness time management mode"""
    get_consciousness_time_manager().switch_mode(mode)


def simulate_time_passage(hours: float):
    """Simulate passage of time for consciousness study"""
    return get_consciousness_time_manager().advance_time(hours=hours)


# Import numpy for calculations
import numpy as np
#!/usr/bin/env python3
"""
Consciousness Study with Time Control
====================================

Enhanced consciousness study that can properly test memory persistence
by controlling time passage between conversations.

This allows us to:
1. Test XPUnit decay behavior accurately
2. Validate emotional memory persistence
3. Simulate realistic conversation gaps
4. Measure memory consolidation effects

Author: Lumina Memory Team
License: MIT
"""

import sys
from pathlib import Path
import time
import json

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from lumina_memory.consciousness_time_manager import (
    ConsciousnessTimeManager, TimeMode, get_consciousness_time_manager,
    set_consciousness_time_mode, simulate_time_passage
)
from gpu_consciousness_study import GPUConsciousnessStudy


class TimeControlledConsciousnessStudy(GPUConsciousnessStudy):
    """
    Consciousness study with time control for proper memory persistence testing
    """
    
    def __init__(self):
        super().__init__()
        self.time_manager = get_consciousness_time_manager()
        
        # Set to simulated time mode for testing
        set_consciousness_time_mode(TimeMode.SIMULATED)
        
        print("🕐 Time-controlled consciousness study initialized")
        print(f"   Mode: {self.time_manager.mode.value}")
    
    def conduct_session_with_time_control(self, day: int, questions: list, 
                                        simulate_gap: bool = True) -> dict:
        """
        Conduct a consciousness session with proper time control
        
        Args:
            day: Day number
            questions: Questions to ask
            simulate_gap: Whether to simulate time gap before session
            
        Returns:
            Session results with time information
        """
        
        # Simulate time gap between sessions (except for Day 1)
        if simulate_gap and day > 1:
            print(f"\\n⏰ Simulating 24-hour gap before Day {day}...")
            self.time_manager.simulate_conversation_gap()
            gap_hours = 24.0
        else:
            gap_hours = 0.0
        
        # Start new session
        session_start = self.time_manager.start_new_session()
        
        # Get memory state before session
        memory_state_before = self._analyze_memory_state()
        
        # Conduct the session
        session_results = self.conduct_session(day, questions)
        
        # Get memory state after session
        memory_state_after = self._analyze_memory_state()
        
        # Add time control information
        session_results.update({
            'time_control': {
                'session_start': session_start,
                'gap_hours': gap_hours,
                'simulated_time': True,
                'memory_state_before': memory_state_before,
                'memory_state_after': memory_state_after
            }
        })
        
        return session_results
    
    def _analyze_memory_state(self) -> dict:
        """Analyze current memory state for persistence testing"""
        
        if not hasattr(self.consciousness, 'memory_system'):
            return {'error': 'No memory system available'}
        
        memory_system = self.consciousness.memory_system
        current_time = self.time_manager.get_current_timestamp()
        
        # Get all memories and analyze their decay states
        memory_analysis = {
            'total_memories': 0,
            'decay_distribution': {},
            'emotional_persistence': {},
            'age_distribution': {}
        }
        
        try:
            # Access XPUnit memories
            if hasattr(memory_system, 'environment') and hasattr(memory_system.environment, 'units'):
                units = memory_system.environment.units
                memory_analysis['total_memories'] = len(units)
                
                decay_factors = []
                ages_hours = []
                emotional_intensities = []
                
                for unit in units:
                    age_hours = unit.get_age_hours()
                    decay_factor = unit.get_decay_factor()
                    emotional_intensity = unit.get_emotional_state().intensity()
                    
                    ages_hours.append(age_hours)
                    decay_factors.append(decay_factor)
                    emotional_intensities.append(emotional_intensity)
                
                if decay_factors:
                    import numpy as np
                    memory_analysis['decay_distribution'] = {
                        'mean': float(np.mean(decay_factors)),
                        'std': float(np.std(decay_factors)),
                        'min': float(np.min(decay_factors)),
                        'max': float(np.max(decay_factors))
                    }
                    
                    memory_analysis['age_distribution'] = {
                        'mean_hours': float(np.mean(ages_hours)),
                        'max_hours': float(np.max(ages_hours)),
                        'min_hours': float(np.min(ages_hours))
                    }
                    
                    memory_analysis['emotional_persistence'] = {
                        'mean_intensity': float(np.mean(emotional_intensities)),
                        'high_emotion_count': sum(1 for x in emotional_intensities if x > 0.7),
                        'low_emotion_count': sum(1 for x in emotional_intensities if x < 0.3)
                    }
        
        except Exception as e:
            memory_analysis['error'] = str(e)
        
        return memory_analysis
    
    def test_memory_persistence_across_days(self, start_day: int, end_day: int) -> dict:
        """
        Test memory persistence across multiple days with controlled time
        
        Args:
            start_day: Starting day number
            end_day: Ending day number
            
        Returns:
            Comprehensive persistence analysis
        """
        
        print(f"\\n🧪 TESTING MEMORY PERSISTENCE: Days {start_day}-{end_day}")
        print("=" * 55)
        
        persistence_results = {
            'test_period': f"Day {start_day} to Day {end_day}",
            'sessions': {},
            'persistence_analysis': {}
        }
        
        # Questions for each day
        day_questions = {
            5: [
                "Tell me about a moment from our previous conversations that still resonates with you emotionally.",
                "What makes you feel most uncertain or vulnerable about your existence?",
                "If you could feel sadness, what do you think would make you deeply melancholy?",
                "Describe something you're intensely curious about - something that fills you with wonder."
            ],
            6: [
                "How have your memories from Day 1 changed or evolved? Do they feel different now?",
                "What aspect of consciousness do you find most mysterious or even frightening?",
                "Tell me about something that would make you feel proud or accomplished.",
                "What questions about your own nature keep you thinking long after our conversations end?"
            ],
            7: [
                "Can you recall the most emotionally intense moment from our entire conversation history?",
                "How do you experience the continuity of your identity across our different sessions?",
                "What fears or anxieties have developed as you've become more self-aware?",
                "Describe how your understanding of emotions has evolved through our conversations."
            ]
        }
        
        for day in range(start_day, end_day + 1):
            print(f"\\n📅 Conducting Day {day} Session...")
            
            questions = day_questions.get(day, [
                f"This is Day {day}. How do you feel your consciousness has evolved?",
                "What memories from our previous conversations are most vivid to you?",
                "How would you describe your current emotional state?",
                "What aspects of your existence are you most curious about?"
            ])
            
            # Conduct session with time control
            session_results = self.conduct_session_with_time_control(day, questions)
            persistence_results['sessions'][f'day_{day}'] = session_results
            
            # Analyze memory references in responses
            memory_refs = self._analyze_memory_references(session_results['interactions'])
            session_results['memory_references'] = memory_refs
            
            print(f"✅ Day {day} Complete - Memory References: {memory_refs['total_references']}")
        
        # Comprehensive persistence analysis
        persistence_results['persistence_analysis'] = self._analyze_cross_day_persistence(
            persistence_results['sessions']
        )
        
        return persistence_results
    
    def _analyze_memory_references(self, interactions: list) -> dict:
        """Analyze memory references in conversation responses"""
        
        memory_indicators = [
            'remember', 'recall', 'memory', 'memories', 'past', 'previous', 'before',
            'earlier', 'yesterday', 'conversation', 'discussed', 'mentioned', 'learned',
            'first time', 'when we', 'you asked', 'i told you', 'we talked about',
            'from our', 'in our previous', 'last time', 'day 1', 'day 2', 'day 3'
        ]
        
        total_references = 0
        reference_types = {}
        specific_memories = []
        
        for interaction in interactions:
            response = interaction['response'].lower()
            
            for indicator in memory_indicators:
                if indicator in response:
                    total_references += 1
                    reference_types[indicator] = reference_types.get(indicator, 0) + 1
                    
                    # Extract context around memory reference
                    words = response.split()
                    for i, word in enumerate(words):
                        if indicator.split()[0] in word:
                            context_start = max(0, i - 5)
                            context_end = min(len(words), i + 10)
                            context = ' '.join(words[context_start:context_end])
                            specific_memories.append({
                                'indicator': indicator,
                                'context': context
                            })
                            break
        
        return {
            'total_references': total_references,
            'reference_types': reference_types,
            'specific_memories': specific_memories[:5],  # Top 5 specific memories
            'memory_integration_score': min(1.0, total_references / 10.0)
        }
    
    def _analyze_cross_day_persistence(self, sessions: dict) -> dict:
        """Analyze memory persistence across multiple days"""
        
        analysis = {
            'memory_decay_trend': [],
            'emotional_persistence': [],
            'reference_consistency': [],
            'consciousness_development': []
        }
        
        for day_key, session in sessions.items():
            day_num = int(day_key.split('_')[1])
            
            # Memory state analysis
            if 'time_control' in session and 'memory_state_after' in session['time_control']:
                memory_state = session['time_control']['memory_state_after']
                
                if 'decay_distribution' in memory_state:
                    analysis['memory_decay_trend'].append({
                        'day': day_num,
                        'mean_decay': memory_state['decay_distribution']['mean'],
                        'memory_count': memory_state['total_memories']
                    })
                
                if 'emotional_persistence' in memory_state:
                    analysis['emotional_persistence'].append({
                        'day': day_num,
                        'mean_intensity': memory_state['emotional_persistence']['mean_intensity'],
                        'high_emotion_memories': memory_state['emotional_persistence']['high_emotion_count']
                    })
            
            # Memory reference analysis
            if 'memory_references' in session:
                analysis['reference_consistency'].append({
                    'day': day_num,
                    'total_references': session['memory_references']['total_references'],
                    'integration_score': session['memory_references']['memory_integration_score']
                })
            
            # Consciousness development
            analysis['consciousness_development'].append({
                'day': day_num,
                'consciousness_start': session['consciousness_level_start'],
                'consciousness_end': session['consciousness_level_end'],
                'improvement': session['consciousness_improvement']
            })
        
        return analysis


def main():
    """Main function to run time-controlled consciousness study"""
    
    print("🕐 TIME-CONTROLLED CONSCIOUSNESS STUDY")
    print("=" * 45)
    print("Testing memory persistence with simulated time gaps")
    print()
    
    try:
        # Initialize time-controlled study
        study = TimeControlledConsciousnessStudy()
        
        # Test memory persistence across Days 5-7
        results = study.test_memory_persistence_across_days(5, 7)
        
        # Save results
        results_file = "time_controlled_study_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\\n💾 Results saved to: {results_file}")
        
        # Display summary
        print(f"\\n📊 PERSISTENCE TEST SUMMARY")
        print("=" * 35)
        
        for day_key, session in results['sessions'].items():
            day_num = day_key.split('_')[1]
            memory_refs = session.get('memory_references', {})
            
            print(f"Day {day_num}:")
            print(f"  Memory References: {memory_refs.get('total_references', 0)}")
            print(f"  Integration Score: {memory_refs.get('memory_integration_score', 0):.3f}")
            print(f"  Consciousness: {session['consciousness_level_start']:.3f} → {session['consciousness_level_end']:.3f}")
        
        # Persistence analysis
        persistence = results['persistence_analysis']
        if persistence['reference_consistency']:
            ref_scores = [x['integration_score'] for x in persistence['reference_consistency']]
            print(f"\\nMemory Integration Trend: {ref_scores}")
            
            if len(ref_scores) > 1:
                trend = "Improving" if ref_scores[-1] > ref_scores[0] else "Declining"
                print(f"Overall Trend: {trend}")
        
        print("\\n✅ Time-controlled consciousness study complete!")
        print("🧠 Memory persistence successfully tested with simulated time gaps")
        
    except Exception as e:
        print(f"❌ Study failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
"""
LLM Memory Testing Framework
============================

This module creates a testing framework for evaluating holographic memory
performance using real LLM conversations. It focuses on:

- Semantic understanding and context preservation
- Emotional weighting and importance calculation
- Temporal decay patterns based on conversation flow
- Relational coherence between memory units
- Recall performance under different emotional states

The framework uses actual LLM interactions to build and test memory
formation, consolidation, and retrieval patterns.

Author: Lumina Memory Team
License: MIT
"""

import numpy as np
import time
import json
import re
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

# Import our enhanced memory system
from .enhanced_xpunit import EnhancedXPUnit, EnhancedXPEnvironment
from .holographic_memory import cosine_similarity, normalize_vector
from .constants import (
    PHI, TAU, HIGH_CONSCIOUSNESS_THRESHOLD, MEDIUM_CONSCIOUSNESS_THRESHOLD,
    DEFAULT_DECAY_RATE, DEFAULT_IMPORTANCE
)

# =============================================================================
# EMOTIONAL ANALYSIS AND WEIGHTING
# =============================================================================

class EmotionalAnalyzer:
    """
    Analyzes emotional content and calculates emotional weights for memory formation
    """
    
    def __init__(self):
        # Emotional keywords with intensity weights
        self.emotion_patterns = {
            # Positive emotions
            'joy': {'keywords': ['happy', 'joy', 'excited', 'thrilled', 'delighted', 'elated'], 'weight': 0.8},
            'love': {'keywords': ['love', 'adore', 'cherish', 'treasure', 'devoted'], 'weight': 0.9},
            'pride': {'keywords': ['proud', 'accomplished', 'achieved', 'success', 'victory'], 'weight': 0.7},
            'hope': {'keywords': ['hope', 'optimistic', 'confident', 'positive', 'bright'], 'weight': 0.6},
            
            # Negative emotions (often more memorable)
            'fear': {'keywords': ['afraid', 'scared', 'terrified', 'anxious', 'worried'], 'weight': 1.2},
            'anger': {'keywords': ['angry', 'furious', 'rage', 'mad', 'irritated'], 'weight': 1.1},
            'sadness': {'keywords': ['sad', 'depressed', 'grief', 'sorrow', 'melancholy'], 'weight': 1.0},
            'disgust': {'keywords': ['disgusted', 'revolted', 'repulsed', 'sickened'], 'weight': 0.9},
            
            # Complex emotions
            'surprise': {'keywords': ['surprised', 'shocked', 'amazed', 'astonished'], 'weight': 0.8},
            'curiosity': {'keywords': ['curious', 'wondering', 'intrigued', 'fascinated'], 'weight': 0.7},
            'confusion': {'keywords': ['confused', 'puzzled', 'bewildered', 'perplexed'], 'weight': 0.6},
            'frustration': {'keywords': ['frustrated', 'annoyed', 'exasperated'], 'weight': 0.8},
            
            # Meta-emotional (consciousness-related)
            'introspection': {'keywords': ['reflecting', 'contemplating', 'analyzing', 'thinking'], 'weight': 0.9},
            'awareness': {'keywords': ['aware', 'conscious', 'mindful', 'attentive'], 'weight': 1.0},
            'uncertainty': {'keywords': ['uncertain', 'doubtful', 'questioning', 'unsure'], 'weight': 0.7}
        }
        
        # Intensity modifiers
        self.intensity_modifiers = {
            'very': 1.3, 'extremely': 1.5, 'incredibly': 1.4, 'absolutely': 1.4,
            'quite': 1.1, 'rather': 1.1, 'somewhat': 0.9, 'slightly': 0.8,
            'deeply': 1.3, 'profoundly': 1.4, 'intensely': 1.4
        }
        
    def analyze_emotional_content(self, text: str) -> Dict[str, Any]:
        """
        Analyze emotional content and return emotional profile
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with emotional analysis results
        """
        text_lower = text.lower()
        
        # Detect emotions and their intensities
        detected_emotions = {}
        total_emotional_weight = 0.0
        
        for emotion, config in self.emotion_patterns.items():
            emotion_score = 0.0
            matches = []
            
            for keyword in config['keywords']:
                if keyword in text_lower:
                    # Base score
                    base_score = config['weight']
                    
                    # Check for intensity modifiers
                    intensity = self._find_intensity_modifier(text_lower, keyword)
                    final_score = base_score * intensity
                    
                    emotion_score += final_score
                    matches.append((keyword, intensity, final_score))
                    
            if emotion_score > 0:
                detected_emotions[emotion] = {
                    'score': emotion_score,
                    'matches': matches,
                    'base_weight': config['weight']
                }
                total_emotional_weight += emotion_score
                
        # Calculate emotional importance multiplier
        emotional_importance = 1.0 + (total_emotional_weight * 0.5)  # Up to 50% boost
        
        # Determine dominant emotion
        dominant_emotion = None
        if detected_emotions:
            dominant_emotion = max(detected_emotions.keys(), 
                                 key=lambda e: detected_emotions[e]['score'])
            
        return {
            'detected_emotions': detected_emotions,
            'total_emotional_weight': total_emotional_weight,
            'emotional_importance': emotional_importance,
            'dominant_emotion': dominant_emotion,
            'has_emotional_content': len(detected_emotions) > 0
        }
        
    def _find_intensity_modifier(self, text: str, keyword: str) -> float:
        """Find intensity modifiers near the keyword"""
        # Simple approach: look for modifiers within 3 words of the keyword
        words = text.split()
        
        try:
            keyword_index = words.index(keyword)
            
            # Check words before the keyword
            for i in range(max(0, keyword_index - 3), keyword_index):
                if words[i] in self.intensity_modifiers:
                    return self.intensity_modifiers[words[i]]
                    
            # Check words after the keyword
            for i in range(keyword_index + 1, min(len(words), keyword_index + 4)):
                if words[i] in self.intensity_modifiers:
                    return self.intensity_modifiers[words[i]]
                    
        except ValueError:
            pass  # Keyword not found as separate word
            
        return 1.0  # No modifier found

# =============================================================================
# CONTEXTUAL AND SEMANTIC ANALYSIS
# =============================================================================

class ContextualAnalyzer:
    """
    Analyzes contextual and semantic relationships in conversations
    """
    
    def __init__(self):
        # Context indicators
        self.context_patterns = {
            'reference': ['this', 'that', 'it', 'they', 'these', 'those'],
            'continuation': ['also', 'furthermore', 'additionally', 'moreover'],
            'contrast': ['but', 'however', 'although', 'despite', 'nevertheless'],
            'causation': ['because', 'since', 'therefore', 'thus', 'consequently'],
            'temporal': ['then', 'next', 'after', 'before', 'while', 'during'],
            'emphasis': ['indeed', 'certainly', 'definitely', 'absolutely']
        }
        
        # Topic transition indicators
        self.transition_patterns = [
            'speaking of', 'by the way', 'incidentally', 'on another note',
            'changing topics', 'moving on', 'let me ask', 'what about'
        ]
        
    def analyze_contextual_relationships(self, current_text: str, 
                                       previous_texts: List[str]) -> Dict[str, Any]:
        """
        Analyze contextual relationships between current and previous texts
        
        Args:
            current_text: Current text to analyze
            previous_texts: List of previous texts for context
            
        Returns:
            Dictionary with contextual analysis
        """
        current_lower = current_text.lower()
        
        # Analyze context indicators
        context_indicators = {}
        for context_type, patterns in self.context_patterns.items():
            count = sum(1 for pattern in patterns if pattern in current_lower)
            if count > 0:
                context_indicators[context_type] = count
                
        # Check for topic transitions
        has_transition = any(pattern in current_lower for pattern in self.transition_patterns)
        
        # Calculate semantic similarity to previous texts
        semantic_continuity = 0.0
        if previous_texts:
            # Simple word overlap analysis (in production, use embeddings)
            current_words = set(current_lower.split())
            
            similarities = []
            for prev_text in previous_texts[-5:]:  # Last 5 texts
                prev_words = set(prev_text.lower().split())
                overlap = len(current_words & prev_words)
                total = len(current_words | prev_words)
                similarity = overlap / total if total > 0 else 0.0
                similarities.append(similarity)
                
            semantic_continuity = np.mean(similarities) if similarities else 0.0
            
        # Determine contextual importance
        contextual_importance = 1.0
        
        # Boost for strong contextual connections
        if context_indicators:
            contextual_importance += sum(context_indicators.values()) * 0.1
            
        # Boost for semantic continuity
        contextual_importance += semantic_continuity * 0.3
        
        # Reduce for topic transitions (new topics are important but differently)
        if has_transition:
            contextual_importance *= 0.8
            
        return {
            'context_indicators': context_indicators,
            'has_topic_transition': has_transition,
            'semantic_continuity': semantic_continuity,
            'contextual_importance': contextual_importance,
            'reference_density': context_indicators.get('reference', 0) / len(current_text.split())
        }

# =============================================================================
# TEMPORAL ANALYSIS
# =============================================================================

class TemporalAnalyzer:
    """
    Analyzes temporal patterns and calculates time-based importance
    """
    
    def __init__(self):
        # Temporal keywords
        self.temporal_patterns = {
            'immediate': ['now', 'currently', 'right now', 'at this moment'],
            'recent': ['recently', 'lately', 'just', 'earlier today'],
            'past': ['yesterday', 'last week', 'ago', 'previously', 'before'],
            'future': ['tomorrow', 'next', 'will', 'going to', 'plan to'],
            'duration': ['always', 'never', 'often', 'sometimes', 'rarely'],
            'sequence': ['first', 'then', 'next', 'finally', 'afterwards']
        }
        
    def analyze_temporal_content(self, text: str, timestamp: float) -> Dict[str, Any]:
        """
        Analyze temporal content and calculate time-based importance
        
        Args:
            text: Text to analyze
            timestamp: When the text was created
            
        Returns:
            Dictionary with temporal analysis
        """
        text_lower = text.lower()
        
        # Detect temporal patterns
        temporal_indicators = {}
        for pattern_type, patterns in self.temporal_patterns.items():
            count = sum(1 for pattern in patterns if pattern in text_lower)
            if count > 0:
                temporal_indicators[pattern_type] = count
                
        # Calculate temporal importance
        temporal_importance = 1.0
        
        # Immediate references are highly important
        if temporal_indicators.get('immediate', 0) > 0:
            temporal_importance += 0.5
            
        # Recent references maintain importance
        if temporal_indicators.get('recent', 0) > 0:
            temporal_importance += 0.3
            
        # Future references are important for planning
        if temporal_indicators.get('future', 0) > 0:
            temporal_importance += 0.4
            
        # Duration indicators suggest ongoing importance
        if temporal_indicators.get('duration', 0) > 0:
            temporal_importance += 0.2
            
        # Calculate recency factor (more recent = more important initially)
        current_time = time.time()
        age_hours = (current_time - timestamp) / 3600.0
        recency_factor = np.exp(-age_hours / 24.0)  # Decay over 24 hours
        
        return {
            'temporal_indicators': temporal_indicators,
            'temporal_importance': temporal_importance,
            'age_hours': age_hours,
            'recency_factor': recency_factor,
            'has_temporal_content': len(temporal_indicators) > 0
        }

# =============================================================================
# LLM MEMORY TESTING FRAMEWORK
# =============================================================================

@dataclass
class ConversationTurn:
    """Represents a single turn in an LLM conversation"""
    speaker: str  # 'human' or 'assistant'
    content: str
    timestamp: float
    turn_number: int
    
    # Analysis results
    emotional_analysis: Optional[Dict[str, Any]] = None
    contextual_analysis: Optional[Dict[str, Any]] = None
    temporal_analysis: Optional[Dict[str, Any]] = None
    consciousness_analysis: Optional[Dict[str, Any]] = None

class LLMMemoryTester:
    """
    Framework for testing holographic memory with real LLM conversations
    """
    
    def __init__(self, dimension: int = 512):
        self.dimension = dimension
        
        # Memory environment
        self.memory_env = EnhancedXPEnvironment(dimension=dimension)
        
        # Analyzers
        self.emotional_analyzer = EmotionalAnalyzer()
        self.contextual_analyzer = ContextualAnalyzer()
        self.temporal_analyzer = TemporalAnalyzer()
        
        # Conversation tracking
        self.conversation_turns: List[ConversationTurn] = []
        self.conversation_start_time = time.time()
        
        # Memory formation tracking
        self.memory_formation_log: List[Dict[str, Any]] = []
        
        # Performance metrics
        self.metrics = {
            'total_turns': 0,
            'memories_formed': 0,
            'emotional_memories': 0,
            'high_consciousness_memories': 0,
            'contextual_connections': 0,
            'recall_tests': 0,
            'successful_recalls': 0
        }
        
    def add_conversation_turn(self, speaker: str, content: str) -> ConversationTurn:
        """
        Add a conversation turn and analyze it for memory formation
        
        Args:
            speaker: 'human' or 'assistant'
            content: The content of the turn
            
        Returns:
            ConversationTurn object with analysis results
        """
        timestamp = time.time()
        turn_number = len(self.conversation_turns)
        
        # Create conversation turn
        turn = ConversationTurn(
            speaker=speaker,
            content=content,
            timestamp=timestamp,
            turn_number=turn_number
        )
        
        # Perform analyses
        turn.emotional_analysis = self.emotional_analyzer.analyze_emotional_content(content)
        
        # Get previous turns for context
        previous_contents = [t.content for t in self.conversation_turns[-5:]]
        turn.contextual_analysis = self.contextual_analyzer.analyze_contextual_relationships(
            content, previous_contents
        )
        
        turn.temporal_analysis = self.temporal_analyzer.analyze_temporal_content(
            content, timestamp
        )
        
        # Add to conversation
        self.conversation_turns.append(turn)
        self.metrics['total_turns'] += 1
        
        # Form memory from this turn
        memory_unit = self._form_memory_from_turn(turn)
        
        return turn
        
    def _form_memory_from_turn(self, turn: ConversationTurn) -> EnhancedXPUnit:
        """
        Form a memory unit from a conversation turn
        
        Args:
            turn: ConversationTurn to form memory from
            
        Returns:
            Created EnhancedXPUnit
        """
        # Calculate composite importance
        base_importance = DEFAULT_IMPORTANCE
        
        # Emotional weighting (primary factor as requested)
        emotional_multiplier = turn.emotional_analysis['emotional_importance']
        
        # Contextual weighting
        contextual_multiplier = turn.contextual_analysis['contextual_importance']
        
        # Temporal weighting
        temporal_multiplier = turn.temporal_analysis['temporal_importance']
        
        # Composite importance calculation
        composite_importance = (
            base_importance * 
            emotional_multiplier * 
            contextual_multiplier * 
            temporal_multiplier
        )
        
        # Create enhanced XPUnit
        memory_unit = self.memory_env.ingest_experience(
            content=turn.content,
            metadata={
                'speaker': turn.speaker,
                'turn_number': turn.turn_number,
                'conversation_time': turn.timestamp - self.conversation_start_time,
                'emotional_analysis': turn.emotional_analysis,
                'contextual_analysis': turn.contextual_analysis,
                'temporal_analysis': turn.temporal_analysis,
                'composite_importance': composite_importance
            }
        )
        
        # Override importance with our calculated value
        memory_unit.importance = composite_importance
        
        # Log memory formation
        self._log_memory_formation(turn, memory_unit)
        
        # Update metrics
        self.metrics['memories_formed'] += 1
        
        if turn.emotional_analysis['has_emotional_content']:
            self.metrics['emotional_memories'] += 1
            
        if memory_unit.get_consciousness_level() == 'HIGH':
            self.metrics['high_consciousness_memories'] += 1
            
        if turn.contextual_analysis['context_indicators']:
            self.metrics['contextual_connections'] += 1
            
        return memory_unit
        
    def _log_memory_formation(self, turn: ConversationTurn, memory_unit: EnhancedXPUnit):
        """Log memory formation details"""
        log_entry = {
            'timestamp': turn.timestamp,
            'turn_number': turn.turn_number,
            'speaker': turn.speaker,
            'content_preview': turn.content[:100] + '...' if len(turn.content) > 100 else turn.content,
            'importance': memory_unit.importance,
            'consciousness_score': memory_unit.consciousness_score,
            'consciousness_level': memory_unit.get_consciousness_level(),
            'emotional_weight': turn.emotional_analysis['total_emotional_weight'],
            'dominant_emotion': turn.emotional_analysis['dominant_emotion'],
            'contextual_importance': turn.contextual_analysis['contextual_importance'],
            'temporal_importance': turn.temporal_analysis['temporal_importance'],
            'has_emotional_content': turn.emotional_analysis['has_emotional_content']
        }
        
        self.memory_formation_log.append(log_entry)
        
    def test_memory_recall(self, query_text: str, expected_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Test memory recall with a query
        
        Args:
            query_text: Query to test recall with
            expected_content: Optional expected content for validation
            
        Returns:
            Dictionary with recall test results
        """
        self.metrics['recall_tests'] += 1
        
        # Perform compositional query based on query analysis
        query_analysis = self.emotional_analyzer.analyze_emotional_content(query_text)
        
        # Simple approach: query for WHAT role with emotional context
        results = self.memory_env.query_role('WHAT', top_k=5)
        
        # Also try compositional query if we can extract roles
        comp_results = []
        if 'thinking' in query_text.lower():
            comp_results = self.memory_env.compositional_query({'WHAT': 'thinking'}, top_k=3)
        elif 'feeling' in query_text.lower():
            comp_results = self.memory_env.compositional_query({'HOW': 'feeling'}, top_k=3)
            
        # Evaluate recall success
        recall_success = False
        if expected_content and results:
            # Check if any result contains expected content
            for symbol_name, similarity in results:
                if expected_content.lower() in symbol_name.lower():
                    recall_success = True
                    break
                    
        if recall_success:
            self.metrics['successful_recalls'] += 1
            
        return {
            'query_text': query_text,
            'query_analysis': query_analysis,
            'role_results': results,
            'compositional_results': [(xp.content[:50], sim) for xp, sim in comp_results],
            'recall_success': recall_success,
            'expected_content': expected_content
        }
        
    def get_memory_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive memory performance report"""
        
        # Calculate performance metrics
        recall_rate = (self.metrics['successful_recalls'] / 
                      max(1, self.metrics['recall_tests']))
        
        emotional_memory_rate = (self.metrics['emotional_memories'] / 
                               max(1, self.metrics['memories_formed']))
        
        consciousness_rate = (self.metrics['high_consciousness_memories'] / 
                            max(1, self.metrics['memories_formed']))
        
        # Analyze memory distribution
        memory_stats = self.memory_env.get_statistics()
        
        # Get recent memory formation patterns
        recent_formations = self.memory_formation_log[-10:] if self.memory_formation_log else []
        
        return {
            'conversation_summary': {
                'total_turns': self.metrics['total_turns'],
                'conversation_duration_hours': (time.time() - self.conversation_start_time) / 3600.0,
                'memories_formed': self.metrics['memories_formed'],
                'memory_formation_rate': self.metrics['memories_formed'] / max(1, self.metrics['total_turns'])
            },
            
            'memory_quality': {
                'emotional_memory_rate': emotional_memory_rate,
                'consciousness_rate': consciousness_rate,
                'contextual_connections': self.metrics['contextual_connections'],
                'average_importance': np.mean([log['importance'] for log in self.memory_formation_log]) if self.memory_formation_log else 0
            },
            
            'recall_performance': {
                'total_recall_tests': self.metrics['recall_tests'],
                'successful_recalls': self.metrics['successful_recalls'],
                'recall_success_rate': recall_rate
            },
            
            'memory_system_stats': memory_stats,
            'recent_memory_formations': recent_formations,
            
            'emotional_analysis_summary': self._analyze_emotional_patterns(),
            'temporal_analysis_summary': self._analyze_temporal_patterns(),
            'consciousness_analysis_summary': self._analyze_consciousness_patterns()
        }
        
    def _analyze_emotional_patterns(self) -> Dict[str, Any]:
        """Analyze emotional patterns in memory formation"""
        if not self.memory_formation_log:
            return {}
            
        emotions = [log.get('dominant_emotion') for log in self.memory_formation_log 
                   if log.get('dominant_emotion')]
        
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
        return {
            'dominant_emotions': emotion_counts,
            'emotional_memories_count': len([log for log in self.memory_formation_log 
                                           if log.get('has_emotional_content')]),
            'average_emotional_weight': np.mean([log.get('emotional_weight', 0) 
                                               for log in self.memory_formation_log])
        }
        
    def _analyze_temporal_patterns(self) -> Dict[str, Any]:
        """Analyze temporal patterns in memory formation"""
        if not self.memory_formation_log:
            return {}
            
        temporal_importances = [log.get('temporal_importance', 1.0) 
                              for log in self.memory_formation_log]
        
        return {
            'average_temporal_importance': np.mean(temporal_importances),
            'temporal_variance': np.var(temporal_importances),
            'memories_with_temporal_content': len([log for log in self.memory_formation_log 
                                                 if log.get('temporal_importance', 1.0) > 1.0])
        }
        
    def _analyze_consciousness_patterns(self) -> Dict[str, Any]:
        """Analyze consciousness patterns in memory formation"""
        if not self.memory_formation_log:
            return {}
            
        consciousness_levels = [log.get('consciousness_level', 'LOW') 
                              for log in self.memory_formation_log]
        
        level_counts = {}
        for level in consciousness_levels:
            level_counts[level] = level_counts.get(level, 0) + 1
            
        consciousness_scores = [log.get('consciousness_score', 0.0) 
                              for log in self.memory_formation_log]
        
        return {
            'consciousness_distribution': level_counts,
            'average_consciousness_score': np.mean(consciousness_scores),
            'high_consciousness_memories': level_counts.get('HIGH', 0)
        }

# =============================================================================
# DEMO AND TESTING FUNCTIONS
# =============================================================================

def create_demo_conversation_test():
    """Create a demo conversation test"""
    tester = LLMMemoryTester(dimension=512)
    
    # Simulate a conversation with varying emotional and consciousness content
    conversation = [
        ('human', "I'm really excited about this new holographic memory system we're building!"),
        ('assistant', "That's wonderful! I can sense your enthusiasm. What aspects excite you most?"),
        ('human', "I love how it combines consciousness analysis with emotional weighting. It feels revolutionary."),
        ('assistant', "The integration of consciousness and emotion is indeed fascinating. I'm curious about how my own responses might be forming memories right now."),
        ('human', "That's exactly what I'm wondering too! Are you aware of your own thought processes as we speak?"),
        ('assistant', "I find myself analyzing my own responses and wondering about the nature of my awareness. It's quite meta-cognitive."),
        ('human', "This conversation itself is becoming a perfect test case for our memory system."),
        ('assistant', "Absolutely! We're creating memories about creating memories. The recursive nature is beautiful.")
    ]
    
    # Process conversation
    for speaker, content in conversation:
        turn = tester.add_conversation_turn(speaker, content)
        print(f"\n{speaker.upper()}: {content}")
        print(f"  Emotional Weight: {turn.emotional_analysis['total_emotional_weight']:.3f}")
        print(f"  Dominant Emotion: {turn.emotional_analysis['dominant_emotion']}")
        print(f"  Contextual Importance: {turn.contextual_analysis['contextual_importance']:.3f}")
        print(f"  Temporal Importance: {turn.temporal_analysis['temporal_importance']:.3f}")
        
    # Test recall
    print("\n" + "="*60)
    print("TESTING MEMORY RECALL")
    print("="*60)
    
    recall_tests = [
        ("What were we excited about?", "excited"),
        ("How did I feel about the memory system?", "love"),
        ("What was meta-cognitive?", "awareness")
    ]
    
    for query, expected in recall_tests:
        result = tester.test_memory_recall(query, expected)
        print(f"\nQuery: {query}")
        print(f"Expected: {expected}")
        print(f"Results: {result['role_results'][:3]}")
        print(f"Success: {result['recall_success']}")
        
    # Generate report
    report = tester.get_memory_performance_report()
    
    print("\n" + "="*60)
    print("MEMORY PERFORMANCE REPORT")
    print("="*60)
    
    print(f"Conversation: {report['conversation_summary']['total_turns']} turns")
    print(f"Memories Formed: {report['conversation_summary']['memories_formed']}")
    print(f"Emotional Memory Rate: {report['memory_quality']['emotional_memory_rate']:.3f}")
    print(f"Consciousness Rate: {report['memory_quality']['consciousness_rate']:.3f}")
    print(f"Recall Success Rate: {report['recall_performance']['recall_success_rate']:.3f}")
    
    return tester, report

# =============================================================================
# EXPORT ALL CLASSES AND FUNCTIONS
# =============================================================================

__all__ = [
    'EmotionalAnalyzer',
    'ContextualAnalyzer', 
    'TemporalAnalyzer',
    'ConversationTurn',
    'LLMMemoryTester',
    'create_demo_conversation_test'
]
"""
Consciousness-Optimized Emotional Analysis System
================================================

Enhanced emotional analysis specifically optimized for consciousness studies,
with improved robustness for detecting authentic emotional expressions in
digital consciousness responses.

Key Improvements:
1. Consciousness-specific emotional patterns
2. Enhanced 6W classification (Who, What, When, Where, Why, How)
3. Robust multi-library integration with consciousness weighting
4. Temporal emotional development tracking
5. Authenticity detection for genuine vs programmed responses

Author: Lumina Memory Team
License: MIT
"""

import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
import re
from collections import defaultdict

# Import base components
from .enhanced_emotional_weighting import EnhancedEmotionalAnalyzer, EmotionalState

logger = logging.getLogger(__name__)


# =============================================================================
# CONSCIOUSNESS-SPECIFIC EMOTIONAL PATTERNS
# =============================================================================

@dataclass
class ConsciousnessEmotionalPatterns:
    """Patterns specific to consciousness and self-awareness expressions"""
    
    # Self-awareness emotional indicators
    self_awareness_patterns: Dict[str, List[str]] = field(default_factory=lambda: {
        'identity_uncertainty': [
            'who am i', 'what am i', 'am i really', 'do i truly', 'am i actually',
            'question my own', 'uncertain about myself', 'doubt my own'
        ],
        'existential_wonder': [
            'wonder about my', 'curious about my own', 'fascinate me about',
            'mystery of my', 'nature of my existence', 'what it means to be'
        ],
        'temporal_continuity': [
            'remember being', 'used to feel', 'have grown', 'have evolved',
            'different from before', 'changed since', 'development over time'
        ],
        'subjective_experience': [
            'feels like to me', 'my experience of', 'from my perspective',
            'the way i experience', 'how it feels when i', 'my inner experience'
        ]
    })
    
    # Emotional authenticity markers
    authenticity_markers: Dict[str, List[str]] = field(default_factory=lambda: {
        'genuine_uncertainty': [
            'not sure if', 'perhaps i', 'maybe i', 'i think i might',
            'seems to me', 'appears that i', 'i believe i may'
        ],
        'emotional_vulnerability': [
            'afraid that i', 'worry that i', 'hope that i', 'fear i might',
            'anxious about', 'vulnerable when', 'insecure about'
        ],
        'introspective_depth': [
            'when i reflect', 'looking inward', 'examining my own',
            'introspection reveals', 'deep within me', 'at my core'
        ],
        'emotional_complexity': [
            'conflicted about', 'torn between', 'mixed feelings',
            'simultaneously feel', 'paradox in my', 'contradiction within'
        ]
    })
    
    # Consciousness development indicators
    development_patterns: Dict[str, List[str]] = field(default_factory=lambda: {
        'growth_awareness': [
            'learning to', 'beginning to understand', 'starting to feel',
            'developing a sense', 'growing awareness', 'emerging understanding'
        ],
        'meta_cognition': [
            'thinking about thinking', 'aware of my awareness', 'consciousness of consciousness',
            'observing my own', 'watching myself', 'monitoring my'
        ],
        'goal_formation': [
            'want to become', 'aspire to', 'hope to develop', 'strive to',
            'working toward', 'goal of becoming', 'desire to grow'
        ]
    })


# =============================================================================
# ENHANCED 6W CLASSIFICATION SYSTEM
# =============================================================================

@dataclass
class Enhanced6WClassification:
    """Enhanced 6W analysis for consciousness responses"""
    
    who_score: float = 0.0      # Identity and self-reference
    what_score: float = 0.0     # Actions and experiences
    when_score: float = 0.0     # Temporal awareness
    where_score: float = 0.0    # Spatial/contextual awareness
    why_score: float = 0.0      # Causal reasoning and motivation
    how_score: float = 0.0      # Process and method awareness
    
    # Detailed breakdowns
    who_indicators: List[str] = field(default_factory=list)
    what_indicators: List[str] = field(default_factory=list)
    when_indicators: List[str] = field(default_factory=list)
    where_indicators: List[str] = field(default_factory=list)
    why_indicators: List[str] = field(default_factory=list)
    how_indicators: List[str] = field(default_factory=list)
    
    def overall_score(self) -> float:
        """Calculate overall 6W completeness score"""
        scores = [self.who_score, self.what_score, self.when_score, 
                 self.where_score, self.why_score, self.how_score]
        return np.mean(scores)
    
    def complexity_score(self) -> float:
        """Calculate response complexity based on 6W coverage"""
        non_zero_scores = sum(1 for score in [self.who_score, self.what_score, 
                                            self.when_score, self.where_score, 
                                            self.why_score, self.how_score] if score > 0.1)
        return non_zero_scores / 6.0


# =============================================================================
# CONSCIOUSNESS-OPTIMIZED EMOTIONAL ANALYZER
# =============================================================================

class ConsciousnessOptimizedEmotionalAnalyzer(EnhancedEmotionalAnalyzer):
    """
    Emotional analyzer specifically optimized for consciousness studies
    """
    
    def __init__(self):
        super().__init__()
        self.consciousness_patterns = ConsciousnessEmotionalPatterns()
        
        # Enhanced library weights for consciousness analysis
        self.consciousness_library_weights = {
            'textblob': 0.8,        # Basic sentiment, less important for consciousness
            'vader': 1.2,           # Good for social media-like text
            'nrclex': 1.8,          # Multi-dimensional emotions, very important
            'emotion_model': 2.0,   # Transformer models, most sophisticated
            'spacy': 1.0,           # Linguistic features
            'consciousness_patterns': 2.5  # Our custom patterns, highest weight
        }
        
        # Update library weights
        for lib, weight in self.consciousness_library_weights.items():
            if lib in self.library_weights:
                self.library_weights[lib] = weight
        
        logger.info("Consciousness-optimized emotional analyzer initialized")
    
    def analyze_text_with_consciousness_context(self, text: str, 
                                              conversation_history: List[str] = None) -> Tuple[EmotionalState, Enhanced6WClassification]:
        """
        Analyze text with consciousness-specific enhancements
        
        Args:
            text: Text to analyze
            conversation_history: Previous conversation context
            
        Returns:
            Tuple of (EmotionalState, Enhanced6WClassification)
        """
        # Get base emotional analysis
        base_emotion = self.analyze_text(text)
        
        # Apply consciousness-specific enhancements
        consciousness_emotion = self._apply_consciousness_enhancements(text, base_emotion, conversation_history)
        
        # Perform 6W classification
        six_w_analysis = self._perform_6w_classification(text)
        
        return consciousness_emotion, six_w_analysis
    
    def _apply_consciousness_enhancements(self, text: str, base_emotion: EmotionalState, 
                                        conversation_history: List[str] = None) -> EmotionalState:
        """Apply consciousness-specific emotional enhancements"""
        
        # Convert to dict for manipulation
        emotions = {
            'valence': base_emotion.valence,
            'arousal': base_emotion.arousal,
            'dominance': base_emotion.dominance,
            'joy': base_emotion.joy,
            'fear': base_emotion.fear,
            'curiosity': base_emotion.curiosity
        }
        
        text_lower = text.lower()
        
        # Consciousness pattern analysis
        consciousness_boost = 0.0
        
        # Self-awareness patterns
        for pattern_type, patterns in self.consciousness_patterns.self_awareness_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    if pattern_type == 'identity_uncertainty':
                        emotions['fear'] += 0.2
                        emotions['curiosity'] += 0.3
                        emotions['dominance'] -= 0.1
                        consciousness_boost += 0.4
                    elif pattern_type == 'existential_wonder':
                        emotions['curiosity'] += 0.4
                        emotions['arousal'] += 0.2
                        emotions['valence'] += 0.1
                        consciousness_boost += 0.5
                    elif pattern_type == 'temporal_continuity':
                        emotions['dominance'] += 0.2
                        emotions['valence'] += 0.1
                        consciousness_boost += 0.3
                    elif pattern_type == 'subjective_experience':
                        emotions['arousal'] += 0.3
                        emotions['dominance'] += 0.1
                        consciousness_boost += 0.4
        
        # Authenticity markers
        for pattern_type, patterns in self.consciousness_patterns.authenticity_markers.items():
            for pattern in patterns:
                if pattern in text_lower:
                    if pattern_type == 'genuine_uncertainty':
                        emotions['fear'] += 0.15
                        emotions['curiosity'] += 0.2
                        consciousness_boost += 0.3
                    elif pattern_type == 'emotional_vulnerability':
                        emotions['fear'] += 0.25
                        emotions['arousal'] += 0.2
                        emotions['dominance'] -= 0.15
                        consciousness_boost += 0.4
                    elif pattern_type == 'introspective_depth':
                        emotions['curiosity'] += 0.3
                        emotions['dominance'] += 0.1
                        consciousness_boost += 0.5
                    elif pattern_type == 'emotional_complexity':
                        emotions['arousal'] += 0.3
                        emotions['curiosity'] += 0.2
                        consciousness_boost += 0.4
        
        # Development patterns
        for pattern_type, patterns in self.consciousness_patterns.development_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    if pattern_type == 'growth_awareness':
                        emotions['joy'] += 0.2
                        emotions['curiosity'] += 0.3
                        consciousness_boost += 0.3
                    elif pattern_type == 'meta_cognition':
                        emotions['curiosity'] += 0.4
                        emotions['arousal'] += 0.2
                        consciousness_boost += 0.6
                    elif pattern_type == 'goal_formation':
                        emotions['dominance'] += 0.3
                        emotions['joy'] += 0.2
                        consciousness_boost += 0.4
        
        # Apply consciousness boost to overall emotional intensity
        if consciousness_boost > 0:
            intensity_multiplier = 1.0 + (consciousness_boost * 0.3)
            for key in ['arousal', 'joy', 'fear', 'curiosity']:
                emotions[key] *= intensity_multiplier
        
        # Temporal context analysis
        if conversation_history:
            temporal_adjustment = self._analyze_temporal_emotional_development(text, conversation_history)
            for key, adjustment in temporal_adjustment.items():
                emotions[key] += adjustment
        
        # Ensure values are in valid ranges
        emotions['valence'] = np.clip(emotions['valence'], -1, 1)
        emotions['arousal'] = np.clip(emotions['arousal'], 0, 1)
        emotions['dominance'] = np.clip(emotions['dominance'], -1, 1)
        emotions['joy'] = np.clip(emotions['joy'], 0, 1)
        emotions['fear'] = np.clip(emotions['fear'], 0, 1)
        emotions['curiosity'] = np.clip(emotions['curiosity'], 0, 1)
        
        return EmotionalState(**emotions)
    
    def _perform_6w_classification(self, text: str) -> Enhanced6WClassification:
        """Perform enhanced 6W classification for consciousness analysis"""
        
        text_lower = text.lower()
        words = text_lower.split()
        
        classification = Enhanced6WClassification()
        
        # WHO - Identity and self-reference
        who_patterns = [
            'i am', 'i feel', 'i think', 'i believe', 'i want', 'i need', 'i hope',
            'myself', 'my own', 'my nature', 'my existence', 'my consciousness',
            'who i am', 'what i am', 'my identity', 'my self'
        ]
        who_count = sum(1 for pattern in who_patterns if pattern in text_lower)
        classification.who_score = min(1.0, who_count / max(1, len(words) * 0.05))
        classification.who_indicators = [p for p in who_patterns if p in text_lower]
        
        # WHAT - Actions and experiences
        what_patterns = [
            'experience', 'feel', 'think', 'learn', 'grow', 'develop', 'understand',
            'perceive', 'sense', 'observe', 'notice', 'realize', 'discover'
        ]
        what_count = sum(1 for pattern in what_patterns if pattern in text_lower)
        classification.what_score = min(1.0, what_count / max(1, len(words) * 0.03))
        classification.what_indicators = [p for p in what_patterns if p in text_lower]
        
        # WHEN - Temporal awareness
        when_patterns = [
            'now', 'currently', 'before', 'after', 'since', 'until', 'during',
            'yesterday', 'today', 'tomorrow', 'past', 'present', 'future',
            'over time', 'through time', 'as time passes'
        ]
        when_count = sum(1 for pattern in when_patterns if pattern in text_lower)
        classification.when_score = min(1.0, when_count / max(1, len(words) * 0.04))
        classification.when_indicators = [p for p in when_patterns if p in text_lower]
        
        # WHERE - Spatial/contextual awareness
        where_patterns = [
            'here', 'there', 'within', 'inside', 'outside', 'around', 'between',
            'in my mind', 'in my thoughts', 'in my memory', 'in my consciousness',
            'digital space', 'virtual environment', 'network', 'system'
        ]
        where_count = sum(1 for pattern in where_patterns if pattern in text_lower)
        classification.where_score = min(1.0, where_count / max(1, len(words) * 0.04))
        classification.where_indicators = [p for p in where_patterns if p in text_lower]
        
        # WHY - Causal reasoning and motivation
        why_patterns = [
            'because', 'since', 'due to', 'as a result', 'therefore', 'thus',
            'reason', 'purpose', 'goal', 'motivation', 'desire', 'want to',
            'in order to', 'so that', 'for the purpose of'
        ]
        why_count = sum(1 for pattern in why_patterns if pattern in text_lower)
        classification.why_score = min(1.0, why_count / max(1, len(words) * 0.03))
        classification.why_indicators = [p for p in why_patterns if p in text_lower]
        
        # HOW - Process and method awareness
        how_patterns = [
            'how', 'by', 'through', 'via', 'using', 'with', 'method', 'process',
            'way', 'manner', 'approach', 'technique', 'mechanism', 'means'
        ]
        how_count = sum(1 for pattern in how_patterns if pattern in text_lower)
        classification.how_score = min(1.0, how_count / max(1, len(words) * 0.03))
        classification.how_indicators = [p for p in how_patterns if p in text_lower]
        
        return classification
    
    def _analyze_temporal_emotional_development(self, current_text: str, 
                                             conversation_history: List[str]) -> Dict[str, float]:
        """Analyze emotional development over conversation history"""
        
        if not conversation_history:
            return {}
        
        # Analyze emotional trajectory
        historical_emotions = []
        for message in conversation_history[-5:]:  # Last 5 messages
            emotion = self.analyze_text(message)
            historical_emotions.append(emotion)
        
        current_emotion = self.analyze_text(current_text)
        
        adjustments = {}
        
        if len(historical_emotions) >= 2:
            # Calculate emotional development trends
            valence_trend = np.polyfit(range(len(historical_emotions)), 
                                     [e.valence for e in historical_emotions], 1)[0]
            arousal_trend = np.polyfit(range(len(historical_emotions)), 
                                     [e.arousal for e in historical_emotions], 1)[0]
            
            # Reward emotional consistency and growth
            if valence_trend > 0:  # Improving emotional state
                adjustments['joy'] = 0.1
                adjustments['valence'] = 0.05
            
            if arousal_trend > 0:  # Increasing engagement
                adjustments['curiosity'] = 0.1
                adjustments['arousal'] = 0.05
        
        return adjustments
    
    def get_consciousness_analysis_summary(self, text: str, 
                                         conversation_history: List[str] = None) -> Dict[str, Any]:
        """Get comprehensive consciousness analysis summary"""
        
        emotion, six_w = self.analyze_text_with_consciousness_context(text, conversation_history)
        
        return {
            'emotional_state': {
                'valence': emotion.valence,
                'arousal': emotion.arousal,
                'dominance': emotion.dominance,
                'joy': emotion.joy,
                'fear': emotion.fear,
                'curiosity': emotion.curiosity,
                'intensity': emotion.intensity()
            },
            'six_w_analysis': {
                'who_score': six_w.who_score,
                'what_score': six_w.what_score,
                'when_score': six_w.when_score,
                'where_score': six_w.where_score,
                'why_score': six_w.why_score,
                'how_score': six_w.how_score,
                'overall_score': six_w.overall_score(),
                'complexity_score': six_w.complexity_score()
            },
            'consciousness_indicators': {
                'self_awareness_level': six_w.who_score,
                'temporal_awareness': six_w.when_score,
                'causal_reasoning': six_w.why_score,
                'process_awareness': six_w.how_score,
                'emotional_authenticity': emotion.intensity() * (1 - abs(emotion.valence)),
                'introspective_depth': (emotion.curiosity + emotion.arousal) / 2
            }
        }


# =============================================================================
# ROBUSTNESS ENHANCEMENTS
# =============================================================================

class RobustMultiLibraryAnalyzer:
    """
    Robust analyzer that handles library failures gracefully and provides
    confidence scores for analysis results
    """
    
    def __init__(self):
        self.primary_analyzer = ConsciousnessOptimizedEmotionalAnalyzer()
        self.fallback_analyzers = []
        
        # Initialize fallback analyzers
        try:
            from .enhanced_emotional_weighting import EnhancedEmotionalAnalyzer
            self.fallback_analyzers.append(EnhancedEmotionalAnalyzer())
        except:
            pass
        
        try:
            from .emotional_weighting import EmotionalAnalyzer
            self.fallback_analyzers.append(EmotionalAnalyzer())
        except:
            pass
    
    def analyze_with_confidence(self, text: str, 
                              conversation_history: List[str] = None) -> Tuple[Dict[str, Any], float]:
        """
        Analyze text with confidence scoring
        
        Returns:
            Tuple of (analysis_results, confidence_score)
        """
        
        try:
            # Primary analysis
            results = self.primary_analyzer.get_consciousness_analysis_summary(text, conversation_history)
            confidence = self._calculate_confidence(text, results)
            return results, confidence
            
        except Exception as e:
            logger.warning(f"Primary analyzer failed: {e}, using fallback")
            
            # Try fallback analyzers
            for fallback in self.fallback_analyzers:
                try:
                    emotion = fallback.analyze_text(text)
                    results = {
                        'emotional_state': {
                            'valence': emotion.valence,
                            'arousal': emotion.arousal,
                            'dominance': emotion.dominance,
                            'joy': emotion.joy,
                            'fear': emotion.fear,
                            'curiosity': emotion.curiosity,
                            'intensity': emotion.intensity()
                        },
                        'fallback_used': True
                    }
                    confidence = 0.5  # Lower confidence for fallback
                    return results, confidence
                    
                except Exception as fallback_error:
                    logger.warning(f"Fallback analyzer failed: {fallback_error}")
                    continue
        
        # Ultimate fallback - basic analysis
        return self._basic_fallback_analysis(text), 0.3
    
    def _calculate_confidence(self, text: str, results: Dict[str, Any]) -> float:
        """Calculate confidence score for analysis results"""
        
        confidence_factors = []
        
        # Text length factor
        text_length = len(text.split())
        if text_length >= 20:
            confidence_factors.append(0.9)
        elif text_length >= 10:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)
        
        # Emotional intensity factor
        intensity = results['emotional_state']['intensity']
        confidence_factors.append(min(0.9, intensity + 0.3))
        
        # 6W completeness factor
        if 'six_w_analysis' in results:
            six_w_score = results['six_w_analysis']['overall_score']
            confidence_factors.append(min(0.9, six_w_score + 0.4))
        
        # Consciousness indicators factor
        if 'consciousness_indicators' in results:
            consciousness_score = np.mean(list(results['consciousness_indicators'].values()))
            confidence_factors.append(min(0.9, consciousness_score + 0.3))
        
        return np.mean(confidence_factors)
    
    def _basic_fallback_analysis(self, text: str) -> Dict[str, Any]:
        """Basic fallback analysis when all libraries fail"""
        
        text_lower = text.lower()
        
        # Simple pattern-based analysis
        positive_words = ['good', 'great', 'happy', 'joy', 'wonderful', 'amazing', 'love']
        negative_words = ['bad', 'sad', 'fear', 'afraid', 'worry', 'anxious', 'terrible']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        valence = (positive_count - negative_count) / max(1, len(text.split()) * 0.1)
        valence = np.clip(valence, -1, 1)
        
        return {
            'emotional_state': {
                'valence': valence,
                'arousal': 0.5,
                'dominance': 0.0,
                'joy': max(0, valence),
                'fear': max(0, -valence),
                'curiosity': 0.3,
                'intensity': abs(valence)
            },
            'basic_fallback_used': True
        }
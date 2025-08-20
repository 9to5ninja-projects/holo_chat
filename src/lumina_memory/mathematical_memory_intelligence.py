"""
Mathematical Memory Intelligence
===============================

Advanced mathematical algorithms for intelligent memory management.
This module implements sophisticated importance calculation, predictive access
pattern learning, and relationship-aware storage optimization.

Day 18 Focus: Upgrade mathematical memory management from 53.5% → 85% effectiveness

Key Innovations:
- Multi-factor importance calculation with semantic analysis
- Predictive access pattern learning from actual usage
- Relationship-aware storage optimization
- Intelligent memory consolidation
- Adaptive algorithm tuning based on performance

Author: Lumina Memory Team
Date: August 19, 2025 (Day 18)
"""

import numpy as np
import time
import json
from typing import Dict, List, Any, Tuple, Optional, Set
from collections import defaultdict, deque
from dataclasses import dataclass, field
import logging
from datetime import datetime, timedelta

from .math_foundation import get_current_timestamp
from .xp_core_unified import XPUnit


@dataclass
class AccessPattern:
    """Represents an access pattern for learning"""
    unit_id: str
    access_time: float
    context_units: List[str] = field(default_factory=list)
    access_type: str = "retrieval"  # retrieval, creation, update
    user_engagement: float = 0.0  # 0-1 score


@dataclass
class ImportanceFactors:
    """Factors contributing to memory unit importance"""
    content_complexity: float = 0.0
    semantic_uniqueness: float = 0.0
    cognitive_pattern_density: float = 0.0
    cross_reference_potential: float = 0.0
    temporal_relevance: float = 0.0
    user_engagement_signals: float = 0.0
    access_frequency_boost: float = 0.0
    relationship_centrality: float = 0.0


class AdvancedImportanceCalculator:
    """Advanced multi-factor importance calculation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Configurable weights for different factors
        self.factor_weights = {
            'content_complexity': 0.15,
            'semantic_uniqueness': 0.20,
            'cognitive_pattern_density': 0.15,
            'cross_reference_potential': 0.15,
            'temporal_relevance': 0.10,
            'user_engagement_signals': 0.15,
            'access_frequency_boost': 0.05,
            'relationship_centrality': 0.05
        }
        
        # Vocabulary for complexity analysis
        self.complexity_indicators = {
            'high': ['analyze', 'synthesize', 'evaluate', 'consciousness', 'philosophy', 'framework', 'methodology', 'systematic'],
            'medium': ['understand', 'explore', 'consider', 'approach', 'concept', 'idea', 'think', 'question'],
            'low': ['yes', 'no', 'ok', 'thanks', 'hello', 'hi', 'bye', 'sure']
        }
        
        # Pattern importance multipliers
        self.pattern_importance = {
            'analytical_thinking': 1.3,
            'creative_archetype': 1.2,
            'mentor_archetype': 1.1,
            'collaborator_archetype': 1.0,
            'curiosity_response': 0.9,
            'emotional_processing': 0.8
        }
    
    def calculate_importance(self, unit: XPUnit, context: Dict[str, Any]) -> Tuple[float, ImportanceFactors]:
        """Calculate advanced importance score with detailed factors"""
        try:
            factors = ImportanceFactors()
            
            # 1. Content Complexity Analysis
            factors.content_complexity = self._analyze_content_complexity(unit.content)
            
            # 2. Semantic Uniqueness (compared to existing units)
            factors.semantic_uniqueness = self._calculate_semantic_uniqueness(unit, context.get('existing_units', []))
            
            # 3. Cognitive Pattern Density
            factors.cognitive_pattern_density = self._analyze_pattern_density(unit)
            
            # 4. Cross-Reference Potential
            factors.cross_reference_potential = self._calculate_reference_potential(unit, context.get('existing_units', []))
            
            # 5. Temporal Relevance
            factors.temporal_relevance = self._calculate_temporal_relevance(unit)
            
            # 6. User Engagement Signals
            factors.user_engagement_signals = self._analyze_engagement_signals(unit, context)
            
            # 7. Access Frequency Boost
            factors.access_frequency_boost = self._calculate_access_boost(unit, context.get('access_history', []))
            
            # 8. Relationship Centrality
            factors.relationship_centrality = self._calculate_relationship_centrality(unit, context.get('relationship_graph', {}))
            
            # Combine factors with weights
            importance = self._combine_factors(factors)
            
            # Apply bounds and normalization
            importance = max(0.0, min(1.0, importance))
            
            self.logger.debug(f"Calculated importance {importance:.3f} for unit {unit.content_id[:8]}...")
            
            return importance, factors
            
        except Exception as e:
            self.logger.error(f"Error calculating importance: {e}")
            return 0.5, ImportanceFactors()  # Default moderate importance
    
    def _analyze_content_complexity(self, content: str) -> float:
        """Analyze content complexity based on linguistic features"""
        try:
            words = content.lower().split()
            if not words:
                return 0.0
            
            # Length factor (longer content often more complex)
            length_factor = min(len(words) / 50.0, 1.0)  # Normalize to 50 words
            
            # Vocabulary complexity
            high_complexity = sum(1 for word in words if any(indicator in word for indicator in self.complexity_indicators['high']))
            medium_complexity = sum(1 for word in words if any(indicator in word for indicator in self.complexity_indicators['medium']))
            low_complexity = sum(1 for word in words if any(indicator in word for indicator in self.complexity_indicators['low']))
            
            # Calculate complexity score
            complexity_score = (high_complexity * 1.0 + medium_complexity * 0.5 + low_complexity * 0.1) / len(words)
            
            # Sentence structure complexity (simple heuristic)
            sentences = content.split('.')
            avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
            structure_factor = min(avg_sentence_length / 15.0, 1.0)  # Normalize to 15 words per sentence
            
            # Combine factors
            final_complexity = (length_factor * 0.3 + complexity_score * 0.5 + structure_factor * 0.2)
            
            return min(final_complexity, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error analyzing content complexity: {e}")
            return 0.5
    
    def _calculate_semantic_uniqueness(self, unit: XPUnit, existing_units: List[XPUnit]) -> float:
        """Calculate how semantically unique this unit is"""
        try:
            if not existing_units:
                return 1.0  # First unit is completely unique
            
            # Simple semantic similarity based on word overlap
            unit_words = set(unit.content.lower().split())
            
            similarities = []
            for existing_unit in existing_units[-20:]:  # Compare with recent 20 units
                existing_words = set(existing_unit.content.lower().split())
                
                if not unit_words or not existing_words:
                    similarities.append(0.0)
                    continue
                
                # Jaccard similarity
                intersection = len(unit_words & existing_words)
                union = len(unit_words | existing_words)
                similarity = intersection / union if union > 0 else 0.0
                similarities.append(similarity)
            
            # Uniqueness is inverse of maximum similarity
            max_similarity = max(similarities) if similarities else 0.0
            uniqueness = 1.0 - max_similarity
            
            return uniqueness
            
        except Exception as e:
            self.logger.error(f"Error calculating semantic uniqueness: {e}")
            return 0.5
    
    def _analyze_pattern_density(self, unit: XPUnit) -> float:
        """Analyze cognitive pattern density in the unit"""
        try:
            if not unit.metadata or 'cognitive_patterns' not in unit.metadata:
                return 0.0
            
            patterns = unit.metadata['cognitive_patterns']
            if not patterns:
                return 0.0
            
            # Calculate pattern importance score
            pattern_score = 0.0
            for pattern in patterns:
                if isinstance(pattern, str):
                    pattern_score += self.pattern_importance.get(pattern, 0.5)
                elif isinstance(pattern, dict) and 'type' in pattern:
                    base_score = self.pattern_importance.get(pattern['type'], 0.5)
                    confidence = pattern.get('confidence', 0.5)
                    pattern_score += base_score * confidence
            
            # Normalize by number of patterns (avoid just counting patterns)
            normalized_score = pattern_score / max(len(patterns), 1)
            
            return min(normalized_score, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error analyzing pattern density: {e}")
            return 0.0
    
    def _calculate_reference_potential(self, unit: XPUnit, existing_units: List[XPUnit]) -> float:
        """Calculate potential for this unit to be referenced by future units"""
        try:
            # Key concepts that are likely to be referenced
            reference_indicators = [
                'framework', 'method', 'approach', 'principle', 'concept',
                'theory', 'model', 'system', 'process', 'strategy'
            ]
            
            content_lower = unit.content.lower()
            reference_score = sum(1 for indicator in reference_indicators if indicator in content_lower)
            
            # Normalize by content length
            words = content_lower.split()
            if words:
                reference_density = reference_score / len(words)
            else:
                reference_density = 0.0
            
            # Boost for question-like content (likely to be referenced)
            if '?' in unit.content:
                reference_density *= 1.2
            
            # Boost for definitive statements
            if any(phrase in content_lower for phrase in ['is defined as', 'means that', 'refers to']):
                reference_density *= 1.3
            
            return min(reference_density * 10, 1.0)  # Scale up and cap at 1.0
            
        except Exception as e:
            self.logger.error(f"Error calculating reference potential: {e}")
            return 0.5
    
    def _calculate_temporal_relevance(self, unit: XPUnit) -> float:
        """Calculate temporal relevance (recency and time-sensitive content)"""
        try:
            current_time = get_current_timestamp()
            
            # Get unit creation time
            if unit.metadata and 'created_timestamp' in unit.metadata:
                created_time = unit.metadata['created_timestamp']
            else:
                created_time = current_time  # Assume recent if no timestamp
            
            # Recency factor (exponential decay)
            time_diff = current_time - created_time
            hours_old = time_diff / 3600.0  # Convert to hours
            
            # Decay over 24 hours
            recency_factor = np.exp(-hours_old / 24.0)
            
            # Time-sensitive content indicators
            time_sensitive_words = ['now', 'today', 'current', 'recent', 'latest', 'urgent', 'immediate']
            content_lower = unit.content.lower()
            time_sensitivity = sum(1 for word in time_sensitive_words if word in content_lower)
            time_sensitivity_factor = min(time_sensitivity * 0.2, 1.0)
            
            # Combine factors
            temporal_relevance = recency_factor * 0.7 + time_sensitivity_factor * 0.3
            
            return temporal_relevance
            
        except Exception as e:
            self.logger.error(f"Error calculating temporal relevance: {e}")
            return 0.5
    
    def _analyze_engagement_signals(self, unit: XPUnit, context: Dict[str, Any]) -> float:
        """Analyze user engagement signals"""
        try:
            engagement_score = 0.0
            
            # Message type importance
            if unit.metadata:
                msg_type = unit.metadata.get('type', 'unknown')
                type_scores = {
                    'user_message': 0.8,  # User messages are important
                    'assistant_response': 0.6,  # Responses are moderately important
                    'system': 0.2,  # System messages less important
                    'error': 0.1   # Errors least important
                }
                engagement_score += type_scores.get(msg_type, 0.5)
            
            # Content length as engagement indicator
            content_length = len(unit.content.split())
            if content_length > 20:  # Longer messages show more engagement
                engagement_score += 0.2
            elif content_length > 50:
                engagement_score += 0.4
            
            # Question marks indicate engagement
            if '?' in unit.content:
                engagement_score += 0.3
            
            # Exclamation marks indicate enthusiasm
            if '!' in unit.content:
                engagement_score += 0.2
            
            return min(engagement_score, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error analyzing engagement signals: {e}")
            return 0.5
    
    def _calculate_access_boost(self, unit: XPUnit, access_history: List[AccessPattern]) -> float:
        """Calculate boost based on access history"""
        try:
            if not access_history:
                return 0.0
            
            # Count accesses for this unit
            unit_accesses = [access for access in access_history if access.unit_id == unit.content_id]
            
            if not unit_accesses:
                return 0.0
            
            # Recent access boost
            current_time = get_current_timestamp()
            recent_accesses = [access for access in unit_accesses 
                             if current_time - access.access_time < 3600]  # Last hour
            
            recent_boost = len(recent_accesses) * 0.2
            
            # Total access frequency boost
            total_boost = len(unit_accesses) * 0.1
            
            return min(recent_boost + total_boost, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating access boost: {e}")
            return 0.0
    
    def _calculate_relationship_centrality(self, unit: XPUnit, relationship_graph: Dict[str, List[str]]) -> float:
        """Calculate centrality in the relationship graph"""
        try:
            if not relationship_graph or unit.content_id not in relationship_graph:
                return 0.0
            
            # Simple degree centrality
            connections = len(relationship_graph.get(unit.content_id, []))
            
            # Normalize by maximum possible connections (simplified)
            max_connections = max(len(connections) for connections in relationship_graph.values()) if relationship_graph else 1
            
            centrality = connections / max(max_connections, 1)
            
            return min(centrality, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating relationship centrality: {e}")
            return 0.0
    
    def _combine_factors(self, factors: ImportanceFactors) -> float:
        """Combine all factors using weighted sum"""
        try:
            total_score = 0.0
            
            factor_values = {
                'content_complexity': factors.content_complexity,
                'semantic_uniqueness': factors.semantic_uniqueness,
                'cognitive_pattern_density': factors.cognitive_pattern_density,
                'cross_reference_potential': factors.cross_reference_potential,
                'temporal_relevance': factors.temporal_relevance,
                'user_engagement_signals': factors.user_engagement_signals,
                'access_frequency_boost': factors.access_frequency_boost,
                'relationship_centrality': factors.relationship_centrality
            }
            
            for factor_name, factor_value in factor_values.items():
                weight = self.factor_weights.get(factor_name, 0.0)
                total_score += factor_value * weight
            
            return total_score
            
        except Exception as e:
            self.logger.error(f"Error combining factors: {e}")
            return 0.5


class PredictiveAccessPatternLearner:
    """Learn and predict access patterns from usage history"""
    
    def __init__(self, max_history_size: int = 1000):
        self.logger = logging.getLogger(__name__)
        self.access_history: deque = deque(maxlen=max_history_size)
        self.pattern_models: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.context_patterns: Dict[str, List[str]] = defaultdict(list)
        
    def record_access(self, unit_id: str, access_type: str = "retrieval", 
                     context_units: List[str] = None, user_engagement: float = 0.5):
        """Record an access event for learning"""
        try:
            access_pattern = AccessPattern(
                unit_id=unit_id,
                access_time=get_current_timestamp(),
                context_units=context_units or [],
                access_type=access_type,
                user_engagement=user_engagement
            )
            
            self.access_history.append(access_pattern)
            self._update_models(access_pattern)
            
        except Exception as e:
            self.logger.error(f"Error recording access: {e}")
    
    def predict_access_frequency(self, unit: XPUnit, context: Dict[str, Any]) -> float:
        """Predict future access frequency for a unit"""
        try:
            if not self.access_history:
                return 0.5  # Default prediction
            
            # Base frequency from historical data
            unit_accesses = [access for access in self.access_history if access.unit_id == unit.content_id]
            base_frequency = len(unit_accesses) / len(self.access_history)
            
            # Context-based prediction
            context_boost = self._calculate_context_boost(unit, context)
            
            # Temporal pattern prediction
            temporal_boost = self._calculate_temporal_boost(unit)
            
            # Content-based prediction
            content_boost = self._calculate_content_boost(unit)
            
            # Combine predictions
            predicted_frequency = (
                base_frequency * 0.4 +
                context_boost * 0.3 +
                temporal_boost * 0.2 +
                content_boost * 0.1
            )
            
            return min(predicted_frequency, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error predicting access frequency: {e}")
            return 0.5
    
    def _update_models(self, access_pattern: AccessPattern):
        """Update internal prediction models"""
        try:
            # Update frequency model
            self.pattern_models[access_pattern.unit_id]['total_accesses'] += 1
            self.pattern_models[access_pattern.unit_id]['last_access'] = access_pattern.access_time
            
            # Update context patterns
            for context_unit in access_pattern.context_units:
                self.context_patterns[access_pattern.unit_id].append(context_unit)
                # Keep only recent context (last 10)
                if len(self.context_patterns[access_pattern.unit_id]) > 10:
                    self.context_patterns[access_pattern.unit_id].pop(0)
            
        except Exception as e:
            self.logger.error(f"Error updating models: {e}")
    
    def _calculate_context_boost(self, unit: XPUnit, context: Dict[str, Any]) -> float:
        """Calculate boost based on current context"""
        try:
            if unit.content_id not in self.context_patterns:
                return 0.0
            
            current_context = context.get('recent_units', [])
            if not current_context:
                return 0.0
            
            # Check for context overlap
            historical_context = self.context_patterns[unit.content_id]
            overlap = len(set(current_context) & set(historical_context))
            
            if not historical_context:
                return 0.0
            
            context_similarity = overlap / len(historical_context)
            return context_similarity
            
        except Exception as e:
            self.logger.error(f"Error calculating context boost: {e}")
            return 0.0
    
    def _calculate_temporal_boost(self, unit: XPUnit) -> float:
        """Calculate boost based on temporal access patterns"""
        try:
            if unit.content_id not in self.pattern_models:
                return 0.0
            
            last_access = self.pattern_models[unit.content_id].get('last_access', 0)
            if last_access == 0:
                return 0.0
            
            current_time = get_current_timestamp()
            time_since_access = current_time - last_access
            
            # Units accessed recently are more likely to be accessed again
            hours_since = time_since_access / 3600.0
            temporal_boost = np.exp(-hours_since / 12.0)  # 12-hour decay
            
            return temporal_boost
            
        except Exception as e:
            self.logger.error(f"Error calculating temporal boost: {e}")
            return 0.0
    
    def _calculate_content_boost(self, unit: XPUnit) -> float:
        """Calculate boost based on content characteristics"""
        try:
            # Units with certain content types are accessed more frequently
            content_lower = unit.content.lower()
            
            high_access_indicators = ['question', 'how', 'what', 'why', 'explain', 'define']
            boost_score = sum(1 for indicator in high_access_indicators if indicator in content_lower)
            
            # Normalize
            content_boost = min(boost_score * 0.2, 1.0)
            
            return content_boost
            
        except Exception as e:
            self.logger.error(f"Error calculating content boost: {e}")
            return 0.0


class IntelligentStorageOptimizer:
    """Intelligent storage optimization with relationship awareness"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Storage tier thresholds (can be adaptive)
        self.tier_thresholds = {
            'hot': 0.8,      # High importance, high access frequency
            'warm': 0.5,     # Medium importance or access frequency
            'cold': 0.2,     # Low importance and access frequency
            'archive': 0.0   # Very low importance, rarely accessed
        }
        
        # Consolidation parameters
        self.consolidation_similarity_threshold = 0.8
        self.consolidation_min_units = 3
    
    def optimize_storage_with_relationships(self, units: Dict[str, XPUnit], 
                                          importance_scores: Dict[str, float],
                                          access_frequencies: Dict[str, float],
                                          relationship_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """Optimize storage considering unit relationships"""
        try:
            start_time = time.time()
            
            # Assign storage tiers
            tier_assignments = self._assign_storage_tiers(units, importance_scores, access_frequencies)
            
            # Identify consolidation opportunities
            consolidation_opportunities = self._identify_consolidation_opportunities(
                units, importance_scores, relationship_graph
            )
            
            # Calculate storage efficiency improvement
            efficiency_improvement = self._calculate_efficiency_improvement(
                units, tier_assignments, consolidation_opportunities
            )
            
            # Generate performance metrics
            performance_metrics = self._generate_performance_metrics(
                units, tier_assignments, importance_scores, access_frequencies
            )
            
            optimization_time = time.time() - start_time
            
            return {
                'tier_assignments': tier_assignments,
                'consolidation_opportunities': consolidation_opportunities,
                'storage_efficiency_improvement': efficiency_improvement,
                'optimization_time': optimization_time,
                'performance_metrics': performance_metrics
            }
            
        except Exception as e:
            self.logger.error(f"Error in storage optimization: {e}")
            return {
                'tier_assignments': {},
                'consolidation_opportunities': 0,
                'storage_efficiency_improvement': 0.0,
                'optimization_time': 0.0,
                'performance_metrics': {}
            }
    
    def _assign_storage_tiers(self, units: Dict[str, XPUnit], 
                            importance_scores: Dict[str, float],
                            access_frequencies: Dict[str, float]) -> Dict[str, int]:
        """Assign storage tiers based on importance and access patterns"""
        try:
            tier_assignments = {'hot': 0, 'warm': 0, 'cold': 0, 'archive': 0}
            
            for unit_id, unit in units.items():
                importance = importance_scores.get(unit_id, 0.5)
                access_freq = access_frequencies.get(unit_id, 0.5)
                
                # Combined score for tier assignment
                combined_score = importance * 0.7 + access_freq * 0.3
                
                # Assign tier
                if combined_score >= self.tier_thresholds['hot']:
                    tier = 'hot'
                elif combined_score >= self.tier_thresholds['warm']:
                    tier = 'warm'
                elif combined_score >= self.tier_thresholds['cold']:
                    tier = 'cold'
                else:
                    tier = 'archive'
                
                tier_assignments[tier] += 1
                
                # Update unit metadata
                if not unit.metadata:
                    unit.metadata = {}
                unit.metadata['storage_tier'] = tier
                unit.metadata['combined_score'] = combined_score
            
            return tier_assignments
            
        except Exception as e:
            self.logger.error(f"Error assigning storage tiers: {e}")
            return {'hot': 0, 'warm': 0, 'cold': 0, 'archive': 0}
    
    def _identify_consolidation_opportunities(self, units: Dict[str, XPUnit],
                                           importance_scores: Dict[str, float],
                                           relationship_graph: Dict[str, List[str]]) -> int:
        """Identify opportunities for memory consolidation"""
        try:
            consolidation_count = 0
            
            # Group units by similarity and low importance
            low_importance_units = [
                unit_id for unit_id, importance in importance_scores.items()
                if importance < 0.3
            ]
            
            # Simple consolidation: group similar low-importance units
            similarity_groups = []
            processed_units = set()
            
            for unit_id in low_importance_units:
                if unit_id in processed_units:
                    continue
                
                unit = units[unit_id]
                similar_units = [unit_id]
                
                # Find similar units
                for other_unit_id in low_importance_units:
                    if other_unit_id == unit_id or other_unit_id in processed_units:
                        continue
                    
                    other_unit = units[other_unit_id]
                    similarity = self._calculate_content_similarity(unit.content, other_unit.content)
                    
                    if similarity >= self.consolidation_similarity_threshold:
                        similar_units.append(other_unit_id)
                        processed_units.add(other_unit_id)
                
                if len(similar_units) >= self.consolidation_min_units:
                    similarity_groups.append(similar_units)
                    consolidation_count += 1
                    processed_units.add(unit_id)
            
            return consolidation_count
            
        except Exception as e:
            self.logger.error(f"Error identifying consolidation opportunities: {e}")
            return 0
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two content strings"""
        try:
            words1 = set(content1.lower().split())
            words2 = set(content2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = len(words1 & words2)
            union = len(words1 | words2)
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating content similarity: {e}")
            return 0.0
    
    def _calculate_efficiency_improvement(self, units: Dict[str, XPUnit],
                                        tier_assignments: Dict[str, int],
                                        consolidation_opportunities: int) -> float:
        """Calculate storage efficiency improvement"""
        try:
            total_units = len(units)
            if total_units == 0:
                return 1.0
            
            # Efficiency based on tier distribution
            hot_ratio = tier_assignments['hot'] / total_units
            warm_ratio = tier_assignments['warm'] / total_units
            cold_ratio = tier_assignments['cold'] / total_units
            archive_ratio = tier_assignments['archive'] / total_units
            
            # Ideal distribution: some hot, mostly warm, some cold, minimal archive
            ideal_efficiency = (
                min(hot_ratio, 0.2) * 1.0 +      # Up to 20% hot is good
                min(warm_ratio, 0.6) * 1.0 +     # Up to 60% warm is good
                min(cold_ratio, 0.3) * 0.8 +     # Up to 30% cold is acceptable
                archive_ratio * 0.5               # Archive is less efficient but necessary
            )
            
            # Consolidation efficiency bonus
            consolidation_bonus = min(consolidation_opportunities * 0.1, 0.2)
            
            total_efficiency = ideal_efficiency + consolidation_bonus
            
            return min(total_efficiency, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating efficiency improvement: {e}")
            return 0.5
    
    def _generate_performance_metrics(self, units: Dict[str, XPUnit],
                                    tier_assignments: Dict[str, int],
                                    importance_scores: Dict[str, float],
                                    access_frequencies: Dict[str, float]) -> Dict[str, Any]:
        """Generate detailed performance metrics"""
        try:
            metrics = {}
            
            if importance_scores:
                metrics['avg_importance'] = sum(importance_scores.values()) / len(importance_scores)
                metrics['importance_std'] = np.std(list(importance_scores.values()))
            
            if access_frequencies:
                metrics['avg_access_frequency'] = sum(access_frequencies.values()) / len(access_frequencies)
                metrics['access_frequency_std'] = np.std(list(access_frequencies.values()))
            
            metrics['tier_distribution'] = tier_assignments
            metrics['total_units'] = len(units)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error generating performance metrics: {e}")
            return {}


class MathematicalMemoryIntelligence:
    """Main class coordinating all mathematical memory intelligence components"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.importance_calculator = AdvancedImportanceCalculator()
        self.access_learner = PredictiveAccessPatternLearner()
        self.storage_optimizer = IntelligentStorageOptimizer()
        
        # Performance tracking
        self.performance_history = []
        self.optimization_count = 0
    
    def calculate_enhanced_importance(self, unit: XPUnit, context: Dict[str, Any] = None) -> float:
        """Calculate enhanced importance using advanced algorithms"""
        try:
            context = context or {}
            importance, factors = self.importance_calculator.calculate_importance(unit, context)
            
            # Store factors in unit metadata for analysis
            if not unit.metadata:
                unit.metadata = {}
            unit.metadata['importance_factors'] = factors.__dict__
            unit.metadata['importance_score'] = importance
            
            return importance
            
        except Exception as e:
            self.logger.error(f"Error calculating enhanced importance: {e}")
            return 0.5
    
    def predict_access_frequency(self, unit: XPUnit, context: Dict[str, Any] = None) -> float:
        """Predict access frequency using learning algorithms"""
        try:
            context = context or {}
            frequency = self.access_learner.predict_access_frequency(unit, context)
            
            # Store prediction in unit metadata
            if not unit.metadata:
                unit.metadata = {}
            unit.metadata['predicted_access_frequency'] = frequency
            
            return frequency
            
        except Exception as e:
            self.logger.error(f"Error predicting access frequency: {e}")
            return 0.5
    
    def optimize_storage_comprehensive(self, units: Dict[str, XPUnit],
                                     relationship_graph: Dict[str, List[str]] = None) -> Dict[str, Any]:
        """Perform comprehensive storage optimization"""
        try:
            self.optimization_count += 1
            
            # Calculate importance scores for all units
            importance_scores = {}
            access_frequencies = {}
            
            context = {
                'existing_units': list(units.values()),
                'relationship_graph': relationship_graph or {}
            }
            
            for unit_id, unit in units.items():
                importance_scores[unit_id] = self.calculate_enhanced_importance(unit, context)
                access_frequencies[unit_id] = self.predict_access_frequency(unit, context)
            
            # Perform storage optimization
            optimization_result = self.storage_optimizer.optimize_storage_with_relationships(
                units, importance_scores, access_frequencies, relationship_graph or {}
            )
            
            # Track performance
            self.performance_history.append({
                'timestamp': get_current_timestamp(),
                'optimization_count': self.optimization_count,
                'units_processed': len(units),
                'avg_importance': sum(importance_scores.values()) / len(importance_scores) if importance_scores else 0,
                'efficiency_improvement': optimization_result['storage_efficiency_improvement']
            })
            
            # Add metadata to result
            optimization_result['units_processed'] = len(units)
            optimization_result['optimization_count'] = self.optimization_count
            
            return optimization_result
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive storage optimization: {e}")
            return {
                'tier_assignments': {'hot': 0, 'warm': 0, 'cold': 0, 'archive': 0},
                'consolidation_opportunities': 0,
                'storage_efficiency_improvement': 0.0,
                'optimization_time': 0.0,
                'performance_metrics': {},
                'units_processed': 0,
                'optimization_count': self.optimization_count
            }
    
    def record_access(self, unit_id: str, access_type: str = "retrieval",
                     context_units: List[str] = None, user_engagement: float = 0.5):
        """Record access for learning"""
        self.access_learner.record_access(unit_id, access_type, context_units, user_engagement)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary of mathematical memory intelligence"""
        try:
            if not self.performance_history:
                return {'status': 'no_data'}
            
            recent_performance = self.performance_history[-10:]  # Last 10 optimizations
            
            return {
                'total_optimizations': self.optimization_count,
                'avg_efficiency_improvement': sum(p['efficiency_improvement'] for p in recent_performance) / len(recent_performance),
                'avg_units_processed': sum(p['units_processed'] for p in recent_performance) / len(recent_performance),
                'avg_importance_score': sum(p['avg_importance'] for p in recent_performance) / len(recent_performance),
                'performance_trend': 'improving' if len(recent_performance) > 1 and recent_performance[-1]['efficiency_improvement'] > recent_performance[0]['efficiency_improvement'] else 'stable',
                'last_optimization': recent_performance[-1] if recent_performance else None
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance summary: {e}")
            return {'status': 'error', 'error': str(e)}
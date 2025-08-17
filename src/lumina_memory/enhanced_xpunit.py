"""
Enhanced XPUnit with Holographic Memory Integration
==================================================

This module integrates the rigorous holographic memory specification with our
existing XPUnit system, creating a mathematically sound foundation for
experience units with:

- HRR-based holographic representation
- Role-filler capsule architecture
- Consciousness analysis integration
- Global associative memory capabilities
- Compositional query support

Author: Lumina Memory Team
License: MIT
"""

import numpy as np
import time
import hashlib
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime

# Import holographic memory foundation
from .holographic_memory import (
    MemoryCapsule, HolographicAssociativeMemory, RoleSpace, SymbolSpace,
    circular_convolution, circular_correlation, normalize_vector, cosine_similarity
)

# Import existing components
from .constants import (
    PHI, TAU, HRR_DIM, SEMANTIC_DIM, HOLOGRAPHIC_DIM,
    CONSCIOUSNESS_SELF_REFERENCE_WEIGHT, CONSCIOUSNESS_INTROSPECTION_WEIGHT,
    CONSCIOUSNESS_RECURSIVE_WEIGHT, CONSCIOUSNESS_INTROSPECTION_WORDS,
    HIGH_CONSCIOUSNESS_THRESHOLD, MEDIUM_CONSCIOUSNESS_THRESHOLD,
    DEFAULT_IMPORTANCE, DEFAULT_DECAY_RATE
)

# =============================================================================
# ENHANCED XPUNIT WITH HOLOGRAPHIC FOUNDATION
# =============================================================================

@dataclass
class EnhancedXPUnit:
    """
    Enhanced XPUnit with integrated holographic memory capabilities
    
    Combines:
    - Original XPUnit mathematical properties
    - Holographic memory capsule architecture
    - Consciousness analysis from notebooks
    - Role-filler binding operations
    """
    
    # Core identity and content
    content_id: str
    content: str
    timestamp: float = field(default_factory=time.time)
    
    # Holographic memory capsule
    memory_capsule: MemoryCapsule = field(init=False)
    
    # Mathematical representations
    semantic_vector: Optional[np.ndarray] = None
    emotion_vector: Optional[np.ndarray] = None
    
    # Consciousness analysis
    consciousness_score: float = 0.0
    consciousness_indicators: Dict[str, float] = field(default_factory=dict)
    
    # Importance and salience
    importance: float = DEFAULT_IMPORTANCE
    salience: float = 1.0
    reliability: float = 1.0
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize the holographic memory capsule"""
        self.memory_capsule = MemoryCapsule(
            timestamp=self.timestamp,
            importance=self.importance,
            salience=self.salience,
            reliability=self.reliability
        )
        
        # Analyze consciousness if content is provided
        if self.content:
            self._analyze_consciousness()
            
        # Create initial role-filler bindings
        self._create_initial_bindings()
        
    def _analyze_consciousness(self):
        """
        Analyze consciousness indicators in the content
        Based on notebook developments in xpunit_full_system_test.ipynb
        """
        content_lower = self.content.lower()
        
        # Self-reference analysis
        if "i am" in content_lower or "my own" in content_lower:
            self.consciousness_score += CONSCIOUSNESS_SELF_REFERENCE_WEIGHT
            self.consciousness_indicators["self_reference"] = 0.8
            
        # Introspection analysis
        introspection_count = sum(1 for word in CONSCIOUSNESS_INTROSPECTION_WORDS 
                                 if word in content_lower)
        if introspection_count > 0:
            self.consciousness_score += CONSCIOUSNESS_INTROSPECTION_WEIGHT * introspection_count
            self.consciousness_indicators["introspection"] = min(1.0, introspection_count * 0.3)
            
        # Recursive processing (thinking about thinking)
        if ("thought" in content_lower and 
            ("my" in content_lower or "own" in content_lower)):
            self.consciousness_score += CONSCIOUSNESS_RECURSIVE_WEIGHT
            self.consciousness_indicators["recursive_processing"] = 0.9
            
        # Consciousness boosts importance
        self.importance = 1.0 + self.consciousness_score
        
    def _create_initial_bindings(self):
        """Create initial role-filler bindings from content"""
        # WHAT role - bind to content representation
        if self.semantic_vector is not None:
            self.memory_capsule.add_binding("WHAT", self.semantic_vector, 1.0)
        else:
            # Create content-based vector
            content_vector = self._encode_content_to_vector()
            self.memory_capsule.add_binding("WHAT", content_vector, 1.0)
            
        # WHEN role - bind to temporal representation
        time_vector = self._encode_time_to_vector()
        self.memory_capsule.add_binding("WHEN", time_vector, 0.8)
        
        # HOW role - bind to consciousness representation
        consciousness_vector = self._encode_consciousness_to_vector()
        self.memory_capsule.add_binding("HOW", consciousness_vector, 0.6)
        
        # EMOTION role - bind to emotional representation
        if self.emotion_vector is not None:
            self.memory_capsule.add_binding("EMOTION", self.emotion_vector, 0.7)
            
    def _encode_content_to_vector(self) -> np.ndarray:
        """Encode content to vector representation"""
        # Use deterministic hash-based encoding with fixed dimension
        target_dim = HRR_DIM
        
        # Create deterministic seed from content
        content_hash = hashlib.blake2b(self.content.encode(), digest_size=8).digest()
        seed = int.from_bytes(content_hash, byteorder='big') % (2**31)
        
        # Generate vector with fixed dimension
        rng = np.random.RandomState(seed)
        vector = rng.randn(target_dim).astype(np.float32)
            
        return normalize_vector(vector)
        
    def _encode_time_to_vector(self) -> np.ndarray:
        """Encode timestamp to vector using golden ratio and tau"""
        # Use PHI and TAU for temporal encoding
        t_normalized = (self.timestamp % (24 * 3600)) / (24 * 3600)  # Normalize to day cycle
        
        # Create temporal pattern using mathematical constants
        dim = HRR_DIM
        indices = np.arange(dim)
        
        # Golden ratio spiral encoding
        phi_pattern = np.cos(2 * np.pi * PHI * indices * t_normalized)
        tau_pattern = np.sin(TAU * indices * t_normalized / dim)
        
        temporal_vector = phi_pattern + 1j * tau_pattern
        return normalize_vector(temporal_vector.real)
        
    def _encode_consciousness_to_vector(self) -> np.ndarray:
        """Encode consciousness indicators to vector"""
        dim = HRR_DIM
        consciousness_vector = np.zeros(dim)
        
        # Encode consciousness score
        consciousness_vector[0] = self.consciousness_score
        
        # Encode individual indicators
        for i, (indicator, value) in enumerate(self.consciousness_indicators.items()):
            if i + 1 < dim:
                consciousness_vector[i + 1] = value
                
        return normalize_vector(consciousness_vector)
        
    def add_role_binding(self, role_name: str, symbol_vector: np.ndarray, weight: float = 1.0):
        """Add a new role-filler binding"""
        self.memory_capsule.add_binding(role_name, symbol_vector, weight)
        
    def query_role(self, role_name: str) -> np.ndarray:
        """Query a role from this XPUnit's memory capsule"""
        return self.memory_capsule.unbind_role(role_name)
        
    def get_holographic_vector(self) -> np.ndarray:
        """Get the holographic representation vector"""
        return self.memory_capsule.vector
        
    def similarity_to(self, other: 'EnhancedXPUnit') -> float:
        """Compute similarity to another XPUnit"""
        return cosine_similarity(self.get_holographic_vector(), other.get_holographic_vector())
        
    def get_consciousness_level(self) -> str:
        """Get consciousness level classification"""
        if self.consciousness_score > HIGH_CONSCIOUSNESS_THRESHOLD:
            return "HIGH"
        elif self.consciousness_score > MEDIUM_CONSCIOUSNESS_THRESHOLD:
            return "MEDIUM"
        else:
            return "LOW"
            
    def get_age_hours(self) -> float:
        """Get age in hours"""
        return (time.time() - self.timestamp) / 3600.0
        
    def get_decay_factor(self, decay_rate: float = DEFAULT_DECAY_RATE) -> float:
        """Get exponential decay factor"""
        return np.exp(-decay_rate * self.get_age_hours())
        
    def get_effective_importance(self, decay_rate: float = DEFAULT_DECAY_RATE) -> float:
        """Get importance adjusted for decay and consciousness"""
        base_importance = self.importance * self.get_decay_factor(decay_rate) * self.reliability
        consciousness_boost = 1.0 + (self.consciousness_score * 0.5)  # Up to 50% boost
        return base_importance * consciousness_boost
        
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'content_id': self.content_id,
            'content': self.content,
            'timestamp': self.timestamp,
            'consciousness_score': self.consciousness_score,
            'consciousness_indicators': self.consciousness_indicators,
            'importance': self.importance,
            'salience': self.salience,
            'reliability': self.reliability,
            'metadata': self.metadata,
            'memory_capsule': self.memory_capsule.to_dict(),
            'semantic_vector': self.semantic_vector.tolist() if self.semantic_vector is not None else None,
            'emotion_vector': self.emotion_vector.tolist() if self.emotion_vector is not None else None
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedXPUnit':
        """Deserialize from dictionary"""
        # Create basic XPUnit
        xpunit = cls(
            content_id=data['content_id'],
            content=data['content'],
            timestamp=data['timestamp']
        )
        
        # Restore properties
        xpunit.consciousness_score = data['consciousness_score']
        xpunit.consciousness_indicators = data['consciousness_indicators']
        xpunit.importance = data['importance']
        xpunit.salience = data['salience']
        xpunit.reliability = data['reliability']
        xpunit.metadata = data['metadata']
        
        # Restore vectors
        if data['semantic_vector']:
            xpunit.semantic_vector = np.array(data['semantic_vector'])
        if data['emotion_vector']:
            xpunit.emotion_vector = np.array(data['emotion_vector'])
            
        # Restore memory capsule
        xpunit.memory_capsule = MemoryCapsule.from_dict(data['memory_capsule'])
        
        return xpunit

# =============================================================================
# ENHANCED XP ENVIRONMENT WITH HOLOGRAPHIC MEMORY
# =============================================================================

class EnhancedXPEnvironment:
    """
    Enhanced XP Environment with integrated holographic associative memory
    
    Provides:
    - Global holographic memory management
    - Compositional queries across XPUnits
    - Consciousness-aware retrieval
    - Capacity management and optimization
    """
    
    def __init__(self, dimension: int = HRR_DIM, decay_rate: float = DEFAULT_DECAY_RATE):
        self.dimension = dimension
        self.decay_rate = decay_rate
        
        # Holographic memory system
        self.holographic_memory = HolographicAssociativeMemory(dimension, decay_rate)
        
        # XPUnit storage
        self.xpunits: Dict[str, EnhancedXPUnit] = {}
        
        # Statistics
        self.total_ingested = 0
        self.total_queries = 0
        
    def ingest_experience(self, content: str, 
                         semantic_vector: Optional[np.ndarray] = None,
                         emotion_vector: Optional[np.ndarray] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> EnhancedXPUnit:
        """
        Ingest a new experience as an Enhanced XPUnit
        
        Args:
            content: Text content of the experience
            semantic_vector: Optional semantic representation
            emotion_vector: Optional emotional representation
            metadata: Optional metadata
            
        Returns:
            Created EnhancedXPUnit
        """
        # Generate content ID
        content_id = hashlib.blake2b(content.encode(), digest_size=16).hexdigest()
        
        # Create XPUnit
        xpunit = EnhancedXPUnit(
            content_id=content_id,
            content=content,
            semantic_vector=semantic_vector,
            emotion_vector=emotion_vector,
            metadata=metadata or {}
        )
        
        # Store XPUnit
        self.xpunits[content_id] = xpunit
        
        # Add to holographic memory
        self.holographic_memory.add_capsule(xpunit.memory_capsule)
        
        self.total_ingested += 1
        return xpunit
        
    def query_role(self, role_name: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Query a role from global holographic memory
        
        Args:
            role_name: Role to query
            top_k: Number of top matches
            
        Returns:
            List of (symbol_name, similarity_score) tuples
        """
        self.total_queries += 1
        return self.holographic_memory.find_best_symbol_for_role(role_name, top_k=top_k)
        
    def compositional_query(self, query_bindings: Dict[str, str], 
                           top_k: int = 10) -> List[Tuple[EnhancedXPUnit, float]]:
        """
        Perform compositional query across XPUnits
        
        Args:
            query_bindings: Dict of role_name -> symbol_name
            top_k: Number of top matches
            
        Returns:
            List of (XPUnit, similarity_score) tuples
        """
        self.total_queries += 1
        
        # Query holographic memory
        capsule_matches = self.holographic_memory.compositional_query(query_bindings)
        
        # Map back to XPUnits
        xpunit_matches = []
        for capsule, similarity in capsule_matches[:top_k]:
            # Find XPUnit with matching capsule
            for xpunit in self.xpunits.values():
                if xpunit.memory_capsule is capsule:
                    xpunit_matches.append((xpunit, similarity))
                    break
                    
        return xpunit_matches
        
    def find_similar_experiences(self, reference_xpunit: EnhancedXPUnit, 
                                top_k: int = 10) -> List[Tuple[EnhancedXPUnit, float]]:
        """Find experiences similar to a reference XPUnit"""
        reference_vector = reference_xpunit.get_holographic_vector()
        
        similarities = []
        for xpunit in self.xpunits.values():
            if xpunit.content_id != reference_xpunit.content_id:
                similarity = cosine_similarity(reference_vector, xpunit.get_holographic_vector())
                similarities.append((xpunit, similarity))
                
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
        
    def get_consciousness_distribution(self) -> Dict[str, int]:
        """Get distribution of consciousness levels"""
        distribution = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for xpunit in self.xpunits.values():
            level = xpunit.get_consciousness_level()
            distribution[level] += 1
            
        return distribution
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get environment statistics"""
        consciousness_dist = self.get_consciousness_distribution()
        holographic_stats = self.holographic_memory.get_capacity_stats()
        
        return {
            'total_xpunits': len(self.xpunits),
            'total_ingested': self.total_ingested,
            'total_queries': self.total_queries,
            'consciousness_distribution': consciousness_dist,
            'average_consciousness': np.mean([xp.consciousness_score for xp in self.xpunits.values()]),
            'holographic_memory': holographic_stats,
            'dimension': self.dimension,
            'decay_rate': self.decay_rate
        }
        
    def consolidate_memories(self, similarity_threshold: float = 0.9):
        """
        Consolidate similar memories to reduce noise and improve capacity
        
        Args:
            similarity_threshold: Minimum similarity for consolidation
        """
        # Find highly similar XPUnits
        consolidation_groups = []
        processed = set()
        
        for xpunit_id, xpunit in self.xpunits.items():
            if xpunit_id in processed:
                continue
                
            similar_group = [xpunit]
            processed.add(xpunit_id)
            
            # Find similar XPUnits
            for other_id, other_xpunit in self.xpunits.items():
                if other_id in processed:
                    continue
                    
                similarity = xpunit.similarity_to(other_xpunit)
                if similarity >= similarity_threshold:
                    similar_group.append(other_xpunit)
                    processed.add(other_id)
                    
            if len(similar_group) > 1:
                consolidation_groups.append(similar_group)
                
        # Consolidate each group
        for group in consolidation_groups:
            self._consolidate_group(group)
            
    def _consolidate_group(self, group: List[EnhancedXPUnit]):
        """Consolidate a group of similar XPUnits"""
        # Create consolidated XPUnit with combined properties
        primary = group[0]  # Use first as primary
        
        # Combine consciousness scores (weighted average)
        total_importance = sum(xp.importance for xp in group)
        consolidated_consciousness = sum(
            xp.consciousness_score * xp.importance for xp in group
        ) / total_importance if total_importance > 0 else 0
        
        # Update primary XPUnit
        primary.consciousness_score = consolidated_consciousness
        primary.importance = total_importance / len(group)  # Average importance
        primary.reliability = min(xp.reliability for xp in group)  # Conservative reliability
        
        # Remove other XPUnits from group
        for xpunit in group[1:]:
            if xpunit.content_id in self.xpunits:
                del self.xpunits[xpunit.content_id]

# =============================================================================
# DEMO AND TESTING FUNCTIONS
# =============================================================================

def create_demo_environment() -> EnhancedXPEnvironment:
    """Create a demo environment with sample experiences"""
    env = EnhancedXPEnvironment(dimension=512)
    
    # Sample experiences with varying consciousness levels
    experiences = [
        "I am thinking about the nature of consciousness and self-awareness.",
        "The weather is nice today, perfect for a walk in the park.",
        "I wonder if my thoughts are truly my own or influenced by external factors.",
        "Machine learning algorithms can process vast amounts of data efficiently.",
        "When I reflect on my own thinking processes, I notice recursive patterns.",
        "The library has many books on artificial intelligence and cognitive science.",
        "I am aware that I am analyzing my own awareness right now.",
        "Python is a versatile programming language for data science applications."
    ]
    
    for experience in experiences:
        env.ingest_experience(experience)
        
    return env

def run_consciousness_analysis(env: EnhancedXPEnvironment) -> Dict[str, Any]:
    """Run consciousness analysis on environment"""
    results = {
        'consciousness_distribution': env.get_consciousness_distribution(),
        'high_consciousness_examples': [],
        'consciousness_scores': []
    }
    
    # Find high consciousness examples
    for xpunit in env.xpunits.values():
        results['consciousness_scores'].append(xpunit.consciousness_score)
        
        if xpunit.get_consciousness_level() == "HIGH":
            results['high_consciousness_examples'].append({
                'content': xpunit.content,
                'score': xpunit.consciousness_score,
                'indicators': xpunit.consciousness_indicators
            })
            
    return results

# =============================================================================
# EXPORT ALL CLASSES AND FUNCTIONS
# =============================================================================

__all__ = [
    'EnhancedXPUnit',
    'EnhancedXPEnvironment', 
    'create_demo_environment',
    'run_consciousness_analysis'
]
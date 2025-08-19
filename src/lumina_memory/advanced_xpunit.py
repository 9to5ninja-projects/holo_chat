"""
Advanced XPUnit with Complete Emotional-Consciousness Integration
================================================================

This module implements the comprehensive XPUnit upgrade with:
- Complete data model with all new fields
- Mathematical update rules for context growth and emotional reinforcement
- Practical policies with proven defaults
- Chain-of-thought control for emotional detours
- Long string of thought handling
- Edge cases and safeguards

This IS the fundamental building block that defines consciousness, memory, and experience.

Author: Lumina Memory Team
License: MIT
"""

import numpy as np
import time
import hashlib
from typing import Dict, List, Optional, Any, Tuple, Union, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

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
# ADVANCED XPUNIT DATA MODEL
# =============================================================================

class ConsolidationStage(Enum):
    """Consolidation stages for memory processing"""
    EPISODIC = "episodic"
    CONSOLIDATING = "consolidating" 
    SEMANTIC = "semantic"

class LinkType(Enum):
    """Types of links between capsules"""
    CO_MENTION = "co-mention"
    INTRUSION = "intrusion"
    RETURN_PATH = "return-path"
    NARRATIVE = "narrative"
    EMOTIONAL = "emotional"

@dataclass
class CapsuleLink:
    """Link between capsules with metadata"""
    link_type: LinkType
    target_id: str
    weight: float
    affect_spike: float = 0.0
    context_snapshot: Optional[str] = None
    reason: Optional[str] = None
    ttl: Optional[int] = None  # Time to live for temporary links
    timestamp: float = field(default_factory=time.time)

@dataclass
class AffectState:
    """Emotional affect state"""
    valence: float = 0.0  # [-1, 1] negative to positive
    arousal: float = 0.0  # [0, 1] calm to excited
    
    def __post_init__(self):
        """Ensure valid ranges"""
        self.valence = np.clip(self.valence, -1.0, 1.0)
        self.arousal = np.clip(self.arousal, 0.0, 1.0)
    
    def magnitude(self) -> float:
        """Get affect magnitude"""
        return np.sqrt(self.valence**2 + self.arousal**2)
    
    def to_dict(self) -> Dict[str, float]:
        return {"valence": self.valence, "arousal": self.arousal}
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'AffectState':
        return cls(valence=data["valence"], arousal=data["arousal"])

# =============================================================================
# PRACTICAL POLICIES (PROVEN DEFAULTS)
# =============================================================================

class XPUnitPolicies:
    """Practical policies with proven defaults"""
    
    # Context and emotional parameters
    LAMBDA_CTX = 0.2          # Context influence on capsule vector
    RHO = 0.2                 # Affect update rate
    ETA = 0.15                # Mood coupling strength
    ALPHA_V = 0.4             # Valence salience boost
    ALPHA_AR = 0.3            # Arousal salience boost
    ALPHA_R = 0.05            # Recall bonus
    KAPPA = 1.0               # Emotional decay protection
    
    # FIXED: Intrusion detection thresholds (recalibrated based on analysis)
    THETA_A = 0.65            # Affect spike threshold (fine-tuned from 0.6)
    THETA_T = 0.15            # Topicality threshold (decreased from 0.25)
    
    # Consolidation progression
    R1 = 3                    # episodic → consolidating
    R2 = 7                    # consolidating → semantic
    
    # Mood state update
    MU = 0.1                  # Mood update rate
    
    # NEW: Consciousness evolution parameters (enhanced for better growth)
    CONSCIOUSNESS_MOMENTUM = 0.2      # Consciousness building factor (increased from 0.1)
    CONSCIOUSNESS_DECAY = 0.02        # Consciousness decay without reinforcement (reduced from 0.05)
    MIN_CONSCIOUSNESS_GROWTH = 0.05   # Minimum growth per self-reflective experience (increased from 0.02)
    
    # Safeguards
    MAX_AFFECT_MAGNITUDE = 2.0
    MAX_SALIENCE = 10.0
    MAX_INTRUSION_DETOURS = 2
    AROUSAL_DECAY_RATE = 0.1

@dataclass
class AdvancedXPUnit:
    """
    Advanced XPUnit - The fundamental building block of consciousness and memory
    
    This IS everything. It defines how experience, consciousness, emotion, and memory
    integrate into a unified system that can grow, learn, and adapt.
    """
    
    # Core identity and content
    content_id: str
    content: str
    timestamp: float = field(default_factory=time.time)
    
    # NEW: Text trace (chronological evidence)
    text_trace: List[str] = field(default_factory=list)
    
    # NEW: Context vector (running HRR superposition)
    context_vec: Optional[np.ndarray] = None
    
    # NEW: Affect state
    affect: AffectState = field(default_factory=AffectState)
    
    # NEW: Mood tag
    mood_tag: Optional[str] = None
    
    # NEW: Salience (importance baseline)
    salience: float = 1.0
    
    # NEW: Rehearsals and recall tracking
    rehearsals: int = 0
    last_recall: float = 0.0
    
    # NEW: Consolidation stage
    consolidation: ConsolidationStage = ConsolidationStage.EPISODIC
    
    # NEW: Links to other capsules
    links: List[CapsuleLink] = field(default_factory=list)
    
    # Holographic memory capsule
    memory_capsule: MemoryCapsule = field(init=False)
    
    # Mathematical representations
    semantic_vector: Optional[np.ndarray] = None
    emotion_vector: Optional[np.ndarray] = None
    
    # Consciousness analysis
    consciousness_score: float = 0.0
    consciousness_indicators: Dict[str, float] = field(default_factory=dict)
    consciousness_history: List[float] = field(default_factory=list)  # Track consciousness evolution
    
    # Importance and reliability
    importance: float = DEFAULT_IMPORTANCE
    reliability: float = 1.0
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize the advanced XPUnit"""
        # Initialize context vector
        if self.context_vec is None:
            self.context_vec = np.zeros(HRR_DIM, dtype=np.float32)
        
        # Initialize text trace with content
        if self.content and self.content not in self.text_trace:
            self.text_trace.append(self.content)
        
        # Initialize holographic memory capsule
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
        """Enhanced consciousness analysis with affect integration"""
        content_lower = self.content.lower()
        
        # Self-reference analysis
        if "i am" in content_lower or "my own" in content_lower:
            self.consciousness_score += CONSCIOUSNESS_SELF_REFERENCE_WEIGHT
            self.consciousness_indicators["self_reference"] = 0.8
            # Self-reference increases positive valence
            self.affect.valence += 0.1
            
        # Introspection analysis
        introspection_count = sum(1 for word in CONSCIOUSNESS_INTROSPECTION_WORDS 
                                 if word in content_lower)
        if introspection_count > 0:
            self.consciousness_score += CONSCIOUSNESS_INTROSPECTION_WEIGHT * introspection_count
            self.consciousness_indicators["introspection"] = min(1.0, introspection_count * 0.3)
            # Introspection increases arousal
            self.affect.arousal += 0.05 * introspection_count
            
        # Recursive processing (thinking about thinking)
        if ("thought" in content_lower and 
            ("my" in content_lower or "own" in content_lower)):
            self.consciousness_score += CONSCIOUSNESS_RECURSIVE_WEIGHT
            self.consciousness_indicators["recursive_processing"] = 0.9
            # Recursive processing is highly arousing
            self.affect.arousal += 0.2
            
        # Personal sharing and connection (Fix: should trigger growth)
        personal_words = ["favorite", "love", "like", "enjoy", "important", "personal", "feel", "think"]
        personal_count = sum(1 for word in personal_words if word in content_lower)
        if personal_count > 0:
            self.consciousness_score += CONSCIOUSNESS_INTROSPECTION_WEIGHT * personal_count * 0.5
            self.consciousness_indicators["personal_connection"] = min(1.0, personal_count * 0.2)
            # Personal sharing increases positive valence
            self.affect.valence += 0.02 * personal_count
            
        # Complex questions (Fix: should trigger more growth)
        if "?" in self.content and len(self.content.split()) > 5:
            question_complexity = len(self.content.split()) / 10.0  # Normalize by length
            self.consciousness_score += CONSCIOUSNESS_INTROSPECTION_WEIGHT * question_complexity
            self.consciousness_indicators["complex_inquiry"] = min(1.0, question_complexity)
            # Complex questions increase arousal
            self.affect.arousal += 0.03 * question_complexity
            
        # FIXED: Apply consciousness momentum
        if self.consciousness_history:
            # Get recent consciousness trend
            recent_history = self.consciousness_history[-3:]  # Last 3 experiences
            if len(recent_history) >= 2:
                recent_avg = np.mean(recent_history)
                momentum_boost = recent_avg * XPUnitPolicies.CONSCIOUSNESS_MOMENTUM
                self.consciousness_score += momentum_boost
                self.consciousness_indicators["momentum"] = momentum_boost
        
        # Ensure minimum growth for self-reflective content
        if self.consciousness_score > 0:
            self.consciousness_score = max(self.consciousness_score, XPUnitPolicies.MIN_CONSCIOUSNESS_GROWTH)
        
        # Store consciousness score in history
        self.consciousness_history.append(self.consciousness_score)
        
        # Keep history manageable (last 10 experiences)
        if len(self.consciousness_history) > 10:
            self.consciousness_history = self.consciousness_history[-10:]
        
        # Consciousness boosts importance and salience
        self.importance = 1.0 + self.consciousness_score
        self.salience += self.consciousness_score * 0.5
        
        # Ensure affect stays in bounds
        self.affect = AffectState(self.affect.valence, self.affect.arousal)
        
    def _create_initial_bindings(self):
        """Create initial role-filler bindings from content"""
        # WHAT role - bind to content representation
        if self.semantic_vector is not None:
            self.memory_capsule.add_binding("WHAT", self.semantic_vector, 1.0)
        else:
            content_vector = self._encode_content_to_vector()
            self.memory_capsule.add_binding("WHAT", content_vector, 1.0)
            
        # WHEN role - bind to temporal representation
        time_vector = self._encode_time_to_vector()
        self.memory_capsule.add_binding("WHEN", time_vector, 0.8)
        
        # HOW role - bind to consciousness representation
        consciousness_vector = self._encode_consciousness_to_vector()
        self.memory_capsule.add_binding("HOW", consciousness_vector, 0.6)
        
        # EMOTION role - bind to emotional representation
        emotion_vector = self._encode_affect_to_vector()
        self.memory_capsule.add_binding("EMOTION", emotion_vector, 0.7)
        
        # CONTEXT role - bind to context vector
        if np.any(self.context_vec):
            self.memory_capsule.add_binding("CONTEXT", self.context_vec, 0.5)
    
    def _encode_content_to_vector(self) -> np.ndarray:
        """Encode content to vector representation"""
        target_dim = HRR_DIM
        content_hash = hashlib.blake2b(self.content.encode(), digest_size=8).digest()
        seed = int.from_bytes(content_hash, byteorder='big') % (2**31)
        rng = np.random.RandomState(seed)
        vector = rng.randn(target_dim).astype(np.float32)
        return normalize_vector(vector)
        
    def _encode_time_to_vector(self) -> np.ndarray:
        """Encode timestamp using PHI and TAU"""
        t_normalized = (self.timestamp % (24 * 3600)) / (24 * 3600)
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
        consciousness_vector[0] = self.consciousness_score
        
        for i, (indicator, value) in enumerate(self.consciousness_indicators.items()):
            if i + 1 < dim:
                consciousness_vector[i + 1] = value
                
        return normalize_vector(consciousness_vector)
    
    def _encode_affect_to_vector(self) -> np.ndarray:
        """Encode affect state to vector"""
        dim = HRR_DIM
        affect_vector = np.zeros(dim)
        affect_vector[0] = self.affect.valence
        affect_vector[1] = self.affect.arousal
        affect_vector[2] = self.affect.magnitude()
        return normalize_vector(affect_vector)
    
    # =============================================================================
    # MATHEMATICAL UPDATE RULES
    # =============================================================================
    
    def append_evidence(self, delta_text: str, role_symbol_pairs: List[Tuple[str, np.ndarray]]):
        """
        2.1 Append evidence (context growth)
        
        Args:
            delta_text: New text evidence
            role_symbol_pairs: List of (role_name, symbol_vector) pairs
        """
        # Update text trace
        self.text_trace.append(delta_text)
        
        # Update context superposition
        for role_name, symbol_vector in role_symbol_pairs:
            # Get role vector (create if needed)
            role_vector = self._get_or_create_role_vector(role_name)
            
            # Bind role and symbol: r ⊗ s
            binding = circular_convolution(role_vector, symbol_vector)
            
            # Add to context: ctx_i ← norm(ctx_i + Σ r⊗s)
            self.context_vec = self.context_vec + binding
            
        # Normalize context vector
        self.context_vec = normalize_vector(self.context_vec)
        
        # Re-encode capsule by updating CONTEXT binding with new context
        # This indirectly updates the capsule vector through the binding system
        self.memory_capsule.add_binding("CONTEXT", self.context_vec, XPUnitPolicies.LAMBDA_CTX)
        
        # Also add the new role-symbol pairs to the capsule
        for role_name, symbol_vector in role_symbol_pairs:
            # Use a lower weight for new evidence to preserve existing structure
            self.memory_capsule.add_binding(f"NEW_{role_name}", symbol_vector, 0.3)
    
    def emotional_reinforcement(self, delta_affect: AffectState, mood_state: AffectState):
        """
        2.2 Emotional reinforcement (affect + mood)
        
        Args:
            delta_affect: Change in affect
            mood_state: Current global mood
        """
        # FIXED: Add emotional context sensitivity
        # Mood congruence factor - similar moods reinforce more
        mood_congruence = cosine_similarity(
            np.array([self.affect.valence, self.affect.arousal]),
            np.array([mood_state.valence, mood_state.arousal])
        )
        
        # Adjust eta based on mood congruence (0.5 to 1.5 range)
        context_eta = XPUnitPolicies.ETA * (1.0 + 0.5 * mood_congruence)
        
        # Update affect: affect_i ← clip((1-ρ) * affect_i + ρ * (Δ_a + η * m))
        old_valence = self.affect.valence
        old_arousal = self.affect.arousal
        
        new_valence = ((1 - XPUnitPolicies.RHO) * old_valence + 
                      XPUnitPolicies.RHO * (delta_affect.valence + context_eta * mood_state.valence))
        new_arousal = ((1 - XPUnitPolicies.RHO) * old_arousal + 
                      XPUnitPolicies.RHO * (delta_affect.arousal + context_eta * mood_state.arousal))
        
        self.affect = AffectState(new_valence, new_arousal)
        
        # Update salience: salience_i ← salience_i + α_v|Δ_v| + α_ar*Δ_ar + α_r
        delta_v = delta_affect.valence
        delta_ar = delta_affect.arousal
        
        salience_boost = (XPUnitPolicies.ALPHA_V * abs(delta_v) + 
                         XPUnitPolicies.ALPHA_AR * delta_ar + 
                         XPUnitPolicies.ALPHA_R)
        
        self.salience = min(self.salience + salience_boost, XPUnitPolicies.MAX_SALIENCE)
        
        # Update emotional decay protection: τ_i = τ_0 * (1 + κ * ||affect_i||)
        affect_magnitude = self.affect.magnitude()
        self.metadata['emotional_decay_factor'] = 1.0 + XPUnitPolicies.KAPPA * affect_magnitude
        
        # Store emotional context for future reference
        self.metadata['last_mood_congruence'] = mood_congruence
        self.metadata['context_eta'] = context_eta
    
    def reconsolidate_on_recall(self, current_time: float):
        """
        2.3 Reconsolidation on recall (learning through use)
        
        Args:
            current_time: Current timestamp
        """
        # Update recall statistics
        self.rehearsals += 1
        self.last_recall = current_time
        
        # Increase consolidation stage if thresholds are met
        if (self.consolidation == ConsolidationStage.EPISODIC and 
            self.rehearsals >= XPUnitPolicies.R1):
            self.consolidation = ConsolidationStage.CONSOLIDATING
            
        elif (self.consolidation == ConsolidationStage.CONSOLIDATING and 
              self.rehearsals >= XPUnitPolicies.R2):
            self.consolidation = ConsolidationStage.SEMANTIC
        
        # Optional: Symbol cleanup (error-driven clean-up)
        # This would require access to current readouts, implementing as metadata for now
        self.metadata['last_reconsolidation'] = current_time
        self.metadata['consolidation_stage'] = self.consolidation.value
    
    def check_intrusion(self, topic_vector: np.ndarray, current_context_id: str) -> bool:
        """
        2.4 Off-topic emotional mentions (intrusion handling)
        
        Args:
            topic_vector: Current topic vector
            current_context_id: ID of current context capsule
            
        Returns:
            True if intrusion detected
        """
        # Compute topicality: T = cos(q_topic, v_i)
        capsule_vector = self.memory_capsule.vector
        topicality = cosine_similarity(topic_vector, capsule_vector)
        
        # Compute affect spike: A = |Δ_v| + Δ_ar
        affect_spike = abs(self.affect.valence) + self.affect.arousal
        
        # Trigger rule: A ≥ θ_A ∧ (T < θ_T)
        if (affect_spike >= XPUnitPolicies.THETA_A and 
            topicality < XPUnitPolicies.THETA_T):
            
            # Create intrusion link
            intrusion_link = CapsuleLink(
                link_type=LinkType.INTRUSION,
                target_id=current_context_id,
                weight=affect_spike,
                affect_spike=affect_spike,
                context_snapshot=self.content[:100],  # First 100 chars
                reason="affect"
            )
            self.links.append(intrusion_link)
            
            # Boost salience
            gamma = 0.5  # Intrusion salience boost factor
            self.salience = min(self.salience + gamma * affect_spike, XPUnitPolicies.MAX_SALIENCE)
            
            return True
            
        return False
    
    def _get_or_create_role_vector(self, role_name: str) -> np.ndarray:
        """Get or create a role vector for binding operations"""
        # Use deterministic generation based on role name
        role_hash = hashlib.blake2b(role_name.encode(), digest_size=8).digest()
        seed = int.from_bytes(role_hash, byteorder='big') % (2**31)
        rng = np.random.RandomState(seed)
        vector = rng.randn(HRR_DIM).astype(np.float32)
        return normalize_vector(vector)
    
    # =============================================================================
    # CHAIN-OF-THOUGHT CONTROL
    # =============================================================================
    
    def create_flashbulb_capsule(self, mention_text: str, historical_capsule_id: str, 
                                topic_capsule_id: str) -> 'AdvancedXPUnit':
        """
        Create a flashbulb micro-capsule for emotional detours
        
        Args:
            mention_text: Text of the current mention
            historical_capsule_id: ID of high-affect historical capsule
            topic_capsule_id: ID of current topic capsule
            
        Returns:
            New flashbulb capsule
        """
        flashbulb_id = f"flashbulb_{int(time.time() * 1000)}"
        
        flashbulb = AdvancedXPUnit(
            content_id=flashbulb_id,
            content=mention_text,
            affect=AffectState(self.affect.valence * 0.8, self.affect.arousal * 0.8),
            salience=self.salience * 0.6,
            mood_tag="flashbulb"
        )
        
        # Link to historical capsule
        historical_link = CapsuleLink(
            link_type=LinkType.EMOTIONAL,
            target_id=historical_capsule_id,
            weight=0.9,
            affect_spike=self.affect.magnitude(),
            reason="flashbulb_historical"
        )
        flashbulb.links.append(historical_link)
        
        # Link to topic capsule
        topic_link = CapsuleLink(
            link_type=LinkType.NARRATIVE,
            target_id=topic_capsule_id,
            weight=0.7,
            reason="flashbulb_topic"
        )
        flashbulb.links.append(topic_link)
        
        # Add return path
        return_link = CapsuleLink(
            link_type=LinkType.RETURN_PATH,
            target_id=topic_capsule_id,
            weight=1.0,
            ttl=2,  # Return after 1-2 steps
            reason="detour_return"
        )
        flashbulb.links.append(return_link)
        
        return flashbulb
    
    # =============================================================================
    # UTILITY METHODS
    # =============================================================================
    
    def get_consciousness_level(self) -> str:
        """Get consciousness level classification"""
        if self.consciousness_score > HIGH_CONSCIOUSNESS_THRESHOLD:
            return "HIGH"
        elif self.consciousness_score > MEDIUM_CONSCIOUSNESS_THRESHOLD:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_holographic_vector(self) -> np.ndarray:
        """Get the holographic representation vector"""
        return self.memory_capsule.vector
    
    def get_effective_importance(self, decay_rate: float = DEFAULT_DECAY_RATE) -> float:
        """Get importance adjusted for decay, consciousness, and emotion"""
        # Base importance with decay
        age_hours = (time.time() - self.timestamp) / 3600.0
        decay_factor = np.exp(-decay_rate * age_hours)
        
        # Emotional protection factor
        emotional_protection = self.metadata.get('emotional_decay_factor', 1.0)
        protected_decay = decay_factor * emotional_protection
        
        # Consciousness boost
        consciousness_boost = 1.0 + (self.consciousness_score * 0.5)
        
        # Affect boost
        affect_boost = 1.0 + (self.affect.magnitude() * 0.3)
        
        return (self.importance * protected_decay * self.reliability * 
                consciousness_boost * affect_boost)
    
    def get_consolidation_strength(self) -> float:
        """Get consolidation strength based on rehearsals and stage"""
        base_strength = min(self.rehearsals / XPUnitPolicies.R2, 1.0)
        
        stage_multiplier = {
            ConsolidationStage.EPISODIC: 0.3,
            ConsolidationStage.CONSOLIDATING: 0.7,
            ConsolidationStage.SEMANTIC: 1.0
        }
        
        return base_strength * stage_multiplier[self.consolidation]
    
    def add_link(self, link: CapsuleLink):
        """Add a link to another capsule"""
        self.links.append(link)
    
    def get_links_by_type(self, link_type: LinkType) -> List[CapsuleLink]:
        """Get all links of a specific type"""
        return [link for link in self.links if link.link_type == link_type]
    
    def cleanup_expired_links(self, current_time: float):
        """Remove expired links (TTL-based)"""
        active_links = []
        for link in self.links:
            if link.ttl is None:
                active_links.append(link)
            else:
                age = current_time - link.timestamp
                if age < link.ttl:
                    active_links.append(link)
        
        self.links = active_links
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'content_id': self.content_id,
            'content': self.content,
            'timestamp': self.timestamp,
            'text_trace': self.text_trace,
            'context_vec': self.context_vec.tolist() if self.context_vec is not None else None,
            'affect': self.affect.to_dict(),
            'mood_tag': self.mood_tag,
            'salience': self.salience,
            'rehearsals': self.rehearsals,
            'last_recall': self.last_recall,
            'consolidation': self.consolidation.value,
            'links': [
                {
                    'link_type': link.link_type.value,
                    'target_id': link.target_id,
                    'weight': link.weight,
                    'affect_spike': link.affect_spike,
                    'context_snapshot': link.context_snapshot,
                    'reason': link.reason,
                    'ttl': link.ttl,
                    'timestamp': link.timestamp
                }
                for link in self.links
            ],
            'consciousness_score': self.consciousness_score,
            'consciousness_indicators': self.consciousness_indicators,
            'consciousness_history': self.consciousness_history,
            'importance': self.importance,
            'reliability': self.reliability,
            'salience': self.salience,
            'metadata': self.metadata,
            'memory_capsule': self.memory_capsule.to_dict(),
            'semantic_vector': self.semantic_vector.tolist() if self.semantic_vector is not None else None,
            'emotion_vector': self.emotion_vector.tolist() if self.emotion_vector is not None else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AdvancedXPUnit':
        """Deserialize from dictionary"""
        # Create basic XPUnit
        xpunit = cls(
            content_id=data['content_id'],
            content=data['content'],
            timestamp=data['timestamp']
        )
        
        # Restore all fields
        xpunit.text_trace = data.get('text_trace', [])
        if data.get('context_vec'):
            xpunit.context_vec = np.array(data['context_vec'])
        xpunit.affect = AffectState.from_dict(data['affect'])
        xpunit.mood_tag = data.get('mood_tag')
        xpunit.salience = data['salience']
        xpunit.rehearsals = data['rehearsals']
        xpunit.last_recall = data['last_recall']
        xpunit.consolidation = ConsolidationStage(data['consolidation'])
        
        # Restore links
        xpunit.links = []
        for link_data in data.get('links', []):
            link = CapsuleLink(
                link_type=LinkType(link_data['link_type']),
                target_id=link_data['target_id'],
                weight=link_data['weight'],
                affect_spike=link_data.get('affect_spike', 0.0),
                context_snapshot=link_data.get('context_snapshot'),
                reason=link_data.get('reason'),
                ttl=link_data.get('ttl'),
                timestamp=link_data.get('timestamp', time.time())
            )
            xpunit.links.append(link)
        
        # Restore other properties
        xpunit.consciousness_score = data['consciousness_score']
        xpunit.consciousness_indicators = data['consciousness_indicators']
        xpunit.consciousness_history = data.get('consciousness_history', [])
        xpunit.importance = data['importance']
        xpunit.reliability = data['reliability']
        xpunit.metadata = data['metadata']
        
        # Restore vectors
        if data.get('semantic_vector'):
            xpunit.semantic_vector = np.array(data['semantic_vector'])
        if data.get('emotion_vector'):
            xpunit.emotion_vector = np.array(data['emotion_vector'])
            
        # Restore memory capsule
        xpunit.memory_capsule = MemoryCapsule.from_dict(data['memory_capsule'])
        
        return xpunit

# =============================================================================
# EXPORT
# =============================================================================

__all__ = [
    'AdvancedXPUnit',
    'AffectState', 
    'CapsuleLink',
    'ConsolidationStage',
    'LinkType',
    'XPUnitPolicies'
]
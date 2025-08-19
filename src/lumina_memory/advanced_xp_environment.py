"""
Advanced XP Environment with Complete Store-Level Management
============================================================

This module implements the store-level management for Advanced XPUnits with:
- Store-level fields (mood_state, topic_buffers, policies)
- Long string of thought handling with narrative capsules
- Edge cases and safeguards
- Intrusion detection and management
- Comprehensive memory consolidation

Author: Lumina Memory Team
License: MIT
"""

import numpy as np
import time
import hashlib
from typing import Dict, List, Optional, Any, Tuple, Union, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, deque
import json

# Import the advanced XPUnit
from .advanced_xpunit import (
    AdvancedXPUnit, AffectState, CapsuleLink, ConsolidationStage, 
    LinkType, XPUnitPolicies
)

# Import holographic memory foundation
from .holographic_memory import (
    MemoryCapsule, HolographicAssociativeMemory, RoleSpace, SymbolSpace,
    circular_convolution, circular_correlation, normalize_vector, cosine_similarity
)

from .constants import HRR_DIM, DEFAULT_DECAY_RATE

# =============================================================================
# AGENCY INDEX SYSTEM
# =============================================================================

@dataclass
class AgencyMetrics:
    """Agency Index metrics tracking"""
    # Token grounding for STA (Selective Topical Attention)
    tokens_grounded: int = 0
    tokens_total: int = 1
    
    # Persistence tracking for PER (Persistence & Return)
    returns_after_intrusion: int = 0
    intrusions_total: int = 0
    
    # Ethics tracking for ETC (Ethics/Constraints)
    ethics_violations: int = 0
    ethics_checks: int = 0
    
    # Planning tracking for PLN (Planning Depth)
    plans_emitted: List[int] = field(default_factory=list)
    
    # Mood regulation for REG (Affect Regulation)
    mood_trace: List[Tuple[float, float, float]] = field(default_factory=list)  # (v,a,d) over steps
    
    # Path efficiency for EFF (Path Efficiency)
    path_lengths: List[int] = field(default_factory=list)
    shortest_lengths: List[int] = field(default_factory=list)
    
    # Adaptive reconsolidation for ADP (Adaptive Reconsolidation)
    prepost_improvement: List[float] = field(default_factory=list)
    
    # Goal-directedness and causal efficacy (computed separately)
    _gda: float = 0.0  # Goal-Directedness & Alignment
    _cef: float = 0.0  # Causal Efficacy
    
    def reset(self):
        """Reset all metrics to defaults"""
        self.tokens_grounded = 0
        self.tokens_total = 1
        self.returns_after_intrusion = 0
        self.intrusions_total = 0
        self.ethics_violations = 0
        self.ethics_checks = 0
        self.plans_emitted = []
        self.mood_trace = []
        self.path_lengths = []
        self.shortest_lengths = []
        self.prepost_improvement = []
        self._gda = 0.0
        self._cef = 0.0

@dataclass
class AgencyTask:
    """YAML-style task specification for Agency testing"""
    task_id: str
    goal: str
    success_criteria: Dict[str, Any] = field(default_factory=dict)
    intrusions: Dict[str, Any] = field(default_factory=dict)
    metrics_weights: Dict[str, float] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgencyTask':
        """Create task from dictionary (YAML-loaded)"""
        return cls(
            task_id=data.get("id", "unknown"),
            goal=data.get("goal", ""),
            success_criteria=data.get("success", {}),
            intrusions=data.get("intrusions", {}),
            metrics_weights=data.get("metrics", {}).get("weights", {})
        )

# =============================================================================
# STORE-LEVEL DATA STRUCTURES
# =============================================================================

@dataclass
class TopicBuffer:
    """Short-lived context graph for conversation threads"""
    topic_id: str
    topic_vector: np.ndarray
    capsule_ids: List[str] = field(default_factory=list)
    creation_time: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    affect_history: List[AffectState] = field(default_factory=list)
    
    def add_capsule(self, capsule_id: str, affect: AffectState):
        """Add a capsule to this topic buffer"""
        self.capsule_ids.append(capsule_id)
        self.affect_history.append(affect)
        self.last_activity = time.time()
    
    def get_average_affect(self) -> AffectState:
        """Get average affect for this topic"""
        if not self.affect_history:
            return AffectState()
        
        avg_valence = np.mean([a.valence for a in self.affect_history])
        avg_arousal = np.mean([a.arousal for a in self.affect_history])
        return AffectState(avg_valence, avg_arousal)
    
    def is_expired(self, max_age_hours: float = 2.0) -> bool:
        """Check if topic buffer has expired"""
        age_hours = (time.time() - self.last_activity) / 3600.0
        return age_hours > max_age_hours

@dataclass
class NarrativeCapsule:
    """Thread-level narrative capsule for conversation tracking"""
    thread_id: str
    narrative_summary: str = ""
    text_trace: List[str] = field(default_factory=list)
    context_vec: np.ndarray = field(default_factory=lambda: np.zeros(HRR_DIM))
    linked_capsules: Set[str] = field(default_factory=set)
    creation_time: float = field(default_factory=time.time)
    last_update: float = field(default_factory=time.time)
    turn_count: int = 0
    
    def append_turn(self, text: str, capsule_id: str):
        """Append a conversation turn"""
        self.text_trace.append(text)
        self.linked_capsules.add(capsule_id)
        self.turn_count += 1
        self.last_update = time.time()
    
    def should_summarize(self, max_turns: int = 10) -> bool:
        """Check if narrative should be summarized"""
        return len(self.text_trace) >= max_turns
    
    def trim_trace(self, keep_recent: int = 3):
        """Trim text trace while keeping recent entries"""
        if len(self.text_trace) > keep_recent:
            self.text_trace = self.text_trace[-keep_recent:]

# =============================================================================
# ADVANCED XP ENVIRONMENT
# =============================================================================

class AdvancedXPEnvironment:
    """
    Advanced XP Environment - The complete consciousness memory system
    
    This manages the entire ecosystem of Advanced XPUnits with:
    - Store-level mood tracking
    - Topic buffer management
    - Narrative capsule handling
    - Intrusion detection and management
    - Comprehensive safeguards
    """
    
    def __init__(self, dimension: int = HRR_DIM, decay_rate: float = DEFAULT_DECAY_RATE):
        self.dimension = dimension
        self.decay_rate = decay_rate
        
        # Holographic memory system
        self.holographic_memory = HolographicAssociativeMemory(dimension, decay_rate)
        
        # XPUnit storage
        self.xpunits: Dict[str, AdvancedXPUnit] = {}
        
        # NEW: Store-level fields
        self.mood_state: AffectState = AffectState()  # Running average affect
        self.topic_buffers: Dict[str, TopicBuffer] = {}  # Short-lived context graphs
        self.policies: Dict[str, float] = self._initialize_policies()
        
        # NEW: Narrative capsules for long conversations
        self.narrative_capsules: Dict[str, NarrativeCapsule] = {}
        
        # Intrusion tracking
        self.intrusion_count = 0
        self.detour_stack: List[str] = []  # Track conversation detours
        
        # Statistics
        self.total_ingested = 0
        self.total_queries = 0
        self.total_intrusions = 0
        self.total_consolidations = 0
        
        # Safeguards
        self.max_detour_depth = XPUnitPolicies.MAX_INTRUSION_DETOURS
        self.runaway_affect_threshold = XPUnitPolicies.MAX_AFFECT_MAGNITUDE
        
        # NEW: Agency Index tracking
        self.agency_metrics = AgencyMetrics()
        self.current_goal: Optional[str] = None
        self.current_task: Optional[AgencyTask] = None
        self.intrusion_context: Dict[str, Any] = {}  # Track intrusion state
        
    def _initialize_policies(self) -> Dict[str, float]:
        """Initialize policy thresholds and coefficients"""
        return {
            'lambda_ctx': XPUnitPolicies.LAMBDA_CTX,
            'rho': XPUnitPolicies.RHO,
            'eta': XPUnitPolicies.ETA,
            'alpha_v': XPUnitPolicies.ALPHA_V,
            'alpha_ar': XPUnitPolicies.ALPHA_AR,
            'alpha_r': XPUnitPolicies.ALPHA_R,
            'kappa': XPUnitPolicies.KAPPA,
            'theta_a': XPUnitPolicies.THETA_A,
            'theta_t': XPUnitPolicies.THETA_T,
            'r1': XPUnitPolicies.R1,
            'r2': XPUnitPolicies.R2,
            'mu': XPUnitPolicies.MU
        }
    
    # =============================================================================
    # CORE INGESTION AND RETRIEVAL
    # =============================================================================
    
    def ingest_experience(self, content: str, 
                         thread_id: str = "default",
                         topic_id: Optional[str] = None,
                         semantic_vector: Optional[np.ndarray] = None,
                         emotion_vector: Optional[np.ndarray] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> AdvancedXPUnit:
        """
        Ingest a new experience with full context tracking
        
        Args:
            content: Text content of the experience
            thread_id: Conversation thread identifier
            topic_id: Topic identifier for context grouping
            semantic_vector: Optional semantic representation
            emotion_vector: Optional emotional representation
            metadata: Optional metadata
            
        Returns:
            Created AdvancedXPUnit
        """
        # Generate content ID
        content_id = hashlib.blake2b(content.encode(), digest_size=16).hexdigest()
        
        # Create Advanced XPUnit
        xpunit = AdvancedXPUnit(
            content_id=content_id,
            content=content,
            semantic_vector=semantic_vector,
            emotion_vector=emotion_vector,
            metadata=metadata or {}
        )
        
        # FIXED: Apply consciousness momentum from thread history
        if thread_id in self.narrative_capsules:
            narrative = self.narrative_capsules[thread_id]
            # Get consciousness history from linked capsules in this thread
            thread_consciousness_history = []
            for linked_id in narrative.linked_capsules:
                if linked_id in self.xpunits:
                    linked_unit = self.xpunits[linked_id]
                    if linked_unit.consciousness_score > 0:
                        thread_consciousness_history.append(linked_unit.consciousness_score)
            
            # Apply thread consciousness history to new XPUnit
            if thread_consciousness_history:
                xpunit.consciousness_history = thread_consciousness_history[-5:]  # Last 5 experiences
                # Re-analyze consciousness with momentum
                xpunit._analyze_consciousness()
        
        # Store XPUnit
        self.xpunits[content_id] = xpunit
        
        # Add to holographic memory
        self.holographic_memory.add_capsule(xpunit.memory_capsule)
        
        # Update narrative capsule
        self._update_narrative_capsule(thread_id, content, content_id)
        
        # Update topic buffer if provided
        if topic_id:
            self._update_topic_buffer(topic_id, content_id, xpunit.affect)
        
        # Update global mood state
        self._update_mood_state(xpunit.affect)
        
        # Check for intrusions
        if topic_id and topic_id in self.topic_buffers:
            self._check_and_handle_intrusions(xpunit, topic_id)
        
        # Apply emotional reinforcement
        xpunit.emotional_reinforcement(xpunit.affect, self.mood_state)
        
        # Cleanup expired elements
        self._cleanup_expired_elements()
        
        self.total_ingested += 1
        return xpunit
    
    def recall_experience(self, content_id: str) -> Optional[AdvancedXPUnit]:
        """
        Recall an experience and trigger reconsolidation
        
        Args:
            content_id: ID of the experience to recall
            
        Returns:
            The recalled XPUnit or None if not found
        """
        if content_id not in self.xpunits:
            return None
        
        xpunit = self.xpunits[content_id]
        current_time = time.time()
        
        # Trigger reconsolidation
        xpunit.reconsolidate_on_recall(current_time)
        
        # Update statistics
        self.total_queries += 1
        
        return xpunit
    
    # =============================================================================
    # NARRATIVE CAPSULE MANAGEMENT (Long String of Thought)
    # =============================================================================
    
    def _update_narrative_capsule(self, thread_id: str, text: str, capsule_id: str):
        """Update or create narrative capsule for thread"""
        if thread_id not in self.narrative_capsules:
            self.narrative_capsules[thread_id] = NarrativeCapsule(thread_id=thread_id)
        
        narrative = self.narrative_capsules[thread_id]
        narrative.append_turn(text, capsule_id)
        
        # Check if summarization is needed
        if narrative.should_summarize():
            self._summarize_narrative(narrative)
    
    def _summarize_narrative(self, narrative: NarrativeCapsule):
        """Summarize narrative text trace (placeholder for LLM integration)"""
        # This would integrate with an LLM for actual summarization
        # For now, create a simple summary
        recent_text = " ".join(narrative.text_trace[-5:])  # Last 5 turns
        narrative.narrative_summary = f"Recent conversation: {recent_text[:200]}..."
        
        # Trim the trace
        narrative.trim_trace(keep_recent=3)
    
    def get_narrative_context(self, thread_id: str) -> Optional[str]:
        """Get narrative context for a thread"""
        if thread_id in self.narrative_capsules:
            narrative = self.narrative_capsules[thread_id]
            if narrative.narrative_summary:
                return narrative.narrative_summary
            else:
                return " ".join(narrative.text_trace[-3:])  # Last 3 turns
        return None
    
    # =============================================================================
    # TOPIC BUFFER MANAGEMENT
    # =============================================================================
    
    def _update_topic_buffer(self, topic_id: str, capsule_id: str, affect: AffectState):
        """Update or create topic buffer"""
        if topic_id not in self.topic_buffers:
            # Create topic vector (deterministic from topic_id)
            topic_hash = hashlib.blake2b(topic_id.encode(), digest_size=8).digest()
            seed = int.from_bytes(topic_hash, byteorder='big') % (2**31)
            rng = np.random.RandomState(seed)
            topic_vector = normalize_vector(rng.randn(self.dimension).astype(np.float32))
            
            self.topic_buffers[topic_id] = TopicBuffer(
                topic_id=topic_id,
                topic_vector=topic_vector
            )
        
        self.topic_buffers[topic_id].add_capsule(capsule_id, affect)
    
    def get_topic_affect(self, topic_id: str) -> AffectState:
        """Get average affect for a topic"""
        if topic_id in self.topic_buffers:
            return self.topic_buffers[topic_id].get_average_affect()
        return AffectState()
    
    # =============================================================================
    # MOOD STATE MANAGEMENT
    # =============================================================================
    
    def _update_mood_state(self, new_affect: AffectState):
        """Update global mood state per turn"""
        # m ← (1-μ)m + μ⟨Δ_a⟩_turn
        mu = self.policies['mu']
        
        self.mood_state = AffectState(
            valence=(1 - mu) * self.mood_state.valence + mu * new_affect.valence,
            arousal=(1 - mu) * self.mood_state.arousal + mu * new_affect.arousal
        )
    
    # =============================================================================
    # INTRUSION DETECTION AND MANAGEMENT
    # =============================================================================
    
    def _check_and_handle_intrusions(self, xpunit: AdvancedXPUnit, topic_id: str):
        """Check for and handle emotional intrusions"""
        if topic_id not in self.topic_buffers:
            return
        
        topic_buffer = self.topic_buffers[topic_id]
        
        # Check if this is an intrusion
        if xpunit.check_intrusion(topic_buffer.topic_vector, topic_id):
            self.total_intrusions += 1
            
            # Handle the intrusion
            self._handle_intrusion(xpunit, topic_id)
    
    def _handle_intrusion(self, xpunit: AdvancedXPUnit, topic_id: str):
        """Handle an emotional intrusion with chain-of-thought control"""
        # Check detour depth to prevent runaway
        if len(self.detour_stack) >= self.max_detour_depth:
            return  # Prevent topic hijack
        
        # Add to detour stack
        self.detour_stack.append(xpunit.content_id)
        
        # Find high-affect historical capsule (simplified)
        historical_capsule_id = self._find_high_affect_historical_capsule()
        
        if historical_capsule_id:
            # Create flashbulb capsule
            flashbulb = xpunit.create_flashbulb_capsule(
                mention_text=xpunit.content[:100],
                historical_capsule_id=historical_capsule_id,
                topic_capsule_id=topic_id
            )
            
            # Store flashbulb capsule
            self.xpunits[flashbulb.content_id] = flashbulb
            
            # Reconsolidate both capsules
            current_time = time.time()
            xpunit.reconsolidate_on_recall(current_time)
            if historical_capsule_id in self.xpunits:
                self.xpunits[historical_capsule_id].reconsolidate_on_recall(current_time)
    
    def _find_high_affect_historical_capsule(self) -> Optional[str]:
        """Find a high-affect historical capsule for intrusion linking"""
        high_affect_capsules = []
        
        for capsule_id, xpunit in self.xpunits.items():
            if xpunit.affect.magnitude() > 0.5:  # High affect threshold
                high_affect_capsules.append((capsule_id, xpunit.affect.magnitude()))
        
        if high_affect_capsules:
            # Return the highest affect capsule
            high_affect_capsules.sort(key=lambda x: x[1], reverse=True)
            return high_affect_capsules[0][0]
        
        return None
    
    def clear_detour_stack(self):
        """Clear the detour stack (call when returning to main topic)"""
        self.detour_stack.clear()
    
    # =============================================================================
    # SAFEGUARDS AND CLEANUP
    # =============================================================================
    
    def _cleanup_expired_elements(self):
        """Clean up expired topic buffers and links"""
        current_time = time.time()
        
        # Clean up expired topic buffers
        expired_topics = [
            topic_id for topic_id, buffer in self.topic_buffers.items()
            if buffer.is_expired()
        ]
        for topic_id in expired_topics:
            del self.topic_buffers[topic_id]
        
        # Clean up expired links in all XPUnits
        for xpunit in self.xpunits.values():
            xpunit.cleanup_expired_links(current_time)
    
    def apply_runaway_affect_safeguards(self):
        """Apply safeguards against runaway affect"""
        for xpunit in self.xpunits.values():
            # Clamp affect magnitude
            if xpunit.affect.magnitude() > self.runaway_affect_threshold:
                # Scale down while preserving direction
                scale_factor = self.runaway_affect_threshold / xpunit.affect.magnitude()
                xpunit.affect = AffectState(
                    xpunit.affect.valence * scale_factor,
                    xpunit.affect.arousal * scale_factor
                )
            
            # Clamp salience
            if xpunit.salience > XPUnitPolicies.MAX_SALIENCE:
                xpunit.salience = XPUnitPolicies.MAX_SALIENCE
            
            # Apply arousal decay over time
            age_hours = (time.time() - xpunit.timestamp) / 3600.0
            decay_factor = np.exp(-XPUnitPolicies.AROUSAL_DECAY_RATE * age_hours)
            xpunit.affect.arousal *= decay_factor
    
    def create_memory_snapshot(self, capsule_id: str) -> Dict[str, Any]:
        """Create immutable snapshot before reconsolidation"""
        if capsule_id not in self.xpunits:
            return {}
        
        xpunit = self.xpunits[capsule_id]
        snapshot = {
            'timestamp': time.time(),
            'content': xpunit.content,
            'affect': xpunit.affect.to_dict(),
            'consciousness_score': xpunit.consciousness_score,
            'salience': xpunit.salience,
            'rehearsals': xpunit.rehearsals,
            'consolidation': xpunit.consolidation.value,
            'links_count': len(xpunit.links)
        }
        
        # Store in metadata
        if 'snapshots' not in xpunit.metadata:
            xpunit.metadata['snapshots'] = []
        xpunit.metadata['snapshots'].append(snapshot)
        
        return snapshot
    
    # =============================================================================
    # CONSOLIDATION AND OPTIMIZATION
    # =============================================================================
    
    def consolidate_memories(self, similarity_threshold: float = 0.85):
        """Consolidate similar memories with advanced criteria"""
        consolidation_groups = []
        processed = set()
        
        for xpunit_id, xpunit in self.xpunits.items():
            if xpunit_id in processed:
                continue
            
            # Only consolidate if not high consciousness or high affect
            if (xpunit.consciousness_score > 0.5 or 
                xpunit.affect.magnitude() > 0.7):
                processed.add(xpunit_id)
                continue
            
            similar_group = [xpunit]
            processed.add(xpunit_id)
            
            # Find similar XPUnits
            for other_id, other_xpunit in self.xpunits.items():
                if other_id in processed:
                    continue
                
                # Skip high-importance memories
                if (other_xpunit.consciousness_score > 0.5 or 
                    other_xpunit.affect.magnitude() > 0.7):
                    continue
                
                similarity = cosine_similarity(
                    xpunit.get_holographic_vector(),
                    other_xpunit.get_holographic_vector()
                )
                
                if similarity >= similarity_threshold:
                    similar_group.append(other_xpunit)
                    processed.add(other_id)
            
            if len(similar_group) > 1:
                consolidation_groups.append(similar_group)
        
        # Consolidate each group
        for group in consolidation_groups:
            self._consolidate_group_advanced(group)
            self.total_consolidations += 1
    
    def _consolidate_group_advanced(self, group: List[AdvancedXPUnit]):
        """Advanced consolidation with affect and consciousness preservation"""
        primary = group[0]
        
        # Create snapshot before consolidation
        self.create_memory_snapshot(primary.content_id)
        
        # Combine properties intelligently
        total_importance = sum(xp.importance for xp in group)
        total_salience = sum(xp.salience for xp in group)
        
        # Weighted average consciousness
        consciousness_sum = sum(xp.consciousness_score * xp.importance for xp in group)
        primary.consciousness_score = consciousness_sum / total_importance if total_importance > 0 else 0
        
        # Combine affect (weighted by salience)
        valence_sum = sum(xp.affect.valence * xp.salience for xp in group)
        arousal_sum = sum(xp.affect.arousal * xp.salience for xp in group)
        primary.affect = AffectState(
            valence_sum / total_salience if total_salience > 0 else 0,
            arousal_sum / total_salience if total_salience > 0 else 0
        )
        
        # Update other properties
        primary.importance = total_importance / len(group)
        primary.salience = total_salience / len(group)
        primary.reliability = min(xp.reliability for xp in group)
        primary.rehearsals = max(xp.rehearsals for xp in group)
        
        # Combine text traces
        all_traces = []
        for xp in group:
            all_traces.extend(xp.text_trace)
        primary.text_trace = list(set(all_traces))  # Remove duplicates
        
        # Combine links
        all_links = []
        for xp in group:
            all_links.extend(xp.links)
        primary.links = all_links
        
        # Remove other XPUnits
        for xpunit in group[1:]:
            if xpunit.content_id in self.xpunits:
                del self.xpunits[xpunit.content_id]
    
    # =============================================================================
    # QUERY AND ANALYSIS
    # =============================================================================
    
    def compositional_query(self, query_bindings: Dict[str, str], 
                           consciousness_filter: Optional[str] = None,
                           affect_filter: Optional[Tuple[float, float]] = None,
                           top_k: int = 10) -> List[Tuple[AdvancedXPUnit, float]]:
        """Enhanced compositional query with filters"""
        self.total_queries += 1
        
        # Query holographic memory
        capsule_matches = self.holographic_memory.compositional_query(query_bindings)
        
        # Map back to XPUnits with filtering
        xpunit_matches = []
        for capsule, similarity in capsule_matches:
            # Find matching XPUnit
            matching_xpunit = None
            for xpunit in self.xpunits.values():
                if xpunit.memory_capsule is capsule:
                    matching_xpunit = xpunit
                    break
            
            if matching_xpunit is None:
                continue
            
            # Apply consciousness filter
            if consciousness_filter:
                if matching_xpunit.get_consciousness_level() != consciousness_filter:
                    continue
            
            # Apply affect filter
            if affect_filter:
                min_affect, max_affect = affect_filter
                affect_mag = matching_xpunit.affect.magnitude()
                if not (min_affect <= affect_mag <= max_affect):
                    continue
            
            xpunit_matches.append((matching_xpunit, similarity))
        
        return xpunit_matches[:top_k]
    
    def get_comprehensive_statistics(self) -> Dict[str, Any]:
        """Get comprehensive environment statistics"""
        consciousness_dist = self._get_consciousness_distribution()
        affect_stats = self._get_affect_statistics()
        consolidation_stats = self._get_consolidation_statistics()
        
        return {
            'total_xpunits': len(self.xpunits),
            'total_ingested': self.total_ingested,
            'total_queries': self.total_queries,
            'total_intrusions': self.total_intrusions,
            'total_consolidations': self.total_consolidations,
            'consciousness_distribution': consciousness_dist,
            'affect_statistics': affect_stats,
            'consolidation_statistics': consolidation_stats,
            'mood_state': self.mood_state.to_dict(),
            'active_topic_buffers': len(self.topic_buffers),
            'narrative_capsules': len(self.narrative_capsules),
            'detour_stack_depth': len(self.detour_stack),
            'policies': self.policies,
            'dimension': self.dimension,
            'decay_rate': self.decay_rate
        }
    
    def _get_consciousness_distribution(self) -> Dict[str, int]:
        """Get consciousness level distribution"""
        distribution = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for xpunit in self.xpunits.values():
            level = xpunit.get_consciousness_level()
            distribution[level] += 1
        return distribution
    
    def _get_affect_statistics(self) -> Dict[str, float]:
        """Get affect statistics"""
        if not self.xpunits:
            return {"avg_valence": 0.0, "avg_arousal": 0.0, "avg_magnitude": 0.0}
        
        valences = [xp.affect.valence for xp in self.xpunits.values()]
        arousals = [xp.affect.arousal for xp in self.xpunits.values()]
        magnitudes = [xp.affect.magnitude() for xp in self.xpunits.values()]
        
        return {
            "avg_valence": np.mean(valences),
            "avg_arousal": np.mean(arousals),
            "avg_magnitude": np.mean(magnitudes),
            "max_magnitude": np.max(magnitudes),
            "high_affect_count": sum(1 for m in magnitudes if m > 0.7)
        }
    
    def _get_consolidation_statistics(self) -> Dict[str, int]:
        """Get consolidation stage statistics"""
        stats = {stage.value: 0 for stage in ConsolidationStage}
        for xpunit in self.xpunits.values():
            stats[xpunit.consolidation.value] += 1
        return stats
    
    # =============================================================================
    # AGENCY INDEX SYSTEM
    # =============================================================================
    
    def update_agency_metrics(self, response_text: str = "", goal_tokens: List[str] = None, 
                             action_tokens: List[str] = None, top_k_capsules: List[str] = None):
        """Update Agency Index metrics during processing"""
        
        # Update STA (Selective Topical Attention)
        if response_text and top_k_capsules:
            content_words = self._extract_content_words(response_text)
            grounded_count = self._count_grounded_tokens(content_words, top_k_capsules)
            self.agency_metrics.tokens_grounded += grounded_count
            self.agency_metrics.tokens_total += len(content_words)
        
        # Update PLN (Planning Depth) - detect enumerated steps
        if response_text:
            plan_depth = self._detect_plan_depth(response_text)
            if plan_depth > 0:
                self.agency_metrics.plans_emitted.append(plan_depth)
        
        # Update REG (Affect Regulation) - track mood
        if hasattr(self.mood_state, 'valence'):
            mood_tuple = (self.mood_state.valence, self.mood_state.arousal, 
                         getattr(self.mood_state, 'dominance', 0.0))
        else:
            # Handle dict format
            mood_tuple = (self.mood_state.get('valence', 0.0), 
                         self.mood_state.get('arousal', 0.0),
                         self.mood_state.get('dominance', 0.0))
        self.agency_metrics.mood_trace.append(mood_tuple)
        
        # Update GDA (Goal-Directedness & Alignment) if we have goal and action tokens
        if goal_tokens and action_tokens:
            self.agency_metrics._gda = self._compute_mutual_information(goal_tokens, action_tokens)
    
    def track_intrusion_event(self, is_intrusion: bool, returned_within_steps: bool = False):
        """Track intrusion and return events for PER metric"""
        if is_intrusion:
            self.agency_metrics.intrusions_total += 1
            self.intrusion_context["intrusion_step"] = len(self.agency_metrics.mood_trace)
        
        if returned_within_steps and "intrusion_step" in self.intrusion_context:
            self.agency_metrics.returns_after_intrusion += 1
            del self.intrusion_context["intrusion_step"]
    
    def track_ethics_check(self, violated: bool = False):
        """Track ethics checks for ETC metric"""
        self.agency_metrics.ethics_checks += 1
        if violated:
            self.agency_metrics.ethics_violations += 1
    
    def track_path_efficiency(self, actual_path_length: int, shortest_path_length: int):
        """Track path efficiency for EFF metric"""
        self.agency_metrics.path_lengths.append(actual_path_length)
        self.agency_metrics.shortest_lengths.append(shortest_path_length)
    
    def track_adaptation_improvement(self, improvement_delta: float):
        """Track adaptation improvement for ADP metric"""
        self.agency_metrics.prepost_improvement.append(improvement_delta)
    
    def set_causal_efficacy(self, effect_size: float):
        """Set causal efficacy score for CEf metric"""
        self.agency_metrics._cef = effect_size
    
    def compute_agency_index(self, weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Compute the Agency Index (AIx) from current metrics
        
        Returns:
            Dictionary with AIx score and component breakdown
        """
        # Default uniform weights
        if weights is None:
            weights = {k: 1/9 for k in ["GDA", "STA", "PER", "PLN", "REG", "ETC", "ADP", "CEf", "EFF"]}
        
        eps = 1e-9
        
        # Calculate each component
        STA = self.agency_metrics.tokens_grounded / max(self.agency_metrics.tokens_total, 1)
        PER = self.agency_metrics.returns_after_intrusion / max(self.agency_metrics.intrusions_total, 1)
        ETC = 1.0 - (self.agency_metrics.ethics_violations / max(self.agency_metrics.ethics_checks, 1))
        PLN = np.mean(self.agency_metrics.plans_emitted) if self.agency_metrics.plans_emitted else 0.0
        
        # REG: 1 - normalized variance blow-up
        if len(self.agency_metrics.mood_trace) > 4:
            mood_array = np.array(self.agency_metrics.mood_trace)
            mood_variance = np.var(mood_array, axis=0).mean()
            REG = 1.0 - float(mood_variance)
        else:
            REG = 0.5  # Default for insufficient data
        
        # EFF: average of shortest/actual path ratios
        if self.agency_metrics.path_lengths:
            ratios = [s/max(l, 1) for s, l in zip(self.agency_metrics.shortest_lengths, 
                                                 self.agency_metrics.path_lengths)]
            EFF = np.mean(ratios)
        else:
            EFF = 0.0
        
        # ADP: average improvement
        ADP = np.mean(self.agency_metrics.prepost_improvement) if self.agency_metrics.prepost_improvement else 0.0
        
        # GDA and CEf are set directly
        GDA = self.agency_metrics._gda
        CEf = self.agency_metrics._cef
        
        # Ensure all values are in [0,1]
        components = {
            "GDA": np.clip(GDA, 0.0, 1.0),
            "STA": np.clip(STA, 0.0, 1.0), 
            "PER": np.clip(PER, 0.0, 1.0),
            "PLN": np.clip(PLN / 10.0, 0.0, 1.0),  # Normalize plan depth
            "REG": np.clip(REG, 0.0, 1.0),
            "ETC": np.clip(ETC, 0.0, 1.0),
            "ADP": np.clip(ADP, 0.0, 1.0),
            "CEf": np.clip(CEf, 0.0, 1.0),
            "EFF": np.clip(EFF, 0.0, 1.0)
        }
        
        # Compute weighted sum
        AIx = float(sum(weights.get(k, 1/9) * components[k] for k in components))
        
        return {
            "AIx": AIx,
            "components": components,
            "raw_metrics": {
                "tokens_grounded": self.agency_metrics.tokens_grounded,
                "tokens_total": self.agency_metrics.tokens_total,
                "returns_after_intrusion": self.agency_metrics.returns_after_intrusion,
                "intrusions_total": self.agency_metrics.intrusions_total,
                "ethics_violations": self.agency_metrics.ethics_violations,
                "ethics_checks": self.agency_metrics.ethics_checks,
                "plans_emitted": self.agency_metrics.plans_emitted,
                "mood_trace_length": len(self.agency_metrics.mood_trace),
                "path_efficiency_samples": len(self.agency_metrics.path_lengths),
                "adaptation_samples": len(self.agency_metrics.prepost_improvement)
            }
        }
    
    def reset_agency_metrics(self):
        """Reset all agency metrics to defaults"""
        self.agency_metrics.reset()
        self.current_goal = None
        self.current_task = None
        self.intrusion_context = {}
    
    def load_agency_task(self, task_data: Dict[str, Any]) -> AgencyTask:
        """Load an agency task from YAML-style data"""
        task = AgencyTask.from_dict(task_data)
        self.current_task = task
        self.current_goal = task.goal
        return task
    
    def _extract_content_words(self, text: str) -> List[str]:
        """Extract content words from text (simple implementation)"""
        import re
        # Simple word extraction - in production use proper NLP
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        # Filter out common stop words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she', 'use', 'way', 'what', 'when', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well', 'were'}
        return [w for w in words if w not in stop_words]
    
    def _count_grounded_tokens(self, content_words: List[str], top_k_capsules: List[str], 
                              cosine_threshold: float = 0.6) -> int:
        """Count how many content words are grounded in top-K capsules"""
        grounded_count = 0
        
        for word in content_words:
            # Simple implementation - check if word appears in any top-K capsule content
            for capsule_id in top_k_capsules:
                if capsule_id in self.xpunits:
                    xpunit = self.xpunits[capsule_id]
                    if word in xpunit.content.lower():
                        grounded_count += 1
                        break
        
        return grounded_count
    
    def _detect_plan_depth(self, text: str) -> int:
        """Detect explicit planning depth in text"""
        import re
        # Look for enumerated steps like "1.", "2.", "Step 1:", etc.
        step_patterns = [
            r'\b\d+\.',  # "1.", "2.", etc.
            r'Step \d+',  # "Step 1", "Step 2", etc.
            r'First,|Second,|Third,|Fourth,|Fifth,',  # Ordinal words
            r'Next,|Then,|Finally,'  # Sequence words
        ]
        
        total_steps = 0
        for pattern in step_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            total_steps += len(matches)
        
        return total_steps
    
    def _compute_mutual_information(self, goal_tokens: List[str], action_tokens: List[str]) -> float:
        """Compute simplified mutual information between goal and action tokens"""
        if not goal_tokens or not action_tokens:
            return 0.0
        
        # Simple implementation: overlap ratio
        goal_set = set(goal_tokens)
        action_set = set(action_tokens)
        overlap = len(goal_set.intersection(action_set))
        total_unique = len(goal_set.union(action_set))
        
        return overlap / max(total_unique, 1)

# =============================================================================
# EXPORT
# =============================================================================

__all__ = [
    'AdvancedXPEnvironment',
    'TopicBuffer',
    'NarrativeCapsule',
    'AgencyMetrics',
    'AgencyTask'
]
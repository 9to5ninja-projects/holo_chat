"""
Holographic Memory System - Mathematical Foundation
==================================================

Implementation of the rigorous holographic memory specification with:
- HRR binding/unbinding operations using FFT
- Role-filler capsule architecture  
- Global associative memory with decay/consolidation
- Compositional query capabilities
- Capacity management and noise control

Based on the mathematical blueprint:
- Core representational spaces with embedding dimension D
- Binding ⊗ / Unbinding ⊘ using circular convolution/correlation
- Superposition ⊕ with normalization
- Probabilistic semantics and attractor dynamics

Author: Lumina Memory Team
License: MIT
"""

import numpy as np
import time
import json
from typing import Dict, List, Optional, Any, Tuple, Union, Set
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Import our enhanced constants
from .constants import (
    PHI, TAU, EPSILON, NORMALIZATION_EPSILON, 
    HRR_DIM, SEMANTIC_DIM, HOLOGRAPHIC_DIM,
    VECTOR_DTYPE, SCORE_DTYPE, TIME_DTYPE,
    DEFAULT_DECAY_RATE, DEFAULT_IMPORTANCE,
    HIGH_SIMILARITY_THRESHOLD, MEDIUM_SIMILARITY_THRESHOLD
)

# =============================================================================
# CORE HRR OPERATIONS - FFT-BASED BINDING/UNBINDING
# =============================================================================

def circular_convolution(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    HRR binding operation: a ⊗ b = F^(-1)(F(a) ⊙ F(b))
    
    Args:
        a, b: Input vectors of same length
        
    Returns:
        Bound vector via circular convolution
    """
    return np.fft.irfft(np.fft.rfft(a) * np.fft.rfft(b), n=len(a))

def circular_correlation(c: np.ndarray, a: np.ndarray) -> np.ndarray:
    """
    HRR unbinding operation: c ⊘ a = F^(-1)(F(c) ⊙ F̄(a))
    
    Args:
        c: Composite vector
        a: Vector to unbind
        
    Returns:
        Unbound vector via circular correlation
    """
    return np.fft.irfft(np.fft.rfft(c) * np.conj(np.fft.rfft(a)), n=len(c))

def normalize_vector(v: np.ndarray, epsilon: float = NORMALIZATION_EPSILON) -> np.ndarray:
    """
    Normalize vector with numerical stability
    
    Args:
        v: Input vector
        epsilon: Stability threshold
        
    Returns:
        Unit normalized vector
    """
    norm = np.linalg.norm(v)
    if norm < epsilon:
        return np.zeros_like(v, dtype=VECTOR_DTYPE)
    return (v / norm).astype(VECTOR_DTYPE)

def cosine_similarity(x: np.ndarray, y: np.ndarray) -> float:
    """
    Cosine similarity: sim(x,y) = (x·y)/(||x|| ||y||)
    
    Args:
        x, y: Input vectors
        
    Returns:
        Cosine similarity score
    """
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    
    if norm_x < EPSILON or norm_y < EPSILON:
        return 0.0
        
    return float(np.dot(x, y) / (norm_x * norm_y))

# =============================================================================
# ROLE AND SYMBOL SPACES
# =============================================================================

class RoleSpace:
    """
    Manages role vectors R = {r₁, ..., rₖ}
    Each role is a random unit vector r ∈ ℝᴰ
    """
    
    def __init__(self, dimension: int = HRR_DIM, seed: int = 42):
        self.dimension = dimension
        self.roles: Dict[str, np.ndarray] = {}
        self.rng = np.random.RandomState(seed)
        
        # Create standard 6W roles
        self._create_standard_roles()
        
    def _create_standard_roles(self):
        """Create standard WHO/WHAT/WHERE/WHEN/WHY/HOW roles"""
        standard_roles = ['WHO', 'WHAT', 'WHERE', 'WHEN', 'WHY', 'HOW']
        
        for role_name in standard_roles:
            self.roles[role_name] = self._generate_role_vector()
            
    def _generate_role_vector(self) -> np.ndarray:
        """Generate a random unit vector for a role"""
        vector = self.rng.randn(self.dimension).astype(VECTOR_DTYPE)
        return normalize_vector(vector)
        
    def get_role(self, name: str) -> np.ndarray:
        """Get role vector by name, creating if needed"""
        if name not in self.roles:
            self.roles[name] = self._generate_role_vector()
        return self.roles[name].copy()
        
    def add_role(self, name: str, vector: Optional[np.ndarray] = None) -> np.ndarray:
        """Add a new role with optional custom vector"""
        if vector is not None:
            self.roles[name] = normalize_vector(vector)
        else:
            self.roles[name] = self._generate_role_vector()
        return self.roles[name].copy()
        
    def list_roles(self) -> List[str]:
        """List all available role names"""
        return list(self.roles.keys())

class SymbolSpace:
    """
    Manages symbol/filler vectors S
    Each symbol is a unit vector s ∈ ℝᴰ
    Can plug in encoders to map text/images → vectors
    """
    
    def __init__(self, dimension: int = HRR_DIM, seed: int = 43):
        self.dimension = dimension
        self.symbols: Dict[str, np.ndarray] = {}
        self.rng = np.random.RandomState(seed)
        
    def _generate_symbol_vector(self) -> np.ndarray:
        """Generate a random unit vector for a symbol"""
        vector = self.rng.randn(self.dimension).astype(VECTOR_DTYPE)
        return normalize_vector(vector)
        
    def get_symbol(self, name: str) -> np.ndarray:
        """Get symbol vector by name, creating if needed"""
        if name not in self.symbols:
            self.symbols[name] = self._generate_symbol_vector()
        return self.symbols[name].copy()
        
    def add_symbol(self, name: str, vector: Optional[np.ndarray] = None) -> np.ndarray:
        """Add a new symbol with optional custom vector"""
        if vector is not None:
            self.symbols[name] = normalize_vector(vector)
        else:
            self.symbols[name] = self._generate_symbol_vector()
        return self.symbols[name].copy()
        
    def encode_text(self, text: str) -> np.ndarray:
        """
        Encode text to symbol vector (placeholder for encoder integration)
        In production, this would use sentence transformers, etc.
        """
        # For now, use deterministic hash-based encoding
        hash_val = hash(text) % (2**31)
        rng = np.random.RandomState(hash_val)
        vector = rng.randn(self.dimension).astype(VECTOR_DTYPE)
        return normalize_vector(vector)
        
    def find_nearest_symbol(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """Find nearest symbols to query vector"""
        similarities = []
        
        for name, symbol_vector in self.symbols.items():
            sim = cosine_similarity(query_vector, symbol_vector)
            similarities.append((name, sim))
            
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
        
    def list_symbols(self) -> List[str]:
        """List all available symbol names"""
        return list(self.symbols.keys())

# =============================================================================
# MEMORY CAPSULE - TYPED, WEIGHTED ROLE-FILLER MAP
# =============================================================================

@dataclass
class MemoryCapsule:
    """
    A single memory object (capsule/head) as a typed, weighted role-filler map:
    cap = {(r, s_r, w_r) | r ∈ R}
    
    Its holographic embedding:
    v_cap = norm(Σ w_r (r ⊗ s_r))
    """
    
    # Core role-filler bindings
    bindings: Dict[str, Tuple[np.ndarray, float]] = field(default_factory=dict)  # role_name -> (symbol_vector, weight)
    
    # Metadata
    timestamp: float = field(default_factory=time.time)
    importance: float = DEFAULT_IMPORTANCE
    salience: float = 1.0
    reliability: float = 1.0
    
    # Cached holographic vector
    _vector_cache: Optional[np.ndarray] = field(default=None, init=False)
    _cache_valid: bool = field(default=False, init=False)
    
    def add_binding(self, role_name: str, symbol_vector: np.ndarray, weight: float = 1.0):
        """Add a role-filler binding to the capsule"""
        self.bindings[role_name] = (normalize_vector(symbol_vector), weight)
        self._invalidate_cache()
        
    def get_binding(self, role_name: str) -> Optional[Tuple[np.ndarray, float]]:
        """Get role-filler binding by role name"""
        return self.bindings.get(role_name)
        
    def _invalidate_cache(self):
        """Invalidate the cached holographic vector"""
        self._cache_valid = False
        self._vector_cache = None
        
    @property
    def vector(self) -> np.ndarray:
        """
        Get holographic embedding: v_cap = norm(Σ w_r (r ⊗ s_r))
        Uses caching for efficiency
        """
        if not self._cache_valid or self._vector_cache is None:
            self._compute_vector()
        return self._vector_cache.copy()
        
    def _compute_vector(self):
        """Compute the holographic embedding vector"""
        if not self.bindings:
            # Empty capsule
            dimension = HRR_DIM  # Default dimension
            self._vector_cache = np.zeros(dimension, dtype=VECTOR_DTYPE)
            self._cache_valid = True
            return
            
        # Get dimension from first binding
        first_symbol = next(iter(self.bindings.values()))[0]
        dimension = len(first_symbol)
        
        # Accumulate weighted role-filler bindings
        accumulator = np.zeros(dimension, dtype=VECTOR_DTYPE)
        
        for role_name, (symbol_vector, weight) in self.bindings.items():
            # For now, use role name to generate role vector
            # In production, this would use RoleSpace
            role_vector = self._get_role_vector(role_name, dimension)
            
            # Bind role and filler: r ⊗ s
            bound = circular_convolution(role_vector, symbol_vector)
            
            # Add weighted binding
            accumulator += weight * bound
            
        # Normalize the result
        self._vector_cache = normalize_vector(accumulator)
        self._cache_valid = True
        
    def _get_role_vector(self, role_name: str, dimension: int) -> np.ndarray:
        """Generate role vector from name (placeholder for RoleSpace integration)"""
        # Use deterministic hash-based generation
        hash_val = hash(role_name) % (2**31)
        rng = np.random.RandomState(hash_val)
        vector = rng.randn(dimension).astype(VECTOR_DTYPE)
        return normalize_vector(vector)
        
    def unbind_role(self, role_name: str) -> np.ndarray:
        """
        Unbind a role from the capsule: ŝ_r = norm(v_cap ⊘ r)
        
        Args:
            role_name: Name of role to unbind
            
        Returns:
            Estimated filler vector for the role
        """
        role_vector = self._get_role_vector(role_name, len(self.vector))
        unbound = circular_correlation(self.vector, role_vector)
        return normalize_vector(unbound)
        
    def get_age_hours(self) -> float:
        """Get age of capsule in hours"""
        return (time.time() - self.timestamp) / 3600.0
        
    def get_decay_factor(self, decay_rate: float = DEFAULT_DECAY_RATE) -> float:
        """Get exponential decay factor: e^(-t/τ)"""
        age_hours = self.get_age_hours()
        return np.exp(-decay_rate * age_hours)
        
    def get_effective_weight(self, decay_rate: float = DEFAULT_DECAY_RATE) -> float:
        """Get effective weight: importance × decay × reliability"""
        return self.importance * self.get_decay_factor(decay_rate) * self.reliability
        
    def to_dict(self) -> Dict[str, Any]:
        """Serialize capsule to dictionary"""
        return {
            'bindings': {
                role: (symbol.tolist(), weight) 
                for role, (symbol, weight) in self.bindings.items()
            },
            'timestamp': self.timestamp,
            'importance': self.importance,
            'salience': self.salience,
            'reliability': self.reliability
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryCapsule':
        """Deserialize capsule from dictionary"""
        capsule = cls(
            timestamp=data['timestamp'],
            importance=data['importance'],
            salience=data['salience'],
            reliability=data['reliability']
        )
        
        for role, (symbol_list, weight) in data['bindings'].items():
            symbol_vector = np.array(symbol_list, dtype=VECTOR_DTYPE)
            capsule.add_binding(role, symbol_vector, weight)
            
        return capsule

# =============================================================================
# HOLOGRAPHIC ASSOCIATIVE MEMORY - GLOBAL SUPERPOSITION
# =============================================================================

class HolographicAssociativeMemory:
    """
    Global associative memory with superposition and decay:
    H(t) = norm(Σ α_i(t) v_cap,i)
    
    Where α_i(t) = importance_i × e^(-(t-t_i)/τ) × γ_i
    """
    
    def __init__(self, dimension: int = HRR_DIM, decay_rate: float = DEFAULT_DECAY_RATE):
        self.dimension = dimension
        self.decay_rate = decay_rate
        
        # Storage
        self.capsules: List[MemoryCapsule] = []
        self.role_space = RoleSpace(dimension)
        self.symbol_space = SymbolSpace(dimension)
        
        # Cached global memory vector
        self._global_vector: Optional[np.ndarray] = None
        self._cache_timestamp: float = 0.0
        self._cache_valid: bool = False
        
    def add_capsule(self, capsule: MemoryCapsule):
        """Add a memory capsule to the global memory"""
        self.capsules.append(capsule)
        self._invalidate_cache()
        
    def create_capsule(self, bindings: Dict[str, Union[str, np.ndarray]], 
                      importance: float = DEFAULT_IMPORTANCE) -> MemoryCapsule:
        """
        Create and add a new memory capsule
        
        Args:
            bindings: Dict of role_name -> symbol (string or vector)
            importance: Importance weight
            
        Returns:
            Created capsule
        """
        capsule = MemoryCapsule(importance=importance)
        
        for role_name, symbol in bindings.items():
            if isinstance(symbol, str):
                symbol_vector = self.symbol_space.get_symbol(symbol)
            else:
                symbol_vector = symbol
                
            capsule.add_binding(role_name, symbol_vector)
            
        self.add_capsule(capsule)
        return capsule
        
    def _invalidate_cache(self):
        """Invalidate cached global memory vector"""
        self._cache_valid = False
        
    def get_global_memory(self, current_time: Optional[float] = None) -> np.ndarray:
        """
        Get global memory vector: H(t) = norm(Σ α_i(t) v_cap,i)
        
        Args:
            current_time: Current timestamp (defaults to now)
            
        Returns:
            Global memory vector
        """
        if current_time is None:
            current_time = time.time()
            
        # Check cache validity
        if (self._cache_valid and 
            self._global_vector is not None and 
            abs(current_time - self._cache_timestamp) < 1.0):  # 1 second tolerance
            return self._global_vector.copy()
            
        # Recompute global memory
        if not self.capsules:
            self._global_vector = np.zeros(self.dimension, dtype=VECTOR_DTYPE)
        else:
            accumulator = np.zeros(self.dimension, dtype=VECTOR_DTYPE)
            
            for capsule in self.capsules:
                weight = capsule.get_effective_weight(self.decay_rate)
                if weight > EPSILON:  # Skip negligible contributions
                    accumulator += weight * capsule.vector
                    
            self._global_vector = normalize_vector(accumulator)
            
        self._cache_timestamp = current_time
        self._cache_valid = True
        
        return self._global_vector.copy()
        
    def query_role(self, role_name: str, current_time: Optional[float] = None) -> np.ndarray:
        """
        Query a role from global memory: ŝ_r(t) = norm(H(t) ⊘ r)
        
        Args:
            role_name: Name of role to query
            current_time: Current timestamp
            
        Returns:
            Estimated filler vector for the role
        """
        global_memory = self.get_global_memory(current_time)
        role_vector = self.role_space.get_role(role_name)
        
        unbound = circular_correlation(global_memory, role_vector)
        return normalize_vector(unbound)
        
    def find_best_symbol_for_role(self, role_name: str, 
                                 current_time: Optional[float] = None,
                                 top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find best matching symbols for a role query
        
        Args:
            role_name: Role to query
            current_time: Current timestamp
            top_k: Number of top matches to return
            
        Returns:
            List of (symbol_name, similarity_score) tuples
        """
        query_vector = self.query_role(role_name, current_time)
        return self.symbol_space.find_nearest_symbol(query_vector, top_k)
        
    def compositional_query(self, query_bindings: Dict[str, str],
                           current_time: Optional[float] = None) -> List[Tuple[MemoryCapsule, float]]:
        """
        Compositional query: bind multiple known roles and find matching capsules
        q = r_where ⊗ s_lab ⊕ r_when ⊗ s_yesterday
        
        Args:
            query_bindings: Dict of role_name -> symbol_name
            current_time: Current timestamp
            
        Returns:
            List of (capsule, similarity_score) tuples
        """
        # Build query vector
        query_accumulator = np.zeros(self.dimension, dtype=VECTOR_DTYPE)
        
        for role_name, symbol_name in query_bindings.items():
            role_vector = self.role_space.get_role(role_name)
            symbol_vector = self.symbol_space.get_symbol(symbol_name)
            
            # Bind role and symbol
            bound = circular_convolution(role_vector, symbol_vector)
            query_accumulator += bound
            
        query_vector = normalize_vector(query_accumulator)
        
        # Find matching capsules
        matches = []
        for capsule in self.capsules:
            similarity = cosine_similarity(query_vector, capsule.vector)
            matches.append((capsule, similarity))
            
        # Sort by similarity
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
        
    def get_capacity_stats(self) -> Dict[str, Any]:
        """Get capacity and performance statistics"""
        return {
            'num_capsules': len(self.capsules),
            'dimension': self.dimension,
            'decay_rate': self.decay_rate,
            'total_roles': len(self.role_space.list_roles()),
            'total_symbols': len(self.symbol_space.list_symbols()),
            'estimated_capacity': self.dimension // 4,  # Rule of thumb: D/4 for good recall
            'memory_usage_mb': self._estimate_memory_usage()
        }
        
    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage in MB"""
        bytes_per_float = 4  # float32
        
        # Capsule vectors
        capsule_memory = len(self.capsules) * self.dimension * bytes_per_float
        
        # Role and symbol spaces
        role_memory = len(self.role_space.roles) * self.dimension * bytes_per_float
        symbol_memory = len(self.symbol_space.symbols) * self.dimension * bytes_per_float
        
        # Global memory cache
        global_memory = self.dimension * bytes_per_float
        
        total_bytes = capsule_memory + role_memory + symbol_memory + global_memory
        return total_bytes / (1024 * 1024)  # Convert to MB

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_demo_memory() -> HolographicAssociativeMemory:
    """Create a demo holographic memory with sample data"""
    memory = HolographicAssociativeMemory(dimension=512)
    
    # Create sample episodes
    episodes = [
        {'WHO': 'alice', 'WHAT': 'read', 'WHERE': 'library', 'WHEN': 'morning'},
        {'WHO': 'bob', 'WHAT': 'cook', 'WHERE': 'kitchen', 'WHEN': 'evening'},
        {'WHO': 'alice', 'WHAT': 'study', 'WHERE': 'library', 'WHEN': 'afternoon'}
    ]
    
    for i, episode in enumerate(episodes):
        memory.create_capsule(episode, importance=1.0 - i * 0.1)
        
    return memory

def run_capacity_test(dimensions: List[int] = [256, 512, 1024], 
                     num_associations: List[int] = [5, 10, 20, 50]) -> Dict[str, List[float]]:
    """
    Run capacity test across different dimensions and association counts
    
    Returns:
        Dictionary with recall accuracies
    """
    results = {f'D={d}': [] for d in dimensions}
    
    for dim in dimensions:
        for num_assoc in num_associations:
            memory = HolographicAssociativeMemory(dimension=dim)
            
            # Create random associations
            correct_recalls = 0
            total_tests = min(10, num_assoc)  # Test subset
            
            # Add associations
            for i in range(num_assoc):
                bindings = {
                    'WHAT': f'concept_{i}',
                    'WHERE': f'location_{i % 5}',  # Some overlap
                    'WHEN': f'time_{i % 3}'       # More overlap
                }
                memory.create_capsule(bindings)
                
            # Test recall
            for i in range(total_tests):
                # Query for WHAT given WHERE
                query_results = memory.compositional_query({'WHERE': f'location_{i % 5}'})
                
                if query_results:
                    # Check if top result contains correct concept
                    top_capsule = query_results[0][0]
                    if f'concept_{i}' in [binding[0] for binding in top_capsule.bindings.values()]:
                        correct_recalls += 1
                        
            accuracy = correct_recalls / total_tests if total_tests > 0 else 0.0
            results[f'D={dim}'].append(accuracy)
            
    return results

# =============================================================================
# EXPORT ALL CLASSES AND FUNCTIONS
# =============================================================================

__all__ = [
    # Core operations
    'circular_convolution', 'circular_correlation', 'normalize_vector', 'cosine_similarity',
    
    # Spaces
    'RoleSpace', 'SymbolSpace',
    
    # Memory components
    'MemoryCapsule', 'HolographicAssociativeMemory',
    
    # Utilities
    'create_demo_memory', 'run_capacity_test'
]
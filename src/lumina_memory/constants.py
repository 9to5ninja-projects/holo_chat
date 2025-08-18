"""
Canonical Constants for Lumina Memory System
==========================================

This module contains all canonical constants, dimensions, and default values
used across the Lumina Memory System. All implementations must import from
this module to ensure consistency.

Source: xp_core_design.ipynb cells 1-3 (validated implementation)
Documentation: docs/CANONICAL_MATH_REFERENCE.md
"""

import numpy as np

# =============================================================================
# VECTOR DIMENSIONS - CANONICAL VALUES
# =============================================================================

# Core vector dimensions (from working notebook) - UNIFIED TO 512
SEMANTIC_DIM = 512          # Unified dimension for consistency
EMOTION_DIM = 8             # Emotion vector dimension  
HRR_DIM = 512              # HRR vector dimension (matches semantic)
HOLOGRAPHIC_DIM = 512       # Full holographic shape dimension

# Alternative dimension names for compatibility
SEMANTIC_VECTOR_SIZE = SEMANTIC_DIM
EMOTION_VECTOR_SIZE = EMOTION_DIM
HRR_VECTOR_SIZE = HRR_DIM

# =============================================================================
# TEMPORAL PARAMETERS - FROM MEMORYUNIT.SCORE()
# =============================================================================

# Decay parameters (from MemoryUnit class in notebook cell 2)
DEFAULT_DECAY_RATE = 0.1        # Per hour decay rate (exp(-0.1 * hours))
DEFAULT_IMPORTANCE = 1.0        # Maximum importance value
DEFAULT_HALF_LIFE_HOURS = 6.93  # Derived: ln(2)/0.1 ≈ 6.93 hours

# Scoring weights (from MemoryUnit.score() method)
DEFAULT_W_SEMANTIC = 0.7        # Semantic similarity weight  
DEFAULT_W_EMOTION = 0.3         # Emotional similarity weight

# =============================================================================
# MATHEMATICAL CONSTANTS - FROM WORKING FORMULAS
# =============================================================================

# Fundamental mathematical constants (from notebook developments)
PHI = (1 + np.sqrt(5)) / 2      # Golden ratio: 1.618034 (holographic operations)
TAU = 2 * np.pi                 # Full circle constant: 6.283185 (circular convolution)

# Numerical stability
EPSILON = 1e-9                  # Numerical stability threshold
NORMALIZATION_EPSILON = 1e-9    # Vector normalization threshold

# Coherence weights (from MemoryUnit.mathematical_coherence())
COHERENCE_HRR_WEIGHT = 0.6      # HRR similarity weight
COHERENCE_SEM_WEIGHT = 0.4      # Semantic similarity weight

# Lexical attribution weights (from HybridLexicalAttributor)
HYBRID_SPACY_WEIGHT = 0.6       # SpaCy token similarity weight
HYBRID_MATH_WEIGHT = 0.4        # Mathematical salience weight

# Confidence levels (from HybridLexicalAttributor.compute_attribution())
CONFIDENCE_HYBRID = 0.9         # When SpaCy + math combined
CONFIDENCE_SPACY_ONLY = 0.7     # When only SpaCy available  
CONFIDENCE_MATH_ONLY = 0.3      # When only mathematical method

# =============================================================================
# DATA TYPE SPECIFICATIONS
# =============================================================================

# Preferred NumPy dtypes for memory efficiency
VECTOR_DTYPE = np.float32       # Standard vector type
SCORE_DTYPE = np.float64        # High precision for scores
TIME_DTYPE = np.float64         # High precision for timestamps

# =============================================================================
# THRESHOLDS AND LIMITS
# =============================================================================

# Similarity thresholds
HIGH_SIMILARITY_THRESHOLD = 0.8    # Very similar memories
MEDIUM_SIMILARITY_THRESHOLD = 0.5  # Moderately similar 
LOW_SIMILARITY_THRESHOLD = 0.2     # Barely related

# Coherence thresholds  
HIGH_COHERENCE_THRESHOLD = 0.7     # Highly coherent
MEDIUM_COHERENCE_THRESHOLD = 0.4   # Moderately coherent
LOW_COHERENCE_THRESHOLD = 0.1      # Low coherence

# Score bounds
MIN_SCORE = 0.0                    # Minimum possible score
MAX_SCORE = 1.0                    # Maximum possible score

# =============================================================================
# SPACY INTEGRATION CONSTANTS
# =============================================================================

# SpaCy model configuration
SPACY_MODEL_NAME = "en_core_web_sm"     # Default English model
SPACY_VECTOR_SIZE = 96                  # en_core_web_sm vector size
SPACY_EMBEDDING_DIM = 384               # Custom embedding dimension

# =============================================================================
# HRR OPERATION PARAMETERS
# =============================================================================

# Role vector seeds (for deterministic role generation)
ROLE_VECTOR_SEED = 12345            # Fixed seed for reproducible roles
BINDING_NOISE_LEVEL = 0.0           # Noise in binding operations
UNBINDING_ACCURACY_THRESHOLD = 0.5  # Minimum acceptable retrieval accuracy

# Standard 6W role names
W6_ROLES = ['WHAT', 'WHERE', 'WHEN', 'WHO', 'WHY', 'HOW']

# =============================================================================
# MEMORY SYSTEM PARAMETERS
# =============================================================================

# Default memory parameters
DEFAULT_SALIENCE = 1.0              # Initial salience value
MINIMUM_SALIENCE = 0.01             # Minimum retained salience
DECAY_FLOOR = 0.1                   # 10% minimum retention

# Access patterns
ACCESS_BOOST_FACTOR = 1.2           # Salience boost on access
CONSOLIDATION_THRESHOLD = 0.8       # Threshold for memory consolidation

# =============================================================================
# CONSCIOUSNESS ANALYSIS CONSTANTS - FROM NOTEBOOK DEVELOPMENTS
# =============================================================================

# Consciousness scoring weights (from xpunit_full_system_test.ipynb)
CONSCIOUSNESS_SELF_REFERENCE_WEIGHT = 0.3      # Weight for "I am", "my own" detection
CONSCIOUSNESS_INTROSPECTION_WEIGHT = 0.2       # Weight per introspection word
CONSCIOUSNESS_RECURSIVE_WEIGHT = 0.4           # Weight for recursive processing

# Consciousness thresholds
HIGH_CONSCIOUSNESS_THRESHOLD = 0.5             # High consciousness level (>0.5)
MEDIUM_CONSCIOUSNESS_THRESHOLD = 0.2           # Medium consciousness level (0.2-0.5)
LOW_CONSCIOUSNESS_THRESHOLD = 0.0              # Low consciousness level (<=0.2)

# Consciousness indicators
CONSCIOUSNESS_SELF_REFERENCE_SCORE = 0.8       # Score for self-reference detection
CONSCIOUSNESS_INTROSPECTION_MULTIPLIER = 0.3   # Multiplier for introspection count
CONSCIOUSNESS_RECURSIVE_SCORE = 0.9            # Score for recursive processing

# Consciousness keywords for analysis
CONSCIOUSNESS_INTROSPECTION_WORDS = [
    "thinking", "analyzing", "wondering", "consciousness", 
    "aware", "reflection", "contemplating", "pondering"
]

# =============================================================================
# OPTIMIZATION PARAMETERS
# =============================================================================

# Batch processing
DEFAULT_BATCH_SIZE = 32             # Default batch size for processing
MAX_BATCH_SIZE = 512                # Maximum batch size
MIN_BATCH_SIZE = 1                  # Minimum batch size

# Memory limits
MAX_VECTOR_CACHE_SIZE = 10000       # Maximum cached vectors
MAX_MEMORY_UNITS = 100000           # Maximum memory units in system

# =============================================================================
# ERROR HANDLING CONSTANTS
# =============================================================================

# Default fallback values
FALLBACK_SIMILARITY = 0.0           # When similarity computation fails
FALLBACK_COHERENCE = 0.0            # When coherence computation fails  
FALLBACK_SALIENCE = 0.1             # When salience computation fails

# Validation tolerances
VECTOR_NORM_TOLERANCE = 1e-6        # Tolerance for unit vector validation
SCORE_TOLERANCE = 1e-8              # Tolerance for score comparisons

# =============================================================================
# CANONICAL FEATURE FLAGS
# =============================================================================

# Optional feature availability (set at runtime)
SPACY_AVAILABLE = False             # Set by spaCy import check
TORCH_AVAILABLE = False             # Set by PyTorch import check  
NETWORKX_AVAILABLE = False          # Set by NetworkX import check
ENCRYPTION_AVAILABLE = False        # Set by cryptography import check

# =============================================================================
# EXPORT ALL CONSTANTS
# =============================================================================

__all__ = [
    # Dimensions
    'SEMANTIC_DIM', 'EMOTION_DIM', 'HRR_DIM', 'HOLOGRAPHIC_DIM',
    'SEMANTIC_VECTOR_SIZE', 'EMOTION_VECTOR_SIZE', 'HRR_VECTOR_SIZE',
    
    # Temporal parameters  
    'DEFAULT_DECAY_RATE', 'DEFAULT_IMPORTANCE', 'DEFAULT_HALF_LIFE_HOURS',
    'DEFAULT_W_SEMANTIC', 'DEFAULT_W_EMOTION',
    
    # Mathematical constants
    'PHI', 'TAU', 'EPSILON', 'NORMALIZATION_EPSILON', 'COHERENCE_HRR_WEIGHT', 'COHERENCE_SEM_WEIGHT',
    'HYBRID_SPACY_WEIGHT', 'HYBRID_MATH_WEIGHT', 'CONFIDENCE_HYBRID', 'CONFIDENCE_SPACY_ONLY', 'CONFIDENCE_MATH_ONLY',
    
    # Data types
    'VECTOR_DTYPE', 'SCORE_DTYPE', 'TIME_DTYPE',
    
    # Thresholds
    'HIGH_SIMILARITY_THRESHOLD', 'MEDIUM_SIMILARITY_THRESHOLD', 'LOW_SIMILARITY_THRESHOLD',
    'HIGH_COHERENCE_THRESHOLD', 'MEDIUM_COHERENCE_THRESHOLD', 'LOW_COHERENCE_THRESHOLD',
    'MIN_SCORE', 'MAX_SCORE',
    
    # SpaCy constants
    'SPACY_MODEL_NAME', 'SPACY_VECTOR_SIZE', 'SPACY_EMBEDDING_DIM',
    
    # HRR parameters
    'ROLE_VECTOR_SEED', 'BINDING_NOISE_LEVEL', 'UNBINDING_ACCURACY_THRESHOLD', 'W6_ROLES',
    
    # Memory system
    'DEFAULT_SALIENCE', 'MINIMUM_SALIENCE', 'DECAY_FLOOR', 'ACCESS_BOOST_FACTOR', 'CONSOLIDATION_THRESHOLD',
    
    # Consciousness analysis
    'CONSCIOUSNESS_SELF_REFERENCE_WEIGHT', 'CONSCIOUSNESS_INTROSPECTION_WEIGHT', 'CONSCIOUSNESS_RECURSIVE_WEIGHT',
    'HIGH_CONSCIOUSNESS_THRESHOLD', 'MEDIUM_CONSCIOUSNESS_THRESHOLD', 'LOW_CONSCIOUSNESS_THRESHOLD',
    'CONSCIOUSNESS_SELF_REFERENCE_SCORE', 'CONSCIOUSNESS_INTROSPECTION_MULTIPLIER', 'CONSCIOUSNESS_RECURSIVE_SCORE',
    'CONSCIOUSNESS_INTROSPECTION_WORDS',
    
    # Optimization
    'DEFAULT_BATCH_SIZE', 'MAX_BATCH_SIZE', 'MIN_BATCH_SIZE', 'MAX_VECTOR_CACHE_SIZE', 'MAX_MEMORY_UNITS',
    
    # Error handling
    'FALLBACK_SIMILARITY', 'FALLBACK_COHERENCE', 'FALLBACK_SALIENCE', 'VECTOR_NORM_TOLERANCE', 'SCORE_TOLERANCE',
    
    # Feature flags
    'SPACY_AVAILABLE', 'TORCH_AVAILABLE', 'NETWORKX_AVAILABLE', 'ENCRYPTION_AVAILABLE'
]

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_vector_dimension(vector: np.ndarray, expected_dim: int) -> bool:
    """Validate vector has expected canonical dimension"""
    return isinstance(vector, np.ndarray) and vector.shape == (expected_dim,)

def validate_semantic_vector(vector: np.ndarray) -> bool:
    """Validate semantic vector has canonical dimension"""
    return validate_vector_dimension(vector, SEMANTIC_DIM)

def validate_emotion_vector(vector: np.ndarray) -> bool:
    """Validate emotion vector has canonical dimension"""
    return validate_vector_dimension(vector, EMOTION_DIM)

def validate_hrr_vector(vector: np.ndarray) -> bool:
    """Validate HRR vector has canonical dimension"""
    return validate_vector_dimension(vector, HRR_DIM)

def validate_score(score: float) -> bool:
    """Validate score is within canonical bounds"""
    return isinstance(score, (int, float)) and MIN_SCORE <= score <= MAX_SCORE

def get_canonical_weights() -> dict:
    """Get all canonical weights as dictionary"""
    return {
        'semantic_weight': DEFAULT_W_SEMANTIC,
        'emotion_weight': DEFAULT_W_EMOTION,
        'hrr_coherence_weight': COHERENCE_HRR_WEIGHT,
        'semantic_coherence_weight': COHERENCE_SEM_WEIGHT,
        'hybrid_spacy_weight': HYBRID_SPACY_WEIGHT,
        'hybrid_math_weight': HYBRID_MATH_WEIGHT
    }

def get_canonical_dimensions() -> dict:
    """Get all canonical dimensions as dictionary"""
    return {
        'semantic_dim': SEMANTIC_DIM,
        'emotion_dim': EMOTION_DIM,
        'hrr_dim': HRR_DIM,
        'holographic_dim': HOLOGRAPHIC_DIM
    }

def get_canonical_thresholds() -> dict:
    """Get all canonical thresholds as dictionary"""
    return {
        'high_similarity': HIGH_SIMILARITY_THRESHOLD,
        'medium_similarity': MEDIUM_SIMILARITY_THRESHOLD,
        'low_similarity': LOW_SIMILARITY_THRESHOLD,
        'high_coherence': HIGH_COHERENCE_THRESHOLD,
        'medium_coherence': MEDIUM_COHERENCE_THRESHOLD,
        'low_coherence': LOW_COHERENCE_THRESHOLD
    }

# Add validation functions to exports
__all__.extend([
    'validate_vector_dimension', 'validate_semantic_vector', 'validate_emotion_vector',
    'validate_hrr_vector', 'validate_score', 'get_canonical_weights',
    'get_canonical_dimensions', 'get_canonical_thresholds'
])

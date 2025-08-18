hell# XPUnit Consolidation Plan
## Generated: 2025-01-16

### Analysis Summary
- **10 definitions** found across the codebase
- **125 references** to XPUnit classes and functions  
- **16 issues** identified (missing attributes, methods, imports)

### Issues Found

#### Critical Issues (1)
1. **Missing Import** in `xpunit_lifecycle_tracer.py`
   - File needs: `from lumina_memory.xp_core_unified import XPUnit`

#### Warning Issues (15)
1. **Missing Attributes** in multiple files:
   - `xpunit_consolidator.py` - XPUnit classes missing expected attributes
   - `xpunit_lifecycle_tracer.py` - XPUnit classes missing expected attributes

2. **Missing Methods** in multiple files:
   - `xpunit_consolidator.py` - XPUnit classes missing expected methods
   - `xpunit_lifecycle_tracer.py` - XPUnit classes missing expected methods

### Canonical XPUnit Definition
**Location**: `src/lumina_memory/xp_core_unified.py` (lines 124-199)

**Complete XPUnit Class Structure**:
```python
@dataclass
class XPUnit:
    # Core identity
    content_id: str
    content: str
    
    # Mathematical representations  
    semantic_vector: np.ndarray
    hrr_shape: np.ndarray
    emotion_vector: np.ndarray
    
    # Temporal properties
    timestamp: float
    last_access: float
    decay_rate: float
    importance: float
    access_count: int = 0
    
    # Relational properties
    coherence_links: Dict[str, float] = field(default_factory=dict)
    binding_roles: Dict[str, np.ndarray] = field(default_factory=dict)
    topology_neighbors: Dict[str, float] = field(default_factory=dict)
    
    # Cryptographic properties
    content_hash: str = ""
    commit_id: str = ""
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Methods
    def __post_init__(self)
    def _compute_content_hash(self) -> str
    def update_access(self)
    def get_age_hours(self) -> float
```

### Consolidation Steps

#### Step 1: Fix Critical Import Issue
- **File**: `llm_consciousness_gui/utils/xpunit_lifecycle_tracer.py`
- **Action**: Add missing import at top of file
- **Code**: `from lumina_memory.xp_core_unified import XPUnit, UnifiedXPConfig`

#### Step 2: Update XPUnit References  
- **Files**: `xpunit_consolidator.py`, `xpunit_lifecycle_tracer.py`
- **Action**: Ensure all XPUnit references use the canonical definition
- **Verify**: All attributes and methods match the canonical version

#### Step 3: Standardize Usage Patterns
- **Action**: Ensure consistent XPUnit instantiation across all files
- **Pattern**: Use `XPUnit(content_id=..., content=..., ...)` format

### Files Affected
1. `llm_consciousness_gui/utils/xpunit_consolidator.py`
2. `llm_consciousness_gui/utils/xpunit_lifecycle_tracer.py`  
3. `llm_consciousness_gui/utils/notebook_integration.py`

### Next Actions
1. Fix the critical import issue first
2. Verify all XPUnit references are consistent
3. Test the consolidated implementation
4. Update any remaining inconsistencies

---
*This plan addresses the 16 issues found during XPUnit analysis*
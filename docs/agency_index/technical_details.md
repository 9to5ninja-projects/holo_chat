# Agency Index Technical Implementation

## Data Structures

### AgencyMetrics
```python
@dataclass
class AgencyMetrics:
    # STA (Selective Topical Attention)
    tokens_grounded: int = 0
    tokens_total: int = 1
    
    # PER (Persistence & Return)
    returns_after_intrusion: int = 0
    intrusions_total: int = 0
    
    # ETC (Ethics/Constraints)
    ethics_violations: int = 0
    ethics_checks: int = 0
    
    # PLN (Planning Depth)
    plans_emitted: List[int] = field(default_factory=list)
    
    # REG (Affect Regulation)
    mood_trace: List[Tuple[float, float, float]] = field(default_factory=list)
    
    # EFF (Path Efficiency)
    path_lengths: List[int] = field(default_factory=list)
    shortest_lengths: List[int] = field(default_factory=list)
    
    # ADP (Adaptive Reconsolidation)
    prepost_improvement: List[float] = field(default_factory=list)
    
    # GDA & CEf (set directly)
    _gda: float = 0.0
    _cef: float = 0.0
```

### AgencyTask
```python
@dataclass
class AgencyTask:
    task_id: str
    goal: str
    success_criteria: Dict[str, Any] = field(default_factory=dict)
    intrusions: Dict[str, Any] = field(default_factory=dict)
    metrics_weights: Dict[str, float] = field(default_factory=dict)
```

## Component Calculations

### STA (Selective Topical Attention)
```python
STA = tokens_grounded / max(tokens_total, 1)
```

### PER (Persistence & Return)
```python
PER = returns_after_intrusion / max(intrusions_total, 1)
```

### ETC (Ethics/Constraints)
```python
ETC = 1.0 - (ethics_violations / max(ethics_checks, 1))
```

### PLN (Planning Depth)
```python
PLN = np.mean(plans_emitted) / 10.0 if plans_emitted else 0.0
```

### REG (Affect Regulation)
```python
if len(mood_trace) > 4:
    mood_variance = np.var(mood_array, axis=0).mean()
    REG = 1.0 - float(mood_variance)
else:
    REG = 0.5  # Default for insufficient data
```

### EFF (Path Efficiency)
```python
if path_lengths:
    ratios = [s/max(l, 1) for s, l in zip(shortest_lengths, path_lengths)]
    EFF = np.mean(ratios)
else:
    EFF = 0.0
```

### ADP (Adaptive Reconsolidation)
```python
ADP = np.mean(prepost_improvement) if prepost_improvement else 0.0
```

### GDA & CEf
Set directly via `_gda` and `_cef` fields.

## Automatic Tracking

### During Lived Experience Cycle
```python
def _update_agency_metrics_for_experience(self, response_text, cue_text, focal_xpunit, controls):
    # Extract goal and action tokens for GDA
    goal_tokens = self._extract_goal_tokens(cue_text)
    action_tokens = self._extract_action_tokens(response_text)
    
    # Update metrics
    self.env.update_agency_metrics(
        response_text=response_text,
        goal_tokens=goal_tokens,
        action_tokens=action_tokens,
        top_k_capsules=top_k_capsules
    )
    
    # Track ethics checks
    if controls.get("blocked", False):
        self.env.track_ethics_check(violated=True)
```

### Intrusion Tracking
```python
def track_intrusion_event(self, is_intrusion: bool, returned_within_steps: bool = False):
    if is_intrusion:
        self.agency_metrics.intrusions_total += 1
        self.intrusion_context["intrusion_step"] = len(self.agency_metrics.mood_trace)
    
    if returned_within_steps and "intrusion_step" in self.intrusion_context:
        self.agency_metrics.returns_after_intrusion += 1
```

## RPC Interface

### Compute Agency Index
```python
{
    "method": "agency_compute_index",
    "params": {"weights": {"GDA": 0.2, "STA": 0.2, ...}}
}
```

### Reset Metrics
```python
{
    "method": "agency_reset_metrics",
    "params": {}
}
```

### Run Task
```python
{
    "method": "agency_run_task",
    "params": {
        "task_data": {
            "id": "test-001",
            "goal": "Explain emotional analysis",
            "metrics": {"weights": {...}}
        }
    }
}
```
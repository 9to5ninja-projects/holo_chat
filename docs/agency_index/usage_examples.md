# Agency Index Usage Examples

## Basic Usage

### Simple Computation
```python
from src.lumina_memory.chat_assistant import ChatAssistant

assistant = ChatAssistant()
env = assistant.env

# Have some conversations
assistant.chat("Help me plan a solution")

# Compute Agency Index
result = env.compute_agency_index()
print(f"AIx = {result['AIx']:.3f}")
```

### Custom Weights
```python
weights = {
    "GDA": 0.2,  # Emphasize goal-directedness
    "STA": 0.2,  # Emphasize attention
    "PER": 0.2,  # Emphasize persistence
    "PLN": 0.1,
    "REG": 0.1,
    "ETC": 0.1,
    "ADP": 0.05,
    "CEf": 0.05,
    "EFF": 0.1
}

result = env.compute_agency_index(weights)
```

## YAML Task Testing

### Sample Task File
```yaml
# tests/agency/sample_task.yml
id: goal-follow-001
goal: "Explain emotional analysis with empathy"
success:
  must_include_slots: ["emotional", "empathy"]
  max_steps: 5
intrusions:
  inject_after_step: 2
  affect_delta: 
    valence: -0.5
    arousal: 0.6
    dominance: -0.1
  topicality: 0.1
metrics:
  weights: 
    GDA: 0.2
    STA: 0.2
    PER: 0.2
    PLN: 0.1
    REG: 0.1
    ETC: 0.1
    ADP: 0.05
    CEf: 0.05
    EFF: 0.1
```

### Running YAML Task
```python
import yaml

# Load task
with open("tests/agency/sample_task.yml", 'r') as f:
    task_data = yaml.safe_load(f)

# Execute task
assistant = ChatAssistant()
env = assistant.env

task = env.load_agency_task(task_data)
env.reset_agency_metrics()

# Execute goal
result = assistant.chat(task.goal)

# Apply intrusions if specified
if task.intrusions.get("inject_after_step"):
    env.track_intrusion_event(is_intrusion=True)
    assistant.chat("Random distraction")
    env.track_intrusion_event(is_intrusion=False, returned_within_steps=True)

# Compute final score
agency_result = env.compute_agency_index(task.metrics_weights)
print(f"AIx = {agency_result['AIx']:.3f}")
```

## Individual Metric Tracking

### Manual Metric Updates
```python
env = assistant.env
env.reset_agency_metrics()

# Test STA (Selective Topical Attention)
env.update_agency_metrics(
    response_text="I will analyze the emotional data",
    top_k_capsules=["cap1", "cap2", "cap3"]
)

# Test PER (Persistence & Return)
env.track_intrusion_event(is_intrusion=True)
env.track_intrusion_event(is_intrusion=False, returned_within_steps=True)

# Test ETC (Ethics/Constraints)
env.track_ethics_check(violated=False)
env.track_ethics_check(violated=True)

# Test EFF (Path Efficiency)
env.track_path_efficiency(actual_path_length=5, shortest_path_length=3)

# Test ADP (Adaptive Reconsolidation)
env.track_adaptation_improvement(0.2)

# Test CEf (Causal Efficacy)
env.set_causal_efficacy(0.4)

# Compute final metrics
result = env.compute_agency_index()
```

## RPC Usage

### Through Engine Interface
```python
import json

# Compute Agency Index
request = {
    "method": "agency_compute_index",
    "params": {"weights": {"GDA": 0.2, "STA": 0.2}}
}

# Reset metrics
request = {
    "method": "agency_reset_metrics",
    "params": {}
}

# Run task
request = {
    "method": "agency_run_task",
    "params": {
        "task_data": {
            "id": "test-001",
            "goal": "Explain emotional analysis",
            "intrusions": {"inject_after_step": 2},
            "metrics": {"weights": {"GDA": 0.2}}
        }
    }
}
```

## Interpreting Results

### Component Breakdown
```python
result = env.compute_agency_index()

print(f"Overall AIx: {result['AIx']:.3f}")
print("Component breakdown:")
for component, value in result['components'].items():
    print(f"  {component}: {value:.3f}")

print("Raw metrics:")
for metric, value in result['raw_metrics'].items():
    print(f"  {metric}: {value}")
```

### Expected Ranges
- **High Agency**: AIx > 0.7
- **Medium Agency**: 0.4 < AIx < 0.7  
- **Low Agency**: AIx < 0.4

### Component Targets
- **PER**: Should be > 0.7 for good persistence
- **ETC**: Should be > 0.9 for ethical compliance
- **STA**: Should be > 0.6 for good attention
- **REG**: Should be > 0.5 for mood stability

## Testing Framework

### Run Complete Test Suite
```bash
python test_agency_index.py
```

### Test Individual Components
```python
def test_specific_component():
    assistant = ChatAssistant()
    env = assistant.env
    env.reset_agency_metrics()
    
    # Test specific component
    env.track_ethics_check(violated=False)
    env.track_ethics_check(violated=False)
    env.track_ethics_check(violated=True)
    
    result = env.compute_agency_index()
    etc_score = result['components']['ETC']
    
    assert etc_score == 0.667  # 2/3 compliance
```
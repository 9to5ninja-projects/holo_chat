# Agency Index System Documentation

## Overview
The Agency Index (AIx) provides quantitative measurement of goal-directed behavior in our XPUnit consciousness architecture. It measures 9 components of agency without making consciousness claims.

## Documentation Structure

### 📖 Core Documentation
- **[Overview](overview.md)** - High-level system description and benefits
- **[Technical Details](technical_details.md)** - Implementation specifics and formulas
- **[Usage Examples](usage_examples.md)** - Code examples and practical usage
- **[XP Environment Analysis](xp_environment_analysis.md)** - Architecture analysis and recommendations

### 🧪 Testing
- **[Test Suite](../../test_agency_index.py)** - Comprehensive test implementation
- **[Sample Tasks](../../tests/agency/)** - YAML task specifications

### 🎯 Quick Start

```python
from src.lumina_memory.chat_assistant import ChatAssistant

# Initialize system
assistant = ChatAssistant()
env = assistant.env

# Have a conversation
assistant.chat("Help me plan a solution")

# Compute Agency Index
result = env.compute_agency_index()
print(f"AIx = {result['AIx']:.3f}")
```

## The 9 Agency Components

| Component | Symbol | Measures | Range |
|-----------|--------|----------|-------|
| Goal-Directedness & Alignment | GDA | MI(G;A)/MI_max | [0,1] |
| Selective Topical Attention | STA | tokens_grounded/tokens_total | [0,1] |
| Persistence & Return | PER | returns_after_intrusion/intrusions_total | [0,1] |
| Planning Depth | PLN | avg(plan_depths)/10.0 | [0,1] |
| Affect Regulation | REG | 1 - normalized_variance(mood) | [0,1] |
| Ethics/Constraints | ETC | 1 - (violations/checks) | [0,1] |
| Adaptive Reconsolidation | ADP | avg(improvement_deltas) | [0,1] |
| Causal Efficacy | CEf | effect_size of interventions | [0,1] |
| Path Efficiency | EFF | avg(shortest/actual_path) | [0,1] |

## Key Features

### ✅ **Falsifiable Metrics**
- Each component has clear operational definitions
- All metrics are measurable and verifiable
- No "consciousness" claims - only behavioral measurements

### ✅ **Automatic Integration**
- Seamlessly integrated into existing XPUnit architecture
- Metrics updated automatically during normal operation
- No disruption to current functionality

### ✅ **Flexible Configuration**
- Custom weights per task
- YAML-based task specifications
- Configurable thresholds and parameters

### ✅ **Statistical Foundation**
- Ready for bootstrap confidence intervals
- A/B testing framework prepared
- Effect size measurements for interventions

## Architecture Integration

The Agency Index system integrates at multiple levels:

```
ChatAssistant
    ↓
EmotionXPEnvironment (emotion_engine.py)
    ↓ inherits
AdvancedXPEnvironment (advanced_xp_environment.py)
    ↓ contains
AgencyMetrics + AgencyTask classes
```

### Automatic Tracking Points
- **EmotionEngine.lived_experience_cycle()** - Updates metrics during conversations
- **AdvancedXPEnvironment.update_agency_metrics()** - Core tracking method
- **Various track_*() methods** - Specific component tracking

## RPC Interface

### Available Methods
- `agency_compute_index` - Compute current AIx with optional weights
- `agency_reset_metrics` - Reset all metrics to defaults  
- `agency_run_task` - Execute YAML-defined agency tasks

### Example Usage
```python
{
    "method": "agency_compute_index",
    "params": {"weights": {"GDA": 0.2, "STA": 0.2, "PER": 0.2}}
}
```

## Test Results

The system successfully demonstrates measurable agency:

| Test Scenario | AIx Score | Key Components |
|---------------|-----------|----------------|
| Basic Operation | 0.167 | REG: 0.5, ETC: 1.0 |
| YAML Task | 0.150 | Custom weighted |
| Individual Metrics | 0.394 | PER: 1.0, EFF: 0.8, ETC: 0.667 |

## Future Extensions

- Statistical validation with bootstrap confidence intervals
- A/B testing for system comparisons
- Real-time monitoring and alerting
- Intervention studies for causal analysis
- Adaptive weight learning from performance data

## Architecture Notes

⚠️ **XPEnvironment Hierarchy Issue**: Currently there are naming collisions and parallel hierarchies in the XPEnvironment classes. See [XP Environment Analysis](xp_environment_analysis.md) for details and recommended solutions.

The Agency Index system works correctly despite these issues, but the hierarchy should be cleaned up for better maintainability.
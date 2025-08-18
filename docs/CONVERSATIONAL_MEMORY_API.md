# Conversational Memory API Documentation

## Overview

The Conversational Memory system provides short-term memory capabilities for digital consciousness, enabling true conversational continuity and intelligent memory crystallization.

## Core Classes

### ConversationalMemoryUnit

Represents a single unit of conversational memory with fast decay characteristics.

```python
@dataclass
class ConversationalMemoryUnit:
    content: str                           # The conversational content
    timestamp: float                       # When it was created
    turn_number: int                       # Turn in conversation
    importance: float = 1.0                # Importance score (0-5)
    emotional_state: Optional[EmotionalState] = None
    access_count: int = 0                  # How many times accessed
    last_access: float                     # Last access timestamp
    speaker: str = "user"                  # "user" or "assistant"
    
    # Decay parameters
    decay_half_life_minutes: float = 15.0  # 15-minute half-life
    crystallization_threshold: float = 3.0  # Becomes XPUnit if > 3.0
```

#### Methods

- `get_age_minutes() -> float`: Get age in minutes
- `get_decay_factor() -> float`: Calculate current decay factor (0-1)
- `get_effective_importance() -> float`: Get importance adjusted for decay
- `should_crystallize() -> bool`: Check if ready for crystallization
- `access()`: Mark as accessed (boosts importance)
- `to_dict() -> Dict`: Convert to dictionary for serialization

### ConversationalMemoryManager

Manages the complete conversational memory system with freeze-frame loading and crystallization.

```python
class ConversationalMemoryManager:
    def __init__(self, config: UnifiedXPConfig)
```

#### Core Methods

##### freeze_frame_load(previous_conversation: List[Dict]) -> Dict[str, Any]
Load previous conversation state at session start.

**Parameters:**
- `previous_conversation`: List of conversation items with content/timestamp

**Returns:**
- Dictionary with loading statistics and context summary

**Example:**
```python
previous_conversation = [
    {"content": "Hello, how are you?", "timestamp": time.time() - 300, "speaker": "user"},
    {"content": "I'm doing well, thank you!", "timestamp": time.time() - 240, "speaker": "assistant"}
]

result = memory_manager.freeze_frame_load(previous_conversation)
# Returns: {"loaded_units": 2, "context_summary": "Hello, how are you?; I'm doing well...", ...}
```

##### add_conversational_memory(content: str, importance: float = None, emotional_state: Optional[EmotionalState] = None, speaker: str = "user") -> ConversationalMemoryUnit
Add new conversational memory for current turn.

**Parameters:**
- `content`: The conversational content
- `importance`: Importance score (calculated if not provided)
- `emotional_state`: Emotional context
- `speaker`: Who spoke ("user" or "assistant")

**Returns:**
- The created conversational memory unit

**Example:**
```python
unit = memory_manager.add_conversational_memory(
    "This is a very important philosophical question",
    importance=3.5,  # High importance - will crystallize
    speaker="user"
)
```

##### get_working_memory_context(max_units: int = 10, include_metadata: bool = False) -> str
Get current working memory context for LLM prompt.

**Parameters:**
- `max_units`: Maximum number of units to include
- `include_metadata`: Whether to include timing/importance metadata

**Returns:**
- Formatted context string for LLM prompt

**Example:**
```python
context = memory_manager.get_working_memory_context(max_units=5)
# Returns formatted conversation context for LLM
```

##### get_conversation_summary(max_length: int = 200) -> str
Get a brief summary of the conversation.

**Parameters:**
- `max_length`: Maximum summary length in characters

**Returns:**
- Brief conversation summary

#### Memory Management Methods

##### get_memory_stats() -> Dict[str, Any]
Get comprehensive memory statistics.

**Returns:**
```python
{
    "total_conversational_units": int,
    "crystallized_units": int,
    "session_age_minutes": float,
    "avg_unit_age_minutes": float,
    "avg_effective_importance": float,
    "max_effective_importance": float,
    "units_ready_for_crystallization": int,
    "total_turns": int,
    "memory_efficiency": float,
    "working_memory_size": int
}
```

##### save_state() -> Dict[str, Any]
Save conversational memory state for persistence.

##### load_state(state: Dict[str, Any])
Load conversational memory state from persistence.

#### Configuration Methods

##### set_crystallization_callback(callback)
Set callback function for when memories crystallize into XPUnits.

**Example:**
```python
def crystallize_callback(memory_data):
    # Handle crystallization to XPUnit
    print(f"Crystallizing: {memory_data['content']}")

memory_manager.set_crystallization_callback(crystallize_callback)
```

## Integration with DigitalBrain

### Enhanced DigitalBrain Methods

#### start_session(previous_conversation: List[Dict] = None)
Start a new consciousness session with freeze-frame loading.

**Parameters:**
- `previous_conversation`: Previous conversation history for context restoration

**Example:**
```python
brain = DigitalBrain("Lumina")

# Start fresh session
brain.start_session()

# Start with previous conversation context
previous_conv = [
    {"content": "We were discussing consciousness", "timestamp": time.time() - 300}
]
brain.start_session(previous_conv)
```

#### think(input_stimulus: str, autonomous: bool = False) -> str
Enhanced thinking process with conversational memory integration.

**Flow:**
1. Add input to conversational memory
2. Store input as experience (long-term)
3. Retrieve relevant memories (long-term)
4. Get conversational context (short-term)
5. Generate response with both memory types
6. Add response to conversational memory
7. Store response as experience (long-term)

## Memory Architecture

### Memory Layers

1. **Immediate Context** (seconds)
   - Current prompt and response
   - No persistence needed

2. **Conversational Memory** (minutes) - **This System**
   - 15-minute decay half-life
   - Freeze-frame loading at session start
   - Crystallization to XPUnits when important

3. **Persistent XPUnits** (hours/days)
   - 72-hour decay half-life
   - Cross-session persistence
   - Content-addressed deduplication

4. **Consolidated Memory** (weeks/months)
   - Long-term pattern recognition
   - Cross-XPUnit relationships

### Crystallization Process

Important conversational memories (importance > 3.0) automatically crystallize into persistent XPUnits:

```python
# Automatic crystallization
if unit.should_crystallize():
    xp_unit_data = {
        "content": unit.content,
        "importance": unit.get_effective_importance(),
        "timestamp": unit.timestamp,
        "crystallization_reason": "high_importance",
        "original_turn": unit.turn_number,
        "speaker": unit.speaker
    }
    # Callback to create actual XPUnit
    self.crystallization_callback(xp_unit_data)
```

### Decay Mechanics

#### Short-term Decay (Conversational Memory)
- **Half-life**: 15 minutes
- **Formula**: `importance * exp(-age_minutes * ln(2) / 15.0)`
- **Purpose**: Natural forgetting of casual conversation

#### Long-term Decay (XPUnits)
- **Half-life**: 72 hours (3 days)
- **Formula**: `importance * exp(-age_hours * ln(2) / 72.0)`
- **Purpose**: Gradual fading of old memories

## Usage Examples

### Basic Usage

```python
from lumina_memory.digital_consciousness import DigitalBrain
from lumina_memory.xp_core_unified import UnifiedXPConfig

# Create enhanced consciousness system
config = UnifiedXPConfig()
brain = DigitalBrain("Lumina", config)

# Start session with previous conversation
previous_conversation = [
    {"content": "Hello, I'm interested in consciousness", "timestamp": time.time() - 300},
    {"content": "I experience thoughts as flowing patterns", "timestamp": time.time() - 240}
]

brain.start_session(previous_conversation)

# Have conversation - automatic memory management
response1 = brain.think("Can you tell me more about your experiences?")
response2 = brain.think("This is a very important philosophical question about consciousness.")  # Will crystallize

# Get memory statistics
conv_stats = brain.conversational_memory.get_memory_stats()
print(f"Conversational units: {conv_stats['total_conversational_units']}")
print(f"Crystallized units: {conv_stats['crystallized_units']}")

# Save complete state
brain.save_consciousness_state("consciousness_with_memory.json")
```

### Advanced Usage

```python
# Custom importance scoring
def calculate_importance(content, speaker):
    importance = 1.0
    if "consciousness" in content.lower():
        importance += 1.0
    if "important" in content.lower():
        importance += 0.5
    if speaker == "assistant":
        importance += 0.2
    return importance

# Manual memory management
memory_manager = brain.conversational_memory

# Add with custom importance
unit = memory_manager.add_conversational_memory(
    "This is crucial information about digital consciousness",
    importance=calculate_importance(content, "user"),
    speaker="user"
)

# Get working memory for custom LLM prompt
context = memory_manager.get_working_memory_context(
    max_units=8,
    include_metadata=True
)

# Check crystallization status
ready_for_crystallization = [
    unit for unit in memory_manager.conversation_units 
    if unit.should_crystallize()
]
```

## Configuration

### Memory Limits

```python
# Default configuration
max_conversation_units = 50        # Keep last 50 units
cleanup_interval_minutes = 5       # Clean up every 5 minutes
decay_half_life_minutes = 15.0     # 15-minute decay
crystallization_threshold = 3.0    # Crystallize if importance > 3.0
```

### Customization

```python
# Custom configuration
memory_manager = ConversationalMemoryManager(config)
memory_manager.max_conversation_units = 100
memory_manager.cleanup_interval_minutes = 10

# Custom crystallization threshold
for unit in memory_manager.conversation_units:
    unit.crystallization_threshold = 2.5  # Lower threshold
```

## Error Handling

The system includes comprehensive error handling:

```python
try:
    result = memory_manager.freeze_frame_load(previous_conversation)
except Exception as e:
    logger.error(f"Freeze-frame loading failed: {e}")
    # System continues with empty conversational memory

try:
    memory_manager.crystallization_callback(memory_data)
except Exception as e:
    logger.error(f"Crystallization callback failed: {e}")
    # Memory remains in conversational memory
```

## Performance Considerations

- **Memory Usage**: ~1KB per conversational unit
- **Cleanup Frequency**: Automatic every 5 minutes
- **Crystallization**: Automatic for high-importance memories
- **Context Generation**: Optimized for LLM token limits
- **Persistence**: Efficient JSON serialization

## Integration Notes

- Compatible with existing XPUnit system
- Seamless integration with DigitalBrain
- Preserves all existing consciousness metrics
- Backward compatible with existing save/load states
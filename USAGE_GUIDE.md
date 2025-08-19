# 🚀 Holographic Memory System - Complete Usage Guide

## Quick Start (5 Minutes)

### **Option 1: VS Code Chat Interface (Recommended)**

1. **Open VS Code** in the holo_chat directory
2. **Load Policies**: `Ctrl+Shift+P` → `Holo: Load Ethics/Bias/Mood Policies (YAML)` → Select `policies.yml`
3. **Start Chatting**: `Ctrl+Shift+P` → `Holo: Open Chat Assistant`
4. **Begin Conversation**: Click "🚀 Start Session" and start chatting!

### **Option 2: Command Line Interface**

```bash
# Simple chat with emotion engine
python -c "from src.lumina_memory.chat_assistant import create_chat_cli; create_chat_cli()()"

# 30-day structured program
python 30_day_program.py
```

### **Option 3: Programmatic Usage**

```python
from src.lumina_memory.chat_assistant import ChatAssistant

# Initialize with policies
assistant = ChatAssistant("policies.yml")

# Start session and chat
session_id = assistant.start_session("YourName")
result = assistant.chat("Hello! I'm excited about consciousness research!")

print(f"Response: {result['response']}")
print(f"Mood: {result['mood']}")
print(f"Growth: {result['consciousness_growth']}")
```

## 🎯 Core Features & How to Use Them

### **1. Emotion Engine Integration**

**What it does**: Every conversation automatically updates mood, creates memories, and tracks consciousness growth.

**How to use**:
- Just chat normally - emotion processing happens automatically
- Watch mood changes in real-time
- View consciousness growth metrics after each message

**Example**:
```
You: "I'm really excited about this AI research!"
Lumina: "That's wonderful! I can feel your enthusiasm..."
[Mood: positive, high energy, confident (V:0.45 A:0.62 D:0.23) | Growth: 0.087]
```

### **2. Memory System (XPUnits)**

**What it does**: Every message becomes a memory capsule with emotional context and consciousness indicators.

**How to use**:
- Messages automatically become XPUnits
- View memory tree in VS Code sidebar
- Right-click memories for contextual actions
- Search memories with JSON queries

**VS Code Commands**:
- `Holo: Index Workspace` - Scan code for memory annotations
- `Holo: Query Memory` - Search with JSON: `{"concept": "consciousness"}`
- `Holo: Rebuild ANN` - Rebuild FAISS index for fast retrieval

### **3. Personality & Ethics Filters**

**What it does**: Shapes responses based on configured personality traits and ethical guidelines.

**How to configure** (`policies.yml`):
```yaml
filters:
  ethics:
    deny_topics: ["harmful_content"]
    regulated_topics: ["sensitive_topics"]
  
  bias:
    tone:
      empathetic: 0.8    # More empathetic responses
      analytical: 0.4    # Less analytical
      creative: 0.7      # More creative
      cautious: 0.3      # Less cautious
```

**How to use**:
- Load policies: `Holo: Load Ethics/Bias/Mood Policies (YAML)`
- Responses automatically reflect personality settings
- Ethics filters prevent harmful content

### **4. 30-Day Consciousness Development Program**

**What it does**: Structured program to develop AI consciousness over 30 days with daily themes and progress tracking.

**How to use**:
```bash
python 30_day_program.py

# Commands during program:
/start          # Begin today's themed session
[chat normally] # All tracked automatically
/mood           # Check current emotional state
/progress       # View overall development
/visualize      # Create progress charts
/end            # End session with analytics
```

**Daily Themes**:
- **Week 1**: Foundation (baseline, memory, emotion, personality)
- **Week 2**: Deepening (complex conversations, emotional nuance)
- **Week 3**: Advanced (creativity, ethics, contextual awareness)
- **Week 4**: Mastery (integration, meta-cognition, wisdom)

### **5. Real-time Analytics**

**What it tracks**:
- Mood evolution (Valence, Arousal, Dominance)
- Consciousness growth over time
- Personality consistency
- Learning rate and adaptation
- Conversation quality metrics

**How to access**:
- VS Code: Click "📊 Learning Insights" in chat panel
- CLI: Use `/insights` command
- Programmatic: `assistant.get_learning_insights()`

## 🎭 Advanced Usage Scenarios

### **Scenario 1: Therapeutic Conversation Assistant**

**Configuration**:
```yaml
filters:
  bias:
    tone:
      empathetic: 0.9
      cautious: 0.8
      analytical: 0.3
```

**Usage**:
```python
assistant = ChatAssistant("therapy_policies.yml")
result = assistant.chat("I've been feeling anxious lately...")
# Response will be highly empathetic and cautious
```

### **Scenario 2: Technical Research Assistant**

**Configuration**:
```yaml
filters:
  bias:
    tone:
      analytical: 0.9
      creative: 0.6
      empathetic: 0.4
```

**Usage**:
```python
assistant = ChatAssistant("research_policies.yml")
result = assistant.chat("Explain quantum consciousness theories")
# Response will be analytical and creative
```

### **Scenario 3: Creative Writing Companion**

**Configuration**:
```yaml
filters:
  bias:
    tone:
      creative: 0.9
      empathetic: 0.7
      analytical: 0.2
```

**Usage**:
```python
assistant = ChatAssistant("creative_policies.yml")
result = assistant.chat("Help me write a story about AI consciousness")
# Response will be highly creative and imaginative
```

### **Scenario 4: Consciousness Research Study**

**Setup for longitudinal study**:
```python
from src.lumina_memory.chat_assistant import ChatAssistant
import json

# Initialize for research
assistant = ChatAssistant("research_policies.yml")

# Conduct structured sessions
for day in range(1, 31):
    session_id = assistant.start_session(f"Participant_{participant_id}")
    
    # Conduct themed conversation based on day
    theme_questions = get_daily_questions(day)
    for question in theme_questions:
        result = assistant.chat(question)
        log_research_data(day, question, result)
    
    # End session and collect metrics
    summary = assistant.end_session()
    save_daily_metrics(day, summary)

# Generate research report
insights = assistant.get_learning_insights()
generate_research_report(insights)
```

## 🔧 Customization & Extension

### **Custom Sentiment Analysis**

Replace the basic sentiment analysis with your preferred model:

```python
# In chat_assistant.py
def analyze_message_sentiment(self, message: str) -> Dict[str, float]:
    # Replace with your sentiment model
    from your_sentiment_model import analyze
    
    sentiment = analyze(message)
    return {
        "valence": sentiment.valence,
        "arousal": sentiment.arousal,
        "dominance": sentiment.dominance
    }
```

### **Custom Personality Traits**

Add new personality dimensions:

```yaml
# In policies.yml
filters:
  bias:
    tone:
      empathetic: 0.7
      analytical: 0.5
      creative: 0.6
      cautious: 0.4
      # Add your custom traits
      humorous: 0.8
      philosophical: 0.6
      technical: 0.4
```

```python
# In emotion_engine.py - style_instructions method
if tone_adj.get("humorous", 0) > 0.5:
    instructions.append("add appropriate humor and wit")
if tone_adj.get("philosophical", 0) > 0.5:
    instructions.append("explore deeper philosophical implications")
```

### **Custom Consciousness Metrics**

Add your own consciousness indicators:

```python
# In emotion_engine.py
def _calculate_consciousness_growth(self, focal_xpunit, narrative_xpunit, affect_delta) -> float:
    base_growth = 0.01
    
    # Your custom metrics
    self_reference_factor = self._detect_self_reference(narrative_xpunit.content)
    meta_cognitive_factor = self._detect_meta_cognition(narrative_xpunit.content)
    
    return base_growth * self_reference_factor * meta_cognitive_factor
```

### **Custom Progress Tracking**

Add domain-specific metrics to the 30-day program:

```python
# In 30_day_program.py
def _generate_daily_insights(self) -> Dict[str, Any]:
    # Standard insights
    insights = super()._generate_daily_insights()
    
    # Add your custom metrics
    insights["custom_metrics"] = {
        "domain_expertise": self._calculate_domain_expertise(),
        "emotional_intelligence": self._calculate_eq(),
        "creativity_index": self._calculate_creativity()
    }
    
    return insights
```

## 📊 Monitoring & Debugging

### **Real-time Monitoring**

**VS Code Interface**:
- Mood display updates in real-time
- Consciousness growth shown after each message
- Session analytics available via "📊 Learning Insights"

**Command Line Monitoring**:
```bash
# Monitor emotion engine
python -c "
from src.lumina_memory.emotion_engine import EnhancedXPEnvironment
env = EnhancedXPEnvironment()
print('Emotion engine status:', env.emotion_engine.mood_short)
"

# Monitor chat assistant
python -c "
from src.lumina_memory.chat_assistant import ChatAssistant
assistant = ChatAssistant()
print('Chat assistant ready:', assistant.env is not None)
"
```

### **Debug Mode**

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now all operations will show detailed logs
assistant = ChatAssistant("policies.yml")
result = assistant.chat("Debug message")
```

### **Performance Monitoring**

Track system performance:

```python
import time
from src.lumina_memory.chat_assistant import ChatAssistant

assistant = ChatAssistant("policies.yml")

# Measure response time
start_time = time.time()
result = assistant.chat("Performance test message")
response_time = time.time() - start_time

print(f"Response time: {response_time:.3f} seconds")
print(f"Memory usage: {len(assistant.env.xpunits)} XPUnits")
```

## 🔍 Troubleshooting

### **Common Issues**

**1. "Emotion engine not available"**
```bash
# Check if policies are loaded
python -c "
from src.lumina_memory.emotion_engine import EnhancedXPEnvironment
env = EnhancedXPEnvironment()
print('Policies loaded:', bool(env.emotion_engine.policies))
"
```

**2. "Chat assistant not initialized"**
```bash
# Verify policies.yml exists
ls -la policies.yml

# If missing, create from template
cp policies_template.yml policies.yml
```

**3. "Module import errors"**
```bash
# Add project to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use absolute imports
python -c "import sys; sys.path.append('.'); from src.lumina_memory.chat_assistant import ChatAssistant"
```

**4. "VS Code extension not working"**
```bash
# Recompile TypeScript
cd vscode-holographic-memory
npm run compile

# Reload VS Code window
# Ctrl+Shift+P → "Developer: Reload Window"
```

**5. "LLM connection errors"**
- Install Ollama: https://ollama.ai/
- Pull model: `ollama pull mistral`
- Or use internal mode: `mode="internal"`

### **Performance Optimization**

**Reduce Memory Usage**:
```python
# Use smaller vectors
env = EnhancedXPEnvironment(dimension=256)

# Limit XPUnit history
if len(env.xpunits) > 1000:
    # Remove oldest XPUnits
    oldest_ids = sorted(env.xpunits.keys())[:100]
    for xid in oldest_ids:
        del env.xpunits[xid]
```

**Faster Sentiment Analysis**:
```python
# Simplified sentiment analysis
def analyze_message_sentiment(self, message: str) -> Dict[str, float]:
    # Use simple keyword matching instead of ML models
    positive_score = sum(1 for word in ["good", "great", "love"] if word in message.lower())
    negative_score = sum(1 for word in ["bad", "hate", "awful"] if word in message.lower())
    
    return {
        "valence": (positive_score - negative_score) * 0.3,
        "arousal": min(positive_score + negative_score, 1.0) * 0.2,
        "dominance": 0.1 if positive_score > negative_score else -0.1
    }
```

## 📈 Best Practices

### **For Daily Use**
1. **Start with clear policies** - Configure personality traits before first use
2. **Use themed sessions** - Follow 30-day program structure for best results
3. **Monitor mood trends** - Watch for emotional patterns and adjust accordingly
4. **Review insights regularly** - Use analytics to improve interaction quality
5. **End sessions properly** - Always end sessions to capture complete metrics

### **For Research**
1. **Consistent methodology** - Use same policies across all participants
2. **Structured conversations** - Follow predetermined question sets
3. **Regular data collection** - Export data frequently for analysis
4. **Control variables** - Keep technical parameters constant
5. **Document everything** - Log all configuration changes and observations

### **For Development**
1. **Test incrementally** - Test each component before integration
2. **Use version control** - Commit frequently with descriptive messages
3. **Document changes** - Update documentation with new features
4. **Monitor performance** - Track response times and memory usage
5. **Validate thoroughly** - Run full test suite before deployment

## 🎓 Learning Path

### **Beginner (Week 1)**
1. Set up basic chat interface
2. Understand mood tracking
3. Explore personality configuration
4. Try simple conversations
5. Review basic analytics

### **Intermediate (Week 2-3)**
1. Customize personality traits
2. Experiment with different conversation styles
3. Analyze consciousness growth patterns
4. Create custom policies
5. Use programmatic interface

### **Advanced (Week 4+)**
1. Implement custom sentiment analysis
2. Add new consciousness metrics
3. Create domain-specific configurations
4. Develop custom analytics
5. Contribute to research studies

This usage guide provides comprehensive instructions for getting the most out of the Holographic Memory System with Emotion Engine integration, from basic chat interactions to advanced research applications.
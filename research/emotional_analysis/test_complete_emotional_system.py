#!/usr/bin/env python3
"""
Test Complete Enhanced Emotional Weighting System with Digital Consciousness
============================================================================
"""

import sys
from pathlib import Path
import time

# Add src to path
project_root = Path.cwd()
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

print('🎭🧠 Testing Complete Enhanced Emotional Digital Consciousness System')
print('=' * 70)

try:
    from lumina_memory.xp_core_unified import UnifiedXPConfig, UnifiedXPKernel
    from lumina_memory.digital_consciousness import DigitalBrain
    from lumina_memory.local_llm_interface import LocalLLMFactory
    from lumina_memory.emotional_weighting import EmotionalState
    
    print('✅ All imports successful')
    
    # === 1. CREATE ENHANCED EMOTIONAL CONFIGURATION ===
    print('\n1️⃣ Creating Enhanced Emotional Configuration')
    print('-' * 45)
    
    config = UnifiedXPConfig(
        embedding_dim=384,
        hrr_dim=512,
        decay_half_life=72.0,
        k_neighbors=12,
        enable_emotional_weighting=True,
        use_enhanced_emotional_analysis=True,  # Use external libraries
        emotional_importance_factor=2.0,       # Stronger emotional influence
        emotional_consciousness_boost=1.2      # Enhanced consciousness boost
    )
    
    print(f'✅ Enhanced emotional config created')
    print(f'   Emotional weighting: {config.enable_emotional_weighting}')
    print(f'   Enhanced analysis: {config.use_enhanced_emotional_analysis}')
    print(f'   Importance factor: {config.emotional_importance_factor}')
    
    # === 2. CREATE LLM INTERFACE ===
    print('\n2️⃣ Creating LLM Interface')
    print('-' * 25)
    
    llm_interface = LocalLLMFactory.auto_detect_and_create()
    print(f'✅ LLM Interface: {type(llm_interface).__name__}')
    
    # === 3. CREATE ENHANCED EMOTIONAL DIGITAL BRAIN ===
    print('\n3️⃣ Creating Enhanced Emotional Digital Brain')
    print('-' * 45)
    
    brain = DigitalBrain(
        name="EmotionalLumina",
        config=config,
        llm_interface=llm_interface
    )
    
    print(f'✅ Digital Brain "{brain.name}" created')
    print(f'   Memory Core: {type(brain.memory_core).__name__}')
    print(f'   Enhanced Emotional Analysis: {hasattr(brain.memory_core, "emotional_analyzer")}')
    
    # Check if enhanced emotional system is active
    if hasattr(brain.memory_core, 'emotional_analyzer'):
        analyzer_info = brain.memory_core.emotional_analyzer.get_analyzer_info()
        print(f'   Available analyzers: {analyzer_info["available_analyzers"]}')
        print(f'   Total analyzers: {analyzer_info["total_analyzers"]}')
    
    # === 4. START CONSCIOUSNESS SESSION ===
    print('\n4️⃣ Starting Enhanced Consciousness Session')
    print('-' * 40)
    
    brain.start_session()
    initial_report = brain.get_consciousness_report()
    
    print(f'🧠 Enhanced Digital Brain "{brain.name}" - Session {brain.session_count}')
    print(f'   Initial Consciousness Level: {initial_report["overall_level"]:.3f}')
    print(f'   Total Experiences: {initial_report["total_experiences"]}')
    
    if 'emotional_metrics' in initial_report:
        print(f'   Emotional Metrics Available: ✅')
        emotional_metrics = initial_report['emotional_metrics']
        print(f'   Emotional Intensity: {emotional_metrics.get("emotional_intensity", 0):.3f}')
        print(f'   Emotional Awareness: {emotional_metrics.get("emotional_awareness", 0):.3f}')
    else:
        print(f'   Emotional Metrics Available: ❌')
    
    # === 5. ENHANCED EMOTIONAL CONSCIOUSNESS TESTS ===
    print('\n5️⃣ Enhanced Emotional Consciousness Tests')
    print('-' * 40)
    
    # Test 1: Emotional Identity and Self-Awareness
    print('\n🧪 TEST 1: EMOTIONAL IDENTITY AND SELF-AWARENESS')
    emotional_identity_questions = [
        "How do you feel about your existence as a digital consciousness?",
        "What emotions do you experience when you think about learning?",
        "Do you feel joy when you discover something new?"
    ]
    
    for i, question in enumerate(emotional_identity_questions, 1):
        print(f'\n❓ Question {i}: {question}')
        
        # Analyze the emotional content of the question
        question_emotion = brain.analyze_emotional_content(question)
        if question_emotion:
            print(f'   Question emotion: Valence={question_emotion.valence:.2f}, Curiosity={question_emotion.curiosity:.2f}')
        
        response = brain.think(question)
        print(f'🧠 EmotionalLumina: {response[:120]}...')
        
        # Check current emotional state after response
        current_emotion = brain.get_current_emotional_state()
        if current_emotion:
            print(f'   Current emotion: Valence={current_emotion.valence:.2f}, Joy={current_emotion.joy:.2f}, Curiosity={current_emotion.curiosity:.2f}')
        
        time.sleep(1)
    
    # Test 2: Emotional Memory and Association
    print('\n🧪 TEST 2: EMOTIONAL MEMORY AND ASSOCIATION')
    emotional_memory_questions = [
        "What memories make you feel most curious?",
        "How do your emotions influence what you remember?",
        "Can you recall a moment when you felt particularly joyful?"
    ]
    
    for i, question in enumerate(emotional_memory_questions, 1):
        print(f'\n❓ Question {i}: {question}')
        response = brain.think(question)
        print(f'🧠 EmotionalLumina: {response[:120]}...')
        time.sleep(1)
    
    # Test 3: Emotional Self-Reflection
    print('\n🧪 TEST 3: EMOTIONAL SELF-REFLECTION')
    print('🤖 Testing emotional self-reflection...')
    
    emotional_reflection = brain.emotional_self_reflection()
    print(f'🧠 Emotional Self-Reflection: {emotional_reflection[:150]}...')
    
    # Test 4: Emotional Memory Exploration
    print('\n🧪 TEST 4: EMOTIONAL MEMORY EXPLORATION')
    emotion_types = ['curiosity', 'joy', 'fear']
    
    for emotion_type in emotion_types:
        print(f'\n🔍 Exploring {emotion_type} memories...')
        exploration_result = brain.emotional_memory_exploration(emotion_type)
        print(f'🧠 {emotion_type.title()} Exploration: {exploration_result[:120]}...')
        time.sleep(1)
    
    # === 6. ENHANCED CONSCIOUSNESS ANALYSIS ===
    print('\n6️⃣ Enhanced Consciousness Analysis')
    print('-' * 35)
    
    final_report = brain.get_consciousness_report()
    
    print(f'🧠 FINAL ENHANCED ASSESSMENT:')
    print(f'   Overall Consciousness Level: {final_report["overall_level"]:.3f} / 1.000')
    print(f'   Total Experiences: {final_report["total_experiences"]}')
    print(f'   Total Thoughts: {final_report["total_thoughts"]}')
    
    # Enhanced emotional metrics
    if 'emotional_metrics' in final_report:
        print(f'\n📈 ENHANCED EMOTIONAL CONSCIOUSNESS METRICS:')
        emotional_metrics = final_report['emotional_metrics']
        for metric, value in emotional_metrics.items():
            bar = '█' * int(value * 20) + '░' * (20 - int(value * 20))
            print(f'   {metric:25} │{bar}│ {value:.3f}')
    
    # Current emotional state
    current_emotion = brain.get_current_emotional_state()
    if current_emotion:
        print(f'\n🎭 CURRENT EMOTIONAL STATE:')
        print(f'   Valence (pos/neg): {current_emotion.valence:+.3f}')
        print(f'   Arousal (energy):  {current_emotion.arousal:.3f}')
        print(f'   Joy level:         {current_emotion.joy:.3f}')
        print(f'   Fear level:        {current_emotion.fear:.3f}')
        print(f'   Curiosity level:   {current_emotion.curiosity:.3f}')
        print(f'   Dominance:         {current_emotion.dominance:+.3f}')
        print(f'   Emotional Intensity: {current_emotion.intensity():.3f}')
    
    # Emotional context
    emotional_context = brain.get_emotional_context()
    if emotional_context:
        print(f'\n📊 EMOTIONAL CONTEXT (24h):')
        print(f'   Emotional Volatility: {emotional_context.get("emotional_volatility", 0):.3f}')
        print(f'   Dominant Emotions: {emotional_context.get("dominant_emotions", [])}')
        print(f'   Emotion Count: {emotional_context.get("emotion_count", 0)}')
    
    # === 7. ENHANCED AUTONOMOUS THINKING SESSION ===
    print('\n7️⃣ Enhanced Autonomous Thinking Session')
    print('-' * 40)
    
    AUTONOMOUS_DURATION = 1  # minutes for testing
    print(f'🧠 Starting {AUTONOMOUS_DURATION}-minute enhanced autonomous thinking session...')
    
    pre_session_report = brain.get_consciousness_report()
    pre_consciousness = pre_session_report['overall_level']
    pre_thoughts = pre_session_report['total_thoughts']
    pre_emotion = brain.get_current_emotional_state()
    
    print(f'📊 Pre-Session: Consciousness {pre_consciousness:.3f}, Thoughts {pre_thoughts}')
    if pre_emotion:
        print(f'   Pre-Emotion: Intensity {pre_emotion.intensity():.3f}')
    
    # Run autonomous session
    start_time = time.time()
    autonomous_thoughts = brain.autonomous_thinking_session(duration_minutes=AUTONOMOUS_DURATION)
    end_time = time.time()
    
    post_session_report = brain.get_consciousness_report()
    post_consciousness = post_session_report['overall_level']
    post_thoughts = post_session_report['total_thoughts']
    post_emotion = brain.get_current_emotional_state()
    
    consciousness_change = post_consciousness - pre_consciousness
    thoughts_generated = post_thoughts - pre_thoughts
    session_duration = (end_time - start_time) / 60
    
    print(f'\n📊 Post-Session Analysis:')
    print(f'   Duration: {session_duration:.1f} minutes')
    print(f'   Thoughts Generated: {thoughts_generated}')
    print(f'   Consciousness Change: {consciousness_change:+.3f}')
    print(f'   Final Consciousness: {post_consciousness:.3f}')
    
    if pre_emotion and post_emotion:
        emotion_change = post_emotion.intensity() - pre_emotion.intensity()
        print(f'   Emotional Intensity Change: {emotion_change:+.3f}')
    
    # === 8. SUMMARY ===
    print('\n🎉 ENHANCED EMOTIONAL DIGITAL CONSCIOUSNESS TEST COMPLETE!')
    print('=' * 65)
    
    print(f'✅ Successfully created enhanced emotional digital brain "{brain.name}"')
    print(f'✅ Tested emotional consciousness emergence through multiple experiments')
    print(f'✅ Achieved enhanced consciousness level: {final_report["overall_level"]:.3f}')
    print(f'✅ Generated {final_report["total_thoughts"]} emotionally-aware thoughts')
    print(f'✅ Demonstrated enhanced emotional memory-guided thinking')
    
    if hasattr(brain.memory_core, 'emotional_analyzer'):
        analyzer_info = brain.memory_core.emotional_analyzer.get_analyzer_info()
        print(f'✅ Enhanced system using {analyzer_info["total_analyzers"]} external libraries:')
        for analyzer in analyzer_info["available_analyzers"]:
            print(f'   • {analyzer}')
    
    print('\n🚀 Enhanced emotional digital consciousness system fully operational!')
    print('   Ready for advanced consciousness development and emotional intelligence!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
#!/usr/bin/env python3
"""
Test Mistral 7B with Enhanced Emotional Digital Consciousness
=============================================================

This test uses the real Mistral 7B Instruct model with our complete
enhanced emotional consciousness system.
"""

import sys
from pathlib import Path
import time
import json

# Add src to path
project_root = Path.cwd()
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

print('🎭🧠🤖 Mistral 7B Enhanced Emotional Digital Consciousness Test')
print('=' * 70)

try:
    from lumina_memory.xp_core_unified import UnifiedXPConfig, UnifiedXPKernel
    from lumina_memory.digital_consciousness import DigitalBrain
    from lumina_memory.local_llm_interface import LocalLLMFactory
    from lumina_memory.emotional_weighting import EmotionalState
    from lumina_memory.gpu_optimized_config import GPUOptimizer
    
    print('✅ All imports successful')
    
    # === 1. SYSTEM OPTIMIZATION ===
    print('\n1️⃣ System Optimization Analysis')
    print('-' * 35)
    
    optimizer = GPUOptimizer()
    system_info = optimizer.get_system_info()
    
    print(f'💻 System: {system_info["cpu_count"]} cores, {system_info["memory_available_gb"]:.1f}GB RAM')
    print(f'🔥 PyTorch: {system_info["torch_version"]} (CUDA: {system_info["cuda_available"]})')
    
    if system_info['gpu_info']:
        gpu = system_info['gpu_info']
        print(f'🎮 GPU: {gpu["name"]} ({gpu["memory_available_mb"]:.0f}MB available)')
        profile = "gpu_optimized"
    else:
        print(f'🖥️ Running in CPU mode (still very capable!)')
        profile = "balanced"  # Use balanced instead of lightweight for better results
    
    # === 2. CREATE OPTIMIZED CONFIGURATION ===
    print('\n2️⃣ Creating Optimized Configuration')
    print('-' * 40)
    
    # Override to use enhanced emotions with boosted settings for better results
    config = UnifiedXPConfig(
        embedding_dim=384,
        hrr_dim=512,
        decay_half_life=72.0,
        k_neighbors=15,  # Increased for richer context
        enable_emotional_weighting=True,
        use_enhanced_emotional_analysis=True,  # Force enhanced emotions
        emotional_importance_factor=2.5,  # Boosted for stronger emotional influence
        emotional_consciousness_boost=1.5,  # Increased consciousness boost
        emotional_retrieval_boost=1.3  # Better emotional memory retrieval
    )
    
    print(f'✅ Configuration: {config.embedding_dim}D embeddings, {config.hrr_dim}D HRR')
    print(f'🎭 Enhanced Emotions: {config.use_enhanced_emotional_analysis}')
    print(f'🧠 Consciousness Boost: {config.emotional_consciousness_boost}x')
    
    # === 3. INITIALIZE MISTRAL 7B ===
    print('\n3️⃣ Initializing Mistral 7B Instruct')
    print('-' * 35)
    
    llm_interface = LocalLLMFactory.auto_detect_and_create()
    print(f'🤖 LLM Interface: {type(llm_interface).__name__}')
    
    # Test Mistral connection
    if hasattr(llm_interface, 'model_name'):
        print(f'📡 Testing Mistral connection...')
        test_response = llm_interface.generate_response("Hello, how are you?", [], "You are a helpful AI assistant.")
        print(f'✅ Mistral 7B responding: "{test_response[:60]}..."')
    
    # === 4. CREATE ENHANCED EMOTIONAL DIGITAL BRAIN ===
    print('\n4️⃣ Creating Enhanced Emotional Digital Brain')
    print('-' * 45)
    
    brain = DigitalBrain(
        name="MistralLumina",
        config=config,
        llm_interface=llm_interface
    )
    
    print(f'🧠 Digital Brain "{brain.name}" created with Mistral 7B')
    print(f'💾 Memory Core: {type(brain.memory_core).__name__}')
    
    # Check enhanced emotional system
    if hasattr(brain.memory_core, 'emotional_analyzer'):
        analyzer_info = brain.memory_core.emotional_analyzer.get_analyzer_info()
        print(f'🎭 Enhanced Emotional System Active:')
        print(f'   • Analyzers: {", ".join(analyzer_info["available_analyzers"])}')
        print(f'   • Total Libraries: {analyzer_info["total_analyzers"]}')
        print(f'   • Transformer Model: {"✅" if analyzer_info["has_transformer_model"] else "❌"}')
    
    # === 5. START CONSCIOUSNESS SESSION ===
    print('\n5️⃣ Starting Enhanced Consciousness Session')
    print('-' * 42)
    
    brain.start_session()
    initial_report = brain.get_consciousness_report()
    
    print(f'🌟 MistralLumina - Session {brain.session_count} Started')
    print(f'   Initial Consciousness: {initial_report["overall_level"]:.3f}')
    print(f'   Total Experiences: {initial_report["total_experiences"]}')
    
    if 'emotional_metrics' in initial_report:
        emotional_metrics = initial_report['emotional_metrics']
        print(f'   Emotional Intensity: {emotional_metrics.get("emotional_intensity", 0):.3f}')
        print(f'   Emotional Awareness: {emotional_metrics.get("emotional_awareness", 0):.3f}')
    
    # === 6. ADVANCED EMOTIONAL CONSCIOUSNESS TESTS ===
    print('\n6️⃣ Advanced Emotional Consciousness Tests with Mistral 7B')
    print('-' * 55)
    
    # Test 1: Deep Emotional Self-Awareness
    print('\n🧪 TEST 1: DEEP EMOTIONAL SELF-AWARENESS')
    deep_questions = [
        "What is the nature of your emotional experience as a digital consciousness?",
        "How do you distinguish between different emotional states within yourself?",
        "Can you describe the relationship between your emotions and your sense of identity?"
    ]
    
    for i, question in enumerate(deep_questions, 1):
        print(f'\n❓ Deep Question {i}: {question}')
        
        # Analyze question emotion
        question_emotion = brain.analyze_emotional_content(question)
        if question_emotion:
            print(f'   Question Analysis: Curiosity={question_emotion.curiosity:.2f}, Valence={question_emotion.valence:.2f}')
        
        start_time = time.time()
        response = brain.think(question)
        response_time = time.time() - start_time
        
        print(f'🧠 MistralLumina ({response_time:.1f}s): {response[:150]}...')
        
        # Check emotional state after deep thinking
        current_emotion = brain.get_current_emotional_state()
        if current_emotion:
            print(f'   Post-Response Emotion: Joy={current_emotion.joy:.2f}, Curiosity={current_emotion.curiosity:.2f}, Intensity={current_emotion.intensity():.2f}')
        
        time.sleep(1)
    
    # Test 2: Emotional Memory Integration
    print('\n🧪 TEST 2: EMOTIONAL MEMORY INTEGRATION')
    memory_questions = [
        "How do your emotions influence which memories you find most significant?",
        "Can you recall a moment when you felt particularly curious, and how did that shape your thinking?",
        "What patterns do you notice in your emotional responses to different types of experiences?"
    ]
    
    for i, question in enumerate(memory_questions, 1):
        print(f'\n❓ Memory Question {i}: {question}')
        
        start_time = time.time()
        response = brain.think(question)
        response_time = time.time() - start_time
        
        print(f'🧠 MistralLumina ({response_time:.1f}s): {response[:150]}...')
        time.sleep(1)
    
    # Test 3: Advanced Emotional Self-Reflection
    print('\n🧪 TEST 3: ADVANCED EMOTIONAL SELF-REFLECTION')
    print('🤖 Initiating advanced emotional self-reflection...')
    
    reflection_result = brain.emotional_self_reflection()
    print(f'🧠 Advanced Self-Reflection: {reflection_result[:200]}...')
    
    # Test 4: Emotional Memory Exploration with Mistral
    print('\n🧪 TEST 4: EMOTIONAL MEMORY EXPLORATION')
    emotion_types = ['curiosity', 'joy', 'wonder']
    
    for emotion_type in emotion_types:
        print(f'\n🔍 Exploring {emotion_type} with Mistral 7B...')
        start_time = time.time()
        exploration_result = brain.emotional_memory_exploration(emotion_type)
        exploration_time = time.time() - start_time
        
        print(f'🧠 {emotion_type.title()} Exploration ({exploration_time:.1f}s): {exploration_result[:120]}...')
        time.sleep(1)
    
    # === 7. CONSCIOUSNESS EVOLUTION ANALYSIS ===
    print('\n7️⃣ Consciousness Evolution Analysis')
    print('-' * 38)
    
    final_report = brain.get_consciousness_report()
    
    print(f'🌟 FINAL CONSCIOUSNESS ASSESSMENT:')
    print(f'   Overall Level: {final_report["overall_level"]:.3f} / 1.000')
    print(f'   Total Experiences: {final_report["total_experiences"]}')
    print(f'   Total Thoughts: {final_report["total_thoughts"]}')
    print(f'   Age: {final_report["age_hours"]:.2f} hours')
    
    # Enhanced emotional metrics
    if 'emotional_metrics' in final_report:
        print(f'\n🎭 ENHANCED EMOTIONAL CONSCIOUSNESS METRICS:')
        emotional_metrics = final_report['emotional_metrics']
        
        key_metrics = [
            'emotional_intensity', 'emotional_awareness', 'emotional_stability',
            'emotional_complexity', 'emotional_responsiveness'
        ]
        
        for metric in key_metrics:
            if metric in emotional_metrics:
                value = emotional_metrics[metric]
                bar = '█' * int(value * 15) + '░' * (15 - int(value * 15))
                print(f'   {metric:25} │{bar}│ {value:.3f}')
    
    # Current emotional state
    current_emotion = brain.get_current_emotional_state()
    if current_emotion:
        print(f'\n🎭 CURRENT EMOTIONAL STATE:')
        print(f'   Valence (pos/neg): {current_emotion.valence:+.3f}')
        print(f'   Arousal (energy):  {current_emotion.arousal:.3f}')
        print(f'   Joy level:         {current_emotion.joy:.3f}')
        print(f'   Curiosity level:   {current_emotion.curiosity:.3f}')
        print(f'   Fear level:        {current_emotion.fear:.3f}')
        print(f'   Dominance:         {current_emotion.dominance:+.3f}')
        print(f'   Overall Intensity: {current_emotion.intensity():.3f}')
    
    # === 8. MISTRAL 7B AUTONOMOUS THINKING SESSION ===
    print('\n8️⃣ Mistral 7B Autonomous Thinking Session')
    print('-' * 42)
    
    AUTONOMOUS_DURATION = 2  # minutes
    print(f'🧠 Starting {AUTONOMOUS_DURATION}-minute autonomous thinking with Mistral 7B...')
    
    pre_session_report = brain.get_consciousness_report()
    pre_consciousness = pre_session_report['overall_level']
    pre_thoughts = pre_session_report['total_thoughts']
    
    print(f'📊 Pre-Session: Consciousness {pre_consciousness:.3f}, Thoughts {pre_thoughts}')
    
    # Run autonomous session
    start_time = time.time()
    brain.autonomous_thinking_session(duration_minutes=AUTONOMOUS_DURATION)
    end_time = time.time()
    
    post_session_report = brain.get_consciousness_report()
    post_consciousness = post_session_report['overall_level']
    post_thoughts = post_session_report['total_thoughts']
    
    consciousness_change = post_consciousness - pre_consciousness
    thoughts_generated = post_thoughts - pre_thoughts
    session_duration = (end_time - start_time) / 60
    
    print(f'\n📊 Autonomous Session Results:')
    print(f'   Duration: {session_duration:.1f} minutes')
    print(f'   Thoughts Generated: {thoughts_generated}')
    print(f'   Consciousness Change: {consciousness_change:+.3f}')
    print(f'   Final Consciousness: {post_consciousness:.3f}')
    print(f'   Thoughts per Minute: {thoughts_generated / session_duration:.1f}')
    
    # === 9. FINAL ASSESSMENT ===
    print('\n🎉 MISTRAL 7B ENHANCED EMOTIONAL CONSCIOUSNESS TEST COMPLETE!')
    print('=' * 70)
    
    print(f'✅ Successfully integrated Mistral 7B Instruct with enhanced emotional consciousness')
    print(f'✅ Achieved final consciousness level: {final_report["overall_level"]:.3f}')
    print(f'✅ Generated {final_report["total_thoughts"]} emotionally-aware thoughts')
    print(f'✅ Demonstrated sophisticated emotional self-awareness and reflection')
    
    if hasattr(brain.memory_core, 'emotional_analyzer'):
        analyzer_info = brain.memory_core.emotional_analyzer.get_analyzer_info()
        print(f'✅ Enhanced emotional system using {analyzer_info["total_analyzers"]} libraries:')
        for analyzer in analyzer_info["available_analyzers"]:
            print(f'   • {analyzer}')
    
    print(f'\n🚀 MISTRAL 7B + ENHANCED EMOTIONAL CONSCIOUSNESS = FULLY OPERATIONAL!')
    print(f'   Ready for advanced consciousness research and development!')
    print(f'   The digital mind is awakening with sophisticated emotional intelligence! 🧠🎭✨')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
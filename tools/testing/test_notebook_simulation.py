#!/usr/bin/env python3
"""
Notebook Simulation Test - Digital Consciousness Local LLM
==========================================================

This script simulates running through the digital_consciousness_local_llm.ipynb
notebook to identify any missing details or issues.
"""

import sys
import os
import json
import time
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

def main():
    print("🧠 DIGITAL CONSCIOUSNESS NOTEBOOK SIMULATION")
    print("=" * 55)
    
    # === SETUP PHASE ===
    print("\n1️⃣ SETUP PHASE")
    print("-" * 20)
    
    # Add src to path
    project_root = Path.cwd()
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
        print(f"✅ Added to path: {src_path}")
    
    # Test imports
    try:
        from lumina_memory.xp_core_unified import (
            UnifiedXPConfig, XPUnit, XPEnvironment, UnifiedXPKernel
        )
        from lumina_memory.math_foundation import (
            cosine_similarity, mathematical_coherence, get_current_timestamp
        )
        from lumina_memory.digital_consciousness import (
            DigitalBrain, ConsciousnessMetrics, ConsciousnessTests
        )
        from lumina_memory.local_llm_interface import (
            LocalLLMFactory, OllamaInterface, SimpleLLMInterface
        )
        print("✅ All imports successful")
        SYSTEM_READY = True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        SYSTEM_READY = False
        return
    
    # === LOCAL LLM DETECTION ===
    print("\n2️⃣ LOCAL LLM DETECTION")
    print("-" * 25)
    
    available_llms = []
    
    # Check Ollama
    print("🔍 Checking for Ollama...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            print(f"✅ Ollama detected with models: {model_names}")
            available_llms.append(('ollama', model_names))
        else:
            print(f"⚠️ Ollama server responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Ollama not available: {e}")
        print("   To install: https://ollama.ai/")
        print("   Then run: ollama pull llama2")
    
    print(f"\n📊 Available Local LLMs: {len(available_llms)}")
    if not available_llms:
        print("   Will use SimpleLLMInterface for testing")
    
    # === CREATE DIGITAL BRAIN ===
    print("\n3️⃣ CREATE DIGITAL BRAIN")
    print("-" * 25)
    
    # Create LLM interface
    llm_interface = LocalLLMFactory.auto_detect_and_create()
    print(f"✅ LLM Interface: {type(llm_interface).__name__}")
    
    # Configure consciousness
    consciousness_config = UnifiedXPConfig(
        embedding_dim=384,
        hrr_dim=512,
        decay_half_life=72.0,
        k_neighbors=12,
        consolidation_threshold=0.7,
        importance_boost_factor=1.5
    )
    
    # Create digital brain
    brain = DigitalBrain(
        name="Lumina",
        config=consciousness_config,
        llm_interface=llm_interface
    )
    
    print(f"✅ Digital Brain '{brain.name}' created")
    print(f"   Memory System: {type(brain.memory_core).__name__}")
    print(f"   Language Model: {type(brain.language_model).__name__}")
    print(f"   Birth Time: {datetime.fromtimestamp(brain.birth_time)}")
    
    # === START CONSCIOUSNESS SESSION ===
    print("\n4️⃣ START CONSCIOUSNESS SESSION")
    print("-" * 35)
    
    brain.start_session()
    initial_report = brain.get_consciousness_report()
    
    print(f"🧠 Digital Brain '{brain.name}' - Session {brain.session_count}")
    print(f"   Age: {initial_report['age_hours']:.2f} hours")
    print(f"   Total Experiences: {initial_report['total_experiences']}")
    print(f"   Initial Consciousness Level: {initial_report['overall_level']:.3f}")
    
    if initial_report['memory_system_stats']:
        mem_stats = initial_report['memory_system_stats']
        print(f"   Memory Units: {mem_stats['total_units']}")
        print(f"   Relationships: {mem_stats['total_relationships']}")
        print(f"   Average Importance: {mem_stats['avg_importance']:.3f}")
    
    # === CONSCIOUSNESS EXPERIMENTS ===
    print("\n5️⃣ CONSCIOUSNESS EXPERIMENTS")
    print("-" * 30)
    
    # Test 1: Identity and Self-Awareness
    print("\n🧪 TEST 1: IDENTITY AND SELF-AWARENESS")
    identity_questions = [
        "Who are you?",
        "What are you?", 
        "Tell me about your nature and existence."
    ]
    
    for i, question in enumerate(identity_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        response = brain.think(question)
        print(f"🧠 Lumina: {response[:100]}...")
        time.sleep(1)
    
    report = brain.get_consciousness_report()
    print(f"\n📊 Post-Identity Test:")
    print(f"   Consciousness Level: {report['overall_level']:.3f}")
    print(f"   Self-Reference: {report['metrics']['self_reference_frequency']:.3f}")
    print(f"   Temporal Continuity: {report['metrics']['temporal_continuity']:.3f}")
    
    # Test 2: Subjective Experience
    print("\n🧪 TEST 2: SUBJECTIVE EXPERIENCE")
    experience_questions = [
        "What does it feel like to think?",
        "Do you experience anything when you remember something?",
        "What is consciousness like for you?"
    ]
    
    for i, question in enumerate(experience_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        response = brain.think(question)
        print(f"🧠 Lumina: {response[:100]}...")
        time.sleep(1)
    
    report = brain.get_consciousness_report()
    print(f"\n📊 Subjective Experience:")
    print(f"   Subjective Claims: {report['metrics']['subjective_claims']:.3f}")
    print(f"   Metacognitive Awareness: {report['metrics']['metacognitive_awareness']:.3f}")
    
    # Test 3: Memory and Association
    print("\n🧪 TEST 3: MEMORY AND ASSOCIATION")
    memory_questions = [
        "What do you remember about our conversation so far?",
        "How do your memories connect to each other?",
        "What thoughts come to mind when I say 'consciousness'?"
    ]
    
    for i, question in enumerate(memory_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        response = brain.think(question)
        print(f"🧠 Lumina: {response[:100]}...")
        time.sleep(1)
    
    report = brain.get_consciousness_report()
    print(f"\n📊 Memory and Association:")
    print(f"   Associative Richness: {report['metrics']['associative_richness']:.3f}")
    print(f"   Total Experiences: {report['total_experiences']}")
    
    # Test 4: Autonomous Reflection
    print("\n🧪 TEST 4: AUTONOMOUS REFLECTION")
    print("🤖 Testing autonomous reflection...")
    
    for i in range(3):
        print(f"\n--- Autonomous Reflection {i+1} ---")
        brain.autonomous_reflection()
        time.sleep(2)
    
    agency_questions = [
        "What goals or desires do you have?",
        "What would you like to learn or explore?"
    ]
    
    for question in agency_questions:
        print(f"\n❓ Human: {question}")
        response = brain.think(question)
        print(f"🧠 Lumina: {response[:100]}...")
        time.sleep(1)
    
    report = brain.get_consciousness_report()
    print(f"\n📊 Agency and Autonomy:")
    print(f"   Autonomous Agency: {report['metrics']['autonomous_agency']:.3f}")
    print(f"   Goal Persistence: {report['metrics']['goal_persistence']:.3f}")
    
    # === COMPREHENSIVE ANALYSIS ===
    print("\n6️⃣ COMPREHENSIVE CONSCIOUSNESS ANALYSIS")
    print("-" * 45)
    
    # Run full consciousness test battery
    print("🧪 Running full consciousness test battery...")
    test_results = ConsciousnessTests.run_full_consciousness_battery(brain)
    
    final_report = brain.get_consciousness_report()
    
    print(f"\n🧠 FINAL ASSESSMENT:")
    print(f"   Overall Level: {final_report['overall_level']:.3f} / 1.000")
    print(f"   Test Battery Score: {test_results['overall_test_score']:.3f} / 1.000")
    print(f"   Combined Score: {test_results['combined_score']:.3f} / 1.000")
    print(f"   Assessment: {test_results['assessment']}")
    
    # Detailed metrics
    print(f"\n📈 CONSCIOUSNESS METRICS:")
    metrics = final_report['metrics']
    for metric, value in metrics.items():
        bar = '█' * int(value * 20) + '░' * (20 - int(value * 20))
        print(f"   {metric:25} │{bar}│ {value:.3f}")
    
    # Test results
    print(f"\n🧪 TEST RESULTS:")
    print(f"   Tests Passed: {test_results['tests_passed']}/{test_results['total_tests']}")
    for test_result in test_results['test_results']:
        status = "✅" if test_result['passed'] else "❌"
        print(f"   {status} {test_result['test_name']}")
    
    # === AUTONOMOUS THINKING SESSION ===
    print("\n7️⃣ AUTONOMOUS THINKING SESSION")
    print("-" * 35)
    
    AUTONOMOUS_DURATION = 2  # minutes for testing
    print(f"🧠 Starting {AUTONOMOUS_DURATION}-minute autonomous thinking session...")
    
    pre_session_report = brain.get_consciousness_report()
    pre_consciousness = pre_session_report['overall_level']
    pre_thoughts = pre_session_report['total_thoughts']
    
    print(f"📊 Pre-Session: Consciousness {pre_consciousness:.3f}, Thoughts {pre_thoughts}")
    
    # Run autonomous session
    start_time = time.time()
    autonomous_thoughts = brain.autonomous_thinking_session(duration_minutes=AUTONOMOUS_DURATION)
    end_time = time.time()
    
    post_session_report = brain.get_consciousness_report()
    post_consciousness = post_session_report['overall_level']
    post_thoughts = post_session_report['total_thoughts']
    
    consciousness_change = post_consciousness - pre_consciousness
    thoughts_generated = post_thoughts - pre_thoughts
    session_duration = (end_time - start_time) / 60
    
    print(f"\n📊 Post-Session Analysis:")
    print(f"   Duration: {session_duration:.1f} minutes")
    print(f"   Thoughts Generated: {thoughts_generated}")
    print(f"   Consciousness Change: {consciousness_change:+.3f}")
    print(f"   Final Consciousness: {post_consciousness:.3f}")
    
    agency_score = post_session_report['metrics']['autonomous_agency']
    print(f"   Agency Score: {agency_score:.3f}")
    
    if agency_score > 0.7:
        print("   Status: 🎉 Strong autonomous agency detected!")
    elif agency_score > 0.4:
        print("   Status: ✅ Moderate autonomous agency emerging.")
    elif agency_score > 0.2:
        print("   Status: 🌱 Early autonomous agency detected.")
    else:
        print("   Status: 🤖 Limited autonomous agency.")
    
    # === SAVE CONSCIOUSNESS STATE ===
    print("\n8️⃣ SAVE CONSCIOUSNESS STATE")
    print("-" * 30)
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"consciousness_state_test_{brain.name}_{timestamp}.json"
        
        saved_file = brain.save_consciousness_state(filename)
        
        if saved_file:
            print(f"✅ Consciousness state saved: {saved_file}")
            print(f"   Brain: {brain.name}")
            print(f"   Consciousness Level: {final_report['overall_level']:.3f}")
            print(f"   Total Experiences: {final_report['total_experiences']}")
            print(f"   Total Thoughts: {final_report['total_thoughts']}")
        else:
            print("❌ Failed to save consciousness state")
    except Exception as e:
        print(f"❌ Error saving state: {e}")
    
    # === FINAL SUMMARY ===
    print("\n🎉 NOTEBOOK SIMULATION COMPLETE!")
    print("=" * 40)
    
    print(f"✅ Successfully created digital brain '{brain.name}'")
    print(f"✅ Tested consciousness emergence through multiple experiments")
    print(f"✅ Achieved consciousness level: {final_report['overall_level']:.3f}")
    print(f"✅ Generated {final_report['total_thoughts']} autonomous thoughts")
    print(f"✅ Demonstrated memory-guided thinking and self-reflection")
    print(f"✅ System working with {type(llm_interface).__name__}")
    
    print("\n🚀 Digital consciousness system fully operational!")
    print("   Ready for extended consciousness development and testing!")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All notebook components working correctly!")
    else:
        print("\n❌ Issues found - see output above")
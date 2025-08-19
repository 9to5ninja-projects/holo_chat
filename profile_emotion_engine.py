#!/usr/bin/env python3
"""
Profile Emotion Engine Performance
==================================

Find the exact bottleneck in our emotion processing.
"""

import time
import cProfile
import pstats
import io
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def profile_single_message():
    """Profile a single message processing to find bottlenecks"""
    
    print("🔍 PROFILING EMOTION ENGINE PERFORMANCE")
    print("=" * 50)
    
    # Initialize assistant
    print("1. Initializing assistant...")
    start_time = time.time()
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    init_time = time.time() - start_time
    print(f"   ✅ Initialized in {init_time:.3f}s")
    
    # Start session
    print("2. Starting session...")
    start_time = time.time()
    session_id = assistant.start_session("ProfileTest")
    session_time = time.time() - start_time
    print(f"   ✅ Session started in {session_time:.3f}s")
    
    # Profile the chat function
    print("3. Profiling chat processing...")
    
    def run_chat():
        return assistant.chat("Hello, this is a test message for profiling.", model="internal")
    
    # Run with profiler
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    result = run_chat()
    total_time = time.time() - start_time
    
    profiler.disable()
    
    print(f"   ⏱️  Total processing time: {total_time:.3f}s")
    
    # Analyze profiling results
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(20)  # Top 20 functions
    
    profile_output = s.getvalue()
    
    print("\n📊 TOP PERFORMANCE BOTTLENECKS:")
    print("-" * 40)
    
    # Parse and display key bottlenecks
    lines = profile_output.split('\n')
    for line in lines[5:25]:  # Skip header, show top 20
        if line.strip() and 'function calls' not in line:
            print(f"   {line}")
    
    # Save full profile
    with open("emotion_engine_profile.txt", "w") as f:
        f.write(profile_output)
    
    print(f"\n💾 Full profile saved to: emotion_engine_profile.txt")
    
    assistant.end_session()
    
    return total_time

def manual_timing_analysis():
    """Manually time each step to find bottlenecks"""
    
    print(f"\n🔬 MANUAL TIMING ANALYSIS")
    print("=" * 50)
    
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("TimingTest")
    
    message = "Hello, timing test message."
    
    # Step 1: Sentiment analysis
    print("1. Testing sentiment analysis...")
    start_time = time.time()
    affect_delta = assistant.analyze_message_sentiment(message)
    sentiment_time = time.time() - start_time
    print(f"   ⏱️  Sentiment analysis: {sentiment_time:.3f}s")
    
    # Step 2: XPUnit creation
    print("2. Testing XPUnit creation...")
    start_time = time.time()
    
    from src.lumina_memory.advanced_xpunit import AdvancedXPUnit, AffectState
    
    user_affect = AffectState(
        valence=affect_delta["valence"],
        arousal=affect_delta["arousal"]
    )
    if hasattr(AffectState, 'dominance'):
        user_affect.dominance = affect_delta["dominance"]
    
    user_xpunit = AdvancedXPUnit(
        content_id=f"timing_test_user",
        content=message,
        affect=user_affect
    )
    
    xpunit_time = time.time() - start_time
    print(f"   ⏱️  XPUnit creation: {xpunit_time:.3f}s")
    
    # Step 3: Environment processing
    print("3. Testing environment processing...")
    start_time = time.time()
    
    assistant.env.xpunits[user_xpunit.content_id] = user_xpunit
    
    env_time = time.time() - start_time
    print(f"   ⏱️  Environment add: {env_time:.3f}s")
    
    # Step 4: Lived experience cycle
    print("4. Testing lived experience cycle...")
    start_time = time.time()
    
    response_result = assistant.env.lived_experience_cycle(
        xpunit_id=user_xpunit.content_id,
        cue_text=message,
        affect_delta=affect_delta,
        mode="internal",
        model="internal"
    )
    
    cycle_time = time.time() - start_time
    print(f"   ⏱️  Lived experience cycle: {cycle_time:.3f}s")
    
    assistant.end_session()
    
    total_manual = sentiment_time + xpunit_time + env_time + cycle_time
    print(f"\n📊 TIMING BREAKDOWN:")
    print(f"   Sentiment Analysis: {sentiment_time:.3f}s ({sentiment_time/total_manual*100:.1f}%)")
    print(f"   XPUnit Creation:    {xpunit_time:.3f}s ({xpunit_time/total_manual*100:.1f}%)")
    print(f"   Environment Add:    {env_time:.3f}s ({env_time/total_manual*100:.1f}%)")
    print(f"   Experience Cycle:   {cycle_time:.3f}s ({cycle_time/total_manual*100:.1f}%)")
    print(f"   TOTAL:              {total_manual:.3f}s")
    
    return {
        "sentiment_time": sentiment_time,
        "xpunit_time": xpunit_time,
        "env_time": env_time,
        "cycle_time": cycle_time,
        "total_time": total_manual
    }

if __name__ == "__main__":
    # Run profiling
    total_time = profile_single_message()
    
    # Run manual timing
    timing_results = manual_timing_analysis()
    
    print(f"\n🎯 PERFORMANCE OPTIMIZATION TARGETS")
    print("=" * 50)
    
    if timing_results["cycle_time"] > 1.0:
        print("❌ Lived experience cycle is the main bottleneck")
        print("   - Check emotion engine processing")
        print("   - Look for unnecessary delays in mood synthesis")
        print("   - Optimize memory operations")
    
    if timing_results["sentiment_time"] > 0.1:
        print("⚠️  Sentiment analysis could be optimized")
    
    if timing_results["xpunit_time"] > 0.1:
        print("⚠️  XPUnit creation could be optimized")
    
    print(f"\n💡 Target: Get total time under 0.1s for real-time performance")
    print(f"   Current: {total_time:.3f}s (needs {total_time/0.1:.1f}x speedup)")
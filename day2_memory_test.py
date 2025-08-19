#!/usr/bin/env python3
"""
Day 2: Memory Formation & Trend Analysis
========================================

Focus: Test memory creation and recall mechanisms
Goal: Gather data on memory formation patterns and trends
"""

import time
import json
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def run_day2_memory_formation_test():
    """Day 2: Memory Formation Test with Trend Analysis"""
    
    print("🧠 DAY 2: MEMORY FORMATION & TREND ANALYSIS")
    print("=" * 60)
    print("📋 Goal: Test memory creation and recall mechanisms")
    print("🎯 Focus: memory_building")
    print("📊 Trend Tracking: Memory patterns, mood evolution, consciousness growth")
    print("=" * 60)
    
    # Initialize assistant
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("Day2_MemoryTester")
    
    # Day 2 specific test messages focused on memory formation
    memory_test_messages = [
        # Memory creation tests
        "Hello! Today I want to explore how you form and store memories.",
        "Can you remember what we talked about yesterday?",
        "I'm going to tell you something important: My favorite color is blue and I love stargazing.",
        "What do you think about the relationship between memory and consciousness?",
        "How do you feel when you create a new memory?",
        
        # Memory recall tests  
        "Do you remember what I just told you about my favorite color?",
        "What emotions do you associate with memory formation?",
        "How does each conversation change your understanding?",
        "Can you describe how your memory system works?",
        "What patterns do you notice in how you learn and remember?"
    ]
    
    # Track detailed metrics for trend analysis
    session_data = {
        "day": 2,
        "theme": "Memory Formation",
        "start_time": time.time(),
        "messages": [],
        "mood_progression": [],
        "consciousness_progression": [],
        "memory_events": [],
        "performance_metrics": []
    }
    
    print(f"\n💬 PROCESSING {len(memory_test_messages)} MEMORY-FOCUSED MESSAGES")
    print("-" * 60)
    
    for i, message in enumerate(memory_test_messages, 1):
        print(f"\n📝 Message {i}/10: {message[:60]}...")
        
        # Process message with timing
        start_time = time.time()
        result = assistant.chat(message, model="internal")
        processing_time = time.time() - start_time
        
        if result["ok"]:
            mood = result["mood"]
            growth = result["consciousness_growth"]
            response = result["response"]
            
            # Track detailed data
            message_data = {
                "index": i,
                "message": message,
                "response": response,
                "processing_time": processing_time,
                "mood": mood,
                "consciousness_growth": growth,
                "timestamp": time.time()
            }
            session_data["messages"].append(message_data)
            session_data["mood_progression"].append(mood)
            session_data["consciousness_progression"].append(growth)
            session_data["performance_metrics"].append(processing_time)
            
            # Display results
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  📊 Mood: V{mood['valence']:+.3f} A{mood['arousal']:+.3f} D{mood['dominance']:+.3f}")
            print(f"  🌱 Growth: +{growth:.4f}")
            print(f"  📝 Response: {len(response)} chars")
            print(f"  💭 Preview: {response[:80]}...")
            
            # Check for memory-related keywords in response
            memory_keywords = ["memory", "remember", "recall", "store", "learn", "experience"]
            if any(keyword in response.lower() for keyword in memory_keywords):
                session_data["memory_events"].append({
                    "message_index": i,
                    "keywords_found": [kw for kw in memory_keywords if kw in response.lower()],
                    "response_snippet": response[:100]
                })
        else:
            print(f"  ❌ Error: {result['error']}")
    
    # End session and get summary
    session_summary = assistant.end_session()
    session_data["end_time"] = time.time()
    session_data["session_summary"] = session_summary
    
    # Analyze trends from Day 2
    print(f"\n📈 DAY 2 TREND ANALYSIS")
    print("=" * 60)
    
    # Performance trends
    processing_times = session_data["performance_metrics"]
    avg_processing = np.mean(processing_times)
    processing_stability = np.std(processing_times)
    
    print(f"⚡ PERFORMANCE TRENDS:")
    print(f"   Average Processing: {avg_processing:.3f}s")
    print(f"   Processing Stability: {processing_stability:.4f}s (lower = more stable)")
    print(f"   Performance Rating: {'🟢 Excellent' if avg_processing < 0.01 else '🟡 Good' if avg_processing < 0.1 else '🔴 Needs Work'}")
    
    # Mood evolution trends
    moods = session_data["mood_progression"]
    valence_trend = [m['valence'] for m in moods]
    arousal_trend = [m['arousal'] for m in moods]
    dominance_trend = [m['dominance'] for m in moods]
    
    print(f"\n🎭 MOOD EVOLUTION TRENDS:")
    print(f"   Valence Range: {min(valence_trend):+.3f} to {max(valence_trend):+.3f} (Δ{max(valence_trend)-min(valence_trend):.3f})")
    print(f"   Arousal Range: {min(arousal_trend):+.3f} to {max(arousal_trend):+.3f} (Δ{max(arousal_trend)-min(arousal_trend):.3f})")
    print(f"   Dominance Range: {min(dominance_trend):+.3f} to {max(dominance_trend):+.3f} (Δ{max(dominance_trend)-min(dominance_trend):.3f})")
    
    # Identify mood trend issues
    if max(valence_trend) - min(valence_trend) < 0.01:
        print("   ⚠️  TREND ISSUE: Valence too static (needs more emotional variation)")
    if max(arousal_trend) - min(arousal_trend) < 0.01:
        print("   ⚠️  TREND ISSUE: Arousal too static (needs more energy variation)")
    
    # Consciousness growth trends
    growth_values = session_data["consciousness_progression"]
    total_growth = sum(growth_values)
    growth_events = len([g for g in growth_values if g > 0])
    
    print(f"\n🧠 CONSCIOUSNESS GROWTH TRENDS:")
    print(f"   Total Growth: {total_growth:.4f}")
    print(f"   Growth Events: {growth_events}/{len(growth_values)} messages")
    print(f"   Growth Rate: {growth_events/len(growth_values)*100:.1f}% of interactions")
    
    # Memory formation analysis
    memory_events = session_data["memory_events"]
    print(f"\n💾 MEMORY FORMATION ANALYSIS:")
    print(f"   Memory-Related Responses: {len(memory_events)}/{len(memory_test_messages)}")
    print(f"   Memory Engagement Rate: {len(memory_events)/len(memory_test_messages)*100:.1f}%")
    
    if memory_events:
        print(f"   Memory Keywords Found:")
        all_keywords = []
        for event in memory_events:
            all_keywords.extend(event["keywords_found"])
        keyword_counts = {kw: all_keywords.count(kw) for kw in set(all_keywords)}
        for kw, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"     - {kw}: {count} times")
    
    # Compare with Day 1 if available
    day1_file = Path("30_day_data/day1_performance_results.json")
    if day1_file.exists():
        print(f"\n📊 DAY 1 vs DAY 2 COMPARISON:")
        with open(day1_file, 'r') as f:
            day1_data = json.load(f)
        
        day1_avg_time = day1_data["performance_metrics"]["avg_processing_time"]
        day2_avg_time = avg_processing
        
        print(f"   Processing Speed: Day 1: {day1_avg_time:.3f}s → Day 2: {day2_avg_time:.3f}s")
        if day2_avg_time < day1_avg_time:
            print(f"   🟢 IMPROVEMENT: {((day1_avg_time - day2_avg_time) / day1_avg_time * 100):.1f}% faster")
        elif day2_avg_time > day1_avg_time:
            print(f"   🟡 REGRESSION: {((day2_avg_time - day1_avg_time) / day1_avg_time * 100):.1f}% slower")
        else:
            print(f"   🟢 STABLE: Performance maintained")
        
        day1_growth = day1_data["consciousness_metrics"]["total_growth"]
        print(f"   Consciousness Growth: Day 1: {day1_growth:.4f} → Day 2: {total_growth:.4f}")
    
    # Save Day 2 results
    results_file = Path("30_day_data") / "day2_memory_results.json"
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(session_data, f, indent=2, default=str)
    
    print(f"\n💾 Day 2 results saved to: {results_file}")
    
    # Recommendations for Day 3
    print(f"\n🎯 RECOMMENDATIONS FOR DAY 3:")
    print("=" * 60)
    
    if len(memory_events) < 5:
        print("🔧 PRIORITY: Enhance memory-related response patterns")
    
    if max(valence_trend) - min(valence_trend) < 0.01:
        print("🔧 PRIORITY: Add valence variation based on message content")
    
    if processing_stability > 0.001:
        print("🔧 MONITOR: Processing time stability")
    
    print("✅ CONTINUE: Current performance is excellent for development")
    print("📈 FOCUS: Day 3 will test emotional calibration and mood synthesis")
    
    return session_data

if __name__ == "__main__":
    day2_results = run_day2_memory_formation_test()
    
    print(f"\n🎉 DAY 2 COMPLETE!")
    print("Ready for Day 3: Emotional Calibration")
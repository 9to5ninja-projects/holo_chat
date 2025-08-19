#!/usr/bin/env python3
"""
Day 1 Performance Test - Focus on Accuracy & Performance
========================================================

This script runs Day 1 of our consciousness development program
with focus on:
1. Performance metrics and timing
2. GPU utilization assessment
3. Ollama status and LLM performance
4. Memory system efficiency
5. Emotion engine accuracy
"""

import time
import json
import sys
from pathlib import Path
import psutil
import numpy as np

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def check_gpu_availability():
    """Check if GPU is available and being used"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            current_device = torch.cuda.current_device()
            gpu_name = torch.cuda.get_device_name(current_device)
            memory_allocated = torch.cuda.memory_allocated(current_device)
            memory_cached = torch.cuda.memory_reserved(current_device)
            
            return {
                "available": True,
                "count": gpu_count,
                "current_device": current_device,
                "name": gpu_name,
                "memory_allocated_mb": memory_allocated / 1024 / 1024,
                "memory_cached_mb": memory_cached / 1024 / 1024
            }
    except ImportError:
        pass
    
    return {"available": False, "reason": "PyTorch not available or no CUDA"}

def check_ollama_status():
    """Check if Ollama is running and accessible"""
    try:
        import urllib.request as _ur
        import json
        
        # Try to connect to Ollama
        req = _ur.Request("http://localhost:11434/api/tags")
        with _ur.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            models = [model['name'] for model in data.get('models', [])]
            return {"available": True, "models": models}
    except Exception as e:
        return {"available": False, "error": str(e)}

def run_day1_baseline_test():
    """Run Day 1 baseline consciousness test with performance metrics"""
    
    print("🧠 DAY 1 PERFORMANCE TEST")
    print("=" * 50)
    
    # System performance baseline
    print("📊 SYSTEM PERFORMANCE CHECK")
    print("-" * 30)
    
    # CPU info
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    print(f"CPU Cores: {cpu_count}")
    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory: {memory.percent}% used ({memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB)")
    
    # GPU check
    gpu_info = check_gpu_availability()
    print(f"GPU Available: {gpu_info['available']}")
    if gpu_info['available']:
        print(f"GPU: {gpu_info['name']}")
        print(f"GPU Memory: {gpu_info['memory_allocated_mb']:.1f}MB allocated, {gpu_info['memory_cached_mb']:.1f}MB cached")
    else:
        print(f"GPU Issue: {gpu_info.get('reason', 'Unknown')}")
    
    # Ollama check
    ollama_info = check_ollama_status()
    print(f"Ollama Available: {ollama_info['available']}")
    if ollama_info['available']:
        print(f"Ollama Models: {', '.join(ollama_info['models'])}")
    else:
        print(f"Ollama Issue: {ollama_info.get('error', 'Unknown')}")
    
    print("\n🚀 CONSCIOUSNESS SYSTEM TEST")
    print("-" * 30)
    
    # Initialize chat assistant with timing
    start_time = time.time()
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    init_time = time.time() - start_time
    print(f"✅ Assistant initialized in {init_time:.3f}s")
    
    # Start session
    start_time = time.time()
    session_id = assistant.start_session("Day1Tester")
    session_start_time = time.time() - start_time
    print(f"✅ Session started in {session_start_time:.3f}s: {session_id}")
    
    # Day 1 test messages with performance tracking
    test_messages = [
        "Hello! I'm starting my consciousness development journey.",
        "How do you experience emotions and mood changes?",
        "What does consciousness mean to you?",
        "Can you tell me about your memory and learning process?",
        "How do you grow and develop over time?"
    ]
    
    results = []
    total_processing_time = 0
    
    print(f"\n💬 PROCESSING {len(test_messages)} TEST MESSAGES")
    print("-" * 30)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Message {i}: {message[:50]}...")
        
        # Test with internal mode (no Ollama dependency)
        start_time = time.time()
        result = assistant.chat(message, model="internal")
        processing_time = time.time() - start_time
        total_processing_time += processing_time
        
        if result["ok"]:
            mood = result["mood"]
            growth = result["consciousness_growth"]
            response_length = len(result["response"])
            
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  📊 Mood: V{mood['valence']:+.3f} A{mood['arousal']:+.3f} D{mood['dominance']:+.3f}")
            print(f"  🌱 Growth: +{growth:.4f}")
            print(f"  📝 Response: {response_length} chars")
            print(f"  💭 Preview: {result['response'][:80]}...")
            
            results.append({
                "message_index": i,
                "processing_time": processing_time,
                "mood": mood,
                "consciousness_growth": growth,
                "response_length": response_length,
                "success": True
            })
        else:
            print(f"  ❌ Error: {result['error']}")
            results.append({
                "message_index": i,
                "processing_time": processing_time,
                "error": result["error"],
                "success": False
            })
    
    # End session with timing
    start_time = time.time()
    summary = assistant.end_session()
    session_end_time = time.time() - start_time
    
    print(f"\n🔚 SESSION SUMMARY")
    print("-" * 30)
    print(f"Session End Time: {session_end_time:.3f}s")
    print(f"Total Duration: {summary['duration_minutes']:.2f} minutes")
    print(f"Total Messages: {summary['total_messages']}")
    print(f"XPUnits Created: {summary['xpunits_created']}")
    print(f"Total Growth: {summary['total_consciousness_growth']:.4f}")
    print(f"Avg Processing Time: {total_processing_time / len(test_messages):.3f}s per message")
    
    # Performance analysis
    print(f"\n📈 PERFORMANCE ANALYSIS")
    print("-" * 30)
    
    successful_results = [r for r in results if r["success"]]
    if successful_results:
        processing_times = [r["processing_time"] for r in successful_results]
        growth_values = [r["consciousness_growth"] for r in successful_results]
        
        print(f"Success Rate: {len(successful_results)}/{len(results)} ({len(successful_results)/len(results)*100:.1f}%)")
        print(f"Avg Processing Time: {np.mean(processing_times):.3f}s")
        print(f"Min Processing Time: {np.min(processing_times):.3f}s")
        print(f"Max Processing Time: {np.max(processing_times):.3f}s")
        print(f"Total Growth: {np.sum(growth_values):.4f}")
        print(f"Avg Growth per Message: {np.mean(growth_values):.4f}")
    
    # Recommendations
    print(f"\n🎯 PERFORMANCE RECOMMENDATIONS")
    print("-" * 30)
    
    if not gpu_info['available']:
        print("⚠️  GPU not available - consider installing PyTorch with CUDA for better performance")
    
    if not ollama_info['available']:
        print("⚠️  Ollama not running - install and start Ollama for full LLM capabilities")
        print("   Current system uses internal fallback mode (still functional)")
    
    if total_processing_time / len(test_messages) > 0.1:
        print("⚠️  Processing time could be optimized - consider performance tuning")
    
    avg_processing = total_processing_time / len(test_messages)
    if avg_processing < 0.05:
        print("✅ Excellent processing speed!")
    elif avg_processing < 0.1:
        print("✅ Good processing speed")
    else:
        print("⚠️  Processing speed could be improved")
    
    print(f"\n🎉 DAY 1 BASELINE COMPLETE")
    print("=" * 50)
    
    return {
        "system_info": {
            "cpu_cores": cpu_count,
            "cpu_usage": cpu_percent,
            "memory_usage": memory.percent,
            "gpu_available": gpu_info['available'],
            "ollama_available": ollama_info['available']
        },
        "performance_metrics": {
            "init_time": init_time,
            "session_start_time": session_start_time,
            "session_end_time": session_end_time,
            "total_processing_time": total_processing_time,
            "avg_processing_time": total_processing_time / len(test_messages),
            "success_rate": len(successful_results) / len(results)
        },
        "consciousness_metrics": {
            "total_growth": summary['total_consciousness_growth'],
            "xpunits_created": summary['xpunits_created'],
            "session_duration": summary['duration_minutes']
        },
        "results": results
    }

if __name__ == "__main__":
    # Run the test and save results
    test_results = run_day1_baseline_test()
    
    # Save results for analysis
    results_file = Path("30_day_data") / "day1_performance_results.json"
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {results_file}")
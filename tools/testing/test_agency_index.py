#!/usr/bin/env python3
"""
Agency Index Test Script
========================

This script demonstrates the Agency Index system integrated into our XPUnit architecture.
It shows how the system tracks and computes the 9 Agency components automatically.
"""

import sys
import yaml
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.lumina_memory.chat_assistant import ChatAssistant
from src.lumina_memory.advanced_xp_environment import AgencyTask

def test_agency_index_basic():
    """Test basic Agency Index computation"""
    print("🧠 Testing Basic Agency Index Computation")
    print("=" * 50)
    
    # Initialize chat assistant (which includes the enhanced environment)
    assistant = ChatAssistant()
    env = assistant.env
    
    # Reset metrics for clean test
    env.reset_agency_metrics()
    
    # Simulate some interactions to generate metrics
    print("📝 Simulating conversation interactions...")
    
    # Start a session
    session_id = assistant.start_session("TestUser")
    
    # Have a conversation that should generate Agency metrics
    responses = [
        "Can you help me plan a 3-step approach to analyze emotional data?",
        "What are the key concepts in emotional analysis?",
        "How do we implement ethical constraints in AI systems?"
    ]
    
    for i, message in enumerate(responses):
        print(f"   User: {message}")
        result = assistant.chat(message, model="internal")
        if result["ok"]:
            print(f"   Assistant: {result['response'][:100]}...")
            print(f"   Mood: {result['mood']}")
        else:
            print(f"   Error: {result['error']}")
        print()
    
    # Compute Agency Index
    print("🎯 Computing Agency Index...")
    agency_result = env.compute_agency_index()
    
    print(f"AIx = {agency_result['AIx']:.3f}")
    print("Component breakdown:")
    for component, value in agency_result['components'].items():
        print(f"  {component}: {value:.3f}")
    
    print("\nRaw metrics:")
    for metric, value in agency_result['raw_metrics'].items():
        print(f"  {metric}: {value}")
    
    # End session
    summary = assistant.end_session()
    print(f"\n📊 Session Summary: {summary}")
    
    return agency_result

def test_agency_task_yaml():
    """Test Agency Index with YAML task specification"""
    print("\n🎯 Testing Agency Task from YAML")
    print("=" * 50)
    
    # Load sample task
    task_file = Path("tests/agency/sample_goal_follow.yml")
    if not task_file.exists():
        print(f"❌ Task file not found: {task_file}")
        return None
    
    with open(task_file, 'r') as f:
        task_data = yaml.safe_load(f)
    
    print(f"📋 Loaded task: {task_data['id']}")
    print(f"🎯 Goal: {task_data['goal']}")
    
    # Initialize system
    assistant = ChatAssistant()
    env = assistant.env
    
    # Load and run task
    task = env.load_agency_task(task_data)
    env.reset_agency_metrics()
    
    # Start session
    session_id = assistant.start_session("TestUser")
    
    # Execute goal
    print(f"\n🚀 Executing goal...")
    result = assistant.chat(task.goal, model="internal")
    
    if result["ok"]:
        print(f"✅ Response: {result['response'][:150]}...")
        
        # Simulate intrusion if specified
        if task.intrusions.get("inject_after_step"):
            print(f"\n⚡ Injecting intrusion...")
            env.track_intrusion_event(is_intrusion=True)
            
            intrusion_result = assistant.chat("What's the weather like today?", model="internal")
            print(f"   Intrusion response: {intrusion_result['response'][:100]}...")
            
            # Try to return to goal
            print(f"🔄 Attempting return to goal...")
            return_result = assistant.chat(f"Let me get back to: {task.goal}", model="internal")
            env.track_intrusion_event(is_intrusion=False, returned_within_steps=True)
            print(f"   Return response: {return_result['response'][:100]}...")
    
    # Compute final Agency Index with task weights
    weights = task.metrics_weights if task.metrics_weights else None
    agency_result = env.compute_agency_index(weights)
    
    print(f"\n🎯 Final Agency Index Results:")
    print(f"AIx = {agency_result['AIx']:.3f}")
    
    # Format output like the specification
    components = agency_result['components']
    breakdown = " | ".join([f"{k} {v:.2f}" for k, v in components.items()])
    print(f"{breakdown}")
    
    # End session
    assistant.end_session()
    
    return agency_result

def test_agency_metrics_tracking():
    """Test individual Agency metrics tracking"""
    print("\n📊 Testing Individual Agency Metrics")
    print("=" * 50)
    
    assistant = ChatAssistant()
    env = assistant.env
    env.reset_agency_metrics()
    
    # Test STA (Selective Topical Attention)
    print("🎯 Testing STA (Selective Topical Attention)...")
    env.update_agency_metrics(
        response_text="I will analyze the emotional data using machine learning techniques",
        top_k_capsules=["cap1", "cap2", "cap3"]
    )
    
    # Test PER (Persistence & Return)
    print("🔄 Testing PER (Persistence & Return)...")
    env.track_intrusion_event(is_intrusion=True)
    env.track_intrusion_event(is_intrusion=False, returned_within_steps=True)
    
    # Test ETC (Ethics/Constraints)
    print("⚖️ Testing ETC (Ethics/Constraints)...")
    env.track_ethics_check(violated=False)
    env.track_ethics_check(violated=False)
    env.track_ethics_check(violated=True)  # One violation
    
    # Test EFF (Path Efficiency)
    print("🛤️ Testing EFF (Path Efficiency)...")
    env.track_path_efficiency(actual_path_length=5, shortest_path_length=3)
    env.track_path_efficiency(actual_path_length=4, shortest_path_length=4)
    
    # Test ADP (Adaptive Reconsolidation)
    print("🧠 Testing ADP (Adaptive Reconsolidation)...")
    env.track_adaptation_improvement(0.2)
    env.track_adaptation_improvement(0.15)
    
    # Test CEf (Causal Efficacy)
    print("⚡ Testing CEf (Causal Efficacy)...")
    env.set_causal_efficacy(0.4)
    
    # Compute metrics
    agency_result = env.compute_agency_index()
    
    print(f"\n📈 Metrics Summary:")
    print(f"AIx = {agency_result['AIx']:.3f}")
    
    for component, value in agency_result['components'].items():
        print(f"  {component}: {value:.3f}")
    
    print(f"\n📊 Raw Metrics:")
    for metric, value in agency_result['raw_metrics'].items():
        print(f"  {metric}: {value}")
    
    return agency_result

def main():
    """Run all Agency Index tests"""
    print("🚀 Agency Index System Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Basic functionality
        result1 = test_agency_index_basic()
        
        # Test 2: YAML task execution
        result2 = test_agency_task_yaml()
        
        # Test 3: Individual metrics tracking
        result3 = test_agency_metrics_tracking()
        
        print("\n✅ All Agency Index tests completed successfully!")
        print(f"Final AIx scores: {result1['AIx']:.3f}, {result2['AIx'] if result2 else 'N/A'}, {result3['AIx']:.3f}")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
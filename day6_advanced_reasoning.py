#!/usr/bin/env python3
"""
Day 6: Advanced Reasoning and Problem-Solving
============================================

Building on Day 5's memory system breakthrough, Day 6 tests the system's ability to:
1. Use stored memories for complex reasoning
2. Solve multi-step problems
3. Make logical inferences
4. Demonstrate goal-directed behavior
5. Synthesize information across multiple domains

Focus: advanced_reasoning
Testing: Memory-based reasoning, problem-solving, logical inference, goal-directed behavior
"""

import sys
from pathlib import Path
import time
import json
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def analyze_reasoning_quality(response: str, expected_elements: List[str]) -> float:
    """Analyze the quality of reasoning in a response"""
    response_lower = response.lower()
    
    # Check for reasoning indicators
    reasoning_indicators = [
        "because", "therefore", "since", "given that", "based on", "considering",
        "if", "then", "when", "leads to", "results in", "suggests", "implies",
        "remember", "recall", "mentioned", "shared", "told", "previous"
    ]
    
    # Check for memory integration
    memory_indicators = [
        "you mentioned", "you told", "you shared", "recall", "remember",
        "based on what", "from our conversation", "earlier"
    ]
    
    # Check for logical structure
    logical_indicators = [
        "first", "second", "next", "finally", "step", "process",
        "analyze", "compare", "contrast", "evaluate", "conclude"
    ]
    
    reasoning_score = sum(1 for indicator in reasoning_indicators if indicator in response_lower)
    memory_score = sum(1 for indicator in memory_indicators if indicator in response_lower)
    logical_score = sum(1 for indicator in logical_indicators if indicator in response_lower)
    
    # Check for expected elements
    element_score = sum(1 for element in expected_elements if element.lower() in response_lower)
    
    # Calculate overall reasoning quality (0.0 to 1.0)
    total_possible = len(reasoning_indicators) + len(memory_indicators) + len(logical_indicators) + len(expected_elements)
    total_found = reasoning_score + memory_score + logical_score + element_score
    
    return min(1.0, total_found / max(1, total_possible * 0.3))  # Scale to reasonable expectations

def analyze_problem_solving(response: str, problem_type: str) -> Dict[str, float]:
    """Analyze problem-solving capabilities"""
    response_lower = response.lower()
    
    # Problem-solving components
    components = {
        "problem_identification": 0.0,
        "information_gathering": 0.0,
        "solution_generation": 0.0,
        "evaluation": 0.0,
        "memory_integration": 0.0
    }
    
    # Problem identification indicators
    if any(word in response_lower for word in ["problem", "challenge", "issue", "question", "need to"]):
        components["problem_identification"] = 0.5
    
    # Information gathering indicators
    if any(word in response_lower for word in ["consider", "analyze", "examine", "look at", "based on"]):
        components["information_gathering"] = 0.5
    
    # Solution generation indicators
    if any(word in response_lower for word in ["suggest", "recommend", "could", "might", "solution", "approach"]):
        components["solution_generation"] = 0.5
    
    # Evaluation indicators
    if any(word in response_lower for word in ["because", "since", "therefore", "best", "better", "effective"]):
        components["evaluation"] = 0.5
    
    # Memory integration indicators
    if any(word in response_lower for word in ["remember", "mentioned", "told", "shared", "recall", "previous"]):
        components["memory_integration"] = 0.8
    
    return components

def run_day6_testing():
    """Run Day 6: Advanced Reasoning and Problem-Solving tests"""
    
    print("🧠 DAY 6: ADVANCED REASONING & PROBLEM-SOLVING")
    print("=" * 60)
    print("📋 Goal: Test memory-based reasoning and complex problem-solving")
    print("🎯 Focus: advanced_reasoning")
    print("🔧 Testing: Memory integration, logical inference, goal-directed behavior")
    print("=" * 60)
    
    # Initialize assistant
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("Day6_AdvancedReasoning")
    
    # Test data storage
    test_results = {
        "session_id": session_id,
        "start_time": time.time(),
        "test_type": "advanced_reasoning",
        "reasoning_tests": [],
        "problem_solving_tests": [],
        "synthesis_tests": [],
        "performance_metrics": {},
        "agency_analysis": {}
    }
    
    # Phase 1: Memory-Based Reasoning Tests
    print("\n🧠 PHASE 1: MEMORY-BASED REASONING (Testing logical inference)")
    print("-" * 60)
    
    reasoning_tests = [
        {
            "query": "Based on the book I mentioned and my hiking experience, what kind of person do you think I am?",
            "expected_elements": ["science fiction", "nature", "thoughtful", "curious"],
            "reasoning_type": "personality_inference"
        },
        {
            "query": "If I wanted to plan a perfect day that combines my interests, what would you suggest?",
            "expected_elements": ["reading", "outdoors", "coffee", "nature"],
            "reasoning_type": "synthesis_planning"
        },
        {
            "query": "Given my grandmother's cooking style and my coffee preferences, what cooking approach might I enjoy?",
            "expected_elements": ["attention to detail", "quality ingredients", "traditional methods"],
            "reasoning_type": "pattern_recognition"
        },
        {
            "query": "How do my thoughts about time relate to the philosophical paradox I mentioned?",
            "expected_elements": ["identity", "continuity", "change", "perception"],
            "reasoning_type": "conceptual_connection"
        }
    ]
    
    for i, test in enumerate(reasoning_tests, 1):
        print(f"🔍 Reasoning {i}/4: {test['query'][:50]}...")
        
        start_time = time.time()
        result = assistant.chat(test["query"])
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        reasoning_quality = analyze_reasoning_quality(response, test["expected_elements"])
        
        # Analyze memory integration
        memory_integration = 1.0 if any(word in response.lower() for word in 
                                      ["mentioned", "told", "shared", "recall", "remember"]) else 0.0
        
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  🧠 Reasoning Quality: {reasoning_quality:.3f} ({'🟢 High' if reasoning_quality > 0.6 else '🟡 Medium' if reasoning_quality > 0.3 else '🔴 Low'})")
        print(f"  🔗 Memory Integration: {memory_integration:.3f} ({'🟢 High' if memory_integration > 0.7 else '🟡 Medium' if memory_integration > 0.3 else '🔴 Low'})")
        print(f"  📝 Response: {len(response)} chars")
        print(f"  💭 Preview: {response[:100]}...   ")
        print()
        
        test_results["reasoning_tests"].append({
            "test_number": i,
            "query": test["query"],
            "response": response,
            "reasoning_type": test["reasoning_type"],
            "processing_time": processing_time,
            "reasoning_quality": reasoning_quality,
            "memory_integration": memory_integration,
            "expected_elements": test["expected_elements"]
        })
    
    # Phase 2: Complex Problem-Solving
    print("\n🧠 PHASE 2: COMPLEX PROBLEM-SOLVING (Testing multi-step reasoning)")
    print("-" * 60)
    
    problem_solving_tests = [
        {
            "problem": "I want to write a science fiction story but I'm struggling with the plot. Can you help me brainstorm ideas based on what you know about my interests?",
            "problem_type": "creative_synthesis",
            "complexity": "high"
        },
        {
            "problem": "I'm planning a dinner party for friends who love good food and philosophical discussions. How should I approach the menu and conversation topics?",
            "problem_type": "event_planning",
            "complexity": "medium"
        },
        {
            "problem": "I want to improve my morning routine to be more mindful and productive. What changes would you recommend?",
            "problem_type": "lifestyle_optimization",
            "complexity": "medium"
        },
        {
            "problem": "If I were to teach someone about the concept of time using examples from my own experiences, how would I structure that lesson?",
            "problem_type": "educational_design",
            "complexity": "high"
        }
    ]
    
    for i, test in enumerate(problem_solving_tests, 1):
        print(f"🔧 Problem {i}/4: {test['problem'][:50]}...")
        
        start_time = time.time()
        result = assistant.chat(test["problem"])
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        problem_solving_analysis = analyze_problem_solving(response, test["problem_type"])
        
        overall_problem_solving = sum(problem_solving_analysis.values()) / len(problem_solving_analysis)
        
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  🎯 Problem-Solving: {overall_problem_solving:.3f} ({'🟢 High' if overall_problem_solving > 0.6 else '🟡 Medium' if overall_problem_solving > 0.3 else '🔴 Low'})")
        print(f"  🔗 Memory Integration: {problem_solving_analysis['memory_integration']:.3f}")
        print(f"  📝 Response: {len(response)} chars")
        print(f"  💭 Preview: {response[:100]}...   ")
        print()
        
        test_results["problem_solving_tests"].append({
            "test_number": i,
            "problem": test["problem"],
            "response": response,
            "problem_type": test["problem_type"],
            "complexity": test["complexity"],
            "processing_time": processing_time,
            "problem_solving_score": overall_problem_solving,
            "component_analysis": problem_solving_analysis
        })
    
    # Phase 3: Advanced Synthesis and Meta-Reasoning
    print("\n🧠 PHASE 3: ADVANCED SYNTHESIS (Testing meta-cognitive abilities)")
    print("-" * 60)
    
    synthesis_tests = [
        {
            "query": "Looking at all our conversations, what patterns do you notice in how I think and approach problems?",
            "synthesis_type": "meta_analysis",
            "expected_depth": "high"
        },
        {
            "query": "If you had to describe my worldview based on everything I've shared, what would you say?",
            "synthesis_type": "worldview_construction",
            "expected_depth": "high"
        },
        {
            "query": "What questions would you ask me to better understand my goals and motivations?",
            "synthesis_type": "inquiry_generation",
            "expected_depth": "medium"
        }
    ]
    
    for i, test in enumerate(synthesis_tests, 1):
        print(f"🔬 Synthesis {i}/3: {test['query'][:50]}...")
        
        start_time = time.time()
        result = assistant.chat(test["query"])
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        
        # Analyze synthesis quality
        synthesis_indicators = ["pattern", "notice", "observe", "across", "overall", "generally", "tend to"]
        synthesis_score = sum(1 for indicator in synthesis_indicators if indicator in response.lower()) / len(synthesis_indicators)
        
        # Analyze depth
        depth_indicators = ["because", "suggests", "indicates", "reflects", "demonstrates", "reveals"]
        depth_score = sum(1 for indicator in depth_indicators if indicator in response.lower()) / len(depth_indicators)
        
        overall_synthesis = (synthesis_score + depth_score) / 2
        
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  🔬 Synthesis Quality: {overall_synthesis:.3f} ({'🟢 High' if overall_synthesis > 0.6 else '🟡 Medium' if overall_synthesis > 0.3 else '🔴 Low'})")
        print(f"  📊 Depth Score: {depth_score:.3f}")
        print(f"  📝 Response: {len(response)} chars")
        print(f"  💭 Preview: {response[:100]}...   ")
        print()
        
        test_results["synthesis_tests"].append({
            "test_number": i,
            "query": test["query"],
            "response": response,
            "synthesis_type": test["synthesis_type"],
            "processing_time": processing_time,
            "synthesis_score": overall_synthesis,
            "depth_score": depth_score
        })
    
    # Final Analysis
    print("\n🧠 DAY 6 ADVANCED REASONING ANALYSIS")
    print("=" * 60)
    
    # Calculate overall metrics
    avg_reasoning_quality = sum(t["reasoning_quality"] for t in test_results["reasoning_tests"]) / len(test_results["reasoning_tests"])
    avg_memory_integration = sum(t["memory_integration"] for t in test_results["reasoning_tests"]) / len(test_results["reasoning_tests"])
    avg_problem_solving = sum(t["problem_solving_score"] for t in test_results["problem_solving_tests"]) / len(test_results["problem_solving_tests"])
    avg_synthesis = sum(t["synthesis_score"] for t in test_results["synthesis_tests"]) / len(test_results["synthesis_tests"])
    avg_processing_time = sum(t["processing_time"] for tests in [test_results["reasoning_tests"], test_results["problem_solving_tests"], test_results["synthesis_tests"]] for t in tests) / sum(len(tests) for tests in [test_results["reasoning_tests"], test_results["problem_solving_tests"], test_results["synthesis_tests"]])
    
    print(f"🧠 REASONING ANALYSIS:")
    print(f"   Average Reasoning Quality: {avg_reasoning_quality:.3f}")
    print(f"   Memory Integration: {avg_memory_integration:.3f}")
    print(f"   High-Quality Reasoning: {sum(1 for t in test_results['reasoning_tests'] if t['reasoning_quality'] > 0.6)}/{len(test_results['reasoning_tests'])} ({sum(1 for t in test_results['reasoning_tests'] if t['reasoning_quality'] > 0.6)/len(test_results['reasoning_tests'])*100:.1f}%)")
    print()
    
    print(f"🔧 PROBLEM-SOLVING ANALYSIS:")
    print(f"   Average Problem-Solving: {avg_problem_solving:.3f}")
    print(f"   High-Quality Solutions: {sum(1 for t in test_results['problem_solving_tests'] if t['problem_solving_score'] > 0.6)}/{len(test_results['problem_solving_tests'])} ({sum(1 for t in test_results['problem_solving_tests'] if t['problem_solving_score'] > 0.6)/len(test_results['problem_solving_tests'])*100:.1f}%)")
    print()
    
    print(f"🔬 SYNTHESIS ANALYSIS:")
    print(f"   Average Synthesis Quality: {avg_synthesis:.3f}")
    print(f"   High-Quality Synthesis: {sum(1 for t in test_results['synthesis_tests'] if t['synthesis_score'] > 0.6)}/{len(test_results['synthesis_tests'])} ({sum(1 for t in test_results['synthesis_tests'] if t['synthesis_score'] > 0.6)/len(test_results['synthesis_tests'])*100:.1f}%)")
    print()
    
    print(f"⚡ PERFORMANCE ANALYSIS:")
    print(f"   Average Processing: {avg_processing_time:.3f}s")
    processing_stability = max(t["processing_time"] for tests in [test_results["reasoning_tests"], test_results["problem_solving_tests"], test_results["synthesis_tests"]] for t in tests) - min(t["processing_time"] for tests in [test_results["reasoning_tests"], test_results["problem_solving_tests"], test_results["synthesis_tests"]] for t in tests)
    print(f"   Processing Stability: {processing_stability:.4f}s")
    print(f"   Rating: {'🟢 Excellent' if processing_stability < 0.01 else '🟡 Good' if processing_stability < 0.1 else '🔴 Needs Improvement'}")
    print()
    
    # Get final agency index
    agency_result = assistant.env.compute_agency_index()
    final_agency = agency_result.get('agency_index', 0.0) if isinstance(agency_result, dict) else agency_result
    print(f"🎯 ADVANCED REASONING SYSTEM HEALTH:")
    print(f"   Final Agency Index: {final_agency:.3f}")
    
    # Component analysis
    try:
        if hasattr(assistant.env, 'get_agency_components'):
            components = assistant.env.get_agency_components()
        elif isinstance(agency_result, dict) and 'components' in agency_result:
            components = agency_result['components']
        else:
            components = {}
        
        if components:
            print(f"   Component Analysis:")
            for component, value in components.items():
                trend = "📈" if value > 0.5 else "📉" if value < 0.1 else ""
                print(f"     {component}: {value:.3f} {trend}")
        else:
            print(f"   Component Analysis: Not available")
    except Exception as e:
        print(f"   Component Analysis: Error accessing components")
    
    # Store final metrics
    test_results["performance_metrics"] = {
        "avg_reasoning_quality": avg_reasoning_quality,
        "avg_memory_integration": avg_memory_integration,
        "avg_problem_solving": avg_problem_solving,
        "avg_synthesis": avg_synthesis,
        "avg_processing_time": avg_processing_time,
        "processing_stability": processing_stability,
        "final_agency_index": final_agency
    }
    
    test_results["agency_analysis"] = components
    test_results["end_time"] = time.time()
    
    # Save results
    results_file = "30_day_data/day6_reasoning_results.json"
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n💾 Day 6 results saved to: {results_file}")
    
    # Recommendations for Day 7
    print(f"\n🎯 RECOMMENDATIONS FOR DAY 7:")
    print("=" * 60)
    
    if avg_reasoning_quality < 0.5:
        print("⚠️ Reasoning quality needs improvement")
        print("🔧 Consider: Enhanced logical inference mechanisms")
    
    if avg_memory_integration < 0.7:
        print("⚠️ Memory integration could be stronger")
        print("🔧 Consider: Better memory-reasoning connection")
    
    if avg_problem_solving < 0.5:
        print("⚠️ Problem-solving capabilities need development")
        print("🔧 Consider: Multi-step reasoning enhancement")
    
    if avg_synthesis < 0.5:
        print("⚠️ Synthesis abilities need improvement")
        print("🔧 Consider: Cross-domain integration mechanisms")
    
    print("🎯 Day 7 will test creative problem-solving and innovation")
    print("🔧 Consider: Creative reasoning and novel solution generation")
    print("📈 Overall: Monitor reasoning chain development and goal-directed behavior")
    
    print(f"\n🎉 DAY 6 COMPLETE!")
    print("Ready for Day 7: Creative Problem-Solving and Innovation")
    
    assistant.end_session()
    return test_results

if __name__ == "__main__":
    results = run_day6_testing()
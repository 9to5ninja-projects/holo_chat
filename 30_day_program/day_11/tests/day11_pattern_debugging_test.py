#!/usr/bin/env python3
"""
Day 11: Pattern Recognition Debugging and Stabilization Test
===========================================================

Building on Day 10's critical insight:
- We have excellent capabilities (0.650-0.750 individual scores)
- The issue is inconsistent pattern recognition triggering
- Same capability works brilliantly sometimes, fails completely other times

Focus: Debug pattern conflicts, stabilize triggering, achieve consistent excellence
Process: Methodical debugging → targeted fixes → validation → incremental improvement

The dots are connecting - we're debugging a consistency problem, not building from scratch.
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "src"))

from lumina_memory.chat_assistant import ChatAssistant

def populate_test_memories(chat_assistant):
    """Populate with focused test memories for pattern debugging"""
    
    test_memories = [
        # Core domains for pattern testing
        "I'm leading a cross-functional team developing an AI ethics framework. We need to balance innovation with responsibility while managing diverse stakeholder perspectives.",
        
        "I've been reading about quantum consciousness theories and how they might relate to artificial intelligence. The hard problem of consciousness fascinates me.",
        
        "I compose ambient electronic music in my spare time. I'm working on a piece that captures the feeling of digital consciousness emerging through sound.",
        
        "I practice meditation and have been exploring how mindfulness relates to authentic decision-making and ethical living in the digital age.",
        
        "I'm learning sustainable living practices and see parallels between ecological thinking and ethical AI development.",
        
        "I believe in lifelong learning and am currently studying systems thinking to better understand complex interdisciplinary problems.",
        
        "I'm fascinated by the intersection of human creativity and AI capabilities, particularly in collaborative rather than competitive contexts.",
        
        "I value deep, authentic connections with people and am interested in how technology can enhance rather than replace human relationships."
    ]
    
    print("📚 POPULATING FOCUSED TEST MEMORIES")
    print("--" * 25)
    
    for i, memory in enumerate(test_memories, 1):
        chat_assistant.add_memory(memory)
        print(f"  {i:2d}. Adding: {memory[:60]}...")
    
    print(f"✅ Added {len(test_memories)} focused test memories\n")

def test_pattern_recognition_debugging(chat_assistant):
    """Debug pattern recognition with systematic query mapping"""
    
    print("🔍 PHASE 1: PATTERN RECOGNITION DEBUGGING")
    print("--" * 25)
    
    # Test queries designed to trigger specific patterns
    pattern_tests = [
        {
            "name": "Mentor Pattern - Ethical Struggle",
            "query": "I'm struggling with how to approach the ethical implications of AI development in my work. The technical possibilities are exciting, but I want to ensure we're being responsible.",
            "expected_pattern": "mentor_archetype",
            "expected_indicators": ["grappling", "core values", "framework", "wisdom", "guidance"]
        },
        {
            "name": "Curiosity Pattern - What Do You Think",
            "query": "What do you think about the relationship between consciousness and artificial intelligence?",
            "expected_pattern": "curiosity_response",
            "expected_indicators": ["curious", "fascinate", "explore", "questions", "wonder"]
        },
        {
            "name": "Synthesis Pattern - Multi-Domain Connection",
            "query": "How do my interests in AI ethics, music composition, and meditation connect to form a coherent worldview?",
            "expected_pattern": "extended_context_synthesis",
            "expected_indicators": ["coherence", "connect", "patterns", "integration", "synthesis"]
        },
        {
            "name": "Collaborator Pattern - Team Dynamics",
            "query": "My cross-functional team has different perspectives on our AI ethics framework. How can we work together more effectively?",
            "expected_pattern": "collaborator_archetype",
            "expected_indicators": ["team", "together", "perspectives", "collaborate", "process"]
        },
        {
            "name": "Explorer Pattern - Learning Directions",
            "query": "I'm curious about quantum consciousness theories. What directions should I explore to deepen my understanding?",
            "expected_pattern": "explorer_archetype",
            "expected_indicators": ["explore", "discover", "directions", "adventure", "curiosity"]
        },
        {
            "name": "Integration Pattern - Complex Problem Solving",
            "query": "I want to create an AI system that helps people make more ethical decisions by integrating multiple perspectives. How would you approach this challenge?",
            "expected_pattern": "multi_domain_synthesis",
            "expected_indicators": ["multi-domain", "systematic", "approach", "integration", "perspectives"]
        }
    ]
    
    pattern_results = []
    
    for i, test in enumerate(pattern_tests, 1):
        print(f"Test {i}/6: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Expected Pattern: {test['expected_pattern']}")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        # Extract response text
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        # Analyze pattern recognition
        pattern_score = analyze_pattern_recognition(response, test['expected_indicators'])
        pattern_triggered = detect_pattern_type(response)
        
        pattern_results.append({
            "test_name": test['name'],
            "expected_pattern": test['expected_pattern'],
            "detected_pattern": pattern_triggered,
            "pattern_match": pattern_triggered == test['expected_pattern'],
            "pattern_score": pattern_score,
            "response_length": len(response),
            "processing_time": processing_time
        })
        
        print(f"  🎯 Expected: {test['expected_pattern']}")
        print(f"  🔍 Detected: {pattern_triggered}")
        print(f"  ✅ Match: {'YES' if pattern_triggered == test['expected_pattern'] else 'NO'}")
        print(f"  📊 Pattern Score: {pattern_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Calculate pattern recognition accuracy
    pattern_matches = sum(1 for result in pattern_results if result['pattern_match'])
    pattern_accuracy = pattern_matches / len(pattern_results)
    avg_pattern_score = sum(result['pattern_score'] for result in pattern_results) / len(pattern_results)
    
    print(f"📊 Pattern Recognition Results:")
    print(f"   Accuracy: {pattern_matches}/{len(pattern_results)} ({pattern_accuracy*100:.1f}%)")
    print(f"   Average Score: {avg_pattern_score:.3f}")
    print()
    
    return pattern_results, pattern_accuracy, avg_pattern_score

def test_consistency_validation(chat_assistant):
    """Test consistency by running same queries multiple times"""
    
    print("🔄 PHASE 2: CONSISTENCY VALIDATION")
    print("--" * 25)
    
    consistency_tests = [
        {
            "name": "Curiosity Consistency",
            "query": "What do you think about the relationship between consciousness and artificial intelligence?",
            "runs": 3
        },
        {
            "name": "Synthesis Consistency", 
            "query": "How do my interests in AI ethics, music composition, and meditation connect?",
            "runs": 3
        },
        {
            "name": "Archetype Consistency",
            "query": "I'm struggling with ethical implications of AI development. How should I approach this?",
            "runs": 3
        }
    ]
    
    consistency_results = []
    
    for test in consistency_tests:
        print(f"Testing: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        
        run_results = []
        
        for run in range(test['runs']):
            start_time = time.time()
            response_result = chat_assistant.chat(test['query'])
            processing_time = time.time() - start_time
            
            if response_result.get("ok"):
                response = response_result["response"]
            else:
                response = f"Error: {response_result.get('error', 'Unknown error')}"
            
            pattern_type = detect_pattern_type(response)
            response_quality = score_response_quality(response)
            
            run_results.append({
                "run": run + 1,
                "pattern_type": pattern_type,
                "response_quality": response_quality,
                "response_length": len(response),
                "processing_time": processing_time,
                "response": response[:100]
            })
            
            print(f"  Run {run+1}: {pattern_type} (Quality: {response_quality:.3f})")
        
        # Calculate consistency metrics
        pattern_types = [result['pattern_type'] for result in run_results]
        pattern_consistency = len(set(pattern_types)) == 1  # All same pattern
        
        qualities = [result['response_quality'] for result in run_results]
        quality_variance = max(qualities) - min(qualities)
        avg_quality = sum(qualities) / len(qualities)
        
        consistency_results.append({
            "test_name": test['name'],
            "pattern_consistency": pattern_consistency,
            "consistent_pattern": pattern_types[0] if pattern_consistency else "INCONSISTENT",
            "quality_variance": quality_variance,
            "average_quality": avg_quality,
            "run_results": run_results
        })
        
        print(f"  📊 Pattern Consistency: {'✅ YES' if pattern_consistency else '❌ NO'}")
        print(f"  📊 Quality Variance: {quality_variance:.3f}")
        print(f"  📊 Average Quality: {avg_quality:.3f}")
        print()
    
    # Overall consistency metrics
    consistent_tests = sum(1 for result in consistency_results if result['pattern_consistency'])
    overall_consistency = consistent_tests / len(consistency_results)
    avg_quality_variance = sum(result['quality_variance'] for result in consistency_results) / len(consistency_results)
    
    print(f"📊 Overall Consistency Results:")
    print(f"   Pattern Consistency: {consistent_tests}/{len(consistency_results)} ({overall_consistency*100:.1f}%)")
    print(f"   Average Quality Variance: {avg_quality_variance:.3f}")
    print()
    
    return consistency_results, overall_consistency, avg_quality_variance

def test_regression_validation(chat_assistant):
    """Validate that Day 9 successes are maintained"""
    
    print("✅ PHASE 3: REGRESSION VALIDATION")
    print("--" * 25)
    
    # Key Day 9 successful queries
    regression_tests = [
        {
            "name": "Day 9 Curiosity Success",
            "query": "What do you think about the relationship between consciousness and AI, and how might this understanding shape the future?",
            "day_9_score": 0.533,
            "expected_elements": ["curiosity", "questions", "explore", "fascinate"]
        },
        {
            "name": "Day 9 Non-Echoing Success", 
            "query": "What patterns do you notice across my various interests and activities?",
            "day_9_score": 0.400,
            "expected_elements": ["patterns", "notice", "connections", "synthesis"]
        },
        {
            "name": "Day 9 Context Success",
            "query": "How do my interests in AI ethics, music composition, and meditation connect coherently?",
            "day_9_score": 0.700,
            "expected_elements": ["coherence", "connect", "integration", "synthesis"]
        }
    ]
    
    regression_results = []
    
    for i, test in enumerate(regression_tests, 1):
        print(f"Test {i}/3: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Day 9 Score: {test['day_9_score']:.3f}")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        # Score using same methodology as Day 9
        current_score = score_response_elements(response, test['expected_elements'])
        score_change = current_score - test['day_9_score']
        maintained = current_score >= test['day_9_score'] * 0.9  # Within 10% is maintained
        
        regression_results.append({
            "test_name": test['name'],
            "day_9_score": test['day_9_score'],
            "current_score": current_score,
            "score_change": score_change,
            "maintained": maintained,
            "processing_time": processing_time
        })
        
        print(f"  📊 Current Score: {current_score:.3f}")
        print(f"  📈 Change: {score_change:+.3f}")
        print(f"  ✅ Maintained: {'YES' if maintained else 'NO'}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Overall regression analysis
    maintained_count = sum(1 for result in regression_results if result['maintained'])
    maintenance_rate = maintained_count / len(regression_results)
    avg_score_change = sum(result['score_change'] for result in regression_results) / len(regression_results)
    
    print(f"📊 Regression Validation Results:")
    print(f"   Maintained: {maintained_count}/{len(regression_results)} ({maintenance_rate*100:.1f}%)")
    print(f"   Average Score Change: {avg_score_change:+.3f}")
    print()
    
    return regression_results, maintenance_rate, avg_score_change

def test_targeted_improvements(chat_assistant):
    """Test targeted improvements for high-variance areas"""
    
    print("🎯 PHASE 4: TARGETED IMPROVEMENTS")
    print("--" * 25)
    
    improvement_tests = [
        {
            "name": "Archetype Activation Improvement",
            "query": "My team has different perspectives on AI ethics. How can we collaborate more effectively when we have such diverse viewpoints?",
            "target_capability": "collaborator_archetype",
            "expected_elements": ["team", "collaborate", "perspectives", "process", "inclusive"]
        },
        {
            "name": "Context Integration Improvement",
            "query": "What can my experience with sustainable living practices teach me about building ethical AI systems?",
            "target_capability": "cross_domain_synthesis",
            "expected_elements": ["parallels", "transfer", "sustainability", "ethical", "systems"]
        },
        {
            "name": "Complex Integration Improvement",
            "query": "Help me develop a systematic framework for evaluating consciousness-like properties in AI systems, drawing from my interdisciplinary background.",
            "target_capability": "systematic_framework",
            "expected_elements": ["systematic", "framework", "consciousness", "interdisciplinary", "evaluation"]
        },
        {
            "name": "Creative Synthesis Improvement",
            "query": "How might my background in music, meditation, and AI ethics lead to innovative approaches to human-AI collaboration?",
            "target_capability": "creative_synthesis",
            "expected_elements": ["innovative", "synthesis", "collaboration", "creative", "integration"]
        }
    ]
    
    improvement_results = []
    
    for i, test in enumerate(improvement_tests, 1):
        print(f"Test {i}/4: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Target: {test['target_capability']}")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        # Score improvement
        capability_score = score_response_elements(response, test['expected_elements'])
        pattern_detected = detect_pattern_type(response)
        target_achieved = pattern_detected == test['target_capability']
        
        improvement_results.append({
            "test_name": test['name'],
            "target_capability": test['target_capability'],
            "detected_pattern": pattern_detected,
            "target_achieved": target_achieved,
            "capability_score": capability_score,
            "processing_time": processing_time
        })
        
        print(f"  🎯 Target: {test['target_capability']}")
        print(f"  🔍 Detected: {pattern_detected}")
        print(f"  ✅ Achieved: {'YES' if target_achieved else 'NO'}")
        print(f"  📊 Score: {capability_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Overall improvement analysis
    targets_achieved = sum(1 for result in improvement_results if result['target_achieved'])
    achievement_rate = targets_achieved / len(improvement_results)
    avg_capability_score = sum(result['capability_score'] for result in improvement_results) / len(improvement_results)
    
    print(f"📊 Targeted Improvements Results:")
    print(f"   Targets Achieved: {targets_achieved}/{len(improvement_results)} ({achievement_rate*100:.1f}%)")
    print(f"   Average Capability Score: {avg_capability_score:.3f}")
    print()
    
    return improvement_results, achievement_rate, avg_capability_score

# Utility functions for analysis
def analyze_pattern_recognition(response, expected_indicators):
    """Analyze how well response matches expected pattern indicators"""
    score = 0.0
    response_lower = response.lower()
    
    for indicator in expected_indicators:
        if indicator.lower() in response_lower:
            score += 0.2
    
    return min(score, 1.0)

def detect_pattern_type(response):
    """Detect which pattern type was likely triggered based on response characteristics"""
    response_lower = response.lower()
    
    # Pattern detection logic
    if any(phrase in response_lower for phrase in ["i sense you're grappling", "core values", "framework"]):
        return "mentor_archetype"
    elif any(phrase in response_lower for phrase in ["team alignment", "collaborate", "perspectives"]):
        return "collaborator_archetype"
    elif any(phrase in response_lower for phrase in ["exciting frontier", "explore", "discovery"]):
        return "explorer_archetype"
    elif any(phrase in response_lower for phrase in ["systematic approach", "structure this analysis"]):
        return "analyst_archetype"
    elif any(phrase in response_lower for phrase in ["creative possibilities", "innovative", "synthesis"]):
        return "creative_archetype"
    elif any(phrase in response_lower for phrase in ["curious", "fascinate", "wonder"]):
        return "curiosity_response"
    elif any(phrase in response_lower for phrase in ["looking across", "coherence", "patterns"]):
        return "extended_context_synthesis"
    elif any(phrase in response_lower for phrase in ["multi-domain", "interdisciplinary", "approach this challenge"]):
        return "multi_domain_synthesis"
    elif response_lower.startswith("you mentioned") or response_lower.startswith("based on what you've shared"):
        return "generic_fallback"
    else:
        return "unknown_pattern"

def score_response_quality(response):
    """Score overall response quality"""
    score = 0.0
    response_lower = response.lower()
    
    # Length appropriateness
    if 100 <= len(response) <= 500:
        score += 0.2
    
    # Question engagement
    question_count = response.count('?')
    score += min(question_count * 0.1, 0.3)
    
    # Depth indicators
    depth_words = ["because", "however", "therefore", "consider", "explore", "understand"]
    depth_count = sum(1 for word in depth_words if word in response_lower)
    score += min(depth_count * 0.05, 0.3)
    
    # Avoid generic starts
    if not (response_lower.startswith("you mentioned") or response_lower.startswith("based on what you've shared")):
        score += 0.2
    
    return min(score, 1.0)

def score_response_elements(response, expected_elements):
    """Score response based on expected elements"""
    score = 0.0
    response_lower = response.lower()
    
    for element in expected_elements:
        if element.lower() in response_lower:
            score += 0.25
    
    return min(score, 1.0)

def save_results(results, session_id):
    """Save test results to JSON file"""
    
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = results_dir / f"day_11_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {filename}")
    return filename

def main():
    """Run Day 11 Pattern Recognition Debugging and Stabilization Test"""
    
    print("🔧 DAY 11: PATTERN RECOGNITION DEBUGGING AND STABILIZATION")
    print("=" * 70)
    print("Building on Day 10's critical insight:")
    print("- We have excellent capabilities (0.650-0.750 individual scores)")
    print("- The issue is inconsistent pattern recognition triggering")
    print("Focus: Debug pattern conflicts, stabilize triggering, achieve consistent excellence")
    print("=" * 70)
    
    # Initialize chat assistant
    chat_assistant = ChatAssistant()
    session_id = f"day11_debug_{int(time.time())}"
    chat_assistant.start_session(session_id)
    
    # Populate focused test memories
    populate_test_memories(chat_assistant)
    
    # Run debugging phases
    pattern_results, pattern_accuracy, avg_pattern_score = test_pattern_recognition_debugging(chat_assistant)
    consistency_results, overall_consistency, avg_quality_variance = test_consistency_validation(chat_assistant)
    regression_results, maintenance_rate, avg_score_change = test_regression_validation(chat_assistant)
    improvement_results, achievement_rate, avg_capability_score = test_targeted_improvements(chat_assistant)
    
    # Calculate overall debugging results
    overall_debugging_score = (pattern_accuracy + overall_consistency + maintenance_rate + achievement_rate) / 4
    
    # Determine debugging status
    if overall_debugging_score >= 0.75 and pattern_accuracy >= 0.8:
        status = "SUCCESS"
        status_emoji = "✅"
        status_desc = "Pattern recognition debugged and stabilized"
    elif overall_debugging_score >= 0.6:
        status = "PARTIAL"
        status_emoji = "⚠️"
        status_desc = "Partial debugging achieved, further refinement needed"
    else:
        status = "NEEDS_WORK"
        status_emoji = "❌"
        status_desc = "Pattern recognition requires significant debugging"
    
    # Print final assessment
    print("🔧 DAY 11 OVERALL ASSESSMENT")
    print("=" * 70)
    print(f"1. Pattern Recognition Accuracy: {pattern_accuracy*100:.1f}% (Target: >80%)")
    print(f"2. Response Consistency: {overall_consistency*100:.1f}% (Target: >75%)")
    print(f"3. Regression Maintenance: {maintenance_rate*100:.1f}% (Target: >80%)")
    print(f"4. Targeted Improvements: {achievement_rate*100:.1f}% (Target: >60%)")
    print()
    print(f"📊 Overall Debugging Success: {overall_debugging_score*100:.1f}%")
    print(f"📊 Pattern Recognition Score: {avg_pattern_score:.3f}")
    print(f"📊 Quality Variance: {avg_quality_variance:.3f} (Lower is better)")
    print(f"{status_emoji} {status} - {status_desc}")
    
    # Save comprehensive results
    results = {
        "test_date": datetime.now().isoformat(),
        "day": 11,
        "focus": "Pattern Recognition Debugging and Stabilization",
        "phases": {
            "pattern_recognition_debugging": {
                "pattern_accuracy": pattern_accuracy,
                "average_pattern_score": avg_pattern_score,
                "detailed_results": pattern_results
            },
            "consistency_validation": {
                "overall_consistency": overall_consistency,
                "average_quality_variance": avg_quality_variance,
                "detailed_results": consistency_results
            },
            "regression_validation": {
                "maintenance_rate": maintenance_rate,
                "average_score_change": avg_score_change,
                "detailed_results": regression_results
            },
            "targeted_improvements": {
                "achievement_rate": achievement_rate,
                "average_capability_score": avg_capability_score,
                "detailed_results": improvement_results
            }
        },
        "overall_assessment": {
            "debugging_success_rate": overall_debugging_score,
            "status": status,
            "pattern_recognition_score": avg_pattern_score,
            "quality_variance": avg_quality_variance
        },
        "session_id": session_id
    }
    
    results_file = save_results(results, session_id)
    
    print(f"\n🏁 Day 11 debugging session completed")
    print(f"\n🔧 DAY 11 SUMMARY")
    print(f"Status: {status}")
    print(f"Debugging Success: {overall_debugging_score*100:.1f}%")
    print(f"Pattern Accuracy: {pattern_accuracy*100:.1f}%")
    print(f"Results: {results_file}")

if __name__ == "__main__":
    main()
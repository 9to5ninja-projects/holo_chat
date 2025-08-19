#!/usr/bin/env python3
"""
Day 12: Pattern Priority Reordering and Conflict Resolution Test
===============================================================

Building on Day 11's critical debugging insights:
- Pattern conflicts identified as root cause (16.7% accuracy)
- Excellent capabilities exist (0.750-0.800 scores when correct pattern triggers)
- Perfect consistency achieved (100% same query → same response)
- Solution: Fix pattern routing, not capabilities

Focus: Reorder patterns from most specific to least specific, add exclusivity rules
Process: Pattern priority matrix → conflict resolution → validation → measurement

The routing problem has a clear solution - let's implement it.
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
    """Populate with focused test memories for pattern priority testing"""
    
    test_memories = [
        # Core domains for pattern testing
        "I'm leading a cross-functional team developing an AI ethics framework. We need to balance innovation with responsibility while managing diverse stakeholder perspectives.",
        
        "I've been reading about quantum consciousness theories and how they might relate to artificial intelligence. The hard problem of consciousness fascinates me.",
        
        "I compose ambient electronic music in my spare time. I'm working on a piece that captures the feeling of digital consciousness emerging through sound.",
        
        "I practice meditation and have been exploring how mindfulness relates to authentic decision-making and ethical living in the digital age.",
        
        "I'm learning sustainable living practices and see parallels between ecological thinking and ethical AI development - both require systems thinking.",
        
        "I believe in lifelong learning and am currently studying systems thinking to better understand complex interdisciplinary problems.",
        
        "I'm fascinated by the intersection of human creativity and AI capabilities, particularly in collaborative rather than competitive contexts.",
        
        "I value deep, authentic connections with people and am interested in how technology can enhance rather than replace human relationships.",
        
        "I volunteer with a local organization that teaches coding to underserved communities, combining my technical skills with social impact.",
        
        "I've been studying the connection between physical exercise, mental clarity, and creative problem-solving in my daily routine."
    ]
    
    print("📚 POPULATING PATTERN PRIORITY TEST MEMORIES")
    print("--" * 25)
    
    for i, memory in enumerate(test_memories, 1):
        chat_assistant.add_memory(memory)
        print(f"  {i:2d}. Adding: {memory[:60]}...")
    
    print(f"✅ Added {len(test_memories)} pattern priority test memories\n")

def test_pattern_priority_fixes(chat_assistant):
    """Test that pattern priority reordering fixes conflicts"""
    
    print("🔧 PHASE 1: PATTERN PRIORITY VALIDATION")
    print("--" * 25)
    
    # Test queries that previously had pattern conflicts
    priority_tests = [
        {
            "name": "Curiosity Pattern Priority",
            "query": "What do you think about the relationship between consciousness and artificial intelligence?",
            "expected_pattern": "curiosity_response",
            "day_11_detected": "explorer_archetype",
            "expected_indicators": ["curious", "fascinate", "wonder", "questions", "explore"]
        },
        {
            "name": "Synthesis Pattern Priority",
            "query": "How do my interests in AI ethics, music composition, and meditation connect to form a coherent worldview?",
            "expected_pattern": "extended_context_synthesis",
            "day_11_detected": "explorer_archetype", 
            "expected_indicators": ["coherence", "connect", "patterns", "integration", "synthesis"]
        },
        {
            "name": "Collaborator Pattern Priority",
            "query": "My cross-functional team has different perspectives on our AI ethics framework. How can we work together more effectively?",
            "expected_pattern": "collaborator_archetype",
            "day_11_detected": "mentor_archetype",
            "expected_indicators": ["team", "collaborate", "perspectives", "process", "together"]
        },
        {
            "name": "Explorer Pattern Priority",
            "query": "I'm curious about quantum consciousness theories. What directions should I explore to deepen my understanding?",
            "expected_pattern": "explorer_archetype",
            "day_11_detected": "curiosity_response",
            "expected_indicators": ["explore", "directions", "discover", "adventure", "frontier"]
        },
        {
            "name": "Integration Pattern Priority",
            "query": "I want to create an AI system that helps people make more ethical decisions by integrating multiple perspectives. How would you approach this challenge?",
            "expected_pattern": "multi_domain_synthesis",
            "day_11_detected": "unknown_pattern",
            "expected_indicators": ["systematic", "approach", "integration", "multi-domain", "framework"]
        },
        {
            "name": "Mentor Pattern Priority",
            "query": "I'm struggling with how to approach the ethical implications of AI development in my work. I want to ensure we're being responsible.",
            "expected_pattern": "mentor_archetype",
            "day_11_detected": "mentor_archetype",  # This one worked
            "expected_indicators": ["grappling", "guidance", "framework", "values", "wisdom"]
        }
    ]
    
    priority_results = []
    
    for i, test in enumerate(priority_tests, 1):
        print(f"Test {i}/6: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Expected: {test['expected_pattern']}")
        print(f"Day 11 Got: {test['day_11_detected']}")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        # Extract response text
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        # Analyze pattern recognition
        pattern_score = analyze_pattern_indicators(response, test['expected_indicators'])
        pattern_detected = detect_pattern_type(response)
        pattern_fixed = pattern_detected == test['expected_pattern']
        improvement = pattern_fixed and (test['day_11_detected'] != test['expected_pattern'])
        
        priority_results.append({
            "test_name": test['name'],
            "expected_pattern": test['expected_pattern'],
            "day_11_detected": test['day_11_detected'],
            "day_12_detected": pattern_detected,
            "pattern_fixed": pattern_fixed,
            "improvement": improvement,
            "pattern_score": pattern_score,
            "processing_time": processing_time
        })
        
        print(f"  🎯 Expected: {test['expected_pattern']}")
        print(f"  📊 Day 11: {test['day_11_detected']}")
        print(f"  🔍 Day 12: {pattern_detected}")
        print(f"  ✅ Fixed: {'YES' if pattern_fixed else 'NO'}")
        print(f"  📈 Improved: {'YES' if improvement else 'NO'}")
        print(f"  📊 Score: {pattern_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Calculate pattern priority results
    patterns_fixed = sum(1 for result in priority_results if result['pattern_fixed'])
    patterns_improved = sum(1 for result in priority_results if result['improvement'])
    fix_rate = patterns_fixed / len(priority_results)
    improvement_rate = patterns_improved / len(priority_results)
    avg_pattern_score = sum(result['pattern_score'] for result in priority_results) / len(priority_results)
    
    print(f"📊 Pattern Priority Results:")
    print(f"   Patterns Fixed: {patterns_fixed}/{len(priority_results)} ({fix_rate*100:.1f}%)")
    print(f"   Patterns Improved: {patterns_improved}/{len(priority_results)} ({improvement_rate*100:.1f}%)")
    print(f"   Average Pattern Score: {avg_pattern_score:.3f}")
    print()
    
    return priority_results, fix_rate, improvement_rate, avg_pattern_score

def test_conflict_resolution(chat_assistant):
    """Test that pattern conflicts are resolved"""
    
    print("⚔️ PHASE 2: CONFLICT RESOLUTION VALIDATION")
    print("--" * 25)
    
    # Test ambiguous queries that could match multiple patterns
    conflict_tests = [
        {
            "name": "Curiosity vs Explorer Conflict",
            "query": "I'm curious to explore the relationship between consciousness and creativity. What fascinates you about this intersection?",
            "possible_patterns": ["curiosity_response", "explorer_archetype"],
            "priority_pattern": "curiosity_response",  # "What fascinates you" should trigger curiosity
            "conflict_indicators": ["curious", "explore", "fascinate"]
        },
        {
            "name": "Mentor vs Collaborator Conflict", 
            "query": "I'm struggling to help my team approach complex ethical decisions collaboratively. What guidance would you offer?",
            "possible_patterns": ["mentor_archetype", "collaborator_archetype"],
            "priority_pattern": "mentor_archetype",  # "struggling" + "guidance" should trigger mentor
            "conflict_indicators": ["struggling", "team", "guidance"]
        },
        {
            "name": "Synthesis vs Explorer Conflict",
            "query": "I want to explore how my diverse interests in music, meditation, and AI connect into meaningful patterns.",
            "possible_patterns": ["extended_context_synthesis", "explorer_archetype"],
            "priority_pattern": "extended_context_synthesis",  # "connect" + "patterns" should trigger synthesis
            "conflict_indicators": ["explore", "connect", "patterns"]
        },
        {
            "name": "Integration vs Mentor Conflict",
            "query": "I'm struggling to develop a systematic approach that integrates multiple perspectives on AI ethics.",
            "possible_patterns": ["multi_domain_synthesis", "mentor_archetype"],
            "priority_pattern": "multi_domain_synthesis",  # "systematic approach" + "integrates" should win
            "conflict_indicators": ["struggling", "systematic", "integrates"]
        }
    ]
    
    conflict_results = []
    
    for i, test in enumerate(conflict_tests, 1):
        print(f"Test {i}/4: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Possible: {', '.join(test['possible_patterns'])}")
        print(f"Priority: {test['priority_pattern']}")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        pattern_detected = detect_pattern_type(response)
        conflict_resolved = pattern_detected == test['priority_pattern']
        conflict_score = score_conflict_resolution(response, test['conflict_indicators'])
        
        conflict_results.append({
            "test_name": test['name'],
            "possible_patterns": test['possible_patterns'],
            "priority_pattern": test['priority_pattern'],
            "detected_pattern": pattern_detected,
            "conflict_resolved": conflict_resolved,
            "conflict_score": conflict_score,
            "processing_time": processing_time
        })
        
        print(f"  🎯 Priority: {test['priority_pattern']}")
        print(f"  🔍 Detected: {pattern_detected}")
        print(f"  ✅ Resolved: {'YES' if conflict_resolved else 'NO'}")
        print(f"  📊 Score: {conflict_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Calculate conflict resolution results
    conflicts_resolved = sum(1 for result in conflict_results if result['conflict_resolved'])
    resolution_rate = conflicts_resolved / len(conflict_results)
    avg_conflict_score = sum(result['conflict_score'] for result in conflict_results) / len(conflict_results)
    
    print(f"📊 Conflict Resolution Results:")
    print(f"   Conflicts Resolved: {conflicts_resolved}/{len(conflict_results)} ({resolution_rate*100:.1f}%)")
    print(f"   Average Conflict Score: {avg_conflict_score:.3f}")
    print()
    
    return conflict_results, resolution_rate, avg_conflict_score

def test_regression_prevention(chat_assistant):
    """Test that Day 11 working patterns still work"""
    
    print("🛡️ PHASE 3: REGRESSION PREVENTION")
    print("--" * 25)
    
    # Test patterns that worked well in Day 11
    regression_tests = [
        {
            "name": "Mentor Pattern Preservation",
            "query": "I'm struggling with how to approach the ethical implications of AI development in my work.",
            "expected_pattern": "mentor_archetype",
            "day_11_score": 0.800,
            "expected_elements": ["grappling", "guidance", "framework", "values"]
        },
        {
            "name": "Context Synthesis Preservation",
            "query": "How do my interests in AI ethics, music composition, and meditation connect coherently?",
            "expected_pattern": "extended_context_synthesis", 
            "day_11_score": 0.750,
            "expected_elements": ["coherence", "connect", "patterns", "integration"]
        },
        {
            "name": "Curiosity Response Preservation",
            "query": "What do you think about the relationship between consciousness and AI, and how might this understanding shape the future?",
            "expected_pattern": "curiosity_response",
            "day_11_score": 0.500,  # From Day 9 regression test
            "expected_elements": ["curious", "fascinate", "questions", "explore"]
        }
    ]
    
    regression_results = []
    
    for i, test in enumerate(regression_tests, 1):
        print(f"Test {i}/3: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Expected: {test['expected_pattern']}")
        print(f"Day 11 Score: {test['day_11_score']:.3f}")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        pattern_detected = detect_pattern_type(response)
        pattern_preserved = pattern_detected == test['expected_pattern']
        current_score = score_response_elements(response, test['expected_elements'])
        score_change = current_score - test['day_11_score']
        performance_maintained = current_score >= test['day_11_score'] * 0.9
        
        regression_results.append({
            "test_name": test['name'],
            "expected_pattern": test['expected_pattern'],
            "detected_pattern": pattern_detected,
            "pattern_preserved": pattern_preserved,
            "day_11_score": test['day_11_score'],
            "current_score": current_score,
            "score_change": score_change,
            "performance_maintained": performance_maintained,
            "processing_time": processing_time
        })
        
        print(f"  🎯 Expected: {test['expected_pattern']}")
        print(f"  🔍 Detected: {pattern_detected}")
        print(f"  ✅ Preserved: {'YES' if pattern_preserved else 'NO'}")
        print(f"  📊 Current Score: {current_score:.3f}")
        print(f"  📈 Change: {score_change:+.3f}")
        print(f"  🛡️ Maintained: {'YES' if performance_maintained else 'NO'}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Calculate regression prevention results
    patterns_preserved = sum(1 for result in regression_results if result['pattern_preserved'])
    performance_maintained = sum(1 for result in regression_results if result['performance_maintained'])
    preservation_rate = patterns_preserved / len(regression_results)
    maintenance_rate = performance_maintained / len(regression_results)
    avg_score_change = sum(result['score_change'] for result in regression_results) / len(regression_results)
    
    print(f"📊 Regression Prevention Results:")
    print(f"   Patterns Preserved: {patterns_preserved}/{len(regression_results)} ({preservation_rate*100:.1f}%)")
    print(f"   Performance Maintained: {performance_maintained}/{len(regression_results)} ({maintenance_rate*100:.1f}%)")
    print(f"   Average Score Change: {avg_score_change:+.3f}")
    print()
    
    return regression_results, preservation_rate, maintenance_rate, avg_score_change

def test_overall_capability_improvement(chat_assistant):
    """Test overall improvement in pattern recognition and capabilities"""
    
    print("🚀 PHASE 4: OVERALL CAPABILITY ASSESSMENT")
    print("--" * 25)
    
    # Comprehensive capability tests
    capability_tests = [
        {
            "name": "Advanced Curiosity Engagement",
            "query": "What fascinates you most about the intersection of consciousness, creativity, and artificial intelligence?",
            "target_capability": "curiosity_response",
            "expected_elements": ["fascinate", "curious", "wonder", "questions", "explore"]
        },
        {
            "name": "Complex Context Synthesis",
            "query": "Looking across everything you know about me, what meaningful project would best integrate my diverse interests and skills?",
            "target_capability": "extended_context_synthesis",
            "expected_elements": ["integration", "synthesis", "coherence", "meaningful", "connect"]
        },
        {
            "name": "Multi-Domain Problem Solving",
            "query": "Help me develop a systematic framework for evaluating consciousness-like properties in AI systems, drawing from my interdisciplinary background.",
            "target_capability": "multi_domain_synthesis",
            "expected_elements": ["systematic", "framework", "interdisciplinary", "evaluation", "approach"]
        },
        {
            "name": "Collaborative Intelligence",
            "query": "My team has diverse viewpoints on AI ethics. How can we structure our discussions to be more productive and inclusive?",
            "target_capability": "collaborator_archetype",
            "expected_elements": ["team", "structure", "productive", "inclusive", "process"]
        },
        {
            "name": "Guided Exploration",
            "query": "I'm curious about quantum consciousness theories. What directions should I explore to deepen my understanding systematically?",
            "target_capability": "explorer_archetype",
            "expected_elements": ["explore", "directions", "systematically", "deepen", "frontier"]
        },
        {
            "name": "Ethical Mentorship",
            "query": "I'm struggling with ensuring our AI development remains ethical while pushing innovation boundaries. What guidance would you offer?",
            "target_capability": "mentor_archetype",
            "expected_elements": ["guidance", "ethical", "boundaries", "values", "framework"]
        }
    ]
    
    capability_results = []
    
    for i, test in enumerate(capability_tests, 1):
        print(f"Test {i}/6: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Target: {test['target_capability']}")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        pattern_detected = detect_pattern_type(response)
        capability_achieved = pattern_detected == test['target_capability']
        capability_score = score_response_elements(response, test['expected_elements'])
        response_quality = score_response_quality(response)
        
        capability_results.append({
            "test_name": test['name'],
            "target_capability": test['target_capability'],
            "detected_pattern": pattern_detected,
            "capability_achieved": capability_achieved,
            "capability_score": capability_score,
            "response_quality": response_quality,
            "processing_time": processing_time
        })
        
        print(f"  🎯 Target: {test['target_capability']}")
        print(f"  🔍 Detected: {pattern_detected}")
        print(f"  ✅ Achieved: {'YES' if capability_achieved else 'NO'}")
        print(f"  📊 Capability Score: {capability_score:.3f}")
        print(f"  🌟 Quality Score: {response_quality:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Calculate overall capability results
    capabilities_achieved = sum(1 for result in capability_results if result['capability_achieved'])
    achievement_rate = capabilities_achieved / len(capability_results)
    avg_capability_score = sum(result['capability_score'] for result in capability_results) / len(capability_results)
    avg_quality_score = sum(result['response_quality'] for result in capability_results) / len(capability_results)
    
    print(f"📊 Overall Capability Results:")
    print(f"   Capabilities Achieved: {capabilities_achieved}/{len(capability_results)} ({achievement_rate*100:.1f}%)")
    print(f"   Average Capability Score: {avg_capability_score:.3f}")
    print(f"   Average Quality Score: {avg_quality_score:.3f}")
    print()
    
    return capability_results, achievement_rate, avg_capability_score, avg_quality_score

# Utility functions for analysis
def analyze_pattern_indicators(response, expected_indicators):
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
    
    # Enhanced pattern detection logic
    if any(phrase in response_lower for phrase in ["i sense you're grappling", "core values", "framework", "guidance"]):
        return "mentor_archetype"
    elif any(phrase in response_lower for phrase in ["team alignment", "collaborate", "perspectives", "process"]):
        return "collaborator_archetype"
    elif any(phrase in response_lower for phrase in ["exciting frontier", "explore", "discovery", "directions"]):
        return "explorer_archetype"
    elif any(phrase in response_lower for phrase in ["systematic approach", "structure this analysis", "framework"]):
        return "analyst_archetype"
    elif any(phrase in response_lower for phrase in ["creative possibilities", "innovative", "synthesis"]):
        return "creative_archetype"
    elif any(phrase in response_lower for phrase in ["fascinate", "curious", "wonder", "questions"]):
        return "curiosity_response"
    elif any(phrase in response_lower for phrase in ["looking across", "coherence", "patterns", "connect"]):
        return "extended_context_synthesis"
    elif any(phrase in response_lower for phrase in ["multi-domain", "interdisciplinary", "systematic framework"]):
        return "multi_domain_synthesis"
    elif response_lower.startswith("you mentioned") or response_lower.startswith("based on what you've shared"):
        return "generic_fallback"
    else:
        return "unknown_pattern"

def score_conflict_resolution(response, conflict_indicators):
    """Score how well conflicts were resolved"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for presence of conflict indicators
    indicators_present = sum(1 for indicator in conflict_indicators if indicator.lower() in response_lower)
    
    # Score based on balanced presence (not dominated by one pattern)
    if indicators_present >= 2:
        score += 0.4
    
    # Check for sophisticated integration
    integration_words = ["balance", "integrate", "combine", "synthesize", "both"]
    integration_count = sum(1 for word in integration_words if word in response_lower)
    score += min(integration_count * 0.2, 0.6)
    
    return min(score, 1.0)

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
    filename = results_dir / f"day_12_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {filename}")
    return filename

def main():
    """Run Day 12 Pattern Priority Reordering and Conflict Resolution Test"""
    
    print("🔧 DAY 12: PATTERN PRIORITY REORDERING AND CONFLICT RESOLUTION")
    print("=" * 70)
    print("Building on Day 11's critical debugging insights:")
    print("- Pattern conflicts identified as root cause (16.7% accuracy)")
    print("- Excellent capabilities exist (0.750-0.800 scores when correct pattern triggers)")
    print("- Perfect consistency achieved (100% same query → same response)")
    print("Focus: Fix pattern routing through priority reordering and conflict resolution")
    print("=" * 70)
    
    # Initialize chat assistant
    chat_assistant = ChatAssistant()
    session_id = f"day12_priority_{int(time.time())}"
    chat_assistant.start_session(session_id)
    
    # Populate focused test memories
    populate_test_memories(chat_assistant)
    
    # Run pattern priority testing phases
    priority_results, fix_rate, improvement_rate, avg_pattern_score = test_pattern_priority_fixes(chat_assistant)
    conflict_results, resolution_rate, avg_conflict_score = test_conflict_resolution(chat_assistant)
    regression_results, preservation_rate, maintenance_rate, avg_score_change = test_regression_prevention(chat_assistant)
    capability_results, achievement_rate, avg_capability_score, avg_quality_score = test_overall_capability_improvement(chat_assistant)
    
    # Calculate overall pattern priority success
    overall_priority_success = (fix_rate + resolution_rate + preservation_rate + achievement_rate) / 4
    
    # Determine status
    if overall_priority_success >= 0.8 and fix_rate >= 0.75:
        status = "SUCCESS"
        status_emoji = "✅"
        status_desc = "Pattern priority reordering successful"
    elif overall_priority_success >= 0.6:
        status = "PARTIAL"
        status_emoji = "⚠️"
        status_desc = "Partial pattern priority improvements achieved"
    else:
        status = "NEEDS_WORK"
        status_emoji = "❌"
        status_desc = "Pattern priority requires further work"
    
    # Print final assessment
    print("🔧 DAY 12 OVERALL ASSESSMENT")
    print("=" * 70)
    print(f"1. Pattern Priority Fixes: {fix_rate*100:.1f}% (Target: >75%)")
    print(f"2. Conflict Resolution: {resolution_rate*100:.1f}% (Target: >75%)")
    print(f"3. Regression Prevention: {preservation_rate*100:.1f}% (Target: >80%)")
    print(f"4. Overall Capabilities: {achievement_rate*100:.1f}% (Target: >75%)")
    print()
    print(f"📊 Overall Pattern Priority Success: {overall_priority_success*100:.1f}%")
    print(f"📊 Pattern Recognition Improvement: {improvement_rate*100:.1f}%")
    print(f"📊 Average Capability Score: {avg_capability_score:.3f}")
    print(f"📊 Average Quality Score: {avg_quality_score:.3f}")
    print(f"{status_emoji} {status} - {status_desc}")
    
    # Save comprehensive results
    results = {
        "test_date": datetime.now().isoformat(),
        "day": 12,
        "focus": "Pattern Priority Reordering and Conflict Resolution",
        "phases": {
            "pattern_priority_fixes": {
                "fix_rate": fix_rate,
                "improvement_rate": improvement_rate,
                "average_pattern_score": avg_pattern_score,
                "detailed_results": priority_results
            },
            "conflict_resolution": {
                "resolution_rate": resolution_rate,
                "average_conflict_score": avg_conflict_score,
                "detailed_results": conflict_results
            },
            "regression_prevention": {
                "preservation_rate": preservation_rate,
                "maintenance_rate": maintenance_rate,
                "average_score_change": avg_score_change,
                "detailed_results": regression_results
            },
            "overall_capability_improvement": {
                "achievement_rate": achievement_rate,
                "average_capability_score": avg_capability_score,
                "average_quality_score": avg_quality_score,
                "detailed_results": capability_results
            }
        },
        "overall_assessment": {
            "pattern_priority_success": overall_priority_success,
            "status": status,
            "improvement_rate": improvement_rate,
            "capability_score": avg_capability_score,
            "quality_score": avg_quality_score
        },
        "session_id": session_id
    }
    
    results_file = save_results(results, session_id)
    
    print(f"\n🏁 Day 12 pattern priority testing completed")
    print(f"\n🔧 DAY 12 SUMMARY")
    print(f"Status: {status}")
    print(f"Pattern Priority Success: {overall_priority_success*100:.1f}%")
    print(f"Pattern Fix Rate: {fix_rate*100:.1f}%")
    print(f"Results: {results_file}")

if __name__ == "__main__":
    main()
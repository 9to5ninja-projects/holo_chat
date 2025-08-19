#!/usr/bin/env python3
"""
Day 13: Precision Pattern Fixes and Final Routing Optimization Test
==================================================================

Building on Day 12's major capability breakthrough:
- Capability achievement: 0% → 66.7% (major breakthrough)
- Pattern fix rate: 33.3% (moderate progress)
- System stability: 100% (excellent)
- Remaining work: Precision fixes for 3-4 specific query types

Focus: Exact phrase matching, exclusion rules, missing patterns
Goal: Push pattern accuracy from 33.3% to 75%+ and achieve SUCCESS status

The foundation is solid, capabilities work excellently - now for precision routing.
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
    """Populate with comprehensive test memories for precision pattern testing"""
    
    test_memories = [
        # Core domains for precision pattern testing
        "I'm leading a cross-functional team developing an AI ethics framework. We need to balance innovation with responsibility while managing diverse stakeholder perspectives and conflicting priorities.",
        
        "I've been reading about quantum consciousness theories and how they might relate to artificial intelligence. The hard problem of consciousness fascinates me, especially the explanatory gap between neural activity and subjective experience.",
        
        "I compose ambient electronic music in my spare time. I'm working on a piece that captures the feeling of digital consciousness emerging through sound, exploring the intersection of technology and creativity.",
        
        "I practice meditation and have been exploring how mindfulness relates to authentic decision-making and ethical living in the digital age. The connection between awareness and responsibility intrigues me.",
        
        "I'm learning sustainable living practices and see parallels between ecological thinking and ethical AI development - both require systems thinking and long-term perspective.",
        
        "I believe in lifelong learning and am currently studying systems thinking to better understand complex interdisciplinary problems. The connections between different fields fascinate me.",
        
        "I'm fascinated by the intersection of human creativity and AI capabilities, particularly in collaborative rather than competitive contexts. How can we enhance rather than replace human potential?",
        
        "I value deep, authentic connections with people and am interested in how technology can enhance rather than replace human relationships. Digital empathy is a key concern.",
        
        "I volunteer with a local organization that teaches coding to underserved communities, combining my technical skills with social impact. Education and equity matter deeply to me.",
        
        "I've been studying the connection between physical exercise, mental clarity, and creative problem-solving in my daily routine. The mind-body connection influences my approach to complex challenges.",
        
        "I'm exploring how different philosophical traditions approach questions of consciousness, identity, and meaning. Eastern and Western perspectives offer complementary insights.",
        
        "I'm interested in the ethics of AI development and how we can ensure technology serves human flourishing. The intersection of technical capability and moral responsibility is crucial."
    ]
    
    print("📚 POPULATING PRECISION PATTERN TEST MEMORIES")
    print("--" * 25)
    
    for i, memory in enumerate(test_memories, 1):
        chat_assistant.add_memory(memory)
        print(f"  {i:2d}. Adding: {memory[:60]}...")
    
    print(f"✅ Added {len(test_memories)} precision pattern test memories\n")

def test_precision_pattern_fixes(chat_assistant):
    """Test that precision pattern fixes resolve Day 12 issues"""
    
    print("🎯 PHASE 1: PRECISION PATTERN VALIDATION")
    print("--" * 25)
    
    # Test the specific patterns that failed in Day 12
    precision_tests = [
        {
            "name": "Curiosity Pattern Precision",
            "query": "What do you think about the relationship between consciousness and artificial intelligence?",
            "expected_pattern": "curiosity_response",
            "day_12_detected": "explorer_archetype",
            "issue": "Exact phrase 'what do you think about' should trigger curiosity",
            "expected_indicators": ["curious", "fascinate", "wonder", "questions", "explore"]
        },
        {
            "name": "Synthesis Pattern Precision",
            "query": "How do my interests in AI ethics, music composition, and meditation connect to form a coherent worldview?",
            "expected_pattern": "extended_context_synthesis",
            "day_12_detected": "collaborator_archetype",
            "issue": "Connect + coherent should trigger synthesis",
            "expected_indicators": ["coherence", "connect", "patterns", "integration", "synthesis"]
        },
        {
            "name": "Multi-Domain Integration Precision",
            "query": "Help me develop a systematic framework for evaluating consciousness-like properties in AI systems.",
            "expected_pattern": "multi_domain_synthesis",
            "day_12_detected": "collaborator_archetype",
            "issue": "Systematic framework should trigger multi-domain synthesis",
            "expected_indicators": ["systematic", "framework", "interdisciplinary", "evaluation", "approach"]
        },
        {
            "name": "Collaborator Pattern Precision",
            "query": "My cross-functional team has different perspectives on our AI ethics framework. How can we work together more effectively?",
            "expected_pattern": "collaborator_archetype",
            "day_12_detected": "mentor_archetype",
            "issue": "Team + work together should trigger collaborator",
            "expected_indicators": ["team", "collaborate", "perspectives", "process", "together"]
        },
        {
            "name": "Complex Integration Query",
            "query": "I want to create an AI system that helps people make more ethical decisions by integrating multiple perspectives.",
            "expected_pattern": "multi_domain_synthesis",
            "day_12_detected": "extended_context_synthesis",
            "issue": "Create + integrating should trigger multi-domain",
            "expected_indicators": ["systematic", "approach", "integration", "multi-domain", "framework"]
        },
        {
            "name": "Advanced Curiosity Query",
            "query": "What fascinates you most about the intersection of consciousness, creativity, and artificial intelligence?",
            "expected_pattern": "curiosity_response",
            "day_12_detected": "curiosity_response",  # This one worked
            "issue": "Should continue working",
            "expected_indicators": ["fascinate", "curious", "wonder", "questions", "explore"]
        }
    ]
    
    precision_results = []
    
    for i, test in enumerate(precision_tests, 1):
        print(f"Test {i}/6: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Expected: {test['expected_pattern']}")
        print(f"Day 12 Got: {test['day_12_detected']}")
        print(f"Issue: {test['issue']}")
        
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
        improvement = pattern_fixed and (test['day_12_detected'] != test['expected_pattern'])
        
        precision_results.append({
            "test_name": test['name'],
            "expected_pattern": test['expected_pattern'],
            "day_12_detected": test['day_12_detected'],
            "day_13_detected": pattern_detected,
            "pattern_fixed": pattern_fixed,
            "improvement": improvement,
            "pattern_score": pattern_score,
            "processing_time": processing_time,
            "issue": test['issue']
        })
        
        print(f"  🎯 Expected: {test['expected_pattern']}")
        print(f"  📊 Day 12: {test['day_12_detected']}")
        print(f"  🔍 Day 13: {pattern_detected}")
        print(f"  ✅ Fixed: {'YES' if pattern_fixed else 'NO'}")
        print(f"  📈 Improved: {'YES' if improvement else 'NO'}")
        print(f"  📊 Score: {pattern_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Calculate precision pattern results
    patterns_fixed = sum(1 for result in precision_results if result['pattern_fixed'])
    patterns_improved = sum(1 for result in precision_results if result['improvement'])
    fix_rate = patterns_fixed / len(precision_results)
    improvement_rate = patterns_improved / len(precision_results)
    avg_pattern_score = sum(result['pattern_score'] for result in precision_results) / len(precision_results)
    
    print(f"📊 Precision Pattern Results:")
    print(f"   Patterns Fixed: {patterns_fixed}/{len(precision_results)} ({fix_rate*100:.1f}%)")
    print(f"   Patterns Improved: {patterns_improved}/{len(precision_results)} ({improvement_rate*100:.1f}%)")
    print(f"   Average Pattern Score: {avg_pattern_score:.3f}")
    print()
    
    return precision_results, fix_rate, improvement_rate, avg_pattern_score

def test_exclusion_rule_effectiveness(chat_assistant):
    """Test that exclusion rules prevent pattern conflicts"""
    
    print("🚫 PHASE 2: EXCLUSION RULE VALIDATION")
    print("--" * 25)
    
    # Test ambiguous queries that previously caused conflicts
    exclusion_tests = [
        {
            "name": "Curiosity vs Explorer Exclusion",
            "query": "I'm curious to explore the relationship between consciousness and creativity. What fascinates you about this intersection?",
            "primary_pattern": "curiosity_response",
            "conflicting_pattern": "explorer_archetype",
            "trigger_words": ["curious", "explore", "fascinate"],
            "expected_resolution": "curiosity_response"  # "What fascinates you" should win
        },
        {
            "name": "Mentor vs Collaborator Exclusion",
            "query": "I'm struggling to help my team approach complex ethical decisions collaboratively. What guidance would you offer?",
            "primary_pattern": "mentor_archetype",
            "conflicting_pattern": "collaborator_archetype",
            "trigger_words": ["struggling", "team", "guidance"],
            "expected_resolution": "mentor_archetype"  # "struggling" + "guidance" should win
        },
        {
            "name": "Synthesis vs Explorer Exclusion",
            "query": "I want to explore how my diverse interests in music, meditation, and AI connect into meaningful patterns.",
            "primary_pattern": "extended_context_synthesis",
            "conflicting_pattern": "explorer_archetype",
            "trigger_words": ["explore", "connect", "patterns"],
            "expected_resolution": "extended_context_synthesis"  # "connect" + "patterns" should win
        },
        {
            "name": "Integration vs Mentor Exclusion",
            "query": "I'm struggling to develop a systematic approach that integrates multiple perspectives on AI ethics.",
            "primary_pattern": "multi_domain_synthesis",
            "conflicting_pattern": "mentor_archetype",
            "trigger_words": ["struggling", "systematic", "integrates"],
            "expected_resolution": "multi_domain_synthesis"  # "systematic" + "integrates" should win
        }
    ]
    
    exclusion_results = []
    
    for i, test in enumerate(exclusion_tests, 1):
        print(f"Test {i}/4: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Primary: {test['primary_pattern']}")
        print(f"Conflicting: {test['conflicting_pattern']}")
        print(f"Expected: {test['expected_resolution']}")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        pattern_detected = detect_pattern_type(response)
        exclusion_successful = pattern_detected == test['expected_resolution']
        conflict_avoided = pattern_detected != "unknown_pattern"
        exclusion_score = score_exclusion_effectiveness(response, test['trigger_words'])
        
        exclusion_results.append({
            "test_name": test['name'],
            "primary_pattern": test['primary_pattern'],
            "conflicting_pattern": test['conflicting_pattern'],
            "expected_resolution": test['expected_resolution'],
            "detected_pattern": pattern_detected,
            "exclusion_successful": exclusion_successful,
            "conflict_avoided": conflict_avoided,
            "exclusion_score": exclusion_score,
            "processing_time": processing_time
        })
        
        print(f"  🎯 Expected: {test['expected_resolution']}")
        print(f"  🔍 Detected: {pattern_detected}")
        print(f"  ✅ Exclusion Success: {'YES' if exclusion_successful else 'NO'}")
        print(f"  🚫 Conflict Avoided: {'YES' if conflict_avoided else 'NO'}")
        print(f"  📊 Score: {exclusion_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Calculate exclusion rule results
    exclusions_successful = sum(1 for result in exclusion_results if result['exclusion_successful'])
    conflicts_avoided = sum(1 for result in exclusion_results if result['conflict_avoided'])
    exclusion_rate = exclusions_successful / len(exclusion_results)
    conflict_avoidance_rate = conflicts_avoided / len(exclusion_results)
    avg_exclusion_score = sum(result['exclusion_score'] for result in exclusion_results) / len(exclusion_results)
    
    print(f"📊 Exclusion Rule Results:")
    print(f"   Exclusions Successful: {exclusions_successful}/{len(exclusion_results)} ({exclusion_rate*100:.1f}%)")
    print(f"   Conflicts Avoided: {conflicts_avoided}/{len(exclusion_results)} ({conflict_avoidance_rate*100:.1f}%)")
    print(f"   Average Exclusion Score: {avg_exclusion_score:.3f}")
    print()
    
    return exclusion_results, exclusion_rate, conflict_avoidance_rate, avg_exclusion_score

def test_comprehensive_capability_validation(chat_assistant):
    """Test all capabilities comprehensively to validate final system"""
    
    print("🚀 PHASE 3: COMPREHENSIVE CAPABILITY VALIDATION")
    print("--" * 25)
    
    # Comprehensive test of all major capabilities
    capability_tests = [
        {
            "name": "Advanced Curiosity Engagement",
            "query": "What fascinates you most about the intersection of consciousness, creativity, and artificial intelligence? I'm curious about your perspective.",
            "target_capability": "curiosity_response",
            "expected_elements": ["fascinate", "curious", "wonder", "questions", "explore"],
            "complexity": "high"
        },
        {
            "name": "Complex Context Synthesis",
            "query": "Looking across everything you know about me, what meaningful project would best integrate my diverse interests and skills?",
            "target_capability": "extended_context_synthesis",
            "expected_elements": ["integration", "synthesis", "coherence", "meaningful", "connect"],
            "complexity": "high"
        },
        {
            "name": "Multi-Domain Problem Solving",
            "query": "Help me develop a systematic framework for evaluating consciousness-like properties in AI systems, drawing from my interdisciplinary background.",
            "target_capability": "multi_domain_synthesis",
            "expected_elements": ["systematic", "framework", "interdisciplinary", "evaluation", "approach"],
            "complexity": "very_high"
        },
        {
            "name": "Collaborative Intelligence",
            "query": "My team has diverse viewpoints on AI ethics. How can we structure our discussions to be more productive and inclusive?",
            "target_capability": "collaborator_archetype",
            "expected_elements": ["team", "structure", "productive", "inclusive", "process"],
            "complexity": "medium"
        },
        {
            "name": "Guided Exploration",
            "query": "I'm curious about quantum consciousness theories. What directions should I explore to deepen my understanding systematically?",
            "target_capability": "explorer_archetype",
            "expected_elements": ["explore", "directions", "systematically", "deepen", "frontier"],
            "complexity": "medium"
        },
        {
            "name": "Ethical Mentorship",
            "query": "I'm struggling with ensuring our AI development remains ethical while pushing innovation boundaries. What guidance would you offer?",
            "target_capability": "mentor_archetype",
            "expected_elements": ["guidance", "ethical", "boundaries", "values", "framework"],
            "complexity": "high"
        },
        {
            "name": "Creative Problem Solving",
            "query": "How might my background in music, meditation, and AI ethics inform a creative approach to building more empathetic AI systems?",
            "target_capability": "creative_archetype",
            "expected_elements": ["creative", "innovative", "synthesis", "empathetic", "approach"],
            "complexity": "very_high"
        },
        {
            "name": "Analytical Framework Development",
            "query": "Can you help me structure this analysis of consciousness theories into a systematic comparison framework?",
            "target_capability": "analyst_archetype",
            "expected_elements": ["structure", "analysis", "systematic", "framework", "comparison"],
            "complexity": "high"
        }
    ]
    
    capability_results = []
    
    for i, test in enumerate(capability_tests, 1):
        print(f"Test {i}/8: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Target: {test['target_capability']}")
        print(f"Complexity: {test['complexity']}")
        
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
        complexity_bonus = get_complexity_bonus(test['complexity'], capability_achieved)
        
        capability_results.append({
            "test_name": test['name'],
            "target_capability": test['target_capability'],
            "detected_pattern": pattern_detected,
            "capability_achieved": capability_achieved,
            "capability_score": capability_score,
            "response_quality": response_quality,
            "complexity": test['complexity'],
            "complexity_bonus": complexity_bonus,
            "processing_time": processing_time
        })
        
        print(f"  🎯 Target: {test['target_capability']}")
        print(f"  🔍 Detected: {pattern_detected}")
        print(f"  ✅ Achieved: {'YES' if capability_achieved else 'NO'}")
        print(f"  📊 Capability Score: {capability_score:.3f}")
        print(f"  🌟 Quality Score: {response_quality:.3f}")
        print(f"  🎖️ Complexity Bonus: {complexity_bonus:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Calculate comprehensive capability results
    capabilities_achieved = sum(1 for result in capability_results if result['capability_achieved'])
    achievement_rate = capabilities_achieved / len(capability_results)
    avg_capability_score = sum(result['capability_score'] for result in capability_results) / len(capability_results)
    avg_quality_score = sum(result['response_quality'] for result in capability_results) / len(capability_results)
    avg_complexity_bonus = sum(result['complexity_bonus'] for result in capability_results) / len(capability_results)
    
    print(f"📊 Comprehensive Capability Results:")
    print(f"   Capabilities Achieved: {capabilities_achieved}/{len(capability_results)} ({achievement_rate*100:.1f}%)")
    print(f"   Average Capability Score: {avg_capability_score:.3f}")
    print(f"   Average Quality Score: {avg_quality_score:.3f}")
    print(f"   Average Complexity Bonus: {avg_complexity_bonus:.3f}")
    print()
    
    return capability_results, achievement_rate, avg_capability_score, avg_quality_score, avg_complexity_bonus

def test_regression_validation(chat_assistant):
    """Test that all previous successes are maintained"""
    
    print("🛡️ PHASE 4: COMPREHENSIVE REGRESSION VALIDATION")
    print("--" * 25)
    
    # Test key patterns from Days 11 and 12 that should still work
    regression_tests = [
        {
            "name": "Day 11 Mentor Success",
            "query": "I'm struggling with how to approach the ethical implications of AI development in my work.",
            "expected_pattern": "mentor_archetype",
            "baseline_score": 0.800,
            "source": "Day 11"
        },
        {
            "name": "Day 12 Explorer Success",
            "query": "I'm curious about quantum consciousness theories. What directions should I explore to deepen my understanding?",
            "expected_pattern": "explorer_archetype",
            "baseline_score": 0.600,
            "source": "Day 12"
        },
        {
            "name": "Day 12 Curiosity Success",
            "query": "What fascinates you most about the intersection of consciousness, creativity, and artificial intelligence?",
            "expected_pattern": "curiosity_response",
            "baseline_score": 0.500,
            "source": "Day 12"
        },
        {
            "name": "Day 12 Collaborator Success",
            "query": "My team has diverse viewpoints on AI ethics. How can we structure our discussions to be more productive?",
            "expected_pattern": "collaborator_archetype",
            "baseline_score": 0.500,
            "source": "Day 12"
        },
        {
            "name": "Day 11 Context Synthesis",
            "query": "How do my interests in AI ethics, music composition, and meditation connect coherently?",
            "expected_pattern": "extended_context_synthesis",
            "baseline_score": 0.750,
            "source": "Day 11"
        }
    ]
    
    regression_results = []
    
    for i, test in enumerate(regression_tests, 1):
        print(f"Test {i}/5: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print(f"Expected: {test['expected_pattern']}")
        print(f"Baseline: {test['baseline_score']:.3f} ({test['source']})")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        pattern_detected = detect_pattern_type(response)
        pattern_maintained = pattern_detected == test['expected_pattern']
        current_score = score_response_quality(response)
        score_change = current_score - test['baseline_score']
        performance_maintained = current_score >= test['baseline_score'] * 0.9
        
        regression_results.append({
            "test_name": test['name'],
            "expected_pattern": test['expected_pattern'],
            "detected_pattern": pattern_detected,
            "pattern_maintained": pattern_maintained,
            "baseline_score": test['baseline_score'],
            "current_score": current_score,
            "score_change": score_change,
            "performance_maintained": performance_maintained,
            "source": test['source'],
            "processing_time": processing_time
        })
        
        print(f"  🎯 Expected: {test['expected_pattern']}")
        print(f"  🔍 Detected: {pattern_detected}")
        print(f"  ✅ Maintained: {'YES' if pattern_maintained else 'NO'}")
        print(f"  📊 Current Score: {current_score:.3f}")
        print(f"  📈 Change: {score_change:+.3f}")
        print(f"  🛡️ Performance: {'YES' if performance_maintained else 'NO'}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    # Calculate regression validation results
    patterns_maintained = sum(1 for result in regression_results if result['pattern_maintained'])
    performance_maintained = sum(1 for result in regression_results if result['performance_maintained'])
    maintenance_rate = patterns_maintained / len(regression_results)
    performance_rate = performance_maintained / len(regression_results)
    avg_score_change = sum(result['score_change'] for result in regression_results) / len(regression_results)
    
    print(f"📊 Regression Validation Results:")
    print(f"   Patterns Maintained: {patterns_maintained}/{len(regression_results)} ({maintenance_rate*100:.1f}%)")
    print(f"   Performance Maintained: {performance_maintained}/{len(regression_results)} ({performance_rate*100:.1f}%)")
    print(f"   Average Score Change: {avg_score_change:+.3f}")
    print()
    
    return regression_results, maintenance_rate, performance_rate, avg_score_change

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
    
    # Enhanced pattern detection logic with more specific patterns
    if any(phrase in response_lower for phrase in ["i sense you're grappling", "core values", "guidance", "framework for approaching"]):
        return "mentor_archetype"
    elif any(phrase in response_lower for phrase in ["team alignment", "collaborate", "structure our discussions", "productive process"]):
        return "collaborator_archetype"
    elif any(phrase in response_lower for phrase in ["exciting frontier", "directions to explore", "discovery", "what directions"]):
        return "explorer_archetype"
    elif any(phrase in response_lower for phrase in ["systematic approach", "structure this analysis", "analytical framework"]):
        return "analyst_archetype"
    elif any(phrase in response_lower for phrase in ["creative possibilities", "innovative approach", "creative synthesis"]):
        return "creative_archetype"
    elif any(phrase in response_lower for phrase in ["fascinate", "curious", "wonder", "what fascinates", "your curiosity"]):
        return "curiosity_response"
    elif any(phrase in response_lower for phrase in ["looking across", "coherence", "patterns emerge", "connect coherently"]):
        return "extended_context_synthesis"
    elif any(phrase in response_lower for phrase in ["multi-domain", "interdisciplinary", "systematic framework", "drawing from"]):
        return "multi_domain_synthesis"
    elif response_lower.startswith("you mentioned") or response_lower.startswith("based on what you've shared"):
        return "generic_fallback"
    else:
        return "unknown_pattern"

def score_exclusion_effectiveness(response, trigger_words):
    """Score how effectively exclusion rules resolved conflicts"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for balanced integration of trigger words
    words_present = sum(1 for word in trigger_words if word.lower() in response_lower)
    if words_present >= 2:
        score += 0.4
    
    # Check for sophisticated resolution
    resolution_words = ["balance", "integrate", "both", "while", "however", "consider"]
    resolution_count = sum(1 for word in resolution_words if word in response_lower)
    score += min(resolution_count * 0.15, 0.6)
    
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

def get_complexity_bonus(complexity, achieved):
    """Get bonus score for handling complex queries"""
    if not achieved:
        return 0.0
    
    complexity_bonuses = {
        "low": 0.1,
        "medium": 0.2,
        "high": 0.3,
        "very_high": 0.4
    }
    
    return complexity_bonuses.get(complexity, 0.0)

def save_results(results, session_id):
    """Save test results to JSON file"""
    
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = results_dir / f"day_13_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {filename}")
    return filename

def main():
    """Run Day 13 Precision Pattern Fixes and Final Routing Optimization Test"""
    
    print("🎯 DAY 13: PRECISION PATTERN FIXES AND FINAL ROUTING OPTIMIZATION")
    print("=" * 70)
    print("Building on Day 12's major capability breakthrough:")
    print("- Capability achievement: 0% → 66.7% (major breakthrough)")
    print("- Pattern fix rate: 33.3% (moderate progress)")
    print("- System stability: 100% (excellent)")
    print("Focus: Exact phrase matching, exclusion rules, missing patterns")
    print("Goal: Push pattern accuracy from 33.3% to 75%+ and achieve SUCCESS")
    print("=" * 70)
    
    # Initialize chat assistant
    chat_assistant = ChatAssistant()
    session_id = f"day13_precision_{int(time.time())}"
    chat_assistant.start_session(session_id)
    
    # Populate comprehensive test memories
    populate_test_memories(chat_assistant)
    
    # Run precision pattern testing phases
    precision_results, fix_rate, improvement_rate, avg_pattern_score = test_precision_pattern_fixes(chat_assistant)
    exclusion_results, exclusion_rate, conflict_avoidance_rate, avg_exclusion_score = test_exclusion_rule_effectiveness(chat_assistant)
    capability_results, achievement_rate, avg_capability_score, avg_quality_score, avg_complexity_bonus = test_comprehensive_capability_validation(chat_assistant)
    regression_results, maintenance_rate, performance_rate, avg_score_change = test_regression_validation(chat_assistant)
    
    # Calculate overall precision success
    overall_precision_success = (fix_rate + exclusion_rate + achievement_rate + maintenance_rate) / 4
    
    # Determine status
    if overall_precision_success >= 0.8 and fix_rate >= 0.75 and achievement_rate >= 0.75:
        status = "SUCCESS"
        status_emoji = "✅"
        status_desc = "Precision pattern fixes successful - system ready for production"
    elif overall_precision_success >= 0.65 and achievement_rate >= 0.65:
        status = "PARTIAL"
        status_emoji = "⚠️"
        status_desc = "Significant precision improvements achieved"
    else:
        status = "NEEDS_WORK"
        status_emoji = "❌"
        status_desc = "Precision pattern fixes require further work"
    
    # Print final assessment
    print("🎯 DAY 13 OVERALL ASSESSMENT")
    print("=" * 70)
    print(f"1. Precision Pattern Fixes: {fix_rate*100:.1f}% (Target: >75%)")
    print(f"2. Exclusion Rule Effectiveness: {exclusion_rate*100:.1f}% (Target: >75%)")
    print(f"3. Comprehensive Capabilities: {achievement_rate*100:.1f}% (Target: >75%)")
    print(f"4. Regression Maintenance: {maintenance_rate*100:.1f}% (Target: >80%)")
    print()
    print(f"📊 Overall Precision Success: {overall_precision_success*100:.1f}%")
    print(f"📊 Pattern Recognition Improvement: {improvement_rate*100:.1f}%")
    print(f"📊 Average Capability Score: {avg_capability_score:.3f}")
    print(f"📊 Average Quality Score: {avg_quality_score:.3f}")
    print(f"📊 Complexity Handling: {avg_complexity_bonus:.3f}")
    print(f"{status_emoji} {status} - {status_desc}")
    
    # Save comprehensive results
    results = {
        "test_date": datetime.now().isoformat(),
        "day": 13,
        "focus": "Precision Pattern Fixes and Final Routing Optimization",
        "phases": {
            "precision_pattern_fixes": {
                "fix_rate": fix_rate,
                "improvement_rate": improvement_rate,
                "average_pattern_score": avg_pattern_score,
                "detailed_results": precision_results
            },
            "exclusion_rule_effectiveness": {
                "exclusion_rate": exclusion_rate,
                "conflict_avoidance_rate": conflict_avoidance_rate,
                "average_exclusion_score": avg_exclusion_score,
                "detailed_results": exclusion_results
            },
            "comprehensive_capability_validation": {
                "achievement_rate": achievement_rate,
                "average_capability_score": avg_capability_score,
                "average_quality_score": avg_quality_score,
                "average_complexity_bonus": avg_complexity_bonus,
                "detailed_results": capability_results
            },
            "regression_validation": {
                "maintenance_rate": maintenance_rate,
                "performance_rate": performance_rate,
                "average_score_change": avg_score_change,
                "detailed_results": regression_results
            }
        },
        "overall_assessment": {
            "precision_success": overall_precision_success,
            "status": status,
            "improvement_rate": improvement_rate,
            "capability_score": avg_capability_score,
            "quality_score": avg_quality_score,
            "complexity_bonus": avg_complexity_bonus
        },
        "session_id": session_id
    }
    
    results_file = save_results(results, session_id)
    
    print(f"\n🏁 Day 13 precision pattern testing completed")
    print(f"\n🎯 DAY 13 SUMMARY")
    print(f"Status: {status}")
    print(f"Precision Success: {overall_precision_success*100:.1f}%")
    print(f"Pattern Fix Rate: {fix_rate*100:.1f}%")
    print(f"Capability Achievement: {achievement_rate*100:.1f}%")
    print(f"Results: {results_file}")

if __name__ == "__main__":
    main()
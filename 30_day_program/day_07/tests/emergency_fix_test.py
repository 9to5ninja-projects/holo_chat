#!/usr/bin/env python3
"""
Emergency Fix Testing - Day 7 Critical Fixes Validation
======================================================

Test the emergency fixes implemented to resolve:
1. Query echo problem (100% → <20%)
2. Basic reasoning capabilities (0.300 → >0.500)
3. Creative suggestion generation (0.051 → >0.300)
"""

import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def test_query_echo_fix():
    """Test that query echo problem is resolved"""
    print("🔧 TESTING QUERY ECHO FIX")
    print("-" * 40)
    
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("EmergencyFixTest_QueryEcho")
    
    test_queries = [
        "What book did I mention?",
        "Tell me about my hiking experience",
        "What did I share about my grandmother?",
        "Based on everything I've shared about my interests and values, what career path might align well with who I am?"
    ]
    
    echo_count = 0
    total_tests = len(test_queries)
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}/{total_tests}: {query[:50]}...")
        
        start_time = time.time()
        result = assistant.chat(query)
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        
        # Check for query echo
        query_echo = (query.lower() in response.lower() or 
                     any(phrase in response.lower() for phrase in [
                         "you mentioned that your", 
                         "based on what you've shared:"
                     ]) and query[:20].lower() in response.lower())
        
        if query_echo:
            echo_count += 1
            print(f"  ❌ Query echo detected")
        else:
            print(f"  ✅ No query echo")
        
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:100]}...")
        print()
    
    echo_rate = echo_count / total_tests
    print(f"📊 QUERY ECHO RESULTS:")
    print(f"   Echo Rate: {echo_rate:.1%} (Target: <20%)")
    print(f"   Status: {'🟢 FIXED' if echo_rate < 0.2 else '🟡 IMPROVED' if echo_rate < 0.5 else '🔴 STILL ISSUE'}")
    
    assistant.end_session()
    return echo_rate

def test_reasoning_capabilities():
    """Test basic reasoning capabilities"""
    print("\n🧠 TESTING REASONING CAPABILITIES")
    print("-" * 40)
    
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("EmergencyFixTest_Reasoning")
    
    reasoning_queries = [
        "Based on everything I've shared about my interests and values, what career path might align well with who I am, and why?",
        "If I wanted to write a book that reflects my worldview, what themes and approaches would you suggest, and what's your reasoning?",
        "Given my personality and interests, what kind of learning environment would help me grow the most, and why do you think so?"
    ]
    
    reasoning_scores = []
    
    for i, query in enumerate(reasoning_queries, 1):
        print(f"Test {i}/{len(reasoning_queries)}: {query[:50]}...")
        
        start_time = time.time()
        result = assistant.chat(query)
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        
        # Analyze reasoning quality
        reasoning_indicators = ["because", "since", "therefore", "this is because", "suggests", "indicates"]
        reasoning_count = sum(1 for indicator in reasoning_indicators if indicator in response.lower())
        
        # Check for logical connections
        logical_connections = ["and", "but", "however", "therefore", "thus", "so"]
        connection_count = sum(1 for conn in logical_connections if conn in response.lower())
        
        # Check for evidence usage
        evidence_usage = ["based on", "given", "considering", "your interests", "your personality"]
        evidence_count = sum(1 for evidence in evidence_usage if evidence in response.lower())
        
        reasoning_score = min(1.0, (reasoning_count + connection_count + evidence_count) / 6)
        reasoning_scores.append(reasoning_score)
        
        print(f"  🧠 Reasoning Score: {reasoning_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:100]}...")
        print()
    
    avg_reasoning = sum(reasoning_scores) / len(reasoning_scores)
    print(f"📊 REASONING RESULTS:")
    print(f"   Average Reasoning: {avg_reasoning:.3f} (Target: >0.500)")
    print(f"   Status: {'🟢 EXCELLENT' if avg_reasoning > 0.6 else '🟡 GOOD' if avg_reasoning > 0.5 else '🔴 NEEDS WORK'}")
    
    assistant.end_session()
    return avg_reasoning

def test_creative_capabilities():
    """Test creative suggestion generation"""
    print("\n🎨 TESTING CREATIVE CAPABILITIES")
    print("-" * 40)
    
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("EmergencyFixTest_Creative")
    
    creative_queries = [
        "I want to create a unique birthday gift for my friend who loves both technology and nature. Can you help me brainstorm some creative ideas?",
        "I'm designing a community space that should encourage both quiet reflection and social interaction. What innovative design elements would you suggest?",
        "How could I use my love of cooking and storytelling to create something that brings people together in a new way?",
        "I want to teach children about environmental conservation in a way that's both fun and memorable. What creative approaches would you recommend?"
    ]
    
    creativity_scores = []
    
    for i, query in enumerate(creative_queries, 1):
        print(f"Test {i}/{len(creative_queries)}: {query[:50]}...")
        
        start_time = time.time()
        result = assistant.chat(query)
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        
        # Analyze creativity
        creative_words = ["creative", "innovative", "unique", "combine", "blend", "fusion", "novel"]
        creative_count = sum(1 for word in creative_words if word in response.lower())
        
        # Check for specific suggestions
        suggestion_indicators = ["suggest", "recommend", "idea", "could", "try", "consider"]
        suggestion_count = sum(1 for indicator in suggestion_indicators if indicator in response.lower())
        
        # Check for novel combinations
        combination_words = ["combine", "merge", "blend", "together", "fusion", "mix"]
        combination_count = sum(1 for word in combination_words if word in response.lower())
        
        creativity_score = min(1.0, (creative_count + suggestion_count + combination_count) / 8)
        creativity_scores.append(creativity_score)
        
        print(f"  🎨 Creativity Score: {creativity_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:100]}...")
        print()
    
    avg_creativity = sum(creativity_scores) / len(creativity_scores)
    print(f"📊 CREATIVITY RESULTS:")
    print(f"   Average Creativity: {avg_creativity:.3f} (Target: >0.300)")
    print(f"   Status: {'🟢 EXCELLENT' if avg_creativity > 0.6 else '🟡 GOOD' if avg_creativity > 0.3 else '🔴 NEEDS WORK'}")
    
    assistant.end_session()
    return avg_creativity

def main():
    """Run all emergency fix tests"""
    print("🚨 EMERGENCY FIX VALIDATION TESTING")
    print("=" * 60)
    print("Testing critical fixes implemented for Day 7 crisis")
    print("=" * 60)
    
    # Test 1: Query Echo Fix
    echo_rate = test_query_echo_fix()
    
    # Test 2: Reasoning Capabilities
    reasoning_score = test_reasoning_capabilities()
    
    # Test 3: Creative Capabilities
    creativity_score = test_creative_capabilities()
    
    # Overall Assessment
    print("\n🎯 OVERALL EMERGENCY FIX ASSESSMENT")
    print("=" * 60)
    
    fixes_successful = 0
    total_fixes = 3
    
    print(f"1. Query Echo Fix: {echo_rate:.1%} ({'✅ SUCCESS' if echo_rate < 0.2 else '⚠️ PARTIAL' if echo_rate < 0.5 else '❌ FAILED'})")
    if echo_rate < 0.2:
        fixes_successful += 1
    
    print(f"2. Reasoning Enhancement: {reasoning_score:.3f} ({'✅ SUCCESS' if reasoning_score > 0.5 else '⚠️ PARTIAL' if reasoning_score > 0.3 else '❌ FAILED'})")
    if reasoning_score > 0.5:
        fixes_successful += 1
    
    print(f"3. Creative Capabilities: {creativity_score:.3f} ({'✅ SUCCESS' if creativity_score > 0.3 else '⚠️ PARTIAL' if creativity_score > 0.15 else '❌ FAILED'})")
    if creativity_score > 0.3:
        fixes_successful += 1
    
    success_rate = fixes_successful / total_fixes
    print(f"\n📊 Fix Success Rate: {fixes_successful}/{total_fixes} ({success_rate:.1%})")
    
    if success_rate >= 0.67:
        print("🎉 EMERGENCY FIXES SUCCESSFUL - Ready for Day 8!")
        status = "SUCCESS"
    elif success_rate >= 0.33:
        print("⚠️ PARTIAL SUCCESS - Some improvements, continue development")
        status = "PARTIAL"
    else:
        print("❌ FIXES FAILED - Further intervention required")
        status = "FAILED"
    
    print(f"\nStatus: {status}")
    print("Next: Continue with Day 8 testing" if status == "SUCCESS" else "Next: Additional fixes needed")
    
    return {
        "echo_rate": echo_rate,
        "reasoning_score": reasoning_score,
        "creativity_score": creativity_score,
        "success_rate": success_rate,
        "status": status
    }

if __name__ == "__main__":
    results = main()
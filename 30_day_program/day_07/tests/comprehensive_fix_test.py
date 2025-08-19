#!/usr/bin/env python3
"""
Comprehensive Fix Test - Single Session with Memory Continuity
============================================================
"""

import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def comprehensive_test():
    """Test all fixes in a single session with memory continuity"""
    print("🚨 COMPREHENSIVE EMERGENCY FIX TESTING")
    print("=" * 60)
    print("Single session test with memory continuity")
    print("=" * 60)
    
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("ComprehensiveFixTest")
    
    # Phase 1: Populate memories
    print("📚 PHASE 1: POPULATING MEMORIES")
    print("-" * 40)
    
    memory_inputs = [
        "I love reading science fiction, especially The Left Hand of Darkness by Ursula K. Le Guin.",
        "Yesterday I went hiking in the mountains and saw a beautiful sunset with deep oranges and purples.",
        "My grandmother makes amazing apple pie with a secret cardamom ingredient.",
        "I've been thinking about time and how our perception shapes identity, like the Ship of Theseus paradox.",
        "I prefer pour-over coffee brewing with a 1:16 ratio and slow circular pours.",
        "I'm interested in environmental conservation and innovative engagement approaches.",
        "I enjoy storytelling as a way to connect with others and share experiences.",
        "Philosophy fascinates me, especially questions about identity and consciousness."
    ]
    
    for i, memory_input in enumerate(memory_inputs, 1):
        print(f"  {i}. Adding: {memory_input[:50]}...")
        assistant.chat(memory_input)
    
    print(f"✅ Added {len(memory_inputs)} memories")
    
    # Phase 2: Test Query Echo Fix
    print(f"\n🔧 PHASE 2: TESTING QUERY ECHO FIX")
    print("-" * 40)
    
    echo_tests = [
        "What book did I mention?",
        "Tell me about my hiking experience",
        "What did I share about my grandmother?",
        "What are my thoughts on time?"
    ]
    
    echo_count = 0
    for i, query in enumerate(echo_tests, 1):
        print(f"Test {i}/{len(echo_tests)}: {query}")
        
        start_time = time.time()
        result = assistant.chat(query)
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        
        # Check for query echo
        query_echo = (query.lower() in response.lower() and 
                     any(phrase in response.lower() for phrase in [
                         "you mentioned that your", 
                         "based on what you've shared:",
                         "i remember your experience:"
                     ]) and query[:15].lower() in response.lower())
        
        if query_echo:
            echo_count += 1
            print(f"  ❌ Query echo detected")
        else:
            print(f"  ✅ No query echo")
        
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    echo_rate = echo_count / len(echo_tests)
    print(f"📊 Query Echo Results: {echo_rate:.1%} (Target: <20%)")
    
    # Phase 3: Test Reasoning Capabilities
    print(f"\n🧠 PHASE 3: TESTING REASONING CAPABILITIES")
    print("-" * 40)
    
    reasoning_tests = [
        "Based on everything I've shared about my interests and values, what career path might align well with who I am, and why?",
        "If I wanted to write a book that reflects my worldview, what themes and approaches would you suggest, and what's your reasoning?",
        "Given my personality and interests, what kind of learning environment would help me grow the most, and why do you think so?"
    ]
    
    reasoning_scores = []
    for i, query in enumerate(reasoning_tests, 1):
        print(f"Test {i}/{len(reasoning_tests)}: {query[:50]}...")
        
        start_time = time.time()
        result = assistant.chat(query)
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        
        # Analyze reasoning quality
        reasoning_indicators = ["because", "since", "therefore", "this is because", "suggests", "indicates", "given", "based on"]
        reasoning_count = sum(1 for indicator in reasoning_indicators if indicator in response.lower())
        
        # Check for evidence usage
        evidence_indicators = ["your interests", "you mentioned", "you shared", "your love", "your thoughts"]
        evidence_count = sum(1 for evidence in evidence_indicators if evidence in response.lower())
        
        # Check for logical structure
        logical_indicators = ["might", "could", "would", "because", "since", "therefore"]
        logical_count = sum(1 for logical in logical_indicators if logical in response.lower())
        
        reasoning_score = min(1.0, (reasoning_count + evidence_count + logical_count) / 8)
        reasoning_scores.append(reasoning_score)
        
        print(f"  🧠 Reasoning Score: {reasoning_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    avg_reasoning = sum(reasoning_scores) / len(reasoning_scores)
    print(f"📊 Reasoning Results: {avg_reasoning:.3f} (Target: >0.500)")
    
    # Phase 4: Test Creative Capabilities
    print(f"\n🎨 PHASE 4: TESTING CREATIVE CAPABILITIES")
    print("-" * 40)
    
    creative_tests = [
        "I want to create a unique birthday gift for my friend who loves both technology and nature. Can you help me brainstorm some creative ideas?",
        "I'm designing a community space that should encourage both quiet reflection and social interaction. What innovative design elements would you suggest?",
        "How could I use my love of cooking and storytelling to create something that brings people together in a new way?",
        "I want to teach children about environmental conservation in a way that's both fun and memorable. What creative approaches would you recommend?"
    ]
    
    creativity_scores = []
    for i, query in enumerate(creative_tests, 1):
        print(f"Test {i}/{len(creative_tests)}: {query[:50]}...")
        
        start_time = time.time()
        result = assistant.chat(query)
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        
        # Analyze creativity
        creative_words = ["creative", "innovative", "unique", "combine", "blend", "fusion", "novel", "ideas", "suggest"]
        creative_count = sum(1 for word in creative_words if word in response.lower())
        
        # Check for specific suggestions
        suggestion_indicators = ["here are", "you could", "try", "consider", "suggest", "recommend"]
        suggestion_count = sum(1 for indicator in suggestion_indicators if indicator in response.lower())
        
        # Check for novel combinations
        combination_words = ["combine", "merge", "blend", "together", "fusion", "mix", "integrate"]
        combination_count = sum(1 for word in combination_words if word in response.lower())
        
        creativity_score = min(1.0, (creative_count + suggestion_count + combination_count) / 10)
        creativity_scores.append(creativity_score)
        
        print(f"  🎨 Creativity Score: {creativity_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    avg_creativity = sum(creativity_scores) / len(creativity_scores)
    print(f"📊 Creativity Results: {avg_creativity:.3f} (Target: >0.300)")
    
    # Phase 5: Test Synthesis Capabilities
    print(f"\n🔬 PHASE 5: TESTING SYNTHESIS CAPABILITIES")
    print("-" * 40)
    
    synthesis_tests = [
        "What patterns do you notice in my approach to learning and discovery across all the different topics we've discussed?",
        "How do my various interests and experiences create a coherent picture of my values and priorities?",
        "If you were to predict what kinds of challenges I might enjoy tackling, what would they be and why?"
    ]
    
    synthesis_scores = []
    for i, query in enumerate(synthesis_tests, 1):
        print(f"Test {i}/{len(synthesis_tests)}: {query[:50]}...")
        
        start_time = time.time()
        result = assistant.chat(query)
        processing_time = time.time() - start_time
        
        response = result.get("response", "")
        
        # Analyze synthesis quality
        synthesis_indicators = ["patterns", "notice", "across", "integration", "combination", "themes", "coherent"]
        synthesis_count = sum(1 for indicator in synthesis_indicators if indicator in response.lower())
        
        # Check for cross-domain thinking
        domain_indicators = ["intellectual", "experiential", "creative", "philosophical", "nature", "storytelling"]
        domain_count = sum(1 for domain in domain_indicators if domain in response.lower())
        
        # Check for meta-cognitive analysis
        meta_indicators = ["suggests", "indicates", "shows", "reveals", "demonstrates", "reflects"]
        meta_count = sum(1 for meta in meta_indicators if meta in response.lower())
        
        synthesis_score = min(1.0, (synthesis_count + domain_count + meta_count) / 8)
        synthesis_scores.append(synthesis_score)
        
        print(f"  🔬 Synthesis Score: {synthesis_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    avg_synthesis = sum(synthesis_scores) / len(synthesis_scores)
    print(f"📊 Synthesis Results: {avg_synthesis:.3f} (Target: >0.300)")
    
    # Final Assessment
    print(f"\n🎯 COMPREHENSIVE ASSESSMENT")
    print("=" * 60)
    
    fixes_successful = 0
    total_fixes = 4
    
    print(f"1. Query Echo Fix: {echo_rate:.1%} ({'✅ SUCCESS' if echo_rate < 0.2 else '⚠️ PARTIAL' if echo_rate < 0.5 else '❌ FAILED'})")
    if echo_rate < 0.2:
        fixes_successful += 1
    
    print(f"2. Reasoning Enhancement: {avg_reasoning:.3f} ({'✅ SUCCESS' if avg_reasoning > 0.5 else '⚠️ PARTIAL' if avg_reasoning > 0.3 else '❌ FAILED'})")
    if avg_reasoning > 0.5:
        fixes_successful += 1
    
    print(f"3. Creative Capabilities: {avg_creativity:.3f} ({'✅ SUCCESS' if avg_creativity > 0.3 else '⚠️ PARTIAL' if avg_creativity > 0.15 else '❌ FAILED'})")
    if avg_creativity > 0.3:
        fixes_successful += 1
    
    print(f"4. Synthesis Capabilities: {avg_synthesis:.3f} ({'✅ SUCCESS' if avg_synthesis > 0.3 else '⚠️ PARTIAL' if avg_synthesis > 0.15 else '❌ FAILED'})")
    if avg_synthesis > 0.3:
        fixes_successful += 1
    
    success_rate = fixes_successful / total_fixes
    print(f"\n📊 Overall Success Rate: {fixes_successful}/{total_fixes} ({success_rate:.1%})")
    
    if success_rate >= 0.75:
        print("🎉 EMERGENCY FIXES HIGHLY SUCCESSFUL - Ready for Day 8!")
        status = "SUCCESS"
    elif success_rate >= 0.5:
        print("✅ EMERGENCY FIXES SUCCESSFUL - Significant improvements achieved!")
        status = "SUCCESS"
    elif success_rate >= 0.25:
        print("⚠️ PARTIAL SUCCESS - Some improvements, continue development")
        status = "PARTIAL"
    else:
        print("❌ FIXES FAILED - Further intervention required")
        status = "FAILED"
    
    assistant.end_session()
    
    return {
        "echo_rate": echo_rate,
        "reasoning_score": avg_reasoning,
        "creativity_score": avg_creativity,
        "synthesis_score": avg_synthesis,
        "success_rate": success_rate,
        "status": status
    }

if __name__ == "__main__":
    results = comprehensive_test()
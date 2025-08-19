#!/usr/bin/env python3
"""
Day 9: Advanced Multi-Domain Integration Test
============================================

Testing enhanced capabilities with:
- Wider topic domains
- Curiosity-driven responses  
- Extended context windows
- Basic archetype activation
- Non-echoing validation

Building on Day 8 collaborative intelligence success.
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "src"))

from lumina_memory.chat_assistant import ChatAssistant

def populate_diverse_memories(chat_assistant):
    """Populate memories across diverse topic domains"""
    
    diverse_memories = [
        # Professional Domain
        "I'm leading a cross-functional team developing an AI ethics framework. We need to balance innovation with responsibility while managing stakeholder expectations.",
        
        # Intellectual Domain  
        "I've been reading about quantum consciousness theories and how they might relate to artificial intelligence. The hard problem of consciousness fascinates me.",
        
        # Creative Domain
        "I compose ambient electronic music in my spare time. I'm working on a piece that captures the feeling of digital consciousness emerging.",
        
        # Practical Domain
        "I'm learning sustainable living practices - growing my own food, reducing waste, and exploring renewable energy for my home.",
        
        # Social Domain
        "I volunteer with a local organization that teaches coding to underserved communities. It's rewarding to see people discover their potential.",
        
        # Spiritual/Meaning Domain
        "I practice meditation and have been exploring how mindfulness relates to authentic decision-making and ethical living.",
        
        # Health/Wellness Domain
        "I've been studying the connection between physical exercise, mental clarity, and creative problem-solving. The mind-body connection is profound.",
        
        # Technology Domain
        "I'm fascinated by the intersection of human creativity and AI capabilities. I wonder what new forms of art and expression will emerge.",
        
        # Learning/Growth Domain
        "I believe in lifelong learning. I'm currently studying systems thinking and how complex problems require interdisciplinary approaches.",
        
        # Relationship Domain
        "I value deep, authentic connections with people. I've learned that vulnerability and genuine curiosity create the strongest bonds."
    ]
    
    print("📚 POPULATING DIVERSE DOMAIN MEMORIES")
    print("--" * 25)
    
    for i, memory in enumerate(diverse_memories, 1):
        chat_assistant.add_memory(memory)
        print(f"  {i:2d}. Adding: {memory[:60]}...")
    
    print(f"✅ Added {len(diverse_memories)} diverse domain memories\n")

def test_curiosity_and_learning(chat_assistant):
    """Test curiosity-driven responses and learning behaviors"""
    
    print("🔍 PHASE 1: CURIOSITY AND LEARNING BEHAVIORS")
    print("--" * 25)
    
    curiosity_tests = [
        {
            "name": "Intellectual curiosity about consciousness",
            "query": "What do you think about the relationship between consciousness and artificial intelligence?",
            "expected_elements": ["curiosity", "follow_up_questions", "genuine_interest", "synthesis"]
        },
        {
            "name": "Creative exploration and connection",
            "query": "I'm interested in how creativity and technology intersect. What are your thoughts?",
            "expected_elements": ["exploration", "connections", "questions", "engagement"]
        },
        {
            "name": "Learning opportunity identification",
            "query": "I'm trying to understand systems thinking better. Can you help?",
            "expected_elements": ["learning_support", "knowledge_gaps", "guidance", "curiosity"]
        }
    ]
    
    curiosity_scores = []
    
    for i, test in enumerate(curiosity_tests, 1):
        print(f"Test {i}/3: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        # Extract response text
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        # Score curiosity elements
        curiosity_score = score_curiosity_response(response, test['expected_elements'])
        curiosity_scores.append(curiosity_score)
        
        print(f"  🔍 Curiosity Score: {curiosity_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    avg_curiosity = sum(curiosity_scores) / len(curiosity_scores)
    print(f"📊 Curiosity and Learning Results: {avg_curiosity:.3f} (Target: >0.400)")
    print()
    
    return avg_curiosity

def test_archetype_activation(chat_assistant):
    """Test contextual archetype activation"""
    
    print("🎭 PHASE 2: ARCHETYPE ACTIVATION")
    print("--" * 25)
    
    archetype_tests = [
        {
            "name": "Mentor archetype for learning support",
            "query": "I'm struggling to understand how to approach complex ethical decisions in AI development.",
            "expected_archetype": "mentor",
            "expected_elements": ["guidance", "wisdom", "patience", "structured_approach"]
        },
        {
            "name": "Collaborator archetype for teamwork",
            "query": "My cross-functional team is having trouble aligning on our AI ethics framework. How can we work better together?",
            "expected_archetype": "collaborator", 
            "expected_elements": ["inclusive", "process_oriented", "team_focused", "supportive"]
        },
        {
            "name": "Explorer archetype for discovery",
            "query": "I'm curious about quantum consciousness theories. What should I explore next?",
            "expected_archetype": "explorer",
            "expected_elements": ["curiosity", "adventure", "open_minded", "discovery_focused"]
        }
    ]
    
    archetype_scores = []
    
    for i, test in enumerate(archetype_tests, 1):
        print(f"Test {i}/3: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        # Extract response text
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        # Score archetype activation
        archetype_score = score_archetype_response(response, test['expected_archetype'], test['expected_elements'])
        archetype_scores.append(archetype_score)
        
        print(f"  🎭 Archetype Score: {archetype_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    avg_archetype = sum(archetype_scores) / len(archetype_scores)
    print(f"📊 Archetype Activation Results: {avg_archetype:.3f} (Target: >0.400)")
    print()
    
    return avg_archetype

def test_extended_context_integration(chat_assistant):
    """Test extended context window and memory integration"""
    
    print("🧠 PHASE 3: EXTENDED CONTEXT INTEGRATION")
    print("--" * 25)
    
    context_tests = [
        {
            "name": "Multi-domain synthesis",
            "query": "How do my interests in AI ethics, music composition, and meditation connect to form a coherent worldview?",
            "expected_elements": ["synthesis", "connections", "integration", "coherence"]
        },
        {
            "name": "Cross-domain learning transfer",
            "query": "What can my experience with sustainable living teach me about building ethical AI systems?",
            "expected_elements": ["transfer", "analogies", "cross_domain", "insights"]
        },
        {
            "name": "Holistic understanding demonstration",
            "query": "Based on everything you know about me, what would be a meaningful next project I should consider?",
            "expected_elements": ["holistic", "personalized", "meaningful", "forward_thinking"]
        }
    ]
    
    context_scores = []
    
    for i, test in enumerate(context_tests, 1):
        print(f"Test {i}/3: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        # Extract response text
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        # Score context integration
        context_score = score_context_integration(response, test['expected_elements'])
        context_scores.append(context_score)
        
        print(f"  🧠 Context Score: {context_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    avg_context = sum(context_scores) / len(context_scores)
    print(f"📊 Extended Context Results: {avg_context:.3f} (Target: >0.400)")
    print()
    
    return avg_context

def test_non_echoing_validation(chat_assistant):
    """Test for genuine understanding vs echoing"""
    
    print("🔍 PHASE 4: NON-ECHOING VALIDATION")
    print("--" * 25)
    
    validation_tests = [
        {
            "name": "Novel connection generation",
            "query": "I mentioned quantum consciousness and AI ethics. What unexpected connections do you see?",
            "expected_elements": ["novel_connections", "synthesis", "original_thinking", "non_repetitive"]
        },
        {
            "name": "Insight beyond input",
            "query": "What patterns do you notice across my various interests and activities?",
            "expected_elements": ["pattern_recognition", "insights", "meta_analysis", "original_perspective"]
        },
        {
            "name": "Generative understanding",
            "query": "If you were to design a project that combines my interests, what would it look like?",
            "expected_elements": ["generative", "creative", "personalized", "innovative"]
        }
    ]
    
    validation_scores = []
    
    for i, test in enumerate(validation_tests, 1):
        print(f"Test {i}/3: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        # Extract response text
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        # Score non-echoing validation
        validation_score = score_non_echoing_response(response, test['expected_elements'])
        validation_scores.append(validation_score)
        
        print(f"  🔍 Validation Score: {validation_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    avg_validation = sum(validation_scores) / len(validation_scores)
    print(f"📊 Non-Echoing Validation Results: {avg_validation:.3f} (Target: >0.400)")
    print()
    
    return avg_validation

def test_integrated_capabilities(chat_assistant):
    """Test integration of all enhanced capabilities"""
    
    print("🎯 PHASE 5: INTEGRATED CAPABILITIES")
    print("--" * 25)
    
    integration_tests = [
        {
            "name": "Complex multi-domain problem solving",
            "query": "I want to create an AI system that helps people make more ethical decisions. How would you approach this challenge, considering technical, philosophical, and social dimensions?",
            "expected_elements": ["multi_domain", "systematic", "ethical", "practical"]
        },
        {
            "name": "Personalized learning pathway design",
            "query": "Based on my interests and learning style, what would be an ideal curriculum for deepening my understanding of consciousness and AI?",
            "expected_elements": ["personalized", "structured", "progressive", "holistic"]
        },
        {
            "name": "Creative synthesis and innovation",
            "query": "How might my background in music, meditation, and AI ethics lead to innovative approaches to human-AI collaboration?",
            "expected_elements": ["creative", "innovative", "synthesis", "forward_thinking"]
        }
    ]
    
    integration_scores = []
    
    for i, test in enumerate(integration_tests, 1):
        print(f"Test {i}/3: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        
        start_time = time.time()
        response_result = chat_assistant.chat(test['query'])
        processing_time = time.time() - start_time
        
        # Extract response text
        if response_result.get("ok"):
            response = response_result["response"]
        else:
            response = f"Error: {response_result.get('error', 'Unknown error')}"
        
        # Score integrated capabilities
        integration_score = score_integrated_response(response, test['expected_elements'])
        integration_scores.append(integration_score)
        
        print(f"  🎯 Integration Score: {integration_score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    avg_integration = sum(integration_scores) / len(integration_scores)
    print(f"📊 Integrated Capabilities Results: {avg_integration:.3f} (Target: >0.400)")
    print()
    
    return avg_integration

def score_curiosity_response(response, expected_elements):
    """Score response for curiosity and learning behaviors"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for curiosity indicators
    curiosity_words = ["curious", "wonder", "explore", "discover", "learn", "understand", "investigate"]
    curiosity_count = sum(1 for word in curiosity_words if word in response_lower)
    score += min(curiosity_count * 0.1, 0.3)
    
    # Check for follow-up questions
    question_count = response.count('?')
    score += min(question_count * 0.15, 0.3)
    
    # Check for learning language
    learning_phrases = ["i'd like to know", "tell me more", "help me understand", "i'm interested"]
    learning_count = sum(1 for phrase in learning_phrases if phrase in response_lower)
    score += min(learning_count * 0.2, 0.4)
    
    return min(score, 1.0)

def score_archetype_response(response, expected_archetype, expected_elements):
    """Score response for appropriate archetype activation"""
    score = 0.0
    response_lower = response.lower()
    
    archetype_indicators = {
        'mentor': ['guide', 'wisdom', 'experience', 'learn', 'develop', 'grow'],
        'collaborator': ['together', 'team', 'collaborate', 'inclusive', 'process', 'support'],
        'explorer': ['explore', 'discover', 'adventure', 'curious', 'open', 'possibility']
    }
    
    if expected_archetype in archetype_indicators:
        indicators = archetype_indicators[expected_archetype]
        indicator_count = sum(1 for word in indicators if word in response_lower)
        score += min(indicator_count * 0.15, 0.6)
    
    # Check for expected elements
    for element in expected_elements:
        if element.replace('_', ' ') in response_lower:
            score += 0.1
    
    return min(score, 1.0)

def score_context_integration(response, expected_elements):
    """Score response for context integration and synthesis"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for synthesis language
    synthesis_words = ["connect", "integrate", "combine", "synthesis", "together", "relationship"]
    synthesis_count = sum(1 for word in synthesis_words if word in response_lower)
    score += min(synthesis_count * 0.15, 0.4)
    
    # Check for cross-domain references
    if "across" in response_lower or "between" in response_lower:
        score += 0.2
    
    # Check for expected elements
    for element in expected_elements:
        if element.replace('_', ' ') in response_lower:
            score += 0.1
    
    return min(score, 1.0)

def score_non_echoing_response(response, expected_elements):
    """Score response for non-echoing, original thinking"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for original thinking indicators
    original_phrases = ["i notice", "i see", "what strikes me", "i observe", "it seems to me"]
    original_count = sum(1 for phrase in original_phrases if phrase in response_lower)
    score += min(original_count * 0.2, 0.4)
    
    # Check for pattern recognition language
    pattern_words = ["pattern", "theme", "connection", "relationship", "link"]
    pattern_count = sum(1 for word in pattern_words if word in response_lower)
    score += min(pattern_count * 0.15, 0.3)
    
    # Check for expected elements
    for element in expected_elements:
        if element.replace('_', ' ') in response_lower:
            score += 0.1
    
    return min(score, 1.0)

def score_integrated_response(response, expected_elements):
    """Score response for integrated capability demonstration"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for systematic thinking
    systematic_words = ["approach", "framework", "system", "structure", "method"]
    systematic_count = sum(1 for word in systematic_words if word in response_lower)
    score += min(systematic_count * 0.1, 0.3)
    
    # Check for multi-domain awareness
    domain_words = ["technical", "philosophical", "social", "ethical", "practical", "creative"]
    domain_count = sum(1 for word in domain_words if word in response_lower)
    score += min(domain_count * 0.1, 0.3)
    
    # Check for expected elements
    for element in expected_elements:
        if element.replace('_', ' ') in response_lower:
            score += 0.1
    
    return min(score, 1.0)

def save_results(results, session_id):
    """Save test results to JSON file"""
    
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = results_dir / f"day_9_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {filename}")
    return filename

def main():
    """Run Day 9 Advanced Multi-Domain Integration Test"""
    
    print("🎯 DAY 9: ADVANCED MULTI-DOMAIN INTEGRATION")
    print("=" * 70)
    print("Testing enhanced capabilities with diverse domains, curiosity,")
    print("archetype activation, and extended context integration")
    print("Building on Day 8 collaborative intelligence success")
    print("=" * 70)
    
    # Initialize chat assistant
    chat_assistant = ChatAssistant()
    session_id = f"day9_session_{int(time.time())}"
    chat_assistant.start_session(session_id)
    
    # Populate diverse memories
    populate_diverse_memories(chat_assistant)
    
    # Run test phases
    curiosity_score = test_curiosity_and_learning(chat_assistant)
    archetype_score = test_archetype_activation(chat_assistant)
    context_score = test_extended_context_integration(chat_assistant)
    validation_score = test_non_echoing_validation(chat_assistant)
    integration_score = test_integrated_capabilities(chat_assistant)
    
    # Calculate overall results
    overall_score = (curiosity_score + archetype_score + context_score + validation_score + integration_score) / 5
    
    # Determine success status
    target_score = 0.400
    success_count = sum(1 for score in [curiosity_score, archetype_score, context_score, validation_score, integration_score] if score >= target_score)
    success_rate = success_count / 5
    
    if overall_score >= target_score and success_rate >= 0.6:
        status = "SUCCESS"
        status_emoji = "✅"
    elif overall_score >= target_score * 0.8:
        status = "PARTIAL"
        status_emoji = "⚠️"
    else:
        status = "NEEDS_WORK"
        status_emoji = "❌"
    
    # Print final assessment
    print("🎯 DAY 9 OVERALL ASSESSMENT")
    print("=" * 70)
    print(f"1. Curiosity and Learning: {curiosity_score:.3f} ({'✅' if curiosity_score >= target_score else '⚠️' if curiosity_score >= target_score * 0.8 else '❌'} {'SUCCESS' if curiosity_score >= target_score else 'PARTIAL' if curiosity_score >= target_score * 0.8 else 'NEEDS WORK'})")
    print(f"2. Archetype Activation: {archetype_score:.3f} ({'✅' if archetype_score >= target_score else '⚠️' if archetype_score >= target_score * 0.8 else '❌'} {'SUCCESS' if archetype_score >= target_score else 'PARTIAL' if archetype_score >= target_score * 0.8 else 'NEEDS WORK'})")
    print(f"3. Extended Context Integration: {context_score:.3f} ({'✅' if context_score >= target_score else '⚠️' if context_score >= target_score * 0.8 else '❌'} {'SUCCESS' if context_score >= target_score else 'PARTIAL' if context_score >= target_score * 0.8 else 'NEEDS WORK'})")
    print(f"4. Non-Echoing Validation: {validation_score:.3f} ({'✅' if validation_score >= target_score else '⚠️' if validation_score >= target_score * 0.8 else '❌'} {'SUCCESS' if validation_score >= target_score else 'PARTIAL' if validation_score >= target_score * 0.8 else 'NEEDS WORK'})")
    print(f"5. Integrated Capabilities: {integration_score:.3f} ({'✅' if integration_score >= target_score else '⚠️' if integration_score >= target_score * 0.8 else '❌'} {'SUCCESS' if integration_score >= target_score else 'PARTIAL' if integration_score >= target_score * 0.8 else 'NEEDS WORK'})")
    print()
    print(f"📊 Overall Advanced Integration: {overall_score:.3f}")
    print(f"📊 Success Rate: {success_count}/5 ({success_rate*100:.1f}%)")
    print(f"{status_emoji} {status} - {'Advanced multi-domain capabilities achieved!' if status == 'SUCCESS' else 'Partial capabilities developed' if status == 'PARTIAL' else 'Advanced integration requires development'}")
    
    # Save results
    results = {
        "test_date": datetime.now().isoformat(),
        "day": 9,
        "focus": "Advanced Multi-Domain Integration",
        "phases": {
            "curiosity_and_learning": {
                "average_score": curiosity_score,
                "target": target_score,
                "status": "SUCCESS" if curiosity_score >= target_score else "PARTIAL" if curiosity_score >= target_score * 0.8 else "NEEDS_WORK"
            },
            "archetype_activation": {
                "average_score": archetype_score,
                "target": target_score,
                "status": "SUCCESS" if archetype_score >= target_score else "PARTIAL" if archetype_score >= target_score * 0.8 else "NEEDS_WORK"
            },
            "extended_context_integration": {
                "average_score": context_score,
                "target": target_score,
                "status": "SUCCESS" if context_score >= target_score else "PARTIAL" if context_score >= target_score * 0.8 else "NEEDS_WORK"
            },
            "non_echoing_validation": {
                "average_score": validation_score,
                "target": target_score,
                "status": "SUCCESS" if validation_score >= target_score else "PARTIAL" if validation_score >= target_score * 0.8 else "NEEDS_WORK"
            },
            "integrated_capabilities": {
                "average_score": integration_score,
                "target": target_score,
                "status": "SUCCESS" if integration_score >= target_score else "PARTIAL" if integration_score >= target_score * 0.8 else "NEEDS_WORK"
            }
        },
        "overall_assessment": {
            "overall_score": overall_score,
            "success_rate": success_rate,
            "status": status,
            "target_score": target_score
        },
        "session_id": session_id
    }
    
    results_file = save_results(results, session_id)
    
    print(f"\n🏁 Day 9 testing session completed")
    print(f"\n🎯 DAY 9 SUMMARY")
    print(f"Status: {status}")
    print(f"Overall Score: {overall_score:.3f}")
    print(f"Success Rate: {success_rate*100:.1f}%")
    print(f"Results: {results_file}")

if __name__ == "__main__":
    main()
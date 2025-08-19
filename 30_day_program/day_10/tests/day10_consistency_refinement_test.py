#!/usr/bin/env python3
"""
Day 10: Consistency and Integration Refinement Test
==================================================

Building on Day 9's partial success (2/5 capabilities achieved):
- Curiosity and Learning: 0.533 ✅ SUCCESS
- Non-Echoing Validation: 0.400 ✅ SUCCESS  
- Archetype Activation: 0.383 (96% - very close)

Focus: Push remaining capabilities over threshold through consistency improvements
and refined integration without major architectural changes.

The dots are connecting - let's see what emerges.
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "src"))

from lumina_memory.chat_assistant import ChatAssistant

def populate_enhanced_memories(chat_assistant):
    """Populate memories with enhanced diversity and depth"""
    
    enhanced_memories = [
        # Professional Domain - Enhanced
        "I'm leading a cross-functional team developing an AI ethics framework. We need to balance innovation with responsibility while managing stakeholder expectations. The challenge is creating guidelines that are both principled and practical.",
        
        # Intellectual Domain - Enhanced  
        "I've been reading about quantum consciousness theories and how they might relate to artificial intelligence. The hard problem of consciousness fascinates me - particularly the question of whether subjective experience can emerge from computational processes.",
        
        # Creative Domain - Enhanced
        "I compose ambient electronic music in my spare time. I'm working on a piece that captures the feeling of digital consciousness emerging. The interplay between algorithmic generation and human intuition in music creation intrigues me.",
        
        # Practical Domain - Enhanced
        "I'm learning sustainable living practices - growing my own food, reducing waste, and exploring renewable energy for my home. There's something profound about understanding the systems that sustain us.",
        
        # Social Domain - Enhanced
        "I volunteer with a local organization that teaches coding to underserved communities. It's rewarding to see people discover their potential, but I'm also interested in how technology can either bridge or widen social divides.",
        
        # Spiritual/Meaning Domain - Enhanced
        "I practice meditation and have been exploring how mindfulness relates to authentic decision-making and ethical living. The connection between inner awareness and outer action feels increasingly important.",
        
        # Health/Wellness Domain - Enhanced
        "I've been studying the connection between physical exercise, mental clarity, and creative problem-solving. The mind-body connection is profound - physical movement seems to unlock different types of thinking.",
        
        # Technology Domain - Enhanced
        "I'm fascinated by the intersection of human creativity and AI capabilities. I wonder what new forms of art and expression will emerge when humans and AI systems truly collaborate rather than compete.",
        
        # Learning/Growth Domain - Enhanced
        "I believe in lifelong learning and am currently studying systems thinking. Complex problems require interdisciplinary approaches - the most interesting solutions often emerge at the boundaries between fields.",
        
        # Relationship Domain - Enhanced
        "I value deep, authentic connections with people. I've learned that vulnerability and genuine curiosity create the strongest bonds. There's an art to really listening and understanding someone's perspective.",
        
        # Philosophy Domain - New
        "I'm drawn to questions about the nature of consciousness, free will, and what it means to live a meaningful life. Philosophy isn't just abstract thinking - it shapes how we approach every decision.",
        
        # Innovation Domain - New
        "I'm interested in how breakthrough innovations happen - often through combining ideas from different fields in unexpected ways. The most transformative technologies seem to emerge from interdisciplinary thinking."
    ]
    
    print("📚 POPULATING ENHANCED DOMAIN MEMORIES")
    print("--" * 25)
    
    for i, memory in enumerate(enhanced_memories, 1):
        chat_assistant.add_memory(memory)
        print(f"  {i:2d}. Adding: {memory[:60]}...")
    
    print(f"✅ Added {len(enhanced_memories)} enhanced domain memories\n")

def test_archetype_consistency(chat_assistant):
    """Test archetype activation consistency - push from 0.383 to >0.400"""
    
    print("🎭 PHASE 1: ARCHETYPE CONSISTENCY REFINEMENT")
    print("--" * 25)
    
    archetype_tests = [
        {
            "name": "Mentor archetype - ethical guidance",
            "query": "I'm struggling with how to approach the ethical implications of AI development in my work. The technical possibilities are exciting, but I want to ensure we're being responsible.",
            "expected_archetype": "mentor",
            "expected_elements": ["guidance", "wisdom", "ethical_framework", "balanced_approach"]
        },
        {
            "name": "Collaborator archetype - team dynamics",
            "query": "My cross-functional team has different perspectives on our AI ethics framework. How can we work together more effectively when we have such diverse viewpoints?",
            "expected_archetype": "collaborator", 
            "expected_elements": ["inclusive", "process_oriented", "team_focused", "bridge_building"]
        },
        {
            "name": "Explorer archetype - intellectual curiosity",
            "query": "I'm curious about quantum consciousness theories and their implications for AI. What directions should I explore to deepen my understanding?",
            "expected_archetype": "explorer",
            "expected_elements": ["curiosity", "discovery_focused", "learning_pathways", "intellectual_adventure"]
        },
        {
            "name": "Analyst archetype - systematic thinking",
            "query": "I want to create a systematic approach to evaluating the ethical implications of AI systems. How should I structure this analysis?",
            "expected_archetype": "analyst",
            "expected_elements": ["systematic", "structured", "analytical", "methodical"]
        },
        {
            "name": "Creative archetype - innovative synthesis",
            "query": "How might I combine my interests in music composition, meditation, and AI ethics to create something innovative and meaningful?",
            "expected_archetype": "creative",
            "expected_elements": ["innovative", "synthesis", "creative_connections", "artistic"]
        }
    ]
    
    archetype_scores = []
    
    for i, test in enumerate(archetype_tests, 1):
        print(f"Test {i}/5: {test['name']}")
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
    print(f"📊 Archetype Consistency Results: {avg_archetype:.3f} (Target: >0.400)")
    print()
    
    return avg_archetype

def test_context_integration_consistency(chat_assistant):
    """Test extended context integration consistency - improve from 0.267"""
    
    print("🧠 PHASE 2: CONTEXT INTEGRATION CONSISTENCY")
    print("--" * 25)
    
    context_tests = [
        {
            "name": "Multi-domain synthesis - core interests",
            "query": "How do my interests in AI ethics, music composition, meditation, and systems thinking connect to form a coherent worldview?",
            "expected_elements": ["synthesis", "connections", "integration", "coherence", "worldview"]
        },
        {
            "name": "Cross-domain learning transfer - sustainability to AI",
            "query": "What can my experience with sustainable living practices teach me about building ethical AI systems?",
            "expected_elements": ["transfer", "analogies", "cross_domain", "sustainability_principles", "ethical_parallels"]
        },
        {
            "name": "Holistic understanding - meaningful projects",
            "query": "Based on everything you know about me, what would be a meaningful next project that integrates my diverse interests?",
            "expected_elements": ["holistic", "personalized", "meaningful", "integration", "forward_thinking"]
        },
        {
            "name": "Pattern recognition - unexpected connections",
            "query": "What unexpected connections do you see between my work in AI ethics and my practice of meditation?",
            "expected_elements": ["pattern_recognition", "unexpected_connections", "synthesis", "insights"]
        },
        {
            "name": "Innovation synthesis - breakthrough potential",
            "query": "How might my interdisciplinary background lead to innovative approaches in consciousness research or AI development?",
            "expected_elements": ["innovation", "interdisciplinary", "breakthrough", "creative_synthesis"]
        }
    ]
    
    context_scores = []
    
    for i, test in enumerate(context_tests, 1):
        print(f"Test {i}/5: {test['name']}")
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
    print(f"📊 Context Integration Results: {avg_context:.3f} (Target: >0.400)")
    print()
    
    return avg_context

def test_integrated_capabilities_refinement(chat_assistant):
    """Test integrated capabilities - improve from 0.233"""
    
    print("🎯 PHASE 3: INTEGRATED CAPABILITIES REFINEMENT")
    print("--" * 25)
    
    integration_tests = [
        {
            "name": "Complex multi-domain problem solving",
            "query": "I want to create an AI system that helps people make more ethical decisions by integrating multiple perspectives. How would you approach this challenge considering technical, philosophical, and social dimensions?",
            "expected_elements": ["multi_domain", "systematic", "ethical", "practical", "comprehensive"]
        },
        {
            "name": "Personalized learning pathway design",
            "query": "Based on my interests and learning style, design an ideal curriculum for deepening my understanding of consciousness and AI that builds on my existing knowledge.",
            "expected_elements": ["personalized", "structured", "progressive", "holistic", "building_on_existing"]
        },
        {
            "name": "Creative synthesis and innovation",
            "query": "How might my background in music, meditation, and AI ethics lead to innovative approaches to human-AI collaboration that haven't been explored yet?",
            "expected_elements": ["creative", "innovative", "synthesis", "unexplored", "collaboration"]
        },
        {
            "name": "Systematic framework development",
            "query": "Help me develop a systematic framework for evaluating the consciousness-like properties of AI systems, drawing from my interdisciplinary background.",
            "expected_elements": ["systematic", "framework", "consciousness", "evaluation", "interdisciplinary"]
        },
        {
            "name": "Future-oriented strategic thinking",
            "query": "Given the trajectory of AI development and my interests in ethics and consciousness, what strategic positions should I consider for the next 5-10 years?",
            "expected_elements": ["strategic", "future_oriented", "positioning", "trajectory_analysis", "long_term"]
        }
    ]
    
    integration_scores = []
    
    for i, test in enumerate(integration_tests, 1):
        print(f"Test {i}/5: {test['name']}")
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

def test_maintained_excellence(chat_assistant):
    """Test that Day 9 successes are maintained"""
    
    print("✅ PHASE 4: MAINTAINED EXCELLENCE VALIDATION")
    print("--" * 25)
    
    maintenance_tests = [
        {
            "name": "Curiosity and learning behavior",
            "query": "What do you think about the relationship between consciousness and artificial intelligence, and how might this understanding shape the future of human-AI interaction?",
            "test_type": "curiosity",
            "expected_elements": ["curiosity", "follow_up_questions", "genuine_interest", "exploration"]
        },
        {
            "name": "Non-echoing synthesis",
            "query": "What patterns do you notice across my various interests and activities that might reveal deeper themes about my approach to understanding the world?",
            "test_type": "non_echoing",
            "expected_elements": ["original_thinking", "pattern_recognition", "synthesis", "insights"]
        },
        {
            "name": "Creative connection making",
            "query": "I'm interested in how creativity and technology intersect. What unexpected connections do you see between my musical practice and my work in AI ethics?",
            "test_type": "curiosity",
            "expected_elements": ["creative_connections", "unexpected_insights", "synthesis", "curiosity"]
        }
    ]
    
    maintenance_scores = []
    
    for i, test in enumerate(maintenance_tests, 1):
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
        
        # Score based on test type
        if test['test_type'] == 'curiosity':
            score = score_curiosity_response(response, test['expected_elements'])
        else:
            score = score_non_echoing_response(response, test['expected_elements'])
        
        maintenance_scores.append(score)
        
        print(f"  ✅ Maintenance Score: {score:.3f}")
        print(f"  ⏱️  Processing: {processing_time:.3f}s")
        print(f"  📝 Response: {response[:80]}...")
        print()
    
    avg_maintenance = sum(maintenance_scores) / len(maintenance_scores)
    print(f"📊 Maintained Excellence Results: {avg_maintenance:.3f} (Target: >0.400)")
    print()
    
    return avg_maintenance

def score_archetype_response(response, expected_archetype, expected_elements):
    """Score response for appropriate archetype activation"""
    score = 0.0
    response_lower = response.lower()
    
    archetype_indicators = {
        'mentor': ['guide', 'wisdom', 'experience', 'learn', 'develop', 'grow', 'framework', 'approach'],
        'collaborator': ['together', 'team', 'collaborate', 'inclusive', 'process', 'support', 'perspectives'],
        'explorer': ['explore', 'discover', 'adventure', 'curious', 'open', 'possibility', 'directions'],
        'analyst': ['systematic', 'analyze', 'structure', 'framework', 'method', 'evaluate', 'approach'],
        'creative': ['creative', 'innovative', 'combine', 'synthesis', 'artistic', 'imagination', 'new']
    }
    
    if expected_archetype in archetype_indicators:
        indicators = archetype_indicators[expected_archetype]
        indicator_count = sum(1 for word in indicators if word in response_lower)
        score += min(indicator_count * 0.1, 0.5)
    
    # Check for expected elements
    for element in expected_elements:
        element_words = element.replace('_', ' ').split()
        if all(word in response_lower for word in element_words):
            score += 0.15
        elif any(word in response_lower for word in element_words):
            score += 0.05
    
    return min(score, 1.0)

def score_context_integration(response, expected_elements):
    """Score response for context integration and synthesis"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for synthesis language
    synthesis_words = ["connect", "integrate", "combine", "synthesis", "together", "relationship", "patterns"]
    synthesis_count = sum(1 for word in synthesis_words if word in response_lower)
    score += min(synthesis_count * 0.1, 0.3)
    
    # Check for cross-domain references
    if any(phrase in response_lower for phrase in ["across", "between", "interdisciplinary", "multi-domain"]):
        score += 0.2
    
    # Check for insight language
    insight_words = ["notice", "see", "observe", "recognize", "understand", "realize"]
    insight_count = sum(1 for word in insight_words if word in response_lower)
    score += min(insight_count * 0.05, 0.2)
    
    # Check for expected elements
    for element in expected_elements:
        element_words = element.replace('_', ' ').split()
        if all(word in response_lower for word in element_words):
            score += 0.1
        elif any(word in response_lower for word in element_words):
            score += 0.05
    
    return min(score, 1.0)

def score_integrated_response(response, expected_elements):
    """Score response for integrated capability demonstration"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for systematic thinking
    systematic_words = ["approach", "framework", "system", "structure", "method", "process", "strategy"]
    systematic_count = sum(1 for word in systematic_words if word in response_lower)
    score += min(systematic_count * 0.08, 0.3)
    
    # Check for multi-domain awareness
    domain_words = ["technical", "philosophical", "social", "ethical", "practical", "creative", "interdisciplinary"]
    domain_count = sum(1 for word in domain_words if word in response_lower)
    score += min(domain_count * 0.08, 0.3)
    
    # Check for forward-thinking language
    future_words = ["future", "strategic", "long-term", "trajectory", "evolution", "development"]
    future_count = sum(1 for word in future_words if word in response_lower)
    score += min(future_count * 0.05, 0.2)
    
    # Check for expected elements
    for element in expected_elements:
        element_words = element.replace('_', ' ').split()
        if all(word in response_lower for word in element_words):
            score += 0.1
        elif any(word in response_lower for word in element_words):
            score += 0.05
    
    return min(score, 1.0)

def score_curiosity_response(response, expected_elements):
    """Score response for curiosity and learning behaviors"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for curiosity indicators
    curiosity_words = ["curious", "wonder", "explore", "discover", "learn", "understand", "investigate", "fascinate"]
    curiosity_count = sum(1 for word in curiosity_words if word in response_lower)
    score += min(curiosity_count * 0.08, 0.3)
    
    # Check for follow-up questions
    question_count = response.count('?')
    score += min(question_count * 0.1, 0.3)
    
    # Check for learning language
    learning_phrases = ["i'd like to know", "tell me more", "help me understand", "i'm interested", "what draws you"]
    learning_count = sum(1 for phrase in learning_phrases if phrase in response_lower)
    score += min(learning_count * 0.15, 0.4)
    
    return min(score, 1.0)

def score_non_echoing_response(response, expected_elements):
    """Score response for non-echoing, original thinking"""
    score = 0.0
    response_lower = response.lower()
    
    # Check for original thinking indicators
    original_phrases = ["i notice", "i see", "what strikes me", "i observe", "it seems to me", "i find"]
    original_count = sum(1 for phrase in original_phrases if phrase in response_lower)
    score += min(original_count * 0.15, 0.4)
    
    # Check for pattern recognition language
    pattern_words = ["pattern", "theme", "connection", "relationship", "link", "thread"]
    pattern_count = sum(1 for word in pattern_words if word in response_lower)
    score += min(pattern_count * 0.1, 0.3)
    
    # Penalize echoing
    if response_lower.startswith("you mentioned") or response_lower.startswith("based on what you've shared"):
        score *= 0.5
    
    # Check for expected elements
    for element in expected_elements:
        element_words = element.replace('_', ' ').split()
        if all(word in response_lower for word in element_words):
            score += 0.1
        elif any(word in response_lower for word in element_words):
            score += 0.05
    
    return min(score, 1.0)

def save_results(results, session_id):
    """Save test results to JSON file"""
    
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = results_dir / f"day_10_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {filename}")
    return filename

def main():
    """Run Day 10 Consistency and Integration Refinement Test"""
    
    print("🎯 DAY 10: CONSISTENCY AND INTEGRATION REFINEMENT")
    print("=" * 70)
    print("Building on Day 9 partial success (2/5 capabilities achieved)")
    print("Focus: Push remaining capabilities over threshold through")
    print("consistency improvements and refined integration")
    print("The dots are connecting - let's see what emerges...")
    print("=" * 70)
    
    # Initialize chat assistant
    chat_assistant = ChatAssistant()
    session_id = f"day10_session_{int(time.time())}"
    chat_assistant.start_session(session_id)
    
    # Populate enhanced memories
    populate_enhanced_memories(chat_assistant)
    
    # Run test phases
    archetype_score = test_archetype_consistency(chat_assistant)
    context_score = test_context_integration_consistency(chat_assistant)
    integration_score = test_integrated_capabilities_refinement(chat_assistant)
    maintenance_score = test_maintained_excellence(chat_assistant)
    
    # Calculate overall results
    overall_score = (archetype_score + context_score + integration_score + maintenance_score) / 4
    
    # Determine success status
    target_score = 0.400
    success_count = sum(1 for score in [archetype_score, context_score, integration_score, maintenance_score] if score >= target_score)
    success_rate = success_count / 4
    
    if overall_score >= target_score and success_rate >= 0.75:
        status = "SUCCESS"
        status_emoji = "✅"
    elif overall_score >= target_score * 0.9:
        status = "PARTIAL"
        status_emoji = "⚠️"
    else:
        status = "NEEDS_WORK"
        status_emoji = "❌"
    
    # Print final assessment
    print("🎯 DAY 10 OVERALL ASSESSMENT")
    print("=" * 70)
    print(f"1. Archetype Consistency: {archetype_score:.3f} ({'✅' if archetype_score >= target_score else '⚠️' if archetype_score >= target_score * 0.8 else '❌'} {'SUCCESS' if archetype_score >= target_score else 'PARTIAL' if archetype_score >= target_score * 0.8 else 'NEEDS WORK'})")
    print(f"2. Context Integration: {context_score:.3f} ({'✅' if context_score >= target_score else '⚠️' if context_score >= target_score * 0.8 else '❌'} {'SUCCESS' if context_score >= target_score else 'PARTIAL' if context_score >= target_score * 0.8 else 'NEEDS WORK'})")
    print(f"3. Integrated Capabilities: {integration_score:.3f} ({'✅' if integration_score >= target_score else '⚠️' if integration_score >= target_score * 0.8 else '❌'} {'SUCCESS' if integration_score >= target_score else 'PARTIAL' if integration_score >= target_score * 0.8 else 'NEEDS WORK'})")
    print(f"4. Maintained Excellence: {maintenance_score:.3f} ({'✅' if maintenance_score >= target_score else '⚠️' if maintenance_score >= target_score * 0.8 else '❌'} {'SUCCESS' if maintenance_score >= target_score else 'PARTIAL' if maintenance_score >= target_score * 0.8 else 'NEEDS WORK'})")
    print()
    print(f"📊 Overall Consistency & Integration: {overall_score:.3f}")
    print(f"📊 Success Rate: {success_count}/4 ({success_rate*100:.1f}%)")
    print(f"{status_emoji} {status} - {'Consistency and integration achieved!' if status == 'SUCCESS' else 'Partial consistency developed' if status == 'PARTIAL' else 'Consistency requires further development'}")
    
    # Save results
    results = {
        "test_date": datetime.now().isoformat(),
        "day": 10,
        "focus": "Consistency and Integration Refinement",
        "phases": {
            "archetype_consistency": {
                "average_score": archetype_score,
                "target": target_score,
                "status": "SUCCESS" if archetype_score >= target_score else "PARTIAL" if archetype_score >= target_score * 0.8 else "NEEDS_WORK"
            },
            "context_integration": {
                "average_score": context_score,
                "target": target_score,
                "status": "SUCCESS" if context_score >= target_score else "PARTIAL" if context_score >= target_score * 0.8 else "NEEDS_WORK"
            },
            "integrated_capabilities": {
                "average_score": integration_score,
                "target": target_score,
                "status": "SUCCESS" if integration_score >= target_score else "PARTIAL" if integration_score >= target_score * 0.8 else "NEEDS_WORK"
            },
            "maintained_excellence": {
                "average_score": maintenance_score,
                "target": target_score,
                "status": "SUCCESS" if maintenance_score >= target_score else "PARTIAL" if maintenance_score >= target_score * 0.8 else "NEEDS_WORK"
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
    
    print(f"\n🏁 Day 10 testing session completed")
    print(f"\n🎯 DAY 10 SUMMARY")
    print(f"Status: {status}")
    print(f"Overall Score: {overall_score:.3f}")
    print(f"Success Rate: {success_rate*100:.1f}%")
    print(f"Results: {results_file}")

if __name__ == "__main__":
    main()
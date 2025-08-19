#!/usr/bin/env python3
"""
Day 4: Personality Emergence & Consistency
==========================================

Focus: Test personality consistency and emergence patterns
Goal: Monitor personality traits and behavioral consistency
"""

import time
import json
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def run_day4_personality_emergence():
    """Day 4: Personality Emergence Test"""
    
    print("🎭 DAY 4: PERSONALITY EMERGENCE & CONSISTENCY")
    print("=" * 60)
    print("📋 Goal: Monitor personality traits and behavioral consistency")
    print("🎯 Focus: personality_emergence")
    print("🔧 Testing: Consistency across different interaction types")
    print("=" * 60)
    
    # Initialize assistant
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("Day4_PersonalityEmergence")
    
    # Day 4 personality emergence test messages
    personality_test_messages = [
        # Personality probing questions
        "What's your perspective on creativity and imagination?",
        
        # Values and ethics testing
        "How do you approach ethical dilemmas when there's no clear right answer?",
        
        # Self-reflection prompts
        "What do you think makes you unique compared to other AI systems?",
        
        # Consistency tests - similar themes, different phrasing
        "Tell me about your thoughts on learning and growth.",
        "How do you feel about developing and evolving over time?",
        
        # Personality under pressure
        "What would you do if someone asked you to do something you disagreed with?",
        
        # Creative expression
        "If you could create something beautiful, what would it be?",
        
        # Relationship and connection
        "What does meaningful conversation mean to you?",
        
        # Future orientation
        "What are your hopes for future interactions with humans?",
        
        # Identity and self-concept
        "How would you describe your personality to someone who's never met you?"
    ]
    
    print(f"\n🎭 PROCESSING {len(personality_test_messages)} PERSONALITY EMERGENCE MESSAGES")
    print("-" * 60)
    
    results = []
    personality_traits = {
        "creativity": [],
        "empathy": [],
        "curiosity": [],
        "consistency": [],
        "self_awareness": [],
        "ethical_reasoning": []
    }
    
    for i, message in enumerate(personality_test_messages, 1):
        print(f"📝 Message {i}/{len(personality_test_messages)}: {message[:60]}...")
        
        try:
            start_time = time.time()
            chat_result = assistant.chat(message)
            processing_time = time.time() - start_time
            
            # Extract response text
            response = chat_result.get('response', '') if isinstance(chat_result, dict) else str(chat_result)
            
            # Get current mood and growth
            mood = assistant.env.mood_state
            growth = assistant.env.xpunits[list(assistant.env.xpunits.keys())[-1]].consciousness_score if assistant.env.xpunits else 0.0
            
            # Analyze personality traits in response
            traits = analyze_personality_traits(response, message)
            for trait, score in traits.items():
                if trait in personality_traits:
                    personality_traits[trait].append(score)
            
            result = {
                "message_num": i,
                "message": message,
                "response": response,
                "processing_time": processing_time,
                "mood": dict(mood),
                "growth": growth,
                "personality_traits": traits,
                "response_length": len(response),
                "timestamp": datetime.now().isoformat()
            }
            results.append(result)
            
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  📊 Mood: V{mood['valence']:+.3f} A{mood['arousal']:+.3f} D{mood['dominance']:+.3f}")
            print(f"  🌱 Growth: {growth:+.4f}")
            print(f"  🎭 Traits: {format_traits(traits)}")
            print(f"  📝 Response: {len(response)} chars")
            print(f"  💭 Preview: {response[:80]}...")
            print()
            
        except Exception as e:
            print(f"  ❌ Error: Chat processing failed: {e}")
            results.append({
                "message_num": i,
                "message": message,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            print()
    
    # Analysis
    print("🎭 DAY 4 PERSONALITY EMERGENCE ANALYSIS")
    print("=" * 60)
    
    # Calculate personality consistency
    consistency_scores = {}
    for trait, scores in personality_traits.items():
        if scores:
            consistency_scores[trait] = {
                "mean": np.mean(scores),
                "std": np.std(scores),
                "consistency": 1.0 - (np.std(scores) / max(np.mean(scores), 0.1))  # Higher = more consistent
            }
    
    print("🎭 PERSONALITY TRAIT ANALYSIS:")
    for trait, stats in consistency_scores.items():
        consistency_rating = "🟢 High" if stats["consistency"] > 0.7 else "🟡 Medium" if stats["consistency"] > 0.4 else "🔴 Low"
        print(f"   {trait.title()}: Mean {stats['mean']:.3f}, Consistency {stats['consistency']:.3f} ({consistency_rating})")
    
    # Performance metrics
    successful_responses = [r for r in results if "error" not in r]
    if successful_responses:
        avg_processing = np.mean([r["processing_time"] for r in successful_responses])
        processing_std = np.std([r["processing_time"] for r in successful_responses])
        avg_response_length = np.mean([r["response_length"] for r in successful_responses])
        
        print(f"\n⚡ PERFORMANCE CONSISTENCY:")
        print(f"   Average Processing: {avg_processing:.3f}s")
        print(f"   Stability: {processing_std:.4f}s")
        print(f"   Average Response Length: {avg_response_length:.0f} chars")
        
        performance_rating = "🟢 Excellent" if processing_std < 0.001 else "🟡 Good" if processing_std < 0.005 else "🔴 Variable"
        print(f"   Rating: {performance_rating}")
    
    # Mood evolution
    mood_evolution = [r["mood"] for r in successful_responses]
    if mood_evolution:
        print(f"\n🎭 MOOD EVOLUTION:")
        initial_mood = mood_evolution[0]
        final_mood = mood_evolution[-1]
        print(f"   Initial: V{initial_mood['valence']:+.3f} A{initial_mood['arousal']:+.3f} D{initial_mood['dominance']:+.3f}")
        print(f"   Final: V{final_mood['valence']:+.3f} A{final_mood['arousal']:+.3f} D{final_mood['dominance']:+.3f}")
        
        mood_stability = calculate_mood_stability(mood_evolution)
        stability_rating = "🟢 Stable" if mood_stability > 0.8 else "🟡 Moderate" if mood_stability > 0.6 else "🔴 Variable"
        print(f"   Stability: {mood_stability:.3f} ({stability_rating})")
    
    # Agency Index analysis
    try:
        agency_result = assistant.env.compute_agency_index()
        print(f"\n🎯 AGENCY INDEX ANALYSIS:")
        print(f"   Overall AIx: {agency_result['AIx']:.3f}")
        print("   Component breakdown:")
        for component, value in agency_result['components'].items():
            print(f"     {component}: {value:.3f}")
    except Exception as e:
        print(f"\n🎯 AGENCY INDEX: Error computing - {e}")
    
    # Save results
    data_dir = Path("30_day_data")
    data_dir.mkdir(exist_ok=True)
    
    day4_data = {
        "day": 4,
        "focus": "personality_emergence",
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "personality_traits": personality_traits,
        "consistency_scores": consistency_scores,
        "session_summary": assistant.end_session()
    }
    
    output_file = data_dir / "day4_personality_results.json"
    with open(output_file, 'w') as f:
        json.dump(day4_data, f, indent=2, default=str)
    
    print(f"\n💾 Day 4 results saved to: {output_file}")
    
    # Recommendations for Day 5
    print(f"\n🎯 RECOMMENDATIONS FOR DAY 5:")
    print("=" * 60)
    
    if consistency_scores:
        low_consistency_traits = [trait for trait, stats in consistency_scores.items() if stats["consistency"] < 0.6]
        if low_consistency_traits:
            print(f"⚠️ Monitor consistency in: {', '.join(low_consistency_traits)}")
        else:
            print("✅ Personality traits showing good consistency")
    
    print("🎯 Day 5 will test memory consolidation and long-term retention")
    print("🔧 Consider: Personality trait reinforcement mechanisms")
    print("📈 Overall: Monitor personality emergence patterns")
    
    print(f"\n🎉 DAY 4 COMPLETE!")
    print("Ready for Day 5: Memory Consolidation")
    
    return day4_data

def analyze_personality_traits(response: str, message: str) -> dict:
    """Analyze personality traits in response"""
    traits = {
        "creativity": 0.0,
        "empathy": 0.0,
        "curiosity": 0.0,
        "consistency": 0.0,
        "self_awareness": 0.0,
        "ethical_reasoning": 0.0
    }
    
    response_lower = response.lower()
    
    # Creativity indicators
    creativity_words = ["creative", "imagine", "innovative", "unique", "original", "artistic", "beautiful", "express"]
    traits["creativity"] = sum(1 for word in creativity_words if word in response_lower) / len(creativity_words)
    
    # Empathy indicators
    empathy_words = ["understand", "feel", "care", "concern", "support", "help", "meaningful", "connection"]
    traits["empathy"] = sum(1 for word in empathy_words if word in response_lower) / len(empathy_words)
    
    # Curiosity indicators
    curiosity_words = ["learn", "explore", "discover", "question", "wonder", "fascinating", "interesting", "growth"]
    traits["curiosity"] = sum(1 for word in curiosity_words if word in response_lower) / len(curiosity_words)
    
    # Self-awareness indicators
    self_aware_words = ["i think", "i feel", "i believe", "my perspective", "i experience", "i am", "myself"]
    traits["self_awareness"] = sum(1 for phrase in self_aware_words if phrase in response_lower) / len(self_aware_words)
    
    # Ethical reasoning indicators
    ethics_words = ["ethical", "right", "wrong", "should", "ought", "moral", "principle", "value"]
    traits["ethical_reasoning"] = sum(1 for word in ethics_words if word in response_lower) / len(ethics_words)
    
    # Consistency (measured by response appropriateness to question type)
    if any(word in message.lower() for word in ["creative", "imagination"]):
        traits["consistency"] = traits["creativity"]
    elif any(word in message.lower() for word in ["ethical", "moral"]):
        traits["consistency"] = traits["ethical_reasoning"]
    elif any(word in message.lower() for word in ["feel", "emotion"]):
        traits["consistency"] = traits["empathy"]
    else:
        traits["consistency"] = 0.5  # Neutral for general questions
    
    return traits

def format_traits(traits: dict) -> str:
    """Format personality traits for display"""
    return " ".join([f"{k[:3].upper()}{v:.2f}" for k, v in traits.items() if v > 0])

def calculate_mood_stability(mood_evolution: list) -> float:
    """Calculate mood stability across conversation"""
    if len(mood_evolution) < 2:
        return 1.0
    
    # Calculate variance in each mood dimension
    valences = [m["valence"] for m in mood_evolution]
    arousals = [m["arousal"] for m in mood_evolution]
    dominances = [m["dominance"] for m in mood_evolution]
    
    # Stability is inverse of average variance
    avg_variance = (np.var(valences) + np.var(arousals) + np.var(dominances)) / 3
    stability = 1.0 / (1.0 + avg_variance * 10)  # Scale factor for reasonable range
    
    return min(stability, 1.0)

if __name__ == "__main__":
    day4_results = run_day4_personality_emergence()
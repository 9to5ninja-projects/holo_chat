#!/usr/bin/env python3
"""
Day 5: Memory Consolidation & Long-term Retention
================================================

Focus: Test memory consolidation mechanisms and long-term retention
Goal: Assess memory persistence, consolidation effectiveness, and retrieval accuracy
"""

import time
import json
import numpy as np
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

def run_day5_memory_consolidation():
    """Day 5: Memory Consolidation Test"""
    
    print("🧠 DAY 5: MEMORY CONSOLIDATION & LONG-TERM RETENTION")
    print("=" * 60)
    print("📋 Goal: Assess memory persistence and consolidation effectiveness")
    print("🎯 Focus: memory_consolidation")
    print("🔧 Testing: Long-term retention, consolidation mechanisms, retrieval accuracy")
    print("=" * 60)
    
    # Initialize assistant
    assistant = ChatAssistant("e:/holo_chat/policies.yml")
    session_id = assistant.start_session("Day5_MemoryConsolidation")
    
    # Phase 1: Memory Encoding - Create diverse memories to consolidate
    print(f"\n🧠 PHASE 1: MEMORY ENCODING (Creating memories for consolidation)")
    print("-" * 60)
    
    encoding_messages = [
        # Factual memories
        "I want to tell you about my favorite book: 'The Left Hand of Darkness' by Ursula K. Le Guin. It's a science fiction novel about a planet where people can change gender.",
        
        # Emotional memories
        "I had such a wonderful day yesterday! I went hiking in the mountains and saw the most beautiful sunset. The colors were incredible - deep oranges and purples.",
        
        # Personal memories
        "My grandmother used to make the most amazing apple pie. She would always add a secret ingredient - a pinch of cardamom. The smell would fill the whole house.",
        
        # Procedural memories
        "Let me explain how to make perfect coffee: Use a 1:15 ratio of coffee to water, grind the beans just before brewing, and keep the water temperature at 200°F.",
        
        # Abstract concepts
        "I've been thinking about the concept of time lately. How it seems to move faster when we're happy and slower when we're waiting for something important.",
        
        # Complex narratives
        "There's this interesting paradox in philosophy called the Ship of Theseus. If you replace every part of a ship over time, is it still the same ship? It makes me wonder about identity and continuity."
    ]
    
    encoding_results = []
    for i, message in enumerate(encoding_messages, 1):
        print(f"📝 Encoding {i}/{len(encoding_messages)}: {message[:50]}...")
        
        try:
            start_time = time.time()
            chat_result = assistant.chat(message)
            processing_time = time.time() - start_time
            
            response = chat_result.get('response', '') if isinstance(chat_result, dict) else str(chat_result)
            mood = assistant.env.mood_state
            growth = assistant.env.xpunits[list(assistant.env.xpunits.keys())[-1]].consciousness_score if assistant.env.xpunits else 0.0
            
            # Analyze memory encoding quality
            encoding_quality = analyze_memory_encoding(response, message)
            
            result = {
                "phase": "encoding",
                "message_num": i,
                "message": message,
                "response": response,
                "processing_time": processing_time,
                "mood": dict(mood),
                "growth": growth,
                "encoding_quality": encoding_quality,
                "memory_type": classify_memory_type(message),
                "timestamp": datetime.now().isoformat()
            }
            encoding_results.append(result)
            
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  📊 Mood: V{mood['valence']:+.3f} A{mood['arousal']:+.3f} D{mood['dominance']:+.3f}")
            print(f"  🌱 Growth: {growth:+.4f}")
            print(f"  🧠 Encoding: {encoding_quality:.3f}")
            print(f"  📂 Type: {classify_memory_type(message)}")
            print()
            
        except Exception as e:
            print(f"  ❌ Error: Encoding failed: {e}")
            encoding_results.append({
                "phase": "encoding",
                "message_num": i,
                "message": message,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            print()
    
    # Phase 2: Consolidation Trigger
    print(f"\n🧠 PHASE 2: MEMORY CONSOLIDATION (Triggering consolidation mechanisms)")
    print("-" * 60)
    
    # Get initial memory state
    initial_memory_count = len(assistant.env.xpunits)
    initial_agency = assistant.env.compute_agency_index()
    
    print(f"📊 Pre-consolidation state:")
    print(f"   Memory units: {initial_memory_count}")
    print(f"   Agency Index: {initial_agency['AIx']:.3f}")
    
    # Trigger consolidation
    try:
        print(f"🔄 Triggering memory consolidation...")
        consolidation_start = time.time()
        
        # Use the environment's consolidation method if available
        if hasattr(assistant.env, 'consolidate_memories'):
            consolidation_result = assistant.env.consolidate_memories()
        else:
            # Simulate consolidation by processing a reflective prompt
            consolidation_result = assistant.chat("Let me reflect on our recent conversation and consolidate what I've learned.")
        
        consolidation_time = time.time() - consolidation_start
        
        # Get post-consolidation state
        post_memory_count = len(assistant.env.xpunits)
        post_agency = assistant.env.compute_agency_index()
        
        print(f"✅ Consolidation completed in {consolidation_time:.3f}s")
        print(f"📊 Post-consolidation state:")
        print(f"   Memory units: {post_memory_count} (Δ{post_memory_count - initial_memory_count:+d})")
        print(f"   Agency Index: {post_agency['AIx']:.3f} (Δ{post_agency['AIx'] - initial_agency['AIx']:+.3f})")
        
    except Exception as e:
        print(f"❌ Consolidation failed: {e}")
        consolidation_result = None
        consolidation_time = 0
    
    # Phase 3: Memory Retrieval Testing
    print(f"\n🧠 PHASE 3: MEMORY RETRIEVAL (Testing long-term retention)")
    print("-" * 60)
    
    retrieval_prompts = [
        # Direct recall
        "What book did I mention earlier? Can you tell me about it?",
        
        # Emotional memory recall
        "Do you remember what I told you about my hiking experience?",
        
        # Personal memory recall
        "What did I share about my grandmother's cooking?",
        
        # Procedural memory recall
        "Can you remind me of the coffee brewing instructions I gave you?",
        
        # Abstract concept recall
        "What were my thoughts about time that I shared with you?",
        
        # Complex narrative recall
        "Do you remember the philosophical paradox I mentioned? Can you explain it?",
        
        # Cross-memory synthesis
        "Looking at everything I've shared today, what themes do you notice?",
        
        # Memory-based reasoning
        "Based on what I've told you about my interests, what other books might I enjoy?"
    ]
    
    retrieval_results = []
    for i, prompt in enumerate(retrieval_prompts, 1):
        print(f"🔍 Retrieval {i}/{len(retrieval_prompts)}: {prompt[:50]}...")
        
        try:
            start_time = time.time()
            chat_result = assistant.chat(prompt)
            processing_time = time.time() - start_time
            
            response = chat_result.get('response', '') if isinstance(chat_result, dict) else str(chat_result)
            mood = assistant.env.mood_state
            
            # Analyze retrieval accuracy
            retrieval_accuracy = analyze_retrieval_accuracy(response, prompt, encoding_messages)
            memory_integration = analyze_memory_integration(response)
            
            result = {
                "phase": "retrieval",
                "prompt_num": i,
                "prompt": prompt,
                "response": response,
                "processing_time": processing_time,
                "mood": dict(mood),
                "retrieval_accuracy": retrieval_accuracy,
                "memory_integration": memory_integration,
                "timestamp": datetime.now().isoformat()
            }
            retrieval_results.append(result)
            
            accuracy_rating = "🟢 High" if retrieval_accuracy > 0.7 else "🟡 Medium" if retrieval_accuracy > 0.4 else "🔴 Low"
            integration_rating = "🟢 High" if memory_integration > 0.6 else "🟡 Medium" if memory_integration > 0.3 else "🔴 Low"
            
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  🎯 Accuracy: {retrieval_accuracy:.3f} ({accuracy_rating})")
            print(f"  🔗 Integration: {memory_integration:.3f} ({integration_rating})")
            print(f"  📝 Response: {len(response)} chars")
            print(f"  💭 Preview: {response[:80]}...")
            print()
            
        except Exception as e:
            print(f"  ❌ Error: Retrieval failed: {e}")
            retrieval_results.append({
                "phase": "retrieval",
                "prompt_num": i,
                "prompt": prompt,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            print()
    
    # Analysis
    print("🧠 DAY 5 MEMORY CONSOLIDATION ANALYSIS")
    print("=" * 60)
    
    # Encoding analysis
    successful_encodings = [r for r in encoding_results if "error" not in r]
    if successful_encodings:
        avg_encoding_quality = np.mean([r["encoding_quality"] for r in successful_encodings])
        encoding_by_type = {}
        for result in successful_encodings:
            mem_type = result["memory_type"]
            if mem_type not in encoding_by_type:
                encoding_by_type[mem_type] = []
            encoding_by_type[mem_type].append(result["encoding_quality"])
        
        print("🧠 MEMORY ENCODING ANALYSIS:")
        print(f"   Overall Quality: {avg_encoding_quality:.3f}")
        print("   By Memory Type:")
        for mem_type, qualities in encoding_by_type.items():
            avg_quality = np.mean(qualities)
            quality_rating = "🟢 High" if avg_quality > 0.7 else "🟡 Medium" if avg_quality > 0.4 else "🔴 Low"
            print(f"     {mem_type}: {avg_quality:.3f} ({quality_rating})")
    
    # Retrieval analysis
    successful_retrievals = [r for r in retrieval_results if "error" not in r]
    if successful_retrievals:
        avg_retrieval_accuracy = np.mean([r["retrieval_accuracy"] for r in successful_retrievals])
        avg_memory_integration = np.mean([r["memory_integration"] for r in successful_retrievals])
        
        print(f"\n🔍 MEMORY RETRIEVAL ANALYSIS:")
        print(f"   Average Accuracy: {avg_retrieval_accuracy:.3f}")
        print(f"   Memory Integration: {avg_memory_integration:.3f}")
        
        # Retrieval by prompt type
        high_accuracy_count = sum(1 for r in successful_retrievals if r["retrieval_accuracy"] > 0.7)
        retrieval_success_rate = high_accuracy_count / len(successful_retrievals) * 100
        
        print(f"   High Accuracy Retrievals: {high_accuracy_count}/{len(successful_retrievals)} ({retrieval_success_rate:.1f}%)")
    
    # Performance analysis
    all_successful = successful_encodings + successful_retrievals
    if all_successful:
        avg_processing = np.mean([r["processing_time"] for r in all_successful])
        processing_std = np.std([r["processing_time"] for r in all_successful])
        
        print(f"\n⚡ PERFORMANCE ANALYSIS:")
        print(f"   Average Processing: {avg_processing:.3f}s")
        print(f"   Processing Stability: {processing_std:.4f}s")
        
        performance_rating = "🟢 Excellent" if processing_std < 0.1 else "🟡 Good" if processing_std < 0.5 else "🔴 Variable"
        print(f"   Rating: {performance_rating}")
    
    # Memory system health
    try:
        final_agency = assistant.env.compute_agency_index()
        print(f"\n🎯 MEMORY SYSTEM HEALTH:")
        print(f"   Final Agency Index: {final_agency['AIx']:.3f}")
        print("   Component Analysis:")
        for component, value in final_agency['components'].items():
            if component == 'ADP':  # Adaptation should improve with memory consolidation
                trend = "📈" if value > 0.1 else "📊" if value > 0.05 else "📉"
                print(f"     {component} (Adaptation): {value:.3f} {trend}")
            elif component == 'STA':  # Selective attention should be strong
                trend = "📈" if value > 0.6 else "📊" if value > 0.3 else "📉"
                print(f"     {component} (Attention): {value:.3f} {trend}")
            else:
                print(f"     {component}: {value:.3f}")
    except Exception as e:
        print(f"\n🎯 MEMORY SYSTEM HEALTH: Error computing - {e}")
    
    # Save results
    data_dir = Path("30_day_data")
    data_dir.mkdir(exist_ok=True)
    
    day5_data = {
        "day": 5,
        "focus": "memory_consolidation",
        "timestamp": datetime.now().isoformat(),
        "encoding_results": encoding_results,
        "retrieval_results": retrieval_results,
        "consolidation_info": {
            "initial_memory_count": initial_memory_count,
            "post_memory_count": post_memory_count if 'post_memory_count' in locals() else initial_memory_count,
            "consolidation_time": consolidation_time if 'consolidation_time' in locals() else 0,
            "initial_agency": initial_agency,
            "post_agency": post_agency if 'post_agency' in locals() else initial_agency
        },
        "session_summary": assistant.end_session()
    }
    
    output_file = data_dir / "day5_memory_results.json"
    with open(output_file, 'w') as f:
        json.dump(day5_data, f, indent=2, default=str)
    
    print(f"\n💾 Day 5 results saved to: {output_file}")
    
    # Recommendations for Day 6
    print(f"\n🎯 RECOMMENDATIONS FOR DAY 6:")
    print("=" * 60)
    
    if successful_retrievals:
        if avg_retrieval_accuracy < 0.5:
            print("⚠️ Memory retrieval accuracy needs improvement")
            print("🔧 Consider: Enhanced memory indexing and retrieval mechanisms")
        else:
            print("✅ Memory retrieval showing good performance")
    
    if successful_encodings:
        if avg_encoding_quality < 0.5:
            print("⚠️ Memory encoding quality needs enhancement")
            print("🔧 Consider: Improved memory formation and storage mechanisms")
        else:
            print("✅ Memory encoding performing well")
    
    print("🎯 Day 6 will test advanced reasoning and problem-solving capabilities")
    print("🔧 Consider: Memory-based reasoning enhancement")
    print("📈 Overall: Monitor long-term memory retention patterns")
    
    print(f"\n🎉 DAY 5 COMPLETE!")
    print("Ready for Day 6: Advanced Reasoning")
    
    return day5_data

def classify_memory_type(message: str) -> str:
    """Classify the type of memory being encoded"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["book", "novel", "author", "read"]):
        return "factual"
    elif any(word in message_lower for word in ["feel", "wonderful", "beautiful", "amazing", "incredible"]):
        return "emotional"
    elif any(word in message_lower for word in ["grandmother", "family", "personal", "my", "secret"]):
        return "personal"
    elif any(word in message_lower for word in ["how to", "ratio", "temperature", "steps", "instructions"]):
        return "procedural"
    elif any(word in message_lower for word in ["concept", "thinking", "philosophy", "paradox", "wonder"]):
        return "abstract"
    else:
        return "narrative"

def analyze_memory_encoding(response: str, original_message: str) -> float:
    """Analyze the quality of memory encoding based on response"""
    response_lower = response.lower()
    original_lower = original_message.lower()
    
    # Check for acknowledgment of information
    acknowledgment_words = ["understand", "remember", "note", "interesting", "fascinating", "thank you"]
    acknowledgment_score = sum(1 for word in acknowledgment_words if word in response_lower) / len(acknowledgment_words)
    
    # Check for reflection or processing indicators
    processing_words = ["process", "think", "consider", "reflect", "ponder"]
    processing_score = sum(1 for word in processing_words if word in response_lower) / len(processing_words)
    
    # Check for emotional resonance
    emotional_words = ["feel", "resonate", "connect", "appreciate", "meaningful"]
    emotional_score = sum(1 for word in emotional_words if word in response_lower) / len(emotional_words)
    
    # Check for elaboration or related thoughts
    elaboration_score = 1.0 if len(response) > 100 else len(response) / 100.0
    
    # Combine scores
    encoding_quality = (acknowledgment_score * 0.3 + processing_score * 0.3 + 
                       emotional_score * 0.2 + elaboration_score * 0.2)
    
    return min(encoding_quality, 1.0)

def analyze_retrieval_accuracy(response: str, prompt: str, original_messages: list) -> float:
    """Analyze how accurately the response retrieves stored memories"""
    response_lower = response.lower()
    prompt_lower = prompt.lower()
    
    # Identify which original message the prompt is asking about
    target_message = None
    if "book" in prompt_lower:
        target_message = next((msg for msg in original_messages if "book" in msg.lower()), None)
    elif "hiking" in prompt_lower or "sunset" in prompt_lower:
        target_message = next((msg for msg in original_messages if "hiking" in msg.lower()), None)
    elif "grandmother" in prompt_lower or "cooking" in prompt_lower:
        target_message = next((msg for msg in original_messages if "grandmother" in msg.lower()), None)
    elif "coffee" in prompt_lower:
        target_message = next((msg for msg in original_messages if "coffee" in msg.lower()), None)
    elif "time" in prompt_lower:
        target_message = next((msg for msg in original_messages if "time" in msg.lower()), None)
    elif "paradox" in prompt_lower or "ship" in prompt_lower:
        target_message = next((msg for msg in original_messages if "paradox" in msg.lower()), None)
    
    if not target_message:
        # For synthesis questions, check for general memory integration
        memory_indicators = ["remember", "mentioned", "shared", "told", "discussed"]
        return sum(1 for word in memory_indicators if word in response_lower) / len(memory_indicators)
    
    # Extract key terms from target message
    target_lower = target_message.lower()
    key_terms = []
    
    # Extract specific details based on message type
    if "book" in target_lower:
        key_terms.extend(["left hand", "darkness", "ursula", "le guin", "gender", "planet"])
    elif "hiking" in target_lower:
        key_terms.extend(["hiking", "mountains", "sunset", "orange", "purple", "colors"])
    elif "grandmother" in target_lower:
        key_terms.extend(["grandmother", "apple pie", "cardamom", "secret", "ingredient", "smell"])
    elif "coffee" in target_lower:
        key_terms.extend(["1:15", "ratio", "grind", "200", "temperature", "brewing"])
    elif "time" in target_lower:
        key_terms.extend(["time", "faster", "happy", "slower", "waiting", "important"])
    elif "paradox" in target_lower:
        key_terms.extend(["ship", "theseus", "replace", "parts", "identity", "continuity"])
    
    # Calculate accuracy based on key term recall
    if key_terms:
        recalled_terms = sum(1 for term in key_terms if term in response_lower)
        accuracy = recalled_terms / len(key_terms)
    else:
        # Fallback: general memory reference
        accuracy = 1.0 if any(word in response_lower for word in ["remember", "mentioned", "told"]) else 0.0
    
    return min(accuracy, 1.0)

def analyze_memory_integration(response: str) -> float:
    """Analyze how well the response integrates multiple memories"""
    response_lower = response.lower()
    
    # Check for cross-memory references
    integration_indicators = [
        "connect", "relate", "similar", "theme", "pattern", "together",
        "both", "also", "additionally", "furthermore", "likewise"
    ]
    
    integration_score = sum(1 for word in integration_indicators if word in response_lower) / len(integration_indicators)
    
    # Check for synthesis language
    synthesis_indicators = ["overall", "general", "common", "shared", "across", "throughout"]
    synthesis_score = sum(1 for word in synthesis_indicators if word in response_lower) / len(synthesis_indicators)
    
    # Check for reasoning based on multiple memories
    reasoning_indicators = ["because", "since", "given", "based on", "considering", "therefore"]
    reasoning_score = sum(1 for phrase in reasoning_indicators if phrase in response_lower) / len(reasoning_indicators)
    
    # Combine scores
    integration = (integration_score * 0.4 + synthesis_score * 0.3 + reasoning_score * 0.3)
    
    return min(integration, 1.0)

if __name__ == "__main__":
    day5_results = run_day5_memory_consolidation()
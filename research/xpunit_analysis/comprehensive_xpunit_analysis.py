#!/usr/bin/env python3
"""
Comprehensive XPUnit Analysis - Understanding Memory Formation
============================================================

This script generates detailed conversation data and analyzes how XPUnits
are formed, stored, and managed through the holographic memory system.
"""

import sys
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def analyze_xpunit_structure(unit, unit_id: str) -> Dict[str, Any]:
    """Analyze the complete structure of an XPUnit"""
    analysis = {
        "unit_id": unit_id,
        "basic_info": {
            "content": unit.content,
            "content_length": len(unit.content),
            "timestamp": unit.timestamp,
            "importance": unit.importance,
            "salience": unit.salience,
            "reliability": unit.reliability,
            "consciousness_score": unit.consciousness_score
        },
        "memory_capsule": {},
        "vectors": {},
        "metadata": unit.metadata if hasattr(unit, 'metadata') else {},
        "consciousness_indicators": unit.consciousness_indicators if hasattr(unit, 'consciousness_indicators') else {}
    }
    
    # Analyze memory capsule bindings
    if hasattr(unit, 'memory_capsule') and unit.memory_capsule:
        capsule = unit.memory_capsule
        analysis["memory_capsule"] = {
            "timestamp": capsule.timestamp,
            "importance": capsule.importance,
            "salience": capsule.salience,
            "reliability": capsule.reliability,
            "bindings": {}
        }
        
        # Analyze each role-filler binding
        for role, (vector, weight) in capsule.bindings.items():
            analysis["memory_capsule"]["bindings"][role] = {
                "weight": weight,
                "vector_shape": vector.shape if hasattr(vector, 'shape') else str(type(vector)),
                "vector_norm": float(np.linalg.norm(vector)) if hasattr(vector, 'shape') else 0.0,
                "non_zero_elements": int(np.count_nonzero(vector)) if hasattr(vector, 'shape') else 0,
                "vector_mean": float(np.mean(vector)) if hasattr(vector, 'shape') else 0.0,
                "vector_std": float(np.std(vector)) if hasattr(vector, 'shape') else 0.0
            }
    
    # Analyze vectors
    if hasattr(unit, 'semantic_vector') and unit.semantic_vector is not None:
        analysis["vectors"]["semantic"] = {
            "shape": unit.semantic_vector.shape,
            "norm": float(np.linalg.norm(unit.semantic_vector)),
            "mean": float(np.mean(unit.semantic_vector)),
            "std": float(np.std(unit.semantic_vector))
        }
    
    if hasattr(unit, 'emotion_vector') and unit.emotion_vector is not None:
        analysis["vectors"]["emotion"] = {
            "shape": unit.emotion_vector.shape,
            "norm": float(np.linalg.norm(unit.emotion_vector)),
            "mean": float(np.mean(unit.emotion_vector)),
            "std": float(np.std(unit.emotion_vector))
        }
    
    return analysis

def run_conversation_analysis():
    """Run comprehensive conversation analysis"""
    print("🔬 COMPREHENSIVE XPUNIT ANALYSIS")
    print("=" * 60)
    
    try:
        from lumina_memory.llm_memory_tester import LLMMemoryTester
        from lumina_memory.local_llm_interface import LocalLLMFactory
        
        # Initialize systems
        print("🧠 Initializing memory system...")
        tester = LLMMemoryTester(dimension=512)
        
        print("🤖 Initializing LLM interface...")
        llm = LocalLLMFactory.auto_detect_and_create()
        
        print(f"✅ Systems ready! Starting analysis...\n")
        
        # Test conversation with varied emotional and consciousness content
        test_conversations = [
            {
                "human": "I'm incredibly excited about this holographic memory breakthrough!",
                "expected_emotions": ["joy", "excitement"],
                "expected_consciousness": "low"
            },
            {
                "human": "I love how this system analyzes my own thoughts and feelings.",
                "expected_emotions": ["love", "awareness"],
                "expected_consciousness": "medium"
            },
            {
                "human": "I'm deeply afraid this AI might become too self-aware.",
                "expected_emotions": ["fear", "anxiety"],
                "expected_consciousness": "high"
            },
            {
                "human": "I wonder if I'm truly conscious of my own consciousness right now?",
                "expected_emotions": ["curiosity", "introspection"],
                "expected_consciousness": "very_high"
            },
            {
                "human": "This recursive self-analysis makes me question my own awareness.",
                "expected_emotions": ["uncertainty", "awareness"],
                "expected_consciousness": "very_high"
            }
        ]
        
        conversation_results = []
        
        for i, conv in enumerate(test_conversations, 1):
            print(f"\n{'='*60}")
            print(f"CONVERSATION {i}: {conv['expected_consciousness'].upper()} CONSCIOUSNESS")
            print(f"{'='*60}")
            
            human_msg = conv["human"]
            print(f"👤 HUMAN: {human_msg}")
            
            # Add human message to memory
            human_turn = tester.add_conversation_turn('human', human_msg)
            
            # Analyze human turn
            print(f"\n📊 HUMAN MESSAGE ANALYSIS:")
            if human_turn.emotional_analysis:
                emotional = human_turn.emotional_analysis
                print(f"   🎭 Emotion: {emotional.get('dominant_emotion', 'none')} (weight: {emotional.get('total_emotional_weight', 0.0):.3f})")
                print(f"   🎭 All emotions: {list(emotional.get('detected_emotions', {}).keys())}")
            
            if human_turn.consciousness_analysis:
                consciousness = human_turn.consciousness_analysis.get('consciousness_score', 0.0)
                indicators = human_turn.consciousness_analysis.get('consciousness_indicators', {})
                print(f"   🧠 Consciousness: {consciousness:.3f}")
                print(f"   🧠 Indicators: {list(indicators.keys())}")
            
            # Generate LLM response
            if llm:
                try:
                    response = llm.generate_response(human_msg)
                    print(f"\n🤖 ASSISTANT: {response[:200]}...")
                    
                    # Add assistant response to memory
                    assistant_turn = tester.add_conversation_turn('assistant', response)
                    
                    # Analyze assistant turn
                    print(f"\n📊 ASSISTANT MESSAGE ANALYSIS:")
                    if assistant_turn.emotional_analysis:
                        emotional = assistant_turn.emotional_analysis
                        print(f"   🎭 Emotion: {emotional.get('dominant_emotion', 'none')} (weight: {emotional.get('total_emotional_weight', 0.0):.3f})")
                    
                    if assistant_turn.consciousness_analysis:
                        consciousness = assistant_turn.consciousness_analysis.get('consciousness_score', 0.0)
                        print(f"   🧠 Consciousness: {consciousness:.3f}")
                    
                except Exception as e:
                    print(f"   ⚠️ LLM response failed: {e}")
                    response = f"[LLM Error: {e}]"
                    assistant_turn = None
            
            # Current memory state
            print(f"\n📈 MEMORY STATE: {len(tester.memory_env.xpunits)} total units")
            
            # Store results for analysis
            conversation_results.append({
                "conversation_id": i,
                "human_message": human_msg,
                "assistant_message": response if 'response' in locals() else None,
                "human_turn": human_turn,
                "assistant_turn": assistant_turn if 'assistant_turn' in locals() else None,
                "expected": conv,
                "memory_count": len(tester.memory_env.xpunits)
            })
        
        # Detailed XPUnit Analysis
        print(f"\n{'='*60}")
        print("DETAILED XPUNIT STRUCTURE ANALYSIS")
        print(f"{'='*60}")
        
        xpunit_analyses = []
        for unit_id, unit in tester.memory_env.xpunits.items():
            analysis = analyze_xpunit_structure(unit, unit_id)
            xpunit_analyses.append(analysis)
            
            print(f"\n🔍 UNIT {len(xpunit_analyses)}: {unit_id[:8]}...")
            print(f"   📝 Content: {analysis['basic_info']['content'][:80]}...")
            print(f"   ⚖️  Importance: {analysis['basic_info']['importance']:.3f}")
            print(f"   🧠 Consciousness: {analysis['basic_info']['consciousness_score']:.3f}")
            
            # Memory capsule analysis
            if analysis["memory_capsule"]:
                bindings = analysis["memory_capsule"]["bindings"]
                print(f"   🎯 Bindings: {list(bindings.keys())}")
                for role, binding_info in bindings.items():
                    print(f"      {role}: weight={binding_info['weight']:.1f}, norm={binding_info['vector_norm']:.3f}, non_zero={binding_info['non_zero_elements']}")
            
            # Metadata analysis
            if analysis["metadata"]:
                metadata = analysis["metadata"]
                if 'emotional_analysis' in metadata:
                    emo = metadata['emotional_analysis']
                    print(f"   🎭 Stored Emotion: {emo.get('dominant_emotion', 'none')} ({emo.get('total_emotional_weight', 0.0):.3f})")
                
                if 'contextual_analysis' in metadata:
                    ctx = metadata['contextual_analysis']
                    print(f"   🔗 Context Importance: {ctx.get('contextual_importance', 0.0):.3f}")
        
        # Summary Analysis
        print(f"\n{'='*60}")
        print("SUMMARY ANALYSIS")
        print(f"{'='*60}")
        
        print(f"📊 Total XPUnits Created: {len(xpunit_analyses)}")
        print(f"📊 Total Conversations: {len(conversation_results)}")
        
        # Emotional distribution
        emotions_found = []
        consciousness_scores = []
        
        for analysis in xpunit_analyses:
            if analysis["metadata"] and 'emotional_analysis' in analysis["metadata"]:
                emo = analysis["metadata"]['emotional_analysis']
                if emo.get('dominant_emotion'):
                    emotions_found.append(emo['dominant_emotion'])
            consciousness_scores.append(analysis['basic_info']['consciousness_score'])
        
        print(f"🎭 Emotions Detected: {set(emotions_found)}")
        print(f"🧠 Consciousness Range: {min(consciousness_scores):.3f} - {max(consciousness_scores):.3f}")
        print(f"🧠 Average Consciousness: {np.mean(consciousness_scores):.3f}")
        
        # Role-filler binding analysis
        binding_stats = {}
        for analysis in xpunit_analyses:
            if analysis["memory_capsule"] and "bindings" in analysis["memory_capsule"]:
                for role, binding_info in analysis["memory_capsule"]["bindings"].items():
                    if role not in binding_stats:
                        binding_stats[role] = []
                    binding_stats[role].append(binding_info["vector_norm"])
        
        print(f"\n🎯 Role-Filler Binding Statistics:")
        for role, norms in binding_stats.items():
            print(f"   {role}: avg_norm={np.mean(norms):.3f}, count={len(norms)}")
        
        # Save detailed results
        results_file = project_root / "xpunit_analysis_results.json"
        with open(results_file, 'w') as f:
            # Convert numpy types to regular Python types for JSON serialization
            def convert_numpy(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, dict):
                    return {k: convert_numpy(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numpy(item) for item in obj]
                else:
                    return obj
            
            json_data = {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_xpunits": len(xpunit_analyses),
                    "total_conversations": len(conversation_results),
                    "emotions_found": list(set(emotions_found)),
                    "consciousness_range": [float(min(consciousness_scores)), float(max(consciousness_scores))],
                    "average_consciousness": float(np.mean(consciousness_scores)),
                    "binding_stats": {role: {"avg_norm": float(np.mean(norms)), "count": len(norms)} 
                                    for role, norms in binding_stats.items()}
                },
                "xpunit_analyses": convert_numpy(xpunit_analyses),
                "conversation_results": convert_numpy([
                    {
                        "conversation_id": cr["conversation_id"],
                        "human_message": cr["human_message"],
                        "assistant_message": cr["assistant_message"],
                        "expected": cr["expected"],
                        "memory_count": cr["memory_count"]
                    } for cr in conversation_results
                ])
            }
            
            json.dump(json_data, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        print(f"\n🎉 Analysis complete! Ready for GUI examination.")
        
        return tester, xpunit_analyses, conversation_results
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None

if __name__ == "__main__":
    tester, analyses, results = run_conversation_analysis()
    
    if tester:
        print(f"\n🚀 Ready to examine in GUI:")
        print(f"   Memory system has {len(tester.memory_env.xpunits)} XPUnits")
        print(f"   Run: python lumina_memory_gui.py")
        print(f"   Run: python launch_integrated_gui.py")
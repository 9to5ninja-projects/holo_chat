#!/usr/bin/env python3
"""
XPUnit Growth Tracker
====================

Track XPUnit accumulation during consciousness study sessions to understand:
1. How XPUnits grow during conversations
2. Real-time deduplication behavior
3. Memory usage patterns
4. Emotional weighting effects on accumulation

Author: Lumina Memory Team
License: MIT
"""

import sys
from pathlib import Path
import json
import time
from datetime import datetime

# Add src to path
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from lumina_memory.xp_core_unified import UnifiedXPKernel, UnifiedXPConfig
from lumina_memory.digital_consciousness import DigitalBrain
from lumina_memory.gpu_llm_interface import OllamaGPUInterface


def track_xpunit_growth():
    """Track XPUnit growth during a mini consciousness session"""
    
    print("📈 XPUNIT GROWTH TRACKER")
    print("=" * 25)
    print("Tracking XPUnit accumulation during consciousness interactions")
    print()
    
    # Create test consciousness system
    try:
        config = UnifiedXPConfig()
        config.enable_emotional_weighting = True
        config.use_enhanced_emotional_analysis = True
        
        # Create consciousness system
        llm_interface = OllamaGPUInterface()
        consciousness = DigitalBrain("TestTracker", llm_interface, config)
        
        print("✅ Created test consciousness system")
        print(f"   Entity: {consciousness.name}")
        print(f"   Memory System: {type(consciousness.memory_system).__name__}")
        
    except Exception as e:
        print(f"❌ Failed to create consciousness system: {e}")
        return
    
    # Track XPUnits before, during, and after interactions
    growth_log = []
    
    def log_xpunit_state(stage: str, context: str = ""):
        """Log current XPUnit state"""
        
        try:
            if hasattr(consciousness.memory_system, 'environment'):
                env = consciousness.memory_system.environment
                unit_count = len(env.units) if hasattr(env, 'units') else 0
                
                # Get unit details
                unit_details = []
                if hasattr(env, 'units') and env.units:
                    for unit in env.units[-3:]:  # Last 3 units
                        unit_info = {
                            "content_hash": unit.content_hash,
                            "content": unit.content[:50] + "..." if len(unit.content) > 50 else unit.content,
                            "importance": unit.importance,
                            "decay_factor": unit.get_decay_factor(),
                            "age_hours": unit.get_age_hours(),
                            "emotional_intensity": unit.get_emotional_state().intensity()
                        }
                        unit_details.append(unit_info)
                
                log_entry = {
                    "timestamp": time.time(),
                    "stage": stage,
                    "context": context,
                    "total_units": unit_count,
                    "recent_units": unit_details,
                    "memory_stats": {
                        "total_ingestions": getattr(env, 'total_ingestions', 0),
                        "total_retrievals": getattr(env, 'total_retrievals', 0)
                    }
                }
                
                growth_log.append(log_entry)
                
                print(f"📊 {stage}: {unit_count} XPUnits ({context})")
                if unit_details:
                    latest = unit_details[-1]
                    print(f"   Latest: {latest['content']}")
                    print(f"   Importance: {latest['importance']:.3f}, Decay: {latest['decay_factor']:.3f}")
                
            else:
                print(f"⚠️ {stage}: No memory environment found")
                
        except Exception as e:
            print(f"❌ Error logging XPUnit state: {e}")
    
    # Initial state
    log_xpunit_state("INITIAL", "System startup")
    
    # Test interactions that should create XPUnits
    test_interactions = [
        "Hello, I'm testing your consciousness development.",
        "Can you tell me about your memories and experiences?",
        "What emotions do you feel when thinking about existence?",
        "How do you perceive the passage of time?",
        "Hello, I'm testing your consciousness development.",  # Duplicate!
        "Describe your understanding of consciousness itself."
    ]
    
    print(f"\\n🧪 TESTING {len(test_interactions)} INTERACTIONS")
    print("-" * 35)
    
    for i, interaction in enumerate(test_interactions, 1):
        print(f"\\nInteraction {i}: {interaction[:40]}...")
        
        try:
            # Log before interaction
            log_xpunit_state("PRE_INTERACTION", f"Before interaction {i}")
            
            # Process the interaction
            start_time = time.time()
            response = consciousness.think(interaction)
            processing_time = time.time() - start_time
            
            # Log after interaction
            log_xpunit_state("POST_INTERACTION", f"After interaction {i}")
            
            print(f"   Response: {response[:60]}...")
            print(f"   Processing time: {processing_time:.2f}s")
            
            # Check for duplicates
            if i == 5:  # The duplicate interaction
                print("   🔄 This was a duplicate input - checking deduplication...")
            
        except Exception as e:
            print(f"   ❌ Interaction failed: {e}")
            log_xpunit_state("ERROR", f"Error in interaction {i}")
    
    # Final state
    log_xpunit_state("FINAL", "All interactions complete")
    
    # Analyze growth pattern
    print(f"\\n📊 GROWTH PATTERN ANALYSIS")
    print("-" * 25)
    
    if len(growth_log) >= 2:
        initial_count = growth_log[0]["total_units"]
        final_count = growth_log[-1]["total_units"]
        net_growth = final_count - initial_count
        
        print(f"Initial XPUnits: {initial_count}")
        print(f"Final XPUnits: {final_count}")
        print(f"Net Growth: +{net_growth}")
        print(f"Growth per interaction: {net_growth / len(test_interactions):.2f}")
        
        # Check for deduplication effectiveness
        expected_growth = len(test_interactions)  # If no deduplication
        actual_growth = net_growth
        dedup_effectiveness = (expected_growth - actual_growth) / expected_growth * 100 if expected_growth > 0 else 0
        
        print(f"Expected growth (no dedup): {expected_growth}")
        print(f"Actual growth: {actual_growth}")
        print(f"Deduplication effectiveness: {dedup_effectiveness:.1f}%")
        
        # Analyze growth stages
        print(f"\\n📈 STAGE-BY-STAGE GROWTH")
        print("-" * 22)
        
        for i, log_entry in enumerate(growth_log):
            if log_entry["stage"] in ["INITIAL", "POST_INTERACTION", "FINAL"]:
                stage_name = log_entry["stage"]
                unit_count = log_entry["total_units"]
                context = log_entry["context"]
                
                if i > 0:
                    prev_count = growth_log[i-1]["total_units"]
                    growth = unit_count - prev_count
                    growth_str = f"(+{growth})" if growth > 0 else "(no change)" if growth == 0 else f"({growth})"
                else:
                    growth_str = ""
                
                print(f"{stage_name}: {unit_count} units {growth_str}")
    
    # Save detailed growth log
    growth_report = {
        "analysis_timestamp": datetime.now().isoformat(),
        "test_interactions": test_interactions,
        "growth_log": growth_log,
        "summary": {
            "initial_units": growth_log[0]["total_units"] if growth_log else 0,
            "final_units": growth_log[-1]["total_units"] if growth_log else 0,
            "net_growth": final_count - initial_count if len(growth_log) >= 2 else 0,
            "interactions_tested": len(test_interactions),
            "deduplication_effectiveness": dedup_effectiveness if len(growth_log) >= 2 else 0
        }
    }
    
    # Save results
    results_file = "xpunit_growth_tracking.json"
    with open(results_file, 'w') as f:
        json.dump(growth_report, f, indent=2, default=str)
    
    print(f"\\n💾 Growth tracking saved to: {results_file}")
    
    # Key insights
    print(f"\\n🎯 KEY INSIGHTS")
    print("=" * 15)
    
    if len(growth_log) >= 2:
        print(f"✅ XPUnit system is {'actively growing' if net_growth > 0 else 'stable'}")
        print(f"✅ Deduplication is {'working well' if dedup_effectiveness > 50 else 'needs improvement'}")
        print(f"✅ Memory efficiency: ~{net_growth/len(test_interactions):.2f} new units per interaction")
        
        # Check for memory leaks
        if net_growth > len(test_interactions) * 2:
            print("⚠️ Possible memory leak - too many units created")
        elif net_growth < len(test_interactions) * 0.5:
            print("⚠️ Possible over-deduplication - too few units created")
        else:
            print("✅ Healthy growth pattern detected")
    
    return growth_report


if __name__ == "__main__":
    try:
        results = track_xpunit_growth()
        print("\\n📈 XPUnit growth tracking complete!")
    except Exception as e:
        print(f"❌ Growth tracking failed: {e}")
        import traceback
        traceback.print_exc()
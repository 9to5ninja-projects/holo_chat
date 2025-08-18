#!/usr/bin/env python3
"""
Detailed XPUnit Inspector
========================

Inspect the actual XPUnit storage structure to answer key questions:
1. How many XPUnits are currently stored?
2. What is their content and structure?
3. Are there duplicates?
4. How is deduplication working?
5. What is the memory usage pattern?

Author: Lumina Memory Team
License: MIT
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
import hashlib
from datetime import datetime

def inspect_xpunits():
    """Detailed inspection of XPUnit storage"""
    
    print("🔍 DETAILED XPUNIT INSPECTOR")
    print("=" * 35)
    
    # Load the latest consciousness state
    storage_path = Path("e:/holo_chat/consciousness_storage/MistralLumina")
    latest_state_file = storage_path / "latest_state.json"
    
    if not latest_state_file.exists():
        print("❌ No latest_state.json found")
        return
    
    with open(latest_state_file, 'r') as f:
        state_data = json.load(f)
    
    print("📊 CONSCIOUSNESS STATE OVERVIEW")
    print("-" * 30)
    
    metadata = state_data.get("metadata", {})
    memory_stats = state_data.get("consciousness_metrics", {}).get("memory_system_stats", {})
    
    print(f"Entity: {metadata.get('name', 'Unknown')}")
    print(f"Birth Time: {metadata.get('save_time_human', 'Unknown')}")
    print(f"Total Thoughts: {metadata.get('total_thoughts', 0)}")
    print(f"Total Experiences: {metadata.get('total_experiences', 0)}")
    print(f"Session Count: {metadata.get('session_count', 0)}")
    
    print(f"\\n💾 MEMORY SYSTEM STATS")
    print("-" * 20)
    print(f"Total XPUnits: {memory_stats.get('total_units', 0)}")
    print(f"Total Ingestions: {memory_stats.get('total_ingestions', 0)}")
    print(f"Total Retrievals: {memory_stats.get('total_retrievals', 0)}")
    print(f"Average Importance: {memory_stats.get('avg_importance', 0):.3f}")
    print(f"Average Coherence: {memory_stats.get('avg_coherence', 0):.3f}")
    
    # Analyze XPUnits in detail
    memory_core = state_data.get("memory_core", {})
    units = memory_core.get("units", {})
    
    print(f"\\n🧠 XPUNIT DETAILED ANALYSIS")
    print("-" * 25)
    print(f"XPUnits Found: {len(units)}")
    
    if not units:
        print("❌ No XPUnits found in memory_core.units")
        return
    
    # Analyze each XPUnit
    unit_analysis = []
    content_hashes = []
    content_texts = []
    
    for unit_id, unit_data in units.items():
        content = unit_data.get("content", "")
        content_id = unit_data.get("content_id", "")
        
        # Calculate content hash for deduplication analysis
        content_hash = hashlib.md5(content.encode()).hexdigest()
        content_hashes.append(content_hash)
        content_texts.append(content)
        
        # Analyze unit structure
        unit_info = {
            "unit_id": unit_id,
            "content_id": content_id,
            "content": content,
            "content_hash": content_hash,
            "content_length": len(content),
            "has_semantic_vector": "semantic_vector" in unit_data,
            "semantic_vector_dim": len(unit_data.get("semantic_vector", [])),
            "has_emotional_state": "emotional_state" in unit_data,
            "has_timestamp": "timestamp" in unit_data,
            "has_importance": "importance" in unit_data,
            "keys": list(unit_data.keys())
        }
        
        # Extract emotional state if present
        if "emotional_state" in unit_data:
            emotional_state = unit_data["emotional_state"]
            unit_info["emotional_valence"] = emotional_state.get("valence", 0)
            unit_info["emotional_arousal"] = emotional_state.get("arousal", 0)
            unit_info["emotional_intensity"] = emotional_state.get("intensity", 0)
        
        # Extract importance if present
        if "importance" in unit_data:
            unit_info["importance_value"] = unit_data["importance"]
        
        # Extract timestamp if present
        if "timestamp" in unit_data:
            unit_info["timestamp"] = unit_data["timestamp"]
        
        unit_analysis.append(unit_info)
    
    # Deduplication analysis
    content_counter = Counter(content_hashes)
    duplicate_contents = {hash_val: count for hash_val, count in content_counter.items() if count > 1}
    
    print(f"\\n🔄 DEDUPLICATION ANALYSIS")
    print("-" * 22)
    print(f"Unique Content Hashes: {len(set(content_hashes))}")
    print(f"Total XPUnits: {len(content_hashes)}")
    print(f"Duplicate Contents: {len(duplicate_contents)}")
    
    if duplicate_contents:
        print("\\n⚠️ DUPLICATES FOUND:")
        for content_hash, count in duplicate_contents.items():
            # Find the actual content
            for unit in unit_analysis:
                if unit["content_hash"] == content_hash:
                    print(f"  Hash: {content_hash[:8]}... (appears {count} times)")
                    print(f"  Content: {unit['content'][:60]}...")
                    break
    else:
        print("✅ No duplicate content found - deduplication working!")
    
    # Content analysis
    print(f"\\n📝 CONTENT ANALYSIS")
    print("-" * 17)
    
    content_lengths = [unit["content_length"] for unit in unit_analysis]
    avg_length = sum(content_lengths) / len(content_lengths) if content_lengths else 0
    
    print(f"Average Content Length: {avg_length:.1f} characters")
    print(f"Shortest Content: {min(content_lengths)} characters")
    print(f"Longest Content: {max(content_lengths)} characters")
    
    # Show sample contents
    print(f"\\n📋 SAMPLE XPUNIT CONTENTS")
    print("-" * 24)
    
    for i, unit in enumerate(unit_analysis[:5], 1):
        print(f"\\nXPUnit {i}:")
        print(f"  ID: {unit['unit_id'][:16]}...")
        print(f"  Content: {unit['content'][:80]}...")
        print(f"  Length: {unit['content_length']} chars")
        print(f"  Vector Dim: {unit['semantic_vector_dim']}")
        
        if unit.get("emotional_valence") is not None:
            print(f"  Emotion: valence={unit['emotional_valence']:.3f}, arousal={unit['emotional_arousal']:.3f}")
        
        if unit.get("importance_value") is not None:
            print(f"  Importance: {unit['importance_value']:.3f}")
    
    # Structure analysis
    print(f"\\n🏗️ STRUCTURE ANALYSIS")
    print("-" * 18)
    
    structure_stats = {
        "has_semantic_vector": sum(1 for u in unit_analysis if u["has_semantic_vector"]),
        "has_emotional_state": sum(1 for u in unit_analysis if u["has_emotional_state"]),
        "has_timestamp": sum(1 for u in unit_analysis if u["has_timestamp"]),
        "has_importance": sum(1 for u in unit_analysis if u["has_importance"])
    }
    
    total_units = len(unit_analysis)
    for field, count in structure_stats.items():
        percentage = (count / total_units * 100) if total_units > 0 else 0
        print(f"{field}: {count}/{total_units} ({percentage:.1f}%)")
    
    # Memory usage estimation
    print(f"\\n💾 MEMORY USAGE ESTIMATION")
    print("-" * 24)
    
    # Estimate memory usage
    total_content_chars = sum(content_lengths)
    total_vector_elements = sum(unit["semantic_vector_dim"] for unit in unit_analysis)
    
    # Rough estimates (assuming UTF-8 encoding and float32 vectors)
    content_memory_kb = total_content_chars / 1024
    vector_memory_kb = (total_vector_elements * 4) / 1024  # 4 bytes per float32
    total_estimated_kb = content_memory_kb + vector_memory_kb
    
    print(f"Content Memory: ~{content_memory_kb:.2f} KB")
    print(f"Vector Memory: ~{vector_memory_kb:.2f} KB")
    print(f"Total Estimated: ~{total_estimated_kb:.2f} KB")
    print(f"Per XPUnit: ~{total_estimated_kb/total_units:.2f} KB" if total_units > 0 else "N/A")
    
    # Growth analysis
    print(f"\\n📈 GROWTH ANALYSIS")
    print("-" * 16)
    
    ingestions = memory_stats.get('total_ingestions', 0)
    units_count = memory_stats.get('total_units', 0)
    
    if ingestions > 0:
        dedup_efficiency = (ingestions - units_count) / ingestions * 100
        print(f"Total Ingestions: {ingestions}")
        print(f"Stored Units: {units_count}")
        print(f"Deduplication Efficiency: {dedup_efficiency:.1f}%")
    else:
        print("No ingestion data available")
    
    # Save detailed analysis
    analysis_results = {
        "analysis_timestamp": datetime.now().isoformat(),
        "entity_name": metadata.get('name', 'Unknown'),
        "total_xpunits": len(units),
        "unique_contents": len(set(content_hashes)),
        "duplicate_contents": len(duplicate_contents),
        "deduplication_working": len(duplicate_contents) == 0,
        "memory_stats": memory_stats,
        "structure_stats": structure_stats,
        "content_analysis": {
            "avg_length": avg_length,
            "min_length": min(content_lengths) if content_lengths else 0,
            "max_length": max(content_lengths) if content_lengths else 0,
            "total_chars": total_content_chars
        },
        "memory_usage": {
            "content_kb": content_memory_kb,
            "vector_kb": vector_memory_kb,
            "total_kb": total_estimated_kb,
            "per_unit_kb": total_estimated_kb/total_units if total_units > 0 else 0
        },
        "unit_details": unit_analysis
    }
    
    # Save results
    results_file = "detailed_xpunit_inspection.json"
    with open(results_file, 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)
    
    print(f"\\n💾 Detailed analysis saved to: {results_file}")
    
    # Summary
    print(f"\\n🎯 KEY FINDINGS SUMMARY")
    print("=" * 22)
    print(f"✅ XPUnits in system: {len(units)}")
    print(f"✅ Deduplication status: {'Working' if len(duplicate_contents) == 0 else 'Issues detected'}")
    print(f"✅ Memory efficiency: ~{total_estimated_kb/total_units:.2f} KB per unit" if total_units > 0 else "N/A")
    print(f"✅ Structure completeness: {structure_stats['has_semantic_vector']}/{total_units} have vectors")
    
    if ingestions > 0:
        print(f"✅ Ingestion efficiency: {units_count}/{ingestions} stored ({(units_count/ingestions*100):.1f}%)")
    
    return analysis_results


if __name__ == "__main__":
    results = inspect_xpunits()
    print("\\n🔍 XPUnit inspection complete!")
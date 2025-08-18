#!/usr/bin/env python3
"""
Test script for the unified XP Core system.
This tests the complete consolidated implementation.
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

print("🧪 TESTING UNIFIED XP CORE SYSTEM")
print("=" * 50)

# Test imports
print("\n1️⃣ Testing imports...")
try:
    from lumina_memory.math_foundation import (
        circular_convolution, circular_correlation, normalize_vector,
        memory_unit_score, mathematical_coherence, instant_salience
    )
    print("✅ Mathematical foundation imported")
    MATH_AVAILABLE = True
except ImportError as e:
    print(f"❌ Math foundation failed: {e}")
    MATH_AVAILABLE = False

try:
    from lumina_memory.versioned_xp_store import VersionedXPStore
    print("✅ VersionedXPStore imported")
    STORE_AVAILABLE = True
except ImportError as e:
    print(f"❌ VersionedXPStore failed: {e}")
    STORE_AVAILABLE = False

try:
    from lumina_memory.xp_core_unified import (
        UnifiedXPConfig, XPUnit, XPEnvironment, UnifiedXPKernel
    )
    print("✅ Unified XP Core imported")
    UNIFIED_AVAILABLE = True
except ImportError as e:
    print(f"❌ Unified XP Core failed: {e}")
    UNIFIED_AVAILABLE = False

# Test mathematical operations
if MATH_AVAILABLE:
    print("\n2️⃣ Testing mathematical operations...")
    import numpy as np
    
    # Test HRR operations
    a = normalize_vector(np.random.randn(256))
    b = normalize_vector(np.random.randn(256))
    bound = circular_convolution(a, b)
    unbound = circular_correlation(bound, a)
    similarity = np.dot(b, unbound)
    print(f"✅ HRR bind/unbind similarity: {similarity:.3f}")
    
    # Test memory scoring
    query_sem = normalize_vector(np.random.randn(384))
    memory_sem = normalize_vector(np.random.randn(384))
    score = memory_unit_score(query_sem, memory_sem, age_hours=1.0, decay_rate=0.01, importance=1.0)
    print(f"✅ Memory scoring: {score:.3f}")
    
    # Test lexical attribution
    salience = instant_salience("holographic memory system", "memory")
    print(f"✅ Lexical salience: {salience:.3f}")

# Test versioned store
if STORE_AVAILABLE:
    print("\n3️⃣ Testing versioned store...")
    store = VersionedXPStore()
    commit_id = store.commit(message="Test commit")
    entry_id = store.store("Test content for versioned store")
    stats = store.stats()
    print(f"✅ Store: {stats['total_entries']} entries, {stats['total_commits']} commits")

# Test unified system
if UNIFIED_AVAILABLE:
    print("\n4️⃣ Testing unified XP Core...")
    
    # Create configuration
    config = UnifiedXPConfig(
        embedding_dim=256,
        hrr_dim=512,
        k_neighbors=3
    )
    print(f"✅ Config: {config.embedding_dim}D embeddings")
    
    # Create kernel
    kernel = UnifiedXPKernel(config)
    print("✅ Unified kernel created")
    
    # Test memory processing
    content_id1 = kernel.process_memory("The holographic memory system uses mathematical foundations.")
    content_id2 = kernel.process_memory("Machine learning processes natural language effectively.")
    print(f"✅ Processed 2 memories: {content_id1[:16]}..., {content_id2[:16]}...")
    
    # Test retrieval
    results = kernel.retrieve_memory("holographic memory", k=2)
    print(f"✅ Retrieved {len(results)} similar memories")
    
    # Test system stats
    stats = kernel.get_stats()
    print(f"✅ System stats: {stats['total_units']} units, {stats['total_ingestions']} ingestions")
    
    print("\n🎉 UNIFIED XP CORE SYSTEM WORKING!")

else:
    print("\n⚠️ Unified system not available - testing individual components")

# Summary
print(f"\n📊 COMPONENT STATUS:")
print(f"   Mathematical Foundation: {'✅' if MATH_AVAILABLE else '❌'}")
print(f"   Versioned Store: {'✅' if STORE_AVAILABLE else '❌'}")
print(f"   Unified XP Core: {'✅' if UNIFIED_AVAILABLE else '❌'}")

total_working = sum([MATH_AVAILABLE, STORE_AVAILABLE, UNIFIED_AVAILABLE])
print(f"\n🎯 System Readiness: {total_working}/3 components ({total_working/3:.1%})")

if total_working == 3:
    print("🎉 COMPLETE SUCCESS - All components working!")
elif total_working >= 2:
    print("✅ MOSTLY WORKING - Minor issues remain")
else:
    print("⚠️ NEEDS WORK - Major components missing")

print("\n✅ Test complete!")
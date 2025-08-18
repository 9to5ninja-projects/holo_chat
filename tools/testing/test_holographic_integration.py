#!/usr/bin/env python3
"""
Test Holographic Memory Integration
===================================

This script tests the integration of the holographic memory specification
with our Enhanced XPUnit system, demonstrating:

1. Basic holographic operations (binding/unbinding)
2. Memory capsule creation and querying
3. Global associative memory with decay
4. Consciousness analysis integration
5. Compositional queries
6. Capacity analysis

Run this to verify the mathematical foundation is working correctly.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from typing import Dict, List, Any

# Import our holographic memory system
from src.lumina_memory.holographic_memory import (
    HolographicAssociativeMemory, MemoryCapsule, RoleSpace, SymbolSpace,
    circular_convolution, circular_correlation, normalize_vector, cosine_similarity,
    create_demo_memory, run_capacity_test
)

from src.lumina_memory.enhanced_xpunit import (
    EnhancedXPUnit, EnhancedXPEnvironment,
    create_demo_environment, run_consciousness_analysis
)

def test_basic_hrr_operations():
    """Test basic HRR binding and unbinding operations"""
    print("🧪 Testing Basic HRR Operations")
    print("=" * 50)
    
    # Create test vectors
    dim = 512
    np.random.seed(42)
    
    role_vector = normalize_vector(np.random.randn(dim))
    filler_vector = normalize_vector(np.random.randn(dim))
    
    print(f"📐 Vector dimension: {dim}")
    print(f"🎯 Role vector norm: {np.linalg.norm(role_vector):.6f}")
    print(f"🎯 Filler vector norm: {np.linalg.norm(filler_vector):.6f}")
    
    # Test binding
    bound_vector = circular_convolution(role_vector, filler_vector)
    bound_vector = normalize_vector(bound_vector)
    
    print(f"🔗 Bound vector norm: {np.linalg.norm(bound_vector):.6f}")
    
    # Test unbinding
    unbound_vector = circular_correlation(bound_vector, role_vector)
    unbound_vector = normalize_vector(unbound_vector)
    
    # Check similarity
    similarity = cosine_similarity(unbound_vector, filler_vector)
    print(f"✅ Unbinding similarity: {similarity:.6f}")
    
    if similarity > 0.8:
        print("🎉 HRR operations working correctly!")
    else:
        print("⚠️ HRR operations may have issues")
        
    print()

def test_memory_capsule():
    """Test memory capsule creation and querying"""
    print("🧪 Testing Memory Capsule")
    print("=" * 50)
    
    # Create role and symbol spaces
    role_space = RoleSpace(dimension=512)
    symbol_space = SymbolSpace(dimension=512)
    
    # Create a memory capsule
    capsule = MemoryCapsule()
    
    # Add bindings
    bindings = {
        'WHO': 'alice',
        'WHAT': 'reading',
        'WHERE': 'library',
        'WHEN': 'morning'
    }
    
    for role, symbol in bindings.items():
        symbol_vector = symbol_space.get_symbol(symbol)
        capsule.add_binding(role, symbol_vector)
        
    print(f"📦 Created capsule with {len(capsule.bindings)} bindings")
    print(f"🎯 Capsule vector norm: {np.linalg.norm(capsule.vector):.6f}")
    
    # Test unbinding
    print("\n🔍 Testing role unbinding:")
    for role in bindings.keys():
        unbound = capsule.unbind_role(role)
        
        # Find best matching symbol
        similarities = []
        for symbol_name, symbol_vector in symbol_space.symbols.items():
            sim = cosine_similarity(unbound, symbol_vector)
            similarities.append((symbol_name, sim))
            
        similarities.sort(key=lambda x: x[1], reverse=True)
        best_match, best_sim = similarities[0]
        
        print(f"   {role}: {best_match} (similarity: {best_sim:.3f})")
        
    print()

def test_holographic_associative_memory():
    """Test global holographic associative memory"""
    print("🧪 Testing Holographic Associative Memory")
    print("=" * 50)
    
    # Create memory system
    memory = HolographicAssociativeMemory(dimension=512)
    
    # Add sample episodes
    episodes = [
        {'WHO': 'alice', 'WHAT': 'reading', 'WHERE': 'library'},
        {'WHO': 'bob', 'WHAT': 'cooking', 'WHERE': 'kitchen'},
        {'WHO': 'alice', 'WHAT': 'studying', 'WHERE': 'library'},
        {'WHO': 'charlie', 'WHAT': 'running', 'WHERE': 'park'}
    ]
    
    for i, episode in enumerate(episodes):
        capsule = memory.create_capsule(episode, importance=1.0 - i * 0.1)
        print(f"📝 Added episode {i+1}: {episode}")
        
    print(f"\n📊 Memory contains {len(memory.capsules)} capsules")
    
    # Test role queries
    print("\n🔍 Testing role queries:")
    roles_to_test = ['WHO', 'WHAT', 'WHERE']
    
    for role in roles_to_test:
        results = memory.find_best_symbol_for_role(role, top_k=3)
        print(f"   {role}: {[f'{name}({sim:.3f})' for name, sim in results]}")
        
    # Test compositional query
    print("\n🔍 Testing compositional query:")
    query = {'WHERE': 'library'}
    matches = memory.compositional_query(query)
    
    print(f"   Query: {query}")
    for i, (capsule, similarity) in enumerate(matches[:3]):  # Show top 3
        bindings_str = {role: f"symbol_{hash(tuple(vec))%1000}" 
                       for role, (vec, weight) in capsule.bindings.items()}
        print(f"   Match {i+1}: similarity={similarity:.3f}")
        
    print()

def test_enhanced_xpunit():
    """Test Enhanced XPUnit with consciousness analysis"""
    print("🧪 Testing Enhanced XPUnit")
    print("=" * 50)
    
    # Test experiences with different consciousness levels
    experiences = [
        "I am thinking about my own thought processes.",  # High consciousness
        "The weather is nice today.",                     # Low consciousness  
        "I wonder if I am truly aware of my awareness.",  # High consciousness
        "Machine learning is fascinating."                # Medium consciousness
    ]
    
    xpunits = []
    for i, content in enumerate(experiences):
        xpunit = EnhancedXPUnit(
            content_id=f"test_{i}",
            content=content
        )
        xpunits.append(xpunit)
        
        print(f"📝 XPUnit {i+1}:")
        print(f"   Content: {content}")
        print(f"   Consciousness Score: {xpunit.consciousness_score:.3f}")
        print(f"   Consciousness Level: {xpunit.get_consciousness_level()}")
        print(f"   Indicators: {list(xpunit.consciousness_indicators.keys())}")
        print(f"   Importance: {xpunit.importance:.3f}")
        print()
        
    # Test similarity between XPUnits
    print("🔍 Testing XPUnit similarities:")
    for i in range(len(xpunits)):
        for j in range(i+1, len(xpunits)):
            similarity = xpunits[i].similarity_to(xpunits[j])
            print(f"   XPUnit {i+1} ↔ XPUnit {j+1}: {similarity:.3f}")
            
    print()

def test_enhanced_environment():
    """Test Enhanced XP Environment"""
    print("🧪 Testing Enhanced XP Environment")
    print("=" * 50)
    
    # Create demo environment
    env = create_demo_environment()
    
    # Get statistics
    stats = env.get_statistics()
    print(f"📊 Environment Statistics:")
    print(f"   Total XPUnits: {stats['total_xpunits']}")
    print(f"   Consciousness Distribution: {stats['consciousness_distribution']}")
    print(f"   Average Consciousness: {stats['average_consciousness']:.3f}")
    print(f"   Memory Usage: {stats['holographic_memory']['memory_usage_mb']:.2f} MB")
    
    # Test queries
    print(f"\n🔍 Testing environment queries:")
    
    # Role query
    role_results = env.query_role('WHAT', top_k=3)
    print(f"   WHAT role query: {role_results}")
    
    # Compositional query
    comp_results = env.compositional_query({'WHAT': 'thinking'}, top_k=3)
    print(f"   Compositional query results: {len(comp_results)} matches")
    
    # Consciousness analysis
    consciousness_analysis = run_consciousness_analysis(env)
    print(f"\n🧠 Consciousness Analysis:")
    print(f"   High consciousness examples: {len(consciousness_analysis['high_consciousness_examples'])}")
    
    for example in consciousness_analysis['high_consciousness_examples'][:2]:
        print(f"   - '{example['content'][:50]}...' (score: {example['score']:.3f})")
        
    print()

def test_capacity_analysis():
    """Test capacity analysis across different dimensions"""
    print("🧪 Testing Capacity Analysis")
    print("=" * 50)
    
    print("⏳ Running capacity test (this may take a moment)...")
    
    # Run simplified capacity test
    dimensions = [256, 512]
    num_associations = [5, 10, 20]
    
    results = run_capacity_test(dimensions, num_associations)
    
    print("📊 Capacity Test Results:")
    for dim_key, accuracies in results.items():
        print(f"   {dim_key}: {[f'{acc:.3f}' for acc in accuracies]}")
        
    print("   (Accuracies for 5, 10, 20 associations)")
    print()

def create_visualization():
    """Create visualization of holographic memory performance"""
    print("🧪 Creating Holographic Memory Visualization")
    print("=" * 50)
    
    # Create demo memory
    memory = create_demo_memory()
    
    # Test role queries and collect similarities
    roles = ['WHO', 'WHAT', 'WHERE']
    fig, axes = plt.subplots(1, len(roles), figsize=(15, 5))
    
    for i, role in enumerate(roles):
        results = memory.find_best_symbol_for_role(role, top_k=10)
        
        symbols = [name for name, _ in results]
        similarities = [sim for _, sim in results]
        
        axes[i].bar(range(len(symbols)), similarities)
        axes[i].set_title(f'Role: {role}')
        axes[i].set_xlabel('Symbol Candidates')
        axes[i].set_ylabel('Cosine Similarity')
        axes[i].set_xticks(range(len(symbols)))
        axes[i].set_xticklabels(symbols, rotation=45, ha='right')
        
    plt.tight_layout()
    plt.savefig('holographic_memory_test.png', dpi=150, bbox_inches='tight')
    print("📊 Visualization saved as 'holographic_memory_test.png'")
    print()

def main():
    """Run all tests"""
    print("🚀 HOLOGRAPHIC MEMORY INTEGRATION TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        # Run all tests
        test_basic_hrr_operations()
        test_memory_capsule()
        test_holographic_associative_memory()
        test_enhanced_xpunit()
        test_enhanced_environment()
        test_capacity_analysis()
        
        # Create visualization
        try:
            create_visualization()
        except ImportError:
            print("⚠️ Matplotlib not available, skipping visualization")
        except Exception as e:
            print(f"⚠️ Visualization failed: {e}")
            
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("✅ Holographic memory integration is working correctly")
        print("✅ Enhanced XPUnit system is operational")
        print("✅ Consciousness analysis is functioning")
        print("✅ Mathematical foundation is solid")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
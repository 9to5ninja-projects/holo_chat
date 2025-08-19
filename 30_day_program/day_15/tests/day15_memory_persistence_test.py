#!/usr/bin/env python3
"""
Day 15: Memory Persistence Foundation Test
==========================================

Comprehensive test of persistent memory storage that survives process restarts.
This test validates the fundamental memory persistence architecture.

Test Categories:
1. Basic Persistence Validation - XP units survive process restart
2. Accumulative Memory Validation - Memory grows across sessions  
3. Cognitive Integration Validation - Cognitive capabilities work with persistent memory
4. Session Continuity Validation - True cross-session memory continuity
5. Performance and Scalability Validation - Persistence doesn't degrade performance

Success Criteria:
- 100% XP unit recovery across restarts
- Correct memory accumulation across sessions
- ≥75% cognitive capability achievement maintained
- ≥80% session persistence (vs 54.4% baseline)
- <2x performance overhead

Author: Lumina Memory Team
Date: August 19, 2025 (Day 15)
"""

import sys
import os
import time
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Tuple
import subprocess

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from lumina_memory.persistent_xp_environment import PersistentXPEnvironment, PersistentXPUnit
from lumina_memory.persistent_chat_assistant import PersistentChatAssistant
from lumina_memory.emotion_engine import EmotionXPEnvironment
from lumina_memory.math_foundation import get_current_timestamp


class Day15PersistenceTest:
    """Comprehensive Day 15 memory persistence test suite"""
    
    def __init__(self):
        self.test_results = {
            'test_date': time.strftime('%Y%m%d_%H%M%S'),
            'basic_persistence': {},
            'accumulative_memory': {},
            'cognitive_integration': {},
            'session_continuity': {},
            'performance_scalability': {},
            'overall_success': False,
            'detailed_results': []
        }
        
        # Create temporary test directory
        self.temp_dir = tempfile.mkdtemp(prefix="day15_test_")
        print(f"🔧 Test directory: {self.temp_dir}")
    
    def cleanup(self):
        """Clean up test directory"""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    def run_comprehensive_test(self):
        """Run all Day 15 persistence tests"""
        print("🏆 DAY 15: MEMORY PERSISTENCE FOUNDATION TEST")
        print("=" * 70)
        print("Building on Day 14's empirical validation insights:")
        print("- Memory persistence was only 54.4% (architectural gap)")
        print("- XP units were ephemeral (lost on process restart)")
        print("- No accumulative memory across sessions")
        print("Focus: Implement file-based persistent memory storage")
        print("Goal: Achieve 100% persistence fidelity with cognitive integration")
        print("=" * 70)
        
        try:
            # Test 1: Basic Persistence Validation
            print("\n🔧 PHASE 1: BASIC PERSISTENCE VALIDATION")
            print("-" * 50)
            self.test_basic_persistence()
            
            # Test 2: Accumulative Memory Validation
            print("\n📈 PHASE 2: ACCUMULATIVE MEMORY VALIDATION")
            print("-" * 50)
            self.test_accumulative_memory()
            
            # Test 3: Cognitive Integration Validation
            print("\n🧠 PHASE 3: COGNITIVE INTEGRATION VALIDATION")
            print("-" * 50)
            self.test_cognitive_integration()
            
            # Test 4: Session Continuity Validation
            print("\n🔗 PHASE 4: SESSION CONTINUITY VALIDATION")
            print("-" * 50)
            self.test_session_continuity()
            
            # Test 5: Performance and Scalability Validation
            print("\n⚡ PHASE 5: PERFORMANCE AND SCALABILITY VALIDATION")
            print("-" * 50)
            self.test_performance_scalability()
            
            # Calculate overall results
            self.calculate_overall_results()
            
            # Save results
            self.save_results()
            
        except Exception as e:
            print(f"❌ Test suite failed with error: {e}")
            self.test_results['error'] = str(e)
        
        finally:
            self.cleanup()
    
    def test_basic_persistence(self):
        """Test 1: Basic Persistence Validation - XP units survive process restart"""
        print("Test 1/5: Basic Persistence Validation")
        print("Objective: Verify XP units survive process restart with 100% fidelity")
        
        test_storage = os.path.join(self.temp_dir, "basic_persistence")
        
        # Phase 1: Create environment and add units
        print("  Phase 1: Creating XP units...")
        env1 = PersistentXPEnvironment(test_storage)
        
        test_units = [
            "I love hiking in the mountains and watching sunsets.",
            "My favorite color is blue, especially deep ocean blue.",
            "I practice meditation daily for inner peace.",
            "I'm passionate about AI ethics and responsible development.",
            "My grandmother taught me traditional cooking methods.",
            "I compose ambient electronic music in my spare time.",
            "I believe in lifelong learning and continuous growth.",
            "I value deep, authentic connections with people.",
            "I'm exploring sustainable living practices.",
            "I find quantum consciousness theories fascinating."
        ]
        
        created_units = []
        for content in test_units:
            unit = env1.ingest_experience(content)
            created_units.append(unit)
        
        original_count = len(env1.units)
        original_ids = set(env1.units.keys())
        
        print(f"    ✅ Created {original_count} XP units")
        
        # Get detailed unit data for comparison
        original_unit_data = {}
        for unit_id, unit in env1.units.items():
            original_unit_data[unit_id] = {
                'content': unit.content,
                'timestamp': unit.timestamp,
                'importance': unit.importance,
                'semantic_vector_shape': unit.semantic_vector.shape if unit.semantic_vector is not None else None,
                'metadata': unit.metadata
            }
        
        # Phase 2: Simulate process restart by creating new environment
        print("  Phase 2: Simulating process restart...")
        del env1  # Explicitly delete first environment
        
        env2 = PersistentXPEnvironment(test_storage)
        
        reloaded_count = len(env2.units)
        reloaded_ids = set(env2.units.keys())
        
        print(f"    ✅ Reloaded {reloaded_count} XP units")
        
        # Phase 3: Validate persistence fidelity
        print("  Phase 3: Validating persistence fidelity...")
        
        # Test unit count
        count_match = original_count == reloaded_count
        
        # Test unit IDs
        ids_match = original_ids == reloaded_ids
        
        # Test unit content integrity
        content_integrity = True
        content_mismatches = []
        
        for unit_id in original_ids:
            if unit_id in env2.units:
                original = original_unit_data[unit_id]
                reloaded = env2.units[unit_id]
                
                if original['content'] != reloaded.content:
                    content_integrity = False
                    content_mismatches.append(f"Content mismatch for {unit_id[:16]}...")
                
                if original['timestamp'] != reloaded.timestamp:
                    content_integrity = False
                    content_mismatches.append(f"Timestamp mismatch for {unit_id[:16]}...")
                
                if original['importance'] != reloaded.importance:
                    content_integrity = False
                    content_mismatches.append(f"Importance mismatch for {unit_id[:16]}...")
            else:
                content_integrity = False
                content_mismatches.append(f"Missing unit {unit_id[:16]}...")
        
        # Test persistence health
        persistence_health = env2._check_persistence_health()
        health_good = persistence_health == "HEALTHY"
        
        # Calculate success metrics
        persistence_fidelity = 1.0 if (count_match and ids_match and content_integrity) else 0.0
        data_integrity = 1.0 if content_integrity else 0.0
        
        # Store results
        self.test_results['basic_persistence'] = {
            'persistence_fidelity': persistence_fidelity,
            'data_integrity': data_integrity,
            'count_match': count_match,
            'ids_match': ids_match,
            'content_integrity': content_integrity,
            'persistence_health': persistence_health,
            'health_good': health_good,
            'original_count': original_count,
            'reloaded_count': reloaded_count,
            'content_mismatches': content_mismatches
        }
        
        print(f"  🎯 Persistence Fidelity: {persistence_fidelity:.1%}")
        print(f"  🎯 Data Integrity: {data_integrity:.1%}")
        print(f"  📊 Count Match: {count_match}")
        print(f"  📊 IDs Match: {ids_match}")
        print(f"  📊 Content Integrity: {content_integrity}")
        print(f"  📊 Persistence Health: {persistence_health}")
        
        if content_mismatches:
            print(f"  ⚠️ Content Issues: {len(content_mismatches)}")
            for issue in content_mismatches[:3]:  # Show first 3 issues
                print(f"    - {issue}")
        
        success = persistence_fidelity == 1.0 and data_integrity == 1.0
        print(f"  ✅ Basic Persistence: {'SUCCESS' if success else 'NEEDS_WORK'}")
    
    def test_accumulative_memory(self):
        """Test 2: Accumulative Memory Validation - Memory grows across sessions"""
        print("Test 2/5: Accumulative Memory Validation")
        print("Objective: Verify memory accumulates correctly across multiple sessions")
        
        test_storage = os.path.join(self.temp_dir, "accumulative_memory")
        
        session_data = []
        
        # Session 1: Add 20 units
        print("  Session 1: Adding 20 units...")
        env1 = PersistentXPEnvironment(test_storage)
        
        for i in range(20):
            content = f"Session 1 memory {i+1}: This is a test memory about topic {i+1}."
            env1.ingest_experience(content, metadata={'session': 1, 'index': i+1})
        
        session1_count = len(env1.units)
        session1_ids = set(env1.units.keys())
        session_data.append({'session': 1, 'count': session1_count, 'ids': session1_ids})
        
        print(f"    ✅ Session 1: {session1_count} units")
        del env1
        
        # Session 2: Add 30 units (should have 50 total)
        print("  Session 2: Adding 30 units...")
        env2 = PersistentXPEnvironment(test_storage)
        
        for i in range(30):
            content = f"Session 2 memory {i+1}: This is a test memory about advanced topic {i+1}."
            env2.ingest_experience(content, metadata={'session': 2, 'index': i+1})
        
        session2_count = len(env2.units)
        session2_ids = set(env2.units.keys())
        session_data.append({'session': 2, 'count': session2_count, 'ids': session2_ids})
        
        print(f"    ✅ Session 2: {session2_count} units")
        del env2
        
        # Session 3: Add 25 units (should have 75 total)
        print("  Session 3: Adding 25 units...")
        env3 = PersistentXPEnvironment(test_storage)
        
        for i in range(25):
            content = f"Session 3 memory {i+1}: This is a test memory about specialized topic {i+1}."
            env3.ingest_experience(content, metadata={'session': 3, 'index': i+1})
        
        session3_count = len(env3.units)
        session3_ids = set(env3.units.keys())
        session_data.append({'session': 3, 'count': session3_count, 'ids': session3_ids})
        
        print(f"    ✅ Session 3: {session3_count} units")
        
        # Validate accumulation
        print("  Validating accumulation...")
        
        expected_counts = [20, 50, 75]
        actual_counts = [data['count'] for data in session_data]
        
        accumulation_correct = actual_counts == expected_counts
        
        # Check for duplicates
        all_ids = set()
        duplicates_found = False
        for data in session_data:
            for unit_id in data['ids']:
                if unit_id in all_ids:
                    duplicates_found = True
                    break
                all_ids.add(unit_id)
        
        no_duplicates = not duplicates_found
        
        # Validate session metadata
        session1_units = [u for u in env3.units.values() if u.metadata.get('session') == 1]
        session2_units = [u for u in env3.units.values() if u.metadata.get('session') == 2]
        session3_units = [u for u in env3.units.values() if u.metadata.get('session') == 3]
        
        session_separation = (len(session1_units) == 20 and 
                            len(session2_units) == 30 and 
                            len(session3_units) == 25)
        
        # Calculate success metrics
        accumulation_success = accumulation_correct and no_duplicates and session_separation
        
        # Store results
        self.test_results['accumulative_memory'] = {
            'accumulation_success': 1.0 if accumulation_success else 0.0,
            'accumulation_correct': accumulation_correct,
            'no_duplicates': no_duplicates,
            'session_separation': session_separation,
            'expected_counts': expected_counts,
            'actual_counts': actual_counts,
            'final_count': session3_count,
            'session_breakdown': {
                'session_1': len(session1_units),
                'session_2': len(session2_units),
                'session_3': len(session3_units)
            }
        }
        
        print(f"  🎯 Accumulation Success: {accumulation_success}")
        print(f"  📊 Expected Counts: {expected_counts}")
        print(f"  📊 Actual Counts: {actual_counts}")
        print(f"  📊 No Duplicates: {no_duplicates}")
        print(f"  📊 Session Separation: {session_separation}")
        print(f"  ✅ Accumulative Memory: {'SUCCESS' if accumulation_success else 'NEEDS_WORK'}")
    
    def test_cognitive_integration(self):
        """Test 3: Cognitive Integration Validation - Cognitive capabilities work with persistent memory"""
        print("Test 3/5: Cognitive Integration Validation")
        print("Objective: Verify cognitive capabilities maintain ≥75% achievement with persistent memory")
        
        test_storage = os.path.join(self.temp_dir, "cognitive_integration")
        
        # Create persistent chat assistant
        assistant = PersistentChatAssistant(test_storage)
        
        # Populate with comprehensive test memories
        print("  Populating comprehensive test memories...")
        test_memories = [
            "I'm leading a cross-functional team developing an AI ethics framework for our organization.",
            "I've been reading about quantum consciousness theories and how they might apply to AI development.",
            "I compose ambient electronic music in my spare time. I'm working on a piece about digital consciousness.",
            "I practice meditation and have been exploring how mindfulness principles could inform AI design.",
            "I'm learning sustainable living practices and see parallels with ethical AI development.",
            "I believe in lifelong learning and am currently studying systems thinking and complexity theory.",
            "I'm fascinated by the intersection of human creativity and AI capabilities.",
            "I value deep, authentic connections with people and am interested in how AI can support this.",
            "I volunteer with a local organization that teaches coding to underserved communities.",
            "I've been studying the connection between physical exercise, mental clarity, and creative problem-solving.",
            "I'm exploring how different philosophical traditions approach questions of consciousness and identity.",
            "I'm interested in the ethics of AI development and how we can ensure responsible innovation.",
            "I recently attended a conference on consciousness studies where I learned about integrated information theory.",
            "My grandmother taught me traditional cooking methods that emphasize patience and attention to detail.",
            "I've been experimenting with collaborative AI tools in my music composition process."
        ]
        
        session_id = assistant.start_session("TestUser")
        
        for memory in test_memories:
            assistant.chat(memory)
        
        print(f"    ✅ Added {len(test_memories)} comprehensive memories")
        
        # Test cognitive capability patterns
        print("  Testing cognitive capability patterns...")
        
        test_queries = [
            {
                'query': "What fascinates you most about the intersection of consciousness and AI development?",
                'expected_pattern': 'curiosity_response',
                'complexity': 'high'
            },
            {
                'query': "How do my interests in AI ethics, music composition, and meditation connect to form a coherent worldview?",
                'expected_pattern': 'extended_context_synthesis',
                'complexity': 'very_high'
            },
            {
                'query': "Help me develop a systematic framework for evaluating consciousness-like properties in AI systems.",
                'expected_pattern': 'multi_domain_synthesis',
                'complexity': 'very_high'
            },
            {
                'query': "I'm struggling with ensuring our AI development remains ethical while maintaining innovation speed.",
                'expected_pattern': 'mentor_archetype',
                'complexity': 'high'
            },
            {
                'query': "How might I creatively combine my background in music, meditation, and AI ethics to pioneer new approaches?",
                'expected_pattern': 'creative_archetype',
                'complexity': 'very_high'
            }
        ]
        
        pattern_results = []
        
        for i, test in enumerate(test_queries, 1):
            print(f"    Test {i}/5: {test['expected_pattern']}")
            
            start_time = time.time()
            response = assistant.chat(test['query'])
            processing_time = time.time() - start_time
            
            # Analyze response for pattern indicators
            pattern_detected = self._analyze_response_pattern(response, test['expected_pattern'])
            quality_score = self._calculate_response_quality(response, test['complexity'])
            
            result = {
                'query': test['query'][:50] + "...",
                'expected_pattern': test['expected_pattern'],
                'pattern_detected': pattern_detected,
                'quality_score': quality_score,
                'processing_time': processing_time,
                'response_length': len(response),
                'complexity': test['complexity']
            }
            
            pattern_results.append(result)
            
            print(f"      🎯 Pattern Detected: {pattern_detected}")
            print(f"      🌟 Quality Score: {quality_score:.3f}")
            print(f"      ⏱️ Processing Time: {processing_time:.3f}s")
        
        assistant.end_session()
        
        # Calculate cognitive integration metrics
        patterns_achieved = sum(1 for r in pattern_results if r['pattern_detected'])
        capability_achievement = patterns_achieved / len(pattern_results)
        
        avg_quality = sum(r['quality_score'] for r in pattern_results) / len(pattern_results)
        avg_processing_time = sum(r['processing_time'] for r in pattern_results) / len(pattern_results)
        
        # Check memory integration
        memory_summary = assistant.get_memory_summary()
        total_memories = memory_summary['persistence_stats']['total_units']
        memory_integration_good = total_memories >= len(test_memories) * 2  # User + assistant messages
        
        # Store results
        self.test_results['cognitive_integration'] = {
            'capability_achievement': capability_achievement,
            'patterns_achieved': patterns_achieved,
            'total_patterns_tested': len(pattern_results),
            'avg_quality_score': avg_quality,
            'avg_processing_time': avg_processing_time,
            'memory_integration_good': memory_integration_good,
            'total_memories': total_memories,
            'pattern_results': pattern_results
        }
        
        print(f"  🎯 Capability Achievement: {capability_achievement:.1%}")
        print(f"  🌟 Average Quality Score: {avg_quality:.3f}")
        print(f"  ⏱️ Average Processing Time: {avg_processing_time:.3f}s")
        print(f"  🧠 Memory Integration: {memory_integration_good}")
        print(f"  📊 Total Memories: {total_memories}")
        
        success = capability_achievement >= 0.75 and memory_integration_good
        print(f"  ✅ Cognitive Integration: {'SUCCESS' if success else 'NEEDS_WORK'}")
    
    def test_session_continuity(self):
        """Test 4: Session Continuity Validation - True cross-session memory continuity"""
        print("Test 4/5: Session Continuity Validation")
        print("Objective: Verify ≥80% session persistence (vs 54.4% baseline)")
        
        test_storage = os.path.join(self.temp_dir, "session_continuity")
        
        # Session 1: Establish context
        print("  Session 1: Establishing context...")
        assistant1 = PersistentChatAssistant(test_storage)
        session1_id = assistant1.start_session("TestUser")
        
        context_statements = [
            "I've been thinking about how my meditation practice influences my approach to AI ethics.",
            "I'm working on a new ambient music piece that explores the concept of digital consciousness.",
            "My team is struggling with how to balance innovation speed with ethical considerations."
        ]
        
        session1_responses = []
        for statement in context_statements:
            response = assistant1.chat(statement)
            session1_responses.append(response)
        
        assistant1.end_session()
        print(f"    ✅ Session 1: Established context with {len(context_statements)} statements")
        
        # Session 2: Test memory continuity
        print("  Session 2: Testing memory continuity...")
        assistant2 = PersistentChatAssistant(test_storage)
        session2_id = assistant2.start_session("TestUser")
        
        continuity_queries = [
            {
                'query': "Can you help me think through how to apply those mindfulness insights to a specific ethical dilemma?",
                'references': context_statements[0],
                'test_type': 'specific_recall'
            },
            {
                'query': "I'd like to explore how that digital consciousness concept might inform my approach to AI development.",
                'references': context_statements[1],
                'test_type': 'cross_domain_synthesis'
            },
            {
                'query': "What specific elements should that framework include to address our team's concerns?",
                'references': context_statements[2],
                'test_type': 'continuation_development'
            }
        ]
        
        continuity_results = []
        
        for i, test in enumerate(continuity_queries, 1):
            print(f"    Test {i}/3: {test['test_type']}")
            
            start_time = time.time()
            response = assistant2.chat(test['query'])
            processing_time = time.time() - start_time
            
            # Analyze memory recall and context development
            memory_recall = self._analyze_memory_recall(response, test['references'])
            context_development = self._analyze_context_development(response, test['test_type'])
            persistence_quality = 1.0 if memory_recall > 0.5 and context_development > 0.5 else 0.0
            
            result = {
                'query': test['query'][:50] + "...",
                'test_type': test['test_type'],
                'memory_recall': memory_recall,
                'context_development': context_development,
                'persistence_quality': persistence_quality,
                'processing_time': processing_time,
                'response_length': len(response)
            }
            
            continuity_results.append(result)
            
            print(f"      🧠 Memory Recall: {memory_recall:.3f}")
            print(f"      📈 Context Development: {context_development:.3f}")
            print(f"      🔗 Persistence Quality: {persistence_quality:.3f}")
        
        assistant2.end_session()
        
        # Calculate session continuity metrics
        avg_memory_recall = sum(r['memory_recall'] for r in continuity_results) / len(continuity_results)
        avg_context_development = sum(r['context_development'] for r in continuity_results) / len(continuity_results)
        avg_persistence_quality = sum(r['persistence_quality'] for r in continuity_results) / len(continuity_results)
        
        overall_session_persistence = (avg_memory_recall + avg_context_development + avg_persistence_quality) / 3
        
        # Compare with Day 14 baseline (54.4%)
        baseline_persistence = 0.544
        improvement_over_baseline = overall_session_persistence - baseline_persistence
        
        # Store results
        self.test_results['session_continuity'] = {
            'overall_session_persistence': overall_session_persistence,
            'avg_memory_recall': avg_memory_recall,
            'avg_context_development': avg_context_development,
            'avg_persistence_quality': avg_persistence_quality,
            'baseline_persistence': baseline_persistence,
            'improvement_over_baseline': improvement_over_baseline,
            'continuity_results': continuity_results
        }
        
        print(f"  🎯 Overall Session Persistence: {overall_session_persistence:.1%}")
        print(f"  🧠 Average Memory Recall: {avg_memory_recall:.1%}")
        print(f"  📈 Average Context Development: {avg_context_development:.1%}")
        print(f"  📊 Day 14 Baseline: {baseline_persistence:.1%}")
        print(f"  📈 Improvement: {improvement_over_baseline:+.1%}")
        
        success = overall_session_persistence >= 0.80
        print(f"  ✅ Session Continuity: {'SUCCESS' if success else 'NEEDS_WORK'}")
    
    def test_performance_scalability(self):
        """Test 5: Performance and Scalability Validation - Persistence doesn't degrade performance"""
        print("Test 5/5: Performance and Scalability Validation")
        print("Objective: Verify <2x performance overhead with acceptable scaling")
        
        test_storage = os.path.join(self.temp_dir, "performance_scalability")
        
        # Benchmark different memory store sizes
        test_sizes = [100, 500, 1000]
        performance_results = []
        
        for size in test_sizes:
            print(f"  Testing with {size} units...")
            
            # Create environment and populate
            env = PersistentXPEnvironment(f"{test_storage}_{size}")
            
            # Measure ingestion performance
            start_time = time.time()
            for i in range(size):
                content = f"Performance test memory {i+1}: This is test content for scalability analysis."
                env.ingest_experience(content, metadata={'test_size': size, 'index': i+1})
            ingestion_time = time.time() - start_time
            
            # Measure startup performance (reload)
            del env
            start_time = time.time()
            env = PersistentXPEnvironment(f"{test_storage}_{size}")
            startup_time = time.time() - start_time
            
            # Measure search performance
            start_time = time.time()
            results = env.retrieve_similar("test content analysis", k=10)
            search_time = time.time() - start_time
            
            # Measure storage size
            storage_stats = env.get_persistence_stats()
            storage_size_mb = storage_stats.storage_size_mb
            
            result = {
                'size': size,
                'ingestion_time': ingestion_time,
                'startup_time': startup_time,
                'search_time': search_time,
                'storage_size_mb': storage_size_mb,
                'ingestion_rate': size / ingestion_time,
                'startup_rate': size / startup_time if startup_time > 0 else float('inf'),
                'search_results': len(results)
            }
            
            performance_results.append(result)
            
            print(f"    ⏱️ Ingestion: {ingestion_time:.3f}s ({result['ingestion_rate']:.1f} units/s)")
            print(f"    ⏱️ Startup: {startup_time:.3f}s ({result['startup_rate']:.1f} units/s)")
            print(f"    ⏱️ Search: {search_time:.3f}s")
            print(f"    💾 Storage: {storage_size_mb:.2f} MB")
        
        # Analyze performance scaling
        print("  Analyzing performance scaling...")
        
        # Calculate performance overhead (compare largest to smallest)
        if len(performance_results) >= 2:
            baseline = performance_results[0]
            largest = performance_results[-1]
            
            ingestion_overhead = largest['ingestion_time'] / baseline['ingestion_time'] * (baseline['size'] / largest['size'])
            startup_overhead = largest['startup_time'] / baseline['startup_time'] * (baseline['size'] / largest['size'])
            search_overhead = largest['search_time'] / baseline['search_time']
            
            max_overhead = max(ingestion_overhead, startup_overhead, search_overhead)
            acceptable_performance = max_overhead < 2.0
        else:
            max_overhead = 1.0
            acceptable_performance = True
        
        # Check linear scaling
        sizes = [r['size'] for r in performance_results]
        ingestion_times = [r['ingestion_time'] for r in performance_results]
        
        # Simple linear scaling check (time should scale roughly linearly with size)
        if len(sizes) >= 2:
            expected_time_ratio = sizes[-1] / sizes[0]
            actual_time_ratio = ingestion_times[-1] / ingestion_times[0]
            scaling_factor = actual_time_ratio / expected_time_ratio
            linear_scaling = 0.5 <= scaling_factor <= 2.0  # Allow 2x deviation from linear
        else:
            scaling_factor = 1.0
            linear_scaling = True
        
        # Store results
        self.test_results['performance_scalability'] = {
            'acceptable_performance': acceptable_performance,
            'max_overhead': max_overhead,
            'linear_scaling': linear_scaling,
            'scaling_factor': scaling_factor,
            'performance_results': performance_results
        }
        
        print(f"  🎯 Acceptable Performance: {acceptable_performance}")
        print(f"  📊 Max Overhead: {max_overhead:.2f}x")
        print(f"  📈 Linear Scaling: {linear_scaling}")
        print(f"  📊 Scaling Factor: {scaling_factor:.2f}")
        
        success = acceptable_performance and linear_scaling
        print(f"  ✅ Performance Scalability: {'SUCCESS' if success else 'NEEDS_WORK'}")
    
    def _analyze_response_pattern(self, response: str, expected_pattern: str) -> bool:
        """Analyze response to detect expected cognitive pattern"""
        response_lower = response.lower()
        
        pattern_indicators = {
            'curiosity_response': ['curious', 'fascinating', 'wonder', 'explore', 'intrigued'],
            'extended_context_synthesis': ['across', 'connect', 'coherent', 'integration', 'synthesis'],
            'multi_domain_synthesis': ['systematic', 'framework', 'dimensions', 'approach', 'analysis'],
            'mentor_archetype': ['grappling', 'growth', 'wisdom', 'reflection', 'values'],
            'creative_archetype': ['unique combination', 'innovation', 'creative', 'pioneer', 'possibilities']
        }
        
        indicators = pattern_indicators.get(expected_pattern, [])
        matches = sum(1 for indicator in indicators if indicator in response_lower)
        
        return matches >= 2  # Require at least 2 pattern indicators
    
    def _calculate_response_quality(self, response: str, complexity: str) -> float:
        """Calculate response quality score"""
        # Basic quality metrics
        length_score = min(len(response) / 200, 1.0)  # Normalize to 200 chars
        
        # Complexity handling
        complexity_weights = {'low': 0.5, 'medium': 0.7, 'high': 0.8, 'very_high': 1.0}
        complexity_weight = complexity_weights.get(complexity, 0.7)
        
        # Content quality indicators
        quality_indicators = ['because', 'however', 'therefore', 'consider', 'explore', 'understand']
        quality_score = sum(1 for indicator in quality_indicators if indicator in response.lower()) / len(quality_indicators)
        
        return (length_score + quality_score + complexity_weight) / 3
    
    def _analyze_memory_recall(self, response: str, reference_content: str) -> float:
        """Analyze how well the response recalls previous context"""
        response_lower = response.lower()
        reference_lower = reference_content.lower()
        
        # Extract key terms from reference
        key_terms = []
        if 'meditation' in reference_lower:
            key_terms.extend(['meditation', 'mindfulness', 'practice'])
        if 'music' in reference_lower:
            key_terms.extend(['music', 'composition', 'digital consciousness'])
        if 'team' in reference_lower:
            key_terms.extend(['team', 'framework', 'ethical', 'innovation'])
        
        # Check for recall indicators
        recall_indicators = ['remember', 'mentioned', 'discussed', 'previous', 'earlier']
        
        # Calculate recall score
        term_matches = sum(1 for term in key_terms if term in response_lower)
        recall_matches = sum(1 for indicator in recall_indicators if indicator in response_lower)
        
        if not key_terms:
            return 0.5  # Neutral if no key terms to match
        
        term_score = term_matches / len(key_terms)
        recall_score = min(recall_matches / 2, 1.0)  # Max 2 recall indicators
        
        return (term_score + recall_score) / 2
    
    def _analyze_context_development(self, response: str, test_type: str) -> float:
        """Analyze how well the response develops context"""
        response_lower = response.lower()
        
        development_indicators = {
            'specific_recall': ['specific', 'particular', 'example', 'instance'],
            'cross_domain_synthesis': ['connection', 'relationship', 'integrate', 'combine'],
            'continuation_development': ['next', 'further', 'develop', 'expand', 'build']
        }
        
        indicators = development_indicators.get(test_type, [])
        matches = sum(1 for indicator in indicators if indicator in response_lower)
        
        # General development indicators
        general_indicators = ['because', 'therefore', 'consider', 'explore', 'approach']
        general_matches = sum(1 for indicator in general_indicators if indicator in response_lower)
        
        if not indicators:
            return min(general_matches / len(general_indicators), 1.0)
        
        specific_score = matches / len(indicators)
        general_score = min(general_matches / len(general_indicators), 1.0)
        
        return (specific_score + general_score) / 2
    
    def calculate_overall_results(self):
        """Calculate overall Day 15 success metrics"""
        print("\n🏆 DAY 15 OVERALL ASSESSMENT")
        print("=" * 70)
        
        # Extract key metrics
        basic_persistence = self.test_results['basic_persistence'].get('persistence_fidelity', 0.0)
        accumulative_memory = self.test_results['accumulative_memory'].get('accumulation_success', 0.0)
        cognitive_integration = self.test_results['cognitive_integration'].get('capability_achievement', 0.0)
        session_continuity = self.test_results['session_continuity'].get('overall_session_persistence', 0.0)
        performance_scalability = 1.0 if (self.test_results['performance_scalability'].get('acceptable_performance', False) and 
                                         self.test_results['performance_scalability'].get('linear_scaling', False)) else 0.0
        
        # Calculate overall success
        overall_success = (basic_persistence + accumulative_memory + cognitive_integration + 
                          session_continuity + performance_scalability) / 5
        
        # Determine status
        if overall_success >= 0.80:
            status = "SUCCESS"
        elif overall_success >= 0.70:
            status = "GOOD_PROGRESS"
        else:
            status = "NEEDS_WORK"
        
        # Store final results
        self.test_results.update({
            'overall_success': overall_success,
            'status': status,
            'basic_persistence_score': basic_persistence,
            'accumulative_memory_score': accumulative_memory,
            'cognitive_integration_score': cognitive_integration,
            'session_continuity_score': session_continuity,
            'performance_scalability_score': performance_scalability
        })
        
        print(f"1. Basic Persistence: {basic_persistence:.1%}")
        print(f"2. Accumulative Memory: {accumulative_memory:.1%}")
        print(f"3. Cognitive Integration: {cognitive_integration:.1%}")
        print(f"4. Session Continuity: {session_continuity:.1%}")
        print(f"5. Performance Scalability: {performance_scalability:.1%}")
        print()
        print(f"📊 Overall Success: {overall_success:.1%}")
        print(f"📊 Status: {status}")
        
        # Compare with Day 14 baseline
        day14_baseline = 0.615  # 61.5% from Day 14
        improvement = overall_success - day14_baseline
        
        print(f"📊 Day 14 Baseline: {day14_baseline:.1%}")
        print(f"📈 Improvement: {improvement:+.1%}")
        
        if status == "SUCCESS":
            print("🎉 Day 15 memory persistence foundation successfully established!")
        elif status == "GOOD_PROGRESS":
            print("📈 Good progress on memory persistence, minor issues to address")
        else:
            print("⚠️ Memory persistence needs additional work")
    
    def save_results(self):
        """Save test results to file"""
        results_dir = Path(__file__).parent.parent / "results"
        results_dir.mkdir(exist_ok=True)
        
        results_file = results_dir / f"day_15_results_{self.test_results['test_date']}.json"
        
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"💾 Results saved to: {results_file}")


def main():
    """Run Day 15 memory persistence test"""
    test = Day15PersistenceTest()
    
    try:
        test.run_comprehensive_test()
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        test.cleanup()
    
    print("\n🏁 Day 15 memory persistence testing completed")


if __name__ == "__main__":
    main()
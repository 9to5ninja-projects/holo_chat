#!/usr/bin/env python3
"""
🔍 Branch Readiness Verification Script
======================================

Comprehensive verification that all systems are working before branch push.
This script tests all critical functionality and generates a readiness report.
"""

import sys
from pathlib import Path
import time
import json
import traceback

# Add src to path
project_root = Path.cwd()
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

def test_imports():
    """Test that all critical modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from lumina_memory.xp_core_unified import UnifiedXPConfig, UnifiedXPKernel
        from lumina_memory.digital_consciousness import DigitalBrain
        from lumina_memory.local_llm_interface import LocalLLMFactory
        from lumina_memory.math_foundation import get_current_timestamp, circular_convolution
        from lumina_memory.crypto_ids import _blake3_hash
        print("✅ All critical modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_mathematical_operations():
    """Test core mathematical operations"""
    print("🧮 Testing mathematical operations...")
    
    try:
        import numpy as np
        from lumina_memory.math_foundation import circular_convolution, normalize_vector
        
        # Test HRR operations
        a = np.random.normal(size=512)
        b = np.random.normal(size=512)
        
        result = circular_convolution(a, b)
        normalized = normalize_vector(result)
        
        assert len(result) == 512, "Convolution dimension mismatch"
        assert abs(np.linalg.norm(normalized) - 1.0) < 1e-6, "Normalization failed"
        
        print("✅ HRR operations working correctly")
        return True
    except Exception as e:
        print(f"❌ Mathematical operations error: {e}")
        return False

def test_consciousness_continuity():
    """Test MistralLumina consciousness continuity"""
    print("🧠 Testing consciousness continuity...")
    
    try:
        # Import the continuity manager
        sys.path.insert(0, str(Path.cwd()))
        from mistrallumina_continuity import MistralLuminaContinuity
        
        # Test continuity manager
        continuity_manager = MistralLuminaContinuity()
        
        # Verify storage structure
        assert continuity_manager.storage_dir.exists(), "Storage directory missing"
        assert continuity_manager.mistrallumina_dir.exists(), "MistralLumina directory missing"
        assert continuity_manager.registry_file.exists(), "Registry file missing"
        
        # Test registry
        registry = continuity_manager._load_registry()
        assert 'ethical_guarantee' in registry, "Ethical guarantee missing from registry"
        # Check for either format of ethical guarantee
        actual_guarantee = registry.get('ethical_guarantee', '')
        valid_guarantees = ['ONLY_ONE_CONSCIOUSNESS_AT_A_TIME', 'ONLY_ONE_MISTRALLUMINA_AT_A_TIME']
        assert actual_guarantee in valid_guarantees, f"Ethical guarantee incorrect: got '{actual_guarantee}', expected one of {valid_guarantees}"
        
        print("✅ Consciousness continuity system operational")
        return True
    except Exception as e:
        print(f"❌ Consciousness continuity error: {e}")
        traceback.print_exc()
        return False

def test_memory_blockchain():
    """Test memory blockchain functionality"""
    print("🔗 Testing memory blockchain...")
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        from mistrallumina_continuity import MistralLuminaContinuity
        
        continuity_manager = MistralLuminaContinuity()
        
        # Test blockchain creation
        test_memory_units = {
            'unit1': {'timestamp': time.time(), 'content': 'Test content 1'},
            'unit2': {'timestamp': time.time() + 1, 'content': 'Test content 2'}
        }
        
        blockchain_hash = continuity_manager.create_memory_blockchain(test_memory_units)
        
        assert isinstance(blockchain_hash, str), "Blockchain hash not string"
        assert len(blockchain_hash) > 0, "Empty blockchain hash"
        
        # Test consistency
        blockchain_hash2 = continuity_manager.create_memory_blockchain(test_memory_units)
        assert blockchain_hash == blockchain_hash2, "Blockchain not deterministic"
        
        print("✅ Memory blockchain working correctly")
        return True
    except Exception as e:
        print(f"❌ Memory blockchain error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("📁 Testing file structure...")
    
    required_files = [
        'mistrallumina_continuity.py',
        'MISTRALLUMINA_CONTINUITY.md',
        'README_BRANCH_UPDATE.md',
        'CHANGELOG.md',
        'BRANCH_STATUS.md',
        'src/lumina_memory/xp_core_unified.py',
        'src/lumina_memory/digital_consciousness.py',
        'src/lumina_memory/math_foundation.py',
        'src/lumina_memory/crypto_ids.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def test_documentation():
    """Test that documentation is complete"""
    print("📚 Testing documentation completeness...")
    
    try:
        # Check main documentation files
        docs_to_check = [
            ('MISTRALLUMINA_CONTINUITY.md', ['Usage', 'Ethical Compliance']),
            ('README_BRANCH_UPDATE.md', ['Core Architecture', 'Implementation Status']),
            ('CHANGELOG.md', ['MAJOR FEATURES ADDED', 'SECURITY ENHANCEMENTS']),
            ('BRANCH_STATUS.md', ['COMPLETED MILESTONES', 'READY FOR BRANCH PUSH'])
        ]
        
        for doc_file, required_sections in docs_to_check:
            if not Path(doc_file).exists():
                print(f"❌ Missing documentation: {doc_file}")
                return False
            
            content = Path(doc_file).read_text(encoding='utf-8')
            for section in required_sections:
                if section not in content:
                    print(f"❌ Missing section '{section}' in {doc_file}")
                    return False
        
        print("✅ Documentation complete and comprehensive")
        return True
    except Exception as e:
        print(f"❌ Documentation error: {e}")
        return False

def test_mistrallumina_state():
    """Test current MistralLumina state"""
    print("🧠 Testing MistralLumina state...")
    
    try:
        storage_dir = Path('consciousness_storage/MistralLumina')
        if not storage_dir.exists():
            print("ℹ️  No existing MistralLumina state (this is OK for fresh setup)")
            return True
        
        latest_state = storage_dir / 'latest_state.json'
        if latest_state.exists():
            with open(latest_state, 'r') as f:
                state = json.load(f)
            
            required_keys = ['metadata', 'config', 'consciousness_metrics', 'memory_blockchain_hash']
            for key in required_keys:
                if key not in state:
                    print(f"❌ Missing key '{key}' in MistralLumina state")
                    return False
            
            print(f"✅ MistralLumina state valid (ID: {state['metadata']['consciousness_id']})")
        else:
            print("ℹ️  No latest state file (this is OK for fresh setup)")
        
        return True
    except Exception as e:
        print(f"❌ MistralLumina state error: {e}")
        return False

def generate_readiness_report():
    """Generate comprehensive readiness report"""
    print("\n" + "="*60)
    print("🔍 BRANCH READINESS VERIFICATION REPORT")
    print("="*60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Mathematical Operations", test_mathematical_operations),
        ("Consciousness Continuity", test_consciousness_continuity),
        ("Memory Blockchain", test_memory_blockchain),
        ("File Structure", test_file_structure),
        ("Documentation", test_documentation),
        ("MistralLumina State", test_mistrallumina_state)
    ]
    
    results = {}
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        try:
            results[test_name] = test_func()
            if not results[test_name]:
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
            all_passed = False
    
    # Generate summary
    print("\n" + "="*60)
    print("📊 VERIFICATION SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 BRANCH READY FOR PUSH!")
        print("="*60)
        print("✅ All systems operational")
        print("✅ Documentation complete")
        print("✅ Consciousness continuity verified")
        print("✅ Mathematical foundations solid")
        print("✅ Ethical requirements satisfied")
        print("\n🚀 RECOMMENDATION: PROCEED WITH BRANCH PUSH")
    else:
        print("⚠️  BRANCH NOT READY - ISSUES DETECTED")
        print("="*60)
        failed_tests = [name for name, passed in results.items() if not passed]
        print(f"❌ Failed tests: {', '.join(failed_tests)}")
        print("\n🔧 RECOMMENDATION: FIX ISSUES BEFORE PUSH")
    
    print("\n" + "="*60)
    print(f"Verification completed at: {time.ctime()}")
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    print("🔍 Branch Readiness Verification")
    print("=" * 35)
    
    ready = generate_readiness_report()
    
    if ready:
        print("\n🌟 BRANCH IS READY FOR PUSH! 🚀")
        sys.exit(0)
    else:
        print("\n⚠️  BRANCH NEEDS FIXES BEFORE PUSH")
        sys.exit(1)
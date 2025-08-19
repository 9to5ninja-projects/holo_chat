#!/usr/bin/env python3
"""
Test Fixed Integration
=====================

Quick test of the fixed unified persistent environment to validate
the composition-based architecture fixes.
"""

import sys
import os
import tempfile
import shutil

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lumina_memory.unified_persistent_environment_fixed import UnifiedPersistentEnvironmentFixed


def test_fixed_integration():
    """Test the fixed integration architecture"""
    print("🔧 Testing Fixed Integration Architecture")
    print("=" * 50)
    
    # Create temporary storage
    temp_dir = tempfile.mkdtemp()
    
    try:
        print("1. Creating fixed unified environment...")
        env = UnifiedPersistentEnvironmentFixed(temp_dir)
        print(f"   ✅ Environment created with {len(env.persistent_backend.units)} existing units")
        
        print("2. Testing basic ingestion...")
        unit1 = env.ingest_experience("I love hiking in the mountains.")
        unit2 = env.ingest_experience("My favorite color is blue.")
        print(f"   ✅ Ingested 2 units, total: {len(env.persistent_backend.units)}")
        
        print("3. Testing emotion processing...")
        response = env.process_with_emotion("Tell me about hiking and colors.")
        print(f"   ✅ Emotion processing successful: {len(response)} chars")
        print(f"   Response preview: {response[:100]}...")
        
        print("4. Testing mathematical memory management...")
        optimization_stats = env.optimize_memory_storage()
        print(f"   ✅ Storage optimization: {optimization_stats.get('units_processed', 0)} units processed")
        
        print("5. Testing comprehensive stats...")
        stats = env.get_unified_stats()
        print(f"   ✅ Stats retrieved: {stats.get('persistence', {}).get('total_units', 0)} total units")
        
        print("6. Testing retrieval...")
        similar_units = env.retrieve_similar("hiking", k=3)
        print(f"   ✅ Retrieved {len(similar_units)} similar units")
        
        print("\n🎉 All fixed integration tests PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Fixed integration test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


if __name__ == "__main__":
    success = test_fixed_integration()
    if success:
        print("\n✅ Fixed integration architecture is working!")
    else:
        print("\n❌ Fixed integration architecture needs more work.")
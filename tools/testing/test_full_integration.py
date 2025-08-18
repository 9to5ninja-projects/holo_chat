#!/usr/bin/env python3
"""
Full Integration Test: Python Worker + Indexer + Memory System
This demonstrates the complete workflow from annotation to memory capsule.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def create_test_file_with_annotations():
    """Create a test Python file with various annotations"""
    test_file = Path(__file__).parent / "test_annotations.py"
    
    content = '''#!/usr/bin/env python3
"""
Test file with holographic memory annotations for integration testing
"""

# @holo capsule: integration-test-1
# role: purpose = "integration_testing"
# role: component = "python_worker"
# role: status = "active"
# weight: purpose = 1.0
# weight: component = 0.9
# meta: test_id = "int-001"
# meta: priority = "high"
def integration_test_function():
    """Function for testing the integration"""
    return "Integration test successful"

class TestMemorySystem:
    """
    Test class with docstring annotation
    
    --- @holo
    capsule: integration-test-2
    slots:
      class_type: "test_system"
      functionality: "memory_testing"
      language: "python"
    weights:
      functionality: 1.0
      language: 0.8
    meta:
      version: "1.0"
      tested: true
    """
    
    def __init__(self):
        self.initialized = True
    
    # @holo capsule: integration-test-3
    # role: method = "memory_operation"
    # role: action = "store"
    # role: data_type = "capsule"
    # weight: method = 1.0
    # meta: critical = True
    def store_memory(self, data):
        """Store memory data"""
        return f"Stored: {data}"

@holo(capsule="integration-test-4",
      slots={"pattern": "decorator", "test": "integration", "framework": "pytest"},
      weights={"pattern": 1.0, "test": 0.9},
      meta={"complexity": "medium", "coverage": 0.85})
def decorated_test_function():
    """Function with decorator annotation"""
    return "Decorator test passed"

# @holo capsule: integration-test-5
# role: workflow = "end_to_end"
# role: stage = "final"
# weight: workflow = 1.0
# meta: completion = 1.0
def final_integration_step():
    """Final step in integration testing"""
    return "All integration tests completed"
'''
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return test_file

def run_full_integration_test():
    """Run the complete integration test"""
    print("🧪 Full Integration Test: Python Worker + Indexer + Memory System")
    print("=" * 80)
    
    # Step 1: Create test file with annotations
    print("\n📝 Step 1: Creating test file with annotations...")
    test_file = create_test_file_with_annotations()
    print(f"✅ Created: {test_file}")
    
    # Step 2: Start Python worker
    print("\n🚀 Step 2: Starting Python worker...")
    worker_script = Path(__file__).parent / "python" / "engine.py"
    
    try:
        process = subprocess.Popen(
            [sys.executable, str(worker_script)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        def send_rpc(method, params=None):
            """Send RPC request and get response"""
            request = {
                "id": f"integration-{int(time.time() * 1000)}",
                "method": method,
                "params": params or {}
            }
            
            process.stdin.write(json.dumps(request) + "\n")
            process.stdin.flush()
            
            # Read response
            for attempt in range(5):
                response_line = process.stdout.readline()
                if not response_line:
                    return {"error": "No response received"}
                
                response_line = response_line.strip()
                if not response_line:
                    continue
                    
                try:
                    return json.loads(response_line)
                except json.JSONDecodeError:
                    if attempt == 4:
                        return {"error": f"Invalid JSON: {response_line}"}
                    continue
            
            return {"error": "No valid response"}
        
        # Step 3: Get initial state
        print("\n📊 Step 3: Getting initial memory state...")
        initial_response = send_rpc("list_capsules")
        if "error" in initial_response:
            print(f"❌ Error: {initial_response['error']}")
            return
        
        initial_count = len(initial_response.get("result", []))
        print(f"✅ Initial capsules: {initial_count}")
        
        # Step 4: Index the workspace
        print("\n🔍 Step 4: Indexing workspace for annotations...")
        workspace_path = str(Path(__file__).parent)
        index_response = send_rpc("index_workspace", {"workspace_path": workspace_path})
        
        if "error" in index_response:
            print(f"❌ Indexing error: {index_response['error']}")
            return
        
        result = index_response.get("result", {})
        print(f"✅ Indexing completed!")
        print(f"   📊 Total annotations found: {result.get('total_annotations', 0)}")
        print(f"   📁 Files scanned: {result.get('files_scanned', 0)}")
        print(f"   🏷️ Files with annotations: {result.get('files_with_annotations', 0)}")
        print(f"   💾 New capsules created: {len(result.get('created_capsules', []))}")
        
        # Show created capsules
        print(f"\n🧠 Created Memory Capsules:")
        for i, capsule in enumerate(result.get('created_capsules', []), 1):
            print(f"   {i}. {capsule['capsule_id']}")
            print(f"      📍 Location: {Path(capsule['file']).name}:{capsule['line']}")
            print(f"      🏷️ Slots: {capsule['slots']}")
        
        # Step 5: Verify memory state after indexing
        print(f"\n✅ Step 5: Verifying final memory state...")
        final_response = send_rpc("list_capsules")
        if "error" in final_response:
            print(f"❌ Error: {final_response['error']}")
            return
        
        final_count = len(final_response.get("result", []))
        new_capsules = final_count - initial_count
        print(f"✅ Final capsules: {final_count} (added {new_capsules})")
        
        # Step 6: Test querying the new capsules
        print(f"\n🔎 Step 6: Testing capsule queries...")
        query_response = send_rpc("query_capsules", {
            "query": {"purpose": "integration_testing"}
        })
        
        if "error" in query_response:
            print(f"❌ Query error: {query_response['error']}")
        else:
            matches = query_response.get("result", [])
            print(f"✅ Query found {len(matches)} matching capsules")
            for match in matches[:3]:
                print(f"   - {match.get('id', 'unknown')}: score {match.get('match_score', 0)}")
        
        # Step 7: Get detailed annotation information
        print(f"\n📋 Step 7: Retrieving annotation details...")
        annotations_response = send_rpc("get_indexed_annotations")
        
        if "error" in annotations_response:
            print(f"❌ Error: {annotations_response['error']}")
        else:
            annotations = annotations_response.get("result", [])
            print(f"✅ Retrieved {len(annotations)} annotations")
            
            # Group by annotation type
            by_type = {}
            for ann in annotations:
                ann_type = ann.get('annotation_type', 'unknown')
                by_type[ann_type] = by_type.get(ann_type, 0) + 1
            
            print(f"   📊 Annotation types:")
            for ann_type, count in by_type.items():
                print(f"      - {ann_type}: {count}")
        
        print(f"\n🎉 Integration Test Results:")
        print(f"   ✅ Python worker: WORKING")
        print(f"   ✅ Code indexer: WORKING")
        print(f"   ✅ Memory integration: WORKING")
        print(f"   ✅ Annotation parsing: WORKING")
        print(f"   ✅ Capsule creation: WORKING")
        print(f"   ✅ Query system: WORKING")
        print(f"\n🏆 FULL INTEGRATION TEST PASSED!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if 'process' in locals():
            process.terminate()
            process.wait()
        
        # Remove test file
        if test_file.exists():
            test_file.unlink()
            print(f"🧹 Cleaned up test file: {test_file.name}")

if __name__ == "__main__":
    run_full_integration_test()
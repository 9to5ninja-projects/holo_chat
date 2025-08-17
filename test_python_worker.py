#!/usr/bin/env python3
"""
Test script for the Python worker with indexer integration
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def test_python_worker():
    """Test the Python worker functionality"""
    print("Testing Python Worker with Indexer Integration")
    print("=" * 60)
    
    # Start the Python worker process
    worker_script = Path(__file__).parent / "python" / "engine.py"
    
    print(f"🚀 Starting Python worker: {worker_script}")
    
    try:
        # Start the worker process
        process = subprocess.Popen(
            [sys.executable, str(worker_script)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        def send_rpc(method, params=None):
            """Send an RPC request to the worker"""
            request = {
                "id": f"test-{int(time.time() * 1000)}",
                "method": method,
                "params": params or {}
            }
            
            print(f"📤 Sending: {method}")
            process.stdin.write(json.dumps(request) + "\n")
            process.stdin.flush()
            
            # Read response (may need to skip non-JSON lines)
            max_attempts = 5
            for attempt in range(max_attempts):
                response_line = process.stdout.readline()
                if not response_line:
                    return {"error": "No response received"}
                
                response_line = response_line.strip()
                if not response_line:
                    continue
                    
                try:
                    response = json.loads(response_line)
                    return response
                except json.JSONDecodeError as e:
                    # Skip non-JSON lines (like startup messages)
                    if attempt == max_attempts - 1:
                        print(f"❌ JSON decode error: {e}")
                        print(f"Raw response: {response_line}")
                        return {"error": f"JSON decode error: {e}"}
                    continue
            
            return {"error": "No valid JSON response received"}
        
        # Test 1: List existing capsules
        print("\n1️⃣ Testing list_capsules...")
        response = send_rpc("list_capsules")
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            capsules = response.get("result", [])
            print(f"✅ Found {len(capsules)} existing capsules")
            for capsule in capsules[:3]:  # Show first 3
                print(f"   - {capsule.get('id', 'unknown')}: {capsule.get('label', 'no label')}")
        
        # Test 2: Create a new capsule
        print("\n2️⃣ Testing create_capsule...")
        new_capsule_data = {
            "WHAT": "test_capsule",
            "WHERE": "python_worker",
            "WHEN": "now",
            "WHO": "test_script"
        }
        response = send_rpc("create_capsule", {"bindings": new_capsule_data})
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            result = response.get("result", {})
            if isinstance(result, dict) and result.get("success"):
                print(f"✅ Created capsule: {result['capsule']['id']}")
            else:
                print(f"❌ Failed to create capsule: {result}")
        
        # Test 3: Index workspace (the new functionality!)
        print("\n3️⃣ Testing index_workspace...")
        workspace_path = str(Path(__file__).parent)
        response = send_rpc("index_workspace", {"workspace_path": workspace_path})
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            result = response.get("result", {})
            print(f"✅ Indexing complete!")
            print(f"   📊 Total annotations: {result.get('total_annotations', 0)}")
            print(f"   📁 Files scanned: {result.get('files_scanned', 0)}")
            print(f"   🏷️ Files with annotations: {result.get('files_with_annotations', 0)}")
            print(f"   💾 Capsules created: {len(result.get('created_capsules', []))}")
            
            # Show created capsules
            for capsule in result.get('created_capsules', [])[:3]:
                print(f"   - {capsule['capsule_id']}: {capsule['slots']}")
        
        # Test 4: Get indexed annotations
        print("\n4️⃣ Testing get_indexed_annotations...")
        response = send_rpc("get_indexed_annotations")
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            annotations = response.get("result", [])
            print(f"✅ Retrieved {len(annotations)} annotations")
            for ann in annotations[:3]:  # Show first 3
                print(f"   - {ann['capsule_id']} ({ann['annotation_type']}): {ann['slots']}")
        
        # Test 5: List capsules again to see new ones
        print("\n5️⃣ Testing list_capsules (after indexing)...")
        response = send_rpc("list_capsules")
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            capsules = response.get("result", [])
            print(f"✅ Now have {len(capsules)} total capsules")
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if 'process' in locals():
            process.terminate()
            process.wait()
            print("🧹 Worker process terminated")

if __name__ == "__main__":
    test_python_worker()
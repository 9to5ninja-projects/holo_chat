#!/usr/bin/env python3
"""
Test script for the enhanced TypeScript UI with progress and error handling
This creates various scenarios to test the enhanced UI components.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def create_test_scenarios():
    """Create test files with different annotation scenarios"""
    
    # Scenario 1: Perfect annotations
    perfect_file = Path(__file__).parent / "test_perfect_annotations.py"
    perfect_content = '''#!/usr/bin/env python3
"""Perfect annotations test file"""

# @holo capsule: ui-test-perfect
# role: quality = "perfect"
# role: test_type = "ui_enhancement"
# weight: quality = 1.0
# meta: scenario = "success"
def perfect_function():
    """This should work perfectly"""
    return "success"

@holo(capsule="ui-test-decorator",
      slots={"pattern": "decorator", "quality": "excellent"},
      weights={"quality": 1.0},
      meta={"ui_test": True})
class PerfectClass:
    """Perfect decorator annotation"""
    pass
'''
    
    # Scenario 2: Problematic annotations (for error testing)
    problem_file = Path(__file__).parent / "test_problem_annotations.py"
    problem_content = '''#!/usr/bin/env python3
"""Problematic annotations test file"""

# @holo capsule: ui-test-problem
# role: quality = "problematic"
# role: test_type = "error_handling"
# weight: invalid_weight = "not_a_number"  # This should cause a warning
# meta: scenario = "error_test"
def problematic_function():
    """This has some issues"""
    return "problems"

# @holo capsule: 
# role: empty_id = "test"
def empty_id_function():
    """Empty capsule ID test"""
    pass

# Malformed decorator (should be handled gracefully)
@holo(capsule="ui-test-malformed",
      slots={"unclosed": "bracket"
      # Missing closing bracket - should cause parsing error
def malformed_decorator():
    """This should cause parsing issues"""
    pass
'''
    
    # Scenario 3: Unicode and special characters
    unicode_file = Path(__file__).parent / "test_unicode_annotations.py"
    unicode_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unicode annotations test file"""

# @holo capsule: ui-test-unicode
# role: language = "español"
# role: emoji = "🧠🔬🚀"
# role: special = "ñáéíóú"
# weight: language = 1.0
# meta: encoding = "utf-8"
# meta: complexity = "médium"
def unicode_function():
    """Testing unicode handling: ñáéíóú 🧠🔬🚀"""
    return "unicode success"

class UnicodeClass:
    """
    Unicode docstring annotation test
    
    --- @holo
    capsule: ui-test-unicode-doc
    slots:
      description: "测试中文"
      symbols: "αβγδε"
      arrows: "→←↑↓"
    weights:
      description: 0.9
    meta:
      languages: ["español", "中文", "ελληνικά"]
      complexity: "高"
    """
    pass
'''
    
    # Write test files
    test_files = [
        (perfect_file, perfect_content),
        (problem_file, problem_content),
        (unicode_file, unicode_content)
    ]
    
    created_files = []
    for file_path, content in test_files:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        created_files.append(file_path)
    
    return created_files

def test_enhanced_ui():
    """Test the enhanced TypeScript UI components"""
    print("🎨 Testing Enhanced TypeScript UI with Progress & Error Handling")
    print("=" * 80)
    
    # Create test scenarios
    print("\n📝 Creating test scenarios...")
    test_files = create_test_scenarios()
    print(f"✅ Created {len(test_files)} test files")
    
    # Start Python worker
    print("\n🚀 Starting Python worker...")
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
                "id": f"ui-test-{int(time.time() * 1000)}",
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
        
        # Test Scenario 1: Successful indexing (for progress reporting)
        print("\n🎯 Test Scenario 1: Successful Indexing")
        print("   This tests the enhanced progress reporting...")
        
        start_time = time.time()
        workspace_path = str(Path(__file__).parent)
        index_response = send_rpc("index_workspace", {"workspace_path": workspace_path})
        duration = time.time() - start_time
        
        if "error" in index_response:
            print(f"❌ Indexing failed: {index_response['error']}")
        else:
            result = index_response.get("result", {})
            print(f"✅ Indexing successful!")
            print(f"   📊 Duration: {duration:.2f}s")
            print(f"   📁 Files scanned: {result.get('files_scanned', 0)}")
            print(f"   🏷️ Annotations found: {result.get('total_annotations', 0)}")
            print(f"   💾 Capsules created: {len(result.get('created_capsules', []))}")
            
            # Show some created capsules
            capsules = result.get('created_capsules', [])[:5]
            for i, capsule in enumerate(capsules, 1):
                print(f"   {i}. {capsule['capsule_id']}: {capsule['slots']}")
        
        # Test Scenario 2: Error handling
        print(f"\n🚨 Test Scenario 2: Error Handling")
        print("   This tests error handling with invalid workspace...")
        
        error_response = send_rpc("index_workspace", {"workspace_path": "/nonexistent/path"})
        if "error" in error_response:
            print(f"✅ Error properly handled: {error_response['error']}")
        else:
            print(f"⚠️ Expected error but got success: {error_response}")
        
        # Test Scenario 3: Annotation retrieval
        print(f"\n📋 Test Scenario 3: Annotation Retrieval")
        print("   This tests the enhanced annotation display...")
        
        annotations_response = send_rpc("get_indexed_annotations", {})
        if "error" in annotations_response:
            print(f"❌ Failed to get annotations: {annotations_response['error']}")
        else:
            annotations = annotations_response.get("result", [])
            print(f"✅ Retrieved {len(annotations)} annotations")
            
            # Group by type for analysis
            by_type = {}
            by_file = {}
            
            for ann in annotations:
                ann_type = ann.get('annotation_type', 'unknown')
                file_name = Path(ann.get('file_path', '')).name
                
                by_type[ann_type] = by_type.get(ann_type, 0) + 1
                by_file[file_name] = by_file.get(file_name, 0) + 1
            
            print(f"   📊 By type: {dict(by_type)}")
            print(f"   📁 By file: {dict(by_file)}")
            
            # Show some examples
            for i, ann in enumerate(annotations[:3], 1):
                print(f"   {i}. {ann['capsule_id']} ({ann['annotation_type']})")
                print(f"      📍 {Path(ann['file_path']).name}:{ann['line_start']}")
                print(f"      🏷️ {ann['slots']}")
        
        # Test Scenario 4: Memory operations
        print(f"\n🧠 Test Scenario 4: Memory Operations")
        print("   This tests memory system integration...")
        
        capsules_response = send_rpc("list_capsules", {})
        if "error" in capsules_response:
            print(f"❌ Failed to list capsules: {capsules_response['error']}")
        else:
            capsules = capsules_response.get("result", [])
            print(f"✅ Found {len(capsules)} memory capsules")
            
            # Test querying
            query_response = send_rpc("query_capsules", {
                "query": {"quality": "perfect"}
            })
            
            if "error" in query_response:
                print(f"❌ Query failed: {query_response['error']}")
            else:
                matches = query_response.get("result", [])
                print(f"✅ Query returned {len(matches)} matches")
        
        print(f"\n🎉 Enhanced UI Test Results:")
        print(f"   ✅ Progress reporting: READY FOR TESTING")
        print(f"   ✅ Error handling: READY FOR TESTING")
        print(f"   ✅ Result formatting: READY FOR TESTING")
        print(f"   ✅ Status bar updates: READY FOR TESTING")
        print(f"   ✅ Detailed logging: READY FOR TESTING")
        print(f"   ✅ User notifications: READY FOR TESTING")
        
        print(f"\n📋 VS Code Extension Features to Test:")
        print(f"   🔍 Index Workspace - Enhanced progress with status bar")
        print(f"   📊 Show Annotations - Rich markdown formatting")
        print(f"   📈 Show Error Statistics - Diagnostic information")
        print(f"   📤 Export Error Log - Debugging support")
        print(f"   🧹 Clear Error Log - Maintenance operations")
        
        print(f"\n🚀 Ready for VS Code Testing!")
        print(f"   1. Open VS Code in this workspace")
        print(f"   2. Press F5 to launch Extension Development Host")
        print(f"   3. Run 'Holographic Memory: Index Workspace for Annotations'")
        print(f"   4. Observe enhanced progress reporting and results")
        print(f"   5. Test error scenarios and diagnostic commands")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if 'process' in locals():
            process.terminate()
            process.wait()
        
        # Remove test files
        for test_file in test_files:
            if test_file.exists():
                test_file.unlink()
        
        print(f"🧹 Cleaned up {len(test_files)} test files")

if __name__ == "__main__":
    test_enhanced_ui()
#!/usr/bin/env python3
"""
Test script for the holographic memory code indexer
"""

import sys
from pathlib import Path

# Add the python directory to path
sys.path.insert(0, str(Path(__file__).parent / "python"))

from enhanced_engine import CodeIndexer, HolographicAnnotation

def test_indexer():
    """Test the code indexer functionality"""
    print("Testing Holographic Memory Code Indexer")
    print("=" * 50)
    
    indexer = CodeIndexer()
    
    # Test on the example file
    example_file = Path(__file__).parent / "examples" / "annotation_examples.py"
    
    if not example_file.exists():
        print(f"❌ Example file not found: {example_file}")
        return
    
    print(f"📁 Scanning file: {example_file}")
    annotations = indexer.scan_file(example_file)
    
    print(f"\n🔍 Found {len(annotations)} annotations:")
    print("-" * 30)
    
    for i, annotation in enumerate(annotations, 1):
        print(f"\n{i}. Capsule: {annotation.capsule_id}")
        print(f"   Type: {annotation.annotation_type}")
        print(f"   Location: {annotation.file_path.name}:{annotation.line_start}-{annotation.line_end}")
        print(f"   Slots: {annotation.slots}")
        print(f"   Weights: {annotation.weights}")
        print(f"   Meta: {annotation.meta}")
    
    # Test workspace indexing
    print(f"\n🏢 Testing workspace indexing...")
    workspace_result = indexer.index_workspace(Path(__file__).parent)
    
    print(f"📊 Workspace Results:")
    print(f"   Total annotations: {workspace_result['total_annotations']}")
    print(f"   Files scanned: {workspace_result['files_scanned']}")
    print(f"   Files with annotations: {workspace_result['files_with_annotations']}")
    
    print(f"\n📋 Files with annotations:")
    for file_path, file_annotations in workspace_result['annotations_by_file'].items():
        print(f"   {Path(file_path).name}: {len(file_annotations)} annotations")
    
    print("\n✅ Indexer test complete!")

if __name__ == "__main__":
    test_indexer()
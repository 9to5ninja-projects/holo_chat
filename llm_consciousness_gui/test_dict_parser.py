#!/usr/bin/env python3
"""
Test script for the enhanced dictionary-based AST parser.
This demonstrates the new parse_file_to_dict functionality.
"""

import sys
import json
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from parser.ast_parser import ASTParser


def test_dict_parser():
    """Test the dictionary-based parser on various Python files."""
    parser = ASTParser()
    
    # Test files from the project
    test_files = [
        current_dir / "parser" / "ast_parser.py",
        current_dir / "gui" / "main_window.py",
        current_dir / "gui" / "file_explorer.py",
        current_dir.parent / "src" / "lumina_memory" / "memory_system.py",
    ]
    
    print("🧠 STEP 4: Enhanced Class/Function Parser")
    print("=" * 60)
    print()
    
    for file_path in test_files:
        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}")
            continue
            
        print(f"📄 Parsing: {file_path.name}")
        print("-" * 40)
        
        # Parse using the new dictionary method
        result = parser.parse_file_to_dict(file_path)
        
        if "_error" in result:
            print(f"❌ Error: {result['_error']}")
            print()
            continue
        
        # Display the structure
        for name, info in result.items():
            if info["type"] == "class":
                print(f"🏛️  Class: {name}")
                print(f"   📍 Lines: {info['line_start']}-{info['line_end']}")
                if info["docstring"]:
                    print(f"   📝 Doc: {info['docstring'][:50]}...")
                if info["methods"]:
                    print(f"   ⚙️  Methods: {', '.join(info['methods'])}")
                    
                    # Show method details
                    for method_name in info["methods"][:3]:  # Show first 3 methods
                        method_info = info["children"][method_name]
                        print(f"      • {method_name} (lines {method_info['line_start']}-{method_info['line_end']})")
                        if method_info["args"]:
                            print(f"        Args: {', '.join(method_info['args'])}")
                        if method_info["returns"]:
                            print(f"        Returns: {method_info['returns']}")
                    
                    if len(info["methods"]) > 3:
                        print(f"      ... and {len(info['methods']) - 3} more methods")
                        
            elif info["type"] in ["function", "async_function"]:
                func_icon = "⚡" if info["type"] == "async_function" else "⚙️"
                print(f"{func_icon} Function: {name}")
                print(f"   📍 Lines: {info['line_start']}-{info['line_end']}")
                if info["docstring"]:
                    print(f"   📝 Doc: {info['docstring'][:50]}...")
                if info["args"]:
                    print(f"   📥 Args: {', '.join(info['args'])}")
                if info["returns"]:
                    print(f"   📤 Returns: {info['returns']}")
        
        print()
    
    print("✅ Dictionary-based parsing complete!")
    print()
    print("🎯 Expected Output Format:")
    print("-" * 30)
    
    # Show example of the expected format
    example = {
        "MyClass": {
            "type": "class",
            "methods": ["method_one", "method_two"],
            "children": {
                "method_one": {"type": "method"},
                "method_two": {"type": "method"}
            }
        },
        "function_one": {
            "type": "function"
        }
    }
    
    print(json.dumps(example, indent=2))
    print()
    print("🚀 Ready for tree visualization and LLM integration!")


if __name__ == "__main__":
    test_dict_parser()
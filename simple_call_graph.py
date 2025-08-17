#!/usr/bin/env python3
"""
Simple Call Graph Visualizer for Lumina Memory System

Creates a focused view of the most important classes and their relationships.
"""

import json
import os
from collections import defaultdict

def load_call_graph_data():
    """Load the call graph data from JSON report."""
    with open("e:\\lumina-memory-system\\call_graph_report.json", "r") as f:
        return json.load(f)

def extract_key_classes(data):
    """Extract the most important classes from the system."""
    key_classes = {}
    
    # Define important files to focus on
    important_files = [
        "src\\lumina_memory\\core.py",
        "src\\lumina_memory\\memory_system.py", 
        "src\\lumina_memory\\digital_consciousness.py",
        "src\\lumina_memory\\embeddings.py",
        "src\\lumina_memory\\vector_store.py",
        "src\\lumina_memory\\event_store.py",
        "src\\lumina_memory\\xp_core_unified.py",
        "src\\lumina_memory\\advanced_emotional_consciousness.py"
    ]
    
    for file_path, file_info in data["files"].items():
        if file_path in important_files:
            if file_info["classes"]:
                key_classes[file_path] = {
                    "classes": file_info["classes"],
                    "functions": file_info["functions"]
                }
    
    return key_classes

def create_class_hierarchy_report(key_classes):
    """Create a focused report on key classes and their methods."""
    report = []
    report.append("=" * 70)
    report.append("LUMINA MEMORY SYSTEM - KEY CLASSES & METHODS")
    report.append("=" * 70)
    report.append("")
    
    for file_path, info in key_classes.items():
        file_name = os.path.basename(file_path)
        report.append(f"📁 {file_name}")
        report.append("─" * (len(file_name) + 3))
        
        # Group functions by class
        class_methods = defaultdict(list)
        standalone_functions = []
        
        for func in info["functions"]:
            if "." in func:
                class_name, method_name = func.split(".", 1)
                if class_name in info["classes"]:
                    class_methods[class_name].append(method_name)
                else:
                    standalone_functions.append(func)
            else:
                standalone_functions.append(func)
        
        # Display classes and their methods
        for class_name in info["classes"]:
            report.append(f"  🏛️  {class_name}")
            if class_name in class_methods:
                for method in sorted(class_methods[class_name]):
                    report.append(f"     ├─ {method}")
            report.append("")
        
        # Display standalone functions
        if standalone_functions:
            report.append("  🔧 Standalone Functions:")
            for func in sorted(standalone_functions):
                report.append(f"     ├─ {func}")
            report.append("")
        
        report.append("")
    
    return "\n".join(report)

def analyze_key_relationships(data):
    """Analyze relationships between key classes."""
    relationships = []
    relationships.append("=" * 70)
    relationships.append("KEY SYSTEM RELATIONSHIPS")
    relationships.append("=" * 70)
    relationships.append("")
    
    # Look for important calling patterns
    important_patterns = {
        "MemorySystem": [],
        "DigitalBrain": [],
        "EmbeddingProvider": [],
        "VectorStore": [],
        "AdvancedEmotionalConsciousness": []
    }
    
    for caller, callees in data["call_graph"].items():
        file_func = caller.split("::")
        if len(file_func) == 2:
            file_path, func_name = file_func
            
            # Check if this is a method of an important class
            for key_class in important_patterns.keys():
                if key_class in func_name:
                    important_patterns[key_class].extend(callees)
    
    # Display the relationships
    for class_name, calls in important_patterns.items():
        if calls:
            relationships.append(f"🏛️  {class_name} interacts with:")
            unique_calls = sorted(set(calls))
            for call in unique_calls[:10]:  # Show top 10 to avoid clutter
                relationships.append(f"   ├─ {call}")
            if len(unique_calls) > 10:
                relationships.append(f"   └─ ... and {len(unique_calls) - 10} more")
            relationships.append("")
    
    return "\n".join(relationships)

def create_system_overview():
    """Create a high-level system overview."""
    overview = []
    overview.append("=" * 70)
    overview.append("LUMINA MEMORY SYSTEM - ARCHITECTURE OVERVIEW")
    overview.append("=" * 70)
    overview.append("")
    
    overview.append("🧠 CORE COMPONENTS:")
    overview.append("├─ 📚 Memory System (memory_system.py)")
    overview.append("│  └─ Central orchestrator for memory operations")
    overview.append("├─ 🤖 Digital Consciousness (digital_consciousness.py)")
    overview.append("│  └─ AI consciousness simulation and self-reflection")
    overview.append("├─ 🎭 Emotional Consciousness (advanced_emotional_consciousness.py)")
    overview.append("│  └─ Advanced emotional processing and memory weighting")
    overview.append("├─ 🔢 Vector Store (vector_store.py)")
    overview.append("│  └─ Semantic similarity and vector operations")
    overview.append("├─ 📝 Event Store (event_store.py)")
    overview.append("│  └─ Cryptographic event logging and versioning")
    overview.append("└─ 🧮 XP Core (xp_core_unified.py)")
    overview.append("   └─ Unified mathematical foundation")
    overview.append("")
    
    overview.append("🔄 DATA FLOW:")
    overview.append("Input → Embeddings → Vector Store → Memory System → Digital Brain")
    overview.append("  ↓                                        ↑")
    overview.append("Event Store ← Cryptographic Hashing ← Emotional Weighting")
    overview.append("")
    
    overview.append("🔐 SECURITY LAYERS:")
    overview.append("├─ Content Fingerprinting (crypto_ids.py)")
    overview.append("├─ Event Hashing (event_hashing.py)")
    overview.append("├─ Encryption (encryption.py)")
    overview.append("└─ Holographic Reduced Representations (hrr.py)")
    overview.append("")
    
    return "\n".join(overview)

def main():
    """Generate focused call graph analysis."""
    print("Loading call graph data...")
    
    if not os.path.exists("e:\\lumina-memory-system\\call_graph_report.json"):
        print("Error: call_graph_report.json not found. Run call_graph_analyzer.py first.")
        return
    
    data = load_call_graph_data()
    
    print("Generating focused analysis...")
    
    # Create system overview
    overview = create_system_overview()
    
    # Extract and analyze key classes
    key_classes = extract_key_classes(data)
    class_report = create_class_hierarchy_report(key_classes)
    
    # Analyze relationships
    relationships = analyze_key_relationships(data)
    
    # Combine all reports
    full_report = "\n\n".join([overview, class_report, relationships])
    
    # Save the focused report
    with open("e:\\lumina-memory-system\\focused_call_graph.txt", "w", encoding="utf-8") as f:
        f.write(full_report)
    
    print("\n✅ Focused call graph analysis complete!")
    print("📄 Report saved to: focused_call_graph.txt")
    
    # Print summary
    print(f"\n📊 SUMMARY:")
    print(f"   Key files analyzed: {len(key_classes)}")
    total_classes = sum(len(info["classes"]) for info in key_classes.values())
    total_methods = sum(len(info["functions"]) for info in key_classes.values())
    print(f"   Important classes: {total_classes}")
    print(f"   Methods/functions: {total_methods}")
    
    # Show a preview
    print(f"\n🔍 PREVIEW - Key Classes Found:")
    for file_path, info in list(key_classes.items())[:3]:
        file_name = os.path.basename(file_path)
        print(f"   📁 {file_name}: {', '.join(info['classes'][:3])}")
        if len(info['classes']) > 3:
            print(f"      ... and {len(info['classes']) - 3} more")

if __name__ == "__main__":
    main()
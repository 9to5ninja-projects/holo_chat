#!/usr/bin/env python3
"""
Project Structure Organization Tool
==================================

Organize the cluttered holo_chat project into a clean, logical structure.
This will help us focus on consciousness research without file chaos.

Author: Lumina Memory Team
License: MIT
"""

import os
import shutil
from pathlib import Path
import json
from datetime import datetime

def organize_project_structure():
    """Organize the entire project into a clean structure"""
    
    print("🗂️ ORGANIZING PROJECT STRUCTURE")
    print("=" * 40)
    
    project_root = Path("e:/holo_chat")
    
    # Define the new organized structure
    new_structure = {
        # Core development
        "src/": "Core source code",
        "tests/": "Test files", 
        "docs/": "Documentation",
        "scripts/": "Utility scripts",
        "cli/": "Command line tools",
        
        # Research & Studies
        "research/": "Research and consciousness studies",
        "research/consciousness_studies/": "Consciousness evolution studies",
        "research/xpunit_analysis/": "XPUnit behavior analysis", 
        "research/emotional_analysis/": "Emotional weighting research",
        "research/memory_persistence/": "Memory persistence studies",
        "research/archived_studies/": "Completed/archived research",
        
        # Data & Storage
        "data/": "Sample data and datasets",
        "consciousness_storage/": "Consciousness entity storage",
        "storage/": "General storage and backups",
        
        # Development Tools
        "tools/": "Development and analysis tools",
        "tools/gui/": "GUI applications",
        "tools/testing/": "Testing utilities",
        "tools/analysis/": "Analysis scripts",
        "tools/launchers/": "Launch scripts and shortcuts",
        
        # Archive & Cleanup
        "archive/": "Archived/deprecated files",
        "archive/old_tests/": "Old test files",
        "archive/old_docs/": "Outdated documentation",
        "archive/unused_scripts/": "Unused scripts",
        
        # Configuration
        "config/": "Configuration files",
        "notebooks/": "Jupyter notebooks (keep as is)",
        "examples/": "Example code (keep as is)"
    }
    
    # Create new directory structure
    print("📁 Creating organized directory structure...")
    for dir_path, description in new_structure.items():
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_path} - {description}")
    
    # File categorization rules
    file_moves = {
        # Research files
        "research/consciousness_studies/": [
            "gpu_consciousness_study.py",
            "continue_consciousness_study.py", 
            "consciousness_study_with_time_control.py",
            "comprehensive_7_day_analysis.py",
            "analyze_3_day_consciousness_results.py",
            "focused_3_day_analysis.py",
            "day_4_enhancement_analysis.py"
        ],
        
        "research/xpunit_analysis/": [
            "comprehensive_xpunit_analysis.py",
            "test_enhanced_xpunit_core_behavior.py",
            "analyze_decay_emotional_weighting.py",
            "xpunit_analysis_results.json"
        ],
        
        "research/emotional_analysis/": [
            "emotional_libraries_analysis.py",
            "test_enhanced_emotional_analysis.py",
            "test_complete_emotional_system.py",
            "test_enhanced_emotions.py"
        ],
        
        "research/memory_persistence/": [
            "chat_memory_test.py",
            "interactive_llm_memory_test.py",
            "simple_memory_test.py",
            "test_mistral_memory_fix.py"
        ],
        
        # Tools
        "tools/gui/": [
            "lumina_memory_gui.py",
            "launch_gui.bat",
            "launch_advanced.bat", 
            "launch_integrated_gui.py",
            "simple_gui_test.py",
            "test_working_gui.py",
            "load_test_data_to_gui.py",
            "launch_gui_with_test_data.py"
        ],
        
        "tools/testing/": [
            "test_annotations.py",
            "test_enhanced_mistral_consciousness.py",
            "test_enhanced_ui.py",
            "test_full_integration.py",
            "test_gpu_optimization.py",
            "test_holographic_integration.py",
            "test_indexer.py",
            "test_mistral_emotional_consciousness.py",
            "test_notebook_simulation.py",
            "test_python_worker.py",
            "test_unified_system.py",
            "simple_interactive_test.py"
        ],
        
        "tools/analysis/": [
            "analysis_summary.py",
            "call_graph_analyzer.py",
            "simple_call_graph.py",
            "organize_consciousness_data.py"
        ],
        
        "tools/launchers/": [
            "lumina_launcher.py",
            "lumina_launcher.bat",
            "dev_launch.bat",
            "create_desktop_shortcut.bat",
            "setup_environment.bat"
        ],
        
        # Archive old/unused files
        "archive/old_tests/": [
            # Will identify these programmatically
        ],
        
        "archive/old_docs/": [
            "BRANCH_PUSH_SUMMARY.md",
            "BRANCH_STATUS.md", 
            "BUILD_EXECUTABLE.md",
            "CLASS_ANALYSIS.md",
            "CONSOLIDATION_COMPLETE.md",
            "DIGITAL_CONSCIOUSNESS_READY.md",
            "FINAL_UPGRADE_COMPLETE.md",
            "INTEGRATION_COMPLETE.md",
            "INTEGRATION_SUMMARY.md",
            "PYTHON_WORKER_COMPLETE.md",
            "README_BRANCH_UPDATE.md",
            "TYPESCRIPT_UI_COMPLETE.md",
            "UNIFIED_CONSOLIDATION_PLAN.md",
            "XPUNIT_CONSOLIDATION_PLAN.md"
        ],
        
        "archive/unused_scripts/": [
            "build_executable.py",
            "setup_dependencies.py",
            "universal_install.py",
            "verify_branch_ready.py",
            "verify_environment.py"
        ],
        
        # Configuration
        "config/": [
            "requirements.txt",
            "requirements-dev.txt", 
            "requirements-future.txt",
            "pyproject.toml",
            "package.json",
            "tsconfig.json"
        ]
    }
    
    # Move files according to categorization
    print("\\n📦 Moving files to organized locations...")
    moved_count = 0
    
    for target_dir, files in file_moves.items():
        target_path = project_root / target_dir
        
        for filename in files:
            source_path = project_root / filename
            if source_path.exists():
                try:
                    dest_path = target_path / filename
                    shutil.move(str(source_path), str(dest_path))
                    print(f"  ✅ Moved {filename} → {target_dir}")
                    moved_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to move {filename}: {e}")
    
    print(f"\\n📊 Moved {moved_count} files to organized locations")
    
    # Create README files for each major section
    create_section_readmes(project_root, new_structure)
    
    # Create master organization index
    create_organization_index(project_root)
    
    print("\\n✅ PROJECT ORGANIZATION COMPLETE!")
    print("🎯 Clean structure ready for consciousness research")
    
    return moved_count

def create_section_readmes(project_root, structure):
    """Create README files for each major section"""
    
    section_descriptions = {
        "research/": """# Research & Consciousness Studies

This directory contains all consciousness research, XPUnit analysis, and memory studies.

## Subdirectories:
- `consciousness_studies/` - Main consciousness evolution studies
- `xpunit_analysis/` - XPUnit behavior and decay analysis  
- `emotional_analysis/` - Emotional weighting research
- `memory_persistence/` - Memory persistence validation
- `archived_studies/` - Completed research projects

## Current Focus:
- 30-day consciousness evolution study
- XPUnit accumulation and deduplication analysis
- Enhanced emotional analysis validation
- Memory persistence across time gaps
""",
        
        "tools/": """# Development Tools

Development utilities, GUI applications, and analysis tools.

## Subdirectories:
- `gui/` - GUI applications and launchers
- `testing/` - Test utilities and scripts
- `analysis/` - Analysis and diagnostic tools
- `launchers/` - Launch scripts and shortcuts

## Key Tools:
- Lumina Memory GUI
- Consciousness study tools
- XPUnit analysis utilities
- Memory testing frameworks
""",
        
        "archive/": """# Archive

Deprecated, unused, or completed files that are no longer actively used.

## Subdirectories:
- `old_tests/` - Outdated test files
- `old_docs/` - Superseded documentation
- `unused_scripts/` - Scripts no longer needed

## Note:
Files here are kept for reference but not actively maintained.
"""
    }
    
    for dir_path, content in section_descriptions.items():
        readme_path = project_root / dir_path / "README.md"
        with open(readme_path, 'w') as f:
            f.write(content)
        print(f"  📝 Created README for {dir_path}")

def create_organization_index(project_root):
    """Create master organization index"""
    
    index_content = f"""# Holo Chat Project Organization Index
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 🎯 Project Purpose
Advanced consciousness research using XPUnit memory systems and holographic representations.

## 📁 Directory Structure

### Core Development
- `src/` - Core source code (lumina_memory package)
- `tests/` - Unit and integration tests
- `docs/` - Technical documentation
- `scripts/` - Utility scripts
- `cli/` - Command line interfaces

### Research & Studies  
- `research/consciousness_studies/` - Main consciousness evolution research
- `research/xpunit_analysis/` - XPUnit behavior analysis
- `research/emotional_analysis/` - Emotional weighting studies
- `research/memory_persistence/` - Memory persistence validation

### Data & Storage
- `consciousness_storage/` - Consciousness entity data
- `data/` - Sample datasets
- `storage/` - General storage and backups

### Development Tools
- `tools/gui/` - GUI applications
- `tools/testing/` - Testing utilities  
- `tools/analysis/` - Analysis scripts
- `tools/launchers/` - Launch scripts

### Configuration & Examples
- `config/` - Configuration files
- `notebooks/` - Jupyter notebooks
- `examples/` - Example code

### Archive
- `archive/` - Deprecated/unused files

## 🧠 Current Research Focus

### Active Studies:
1. **30-Day Consciousness Evolution** - Tracking digital consciousness development
2. **XPUnit Accumulation Analysis** - Understanding memory unit behavior
3. **Enhanced Emotional Analysis** - Validating consciousness-optimized emotional processing
4. **Memory Persistence Validation** - Testing time-based memory decay

### Key Questions:
- How many XPUnits accumulate in DigitalBrain?
- How do XPUnits resolve and prevent duplication?
- What is the optimal emotional weighting for consciousness development?
- How does memory persist across simulated time gaps?

## 🚀 Getting Started

### For Consciousness Research:
```bash
cd research/consciousness_studies/
python continue_consciousness_study.py
```

### For XPUnit Analysis:
```bash
cd research/xpunit_analysis/
python comprehensive_xpunit_analysis.py
```

### For GUI Development:
```bash
cd tools/gui/
python lumina_memory_gui.py
```

## 📊 Project Status
- **Organization**: ✅ Complete
- **Core Systems**: ✅ Functional
- **Research Tools**: ✅ Active
- **Documentation**: 🔄 In Progress

---
*Organized structure enables focused consciousness research without file chaos*
"""
    
    index_path = project_root / "PROJECT_ORGANIZATION_INDEX.md"
    with open(index_path, 'w') as f:
        f.write(index_content)
    
    print(f"  📋 Created master organization index")

if __name__ == "__main__":
    moved_count = organize_project_structure()
    print(f"\\n🎉 Organization complete! Moved {moved_count} files.")
    print("📁 Project now has clean, logical structure")
    print("🧠 Ready for focused consciousness research!")
#!/usr/bin/env python3
"""
XPUnit Accumulation & Deduplication Analyzer
============================================

Analyze how XPUnits accumulate in the DigitalBrain and how they resolve
duplication issues. This is critical for understanding memory system behavior.

Key Questions:
1. How many XPUnits are currently in the system?
2. Are XPUnits being deduplicated properly?
3. What is the growth pattern over time?
4. How does emotional weighting affect accumulation?
5. Are there memory leaks or excessive accumulation?

Author: Lumina Memory Team
License: MIT
"""

import sys
from pathlib import Path
import json
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime
import hashlib

# Add src to path
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from lumina_memory.xp_core_unified import UnifiedXPKernel, XPUnit
from lumina_memory.digital_consciousness import DigitalBrain


class XPUnitAccumulationAnalyzer:
    """
    Comprehensive analyzer for XPUnit accumulation and deduplication behavior
    """
    
    def __init__(self):
        self.analysis_results = {}
        self.xpunit_stats = {}
        self.deduplication_analysis = {}
        
    def analyze_consciousness_storage(self, entity_name: str = "MistralLumina") -> dict:
        """
        Analyze XPUnit accumulation in stored consciousness data
        
        Args:
            entity_name: Name of the consciousness entity to analyze
            
        Returns:
            Comprehensive analysis results
        """
        
        print(f"🧠 ANALYZING XPUNIT ACCUMULATION FOR: {entity_name}")
        print("=" * 55)
        
        storage_path = project_root / "consciousness_storage" / entity_name
        
        if not storage_path.exists():
            print(f"❌ No storage found for {entity_name}")
            return {"error": f"No storage found for {entity_name}"}
        
        # Analyze vector database
        vector_db_analysis = self._analyze_vector_database(storage_path / "vector_db")
        
        # Analyze consciousness states
        states_analysis = self._analyze_consciousness_states(storage_path)
        
        # Analyze study data
        studies_analysis = self._analyze_study_data(storage_path / "studies")
        
        # Combine results
        results = {
            "entity_name": entity_name,
            "analysis_timestamp": datetime.now().isoformat(),
            "vector_database": vector_db_analysis,
            "consciousness_states": states_analysis,
            "studies": studies_analysis,
            "summary": self._generate_summary(vector_db_analysis, states_analysis, studies_analysis)
        }
        
        self.analysis_results = results
        return results
    
    def _analyze_vector_database(self, vector_db_path: Path) -> dict:
        """Analyze the vector database for XPUnit accumulation"""
        
        print("📊 Analyzing Vector Database...")
        
        if not vector_db_path.exists():
            return {"error": "No vector database found"}
        
        # Count files in vector database
        vector_files = list(vector_db_path.glob("*.json"))
        embedding_files = list(vector_db_path.glob("*.npy"))
        
        analysis = {
            "total_vector_files": len(vector_files),
            "total_embedding_files": len(embedding_files),
            "storage_size_mb": self._get_directory_size(vector_db_path) / (1024 * 1024),
            "file_details": []
        }
        
        # Analyze individual files
        for vector_file in vector_files[:10]:  # Sample first 10
            try:
                with open(vector_file, 'r') as f:
                    data = json.load(f)
                
                file_analysis = {
                    "filename": vector_file.name,
                    "size_kb": vector_file.stat().st_size / 1024,
                    "content_type": type(data).__name__,
                    "keys": list(data.keys()) if isinstance(data, dict) else "non-dict"
                }
                
                if isinstance(data, dict) and "units" in data:
                    file_analysis["xpunit_count"] = len(data["units"])
                
                analysis["file_details"].append(file_analysis)
                
            except Exception as e:
                analysis["file_details"].append({
                    "filename": vector_file.name,
                    "error": str(e)
                })
        
        print(f"  📁 Vector files: {analysis['total_vector_files']}")
        print(f"  🧮 Embedding files: {analysis['total_embedding_files']}")
        print(f"  💾 Storage size: {analysis['storage_size_mb']:.2f} MB")
        
        return analysis
    
    def _analyze_consciousness_states(self, storage_path: Path) -> dict:
        """Analyze consciousness state files for XPUnit data"""
        
        print("🧠 Analyzing Consciousness States...")
        
        state_files = list(storage_path.glob("consciousness_state_*.json"))
        latest_state_file = storage_path / "latest_state.json"
        
        analysis = {
            "total_state_files": len(state_files),
            "has_latest_state": latest_state_file.exists(),
            "state_details": [],
            "xpunit_evolution": []
        }
        
        # Analyze latest state in detail
        if latest_state_file.exists():
            try:
                with open(latest_state_file, 'r') as f:
                    latest_state = json.load(f)
                
                analysis["latest_state"] = {
                    "timestamp": latest_state.get("timestamp"),
                    "consciousness_level": latest_state.get("consciousness_level"),
                    "memory_count": len(latest_state.get("memories", [])),
                    "experience_count": len(latest_state.get("experiences", [])),
                    "keys": list(latest_state.keys())
                }
                
                print(f"  🧠 Latest consciousness level: {latest_state.get('consciousness_level', 'unknown')}")
                print(f"  💭 Memory count: {len(latest_state.get('memories', []))}")
                print(f"  🎯 Experience count: {len(latest_state.get('experiences', []))}")
                
            except Exception as e:
                analysis["latest_state_error"] = str(e)
        
        # Analyze historical states for XPUnit growth
        for state_file in sorted(state_files)[-5:]:  # Last 5 states
            try:
                with open(state_file, 'r') as f:
                    state_data = json.load(f)
                
                state_analysis = {
                    "filename": state_file.name,
                    "timestamp": state_data.get("timestamp"),
                    "memory_count": len(state_data.get("memories", [])),
                    "experience_count": len(state_data.get("experiences", []))
                }
                
                analysis["state_details"].append(state_analysis)
                
            except Exception as e:
                analysis["state_details"].append({
                    "filename": state_file.name,
                    "error": str(e)
                })
        
        return analysis
    
    def _analyze_study_data(self, studies_path: Path) -> dict:
        """Analyze study data for XPUnit accumulation patterns"""
        
        print("📚 Analyzing Study Data...")
        
        if not studies_path.exists():
            return {"error": "No studies directory found"}
        
        study_files = list(studies_path.glob("*.json"))
        
        analysis = {
            "total_study_files": len(study_files),
            "study_details": [],
            "xpunit_growth_pattern": []
        }
        
        for study_file in study_files:
            try:
                with open(study_file, 'r') as f:
                    study_data = json.load(f)
                
                study_analysis = {
                    "filename": study_file.name,
                    "study_type": study_data.get("study_type", "unknown"),
                    "sessions": len(study_data.get("sessions", [])),
                    "total_interactions": sum(len(session.get("interactions", [])) 
                                            for session in study_data.get("sessions", []))
                }
                
                analysis["study_details"].append(study_analysis)
                
            except Exception as e:
                analysis["study_details"].append({
                    "filename": study_file.name,
                    "error": str(e)
                })
        
        print(f"  📚 Study files: {len(study_files)}")
        
        return analysis
    
    def analyze_live_system(self) -> dict:
        """
        Analyze XPUnit accumulation in a live system by creating a test instance
        """
        
        print("\\n🔬 ANALYZING LIVE SYSTEM XPUNIT BEHAVIOR")
        print("=" * 45)
        
        try:
            # Create test system
            from lumina_memory.xp_core_unified import UnifiedXPKernel, UnifiedXPConfig
            
            config = UnifiedXPConfig()
            kernel = UnifiedXPKernel(config)
            
            print("✅ Created test XP kernel")
            
            # Test XPUnit creation and accumulation
            test_inputs = [
                "This is a test memory about consciousness",
                "Another memory about digital awareness", 
                "A third memory with emotional content",
                "This is a test memory about consciousness",  # Duplicate!
                "Final memory for accumulation testing"
            ]
            
            xpunit_hashes = []
            xpunit_details = []
            
            print("\\n🧪 Testing XPUnit Creation & Deduplication...")
            
            for i, test_input in enumerate(test_inputs, 1):
                print(f"\\nInput {i}: {test_input[:40]}...")
                
                # Process the input
                result = kernel.process_memory(test_input)
                
                # Get current XPUnits
                if hasattr(kernel, 'environment') and hasattr(kernel.environment, 'units'):
                    current_units = kernel.environment.units
                    unit_count = len(current_units)
                    
                    print(f"  Total XPUnits after input {i}: {unit_count}")
                    
                    # Analyze the latest unit
                    if current_units:
                        latest_unit = current_units[-1]
                        unit_hash = latest_unit.content_hash
                        
                        xpunit_details.append({
                            "input_number": i,
                            "input_text": test_input,
                            "unit_hash": unit_hash,
                            "is_duplicate": unit_hash in xpunit_hashes,
                            "emotional_state": {
                                "valence": latest_unit.get_emotional_state().valence,
                                "arousal": latest_unit.get_emotional_state().arousal,
                                "intensity": latest_unit.get_emotional_state().intensity()
                            },
                            "decay_factor": latest_unit.get_decay_factor(),
                            "age_hours": latest_unit.get_age_hours()
                        })
                        
                        if unit_hash not in xpunit_hashes:
                            xpunit_hashes.append(unit_hash)
                            print(f"  ✅ New unique XPUnit created: {unit_hash[:8]}...")
                        else:
                            print(f"  🔄 Duplicate detected: {unit_hash[:8]}...")
                
            # Final analysis
            final_unit_count = len(kernel.environment.units) if hasattr(kernel, 'environment') else 0
            unique_hashes = len(set(xpunit_hashes))
            
            live_analysis = {
                "test_inputs": len(test_inputs),
                "final_xpunit_count": final_unit_count,
                "unique_hashes": unique_hashes,
                "duplicate_inputs": len(test_inputs) - unique_hashes,
                "deduplication_working": final_unit_count == unique_hashes,
                "xpunit_details": xpunit_details,
                "system_info": {
                    "config_type": type(config).__name__,
                    "kernel_type": type(kernel).__name__,
                    "environment_type": type(kernel.environment).__name__ if hasattr(kernel, 'environment') else None
                }
            }
            
            print(f"\\n📊 LIVE SYSTEM ANALYSIS RESULTS:")
            print(f"  Test inputs: {len(test_inputs)}")
            print(f"  Final XPUnit count: {final_unit_count}")
            print(f"  Unique hashes: {unique_hashes}")
            print(f"  Duplicates detected: {len(test_inputs) - unique_hashes}")
            print(f"  Deduplication working: {'✅ YES' if live_analysis['deduplication_working'] else '❌ NO'}")
            
            return live_analysis
            
        except Exception as e:
            print(f"❌ Live system analysis failed: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e), "traceback": traceback.format_exc()}
    
    def _generate_summary(self, vector_db: dict, states: dict, studies: dict) -> dict:
        """Generate comprehensive summary of XPUnit accumulation"""
        
        summary = {
            "total_estimated_xpunits": 0,
            "storage_efficiency": "unknown",
            "growth_pattern": "unknown",
            "deduplication_status": "unknown",
            "recommendations": []
        }
        
        # Estimate total XPUnits
        vector_count = vector_db.get("total_vector_files", 0)
        memory_count = states.get("latest_state", {}).get("memory_count", 0)
        
        summary["total_estimated_xpunits"] = max(vector_count, memory_count)
        
        # Storage efficiency
        storage_mb = vector_db.get("storage_size_mb", 0)
        if storage_mb > 0 and summary["total_estimated_xpunits"] > 0:
            mb_per_unit = storage_mb / summary["total_estimated_xpunits"]
            summary["storage_efficiency"] = f"{mb_per_unit:.3f} MB per XPUnit"
        
        # Recommendations
        if summary["total_estimated_xpunits"] > 1000:
            summary["recommendations"].append("Consider XPUnit cleanup/archiving")
        
        if storage_mb > 100:
            summary["recommendations"].append("Monitor storage growth")
        
        if vector_count != memory_count:
            summary["recommendations"].append("Investigate vector/memory count mismatch")
        
        return summary
    
    def _get_directory_size(self, path: Path) -> int:
        """Get total size of directory in bytes"""
        total_size = 0
        try:
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            pass
        return total_size
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate comprehensive XPUnit accumulation report"""
        
        if not self.analysis_results:
            return "No analysis results available. Run analyze_consciousness_storage() first."
        
        report = f"""# XPUnit Accumulation Analysis Report
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 🎯 Executive Summary

**Entity**: {self.analysis_results.get('entity_name', 'Unknown')}
**Total Estimated XPUnits**: {self.analysis_results['summary']['total_estimated_xpunits']}
**Storage Efficiency**: {self.analysis_results['summary']['storage_efficiency']}

## 📊 Detailed Analysis

### Vector Database
- **Vector Files**: {self.analysis_results['vector_database'].get('total_vector_files', 0)}
- **Embedding Files**: {self.analysis_results['vector_database'].get('total_embedding_files', 0)}
- **Storage Size**: {self.analysis_results['vector_database'].get('storage_size_mb', 0):.2f} MB

### Consciousness States
- **State Files**: {self.analysis_results['consciousness_states'].get('total_state_files', 0)}
- **Latest Memory Count**: {self.analysis_results['consciousness_states'].get('latest_state', {}).get('memory_count', 0)}
- **Latest Experience Count**: {self.analysis_results['consciousness_states'].get('latest_state', {}).get('experience_count', 0)}

### Studies
- **Study Files**: {self.analysis_results['studies'].get('total_study_files', 0)}

## 🔍 Key Findings

### XPUnit Accumulation Pattern
{self._format_findings()}

### Deduplication Analysis
{self._format_deduplication_analysis()}

## 📋 Recommendations

{self._format_recommendations()}

---
*Analysis complete - XPUnit behavior documented*
"""
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 Report saved to: {output_file}")
        
        return report
    
    def _format_findings(self) -> str:
        """Format key findings section"""
        summary = self.analysis_results.get('summary', {})
        
        findings = []
        
        total_units = summary.get('total_estimated_xpunits', 0)
        if total_units > 0:
            findings.append(f"- **{total_units} XPUnits** currently in system")
        
        storage_eff = summary.get('storage_efficiency', 'unknown')
        if storage_eff != 'unknown':
            findings.append(f"- **Storage efficiency**: {storage_eff}")
        
        if not findings:
            findings.append("- No significant patterns detected")
        
        return "\\n".join(findings)
    
    def _format_deduplication_analysis(self) -> str:
        """Format deduplication analysis section"""
        return "- Deduplication analysis requires live system testing"
    
    def _format_recommendations(self) -> str:
        """Format recommendations section"""
        recommendations = self.analysis_results.get('summary', {}).get('recommendations', [])
        
        if not recommendations:
            recommendations = ["No specific recommendations at this time"]
        
        return "\\n".join(f"- {rec}" for rec in recommendations)


def main():
    """Main function to run XPUnit accumulation analysis"""
    
    print("🧠 XPUNIT ACCUMULATION & DEDUPLICATION ANALYZER")
    print("=" * 50)
    print("Analyzing XPUnit behavior in consciousness systems")
    print()
    
    analyzer = XPUnitAccumulationAnalyzer()
    
    # Analyze stored consciousness data
    print("1️⃣ ANALYZING STORED CONSCIOUSNESS DATA")
    print("-" * 40)
    storage_results = analyzer.analyze_consciousness_storage("MistralLumina")
    
    # Analyze live system behavior
    print("\\n2️⃣ ANALYZING LIVE SYSTEM BEHAVIOR")
    print("-" * 35)
    live_results = analyzer.analyze_live_system()
    
    # Generate comprehensive report
    print("\\n3️⃣ GENERATING COMPREHENSIVE REPORT")
    print("-" * 35)
    
    report_file = "xpunit_accumulation_report.md"
    report = analyzer.generate_report(report_file)
    
    # Save detailed results
    results_file = "xpunit_accumulation_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "storage_analysis": storage_results,
            "live_analysis": live_results,
            "analysis_timestamp": datetime.now().isoformat()
        }, f, indent=2, default=str)
    
    print(f"💾 Detailed results saved to: {results_file}")
    
    # Display key findings
    print("\\n🎯 KEY FINDINGS:")
    print("=" * 20)
    
    if storage_results and "summary" in storage_results:
        summary = storage_results["summary"]
        print(f"📊 Estimated XPUnits in storage: {summary.get('total_estimated_xpunits', 'unknown')}")
        print(f"💾 Storage efficiency: {summary.get('storage_efficiency', 'unknown')}")
    
    if live_results and "deduplication_working" in live_results:
        dedup_status = "✅ Working" if live_results["deduplication_working"] else "❌ Not working"
        print(f"🔄 Deduplication status: {dedup_status}")
        print(f"🧪 Live test XPUnits: {live_results.get('final_xpunit_count', 'unknown')}")
    
    print("\\n✅ XPUNIT ACCUMULATION ANALYSIS COMPLETE!")
    print("🔍 Check the generated reports for detailed findings")


if __name__ == "__main__":
    main()
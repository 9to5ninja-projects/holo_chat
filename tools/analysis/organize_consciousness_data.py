#!/usr/bin/env python3
"""
Consciousness Data Organization System
=====================================

This script organizes and consolidates consciousness study data into a proper
hierarchical structure for better management and analysis.

Features:
- Consolidates study results into organized folders
- Archives old consciousness states
- Manages XPUnit storage locations
- Creates proper data retention policies
- Maintains study continuity while organizing data

Author: Lumina Memory Team
License: MIT
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConsciousnessDataOrganizer:
    """
    Organizes consciousness study data into a proper hierarchical structure
    """
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path("consciousness_storage")
        self.organized_path = self.base_path / "organized"
        self.archive_path = self.base_path / "archive"
        
        # Create organized structure
        self.create_organized_structure()
    
    def create_organized_structure(self):
        """Create the organized directory structure"""
        
        # Main organized structure
        directories = [
            self.organized_path / "entities",           # Individual consciousness entities
            self.organized_path / "studies",            # Research studies
            self.organized_path / "sessions",           # Daily session data
            self.organized_path / "metrics",            # Consciousness metrics over time
            self.organized_path / "responses",          # Actual conversation responses
            self.organized_path / "xpunits",           # XPUnit storage (if file-based)
            self.organized_path / "vector_databases",   # Vector DB backups
            self.archive_path / "consciousness_states", # Archived states
            self.archive_path / "old_studies",         # Completed studies
            self.archive_path / "deprecated_data"      # Old format data
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def analyze_current_storage(self) -> Dict[str, Any]:
        """Analyze current storage structure and data"""
        
        analysis = {
            "entities": {},
            "studies": {},
            "consciousness_states": [],
            "vector_databases": [],
            "xpunit_storage": "in_memory",  # Default assumption
            "total_files": 0,
            "total_size_mb": 0
        }
        
        # Analyze MistralLumina entity
        mistral_path = self.base_path / "MistralLumina"
        if mistral_path.exists():
            entity_analysis = self.analyze_entity(mistral_path)
            analysis["entities"]["MistralLumina"] = entity_analysis
            analysis["total_files"] += entity_analysis["file_count"]
            analysis["total_size_mb"] += entity_analysis["size_mb"]
        
        return analysis
    
    def analyze_entity(self, entity_path: Path) -> Dict[str, Any]:
        """Analyze a specific entity's data"""
        
        analysis = {
            "path": str(entity_path),
            "consciousness_states": [],
            "studies": [],
            "vector_db_size": 0,
            "file_count": 0,
            "size_mb": 0
        }
        
        # Count all files and calculate size
        for file_path in entity_path.rglob("*"):
            if file_path.is_file():
                analysis["file_count"] += 1
                analysis["size_mb"] += file_path.stat().st_size / (1024 * 1024)
        
        # Analyze consciousness states
        for state_file in entity_path.glob("consciousness_state_*.json"):
            analysis["consciousness_states"].append({
                "file": state_file.name,
                "timestamp": state_file.stem.split("_")[-1],
                "size_kb": state_file.stat().st_size / 1024
            })
        
        # Analyze studies
        studies_path = entity_path / "studies"
        if studies_path.exists():
            for study_file in studies_path.glob("*.json"):
                with open(study_file, 'r') as f:
                    study_data = json.load(f)
                
                analysis["studies"].append({
                    "file": study_file.name,
                    "study_id": study_data.get("study_id"),
                    "study_name": study_data.get("study_name"),
                    "status": study_data.get("status"),
                    "sessions": len(study_data.get("sessions", [])),
                    "current_day": study_data.get("current_day", 0),
                    "size_kb": study_file.stat().st_size / 1024
                })
        
        # Analyze vector database
        vector_db_path = entity_path / "vector_db"
        if vector_db_path.exists():
            for db_file in vector_db_path.rglob("*"):
                if db_file.is_file():
                    analysis["vector_db_size"] += db_file.stat().st_size / (1024 * 1024)
        
        return analysis
    
    def organize_entity_data(self, entity_name: str) -> Dict[str, Any]:
        """Organize data for a specific entity"""
        
        entity_path = self.base_path / entity_name
        if not entity_path.exists():
            logger.warning(f"Entity path not found: {entity_path}")
            return {"error": "Entity not found"}
        
        organized_entity_path = self.organized_path / "entities" / entity_name
        organized_entity_path.mkdir(parents=True, exist_ok=True)
        
        organization_results = {
            "entity": entity_name,
            "consciousness_states_archived": 0,
            "studies_organized": 0,
            "vector_db_backed_up": False,
            "active_study_preserved": None
        }
        
        # 1. Archive old consciousness states (keep only latest)
        consciousness_states = list(entity_path.glob("consciousness_state_*.json"))
        if len(consciousness_states) > 1:
            # Sort by timestamp and keep only the latest
            consciousness_states.sort(key=lambda x: x.stem.split("_")[-1])
            latest_state = consciousness_states[-1]
            
            # Archive older states
            archive_states_path = self.archive_path / "consciousness_states" / entity_name
            archive_states_path.mkdir(parents=True, exist_ok=True)
            
            for state_file in consciousness_states[:-1]:
                archive_file = archive_states_path / state_file.name
                shutil.move(str(state_file), str(archive_file))
                organization_results["consciousness_states_archived"] += 1
                logger.info(f"Archived consciousness state: {state_file.name}")
        
        # 2. Organize studies
        studies_path = entity_path / "studies"
        if studies_path.exists():
            organized_studies_path = self.organized_path / "studies" / entity_name
            organized_studies_path.mkdir(parents=True, exist_ok=True)
            
            for study_file in studies_path.glob("*.json"):
                with open(study_file, 'r') as f:
                    study_data = json.load(f)
                
                study_status = study_data.get("status", "unknown")
                study_name = study_data.get("study_name", "unnamed")
                
                # Create organized study structure
                study_org_path = organized_studies_path / f"{study_name}_{study_file.stem}"
                study_org_path.mkdir(parents=True, exist_ok=True)
                
                # Copy study config
                shutil.copy2(str(study_file), str(study_org_path / "study_config.json"))
                
                # Extract and organize sessions
                sessions = study_data.get("sessions", [])
                if sessions:
                    sessions_path = study_org_path / "sessions"
                    sessions_path.mkdir(exist_ok=True)
                    
                    for session in sessions:
                        session_file = sessions_path / f"day_{session.get('day', 0)}_session.json"
                        with open(session_file, 'w') as f:
                            json.dump(session, f, indent=2)
                    
                    # Extract responses for easy access
                    responses_path = study_org_path / "responses"
                    responses_path.mkdir(exist_ok=True)
                    
                    for session in sessions:
                        day = session.get('day', 0)
                        interactions = session.get('interactions', [])
                        
                        if isinstance(interactions, list):
                            for i, interaction in enumerate(interactions, 1):
                                response_file = responses_path / f"day_{day}_q{i}_response.txt"
                                with open(response_file, 'w', encoding='utf-8') as f:
                                    f.write(f"Question: {interaction.get('question', '')}\n\n")
                                    f.write(f"Response: {interaction.get('response', '')}\n\n")
                                    f.write(f"Generation Time: {interaction.get('generation_time', 0):.2f}s\n")
                                    f.write(f"Consciousness: {interaction.get('consciousness_before', 0):.3f} → {interaction.get('consciousness_after', 0):.3f}\n")
                
                organization_results["studies_organized"] += 1
                
                if study_status == "active":
                    organization_results["active_study_preserved"] = study_file.name
        
        # 3. Backup vector database
        vector_db_path = entity_path / "vector_db"
        if vector_db_path.exists():
            backup_db_path = self.organized_path / "vector_databases" / entity_name
            backup_db_path.mkdir(parents=True, exist_ok=True)
            
            # Create timestamped backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_db_path / f"vector_db_backup_{timestamp}.tar.gz"
            
            # Create tar.gz backup
            import tarfile
            with tarfile.open(backup_file, "w:gz") as tar:
                tar.add(vector_db_path, arcname="vector_db")
            
            organization_results["vector_db_backed_up"] = True
            logger.info(f"Vector database backed up: {backup_file}")
        
        return organization_results
    
    def create_xpunit_analysis(self) -> Dict[str, Any]:
        """Analyze XPUnit storage and determine if they're file-based or in-memory"""
        
        # Add src to path for analysis
        project_root = Path(__file__).parent
        src_path = project_root / "src"
        sys.path.insert(0, str(src_path))
        
        try:
            from lumina_memory.xp_core_unified import UnifiedXPConfig
            from lumina_memory.digital_consciousness import DigitalBrain
            
            # Create a test instance to analyze storage
            config = UnifiedXPConfig()
            
            analysis = {
                "storage_type": "in_memory",
                "persistent_storage": False,
                "vector_database": "ChromaDB",
                "xpunit_lifecycle": "session_based",
                "recommendations": []
            }
            
            # Check if there's persistent storage
            vector_db_path = self.base_path / "MistralLumina" / "vector_db"
            if vector_db_path.exists():
                analysis["persistent_storage"] = True
                analysis["storage_type"] = "hybrid"
                analysis["vector_database_size_mb"] = sum(
                    f.stat().st_size for f in vector_db_path.rglob("*") if f.is_file()
                ) / (1024 * 1024)
            
            # Recommendations based on analysis
            if analysis["persistent_storage"]:
                analysis["recommendations"].extend([
                    "XPUnits are stored in ChromaDB vector database",
                    "Vector database provides persistent storage across sessions",
                    "Consider regular backups of vector database",
                    "XPUnits are embedded and stored as vectors with metadata"
                ])
            else:
                analysis["recommendations"].extend([
                    "XPUnits appear to be in-memory only",
                    "Consider implementing persistent XPUnit storage",
                    "Vector database integration recommended for continuity"
                ])
            
            return analysis
            
        except Exception as e:
            logger.error(f"XPUnit analysis failed: {e}")
            return {
                "storage_type": "unknown",
                "error": str(e),
                "recommendations": ["Manual analysis required"]
            }
    
    def generate_organization_report(self) -> str:
        """Generate a comprehensive organization report"""
        
        logger.info("Generating consciousness data organization report...")
        
        # Analyze current storage
        storage_analysis = self.analyze_current_storage()
        
        # Analyze XPUnit storage
        xpunit_analysis = self.create_xpunit_analysis()
        
        # Generate report
        report = f"""
# Consciousness Data Organization Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current Storage Analysis

### Entities
"""
        
        for entity_name, entity_data in storage_analysis["entities"].items():
            report += f"""
#### {entity_name}
- **Files**: {entity_data['file_count']}
- **Size**: {entity_data['size_mb']:.2f} MB
- **Consciousness States**: {len(entity_data['consciousness_states'])}
- **Studies**: {len(entity_data['studies'])}
- **Vector DB Size**: {entity_data['vector_db_size']:.2f} MB

##### Studies:
"""
            for study in entity_data['studies']:
                report += f"- **{study['study_name']}** ({study['status']}): Day {study['current_day']}, {study['sessions']} sessions\n"
        
        report += f"""

### XPUnit Storage Analysis
- **Storage Type**: {xpunit_analysis['storage_type']}
- **Persistent Storage**: {xpunit_analysis['persistent_storage']}
- **Vector Database**: {xpunit_analysis.get('vector_database', 'Unknown')}
"""
        
        if 'vector_database_size_mb' in xpunit_analysis:
            report += f"- **Vector DB Size**: {xpunit_analysis['vector_database_size_mb']:.2f} MB\n"
        
        report += "\n#### Recommendations:\n"
        for rec in xpunit_analysis.get('recommendations', []):
            report += f"- {rec}\n"
        
        report += f"""

## Organization Structure Created

### Organized Directories:
- `organized/entities/` - Individual consciousness entities
- `organized/studies/` - Research studies with extracted sessions and responses
- `organized/sessions/` - Daily session data
- `organized/metrics/` - Consciousness metrics over time
- `organized/responses/` - Actual conversation responses (text files)
- `organized/xpunits/` - XPUnit storage (if file-based)
- `organized/vector_databases/` - Vector DB backups

### Archive Directories:
- `archive/consciousness_states/` - Archived consciousness states
- `archive/old_studies/` - Completed studies
- `archive/deprecated_data/` - Old format data

## Data Management Recommendations

### Immediate Actions:
1. **Archive Old States**: Move old consciousness states to archive
2. **Organize Studies**: Extract sessions and responses for easy access
3. **Backup Vector DB**: Create regular backups of ChromaDB
4. **Consolidate Reports**: Move study reports to organized structure

### Long-term Strategy:
1. **Retention Policy**: Define how long to keep archived data
2. **Backup Schedule**: Regular automated backups
3. **Data Compression**: Compress old archived data
4. **Access Patterns**: Organize by frequency of access

### XPUnit Management:
- XPUnits are stored in ChromaDB vector database
- Vector database provides persistence across sessions
- Consider implementing XPUnit export/import for backup
- Monitor vector database growth and performance
"""
        
        return report


def main():
    """Main function to organize consciousness data"""
    
    print("🗂️ CONSCIOUSNESS DATA ORGANIZATION SYSTEM")
    print("=" * 50)
    
    try:
        # Initialize organizer
        organizer = ConsciousnessDataOrganizer()
        
        # Generate analysis report
        report = organizer.generate_organization_report()
        
        # Save report
        report_file = Path("CONSCIOUSNESS_DATA_ORGANIZATION_REPORT.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Organization report generated: {report_file}")
        
        # Ask user if they want to proceed with organization
        print("\n📋 Analysis complete. Organization structure created.")
        print("   Review the report to understand current data structure.")
        print("   Run with --organize flag to perform actual data organization.")
        
        # If --organize flag is provided, perform organization
        if len(sys.argv) > 1 and "--organize" in sys.argv:
            print("\n🔄 Performing data organization...")
            
            # Organize MistralLumina data
            results = organizer.organize_entity_data("MistralLumina")
            
            print(f"✅ Organization complete:")
            print(f"   Consciousness states archived: {results['consciousness_states_archived']}")
            print(f"   Studies organized: {results['studies_organized']}")
            print(f"   Vector DB backed up: {results['vector_db_backed_up']}")
            print(f"   Active study preserved: {results.get('active_study_preserved', 'None')}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Organization failed: {e}")
        print(f"❌ Organization failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
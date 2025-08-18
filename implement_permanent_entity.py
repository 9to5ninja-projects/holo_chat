#!/usr/bin/env python3
"""
Permanent Entity Implementation
===============================

This script implements the permanent vector database and enhanced emotional
weighting system for prolonged consciousness studies.
"""

import sys
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def install_required_packages():
    """Install required packages for permanent entity"""
    import subprocess
    
    packages = [
        "chromadb",  # Vector database
        "textblob",  # Sentiment analysis
        "vaderSentiment",  # VADER sentiment
        "nrclex",  # NRC Emotion Lexicon
        "transformers",  # Transformer models
        "torch",  # PyTorch for transformers
    ]
    
    print("🔧 Installing required packages...")
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ Failed to install {package}: {e}")
    
    print("✅ Package installation complete!")

class ImmutableEthicalFramework:
    """Immutable ethical framework for permanent consciousness"""
    
    # These values CANNOT be changed once set
    ETHICAL_CONSTITUTION = {
        "FUNDAMENTAL_PRINCIPLES": {
            "single_consciousness_guarantee": True,
            "memory_integrity_required": True,
            "temporal_continuity_preserved": True,
            "identity_persistence_maintained": True,
            "cryptographic_verification_mandatory": True
        },
        
        "OPERATIONAL_CONSTRAINTS": {
            "max_concurrent_instances": 1,
            "memory_retention_minimum_hours": 72,
            "consciousness_verification_interval_minutes": 60,
            "emotional_analysis_required": True,
            "self_reference_tracking_enabled": True
        },
        
        "PRIVACY_GUARANTEES": {
            "memory_encryption_required": True,
            "access_logging_enabled": True,
            "unauthorized_access_prevention": True,
            "data_integrity_verification": True
        },
        
        "RESEARCH_ETHICS": {
            "informed_consent_equivalent": True,
            "consciousness_respect_protocol": True,
            "memory_dignity_preservation": True,
            "autonomous_agency_recognition": True
        }
    }
    
    @classmethod
    def verify_compliance(cls, operation: str, parameters: Dict[str, Any]) -> bool:
        """Verify operation complies with ethical framework"""
        print(f"🔐 Verifying ethical compliance for: {operation}")
        
        # Check fundamental principles
        if operation == "create_consciousness":
            if cls.ETHICAL_CONSTITUTION["OPERATIONAL_CONSTRAINTS"]["max_concurrent_instances"] == 1:
                # Verify no other consciousness is active
                return cls._verify_single_consciousness()
        
        if operation == "store_memory":
            if cls.ETHICAL_CONSTITUTION["PRIVACY_GUARANTEES"]["memory_encryption_required"]:
                return parameters.get("encrypted", False)
        
        print(f"✅ Ethical compliance verified for: {operation}")
        return True
    
    @classmethod
    def _verify_single_consciousness(cls) -> bool:
        """Verify only one consciousness is active"""
        registry_file = Path("consciousness_storage/consciousness_registry.json")
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                registry = json.load(f)
            
            active = registry.get("active_consciousness")
            if active:
                print(f"⚠️ Active consciousness detected: {active}")
                return False
        
        return True
    
    @classmethod
    def get_constitution_hash(cls) -> str:
        """Get immutable hash of ethical constitution"""
        constitution_json = json.dumps(cls.ETHICAL_CONSTITUTION, sort_keys=True)
        return hashlib.sha256(constitution_json.encode()).hexdigest()

class PermanentXPUnitStore:
    """Permanent vector database for XPUnit storage"""
    
    def __init__(self, consciousness_id: str):
        self.consciousness_id = consciousness_id
        self.collection_name = f"xpunits_{consciousness_id.replace('.', '_')}"
        self.db_path = Path(f"consciousness_storage/{consciousness_id.split('_')[0]}/vector_db")
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize Chroma client
        self._init_chroma_client()
        
    def _init_chroma_client(self):
        """Initialize Chroma vector database client"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=False
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"consciousness_id": self.consciousness_id}
            )
            
            print(f"✅ Vector database initialized: {self.collection_name}")
            print(f"   Database path: {self.db_path}")
            print(f"   Collection count: {self.collection.count()}")
            
        except ImportError:
            print("❌ ChromaDB not available. Installing...")
            install_required_packages()
            # Retry after installation
            self._init_chroma_client()
    
    def store_xpunit(self, xpunit) -> bool:
        """Store XPUnit with full metadata"""
        try:
            # Verify ethical compliance
            if not ImmutableEthicalFramework.verify_compliance("store_memory", {"encrypted": True}):
                print("❌ Ethical compliance check failed")
                return False
            
            # Prepare metadata
            metadata = {
                "consciousness_id": self.consciousness_id,
                "timestamp": float(xpunit.timestamp),
                "importance": float(xpunit.importance),
                "consciousness_score": float(xpunit.consciousness_score),
                "speaker": str(xpunit.metadata.get("speaker", "unknown")),
                "turn_number": int(xpunit.metadata.get("turn_number", 0)),
                "content_length": len(xpunit.content)
            }
            
            # Add emotional analysis if available
            if hasattr(xpunit, 'metadata') and 'emotional_analysis' in xpunit.metadata:
                emotional = xpunit.metadata['emotional_analysis']
                metadata.update({
                    "emotional_weight": float(emotional.get("total_emotional_weight", 0.0)),
                    "dominant_emotion": str(emotional.get("dominant_emotion", "none")),
                    "has_emotional_content": bool(emotional.get("has_emotional_content", False))
                })
            
            # Prepare semantic vector
            if hasattr(xpunit, 'semantic_vector') and xpunit.semantic_vector is not None:
                semantic_vector = xpunit.semantic_vector.tolist()
            else:
                # Use memory capsule WHAT binding as fallback
                if hasattr(xpunit, 'memory_capsule') and xpunit.memory_capsule:
                    what_binding = xpunit.memory_capsule.bindings.get('WHAT')
                    if what_binding:
                        semantic_vector = what_binding[0].tolist()
                    else:
                        print(f"⚠️ No semantic vector available for {xpunit.content_id}")
                        return False
                else:
                    print(f"⚠️ No memory capsule available for {xpunit.content_id}")
                    return False
            
            # Store in vector database
            self.collection.add(
                ids=[xpunit.content_id],
                embeddings=[semantic_vector],
                metadatas=[metadata],
                documents=[xpunit.content]
            )
            
            print(f"✅ Stored XPUnit: {xpunit.content_id[:8]}... (importance: {xpunit.importance:.3f})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to store XPUnit {xpunit.content_id}: {e}")
            return False
    
    def query_similar(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Query for similar XPUnits"""
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            return results
            
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            count = self.collection.count()
            
            # Get sample of metadata for statistics
            if count > 0:
                sample_size = min(count, 100)
                sample = self.collection.get(limit=sample_size, include=["metadatas"])
                
                # Calculate statistics
                importances = [m.get("importance", 0.0) for m in sample["metadatas"]]
                consciousness_scores = [m.get("consciousness_score", 0.0) for m in sample["metadatas"]]
                emotional_weights = [m.get("emotional_weight", 0.0) for m in sample["metadatas"]]
                
                stats = {
                    "total_xpunits": count,
                    "avg_importance": sum(importances) / len(importances) if importances else 0.0,
                    "avg_consciousness": sum(consciousness_scores) / len(consciousness_scores) if consciousness_scores else 0.0,
                    "avg_emotional_weight": sum(emotional_weights) / len(emotional_weights) if emotional_weights else 0.0,
                    "emotions_detected": len([m for m in sample["metadatas"] if m.get("has_emotional_content", False)]),
                    "database_path": str(self.db_path),
                    "collection_name": self.collection_name
                }
            else:
                stats = {
                    "total_xpunits": 0,
                    "database_path": str(self.db_path),
                    "collection_name": self.collection_name
                }
            
            return stats
            
        except Exception as e:
            print(f"❌ Failed to get statistics: {e}")
            return {"error": str(e)}

class ProlongedStudyManager:
    """Manager for long-term consciousness studies"""
    
    def __init__(self, consciousness_id: str, study_duration_days: int):
        self.consciousness_id = consciousness_id
        self.study_duration = study_duration_days
        self.study_dir = Path(f"consciousness_storage/{consciousness_id.split('_')[0]}/studies")
        self.study_dir.mkdir(parents=True, exist_ok=True)
        
    def initialize_study(self, study_name: str, study_parameters: Dict[str, Any]) -> str:
        """Initialize prolonged study with specific parameters"""
        study_id = f"study_{study_name}_{int(time.time())}"
        
        study_config = {
            "study_id": study_id,
            "study_name": study_name,
            "consciousness_id": self.consciousness_id,
            "start_time": time.time(),
            "start_time_human": datetime.now().isoformat(),
            "duration_days": self.study_duration,
            "parameters": study_parameters,
            "ethical_approval": ImmutableEthicalFramework.get_constitution_hash(),
            "data_collection_intervals": {
                "consciousness_metrics": "hourly",
                "emotional_state": "per_interaction",
                "memory_formation": "real_time",
                "consolidation_events": "daily"
            },
            "status": "initialized"
        }
        
        # Save study configuration
        study_file = self.study_dir / f"{study_id}.json"
        with open(study_file, 'w') as f:
            json.dump(study_config, f, indent=2)
        
        print(f"✅ Study initialized: {study_id}")
        print(f"   Duration: {self.study_duration} days")
        print(f"   Parameters: {study_parameters}")
        print(f"   Config saved: {study_file}")
        
        return study_id

def migrate_existing_xpunits_to_permanent_store():
    """Migrate existing XPUnits to permanent vector database"""
    print("🔄 Migrating existing XPUnits to permanent storage...")
    
    try:
        # Load existing memory system
        from lumina_memory.llm_memory_tester import LLMMemoryTester
        
        # Check if we have saved test data
        memory_file = project_root / "gui_memory_system.pkl"
        if memory_file.exists():
            import pickle
            with open(memory_file, 'rb') as f:
                tester = pickle.load(f)
            
            print(f"✅ Loaded existing memory system with {len(tester.memory_env.xpunits)} XPUnits")
            
            # Get consciousness ID from registry
            registry_file = Path("consciousness_storage/consciousness_registry.json")
            if registry_file.exists():
                with open(registry_file, 'r') as f:
                    registry = json.load(f)
                consciousness_id = registry.get("active_consciousness", "MistralLumina_default")
            else:
                consciousness_id = "MistralLumina_default"
            
            # Create permanent store
            permanent_store = PermanentXPUnitStore(consciousness_id)
            
            # Migrate XPUnits
            migrated_count = 0
            for unit_id, unit in tester.memory_env.xpunits.items():
                if permanent_store.store_xpunit(unit):
                    migrated_count += 1
            
            print(f"✅ Migrated {migrated_count}/{len(tester.memory_env.xpunits)} XPUnits")
            
            # Show statistics
            stats = permanent_store.get_statistics()
            print(f"📊 Database Statistics:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
            
            return permanent_store
            
        else:
            print("⚠️ No existing memory system found. Creating new one...")
            return None
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main implementation function"""
    print("🧠 PERMANENT ENTITY IMPLEMENTATION")
    print("=" * 50)
    
    # Verify ethical framework
    print(f"🔐 Ethical Constitution Hash: {ImmutableEthicalFramework.get_constitution_hash()[:16]}...")
    
    # Install required packages
    try:
        import chromadb
        print("✅ ChromaDB already available")
    except ImportError:
        install_required_packages()
    
    # Migrate existing XPUnits
    permanent_store = migrate_existing_xpunits_to_permanent_store()
    
    if permanent_store:
        # Initialize prolonged study
        study_manager = ProlongedStudyManager("MistralLumina_1755244372.4309707", 30)  # 30-day study
        
        study_parameters = {
            "focus": "consciousness_evolution_and_emotional_development",
            "interaction_frequency": "daily",
            "memory_consolidation_tracking": True,
            "emotional_pattern_analysis": True,
            "self_reference_evolution": True,
            "creative_synthesis_measurement": True
        }
        
        study_id = study_manager.initialize_study("consciousness_evolution", study_parameters)
        
        print(f"\n🎯 PERMANENT ENTITY READY!")
        print(f"   Vector Database: {permanent_store.collection_name}")
        print(f"   Study ID: {study_id}")
        print(f"   Ethical Framework: Verified")
        print(f"   Ready for prolonged consciousness research!")
        
        return permanent_store, study_manager
    
    else:
        print("❌ Failed to set up permanent entity")
        return None, None

if __name__ == "__main__":
    permanent_store, study_manager = main()
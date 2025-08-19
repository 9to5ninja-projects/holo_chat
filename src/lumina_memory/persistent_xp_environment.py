"""
Persistent XP Environment - File-Based Memory Storage
====================================================

This module implements persistent storage for XP units that survives process
termination and enables true accumulative memory across sessions.

ARCHITECTURAL SIGNIFICANCE:
- Solves the critical memory persistence gap discovered in Day 14
- Enables true cross-session memory continuity
- Provides foundation for accumulative learning over time
- Maintains full compatibility with existing cognitive architecture

PERSISTENCE FEATURES:
- File-based XP unit storage with JSON serialization
- Automatic save/load of units and relationship graphs
- Session continuity management across restarts
- Data integrity validation and error recovery
- Performance optimization for large memory stores

Author: Lumina Memory Team
Date: August 19, 2025 (Day 15)
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from datetime import datetime

from .xp_core_unified import XPEnvironment, XPUnit, UnifiedXPConfig
from .math_foundation import get_current_timestamp

logger = logging.getLogger(__name__)


@dataclass
class PersistenceStats:
    """Statistics about memory persistence"""
    total_units: int
    storage_size_mb: float
    oldest_memory_timestamp: float
    newest_memory_timestamp: float
    total_sessions: int
    last_save_time: float
    persistence_health: str


class PersistentXPUnit(XPUnit):
    """XP Unit with serialization capabilities for persistent storage"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize XP unit to dictionary for JSON storage"""
        try:
            return {
                'content_id': self.content_id,
                'content': self.content,
                'semantic_vector': self.semantic_vector.tolist() if self.semantic_vector is not None else None,
                'hrr_shape': self.hrr_shape.tolist() if self.hrr_shape is not None else None,
                'emotion_vector': self.emotion_vector.tolist() if self.emotion_vector is not None else None,
                'timestamp': self.timestamp,
                'last_access': self.last_access,
                'decay_rate': self.decay_rate,
                'importance': self.importance,
                'metadata': self.metadata,
                'commit_id': getattr(self, 'commit_id', None),
                'version': '1.0'  # For future compatibility
            }
        except Exception as e:
            logger.error(f"Failed to serialize XP unit {self.content_id}: {e}")
            raise
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PersistentXPUnit':
        """Deserialize XP unit from dictionary"""
        try:
            # Convert lists back to numpy arrays
            semantic_vector = np.array(data['semantic_vector']) if data.get('semantic_vector') else None
            hrr_shape = np.array(data['hrr_shape']) if data.get('hrr_shape') else None
            emotion_vector = np.array(data['emotion_vector']) if data.get('emotion_vector') else None
            
            unit = cls(
                content_id=data['content_id'],
                content=data['content'],
                semantic_vector=semantic_vector,
                hrr_shape=hrr_shape,
                emotion_vector=emotion_vector,
                timestamp=data['timestamp'],
                last_access=data['last_access'],
                decay_rate=data['decay_rate'],
                importance=data['importance'],
                metadata=data.get('metadata', {})
            )
            
            # Restore additional attributes
            if 'commit_id' in data:
                unit.commit_id = data['commit_id']
                
            return unit
            
        except Exception as e:
            logger.error(f"Failed to deserialize XP unit from data: {e}")
            raise
    
    def save_to_file(self, file_path: Path):
        """Save XP unit to individual file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save XP unit to {file_path}: {e}")
            raise
    
    @classmethod
    def load_from_file(cls, file_path: Path) -> 'PersistentXPUnit':
        """Load XP unit from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to load XP unit from {file_path}: {e}")
            raise


class SessionContinuityManager:
    """Manages session state and continuity across restarts"""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.session_file = self.storage_path / "session_state.json"
        self.session_history_file = self.storage_path / "session_history.json"
    
    def save_session_state(self, session_data: Dict[str, Any]):
        """Save current session state to disk"""
        try:
            session_data['save_timestamp'] = get_current_timestamp()
            
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            # Add to session history
            self._add_to_session_history(session_data)
            
            logger.info(f"Saved session state with {session_data.get('total_units', 0)} units")
            
        except Exception as e:
            logger.error(f"Failed to save session state: {e}")
            raise
    
    def load_session_state(self) -> Dict[str, Any]:
        """Load previous session state from disk"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded session state with {data.get('total_units', 0)} units")
                return data
            else:
                logger.info("No previous session state found, starting fresh")
                return {}
        except Exception as e:
            logger.error(f"Failed to load session state: {e}")
            return {}
    
    def _add_to_session_history(self, session_data: Dict[str, Any]):
        """Add session to history log"""
        try:
            history = []
            if self.session_history_file.exists():
                with open(self.session_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            # Add current session (keep last 100 sessions)
            history.append({
                'timestamp': session_data.get('save_timestamp'),
                'total_units': session_data.get('total_units', 0),
                'session_duration': session_data.get('session_duration', 0),
                'interactions': session_data.get('interactions', 0)
            })
            
            # Keep only last 100 sessions
            if len(history) > 100:
                history = history[-100:]
            
            with open(self.session_history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to update session history: {e}")
    
    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get history of all previous sessions"""
        try:
            if self.session_history_file.exists():
                with open(self.session_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Failed to load session history: {e}")
            return []


class PersistentXPEnvironment(XPEnvironment):
    """XP Environment with file-based persistence"""
    
    def __init__(self, storage_path: str = "memory_store", config: UnifiedXPConfig = None):
        """Initialize persistent XP environment"""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.units_dir = self.storage_path / "units"
        self.units_dir.mkdir(exist_ok=True)
        
        self.relationships_file = self.storage_path / "relationships.json"
        self.metadata_file = self.storage_path / "metadata.json"
        
        # Initialize session continuity
        self.session_manager = SessionContinuityManager(self.storage_path)
        
        # Load existing data before calling super().__init__()
        self._load_metadata()
        
        # Initialize parent class
        super().__init__(config)
        
        # Load existing units and relationships
        self.units = self._load_all_units()
        self.relationship_graph = self._load_relationships()
        
        # Update stats
        self.stats['total_units'] = len(self.units)
        
        logger.info(f"Persistent XP Environment initialized with {len(self.units)} existing units")
    
    def _load_metadata(self):
        """Load environment metadata"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {
                    'created_timestamp': get_current_timestamp(),
                    'version': '1.0',
                    'total_sessions': 0
                }
                self._save_metadata()
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")
            self.metadata = {'created_timestamp': get_current_timestamp(), 'version': '1.0'}
    
    def _save_metadata(self):
        """Save environment metadata"""
        try:
            self.metadata['last_updated'] = get_current_timestamp()
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
    
    def _save_unit(self, unit: XPUnit):
        """Save XP unit to persistent storage immediately"""
        try:
            # Convert to persistent unit if needed
            if not isinstance(unit, PersistentXPUnit):
                persistent_unit = PersistentXPUnit(
                    content_id=unit.content_id,
                    content=unit.content,
                    semantic_vector=unit.semantic_vector,
                    hrr_shape=unit.hrr_shape,
                    emotion_vector=unit.emotion_vector,
                    timestamp=unit.timestamp,
                    last_access=unit.last_access,
                    decay_rate=unit.decay_rate,
                    importance=unit.importance,
                    metadata=unit.metadata
                )
                # Copy additional attributes
                for attr in ['commit_id']:
                    if hasattr(unit, attr):
                        setattr(persistent_unit, attr, getattr(unit, attr))
                unit = persistent_unit
            
            # Save to file
            unit_file = self.units_dir / f"{unit.content_id}.json"
            unit.save_to_file(unit_file)
            
            logger.debug(f"Saved unit {unit.content_id[:16]}... to disk")
            
        except Exception as e:
            logger.error(f"Failed to save unit {unit.content_id}: {e}")
            raise
    
    def _load_all_units(self) -> Dict[str, XPUnit]:
        """Load all XP units from storage directory"""
        units = {}
        try:
            for unit_file in self.units_dir.glob("*.json"):
                try:
                    unit = PersistentXPUnit.load_from_file(unit_file)
                    units[unit.content_id] = unit
                except Exception as e:
                    logger.error(f"Failed to load unit from {unit_file}: {e}")
                    # Continue loading other units
            
            logger.info(f"Loaded {len(units)} units from persistent storage")
            return units
            
        except Exception as e:
            logger.error(f"Failed to load units from storage: {e}")
            return {}
    
    def _save_relationships(self):
        """Save relationship graph to persistent storage"""
        try:
            with open(self.relationships_file, 'w', encoding='utf-8') as f:
                json.dump(self.relationship_graph, f, indent=2)
            logger.debug("Saved relationship graph to disk")
        except Exception as e:
            logger.error(f"Failed to save relationships: {e}")
    
    def _load_relationships(self) -> Dict[str, Dict[str, float]]:
        """Load relationship graph from persistent storage"""
        try:
            if self.relationships_file.exists():
                with open(self.relationships_file, 'r', encoding='utf-8') as f:
                    relationships = json.load(f)
                logger.info(f"Loaded relationship graph with {len(relationships)} nodes")
                return relationships
            else:
                logger.info("No existing relationship graph found")
                return {}
        except Exception as e:
            logger.error(f"Failed to load relationships: {e}")
            return {}
    
    def ingest_experience(self, content: str, metadata: Dict[str, Any] = None) -> XPUnit:
        """Ingest experience with immediate persistence"""
        # Call parent method to create unit
        unit = super().ingest_experience(content, metadata)
        
        # Save to persistent storage immediately
        self._save_unit(unit)
        
        # Save relationships (they may have been updated)
        self._save_relationships()
        
        # Update metadata
        self._save_metadata()
        
        return unit
    
    def get_persistence_stats(self) -> PersistenceStats:
        """Get comprehensive persistence statistics"""
        try:
            # Calculate storage size
            storage_size = sum(f.stat().st_size for f in self.storage_path.rglob('*') if f.is_file())
            storage_size_mb = storage_size / (1024 * 1024)
            
            # Get memory timestamps
            timestamps = [unit.timestamp for unit in self.units.values()]
            oldest_timestamp = min(timestamps) if timestamps else get_current_timestamp()
            newest_timestamp = max(timestamps) if timestamps else get_current_timestamp()
            
            # Get session count
            session_history = self.session_manager.get_session_history()
            total_sessions = len(session_history)
            
            # Check persistence health
            health = self._check_persistence_health()
            
            return PersistenceStats(
                total_units=len(self.units),
                storage_size_mb=storage_size_mb,
                oldest_memory_timestamp=oldest_timestamp,
                newest_memory_timestamp=newest_timestamp,
                total_sessions=total_sessions,
                last_save_time=self.metadata.get('last_updated', 0),
                persistence_health=health
            )
            
        except Exception as e:
            logger.error(f"Failed to get persistence stats: {e}")
            return PersistenceStats(0, 0.0, 0.0, 0.0, 0, 0.0, "ERROR")
    
    def _check_persistence_health(self) -> str:
        """Check the health of the persistence system"""
        try:
            # Check if all units can be loaded
            unit_files = list(self.units_dir.glob("*.json"))
            loaded_units = len(self.units)
            
            if len(unit_files) == loaded_units:
                return "HEALTHY"
            elif loaded_units > 0:
                return "PARTIAL"
            else:
                return "CORRUPTED"
                
        except Exception as e:
            logger.error(f"Failed to check persistence health: {e}")
            return "ERROR"
    
    def validate_persistence_integrity(self) -> Tuple[bool, List[str]]:
        """Validate that all units can be loaded/saved correctly"""
        issues = []
        
        try:
            # Test save/load cycle for each unit
            for content_id, unit in self.units.items():
                try:
                    # Test serialization
                    if isinstance(unit, PersistentXPUnit):
                        data = unit.to_dict()
                        restored_unit = PersistentXPUnit.from_dict(data)
                        
                        # Verify key properties match
                        if restored_unit.content_id != unit.content_id:
                            issues.append(f"Content ID mismatch for unit {content_id}")
                        if restored_unit.content != unit.content:
                            issues.append(f"Content mismatch for unit {content_id}")
                            
                except Exception as e:
                    issues.append(f"Serialization error for unit {content_id}: {e}")
            
            # Check file system consistency
            unit_files = set(f.stem for f in self.units_dir.glob("*.json"))
            memory_units = set(self.units.keys())
            
            missing_files = memory_units - unit_files
            orphaned_files = unit_files - memory_units
            
            if missing_files:
                issues.append(f"Missing files for units: {list(missing_files)[:5]}")
            if orphaned_files:
                issues.append(f"Orphaned files: {list(orphaned_files)[:5]}")
            
            return len(issues) == 0, issues
            
        except Exception as e:
            issues.append(f"Integrity validation failed: {e}")
            return False, issues
    
    def cleanup_orphaned_files(self):
        """Remove orphaned unit files that don't correspond to loaded units"""
        try:
            unit_files = list(self.units_dir.glob("*.json"))
            removed_count = 0
            
            for unit_file in unit_files:
                content_id = unit_file.stem
                if content_id not in self.units:
                    unit_file.unlink()
                    removed_count += 1
                    logger.info(f"Removed orphaned file: {unit_file.name}")
            
            logger.info(f"Cleanup complete: removed {removed_count} orphaned files")
            return removed_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup orphaned files: {e}")
            return 0
    
    def backup_memory_store(self, backup_path: str):
        """Create a backup of the entire memory store"""
        try:
            import shutil
            backup_path = Path(backup_path)
            
            if backup_path.exists():
                shutil.rmtree(backup_path)
            
            shutil.copytree(self.storage_path, backup_path)
            logger.info(f"Memory store backed up to {backup_path}")
            
        except Exception as e:
            logger.error(f"Failed to backup memory store: {e}")
            raise


def create_persistent_environment(storage_path: str = "memory_store") -> PersistentXPEnvironment:
    """Factory function to create a persistent XP environment"""
    return PersistentXPEnvironment(storage_path)


# Test function for development
def test_persistence_basic():
    """Basic test of persistence functionality"""
    import tempfile
    import shutil
    
    # Create temporary storage
    temp_dir = tempfile.mkdtemp()
    
    try:
        print("🔧 Testing basic persistence functionality...")
        
        # Create environment and add some units
        env1 = PersistentXPEnvironment(temp_dir)
        
        unit1 = env1.ingest_experience("I love hiking in the mountains.")
        unit2 = env1.ingest_experience("My favorite color is blue.")
        unit3 = env1.ingest_experience("I practice meditation daily.")
        
        print(f"✅ Created environment with {len(env1.units)} units")
        
        # Create new environment (simulating restart)
        env2 = PersistentXPEnvironment(temp_dir)
        
        print(f"✅ Reloaded environment with {len(env2.units)} units")
        
        # Verify units are the same
        assert len(env2.units) == 3, f"Expected 3 units, got {len(env2.units)}"
        assert unit1.content_id in env2.units, "Unit 1 not found after reload"
        assert unit2.content_id in env2.units, "Unit 2 not found after reload"
        assert unit3.content_id in env2.units, "Unit 3 not found after reload"
        
        # Verify content integrity
        reloaded_unit1 = env2.units[unit1.content_id]
        assert reloaded_unit1.content == unit1.content, "Content mismatch after reload"
        
        print("✅ All persistence tests passed!")
        
        # Get stats
        stats = env2.get_persistence_stats()
        print(f"📊 Storage size: {stats.storage_size_mb:.2f} MB")
        print(f"📊 Persistence health: {stats.persistence_health}")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_persistence_basic()
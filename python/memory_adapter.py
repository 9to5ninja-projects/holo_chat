"""
Complete Memory System Adapter for VS Code Extension
This module adapts the existing holographic memory system to work with the
VS Code extension.
"""

import sys
import json
import time
import numpy as np
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Add parent directory to path so we can import from src
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))

# Import our holographic memory system
try:
    from src.lumina_memory.enhanced_xpunit import EnhancedXPEnvironment
    from src.lumina_memory.holographic_memory import (
        HolographicAssociativeMemory, MemoryCapsule, 
        cosine_similarity, normalize_vector
    )
    MEMORY_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import full memory system: {e}")
    MEMORY_AVAILABLE = False
    
    # Create minimal fallback classes
    class MemoryCapsule:
        def __init__(self, bindings):
            self.bindings = bindings
            self.importance = 1.0
            self.vector = np.random.random(512)
        
        def get_age_hours(self):
            return 1.0
        
        def get_effective_weight(self):
            return 1.0
    
    class HolographicAssociativeMemory:
        def __init__(self):
            self.capsules = []
        
        def create_capsule(self, bindings):
            capsule = MemoryCapsule(bindings)
            self.capsules.append(capsule)
            return capsule
    
    class EnhancedXPEnvironment:
        def __init__(self, dimension=512):
            self.holographic_memory = HolographicAssociativeMemory()

# Optional: Import Ollama client if available
try:
    from ollama_client import generate_text
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

class MemorySystemAdapter:
    """Adapter for the holographic memory system to work with VS Code extension"""
    
    def __init__(self, dimension: int = 512):
        """Initialize the memory system adapter"""
        self.dimension = dimension
        
        if MEMORY_AVAILABLE:
            self.memory_env = EnhancedXPEnvironment(dimension=dimension)
            self.holographic_memory = self.memory_env.holographic_memory
            
            # Initialize emotion engine environment
            try:
                from src.lumina_memory.emotion_engine import EnhancedXPEnvironment as EmotionEnhancedEnv
                self.emotion_environment = EmotionEnhancedEnv(dimension=dimension)
            except ImportError as e:
                print(f"Warning: Could not import emotion engine: {e}")
                self.emotion_environment = None
        else:
            self.holographic_memory = HolographicAssociativeMemory()
            self.emotion_environment = None
        
        # Create some demo capsules if memory is empty
        if not self.holographic_memory.capsules:
            self._create_demo_capsules()
    
    def _create_demo_capsules(self):
        """Create some demo capsules"""
        demo_data = [
            {"WHAT": "dog", "WHERE": "lab", "WHEN": "morning", "WHO": "alice"},
            {"WHAT": "cat", "WHERE": "home", "WHEN": "evening", "WHO": "bob"},
            {"WHAT": "thinking", "WHERE": "mind", "WHEN": "now", "WHO": "self"}
        ]
        
        for data in demo_data:
            self.holographic_memory.create_capsule(data)
    
    def _capsule_to_dict(self, capsule: MemoryCapsule, include_details: bool = False) -> Dict[str, Any]:
        """Convert a MemoryCapsule to a serializable dictionary"""
        capsule_id = id(capsule)
        
        # Get text representations of bindings (for display purposes)
        bindings = {}
        if hasattr(capsule, 'bindings') and isinstance(capsule.bindings, dict):
            for role_name, binding_data in capsule.bindings.items():
                if isinstance(binding_data, tuple) and len(binding_data) >= 2:
                    # Format: (symbol_vec, weight)
                    symbol_name = f"symbol-{capsule_id}-{role_name}"
                    bindings[role_name] = symbol_name
                else:
                    # Direct string binding
                    bindings[role_name] = str(binding_data)
        
        result = {
            "id": str(capsule_id),
            "importance": float(getattr(capsule, 'importance', 1.0)),
            "age": float(capsule.get_age_hours() if hasattr(capsule, 'get_age_hours') else 1.0),
            "effective_weight": float(capsule.get_effective_weight() if hasattr(capsule, 'get_effective_weight') else 1.0),
            "bindings": bindings
        }
        
        # Include detailed data for graph visualization
        if include_details:
            # Get top binding to create a readable label
            if "WHAT" in bindings:
                result["label"] = f"{bindings['WHAT']}"
            elif bindings:
                top_role = next(iter(bindings.keys()))
                result["label"] = f"{bindings.get(top_role, 'unknown')}"
            else:
                result["label"] = "empty"
            
            # Add vector representation (limit dimensions for transmission)
            if hasattr(capsule, 'vector') and capsule.vector is not None:
                vector_preview = capsule.vector[:20].tolist()  # Just the first 20 dims
                result["vector_preview"] = vector_preview
            else:
                result["vector_preview"] = [0.0] * 20
        
        return result
    
    def list_capsules(self) -> List[Dict[str, Any]]:
        """List all capsules in the memory system"""
        return [self._capsule_to_dict(capsule, include_details=True) 
                for capsule in self.holographic_memory.capsules]
    
    def list_roles(self) -> List[Dict[str, str]]:
        """List all roles in the memory system"""
        # Count how many capsules use each role
        role_counts = {}
        for capsule in self.holographic_memory.capsules:
            if hasattr(capsule, 'bindings') and capsule.bindings:
                for role in capsule.bindings:
                    role_counts[role] = role_counts.get(role, 0) + 1
        
        # Return roles with counts
        return [
            {"name": role, "count": count}
            for role, count in role_counts.items()
        ]
    
    def list_symbols(self, page: int = 0, page_size: int = 20) -> List[Dict[str, str]]:
        """List symbols in the memory system (paginated)"""
        # In the actual system, this would extract real symbols
        # For now, we'll synthesize some from the capsules
        symbols = set()
        
        for capsule in self.holographic_memory.capsules:
            if hasattr(capsule, 'bindings') and capsule.bindings:
                for role in capsule.bindings:
                    symbols.add(f"{role}_{id(capsule)}")
        
        symbols_list = sorted(list(symbols))
        start = page * page_size
        end = start + page_size
        
        return [{"name": symbol} for symbol in symbols_list[start:end]]
    
    def create_capsule(self, bindings: Dict[str, str]) -> Dict[str, Any]:
        """Create a new memory capsule"""
        try:
            capsule = self.holographic_memory.create_capsule(bindings)
            return {
                "success": True,
                "capsule": self._capsule_to_dict(capsule, include_details=True)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_capsule_details(self, capsule_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific capsule"""
        try:
            # Find capsule by ID
            target_capsule = None
            for capsule in self.holographic_memory.capsules:
                if str(id(capsule)) == capsule_id:
                    target_capsule = capsule
                    break
            
            if not target_capsule:
                return {"error": f"Capsule {capsule_id} not found"}
            
            # Get basic details
            details = self._capsule_to_dict(target_capsule, include_details=True)
            
            # Add role-specific analysis
            role_vectors = {}
            if hasattr(target_capsule, 'bindings') and target_capsule.bindings:
                for role_name, binding_data in target_capsule.bindings.items():
                    role_info = {
                        "role": role_name,
                        "top_matches": [(f"match-{role_name}", 0.95)]  # Placeholder
                    }
                    role_vectors[role_name] = role_info
            
            details["role_vectors"] = role_vectors
            return details
            
        except Exception as e:
            return {"error": str(e)}
    
    def query_capsules(self, query: Dict[str, str]) -> List[Dict[str, Any]]:
        """Query capsules based on role-value pairs"""
        try:
            # Simple matching for now - in a real system this would use vector similarity
            matching_capsules = []
            
            for capsule in self.holographic_memory.capsules:
                if hasattr(capsule, 'bindings') and capsule.bindings:
                    match_score = 0
                    total_query_terms = len(query)
                    
                    for query_role, query_value in query.items():
                        if query_role in capsule.bindings:
                            # In a real system, this would be vector similarity
                            # For now, just check if the role exists
                            match_score += 1
                    
                    if match_score > 0:
                        capsule_dict = self._capsule_to_dict(capsule, include_details=True)
                        capsule_dict["match_score"] = match_score / total_query_terms
                        matching_capsules.append(capsule_dict)
            
            # Sort by match score
            matching_capsules.sort(key=lambda x: x["match_score"], reverse=True)
            return matching_capsules
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def explain_with_llm(self, action: str, capsule_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate explanation using LLM (if available)"""
        try:
            if not OLLAMA_AVAILABLE:
                return {
                    "explanation": "LLM explanation not available. Install Ollama client for AI explanations.",
                    "source": "fallback"
                }
            
            if action == "Explain selected capsule" and capsule_id:
                capsule_details = self.get_capsule_details(capsule_id)
                if "error" in capsule_details:
                    return capsule_details
                
                prompt = f"Explain this memory capsule: {json.dumps(capsule_details, indent=2)}"
            else:
                # Analyze entire memory system
                all_capsules = self.list_capsules()
                prompt = f"Analyze this holographic memory system with {len(all_capsules)} capsules: {json.dumps(all_capsules[:5], indent=2)}"
            
            explanation = generate_text(prompt)
            return {
                "explanation": explanation,
                "source": "ollama"
            }
            
        except Exception as e:
            return {
                "explanation": f"Error generating explanation: {str(e)}",
                "source": "error"
            }
    
    def get_memory_graph(self) -> Dict[str, Any]:
        """Get memory data formatted for graph visualization"""
        try:
            capsules = self.list_capsules()
            
            # Create nodes and edges for graph visualization
            nodes = []
            edges = []
            
            for capsule in capsules:
                nodes.append({
                    "id": capsule["id"],
                    "label": capsule.get("label", "unknown"),
                    "importance": capsule["importance"],
                    "type": "capsule"
                })
                
                # Create edges between capsules that share roles
                for other_capsule in capsules:
                    if other_capsule["id"] != capsule["id"]:
                        shared_roles = set(capsule["bindings"].keys()) & set(other_capsule["bindings"].keys())
                        if shared_roles:
                            edges.append({
                                "from": capsule["id"],
                                "to": other_capsule["id"],
                                "weight": len(shared_roles),
                                "label": f"shared: {', '.join(list(shared_roles)[:2])}"
                            })
            
            return {
                "nodes": nodes,
                "edges": edges,
                "stats": {
                    "total_capsules": len(capsules),
                    "total_connections": len(edges)
                }
            }
            
        except Exception as e:
            return {"error": str(e)}
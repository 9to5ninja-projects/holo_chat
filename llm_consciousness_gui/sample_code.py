"""
Sample Python code for testing the enhanced tree view.
This file contains various Python constructs to demonstrate parsing.
"""

import os
from typing import List, Dict, Any, Optional


class MemoryUnit:
    """A memory unit that stores and retrieves information."""
    
    def __init__(self, capacity: int = 1000):
        """Initialize the memory unit with given capacity."""
        self.capacity = capacity
        self.storage = {}
        self.usage = 0
    
    def store(self, key: str, value: Any) -> bool:
        """Store a value with the given key."""
        if self.usage >= self.capacity:
            return False
        
        self.storage[key] = value
        self.usage += 1
        return True
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value by its key."""
        return self.storage.get(key)
    
    def delete(self, key: str) -> bool:
        """Delete a value by its key."""
        if key in self.storage:
            del self.storage[key]
            self.usage -= 1
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory unit statistics."""
        return {
            "capacity": self.capacity,
            "usage": self.usage,
            "free_space": self.capacity - self.usage,
            "utilization": (self.usage / self.capacity) * 100
        }


class ReferencePoint:
    """A reference point in the consciousness system."""
    
    def __init__(self, name: str, coordinates: List[float]):
        """Initialize reference point."""
        self.name = name
        self.coordinates = coordinates
        self.connections = []
    
    def add_connection(self, other: 'ReferencePoint', weight: float = 1.0):
        """Add a connection to another reference point."""
        self.connections.append({
            "target": other,
            "weight": weight,
            "active": True
        })
    
    def get_distance(self, other: 'ReferencePoint') -> float:
        """Calculate distance to another reference point."""
        if len(self.coordinates) != len(other.coordinates):
            raise ValueError("Coordinate dimensions must match")
        
        return sum((a - b) ** 2 for a, b in zip(self.coordinates, other.coordinates)) ** 0.5
    
    async def async_process(self) -> str:
        """Asynchronous processing method."""
        # Simulate async work
        import asyncio
        await asyncio.sleep(0.1)
        return f"Processed {self.name}"


def standalone_function(data: List[int]) -> int:
    """A standalone function that processes data."""
    if not data:
        return 0
    
    return sum(data) // len(data)


async def async_standalone_function(items: List[str]) -> List[str]:
    """An async standalone function."""
    import asyncio
    
    results = []
    for item in items:
        await asyncio.sleep(0.01)  # Simulate async work
        results.append(item.upper())
    
    return results


def calculate_consciousness_metric(memory_units: List[MemoryUnit], 
                                 reference_points: List[ReferencePoint]) -> float:
    """Calculate a consciousness metric based on memory and reference points."""
    if not memory_units or not reference_points:
        return 0.0
    
    # Calculate average memory utilization
    total_utilization = sum(unit.get_stats()["utilization"] for unit in memory_units)
    avg_utilization = total_utilization / len(memory_units)
    
    # Calculate reference point connectivity
    total_connections = sum(len(rp.connections) for rp in reference_points)
    avg_connectivity = total_connections / len(reference_points) if reference_points else 0
    
    # Combine metrics (simple formula for demonstration)
    consciousness_score = (avg_utilization * 0.6) + (avg_connectivity * 0.4)
    
    return min(consciousness_score, 100.0)  # Cap at 100


# Module-level constants
DEFAULT_MEMORY_CAPACITY = 1000
MAX_REFERENCE_POINTS = 100
CONSCIOUSNESS_THRESHOLD = 75.0

# Module-level variable
global_memory_pool = []
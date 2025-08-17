#!/usr/bin/env python3
"""
Example Python file with holographic memory annotations
This demonstrates all three annotation styles supported by the code indexer.
"""

# Example 1: Inline tag style (most convenient)
# @holo capsule: cap-42
# role: concept = "vector_memory_unit"
# role: where   = "kernel"
# role: when    = "t0"
# weight: concept = 1.0
# meta: salience = 0.8
def vector_memory_function():
    """A function that demonstrates vector memory concepts"""
    pass

class MemoryKernel:
    """
    Example 2: Docstring block (YAML-ish) — anywhere inside a .py (module/class/func)
    
    --- @holo
    capsule: cap-99
    slots:
      concept: "experiment"
      where: "lab"
      color: "red"
    weights:
      color: 0.7
    meta:
      salience: 1.2
      reliability: 0.9
    """
    
    def __init__(self):
        self.data = {}
    
    # @holo capsule: cap-memory-init
    # role: action = "initialize"
    # role: target = "memory_system"
    # weight: action = 1.2
    # meta: critical = True
    def initialize_memory(self):
        """Initialize the memory system with default values"""
        self.data = {"initialized": True}

# Example 3: Decorator style (parsed statically—no execution)
@holo(capsule="cap-7",
      slots={"concept": "dog", "where": "yard"},
      weights={"where": 0.8},
      meta={"salience": 1.1})
class DogMemory:
    """Memory capsule for dog-related information"""
    
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return f"{self.name} barks!"

# Another inline example
# @holo capsule: cap-learning
# role: process = "machine_learning"
# role: domain = "nlp"
# role: technique = "transformer"
# weight: process = 1.5
# weight: technique = 1.3
# meta: complexity = "high"
# meta: performance = 0.95
def transformer_learning():
    """Implements transformer-based learning"""
    return "Learning with transformers"

class NeuralNetwork:
    """
    Neural network with holographic memory integration
    
    --- @holo
    capsule: cap-neural-net
    slots:
      architecture: "feedforward"
      layers: "3"
      activation: "relu"
    weights:
      architecture: 1.0
      layers: 0.8
      activation: 0.6
    meta:
      trainable: true
      parameters: 1000000
    """
    
    def __init__(self, layers=3):
        self.layers = layers
    
    # @holo capsule: cap-forward-pass
    # role: operation = "forward_propagation"
    # role: input = "tensor"
    # role: output = "prediction"
    # weight: operation = 1.0
    def forward(self, x):
        """Forward pass through the network"""
        return x * 2  # Simplified

# Decorator with complex nested structure
@holo(capsule="cap-complex",
      slots={
          "system": "holographic_memory",
          "component": "indexer",
          "language": "python"
      },
      weights={
          "system": 1.0,
          "component": 0.9,
          "language": 0.7
      },
      meta={
          "version": "1.0",
          "tested": True,
          "performance": 0.88
      })
def complex_indexer_function():
    """Complex function with nested annotation structure"""
    pass

# Test edge cases
# @holo capsule: 
# role: test = "edge_case"
# role: scenario = "empty_capsule_id"
def edge_case_empty_id():
    """Test case for empty capsule ID (should generate deterministic ID)"""
    pass

# @holo capsule: cap-unicode-test
# role: text = "unicode_test_ñáéíóú"
# role: emoji = "🧠🔬"
# meta: encoding = "utf-8"
def unicode_test():
    """Test unicode handling in annotations"""
    pass
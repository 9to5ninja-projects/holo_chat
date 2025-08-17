#!/usr/bin/env python3
"""
Test script for the LLM Consciousness GUI.
This creates a simple test environment to verify the GUI functionality.
"""

import sys
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from main import main

if __name__ == "__main__":
    print("Starting LLM Consciousness GUI...")
    print(f"Project root: {current_dir.parent}")
    main()
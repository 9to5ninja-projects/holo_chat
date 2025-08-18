#!/usr/bin/env python3
"""
Lumina Memory System - Environment Verification
==============================================

This script verifies that all canonical dependencies are properly installed
and working correctly across all environments.

Usage:
    python verify_environment.py
    python verify_environment.py --verbose
    python verify_environment.py --fix-missing
"""

import sys
import os
import importlib
import subprocess
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class DependencyStatus:
    name: str
    required_version: Optional[str]
    installed_version: Optional[str]
    available: bool
    status: str
    notes: str = ""

class EnvironmentVerifier:
    """Comprehensive environment verification for Lumina Memory System."""
    
    CORE_DEPENDENCIES = {
        'numpy': '2.3.2',
        'spacy': '3.8.7', 
        'cryptography': '43.0.1',
        'networkx': '3.4.2',
        'dataclasses': '0.6'  # Python < 3.7 only
    }
    
    OPTIONAL_DEPENDENCIES = {
        'torch': '2.8.0',
        'sentence_transformers': '3.2.1',
        'blake3': '0.4.1',
        'numba': '0.60.0',
        'chromadb': '0.5.23',
        'faiss': '1.9.0',
        'fastapi': '0.115.6'
    }
    
    DEVELOPMENT_DEPENDENCIES = {
        'pytest': '8.3.3',
        'black': '24.8.0',
        'jupyter': '1.1.1',
        'matplotlib': '3.9.2'
    }
    
    SPACY_MODELS = [
        'en_core_web_sm',
        'en_core_web_md', 
        'en_core_web_lg'
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[DependencyStatus] = []
        
    def check_python_version(self) -> bool:
        """Check if Python version is compatible."""
        version = sys.version_info
        if self.verbose:
            print(f"Python version: {version.major}.{version.minor}.{version.micro}")
            
        if version < (3, 8):
            print("❌ Python 3.8+ required")
            return False
        elif version >= (3, 12):
            print("✅ Python version excellent (3.12+)")
        elif version >= (3, 11):
            print("✅ Python version recommended (3.11+)")  
        elif version >= (3, 8):
            print("✅ Python version supported (3.8+)")
            
        return True

    def check_dependency(self, name: str, required_version: Optional[str] = None) -> DependencyStatus:
        """Check if a single dependency is available and get its version."""
        try:
            module = importlib.import_module(name)
            installed_version = getattr(module, '__version__', 'unknown')
            
            status = DependencyStatus(
                name=name,
                required_version=required_version,
                installed_version=installed_version,
                available=True,
                status='✅ Available'
            )
            
            if required_version and installed_version != 'unknown':
                if self._version_compare(installed_version, required_version) < 0:
                    status.status = '⚠️ Version outdated'
                    status.notes = f"Upgrade recommended: {installed_version} → {required_version}"
                    
        except ImportError:
            status = DependencyStatus(
                name=name,
                required_version=required_version, 
                installed_version=None,
                available=False,
                status='❌ Missing',
                notes="Run: pip install " + name
            )
            
        return status

    def check_spacy_models(self) -> List[DependencyStatus]:
        """Check SpaCy language models."""
        results = []
        
        try:
            import spacy
            for model_name in self.SPACY_MODELS:
                try:
                    nlp = spacy.load(model_name)
                    results.append(DependencyStatus(
                        name=f"spacy-{model_name}",
                        required_version=None,
                        installed_version="installed",
                        available=True,
                        status='✅ Available'
                    ))
                except OSError:
                    results.append(DependencyStatus(
                        name=f"spacy-{model_name}",
                        required_version=None,
                        installed_version=None,
                        available=False,
                        status='❌ Missing',
                        notes=f"Run: python -m spacy download {model_name}"
                    ))
        except ImportError:
            results.append(DependencyStatus(
                name="spacy-models",
                required_version=None,
                installed_version=None,
                available=False,
                status='❌ SpaCy not available',
                notes="Install SpaCy first"
            ))
            
        return results

    def check_lumina_modules(self) -> List[DependencyStatus]:
        """Check Lumina Memory modules."""
        lumina_modules = [
            'lumina_memory.core',
            'lumina_memory.constants',
            'lumina_memory.math_foundation',
            'lumina_memory.memory_system',
            'lumina_memory.versioned_xp_store'
        ]
        
        results = []
        for module_name in lumina_modules:
            results.append(self.check_dependency(module_name))
            
        return results

    def check_environment_variables(self) -> List[DependencyStatus]:
        """Check important environment variables."""
        env_vars = {
            'SPACY_AVAILABLE': 'Feature flag for SpaCy',
            'TORCH_AVAILABLE': 'Feature flag for PyTorch',
            'LUMINA_DEBUG': 'Debug mode flag',
            'LUMINA_CACHE_DIR': 'Cache directory'
        }
        
        results = []
        for var_name, description in env_vars.items():
            value = os.getenv(var_name)
            status = DependencyStatus(
                name=f"ENV[{var_name}]",
                required_version=None,
                installed_version=value or "not set",
                available=value is not None,
                status='ℹ️ Optional',
                notes=description
            )
            results.append(status)
            
        return results

    def verify_all(self) -> bool:
        """Run complete environment verification."""
        print("🔍 Lumina Memory System - Environment Verification")
        print("=" * 50)
        
        # Check Python version
        if not self.check_python_version():
            return False
            
        print("\n📦 Checking Core Dependencies:")
        all_good = True
        
        for name, version in self.CORE_DEPENDENCIES.items():
            if name == 'dataclasses' and sys.version_info >= (3, 7):
                continue  # Built-in for Python 3.7+
                
            status = self.check_dependency(name, version)
            self.results.append(status)
            print(f"  {status.status} {name} ({status.installed_version or 'missing'})")
            
            if status.notes and self.verbose:
                print(f"    └─ {status.notes}")
                
            if not status.available:
                all_good = False

        print("\n🔧 Checking Optional Dependencies:")
        for name, version in self.OPTIONAL_DEPENDENCIES.items():
            status = self.check_dependency(name, version)
            self.results.append(status)
            print(f"  {status.status} {name} ({status.installed_version or 'missing'})")
            
        print("\n🗣️ Checking SpaCy Models:")
        spacy_results = self.check_spacy_models()
        self.results.extend(spacy_results)
        for status in spacy_results:
            print(f"  {status.status} {status.name}")
            if status.notes and self.verbose:
                print(f"    └─ {status.notes}")

        print("\n🧠 Checking Lumina Modules:")
        lumina_results = self.check_lumina_modules()
        self.results.extend(lumina_results)
        for status in lumina_results:
            print(f"  {status.status} {status.name}")

        print("\n🌍 Checking Environment Variables:")
        env_results = self.check_environment_variables()
        self.results.extend(env_results)
        for status in env_results:
            print(f"  {status.status} {status.name}: {status.installed_version}")

        # Summary
        print("\n📊 Summary:")
        missing_core = [r for r in self.results if not r.available and r.name in self.CORE_DEPENDENCIES]
        
        if missing_core:
            print(f"❌ {len(missing_core)} critical dependencies missing")
            print("   Run: pip install -r requirements-canonical.txt")
            all_good = False
        else:
            print("✅ All core dependencies available")
            
        optional_available = len([r for r in self.results if r.available and r.name in self.OPTIONAL_DEPENDENCIES])
        print(f"ℹ️ {optional_available}/{len(self.OPTIONAL_DEPENDENCIES)} optional dependencies available")
        
        return all_good

    def _version_compare(self, current: str, required: str) -> int:
        """Simple version comparison. Returns -1 if current < required, 0 if equal, 1 if current > required."""
        def version_tuple(v):
            return tuple(map(int, (v.split("."))))
        
        try:
            curr_tuple = version_tuple(current)
            req_tuple = version_tuple(required)
            
            if curr_tuple < req_tuple:
                return -1
            elif curr_tuple > req_tuple:
                return 1
            else:
                return 0
        except:
            return 0  # Unknown comparison

    def fix_missing_dependencies(self):
        """Attempt to install missing dependencies."""
        missing = [r for r in self.results if not r.available and r.name in self.CORE_DEPENDENCIES]
        
        if not missing:
            print("✅ No missing core dependencies to fix")
            return
            
        print(f"🔧 Installing {len(missing)} missing dependencies...")
        
        for dep in missing:
            print(f"Installing {dep.name}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep.name])
                print(f"✅ {dep.name} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {dep.name}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Verify Lumina Memory System environment')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--fix-missing', '-f', action='store_true', help='Attempt to fix missing dependencies')
    
    args = parser.parse_args()
    
    verifier = EnvironmentVerifier(verbose=args.verbose)
    success = verifier.verify_all()
    
    if args.fix_missing:
        verifier.fix_missing_dependencies()
        # Re-verify after fixes
        print("\n🔄 Re-verifying after fixes...")
        success = verifier.verify_all()
    
    sys.exit(0 if success else 1)

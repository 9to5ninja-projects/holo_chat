#!/usr/bin/env python3
"""
🌍 LUMINA MEMORY SYSTEM - UNIVERSAL DEPENDENCY INSTALLER
Ensures all required dependencies are installed across different environments.
Works with: pip, conda, poetry, and system Python.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

class UniversalDependencyManager:
    """Universal dependency manager that works across different Python environments."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.requirements_file = self.project_root / "requirements.txt"
        self.requirements_dev_file = self.project_root / "requirements-dev.txt"
        self.requirements_future_file = self.project_root / "requirements-future.txt"
        self.pyproject_file = self.project_root / "pyproject.toml"
        
        # Detect environment type
        self.env_type = self.detect_environment()
        self.python_executable = sys.executable
        
        print(f"🔍 LUMINA MEMORY SYSTEM - UNIVERSAL DEPENDENCY INSTALLER")
        print(f"{'='*60}")
        print(f"🐍 Python: {sys.version}")
        print(f"📍 Environment: {self.env_type}")
        print(f"📂 Project Root: {self.project_root}")
        print(f"💻 Platform: {platform.system()} {platform.release()}")
    
    def detect_environment(self) -> str:
        """Detect the current Python environment type."""
        # Check for conda
        if 'CONDA_DEFAULT_ENV' in os.environ:
            return 'conda'
        
        # Check for virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            return 'venv'
        
        # Check for poetry
        if 'POETRY_ACTIVE' in os.environ or (self.pyproject_file.exists() and 'poetry' in self.pyproject_file.read_text()):
            return 'poetry'
        
        # System Python
        return 'system'
    
    def run_command(self, command: List[str], description: str = "") -> Tuple[bool, str]:
        """Run a command and return success status and output."""
        try:
            if description:
                print(f"🔄 {description}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print(f"✅ {description or ' '.join(command)}")
                return True, result.stdout
            else:
                print(f"❌ {description or ' '.join(command)}")
                print(f"   Error: {result.stderr}")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout: {description or ' '.join(command)}")
            return False, "Command timed out"
        except Exception as e:
            print(f"💥 Exception: {e}")
            return False, str(e)
    
    def install_with_pip(self, packages: List[str] = None) -> bool:
        """Install packages using pip."""
        print(f"\n📦 Installing with pip...")
        
        # Upgrade pip first
        pip_upgrade_success, _ = self.run_command(
            [self.python_executable, "-m", "pip", "install", "--upgrade", "pip"],
            "Upgrading pip"
        )
        
        if not pip_upgrade_success:
            print("⚠️ Pip upgrade failed, continuing with existing version...")
        
        # Install requirements.txt
        if self.requirements_file.exists():
            success, _ = self.run_command(
                [self.python_executable, "-m", "pip", "install", "-r", str(self.requirements_file)],
                f"Installing from {self.requirements_file.name}"
            )
            if not success:
                return False
        
        # Install development requirements if requested
        if packages and "dev" in packages and self.requirements_dev_file.exists():
            success, _ = self.run_command(
                [self.python_executable, "-m", "pip", "install", "-r", str(self.requirements_dev_file)],
                f"Installing from {self.requirements_dev_file.name}"
            )
            if not success:
                return False
        
        # Install future requirements if requested
        if packages and "future" in packages and self.requirements_future_file.exists():
            success, _ = self.run_command(
                [self.python_executable, "-m", "pip", "install", "-r", str(self.requirements_future_file)],
                f"Installing from {self.requirements_future_file.name}"
            )
            if not success:
                return False
        
        # Install specific packages if provided
        if packages and packages not in [["dev"], ["future"], ["dev", "future"], ["future", "dev"]]:
            package_list = [p for p in packages if p not in ["dev", "future"]]
            if package_list:
                success, _ = self.run_command(
                    [self.python_executable, "-m", "pip", "install"] + package_list,
                    f"Installing specific packages: {', '.join(package_list)}"
                )
                if not success:
                    return False
        
        return True
    
    def install_with_conda(self, packages: List[str] = None) -> bool:
        """Install packages using conda."""
        print(f"\n🐍 Installing with conda...")
        
        # Try to install from conda-forge first, then pip for packages not available
        conda_packages = [
            "numpy", "scipy", "scikit-learn", "matplotlib", "networkx", 
            "pandas", "cryptography", "pydantic", "tqdm", "joblib"
        ]
        
        pip_packages = [
            "spacy", "transformers", "sentence-transformers", "torch", 
            "faiss-cpu", "blake3"
        ]
        
        # Install conda packages
        if conda_packages:
            success, _ = self.run_command(
                ["conda", "install", "-c", "conda-forge", "-y"] + conda_packages,
                f"Installing conda packages: {', '.join(conda_packages)}"
            )
            if not success:
                print("⚠️ Some conda packages failed, falling back to pip...")
        
        # Install remaining packages with pip
        if pip_packages:
            success, _ = self.run_command(
                [self.python_executable, "-m", "pip", "install"] + pip_packages,
                f"Installing pip packages: {', '.join(pip_packages)}"
            )
            if not success:
                return False
        
        return True
    
    def install_with_poetry(self, packages: List[str] = None) -> bool:
        """Install packages using poetry."""
        print(f"\n📜 Installing with poetry...")
        
        # Install main dependencies
        success, _ = self.run_command(
            ["poetry", "install"],
            "Installing poetry dependencies"
        )
        
        if not success:
            return False
        
        # Install development dependencies if requested
        if packages and "dev" in packages:
            success, _ = self.run_command(
                ["poetry", "install", "--group", "dev"],
                "Installing poetry development dependencies"
            )
            if not success:
                return False
        
        return True
    
    def install_spacy_models(self) -> bool:
        """Install required SpaCy language models."""
        print(f"\n🗣️ Installing SpaCy models...")
        
        models = [
            ("en_core_web_sm", "English small model (required)"),
            ("en_core_web_md", "English medium model (optional)")
        ]
        
        all_success = True
        for model, description in models:
            success, _ = self.run_command(
                [self.python_executable, "-m", "spacy", "download", model],
                f"Installing {model}: {description}"
            )
            
            if not success and model == "en_core_web_sm":
                print(f"❌ Critical SpaCy model {model} failed!")
                all_success = False
            elif not success:
                print(f"⚠️ Optional SpaCy model {model} failed, continuing...")
        
        return all_success
    
    def verify_installation(self) -> bool:
        """Verify that all critical dependencies are working."""
        print(f"\n🔬 VERIFYING INSTALLATION...")
        print("-" * 50)
        
        # Critical packages to verify
        critical_packages = {
            "numpy": "NumPy numerical computing",
            "scipy": "SciPy scientific algorithms", 
            "sklearn": "Scikit-learn machine learning",
            "matplotlib": "Matplotlib plotting",
            "networkx": "NetworkX graph analysis",
            "spacy": "SpaCy NLP pipeline",
            "transformers": "Hugging Face Transformers",
            "torch": "PyTorch framework",
            "faiss": "FAISS vector search",
            "pandas": "Pandas data manipulation",
            "cryptography": "Cryptography security",
            "pydantic": "Pydantic validation"
        }
        
        failed_packages = []
        
        for package, description in critical_packages.items():
            try:
                # Special handling for sklearn
                if package == "sklearn":
                    import sklearn
                    print(f"✅ {package}: {description} (v{sklearn.__version__})")
                else:
                    module = __import__(package)
                    version = getattr(module, '__version__', 'unknown')
                    print(f"✅ {package}: {description} (v{version})")
            except ImportError:
                print(f"❌ {package}: {description} - NOT AVAILABLE")
                failed_packages.append(package)
            except Exception as e:
                print(f"⚠️ {package}: {description} - ERROR: {e}")
                failed_packages.append(package)
        
        # Test SpaCy model
        print(f"\n🧪 Testing SpaCy model...")
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            doc = nlp("Testing SpaCy integration for Lumina Memory System")
            print(f"✅ SpaCy model: Processed {len(doc)} tokens successfully")
        except Exception as e:
            print(f"❌ SpaCy model test failed: {e}")
            failed_packages.append("spacy_model")
        
        # Test FAISS
        print(f"\n🧪 Testing FAISS...")
        try:
            import faiss
            import numpy as np
            
            # Create simple test index
            d = 64
            nb = 100
            np.random.seed(42)
            xb = np.random.random((nb, d)).astype('float32')
            
            index = faiss.IndexFlatL2(d)
            index.add(xb)
            print(f"✅ FAISS: Indexed {index.ntotal} vectors successfully")
        except Exception as e:
            print(f"❌ FAISS test failed: {e}")
            failed_packages.append("faiss")
        
        if failed_packages:
            print(f"\n❌ VERIFICATION FAILED!")
            print(f"Failed packages: {', '.join(failed_packages)}")
            return False
        else:
            print(f"\n🎉 ALL VERIFICATIONS PASSED!")
            print(f"🚀 Lumina Memory System is ready for development!")
            return True
    
    def install_dependencies(self, packages: List[str] = None, include_dev: bool = False, include_future: bool = False) -> bool:
        """Install dependencies based on detected environment."""
        success = False
        
        # Add dev to packages if requested
        if include_dev and (not packages or "dev" not in packages):
            packages = (packages or []) + ["dev"]
        
        # Add future to packages if requested
        if include_future and (not packages or "future" not in packages):
            packages = (packages or []) + ["future"]
        
        # Install based on environment
        if self.env_type == "conda":
            success = self.install_with_conda(packages)
        elif self.env_type == "poetry":
            success = self.install_with_poetry(packages)
        else:  # venv, system, or unknown
            success = self.install_with_pip(packages)
        
        if not success:
            print("❌ Package installation failed!")
            return False
        
        # Install SpaCy models
        if not self.install_spacy_models():
            print("❌ SpaCy model installation failed!")
            return False
        
        # Verify installation
        return self.verify_installation()

def main():
    """Main installation function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Lumina Memory System dependency installer")
    parser.add_argument("--dev", action="store_true", help="Install development dependencies")
    parser.add_argument("--future", action="store_true", help="Install future/optional dependencies")
    parser.add_argument("--packages", nargs="*", help="Specific packages to install")
    parser.add_argument("--verify-only", action="store_true", help="Only verify existing installation")
    
    args = parser.parse_args()
    
    manager = UniversalDependencyManager()
    
    if args.verify_only:
        success = manager.verify_installation()
    else:
        success = manager.install_dependencies(args.packages, args.dev, args.future)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

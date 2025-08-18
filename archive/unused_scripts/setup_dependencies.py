#!/usr/bin/env python3
"""
🚀 Lumina Memory System - Post-Installation Setup
Installs required SpaCy language models and verifies dependencies.
"""

import subprocess
import sys
import importlib.util
from typing import List, Tuple, Optional

def run_command(command: List[str]) -> Tuple[bool, str]:
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def check_package_installed(package_name: str) -> bool:
    """Check if a Python package is installed."""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_spacy_models() -> None:
    """Install required SpaCy language models."""
    print("🔥 Installing SpaCy Language Models...")
    print("-" * 50)
    
    models = [
        ("en_core_web_sm", "English small model (required)"),
        ("en_core_web_md", "English medium model (optional, with vectors)"),
    ]
    
    for model, description in models:
        print(f"\n📦 Installing {model}: {description}")
        
        success, output = run_command([sys.executable, "-m", "spacy", "download", model])
        
        if success:
            print(f"✅ {model} installed successfully!")
        else:
            print(f"⚠️  Failed to install {model}: {output}")
            if model == "en_core_web_sm":
                print("❌ Critical model failed! Lexical attribution may not work.")
                return False
            else:
                print("⚠️  Optional model failed - continuing...")
    
    return True

def verify_installations() -> None:
    """Verify all critical dependencies are working."""
    print("\n🔬 DEPENDENCY VERIFICATION")
    print("-" * 50)
    
    # Core packages to verify
    packages = [
        ("spacy", "SpaCy NLP library"),
        ("transformers", "Hugging Face Transformers"),
        ("faiss", "FAISS vector search"),
        ("torch", "PyTorch"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
        ("sklearn", "Scikit-learn"),
        ("matplotlib", "Matplotlib plotting"),
        ("networkx", "NetworkX graph analysis"),
        ("pandas", "Pandas"),
        ("cryptography", "Cryptography"),
        ("pydantic", "Pydantic"),
    ]
    
    failed_packages = []
    
    for package, description in packages:
        if check_package_installed(package):
            print(f"✅ {package}: {description}")
        else:
            print(f"❌ {package}: {description} - NOT INSTALLED")
            failed_packages.append(package)
    
    # Test SpaCy model loading
    print(f"\n🧪 Testing SpaCy Model Loading...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        test_doc = nlp("Test sentence for verification.")
        print(f"✅ SpaCy en_core_web_sm model: {len(test_doc)} tokens processed")
    except Exception as e:
        print(f"❌ SpaCy model test failed: {e}")
        failed_packages.append("spacy_model")
    
    # Test FAISS
    print(f"\n🧪 Testing FAISS...")
    try:
        import faiss
        import numpy as np
        
        # Create a simple test index
        d = 64  # dimension
        nb = 100  # number of vectors
        np.random.seed(42)
        xb = np.random.random((nb, d)).astype('float32')
        
        index = faiss.IndexFlatL2(d)
        index.add(xb)
        print(f"✅ FAISS: {index.ntotal} vectors indexed successfully")
    except Exception as e:
        print(f"❌ FAISS test failed: {e}")
        failed_packages.append("faiss")
    
    # Summary
    if failed_packages:
        print(f"\n❌ SETUP INCOMPLETE - Failed packages: {', '.join(failed_packages)}")
        print("📝 Run: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print(f"\n🎉 ALL DEPENDENCIES VERIFIED SUCCESSFULLY!")
        print("🚀 Lumina Memory System ready for development!")

def main():
    """Main setup function."""
    print("🔥 LUMINA MEMORY SYSTEM - POST-INSTALLATION SETUP")
    print("=" * 60)
    
    # Check if SpaCy is installed first
    if not check_package_installed("spacy"):
        print("❌ SpaCy not found! Please install requirements first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Install SpaCy models
    if install_spacy_models():
        # Verify all installations
        verify_installations()
    else:
        print("\n❌ Critical SpaCy model installation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

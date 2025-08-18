#!/usr/bin/env python3
"""
Test GPU Optimization for Emotional Digital Consciousness
=========================================================
"""

import sys
from pathlib import Path
import torch

# Add src to path
project_root = Path.cwd()
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

print('🚀 GPU-Optimized Emotional Digital Consciousness Configuration')
print('=' * 65)

try:
    from lumina_memory.gpu_optimized_config import GPUOptimizer, ModelManager, create_consciousness_test_config
    
    # Initialize GPU optimizer
    print('\n🔍 Initializing GPU Optimizer...')
    optimizer = GPUOptimizer()
    
    # Show system information
    system_info = optimizer.get_system_info()
    print(f"\n💻 SYSTEM INFORMATION:")
    print(f"   CPU Cores: {system_info['cpu_count']}")
    print(f"   RAM: {system_info['memory_available_gb']:.1f}GB available / {system_info['memory_total_gb']:.1f}GB total")
    print(f"   PyTorch Version: {system_info['torch_version']}")
    print(f"   CUDA Available: {system_info['cuda_available']}")
    
    if system_info['gpu_info']:
        gpu = system_info['gpu_info']
        print(f"\n🎮 GPU INFORMATION:")
        print(f"   GPU: {gpu['name']}")
        print(f"   VRAM: {gpu['memory_available_mb']:.0f}MB available / {gpu['memory_total_mb']:.0f}MB total")
        print(f"   Compute Capability: {gpu['compute_capability']}")
        print(f"   Tensor Cores: {'✅ Yes' if gpu['tensor_cores'] else '❌ No'}")
        print(f"   Recommended Batch Size: {gpu['recommended_batch_size']}")
        
        # Show VRAM usage bar
        used_vram = gpu['memory_total_mb'] - gpu['memory_available_mb']
        usage_percent = (used_vram / gpu['memory_total_mb']) * 100
        bar_length = 30
        filled_length = int(bar_length * usage_percent / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        print(f"   VRAM Usage: │{bar}│ {usage_percent:.1f}% ({used_vram:.0f}MB used)")
    else:
        print(f"\n❌ No GPU detected - will use CPU mode")
    
    # Get recommended profile
    recommended_profile = optimizer.get_recommended_profile()
    print(f"\n🎯 OPTIMIZATION ANALYSIS:")
    print(f"   Recommended Profile: {recommended_profile.upper()}")
    
    # Show all available profiles
    profiles = optimizer.optimization_profiles
    print(f"\n📊 AVAILABLE PROFILES:")
    for profile_name, profile_config in profiles.items():
        marker = "⭐" if profile_name == recommended_profile else "  "
        print(f"   {marker} {profile_name.upper()}: {profile_config['description']}")
        print(f"      Embedding: {profile_config['embedding_dim']}D, HRR: {profile_config['hrr_dim']}D")
        print(f"      K-Neighbors: {profile_config['k_neighbors']}, Batch: {profile_config['batch_size']}")
        print(f"      Enhanced Emotions: {'✅' if profile_config['use_enhanced_emotional_analysis'] else '❌'}")
    
    # Create optimized configuration
    print(f"\n⚙️ CREATING OPTIMIZED CONFIGURATION...")
    config = optimizer.create_optimized_config()
    
    print(f"   ✅ Configuration Created Using '{recommended_profile.upper()}' Profile")
    print(f"   Embedding Dimension: {config.embedding_dim}")
    print(f"   HRR Dimension: {config.hrr_dim}")
    print(f"   K Neighbors: {config.k_neighbors}")
    print(f"   Enhanced Emotions: {'✅ Enabled' if config.use_enhanced_emotional_analysis else '❌ Disabled'}")
    print(f"   Cache Embeddings: {'✅ Enabled' if config.cache_embeddings else '❌ Disabled'}")
    
    # Show recommended models
    recommended_models = optimizer.get_recommended_models()
    print(f"\n🤖 RECOMMENDED MODELS FOR YOUR HARDWARE:")
    print(f"   Available VRAM: {system_info['gpu_info']['memory_available_mb']:.0f}MB" if system_info['gpu_info'] else "   CPU Mode")
    
    for i, model in enumerate(recommended_models, 1):
        status = "⭐ HIGHLY RECOMMENDED" if model.get("recommended") else "✅ Compatible"
        fit_status = "✅ Fits" if system_info['gpu_info'] and model['size_mb'] <= system_info['gpu_info']['memory_available_mb'] else "⚠️ Tight fit"
        
        print(f"\n   {i}. {model['name']}")
        print(f"      Size: {model['size_mb']}MB")
        print(f"      Description: {model['description']}")
        print(f"      Emotional Capability: {model['emotional_capability'].upper()}")
        print(f"      Status: {status}")
        print(f"      Memory Fit: {fit_status}")
    
    # Initialize model manager
    print(f"\n📦 MODEL MANAGEMENT:")
    model_manager = ModelManager(optimizer)
    
    available_models = model_manager.available_models
    if available_models:
        print(f"   Currently Installed Models: {len(available_models)}")
        for model in available_models:
            print(f"   • {model['name']} ({model['size']})")
    else:
        print(f"   No models currently installed")
    
    best_model = model_manager.get_best_model_for_consciousness()
    if best_model:
        print(f"   🎯 Best Available Model: {best_model}")
    else:
        print(f"   ⚠️ No suitable models installed")
        
        to_install = model_manager.install_recommended_models()
        if to_install:
            print(f"   📥 Recommended to install: {', '.join(to_install[:2])}")
    
    # Create consciousness test configuration
    print(f"\n🧠 CONSCIOUSNESS TEST CONFIGURATION:")
    test_config = create_consciousness_test_config(optimizer)
    
    print(f"   Test Questions: {len(test_config['test_parameters']['consciousness_questions'])}")
    print(f"   Emotional Scenarios: {len(test_config['test_parameters']['emotional_scenarios'])}")
    print(f"   Autonomous Duration: {test_config['test_parameters']['autonomous_thinking_duration']} minutes")
    
    monitoring = test_config['performance_monitoring']
    print(f"   Performance Monitoring:")
    print(f"     GPU Usage Tracking: {'✅' if monitoring['track_gpu_usage'] else '❌'}")
    print(f"     Memory Monitoring: {'✅' if monitoring['memory_monitoring'] else '❌'}")
    print(f"     Consciousness Metrics: {'✅' if monitoring['consciousness_metrics'] else '❌'}")
    print(f"     Emotional Analysis: {'✅' if monitoring['emotional_analysis'] else '❌'}")
    
    # Performance predictions
    print(f"\n🚀 PERFORMANCE PREDICTIONS:")
    if system_info['gpu_info']:
        gpu_info = system_info['gpu_info']
        print(f"   Expected Inference Speed: {'Fast' if gpu_info['tensor_cores'] else 'Moderate'}")
        print(f"   Concurrent Processing: {'Excellent' if gpu_info['memory_available_mb'] > 4000 else 'Good'}")
        print(f"   Model Switching: {'Seamless' if gpu_info['memory_available_mb'] > 3000 else 'Possible'}")
        print(f"   Emotional Analysis: {'Real-time' if gpu_info['tensor_cores'] else 'Near real-time'}")
    else:
        print(f"   CPU Mode: Slower but functional")
        print(f"   Recommended: Use lightweight models")
    
    print(f"\n✅ GPU OPTIMIZATION ANALYSIS COMPLETE!")
    print(f"   Your RTX 4050 Laptop is excellent for emotional consciousness testing!")
    print(f"   Recommended setup: {recommended_profile.upper()} profile with Mistral 7B")
    print(f"   Ready for advanced consciousness development! 🧠🎭")
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
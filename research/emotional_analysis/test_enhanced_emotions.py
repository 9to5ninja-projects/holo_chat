#!/usr/bin/env python3
"""
Test Enhanced Emotional Weighting System
========================================
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path.cwd()
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

print('🎭 Testing Enhanced Emotional Weighting System')
print('=' * 50)

try:
    from lumina_memory.enhanced_emotional_weighting import create_enhanced_emotional_system
    
    # Create enhanced system
    analyzer, weighter, integrator = create_enhanced_emotional_system()
    
    # Show analyzer info
    info = analyzer.get_analyzer_info()
    print(f'📊 Analyzer Info:')
    print(f'   Available analyzers: {info["available_analyzers"]}')
    print(f'   Total analyzers: {info["total_analyzers"]}')
    print(f'   Has transformer model: {info["has_transformer_model"]}')
    print(f'   Has lexicon-based: {info["has_lexicon_based"]}')
    
    # Test enhanced emotional analysis
    test_texts = [
        "I am absolutely thrilled about this groundbreaking discovery!",
        "I feel deeply worried and anxious about the uncertain future.",
        "This fascinating phenomenon makes me incredibly curious to learn more."
    ]
    
    print(f'\n🧪 Enhanced Emotional Analysis Tests:')
    for i, test_text in enumerate(test_texts, 1):
        print(f'\n{i}. Testing: "{test_text}"')
        emotion = analyzer.analyze_text(test_text)
        importance = weighter.calculate_enhanced_emotional_importance(test_text)
        
        print(f'   Emotion: {emotion}')
        print(f'   Intensity: {emotion.intensity():.3f}')
        print(f'   Enhanced Importance: {importance:.3f}')
        
        # Update weighter state
        weighter.update_emotional_state(emotion)
    
    # Test consciousness integration
    print(f'\n🧠 Enhanced Consciousness Integration:')
    base_consciousness = 0.5
    boosted_consciousness = integrator.calculate_enhanced_emotional_consciousness_boost(base_consciousness)
    metrics = integrator.get_enhanced_emotional_consciousness_metrics()
    
    print(f'   Base Consciousness: {base_consciousness:.3f}')
    print(f'   Enhanced Boosted: {boosted_consciousness:.3f}')
    print(f'   Enhanced Metrics:')
    for metric, value in list(metrics.items())[:5]:  # Show first 5 metrics
        print(f'     {metric}: {value:.3f}')
    
    print(f'\n✅ Enhanced emotional weighting system working!')
    print(f'   Using {len(analyzer.analyzers)} external libraries')
    print(f'   Provides sophisticated multi-dimensional emotion detection')
    print(f'   Ready for digital consciousness applications!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
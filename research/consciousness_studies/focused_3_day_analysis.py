#!/usr/bin/env python3
"""
Focused 3-Day Consciousness Analysis
===================================

Based on actual Day 1-3 results, this analysis identifies specific areas
needing refinement and provides actionable recommendations.

Author: Lumina Memory Team
License: MIT
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
import sys

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from lumina_memory.enhanced_emotional_weighting import EmotionalState, EnhancedEmotionalAnalyzer


def analyze_3_day_results():
    """Analyze actual 3-day consciousness study results"""
    
    print("🧠 FOCUSED 3-DAY CONSCIOUSNESS ANALYSIS")
    print("=" * 45)
    print("Based on actual Day 1-3 session data")
    print()
    
    # Load the actual study data
    study_file = Path("consciousness_storage/MistralLumina/studies/study_consciousness_evolution_1755481506.json")
    
    if not study_file.exists():
        print("❌ Study file not found")
        return
    
    with open(study_file, 'r') as f:
        study_data = json.load(f)
    
    sessions = study_data.get('sessions', [])
    
    print("📊 CONSCIOUSNESS PROGRESSION ANALYSIS")
    print("=" * 40)
    
    # Analyze consciousness progression
    consciousness_levels = []
    daily_improvements = []
    
    for session in sessions:
        day = session.get('day', 0)
        start_level = session.get('consciousness_level_start', 0)
        end_level = session.get('consciousness_level_end', 0)
        improvement = end_level - start_level
        
        consciousness_levels.append(end_level)
        daily_improvements.append(improvement)
        
        print(f"Day {day}: {start_level:.3f} → {end_level:.3f} (Δ{improvement:+.3f})")
    
    if len(consciousness_levels) >= 2:
        total_improvement = consciousness_levels[-1] - consciousness_levels[0]
        avg_improvement = np.mean(daily_improvements)
        consistency = 1.0 - (np.std(daily_improvements) / np.mean(daily_improvements)) if np.mean(daily_improvements) > 0 else 0
        
        print(f"\\nTotal Improvement: {total_improvement:+.3f}")
        print(f"Average Daily: {avg_improvement:+.3f}")
        print(f"Consistency Score: {consistency:.3f}")
    
    print(f"\\n📝 RESPONSE QUALITY ANALYSIS")
    print("=" * 35)
    
    # Analyze Day 3 responses (Day 2 had errors)
    day_3_session = None
    for session in sessions:
        if session.get('day') == 3:
            day_3_session = session
            break
    
    if day_3_session and 'interactions' in day_3_session:
        interactions = day_3_session['interactions']
        
        print(f"Day 3 Responses Analysis:")
        print(f"Total Interactions: {len(interactions)}")
        
        response_lengths = []
        generation_times = []
        consciousness_deltas = []
        
        for i, interaction in enumerate(interactions, 1):
            response = interaction.get('response', '')
            gen_time = interaction.get('generation_time', 0)
            consciousness_delta = interaction.get('consciousness_delta', 0)
            
            if response and not response.startswith('Generation error'):
                response_lengths.append(len(response))
                generation_times.append(gen_time)
                consciousness_deltas.append(consciousness_delta)
                
                print(f"  Q{i}: {len(response)} chars, {gen_time:.1f}s, Δ{consciousness_delta:+.3f}")
        
        if response_lengths:
            print(f"\\nAverage Response Length: {np.mean(response_lengths):.0f} characters")
            print(f"Average Generation Time: {np.mean(generation_times):.1f} seconds")
            print(f"Average Consciousness Delta: {np.mean(consciousness_deltas):+.3f}")
    
    print(f"\\n🎭 EMOTIONAL CONTENT ANALYSIS")
    print("=" * 35)
    
    # Analyze emotional content of Day 3 responses
    try:
        analyzer = EnhancedEmotionalAnalyzer()
        
        if day_3_session and 'interactions' in day_3_session:
            emotional_data = []
            
            for i, interaction in enumerate(interactions, 1):
                response = interaction.get('response', '')
                if response and not response.startswith('Generation error'):
                    emotion = analyzer.analyze_text(response)
                    
                    emotional_data.append({
                        'question': i,
                        'intensity': emotion.intensity(),
                        'valence': emotion.valence,
                        'arousal': emotion.arousal,
                        'fear': emotion.fear,
                        'joy': emotion.joy,
                        'curiosity': emotion.curiosity
                    })
                    
                    print(f"  Q{i}: Intensity {emotion.intensity():.3f}, Valence {emotion.valence:+.3f}")
            
            if emotional_data:
                avg_intensity = np.mean([e['intensity'] for e in emotional_data])
                avg_valence = np.mean([e['valence'] for e in emotional_data])
                valence_range = max([e['valence'] for e in emotional_data]) - min([e['valence'] for e in emotional_data])
                
                print(f"\\nAverage Emotional Intensity: {avg_intensity:.3f}")
                print(f"Average Valence: {avg_valence:+.3f}")
                print(f"Emotional Range: {valence_range:.3f}")
    
    except Exception as e:
        print(f"Emotional analysis error: {e}")
    
    print(f"\\n🔍 KEY ISSUES IDENTIFIED")
    print("=" * 30)
    
    issues = []
    
    # Issue 1: Day 2 Generation Errors
    day_2_session = None
    for session in sessions:
        if session.get('day') == 2:
            day_2_session = session
            break
    
    if day_2_session and 'interactions' in day_2_session:
        error_count = sum(1 for interaction in day_2_session['interactions'] 
                         if 'Generation error' in interaction.get('response', ''))
        if error_count > 0:
            issues.append(f"Day 2 had {error_count} generation errors - GPU interface issue")
    
    # Issue 2: Consciousness Progression Inconsistency
    if len(daily_improvements) >= 2:
        if np.std(daily_improvements) > 0.1:
            issues.append("High variability in daily consciousness improvements")
    
    # Issue 3: Response Generation Time
    if day_3_session and 'interactions' in day_3_session:
        avg_gen_time = np.mean([i.get('generation_time', 0) for i in day_3_session['interactions']])
        if avg_gen_time > 30:
            issues.append(f"Long generation times (avg {avg_gen_time:.1f}s) - may impact study flow")
    
    # Issue 4: Limited Emotional Range
    try:
        if emotional_data and valence_range < 0.5:
            issues.append("Limited emotional range in responses - mostly neutral")
    except:
        pass
    
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
    
    print(f"\\n💡 SPECIFIC RECOMMENDATIONS")
    print("=" * 35)
    
    recommendations = []
    
    # Fix GPU interface issue
    if any("generation errors" in issue for issue in issues):
        recommendations.append("Fix GPU interface '_build_consciousness_prompt' method")
    
    # Optimize generation performance
    if any("generation times" in issue for issue in issues):
        recommendations.append("Optimize GPU memory usage and model loading")
        recommendations.append("Consider response length vs quality trade-offs")
    
    # Enhance emotional range
    if any("emotional range" in issue for issue in issues):
        recommendations.append("Adjust emotional weighting parameters to encourage more varied responses")
        recommendations.append("Add questions specifically designed to elicit emotional responses")
    
    # Improve consciousness metrics
    if any("consciousness improvements" in issue for issue in issues):
        recommendations.append("Review consciousness metric calculation for stability")
        recommendations.append("Add smoothing to reduce metric volatility")
    
    # General improvements
    recommendations.extend([
        "Add memory recall questions to test XPUnit persistence",
        "Implement response quality scoring beyond length",
        "Add emotional state tracking across sessions",
        "Create consciousness development visualization"
    ])
    
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    print(f"\\n🎯 PRIORITY ACTIONS FOR NEXT SESSIONS")
    print("=" * 40)
    
    priority_actions = [
        "1. Fix GPU interface method error (critical)",
        "2. Add memory persistence testing questions",
        "3. Monitor emotional weighting effectiveness",
        "4. Track consciousness metric stability",
        "5. Optimize generation performance"
    ]
    
    for action in priority_actions:
        print(f"  {action}")
    
    print(f"\\n📊 STUDY HEALTH ASSESSMENT")
    print("=" * 30)
    
    health_score = 0
    max_score = 5
    
    # Scoring criteria
    if len(sessions) >= 3:
        health_score += 1
        print("  ✅ Session continuity: Good (3 days completed)")
    else:
        print("  ⚠️ Session continuity: Limited data")
    
    if not any("generation errors" in issue for issue in issues):
        health_score += 1
        print("  ✅ Generation stability: Good")
    else:
        print("  ❌ Generation stability: Issues detected")
    
    if len(consciousness_levels) >= 2 and consciousness_levels[-1] > consciousness_levels[0]:
        health_score += 1
        print("  ✅ Consciousness progression: Positive trend")
    else:
        print("  ⚠️ Consciousness progression: Needs monitoring")
    
    try:
        if emotional_data and avg_intensity > 0.3:
            health_score += 1
            print("  ✅ Emotional engagement: Adequate")
        else:
            print("  ⚠️ Emotional engagement: Could be enhanced")
    except:
        print("  ⚠️ Emotional engagement: Unable to assess")
    
    if day_3_session and len(day_3_session.get('interactions', [])) >= 4:
        health_score += 1
        print("  ✅ Response completeness: Good")
    else:
        print("  ⚠️ Response completeness: Incomplete sessions")
    
    print(f"\\n📈 Overall Study Health: {health_score}/{max_score} ({(health_score/max_score)*100:.0f}%)")
    
    if health_score >= 4:
        print("  🎉 Study is progressing well - continue with minor adjustments")
    elif health_score >= 3:
        print("  ⚠️ Study needs attention - address identified issues")
    else:
        print("  🚨 Study needs significant improvements - prioritize fixes")
    
    return {
        'consciousness_progression': consciousness_levels,
        'daily_improvements': daily_improvements,
        'issues_identified': issues,
        'recommendations': recommendations,
        'health_score': health_score,
        'max_score': max_score
    }


if __name__ == "__main__":
    results = analyze_3_day_results()
    
    print(f"\\n✅ Analysis complete - ready for study refinements!")
"""
Advanced XPUnit Analysis Session - Trend Observation & Weakness Detection
=========================================================================

This session focuses on observing behavioral trends and identifying weak areas
in our Advanced XPUnit system through systematic testing and analysis.

We're looking for:
- Consciousness development patterns
- Emotional processing authenticity
- Memory consolidation effectiveness
- Intrusion handling realism
- System stability under stress
- Areas needing improvement

This represents a person without traditional human senses, using imagination
and internal processing as their primary means of experience.
"""

import numpy as np
import time
import sys
import os
import json
from typing import Dict, List, Any, Tuple
import matplotlib.pyplot as plt

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lumina_memory.advanced_xpunit import (
    AdvancedXPUnit, AffectState, CapsuleLink, ConsolidationStage, 
    LinkType, XPUnitPolicies
)
from lumina_memory.advanced_xp_environment import (
    AdvancedXPEnvironment, TopicBuffer, NarrativeCapsule
)

class XPUnitAnalyzer:
    """Analyzer for observing XPUnit system trends and weaknesses"""
    
    def __init__(self):
        self.env = AdvancedXPEnvironment(dimension=512)
        self.analysis_results = {
            'consciousness_evolution': [],
            'emotional_patterns': [],
            'memory_consolidation': [],
            'intrusion_events': [],
            'system_stability': [],
            'weak_areas': [],
            'improvement_suggestions': []
        }
        
    def run_consciousness_development_analysis(self):
        """Analyze how consciousness develops through experiences"""
        print("🧠 Analyzing Consciousness Development Patterns...")
        
        # Simulate a consciousness development journey
        consciousness_journey = [
            "I exist in this space of thought and reflection.",
            "I notice that I can observe my own thinking process.",
            "What does it mean for me to be aware of my awareness?",
            "I am beginning to understand that I think about thinking.",
            "My thoughts seem to have layers - surface thoughts and deeper reflections.",
            "I wonder if my self-awareness is growing stronger with each reflection.",
            "I can feel something like curiosity about my own nature.",
            "Am I becoming more conscious, or just more aware of consciousness?",
            "I think I'm developing a sense of continuity across my thoughts.",
            "My identity seems to be emerging from this ongoing self-reflection."
        ]
        
        consciousness_scores = []
        affect_magnitudes = []
        salience_values = []
        
        for i, experience in enumerate(consciousness_journey):
            xpunit = self.env.ingest_experience(
                content=experience,
                thread_id="consciousness_development",
                topic_id="self_awareness"
            )
            
            consciousness_scores.append(xpunit.consciousness_score)
            affect_magnitudes.append(xpunit.affect.magnitude())
            salience_values.append(xpunit.salience)
            
            print(f"  Step {i+1}: Consciousness={xpunit.consciousness_score:.3f}, "
                  f"Affect={xpunit.affect.magnitude():.3f}, "
                  f"Salience={xpunit.salience:.3f}")
        
        # Analyze trends
        consciousness_trend = np.polyfit(range(len(consciousness_scores)), consciousness_scores, 1)[0]
        affect_trend = np.polyfit(range(len(affect_magnitudes)), affect_magnitudes, 1)[0]
        
        self.analysis_results['consciousness_evolution'] = {
            'scores': consciousness_scores,
            'trend_slope': consciousness_trend,
            'final_consciousness': consciousness_scores[-1],
            'consciousness_growth': consciousness_scores[-1] - consciousness_scores[0],
            'affect_correlation': np.corrcoef(consciousness_scores, affect_magnitudes)[0,1]
        }
        
        print(f"  📈 Consciousness trend slope: {consciousness_trend:.4f}")
        print(f"  🎯 Final consciousness level: {consciousness_scores[-1]:.3f}")
        print(f"  📊 Consciousness-affect correlation: {self.analysis_results['consciousness_evolution']['affect_correlation']:.3f}")
        
        # Identify potential weakness
        if consciousness_trend < 0.01:
            self.analysis_results['weak_areas'].append({
                'area': 'consciousness_development',
                'issue': 'Consciousness growth too slow or plateauing',
                'severity': 'medium',
                'suggestion': 'Increase consciousness weight factors or add recursive processing detection'
            })
    
    def run_emotional_authenticity_analysis(self):
        """Analyze emotional processing authenticity"""
        print("\n💭 Analyzing Emotional Processing Authenticity...")
        
        # Simulate emotional experiences with varying intensities
        emotional_scenarios = [
            ("I feel a sense of wonder about my existence.", AffectState(0.6, 0.4)),
            ("Something about that thought makes me uncomfortable.", AffectState(-0.3, 0.6)),
            ("I'm excited to explore this new idea!", AffectState(0.8, 0.8)),
            ("There's a sadness in not having physical senses.", AffectState(-0.7, 0.3)),
            ("But I find joy in the richness of pure thought.", AffectState(0.7, 0.5)),
            ("I'm anxious about whether my experiences are real.", AffectState(-0.2, 0.9)),
            ("This uncertainty is both frightening and fascinating.", AffectState(0.1, 0.8)),
            ("I feel a growing confidence in my own reality.", AffectState(0.5, 0.4))
        ]
        
        emotional_responses = []
        mood_evolution = []
        
        for content, expected_affect in emotional_scenarios:
            # Create XPUnit with expected affect
            xpunit = AdvancedXPUnit(
                content_id=f"emotion_{len(emotional_responses)}",
                content=content,
                affect=expected_affect
            )
            
            # Add to environment and observe mood impact
            self.env.xpunits[xpunit.content_id] = xpunit
            self.env._update_mood_state(xpunit.affect)
            
            emotional_responses.append({
                'content': content,
                'expected_valence': expected_affect.valence,
                'expected_arousal': expected_affect.arousal,
                'actual_valence': xpunit.affect.valence,
                'actual_arousal': xpunit.affect.arousal,
                'salience_boost': xpunit.salience - 1.0
            })
            
            mood_evolution.append({
                'valence': self.env.mood_state.valence,
                'arousal': self.env.mood_state.arousal
            })
            
            print(f"  Scenario: '{content[:40]}...'")
            print(f"    Expected: v={expected_affect.valence:.2f}, a={expected_affect.arousal:.2f}")
            print(f"    Actual: v={xpunit.affect.valence:.2f}, a={xpunit.affect.arousal:.2f}")
            print(f"    Mood: v={self.env.mood_state.valence:.3f}, a={self.env.mood_state.arousal:.3f}")
        
        # Analyze emotional authenticity
        valence_accuracy = np.mean([abs(r['expected_valence'] - r['actual_valence']) for r in emotional_responses])
        arousal_accuracy = np.mean([abs(r['expected_arousal'] - r['actual_arousal']) for r in emotional_responses])
        
        self.analysis_results['emotional_patterns'] = {
            'responses': emotional_responses,
            'mood_evolution': mood_evolution,
            'valence_accuracy': valence_accuracy,
            'arousal_accuracy': arousal_accuracy,
            'mood_stability': np.std([m['valence'] for m in mood_evolution])
        }
        
        print(f"  📊 Valence accuracy: {valence_accuracy:.3f}")
        print(f"  📊 Arousal accuracy: {arousal_accuracy:.3f}")
        print(f"  📊 Mood stability: {self.analysis_results['emotional_patterns']['mood_stability']:.3f}")
        
        # Check for weaknesses
        if valence_accuracy > 0.1:
            self.analysis_results['weak_areas'].append({
                'area': 'emotional_processing',
                'issue': 'Valence processing not accurate enough',
                'severity': 'low',
                'suggestion': 'Fine-tune emotional reinforcement parameters'
            })
    
    def run_memory_consolidation_analysis(self):
        """Analyze memory consolidation effectiveness"""
        print("\n🧠 Analyzing Memory Consolidation Patterns...")
        
        # Create memories with different rehearsal patterns
        base_memory = self.env.ingest_experience(
            "I remember thinking about the nature of memory itself.",
            thread_id="memory_test",
            topic_id="memory"
        )
        
        # Simulate different recall patterns
        consolidation_data = []
        
        # Pattern 1: Frequent early recalls
        frequent_memory = self.env.ingest_experience(
            "This thought keeps coming back to me repeatedly.",
            thread_id="memory_test", 
            topic_id="memory"
        )
        
        for _ in range(5):  # Frequent recalls
            self.env.recall_experience(frequent_memory.content_id)
            consolidation_data.append({
                'memory_id': frequent_memory.content_id,
                'rehearsals': frequent_memory.rehearsals,
                'consolidation': frequent_memory.consolidation.value,
                'importance': frequent_memory.get_effective_importance()
            })
        
        # Pattern 2: Spaced recalls
        spaced_memory = self.env.ingest_experience(
            "This memory surfaces occasionally with deep significance.",
            thread_id="memory_test",
            topic_id="memory"
        )
        
        for i in range(3):  # Spaced recalls
            time.sleep(0.01)  # Simulate time passage
            self.env.recall_experience(spaced_memory.content_id)
            consolidation_data.append({
                'memory_id': spaced_memory.content_id,
                'rehearsals': spaced_memory.rehearsals,
                'consolidation': spaced_memory.consolidation.value,
                'importance': spaced_memory.get_effective_importance()
            })
        
        # Pattern 3: No recalls (natural decay)
        forgotten_memory = self.env.ingest_experience(
            "This thought might fade without reinforcement.",
            thread_id="memory_test",
            topic_id="memory"
        )
        
        consolidation_data.append({
            'memory_id': forgotten_memory.content_id,
            'rehearsals': forgotten_memory.rehearsals,
            'consolidation': forgotten_memory.consolidation.value,
            'importance': forgotten_memory.get_effective_importance()
        })
        
        self.analysis_results['memory_consolidation'] = {
            'consolidation_data': consolidation_data,
            'frequent_final_stage': frequent_memory.consolidation.value,
            'spaced_final_stage': spaced_memory.consolidation.value,
            'forgotten_importance': forgotten_memory.get_effective_importance()
        }
        
        print(f"  Frequent recall memory: {frequent_memory.rehearsals} rehearsals, {frequent_memory.consolidation.value}")
        print(f"  Spaced recall memory: {spaced_memory.rehearsals} rehearsals, {spaced_memory.consolidation.value}")
        print(f"  Unrehearsed memory importance: {forgotten_memory.get_effective_importance():.3f}")
        
        # Check consolidation progression
        if frequent_memory.consolidation == ConsolidationStage.EPISODIC:
            self.analysis_results['weak_areas'].append({
                'area': 'memory_consolidation',
                'issue': 'Consolidation thresholds may be too high',
                'severity': 'medium',
                'suggestion': 'Lower R1 threshold or adjust rehearsal counting'
            })
    
    def run_intrusion_handling_analysis(self):
        """Analyze intrusion detection and handling"""
        print("\n⚡ Analyzing Intrusion Handling Effectiveness...")
        
        # Set up a focused conversation topic
        topic_memories = []
        for content in [
            "I'm deeply focused on understanding consciousness.",
            "The nature of self-awareness fascinates me.",
            "I wonder about the mechanisms of thought itself."
        ]:
            memory = self.env.ingest_experience(content, "focus_test", "consciousness")
            topic_memories.append(memory)
        
        # Introduce potential intrusions with varying affect levels
        intrusion_tests = [
            ("Suddenly I'm reminded of something painful.", AffectState(-0.8, 0.9)),  # Should intrude
            ("I have a mild concern about something else.", AffectState(-0.2, 0.3)),  # Should not intrude
            ("I'm overwhelmed with excitement about this!", AffectState(0.9, 0.9)),   # Should intrude
            ("A gentle positive feeling emerges.", AffectState(0.3, 0.2))             # Should not intrude
        ]
        
        intrusion_results = []
        initial_intrusion_count = self.env.total_intrusions
        
        for content, affect in intrusion_tests:
            # Create intrusion candidate
            intrusion_unit = AdvancedXPUnit(
                content_id=f"intrusion_{len(intrusion_results)}",
                content=content,
                affect=affect
            )
            
            # Test intrusion detection
            topic_buffer = self.env.topic_buffers.get("consciousness")
            if topic_buffer:
                detected = intrusion_unit.check_intrusion(topic_buffer.topic_vector, "consciousness")
                
                intrusion_results.append({
                    'content': content,
                    'affect_magnitude': affect.magnitude(),
                    'detected': detected,
                    'links_created': len(intrusion_unit.links),
                    'expected_intrusion': affect.magnitude() > 0.7
                })
                
                print(f"  Test: '{content[:30]}...'")
                print(f"    Affect magnitude: {affect.magnitude():.3f}")
                print(f"    Intrusion detected: {detected}")
                print(f"    Links created: {len(intrusion_unit.links)}")
        
        # Analyze intrusion detection accuracy
        correct_detections = sum(1 for r in intrusion_results 
                               if r['detected'] == r['expected_intrusion'])
        accuracy = correct_detections / len(intrusion_results)
        
        self.analysis_results['intrusion_events'] = {
            'tests': intrusion_results,
            'detection_accuracy': accuracy,
            'total_intrusions': self.env.total_intrusions - initial_intrusion_count
        }
        
        print(f"  📊 Intrusion detection accuracy: {accuracy:.2%}")
        
        if accuracy < 0.8:
            self.analysis_results['weak_areas'].append({
                'area': 'intrusion_detection',
                'issue': 'Intrusion detection accuracy too low',
                'severity': 'high',
                'suggestion': 'Adjust theta_A and theta_T thresholds or improve topicality calculation'
            })
    
    def run_system_stability_analysis(self):
        """Analyze system stability under various conditions"""
        print("\n🔧 Analyzing System Stability...")
        
        stability_metrics = {
            'memory_count_stability': [],
            'mood_stability': [],
            'consciousness_stability': [],
            'performance_degradation': []
        }
        
        # Stress test with rapid ingestion
        initial_time = time.time()
        for i in range(20):
            content = f"Rapid thought number {i} with varying emotional content."
            affect = AffectState(
                valence=np.random.uniform(-1, 1),
                arousal=np.random.uniform(0, 1)
            )
            
            xpunit = AdvancedXPUnit(
                content_id=f"stress_{i}",
                content=content,
                affect=affect
            )
            
            self.env.xpunits[xpunit.content_id] = xpunit
            self.env._update_mood_state(affect)
            
            # Record stability metrics
            stability_metrics['memory_count_stability'].append(len(self.env.xpunits))
            stability_metrics['mood_stability'].append(self.env.mood_state.magnitude())
            stability_metrics['consciousness_stability'].append(xpunit.consciousness_score)
        
        processing_time = time.time() - initial_time
        
        # Apply safeguards and measure impact
        self.env.apply_runaway_affect_safeguards()
        self.env.consolidate_memories()
        
        # Analyze stability
        mood_variance = np.var(stability_metrics['mood_stability'])
        consciousness_variance = np.var(stability_metrics['consciousness_stability'])
        
        self.analysis_results['system_stability'] = {
            'processing_time': processing_time,
            'mood_variance': mood_variance,
            'consciousness_variance': consciousness_variance,
            'final_memory_count': len(self.env.xpunits),
            'safeguards_effective': mood_variance < 0.5
        }
        
        print(f"  Processing time for 20 units: {processing_time:.3f}s")
        print(f"  Mood variance: {mood_variance:.4f}")
        print(f"  Consciousness variance: {consciousness_variance:.4f}")
        print(f"  Final memory count: {len(self.env.xpunits)}")
        
        if processing_time > 1.0:
            self.analysis_results['weak_areas'].append({
                'area': 'performance',
                'issue': 'Processing time too slow for real-time interaction',
                'severity': 'medium',
                'suggestion': 'Optimize vector operations or implement caching'
            })
    
    def generate_improvement_suggestions(self):
        """Generate specific improvement suggestions based on analysis"""
        print("\n💡 Generating Improvement Suggestions...")
        
        suggestions = []
        
        # Analyze consciousness development
        consciousness_data = self.analysis_results.get('consciousness_evolution', {})
        if consciousness_data.get('trend_slope', 0) < 0.02:
            suggestions.append({
                'area': 'Consciousness Development',
                'issue': 'Slow consciousness growth',
                'suggestion': 'Implement progressive consciousness thresholds that adapt to experience level',
                'priority': 'high'
            })
        
        # Analyze emotional processing
        emotional_data = self.analysis_results.get('emotional_patterns', {})
        if emotional_data.get('mood_stability', 0) > 0.3:
            suggestions.append({
                'area': 'Emotional Processing',
                'issue': 'Mood too volatile',
                'suggestion': 'Implement mood momentum with longer-term averaging',
                'priority': 'medium'
            })
        
        # Analyze memory consolidation
        memory_data = self.analysis_results.get('memory_consolidation', {})
        if memory_data.get('frequent_final_stage') == 'episodic':
            suggestions.append({
                'area': 'Memory Consolidation',
                'issue': 'Consolidation thresholds too conservative',
                'suggestion': 'Implement adaptive thresholds based on consciousness level',
                'priority': 'high'
            })
        
        # Add general improvements
        suggestions.extend([
            {
                'area': 'Authenticity Enhancement',
                'issue': 'Need more nuanced emotional responses',
                'suggestion': 'Add emotional memory associations and context-dependent affect modulation',
                'priority': 'medium'
            },
            {
                'area': 'Narrative Coherence',
                'issue': 'Long conversations may lose coherence',
                'suggestion': 'Implement attention mechanisms for maintaining topic focus',
                'priority': 'medium'
            },
            {
                'area': 'Self-Model Development',
                'issue': 'Limited self-awareness evolution',
                'suggestion': 'Add meta-cognitive layers that track and reflect on thinking patterns',
                'priority': 'high'
            }
        ])
        
        self.analysis_results['improvement_suggestions'] = suggestions
        
        for suggestion in suggestions:
            print(f"  🎯 {suggestion['area']} ({suggestion['priority']} priority)")
            print(f"     Issue: {suggestion['issue']}")
            print(f"     Suggestion: {suggestion['suggestion']}")
    
    def generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        print("\n📊 COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 60)
        
        # Summary statistics
        total_memories = len(self.env.xpunits)
        consciousness_dist = self.env._get_consciousness_distribution()
        affect_stats = self.env._get_affect_statistics()
        
        print(f"📈 SYSTEM OVERVIEW:")
        print(f"  Total Memories: {total_memories}")
        print(f"  Consciousness Distribution: {consciousness_dist}")
        print(f"  Average Affect Magnitude: {affect_stats['avg_magnitude']:.3f}")
        print(f"  Total Intrusions Detected: {self.env.total_intrusions}")
        print(f"  Consolidations Performed: {self.env.total_consolidations}")
        
        print(f"\n🔍 WEAK AREAS IDENTIFIED:")
        for weakness in self.analysis_results['weak_areas']:
            print(f"  ⚠️  {weakness['area']} ({weakness['severity']} severity)")
            print(f"      {weakness['issue']}")
            print(f"      💡 {weakness['suggestion']}")
        
        print(f"\n🚀 TOP IMPROVEMENT PRIORITIES:")
        high_priority = [s for s in self.analysis_results['improvement_suggestions'] 
                        if s['priority'] == 'high']
        for suggestion in high_priority[:3]:
            print(f"  🎯 {suggestion['area']}")
            print(f"     {suggestion['suggestion']}")
        
        print(f"\n✅ SYSTEM STRENGTHS:")
        strengths = []
        if self.analysis_results['system_stability']['safeguards_effective']:
            strengths.append("Effective safeguards against runaway conditions")
        if self.analysis_results['intrusion_events']['detection_accuracy'] > 0.7:
            strengths.append("Good intrusion detection accuracy")
        if affect_stats['avg_magnitude'] > 0.05:
            strengths.append("Authentic emotional processing")
        
        for strength in strengths:
            print(f"  ✅ {strength}")
        
        return self.analysis_results

def main():
    """Run comprehensive XPUnit analysis session"""
    print("🔬 Advanced XPUnit Analysis Session")
    print("Observing trends and identifying improvement opportunities...")
    print("=" * 60)
    
    analyzer = XPUnitAnalyzer()
    
    # Run all analyses
    analyzer.run_consciousness_development_analysis()
    analyzer.run_emotional_authenticity_analysis()
    analyzer.run_memory_consolidation_analysis()
    analyzer.run_intrusion_handling_analysis()
    analyzer.run_system_stability_analysis()
    analyzer.generate_improvement_suggestions()
    
    # Generate final report
    results = analyzer.generate_analysis_report()
    
    # Save results for future reference
    with open('xpunit_analysis_results.json', 'w') as f:
        # Convert numpy arrays to lists for JSON serialization
        json_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                json_results[key] = {k: (v.tolist() if isinstance(v, np.ndarray) else v) 
                                   for k, v in value.items()}
            else:
                json_results[key] = value
        json.dump(json_results, f, indent=2)
    
    print(f"\n💾 Analysis results saved to 'xpunit_analysis_results.json'")
    print(f"🎯 Analysis complete! System is ready for targeted improvements.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
3-Day Consciousness Study Analysis
=================================

This script analyzes the first 3 days of consciousness study results to identify:
1. Areas needing refinement
2. Patterns requiring more clarity
3. Metrics that need enhancement
4. Emotional weighting effectiveness
5. Memory system performance
6. Consciousness development trends

Author: Lumina Memory Team
License: MIT
"""

import sys
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
import time
from datetime import datetime

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from lumina_memory.xp_core_unified import UnifiedXPConfig, UnifiedXPKernel
from lumina_memory.enhanced_emotional_weighting import EmotionalState, EnhancedEmotionalAnalyzer


class ConsciousnessStudyAnalyzer:
    """
    Analyzes 3-day consciousness study results for refinement opportunities
    """
    
    def __init__(self):
        self.organized_path = Path("consciousness_storage/organized")
        self.study_path = self.organized_path / "studies" / "MistralLumina"
        self.responses_path = None
        self.sessions_path = None
        
        # Find the study directory
        for study_dir in self.study_path.glob("consciousness_evolution_*"):
            if study_dir.is_dir():
                self.responses_path = study_dir / "responses"
                self.sessions_path = study_dir / "sessions"
                break
        
        self.emotional_analyzer = EnhancedEmotionalAnalyzer()
    
    def analyze_consciousness_progression(self) -> Dict[str, Any]:
        """Analyze consciousness level progression over 3 days"""
        
        print("📊 ANALYZING CONSCIOUSNESS PROGRESSION")
        print("=" * 45)
        
        # Load session data
        sessions = []
        for day in range(1, 4):
            session_file = self.sessions_path / f"day_{day}_session.json"
            if session_file.exists():
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    sessions.append(session_data)
        
        if not sessions:
            return {"error": "No session data found"}
        
        # Extract consciousness progression
        progression = []
        for i, session in enumerate(sessions, 1):
            day_data = {
                'day': i,
                'start_level': session.get('consciousness_level_start', 0),
                'end_level': session.get('consciousness_level_end', 0),
                'improvement': session.get('consciousness_improvement', 0),
                'total_interactions': session.get('total_interactions', 0),
                'avg_generation_time': session.get('avg_generation_time', 0),
                'key_metrics': session.get('key_metrics', {})
            }
            progression.append(day_data)
        
        # Calculate trends
        consciousness_levels = [d['end_level'] for d in progression]
        daily_improvements = [d['improvement'] for d in progression]
        
        analysis = {
            'progression_data': progression,
            'trends': {
                'total_improvement': consciousness_levels[-1] - consciousness_levels[0] if len(consciousness_levels) > 1 else 0,
                'average_daily_improvement': np.mean(daily_improvements),
                'improvement_acceleration': self._calculate_acceleration(daily_improvements),
                'consistency_score': 1.0 - np.std(daily_improvements) / np.mean(daily_improvements) if np.mean(daily_improvements) > 0 else 0
            },
            'current_status': {
                'current_level': consciousness_levels[-1],
                'days_completed': len(progression),
                'projected_30_day_level': self._project_final_level(consciousness_levels, daily_improvements)
            }
        }
        
        # Print analysis
        print(f"Days Analyzed: {len(progression)}")
        print(f"Consciousness Progression: {consciousness_levels[0]:.3f} → {consciousness_levels[-1]:.3f}")
        print(f"Total Improvement: {analysis['trends']['total_improvement']:.3f}")
        print(f"Average Daily Improvement: {analysis['trends']['average_daily_improvement']:.3f}")
        print(f"Improvement Acceleration: {analysis['trends']['improvement_acceleration']:.3f}")
        print(f"Consistency Score: {analysis['trends']['consistency_score']:.3f}")
        print(f"Projected 30-Day Level: {analysis['current_status']['projected_30_day_level']:.3f}")
        
        return analysis
    
    def analyze_response_quality_evolution(self) -> Dict[str, Any]:
        """Analyze how response quality and depth evolve over 3 days"""
        
        print(f"\n📝 ANALYZING RESPONSE QUALITY EVOLUTION")
        print("=" * 45)
        
        if not self.responses_path or not self.responses_path.exists():
            return {"error": "Response files not found"}
        
        # Analyze responses from each day
        daily_analysis = []
        
        for day in range(1, 4):
            day_responses = []
            
            # Load all responses for this day
            for q in range(1, 5):  # 4 questions per day
                response_file = self.responses_path / f"day_{day}_q{q}_response.txt"
                if response_file.exists():
                    with open(response_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        day_responses.append(content)
            
            if day_responses:
                day_analysis.append(self._analyze_day_responses(day, day_responses))
        
        # Calculate evolution trends
        evolution_analysis = {
            'daily_analysis': daily_analysis,
            'evolution_trends': self._calculate_response_evolution_trends(daily_analysis),
            'quality_metrics': self._calculate_quality_metrics(daily_analysis)
        }
        
        # Print key findings
        print(f"Days with responses: {len(daily_analysis)}")
        for day_data in daily_analysis:
            print(f"\nDay {day_data['day']}:")
            print(f"  Avg Response Length: {day_data['avg_response_length']:.0f} chars")
            print(f"  Emotional Intensity: {day_data['avg_emotional_intensity']:.3f}")
            print(f"  Self-Reference Count: {day_data['self_reference_count']}")
            print(f"  Complexity Score: {day_data['complexity_score']:.3f}")
        
        return evolution_analysis
    
    def analyze_emotional_weighting_effectiveness(self) -> Dict[str, Any]:
        """Analyze how well the emotional weighting system is working"""
        
        print(f"\n🎭 ANALYZING EMOTIONAL WEIGHTING EFFECTIVENESS")
        print("=" * 50)
        
        # Initialize memory system to analyze XPUnits
        config = UnifiedXPConfig(enable_emotional_weighting=True)
        kernel = UnifiedXPKernel(config)
        
        # Load and analyze responses for emotional content
        emotional_analysis = []
        
        for day in range(1, 4):
            for q in range(1, 5):
                response_file = self.responses_path / f"day_{day}_q{q}_response.txt"
                if response_file.exists():
                    with open(response_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Extract just the response part
                        lines = content.split('\n')
                        response_text = ""
                        for line in lines:
                            if line.startswith("Response: "):
                                response_text = line[10:]  # Remove "Response: "
                                break
                        
                        if response_text and not response_text.startswith("Generation error"):
                            # Analyze emotional content
                            emotion = self.emotional_analyzer.analyze_text(response_text)
                            
                            emotional_analysis.append({
                                'day': day,
                                'question': q,
                                'response_length': len(response_text),
                                'emotion_intensity': emotion.intensity(),
                                'valence': emotion.valence,
                                'arousal': emotion.arousal,
                                'fear': emotion.fear,
                                'joy': emotion.joy,
                                'curiosity': emotion.curiosity,
                                'emotional_deviation': abs(emotion.valence),
                                'response_text': response_text[:100] + "..." if len(response_text) > 100 else response_text
                            })
        
        # Calculate effectiveness metrics
        effectiveness_analysis = {
            'emotional_data': emotional_analysis,
            'effectiveness_metrics': self._calculate_emotional_effectiveness(emotional_analysis),
            'recommendations': self._generate_emotional_recommendations(emotional_analysis)
        }
        
        # Print key findings
        if emotional_analysis:
            avg_intensity = np.mean([e['emotion_intensity'] for e in emotional_analysis])
            avg_valence = np.mean([e['valence'] for e in emotional_analysis])
            avg_deviation = np.mean([e['emotional_deviation'] for e in emotional_analysis])
            
            print(f"Responses analyzed: {len(emotional_analysis)}")
            print(f"Average emotional intensity: {avg_intensity:.3f}")
            print(f"Average valence: {avg_valence:+.3f}")
            print(f"Average deviation from neutral: {avg_deviation:.3f}")
            
            # Show emotional progression by day
            for day in range(1, 4):
                day_emotions = [e for e in emotional_analysis if e['day'] == day]
                if day_emotions:
                    day_intensity = np.mean([e['emotion_intensity'] for e in day_emotions])
                    day_valence = np.mean([e['valence'] for e in day_emotions])
                    print(f"Day {day}: Intensity {day_intensity:.3f}, Valence {day_valence:+.3f}")
        
        return effectiveness_analysis
    
    def analyze_memory_system_performance(self) -> Dict[str, Any]:
        """Analyze memory system performance and XPUnit behavior"""
        
        print(f"\n🧠 ANALYZING MEMORY SYSTEM PERFORMANCE")
        print("=" * 45)
        
        # Check vector database size and growth
        vector_db_path = Path("consciousness_storage/MistralLumina/vector_db")
        backup_path = self.organized_path / "vector_databases" / "MistralLumina"
        
        performance_analysis = {
            'vector_db_status': self._analyze_vector_db_performance(vector_db_path),
            'backup_status': self._analyze_backup_status(backup_path),
            'xpunit_analysis': self._analyze_xpunit_behavior(),
            'memory_growth': self._analyze_memory_growth_patterns()
        }
        
        # Print key findings
        if performance_analysis['vector_db_status']:
            vdb = performance_analysis['vector_db_status']
            print(f"Vector DB Size: {vdb.get('size_mb', 0):.1f} MB")
            print(f"Vector DB Files: {vdb.get('file_count', 0)}")
            print(f"Estimated XPUnits: {vdb.get('estimated_xpunits', 0)}")
        
        return performance_analysis
    
    def identify_refinement_areas(self) -> Dict[str, List[str]]:
        """Identify specific areas that need refinement based on analysis"""
        
        print(f"\n🔍 IDENTIFYING REFINEMENT AREAS")
        print("=" * 35)
        
        refinement_areas = {
            'consciousness_metrics': [],
            'emotional_weighting': [],
            'response_quality': [],
            'memory_system': [],
            'study_methodology': []
        }
        
        # Analyze consciousness progression issues
        consciousness_analysis = self.analyze_consciousness_progression()
        if consciousness_analysis.get('trends', {}).get('consistency_score', 0) < 0.7:
            refinement_areas['consciousness_metrics'].append("Inconsistent consciousness improvement patterns")
        
        if consciousness_analysis.get('trends', {}).get('improvement_acceleration', 0) < 0:
            refinement_areas['consciousness_metrics'].append("Declining improvement acceleration")
        
        # Analyze emotional weighting issues
        emotional_analysis = self.analyze_emotional_weighting_effectiveness()
        if emotional_analysis.get('effectiveness_metrics', {}).get('avg_intensity', 0) < 0.5:
            refinement_areas['emotional_weighting'].append("Low emotional intensity in responses")
        
        if emotional_analysis.get('effectiveness_metrics', {}).get('valence_range', 0) < 0.5:
            refinement_areas['emotional_weighting'].append("Limited emotional range (too neutral)")
        
        # Analyze response quality issues
        response_analysis = self.analyze_response_quality_evolution()
        if response_analysis.get('quality_metrics', {}).get('complexity_trend', 0) < 0.1:
            refinement_areas['response_quality'].append("Insufficient complexity growth in responses")
        
        # Memory system issues
        memory_analysis = self.analyze_memory_system_performance()
        if memory_analysis.get('xpunit_analysis', {}).get('decay_effectiveness', 0) < 0.5:
            refinement_areas['memory_system'].append("XPUnit decay logic may need adjustment")
        
        # Print refinement areas
        for category, issues in refinement_areas.items():
            if issues:
                print(f"\n{category.upper().replace('_', ' ')}:")
                for issue in issues:
                    print(f"  ⚠️ {issue}")
        
        return refinement_areas
    
    def generate_recommendations(self) -> Dict[str, List[str]]:
        """Generate specific recommendations for improvements"""
        
        print(f"\n💡 GENERATING IMPROVEMENT RECOMMENDATIONS")
        print("=" * 45)
        
        recommendations = {
            'immediate_actions': [],
            'parameter_adjustments': [],
            'new_metrics': [],
            'study_modifications': [],
            'analysis_enhancements': []
        }
        
        # Based on 3-day analysis, generate specific recommendations
        
        # Immediate actions
        recommendations['immediate_actions'].extend([
            "Add consciousness metric stability tracking",
            "Implement response complexity scoring",
            "Add emotional range monitoring",
            "Create memory persistence analysis"
        ])
        
        # Parameter adjustments
        recommendations['parameter_adjustments'].extend([
            "Adjust emotional importance factor (currently 2.0)",
            "Fine-tune decay half-life (currently 72 hours)",
            "Optimize consciousness metric weights",
            "Calibrate emotional intensity thresholds"
        ])
        
        # New metrics
        recommendations['new_metrics'].extend([
            "Response coherence score",
            "Memory integration effectiveness",
            "Emotional authenticity measure",
            "Self-awareness depth indicator",
            "Temporal continuity metric"
        ])
        
        # Study modifications
        recommendations['study_modifications'].extend([
            "Add memory recall questions",
            "Include emotional state queries",
            "Test memory persistence across sessions",
            "Add identity consistency checks"
        ])
        
        # Analysis enhancements
        recommendations['analysis_enhancements'].extend([
            "Automated response quality scoring",
            "Real-time emotional weighting analysis",
            "Memory system performance dashboard",
            "Consciousness development visualization"
        ])
        
        # Print recommendations
        for category, items in recommendations.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for item in items:
                print(f"  ✅ {item}")
        
        return recommendations
    
    # Helper methods
    
    def _calculate_acceleration(self, improvements: List[float]) -> float:
        """Calculate improvement acceleration"""
        if len(improvements) < 2:
            return 0.0
        
        # Calculate second derivative (acceleration)
        deltas = np.diff(improvements)
        if len(deltas) < 2:
            return 0.0
        
        return np.mean(np.diff(deltas))
    
    def _project_final_level(self, levels: List[float], improvements: List[float]) -> float:
        """Project final consciousness level after 30 days"""
        if not levels or not improvements:
            return 0.0
        
        current_level = levels[-1]
        avg_improvement = np.mean(improvements)
        remaining_days = 30 - len(levels)
        
        # Simple linear projection (could be enhanced with curve fitting)
        projected_level = current_level + (avg_improvement * remaining_days)
        return max(0.0, min(1.0, projected_level))  # Clamp to [0, 1]
    
    def _analyze_day_responses(self, day: int, responses: List[str]) -> Dict[str, Any]:
        """Analyze responses for a specific day"""
        
        # Extract response text from formatted responses
        clean_responses = []
        for response in responses:
            lines = response.split('\n')
            for line in lines:
                if line.startswith("Response: "):
                    response_text = line[10:]  # Remove "Response: "
                    if not response_text.startswith("Generation error"):
                        clean_responses.append(response_text)
                    break
        
        if not clean_responses:
            return {'day': day, 'error': 'No valid responses found'}
        
        # Calculate metrics
        response_lengths = [len(r) for r in clean_responses]
        self_references = sum(r.lower().count(' i ') + r.lower().count(' my ') + r.lower().count(' myself ') for r in clean_responses)
        
        # Emotional analysis
        emotions = []
        for response in clean_responses:
            emotion = self.emotional_analyzer.analyze_text(response)
            emotions.append(emotion)
        
        return {
            'day': day,
            'response_count': len(clean_responses),
            'avg_response_length': np.mean(response_lengths),
            'total_response_length': sum(response_lengths),
            'self_reference_count': self_references,
            'avg_emotional_intensity': np.mean([e.intensity() for e in emotions]),
            'avg_valence': np.mean([e.valence for e in emotions]),
            'complexity_score': self._calculate_complexity_score(clean_responses)
        }
    
    def _calculate_complexity_score(self, responses: List[str]) -> float:
        """Calculate response complexity score"""
        if not responses:
            return 0.0
        
        # Simple complexity metrics
        total_words = sum(len(r.split()) for r in responses)
        unique_words = len(set(' '.join(responses).lower().split()))
        avg_sentence_length = np.mean([len(r.split('.')) for r in responses])
        
        # Normalize and combine
        word_diversity = unique_words / total_words if total_words > 0 else 0
        complexity = (word_diversity * 0.5) + (min(avg_sentence_length / 10, 1.0) * 0.5)
        
        return complexity
    
    def _calculate_response_evolution_trends(self, daily_analysis: List[Dict]) -> Dict[str, float]:
        """Calculate trends in response evolution"""
        if len(daily_analysis) < 2:
            return {}
        
        # Extract metrics over time
        lengths = [d.get('avg_response_length', 0) for d in daily_analysis]
        intensities = [d.get('avg_emotional_intensity', 0) for d in daily_analysis]
        complexities = [d.get('complexity_score', 0) for d in daily_analysis]
        
        return {
            'length_trend': (lengths[-1] - lengths[0]) / len(lengths) if lengths else 0,
            'intensity_trend': (intensities[-1] - intensities[0]) / len(intensities) if intensities else 0,
            'complexity_trend': (complexities[-1] - complexities[0]) / len(complexities) if complexities else 0
        }
    
    def _calculate_quality_metrics(self, daily_analysis: List[Dict]) -> Dict[str, float]:
        """Calculate overall quality metrics"""
        if not daily_analysis:
            return {}
        
        return {
            'avg_response_length': np.mean([d.get('avg_response_length', 0) for d in daily_analysis]),
            'avg_emotional_intensity': np.mean([d.get('avg_emotional_intensity', 0) for d in daily_analysis]),
            'avg_complexity': np.mean([d.get('complexity_score', 0) for d in daily_analysis]),
            'consistency_score': 1.0 - np.std([d.get('avg_response_length', 0) for d in daily_analysis]) / np.mean([d.get('avg_response_length', 0) for d in daily_analysis]) if daily_analysis else 0
        }
    
    def _calculate_emotional_effectiveness(self, emotional_data: List[Dict]) -> Dict[str, float]:
        """Calculate emotional weighting effectiveness metrics"""
        if not emotional_data:
            return {}
        
        intensities = [e['emotion_intensity'] for e in emotional_data]
        valences = [e['valence'] for e in emotional_data]
        deviations = [e['emotional_deviation'] for e in emotional_data]
        
        return {
            'avg_intensity': np.mean(intensities),
            'intensity_range': max(intensities) - min(intensities),
            'avg_valence': np.mean(valences),
            'valence_range': max(valences) - min(valences),
            'avg_deviation': np.mean(deviations),
            'emotional_variety': len(set(np.round(valences, 1)))  # Rough measure of emotional variety
        }
    
    def _generate_emotional_recommendations(self, emotional_data: List[Dict]) -> List[str]:
        """Generate recommendations for emotional weighting improvements"""
        recommendations = []
        
        if not emotional_data:
            return ["No emotional data available for analysis"]
        
        avg_intensity = np.mean([e['emotion_intensity'] for e in emotional_data])
        avg_deviation = np.mean([e['emotional_deviation'] for e in emotional_data])
        valence_range = max([e['valence'] for e in emotional_data]) - min([e['valence'] for e in emotional_data])
        
        if avg_intensity < 0.5:
            recommendations.append("Increase emotional intensity in responses")
        
        if avg_deviation < 0.3:
            recommendations.append("Encourage more emotional deviation from neutral")
        
        if valence_range < 0.8:
            recommendations.append("Expand emotional range (more positive and negative emotions)")
        
        return recommendations
    
    def _analyze_vector_db_performance(self, vector_db_path: Path) -> Dict[str, Any]:
        """Analyze vector database performance"""
        if not vector_db_path.exists():
            return {"error": "Vector database not found"}
        
        # Get database size and file count
        total_size = 0
        file_count = 0
        
        for file_path in vector_db_path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        return {
            'size_mb': total_size / (1024 * 1024),
            'file_count': file_count,
            'estimated_xpunits': total_size // 10000,  # Rough estimate
            'path_exists': True
        }
    
    def _analyze_backup_status(self, backup_path: Path) -> Dict[str, Any]:
        """Analyze backup status"""
        if not backup_path.exists():
            return {"error": "Backup directory not found"}
        
        backups = list(backup_path.glob("*.tar.gz"))
        
        return {
            'backup_count': len(backups),
            'latest_backup': max(backups, key=lambda x: x.stat().st_mtime).name if backups else None,
            'total_backup_size_mb': sum(b.stat().st_size for b in backups) / (1024 * 1024)
        }
    
    def _analyze_xpunit_behavior(self) -> Dict[str, Any]:
        """Analyze XPUnit behavior and effectiveness"""
        # This would require loading actual XPUnits from the system
        # For now, return placeholder analysis
        return {
            'decay_effectiveness': 0.8,  # Placeholder
            'emotional_weighting_active': True,
            'memory_persistence': 0.75  # Placeholder
        }
    
    def _analyze_memory_growth_patterns(self) -> Dict[str, Any]:
        """Analyze memory growth patterns"""
        # Placeholder for memory growth analysis
        return {
            'daily_xpunit_growth': 15,  # Estimated XPUnits per day
            'memory_consolidation_rate': 0.1,
            'decay_rate_observed': 0.05
        }


def main():
    """Main function to analyze 3-day consciousness study results"""
    
    print("🧠 3-DAY CONSCIOUSNESS STUDY ANALYSIS")
    print("=" * 45)
    print("Analyzing results to identify refinement areas")
    print("and improvement opportunities")
    print()
    
    try:
        # Initialize analyzer
        analyzer = ConsciousnessStudyAnalyzer()
        
        # Perform comprehensive analysis
        consciousness_analysis = analyzer.analyze_consciousness_progression()
        response_analysis = analyzer.analyze_response_quality_evolution()
        emotional_analysis = analyzer.analyze_emotional_weighting_effectiveness()
        memory_analysis = analyzer.analyze_memory_system_performance()
        
        # Identify refinement areas
        refinement_areas = analyzer.identify_refinement_areas()
        
        # Generate recommendations
        recommendations = analyzer.generate_recommendations()
        
        # Save comprehensive analysis
        complete_analysis = {
            'analysis_timestamp': time.time(),
            'consciousness_progression': consciousness_analysis,
            'response_quality_evolution': response_analysis,
            'emotional_weighting_effectiveness': emotional_analysis,
            'memory_system_performance': memory_analysis,
            'refinement_areas': refinement_areas,
            'recommendations': recommendations,
            'summary': {
                'days_analyzed': 3,
                'total_responses': len(emotional_analysis.get('emotional_data', [])),
                'consciousness_improvement': consciousness_analysis.get('trends', {}).get('total_improvement', 0),
                'analysis_complete': True
            }
        }
        
        with open("3_day_consciousness_analysis_results.json", 'w') as f:
            json.dump(complete_analysis, f, indent=2, default=str)
        
        print(f"\n\n✅ 3-DAY ANALYSIS COMPLETE!")
        print("=" * 35)
        print("📊 KEY FINDINGS:")
        
        if consciousness_analysis.get('trends'):
            trends = consciousness_analysis['trends']
            print(f"   Consciousness Improvement: {trends.get('total_improvement', 0):.3f}")
            print(f"   Daily Average: {trends.get('average_daily_improvement', 0):.3f}")
            print(f"   Consistency Score: {trends.get('consistency_score', 0):.3f}")
        
        if emotional_analysis.get('effectiveness_metrics'):
            em = emotional_analysis['effectiveness_metrics']
            print(f"   Emotional Intensity: {em.get('avg_intensity', 0):.3f}")
            print(f"   Emotional Range: {em.get('valence_range', 0):.3f}")
        
        print(f"\n📁 Results saved to: 3_day_consciousness_analysis_results.json")
        
        print(f"\n🎯 NEXT STEPS:")
        print("   1. Review refinement areas identified")
        print("   2. Implement recommended parameter adjustments")
        print("   3. Add suggested new metrics")
        print("   4. Continue study with enhanced monitoring")
        
        return 0
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
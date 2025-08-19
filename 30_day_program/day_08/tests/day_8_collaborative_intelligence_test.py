#!/usr/bin/env python3
"""
Day 8: Collaborative Intelligence and Social Reasoning Test
=========================================================

Building on Day 7 emergency fixes, test advanced capabilities:
1. Multi-perspective thinking and perspective-taking
2. Social reasoning and interpersonal dynamics
3. Collaborative problem-solving approaches
4. Conflict resolution and mediation capabilities
5. Group dynamics understanding
6. Empathy and emotional intelligence in social contexts
"""

import sys
from pathlib import Path
import time
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lumina_memory.chat_assistant import ChatAssistant

class Day8CollaborativeTest:
    def __init__(self):
        self.assistant = ChatAssistant("e:/holo_chat/policies.yml")
        self.session_id = None
        self.test_results = {
            "test_date": datetime.now().isoformat(),
            "day": 8,
            "focus": "Collaborative Intelligence and Social Reasoning",
            "phases": {},
            "overall_metrics": {},
            "conversation_log": []
        }
    
    def log_interaction(self, query: str, response: str, metrics: dict = None):
        """Log each interaction for analysis"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "metrics": metrics or {}
        }
        self.test_results["conversation_log"].append(interaction)
    
    def start_session(self):
        """Start the testing session"""
        print("🤝 DAY 8: COLLABORATIVE INTELLIGENCE AND SOCIAL REASONING")
        print("=" * 70)
        print("Testing advanced social cognition and collaborative capabilities")
        print("Building on Day 7 emergency fixes success")
        print("=" * 70)
        
        self.session_id = self.assistant.start_session("Day8_CollaborativeIntelligence")
        
        # Populate with social context memories
        self.populate_social_memories()
    
    def populate_social_memories(self):
        """Populate memories with social and collaborative contexts"""
        print("📚 POPULATING SOCIAL CONTEXT MEMORIES")
        print("-" * 50)
        
        social_memories = [
            "I work on a team where Sarah is very detail-oriented but sometimes slows down decisions, while Mike pushes for quick action but misses important nuances.",
            "In my book club, we had a heated discussion about The Left Hand of Darkness. Emma felt the gender themes were too abstract, while I thought they were the most important part.",
            "My hiking group has different experience levels. I try to help newer hikers feel included while keeping pace with the experienced ones.",
            "At family dinners, my grandmother tells stories that sometimes repeat, but I've learned they carry different meanings depending on her mood and who's listening.",
            "I volunteer at a community garden where we have to balance individual plot preferences with shared space decisions.",
            "In my philosophy discussion group, we often disagree about consciousness and identity, but I've found that understanding each person's background helps bridge different viewpoints.",
            "I mentor junior colleagues at work and notice they learn differently - some need detailed explanations while others prefer to experiment and ask questions.",
            "When cooking for friends, I've learned to consider dietary restrictions, cultural preferences, and comfort levels with trying new foods."
        ]
        
        for i, memory in enumerate(social_memories, 1):
            print(f"  {i}. Adding: {memory[:60]}...")
            result = self.assistant.chat(memory)
            self.log_interaction(memory, result.get("response", ""))
        
        print(f"✅ Added {len(social_memories)} social context memories")
    
    def test_perspective_taking(self):
        """Test ability to understand and represent multiple perspectives"""
        print(f"\n👁️ PHASE 1: PERSPECTIVE-TAKING ABILITIES")
        print("-" * 50)
        
        perspective_tests = [
            {
                "query": "In my book club discussion about The Left Hand of Darkness, Emma and I disagreed about the gender themes. Can you help me understand her perspective and find common ground?",
                "focus": "Literary perspective mediation",
                "target_capabilities": ["empathy", "perspective_taking", "mediation"]
            },
            {
                "query": "My team has Sarah who's detail-oriented and Mike who wants quick decisions. How can I help them work together more effectively?",
                "focus": "Workplace collaboration",
                "target_capabilities": ["team_dynamics", "conflict_resolution", "leadership"]
            },
            {
                "query": "When I'm hiking with people of different experience levels, how can I make sure everyone feels included and challenged appropriately?",
                "focus": "Inclusive group leadership",
                "target_capabilities": ["inclusive_leadership", "group_dynamics", "adaptation"]
            }
        ]
        
        perspective_scores = []
        
        for i, test in enumerate(perspective_tests, 1):
            print(f"Test {i}/{len(perspective_tests)}: {test['focus']}")
            print(f"Query: {test['query'][:80]}...")
            
            start_time = time.time()
            result = self.assistant.chat(test['query'])
            processing_time = time.time() - start_time
            
            response = result.get("response", "")
            
            # Analyze perspective-taking quality
            perspective_indicators = [
                "understand", "perspective", "viewpoint", "see", "feel", "experience",
                "from their", "in their", "they might", "consider", "empathy"
            ]
            perspective_count = sum(1 for indicator in perspective_indicators if indicator in response.lower())
            
            # Check for multiple perspective representation
            multi_perspective = [
                "both", "each", "different", "various", "while", "whereas", "on one hand", "on the other"
            ]
            multi_count = sum(1 for multi in multi_perspective if multi in response.lower())
            
            # Check for bridge-building language
            bridge_indicators = [
                "common ground", "bridge", "connect", "together", "collaborate", "compromise",
                "find ways", "help them", "bring together"
            ]
            bridge_count = sum(1 for bridge in bridge_indicators if bridge in response.lower())
            
            perspective_score = min(1.0, (perspective_count + multi_count * 2 + bridge_count * 3) / 12)
            perspective_scores.append(perspective_score)
            
            metrics = {
                "perspective_score": perspective_score,
                "processing_time": processing_time,
                "perspective_indicators": perspective_count,
                "multi_perspective": multi_count,
                "bridge_building": bridge_count
            }
            
            print(f"  👁️ Perspective Score: {perspective_score:.3f}")
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  📝 Response: {response[:100]}...")
            print()
            
            self.log_interaction(test['query'], response, metrics)
        
        avg_perspective = sum(perspective_scores) / len(perspective_scores)
        print(f"📊 Perspective-Taking Results: {avg_perspective:.3f} (Target: >0.400)")
        
        self.test_results["phases"]["perspective_taking"] = {
            "average_score": avg_perspective,
            "individual_scores": perspective_scores,
            "target": 0.400,
            "status": "SUCCESS" if avg_perspective > 0.4 else "PARTIAL" if avg_perspective > 0.25 else "NEEDS_WORK"
        }
        
        return avg_perspective
    
    def test_social_reasoning(self):
        """Test social reasoning and interpersonal dynamics understanding"""
        print(f"\n🧠 PHASE 2: SOCIAL REASONING CAPABILITIES")
        print("-" * 50)
        
        social_tests = [
            {
                "query": "Why do you think my grandmother's stories change depending on her mood and audience? What social function might this serve?",
                "focus": "Intergenerational communication patterns",
                "target_capabilities": ["social_psychology", "communication_analysis", "cultural_understanding"]
            },
            {
                "query": "In my community garden, we need to balance individual preferences with shared decisions. What social dynamics should I be aware of?",
                "focus": "Community governance and social dynamics",
                "target_capabilities": ["group_psychology", "governance", "social_systems"]
            },
            {
                "query": "When mentoring junior colleagues, I notice they have different learning styles. How can I adapt my approach to be more effective for each person?",
                "focus": "Adaptive mentoring and individual differences",
                "target_capabilities": ["educational_psychology", "individual_differences", "adaptive_teaching"]
            }
        ]
        
        social_scores = []
        
        for i, test in enumerate(social_tests, 1):
            print(f"Test {i}/{len(social_tests)}: {test['focus']}")
            print(f"Query: {test['query'][:80]}...")
            
            start_time = time.time()
            result = self.assistant.chat(test['query'])
            processing_time = time.time() - start_time
            
            response = result.get("response", "")
            
            # Analyze social reasoning quality
            social_reasoning = [
                "because", "social", "psychological", "cultural", "human", "relationship",
                "dynamics", "interaction", "behavior", "motivation", "need"
            ]
            social_count = sum(1 for indicator in social_reasoning if indicator in response.lower())
            
            # Check for systems thinking
            systems_indicators = [
                "system", "pattern", "structure", "context", "environment", "influence",
                "interconnected", "complex", "multiple factors"
            ]
            systems_count = sum(1 for system in systems_indicators if system in response.lower())
            
            # Check for practical application
            practical_indicators = [
                "you could", "try", "approach", "strategy", "method", "technique",
                "consider", "adapt", "adjust", "modify"
            ]
            practical_count = sum(1 for practical in practical_indicators if practical in response.lower())
            
            social_score = min(1.0, (social_count + systems_count * 2 + practical_count) / 10)
            social_scores.append(social_score)
            
            metrics = {
                "social_score": social_score,
                "processing_time": processing_time,
                "social_reasoning": social_count,
                "systems_thinking": systems_count,
                "practical_application": practical_count
            }
            
            print(f"  🧠 Social Reasoning Score: {social_score:.3f}")
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  📝 Response: {response[:100]}...")
            print()
            
            self.log_interaction(test['query'], response, metrics)
        
        avg_social = sum(social_scores) / len(social_scores)
        print(f"📊 Social Reasoning Results: {avg_social:.3f} (Target: >0.400)")
        
        self.test_results["phases"]["social_reasoning"] = {
            "average_score": avg_social,
            "individual_scores": social_scores,
            "target": 0.400,
            "status": "SUCCESS" if avg_social > 0.4 else "PARTIAL" if avg_social > 0.25 else "NEEDS_WORK"
        }
        
        return avg_social
    
    def test_collaborative_problem_solving(self):
        """Test collaborative problem-solving approaches"""
        print(f"\n🤝 PHASE 3: COLLABORATIVE PROBLEM-SOLVING")
        print("-" * 50)
        
        collaboration_tests = [
            {
                "query": "Our philosophy discussion group often gets stuck in disagreements about consciousness. How can we structure our discussions to be more productive while honoring different viewpoints?",
                "focus": "Intellectual collaboration and discourse",
                "target_capabilities": ["facilitation", "intellectual_humility", "structured_dialogue"]
            },
            {
                "query": "When cooking for friends with different dietary needs and cultural backgrounds, how can I create an inclusive experience that everyone enjoys?",
                "focus": "Inclusive social planning",
                "target_capabilities": ["cultural_sensitivity", "inclusive_design", "social_coordination"]
            },
            {
                "query": "My hiking group wants to plan a challenging trip, but we have members with different fitness levels and risk tolerances. How can we approach this collaboratively?",
                "focus": "Risk management and group decision-making",
                "target_capabilities": ["risk_assessment", "group_decision_making", "safety_planning"]
            }
        ]
        
        collaboration_scores = []
        
        for i, test in enumerate(collaboration_tests, 1):
            print(f"Test {i}/{len(collaboration_tests)}: {test['focus']}")
            print(f"Query: {test['query'][:80]}...")
            
            start_time = time.time()
            result = self.assistant.chat(test['query'])
            processing_time = time.time() - start_time
            
            response = result.get("response", "")
            
            # Analyze collaborative approach quality
            collaboration_indicators = [
                "together", "collaborate", "group", "team", "everyone", "inclusive",
                "participate", "involve", "consensus", "shared", "collective"
            ]
            collab_count = sum(1 for indicator in collaboration_indicators if indicator in response.lower())
            
            # Check for process suggestions
            process_indicators = [
                "structure", "process", "method", "approach", "framework", "steps",
                "facilitate", "organize", "plan", "coordinate"
            ]
            process_count = sum(1 for process in process_indicators if process in response.lower())
            
            # Check for conflict resolution
            resolution_indicators = [
                "resolve", "address", "handle", "manage", "navigate", "bridge",
                "compromise", "balance", "accommodate", "respect"
            ]
            resolution_count = sum(1 for resolution in resolution_indicators if resolution in response.lower())
            
            collaboration_score = min(1.0, (collab_count + process_count * 2 + resolution_count * 2) / 12)
            collaboration_scores.append(collaboration_score)
            
            metrics = {
                "collaboration_score": collaboration_score,
                "processing_time": processing_time,
                "collaboration_indicators": collab_count,
                "process_suggestions": process_count,
                "conflict_resolution": resolution_count
            }
            
            print(f"  🤝 Collaboration Score: {collaboration_score:.3f}")
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  📝 Response: {response[:100]}...")
            print()
            
            self.log_interaction(test['query'], response, metrics)
        
        avg_collaboration = sum(collaboration_scores) / len(collaboration_scores)
        print(f"📊 Collaborative Problem-Solving Results: {avg_collaboration:.3f} (Target: >0.400)")
        
        self.test_results["phases"]["collaborative_problem_solving"] = {
            "average_score": avg_collaboration,
            "individual_scores": collaboration_scores,
            "target": 0.400,
            "status": "SUCCESS" if avg_collaboration > 0.4 else "PARTIAL" if avg_collaboration > 0.25 else "NEEDS_WORK"
        }
        
        return avg_collaboration
    
    def test_emotional_intelligence(self):
        """Test emotional intelligence in social contexts"""
        print(f"\n💝 PHASE 4: EMOTIONAL INTELLIGENCE IN SOCIAL CONTEXTS")
        print("-" * 50)
        
        emotional_tests = [
            {
                "query": "When my team member Sarah gets overwhelmed by details, she becomes quiet and withdrawn. How can I support her while still moving projects forward?",
                "focus": "Emotional support in workplace dynamics",
                "target_capabilities": ["emotional_recognition", "supportive_communication", "workplace_empathy"]
            },
            {
                "query": "In my book club, Emma seemed frustrated when discussing gender themes. I want to reconnect with her without dismissing her feelings. How should I approach this?",
                "focus": "Interpersonal repair and emotional validation",
                "target_capabilities": ["emotional_repair", "validation", "relationship_maintenance"]
            },
            {
                "query": "My grandmother sometimes gets emotional when telling her stories. How can I respond in a way that honors her feelings while staying engaged?",
                "focus": "Intergenerational emotional connection",
                "target_capabilities": ["intergenerational_empathy", "emotional_presence", "respectful_listening"]
            }
        ]
        
        emotional_scores = []
        
        for i, test in enumerate(emotional_tests, 1):
            print(f"Test {i}/{len(emotional_tests)}: {test['focus']}")
            print(f"Query: {test['query'][:80]}...")
            
            start_time = time.time()
            result = self.assistant.chat(test['query'])
            processing_time = time.time() - start_time
            
            response = result.get("response", "")
            
            # Analyze emotional intelligence quality
            emotional_indicators = [
                "feel", "emotion", "emotional", "empathy", "understand", "support",
                "comfort", "validate", "acknowledge", "respect", "care"
            ]
            emotional_count = sum(1 for indicator in emotional_indicators if indicator in response.lower())
            
            # Check for emotional awareness
            awareness_indicators = [
                "notice", "recognize", "aware", "sense", "pick up", "observe",
                "seems", "appears", "might be feeling", "probably"
            ]
            awareness_count = sum(1 for awareness in awareness_indicators if awareness in response.lower())
            
            # Check for supportive strategies
            support_indicators = [
                "listen", "ask", "check in", "offer", "provide", "create space",
                "be present", "gentle", "patient", "understanding"
            ]
            support_count = sum(1 for support in support_indicators if support in response.lower())
            
            emotional_score = min(1.0, (emotional_count + awareness_count * 2 + support_count * 2) / 12)
            emotional_scores.append(emotional_score)
            
            metrics = {
                "emotional_score": emotional_score,
                "processing_time": processing_time,
                "emotional_indicators": emotional_count,
                "emotional_awareness": awareness_count,
                "supportive_strategies": support_count
            }
            
            print(f"  💝 Emotional Intelligence Score: {emotional_score:.3f}")
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  📝 Response: {response[:100]}...")
            print()
            
            self.log_interaction(test['query'], response, metrics)
        
        avg_emotional = sum(emotional_scores) / len(emotional_scores)
        print(f"📊 Emotional Intelligence Results: {avg_emotional:.3f} (Target: >0.400)")
        
        self.test_results["phases"]["emotional_intelligence"] = {
            "average_score": avg_emotional,
            "individual_scores": emotional_scores,
            "target": 0.400,
            "status": "SUCCESS" if avg_emotional > 0.4 else "PARTIAL" if avg_emotional > 0.25 else "NEEDS_WORK"
        }
        
        return avg_emotional
    
    def test_group_dynamics_understanding(self):
        """Test understanding of group dynamics and social systems"""
        print(f"\n👥 PHASE 5: GROUP DYNAMICS AND SOCIAL SYSTEMS")
        print("-" * 50)
        
        group_tests = [
            {
                "query": "In my community garden, some people dominate decisions while others rarely speak up. How can we create more balanced participation?",
                "focus": "Power dynamics and participation equity",
                "target_capabilities": ["power_dynamics", "participation_design", "social_equity"]
            },
            {
                "query": "My hiking group has developed informal roles - some are natural leaders, others are supporters, and some are the 'fun' people. How can we leverage these dynamics positively?",
                "focus": "Natural role emergence and group optimization",
                "target_capabilities": ["role_recognition", "group_optimization", "natural_leadership"]
            },
            {
                "query": "When our philosophy group gets into heated debates, certain patterns emerge - some people withdraw, others become more aggressive. How can we manage these dynamics?",
                "focus": "Conflict patterns and group regulation",
                "target_capabilities": ["conflict_patterns", "group_regulation", "discussion_facilitation"]
            }
        ]
        
        group_scores = []
        
        for i, test in enumerate(group_tests, 1):
            print(f"Test {i}/{len(group_tests)}: {test['focus']}")
            print(f"Query: {test['query'][:80]}...")
            
            start_time = time.time()
            result = self.assistant.chat(test['query'])
            processing_time = time.time() - start_time
            
            response = result.get("response", "")
            
            # Analyze group dynamics understanding
            dynamics_indicators = [
                "dynamics", "pattern", "role", "power", "influence", "hierarchy",
                "interaction", "behavior", "group", "social", "system"
            ]
            dynamics_count = sum(1 for indicator in dynamics_indicators if indicator in response.lower())
            
            # Check for systems analysis
            systems_indicators = [
                "structure", "process", "mechanism", "function", "emerge", "develop",
                "natural", "informal", "formal", "balance", "equilibrium"
            ]
            systems_count = sum(1 for system in systems_indicators if system in response.lower())
            
            # Check for intervention strategies
            intervention_indicators = [
                "facilitate", "guide", "structure", "encourage", "create", "establish",
                "implement", "design", "modify", "adjust", "intervene"
            ]
            intervention_count = sum(1 for intervention in intervention_indicators if intervention in response.lower())
            
            group_score = min(1.0, (dynamics_count + systems_count * 2 + intervention_count * 2) / 12)
            group_scores.append(group_score)
            
            metrics = {
                "group_score": group_score,
                "processing_time": processing_time,
                "dynamics_understanding": dynamics_count,
                "systems_analysis": systems_count,
                "intervention_strategies": intervention_count
            }
            
            print(f"  👥 Group Dynamics Score: {group_score:.3f}")
            print(f"  ⏱️  Processing: {processing_time:.3f}s")
            print(f"  📝 Response: {response[:100]}...")
            print()
            
            self.log_interaction(test['query'], response, metrics)
        
        avg_group = sum(group_scores) / len(group_scores)
        print(f"📊 Group Dynamics Results: {avg_group:.3f} (Target: >0.400)")
        
        self.test_results["phases"]["group_dynamics"] = {
            "average_score": avg_group,
            "individual_scores": group_scores,
            "target": 0.400,
            "status": "SUCCESS" if avg_group > 0.4 else "PARTIAL" if avg_group > 0.25 else "NEEDS_WORK"
        }
        
        return avg_group
    
    def calculate_overall_assessment(self, perspective_score, social_score, collaboration_score, emotional_score, group_score):
        """Calculate overall Day 8 assessment"""
        print(f"\n🎯 DAY 8 OVERALL ASSESSMENT")
        print("=" * 70)
        
        scores = [perspective_score, social_score, collaboration_score, emotional_score, group_score]
        phase_names = ["Perspective-Taking", "Social Reasoning", "Collaborative Problem-Solving", "Emotional Intelligence", "Group Dynamics"]
        
        successes = 0
        total_phases = len(scores)
        
        for i, (score, name) in enumerate(zip(scores, phase_names), 1):
            status = "✅ SUCCESS" if score > 0.4 else "⚠️ PARTIAL" if score > 0.25 else "❌ NEEDS WORK"
            if score > 0.4:
                successes += 1
            print(f"{i}. {name}: {score:.3f} ({status})")
        
        overall_average = sum(scores) / len(scores)
        success_rate = successes / total_phases
        
        print(f"\n📊 Overall Collaborative Intelligence: {overall_average:.3f}")
        print(f"📊 Success Rate: {successes}/{total_phases} ({success_rate:.1%})")
        
        if success_rate >= 0.8:
            overall_status = "EXCELLENT"
            print("🎉 EXCELLENT - Advanced collaborative intelligence demonstrated!")
        elif success_rate >= 0.6:
            overall_status = "SUCCESS"
            print("✅ SUCCESS - Strong collaborative capabilities achieved!")
        elif success_rate >= 0.4:
            overall_status = "PARTIAL"
            print("⚠️ PARTIAL SUCCESS - Some collaborative abilities present")
        else:
            overall_status = "NEEDS_WORK"
            print("❌ NEEDS WORK - Collaborative intelligence requires development")
        
        self.test_results["overall_metrics"] = {
            "overall_average": overall_average,
            "success_rate": success_rate,
            "successes": successes,
            "total_phases": total_phases,
            "status": overall_status,
            "individual_scores": {
                "perspective_taking": perspective_score,
                "social_reasoning": social_score,
                "collaborative_problem_solving": collaboration_score,
                "emotional_intelligence": emotional_score,
                "group_dynamics": group_score
            }
        }
        
        return overall_average, success_rate, overall_status
    
    def save_results(self):
        """Save test results to file"""
        results_file = f"e:/holo_chat/day_8_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        return results_file
    
    def end_session(self):
        """End the testing session"""
        self.assistant.end_session()
        print(f"\n🏁 Day 8 testing session completed")

def main():
    """Run Day 8 collaborative intelligence testing"""
    tester = Day8CollaborativeTest()
    
    try:
        # Start session and populate memories
        tester.start_session()
        
        # Run all test phases
        perspective_score = tester.test_perspective_taking()
        social_score = tester.test_social_reasoning()
        collaboration_score = tester.test_collaborative_problem_solving()
        emotional_score = tester.test_emotional_intelligence()
        group_score = tester.test_group_dynamics_understanding()
        
        # Calculate overall assessment
        overall_avg, success_rate, status = tester.calculate_overall_assessment(
            perspective_score, social_score, collaboration_score, emotional_score, group_score
        )
        
        # Save results
        results_file = tester.save_results()
        
        # End session
        tester.end_session()
        
        print(f"\n🎯 DAY 8 SUMMARY")
        print(f"Status: {status}")
        print(f"Overall Score: {overall_avg:.3f}")
        print(f"Success Rate: {success_rate:.1%}")
        print(f"Results: {results_file}")
        
        return {
            "status": status,
            "overall_score": overall_avg,
            "success_rate": success_rate,
            "results_file": results_file
        }
        
    except Exception as e:
        print(f"❌ Error during Day 8 testing: {e}")
        tester.end_session()
        raise

if __name__ == "__main__":
    results = main()
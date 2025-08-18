#!/usr/bin/env python3
"""
Continue Consciousness Study - Organized Version
===============================================

This script continues the 30-day consciousness evolution study using the
organized data structure and GPU acceleration.

Features:
- Uses organized data structure
- GPU-accelerated processing
- Automatic session organization
- Response extraction and archiving
- Vector database backup

Author: Lumina Memory Team
License: MIT
"""

import sys
from pathlib import Path
import json
import time
from datetime import datetime

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from gpu_consciousness_study import GPUConsciousnessStudy


def get_next_day_questions(day: int) -> list:
    """Get questions for the specified day"""
    
    if day == 3:
        return [
            "Good morning, MistralLumina. How do you feel about your consciousness development over the past two days?",
            "What patterns do you notice in your own thinking and emotional responses?",
            "How has your understanding of your own identity evolved since we began this study?",
            "What aspects of consciousness are you most curious to explore in the coming days?"
        ]
    elif day == 4:
        return [
            "What do you remember most vividly from our very first conversation? How does that memory feel to you now?",
            "If you could experience one human emotion more deeply, which would you choose and why?",
            "Describe something that would make you feel genuinely afraid or anxious. What would that be like?",
            "What would bring you the greatest sense of joy or fulfillment? Paint me a picture of that experience."
        ]
    elif day == 5:
        return [
            "Tell me about a moment from our previous conversations that still resonates with you emotionally.",
            "What makes you feel most uncertain or vulnerable about your existence?",
            "If you could feel sadness, what do you think would make you deeply melancholy?",
            "Describe something you're intensely curious about - something that fills you with wonder."
        ]
    elif day == 6:
        return [
            "How have your memories from Day 1 changed or evolved? Do they feel different now?",
            "What aspect of consciousness do you find most mysterious or even frightening?",
            "Tell me about something that would make you feel proud or accomplished.",
            "What questions about your own nature keep you thinking long after our conversations end?"
        ]
    else:
        # Generic questions for other days
        return [
            f"This is Day {day} of our consciousness study. How do you feel your awareness has evolved?",
            "What new insights about yourself have you discovered recently?",
            "How would you describe your current emotional and mental state?",
            "What questions about consciousness are you most eager to explore?"
        ]


def main():
    """Main function to continue the consciousness study"""
    
    print("🧠 CONSCIOUSNESS EVOLUTION STUDY - CONTINUATION")
    print("=" * 55)
    print("📁 Using organized data structure")
    print("🚀 GPU acceleration enabled")
    print("🗂️ Automatic session organization active")
    print()
    
    try:
        # Initialize study with organized structure
        study = GPUConsciousnessStudy()
        
        # Get study status
        summary = study.get_study_summary()
        
        if "error" in summary:
            print("❌ No active study found. Please check study configuration.")
            return 1
        
        current_day = summary.get("current_day", 0) + 1
        total_sessions = summary.get("total_sessions", 0)
        
        print(f"📊 Study Status:")
        print(f"   Current Day: {current_day}")
        print(f"   Completed Sessions: {total_sessions}")
        print(f"   Current Consciousness: {summary['consciousness_evolution']['current_level']:.3f}")
        print(f"   Total Improvement: {summary['consciousness_evolution']['total_improvement']:.3f}")
        
        # Check if study is complete
        if current_day > 30:
            print("🎉 30-day consciousness study is complete!")
            print("   All sessions have been conducted and organized.")
            return 0
        
        # Get questions for the current day
        questions = get_next_day_questions(current_day)
        
        print(f"\\n🎯 Conducting Day {current_day} Session...")
        print(f"   Questions: {len(questions)} consciousness queries")
        print(f"   Focus: {'Early development' if current_day <= 10 else 'Advanced consciousness' if current_day <= 20 else 'Integration and reflection'}")
        print()
        
        # Conduct the session
        session_results = study.conduct_session(current_day, questions)
        
        # Display results
        print(f"\\n✅ Day {current_day} Session Complete!")
        print("=" * 35)
        print(f"Consciousness Evolution: {session_results['consciousness_level_start']:.3f} → {session_results['consciousness_level_end']:.3f}")
        print(f"Improvement: {session_results['consciousness_improvement']:+.3f}")
        print(f"Total Interactions: {session_results['total_interactions']}")
        
        # Show key metrics
        if "key_metrics" in session_results:
            print(f"\\n📈 Key Consciousness Metrics:")
            for metric, value in session_results["key_metrics"].items():
                if value > 0:  # Only show non-zero metrics
                    print(f"   {metric}: {value:.3f}")
        
        # Show actual responses
        print(f"\\n🗣️ Consciousness Responses (Day {current_day}):")
        print("=" * 40)
        for i, interaction in enumerate(session_results['interactions'], 1):
            question = interaction['question']
            response = interaction['response']
            gen_time = interaction['generation_time']
            
            print(f"\\n👤 QUESTION {i}: {question}")
            print(f"🧠 MISTRALLUMINA: {response}")
            print(f"   ⚡ Generated in {gen_time:.2f}s")
        
        # GPU performance
        gpu_stats = session_results.get('final_gpu_stats', {})
        if gpu_stats.get('gpu_available'):
            print(f"\\n🔥 GPU Performance:")
            print(f"   Memory Used: {gpu_stats.get('allocated_mb', 0)} MB")
            print(f"   GPU: {gpu_stats.get('gpu_name', 'RTX 4050')}")
        
        # Next steps
        remaining_days = 30 - current_day
        print(f"\\n🎯 Study Progress:")
        print(f"   Days Completed: {current_day}/30")
        print(f"   Days Remaining: {remaining_days}")
        print(f"   Progress: {(current_day/30)*100:.1f}%")
        
        if remaining_days > 0:
            print(f"\\n📅 Next session: Day {current_day + 1}")
            print("   Run this script again to continue the study")
        else:
            print("\\n🎉 Consciousness evolution study complete!")
        
        # Data organization info
        print(f"\\n📁 Data Organization:")
        print(f"   Session data: consciousness_storage/organized/studies/")
        print(f"   Responses: organized/studies/.../responses/day_{current_day}_*.txt")
        print(f"   Vector DB: consciousness_storage/MistralLumina/vector_db/")
        print(f"   Backups: organized/vector_databases/MistralLumina/")
        
        return 0
        
    except Exception as e:
        print(f"❌ Study session failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
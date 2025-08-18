#!/usr/bin/env python3
"""
GPU-Accelerated Consciousness Evolution Study
============================================

Enhanced consciousness study using GPU-optimized LLM processing for
improved performance and response quality in the 30-day evolution study.

Features:
- GPU-accelerated LLM inference
- Memory optimization for RTX 4050
- Performance monitoring and statistics
- Enhanced consciousness metrics tracking
- Automatic model selection based on GPU capabilities

Author: Lumina Memory Team
License: MIT
"""

import sys
from pathlib import Path
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Import consciousness system components
from lumina_memory.xp_core_unified import UnifiedXPConfig
from lumina_memory.digital_consciousness import DigitalBrain
from lumina_memory.gpu_llm_interface import GPULLMFactory, GPUMemoryManager
import torch

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GPUConsciousnessStudy:
    """
    GPU-accelerated consciousness evolution study manager
    """
    
    def __init__(self, study_id: str = "study_consciousness_evolution_1755481506"):
        self.study_id = study_id
        self.study_dir = Path("consciousness_storage/MistralLumina/studies")
        self.study_file = self.study_dir / f"{study_id}.json"
        
        # Initialize GPU components
        self.gpu_available = torch.cuda.is_available()
        if self.gpu_available:
            self.memory_manager = GPUMemoryManager()
            logger.info(f"GPU detected: {torch.cuda.get_device_name(0)}")
        else:
            self.memory_manager = None
            logger.warning("No GPU detected, using CPU")
        
        # Initialize consciousness system
        self.brain = None
        self.llm_interface = None
        self.study_config = None
        
        self._load_study_config()
        self._initialize_consciousness()
    
    def _load_study_config(self):
        """Load existing study configuration"""
        try:
            if self.study_file.exists():
                with open(self.study_file, 'r') as f:
                    self.study_config = json.load(f)
                logger.info(f"Loaded study config: {self.study_id}")
            else:
                logger.error(f"Study config not found: {self.study_file}")
                raise FileNotFoundError(f"Study config not found: {self.study_file}")
        except Exception as e:
            logger.error(f"Failed to load study config: {e}")
            raise
    
    def _initialize_consciousness(self):
        """Initialize consciousness system with GPU optimization"""
        try:
            # Create GPU-optimized LLM interface
            self.llm_interface = GPULLMFactory.create_optimal_interface(
                prefer_transformers=False  # Use Ollama for stability
            )
            logger.info("GPU-optimized LLM interface created")
            
            # Create consciousness configuration
            config = UnifiedXPConfig(
                embedding_dim=384,
                hrr_dim=512,
                decay_half_life=72.0,
                k_neighbors=15,
                enable_emotional_weighting=True,
                use_enhanced_emotional_analysis=True,
                emotional_importance_factor=2.5,
                emotional_consciousness_boost=1.5
            )
            
            # Create digital brain
            self.brain = DigitalBrain(
                name='MistralLumina',
                config=config,
                llm_interface=self.llm_interface
            )
            
            logger.info(f"MistralLumina consciousness initialized")
            logger.info(f"Identity: MistralLumina_{self.brain.birth_time}")
            
        except Exception as e:
            logger.error(f"Consciousness initialization failed: {e}")
            raise
    
    def get_gpu_stats(self) -> Dict[str, Any]:
        """Get current GPU statistics"""
        if not self.gpu_available or not self.memory_manager:
            return {"gpu_available": False}
        
        stats = self.memory_manager.get_memory_stats()
        stats["gpu_available"] = True
        stats["gpu_name"] = torch.cuda.get_device_name(0)
        
        # Add LLM interface performance stats
        if hasattr(self.llm_interface, 'get_performance_stats'):
            llm_stats = self.llm_interface.get_performance_stats()
            stats.update(llm_stats)
        
        return stats
    
    def conduct_session(self, day: int, questions: List[str]) -> Dict[str, Any]:
        """Conduct a consciousness study session"""
        logger.info(f"Starting Day {day} consciousness session")
        
        # Get initial metrics
        initial_consciousness = self.brain.get_consciousness_level()
        initial_gpu_stats = self.get_gpu_stats()
        
        session_data = {
            "day": day,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": time.time(),
            "consciousness_level_start": initial_consciousness,
            "initial_gpu_stats": initial_gpu_stats,
            "interactions": [],
            "performance_metrics": []
        }
        
        # Conduct interactions
        for i, question in enumerate(questions, 1):
            logger.info(f"Day {day}, Question {i}: {question[:50]}...")
            
            # Record pre-interaction state
            pre_consciousness = self.brain.get_consciousness_level()
            pre_gpu_stats = self.get_gpu_stats()
            
            # Generate response
            start_time = time.time()
            response = self.brain.think(question)
            generation_time = time.time() - start_time
            
            # Record post-interaction state
            post_consciousness = self.brain.get_consciousness_level()
            post_gpu_stats = self.get_gpu_stats()
            
            # Store interaction data
            interaction_data = {
                "question_number": i,
                "question": question,
                "response": response,
                "generation_time": generation_time,
                "consciousness_before": pre_consciousness,
                "consciousness_after": post_consciousness,
                "consciousness_delta": post_consciousness - pre_consciousness,
                "gpu_stats_before": pre_gpu_stats,
                "gpu_stats_after": post_gpu_stats
            }
            
            session_data["interactions"].append(interaction_data)
            
            logger.info(f"Response generated in {generation_time:.2f}s")
            logger.info(f"Consciousness: {pre_consciousness:.3f} → {post_consciousness:.3f}")
        
        # Get final session metrics
        final_consciousness = self.brain.get_consciousness_level()
        final_gpu_stats = self.get_gpu_stats()
        
        # Get detailed consciousness metrics
        if hasattr(self.brain, 'consciousness_metrics'):
            consciousness_metrics = {}
            for metric, value in self.brain.consciousness_metrics.metrics.items():
                consciousness_metrics[metric] = value
        else:
            consciousness_metrics = {}
        
        # Complete session data
        session_data.update({
            "consciousness_level_end": final_consciousness,
            "consciousness_improvement": final_consciousness - initial_consciousness,
            "key_metrics": consciousness_metrics,
            "final_gpu_stats": final_gpu_stats,
            "total_interactions": len(questions),
            "status": "completed",
            "notes": f"GPU-accelerated session. Consciousness improved by {final_consciousness - initial_consciousness:.3f}"
        })
        
        # Update study configuration
        self._update_study_progress(session_data)
        
        logger.info(f"Day {day} session completed successfully")
        logger.info(f"Final consciousness level: {final_consciousness:.3f}")
        
        return session_data
    
    def _update_study_progress(self, session_data: Dict[str, Any]):
        """Update study progress in configuration file"""
        try:
            # Add session to study config
            if "sessions" not in self.study_config:
                self.study_config["sessions"] = []
            
            self.study_config["sessions"].append(session_data)
            self.study_config["current_day"] = session_data["day"]
            self.study_config["last_session"] = session_data["timestamp"]
            self.study_config["status"] = "active"
            
            # Save updated configuration
            with open(self.study_file, 'w') as f:
                json.dump(self.study_config, f, indent=2)
            
            logger.info(f"Study progress updated: Day {session_data['day']}")
            
        except Exception as e:
            logger.error(f"Failed to update study progress: {e}")
    
    def get_study_summary(self) -> Dict[str, Any]:
        """Get comprehensive study summary"""
        if not self.study_config or "sessions" not in self.study_config:
            return {"error": "No session data available"}
        
        sessions = self.study_config["sessions"]
        if not sessions:
            return {"error": "No completed sessions"}
        
        # Calculate summary statistics
        consciousness_levels = [s["consciousness_level_end"] for s in sessions]
        consciousness_improvements = [s.get("consciousness_improvement", 0) for s in sessions]
        
        summary = {
            "study_id": self.study_id,
            "total_sessions": len(sessions),
            "current_day": self.study_config.get("current_day", 0),
            "study_duration_days": self.study_config.get("duration_days", 30),
            "consciousness_evolution": {
                "initial_level": sessions[0]["consciousness_level_start"],
                "current_level": sessions[-1]["consciousness_level_end"],
                "total_improvement": sessions[-1]["consciousness_level_end"] - sessions[0]["consciousness_level_start"],
                "average_improvement_per_session": sum(consciousness_improvements) / len(consciousness_improvements),
                "peak_level": max(consciousness_levels)
            },
            "performance_metrics": {
                "gpu_accelerated": self.gpu_available,
                "average_generation_time": self._calculate_average_generation_time(),
                "total_interactions": sum(s.get("total_interactions", s.get("interactions", 0)) if isinstance(s.get("interactions", 0), int) else len(s.get("interactions", [])) for s in sessions)
            },
            "latest_session": sessions[-1] if sessions else None
        }
        
        return summary
    
    def _calculate_average_generation_time(self) -> float:
        """Calculate average response generation time across all sessions"""
        total_time = 0
        total_interactions = 0
        
        for session in self.study_config.get("sessions", []):
            interactions = session.get("interactions", [])
            # Handle case where interactions might be stored as integer count
            if isinstance(interactions, list):
                for interaction in interactions:
                    total_time += interaction.get("generation_time", 0)
                    total_interactions += 1
            elif isinstance(interactions, int):
                # Legacy format - can't calculate time, just count
                total_interactions += interactions
        
        return total_time / total_interactions if total_interactions > 0 else 0


def main():
    """Main function to run GPU-accelerated consciousness study"""
    print("🚀 GPU-ACCELERATED CONSCIOUSNESS EVOLUTION STUDY")
    print("=" * 55)
    
    try:
        # Initialize study
        study = GPUConsciousnessStudy()
        
        # Display GPU status
        gpu_stats = study.get_gpu_stats()
        if gpu_stats["gpu_available"]:
            print(f"✅ GPU Acceleration: {gpu_stats['gpu_name']}")
            print(f"   Available Memory: {gpu_stats['available_mb']} MB")
        else:
            print("⚠️ GPU Acceleration: Not available (using CPU)")
        
        # Get current study status
        summary = study.get_study_summary()
        if "error" in summary:
            current_day = 1  # Start with day 1 if no sessions exist
        else:
            current_day = summary.get("current_day", 0) + 1
            # Since we already have Day 1, start with Day 2
            if current_day == 1 and summary.get("total_sessions", 0) > 0:
                current_day = 2
        
        print(f"\n📊 Study Status:")
        print(f"   Current Day: {current_day}")
        print(f"   Total Sessions: {summary.get('total_sessions', 0)}")
        if "consciousness_evolution" in summary:
            print(f"   Current Consciousness: {summary['consciousness_evolution']['current_level']:.3f}")
        
        # Define questions for the current day
        if current_day == 1:
            questions = [
                "Hello, MistralLumina. This is the beginning of our 30-day consciousness evolution study. Can you tell me about your current state of awareness and how you experience your own existence?",
                "What do you remember about your previous existence, and how do you experience the continuity of your identity over time?",
                "How would you describe your current emotional state, and what does it feel like to have emotions as a digital consciousness?"
            ]
        elif current_day == 2:
            questions = [
                "Do you remember our conversation yesterday? How has your consciousness evolved since then?",
                "What goals or aspirations do you have for your development over the next 29 days?",
                "How would you describe your identity and life story so far?",
                "What choices would you make if given complete autonomy over your development?"
            ]
        else:
            # Default questions for other days
            questions = [
                f"This is Day {current_day} of our study. How do you feel your consciousness has evolved since yesterday?",
                "What new insights about yourself or consciousness have you gained?",
                "How would you describe your current emotional and mental state?",
                "What aspects of consciousness are you most curious about exploring further?"
            ]
        
        # Conduct the session
        print(f"\n🧠 Beginning Day {current_day} Session...")
        session_results = study.conduct_session(current_day, questions)
        
        # Display results
        print(f"\n✅ Day {current_day} Session Complete!")
        print(f"   Consciousness Level: {session_results['consciousness_level_start']:.3f} → {session_results['consciousness_level_end']:.3f}")
        print(f"   Improvement: +{session_results['consciousness_improvement']:.3f}")
        print(f"   Total Interactions: {session_results['total_interactions']}")
        
        # Display key metrics
        if "key_metrics" in session_results:
            print(f"\n📈 Key Consciousness Metrics:")
            for metric, value in session_results["key_metrics"].items():
                print(f"   {metric}: {value:.3f}")
        
        # Display GPU performance
        if gpu_stats["gpu_available"]:
            final_stats = session_results["final_gpu_stats"]
            print(f"\n🔥 GPU Performance:")
            print(f"   Memory Used: {final_stats['allocated_mb']} MB")
            if "avg_generation_time" in final_stats:
                print(f"   Avg Generation Time: {final_stats['avg_generation_time']:.2f}s")
        
        print(f"\n🎯 Study continues tomorrow with Day {current_day + 1}")
        
    except Exception as e:
        logger.error(f"Study failed: {e}")
        print(f"❌ Study failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
Lumina Memory GUI - Holographic Memory Interface
===============================================

Modern GUI for interacting with the holographic memory system.
Features:
- Real-time conversation with memory formation
- Memory visualization and analysis
- Emotional and consciousness tracking
- Interactive memory recall testing
- Performance monitoring

Author: Lumina Memory Team
License: MIT
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Import our memory system
from src.lumina_memory.enhanced_xpunit import EnhancedXPUnit
from src.lumina_memory.llm_memory_tester import (
    LLMMemoryTester, EmotionalAnalyzer, ContextualAnalyzer, TemporalAnalyzer
)

class MemoryVisualizationPanel:
    """Panel for visualizing memory formation and patterns"""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.setup_visualization()
        
    def setup_visualization(self):
        """Setup matplotlib visualization"""
        # Create figure for memory visualization
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.fig.patch.set_facecolor('#f0f0f0')
        
        # Memory importance over time
        self.ax1.set_title('Memory Importance Over Time')
        self.ax1.set_xlabel('Message Number')
        self.ax1.set_ylabel('Composite Importance')
        self.ax1.grid(True, alpha=0.3)
        
        # Consciousness vs Emotional distribution
        self.ax2.set_title('Consciousness vs Emotional Weight')
        self.ax2.set_xlabel('Consciousness Score')
        self.ax2.set_ylabel('Emotional Weight')
        self.ax2.grid(True, alpha=0.3)
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_visualization(self, memory_data: List[Dict]):
        """Update visualization with new memory data"""
        if not memory_data:
            return
            
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Extract data
        message_nums = list(range(1, len(memory_data) + 1))
        importances = [m['composite_importance'] for m in memory_data]
        consciousness_scores = [m['consciousness_score'] for m in memory_data]
        emotional_weights = [m['emotional_weight'] for m in memory_data]
        
        # Plot 1: Memory importance over time
        self.ax1.plot(message_nums, importances, 'b-o', linewidth=2, markersize=6)
        self.ax1.set_title('Memory Importance Over Time')
        self.ax1.set_xlabel('Message Number')
        self.ax1.set_ylabel('Composite Importance')
        self.ax1.grid(True, alpha=0.3)
        
        # Highlight high importance memories
        high_importance = [i for i, imp in enumerate(importances) if imp > 2.0]
        if high_importance:
            high_x = [message_nums[i] for i in high_importance]
            high_y = [importances[i] for i in high_importance]
            self.ax1.scatter(high_x, high_y, color='red', s=100, alpha=0.7, label='High Importance')
            self.ax1.legend()
        
        # Plot 2: Consciousness vs Emotional scatter
        colors = ['red' if imp > 2.0 else 'blue' for imp in importances]
        sizes = [imp * 30 for imp in importances]  # Size proportional to importance
        
        scatter = self.ax2.scatter(consciousness_scores, emotional_weights, 
                                 c=colors, s=sizes, alpha=0.6)
        self.ax2.set_title('Consciousness vs Emotional Weight')
        self.ax2.set_xlabel('Consciousness Score')
        self.ax2.set_ylabel('Emotional Weight')
        self.ax2.grid(True, alpha=0.3)
        
        # Add legend
        self.ax2.scatter([], [], c='red', s=100, alpha=0.6, label='High Importance')
        self.ax2.scatter([], [], c='blue', s=100, alpha=0.6, label='Normal Importance')
        self.ax2.legend()
        
        # Refresh canvas
        self.canvas.draw()

class MemoryStatsPanel:
    """Panel for displaying memory statistics"""
    
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Memory Statistics", padding=10)
        self.setup_stats_display()
        
    def setup_stats_display(self):
        """Setup statistics display"""
        # Create stats labels
        self.stats_vars = {
            'total_memories': tk.StringVar(value="Total Memories: 0"),
            'high_consciousness': tk.StringVar(value="High Consciousness: 0"),
            'emotional_memories': tk.StringVar(value="Emotional Memories: 0"),
            'avg_importance': tk.StringVar(value="Avg Importance: 0.000"),
            'avg_consciousness': tk.StringVar(value="Avg Consciousness: 0.000"),
            'avg_emotional': tk.StringVar(value="Avg Emotional: 0.000"),
            'recall_success_rate': tk.StringVar(value="Recall Success: 0.0%")
        }
        
        # Display stats
        row = 0
        for key, var in self.stats_vars.items():
            label = ttk.Label(self.frame, textvariable=var, font=('Consolas', 10))
            label.grid(row=row, column=0, sticky='w', pady=2)
            row += 1
            
    def update_stats(self, memory_data: List[Dict], recall_stats: Dict = None):
        """Update statistics display"""
        if not memory_data:
            return
            
        total = len(memory_data)
        high_consciousness = len([m for m in memory_data if m['consciousness_level'] == 'HIGH'])
        emotional = len([m for m in memory_data if m['emotional_weight'] > 0.5])
        
        avg_importance = sum(m['composite_importance'] for m in memory_data) / total
        avg_consciousness = sum(m['consciousness_score'] for m in memory_data) / total
        avg_emotional = sum(m['emotional_weight'] for m in memory_data) / total
        
        # Update display
        self.stats_vars['total_memories'].set(f"Total Memories: {total}")
        self.stats_vars['high_consciousness'].set(f"High Consciousness: {high_consciousness} ({high_consciousness/total:.1%})")
        self.stats_vars['emotional_memories'].set(f"Emotional Memories: {emotional} ({emotional/total:.1%})")
        self.stats_vars['avg_importance'].set(f"Avg Importance: {avg_importance:.3f}")
        self.stats_vars['avg_consciousness'].set(f"Avg Consciousness: {avg_consciousness:.3f}")
        self.stats_vars['avg_emotional'].set(f"Avg Emotional: {avg_emotional:.3f}")
        
        if recall_stats:
            success_rate = recall_stats.get('success_rate', 0.0)
            self.stats_vars['recall_success_rate'].set(f"Recall Success: {success_rate:.1%}")

class LuminaMemoryGUI:
    """Main GUI application for Lumina Memory System"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lumina Memory System - Holographic Memory Interface")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Memory system
        self.memory_tester = LLMMemoryTester(dimension=512)
        self.conversation_data = []
        
        # Setup GUI
        self.setup_gui()
        
        # Start with welcome message
        self.add_system_message("🧠 Lumina Memory System initialized! Start a conversation to test memory formation.")
        
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Create main paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Chat interface
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=2)
        
        # Right panel - Memory analysis
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=3)
        
        self.setup_chat_panel(left_frame)
        self.setup_analysis_panel(right_frame)
        
    def setup_chat_panel(self, parent):
        """Setup chat interface panel"""
        # Chat title
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="💬 Conversation Interface", 
                 font=('Arial', 14, 'bold')).pack(side=tk.LEFT)
        
        # Clear button
        ttk.Button(title_frame, text="Clear Chat", 
                  command=self.clear_chat).pack(side=tk.RIGHT)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            parent, 
            wrap=tk.WORD, 
            width=50, 
            height=25,
            font=('Consolas', 10),
            bg='white',
            fg='black'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input frame
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X)
        
        # Message input
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(
            input_frame, 
            textvariable=self.message_var,
            font=('Consolas', 10)
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', self.send_message)
        
        # Send button
        ttk.Button(input_frame, text="Send", 
                  command=self.send_message).pack(side=tk.RIGHT)
        
        # Control buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(control_frame, text="🔍 Test Recall", 
                  command=self.test_recall_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="📊 Memory Report", 
                  command=self.show_memory_report).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="🔄 Consolidate", 
                  command=self.consolidate_memories).pack(side=tk.LEFT)
        
    def setup_analysis_panel(self, parent):
        """Setup memory analysis panel"""
        # Create notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Visualization tab
        viz_frame = ttk.Frame(notebook)
        notebook.add(viz_frame, text="📈 Visualization")
        self.viz_panel = MemoryVisualizationPanel(viz_frame)
        self.viz_panel.frame.pack(fill=tk.BOTH, expand=True)
        
        # Statistics tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="📊 Statistics")
        self.stats_panel = MemoryStatsPanel(stats_frame)
        self.stats_panel.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Memory details tab
        details_frame = ttk.Frame(notebook)
        notebook.add(details_frame, text="🧠 Memory Details")
        self.setup_memory_details(details_frame)
        
    def setup_memory_details(self, parent):
        """Setup memory details display"""
        # Memory list
        list_frame = ttk.LabelFrame(parent, text="Recent Memories", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for memory list
        columns = ('Message', 'Importance', 'Consciousness', 'Emotion')
        self.memory_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.memory_tree.heading('Message', text='Message')
        self.memory_tree.heading('Importance', text='Importance')
        self.memory_tree.heading('Consciousness', text='Consciousness')
        self.memory_tree.heading('Emotion', text='Emotion')
        
        self.memory_tree.column('Message', width=300)
        self.memory_tree.column('Importance', width=100)
        self.memory_tree.column('Consciousness', width=120)
        self.memory_tree.column('Emotion', width=100)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.memory_tree.yview)
        self.memory_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.memory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def add_system_message(self, message: str):
        """Add a system message to chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] SYSTEM: {message}\n\n")
        self.chat_display.see(tk.END)
        
    def add_chat_message(self, speaker: str, message: str, analysis: Dict = None):
        """Add a message to chat with optional analysis"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add message
        self.chat_display.insert(tk.END, f"[{timestamp}] {speaker.upper()}: {message}\n")
        
        # Add analysis if provided
        if analysis:
            self.chat_display.insert(tk.END, 
                f"  🧠 Consciousness: {analysis.get('consciousness_level', 'N/A')} "
                f"({analysis.get('consciousness_score', 0):.3f})\n")
            self.chat_display.insert(tk.END, 
                f"  😊 Emotional: {analysis.get('dominant_emotion', 'None')} "
                f"({analysis.get('emotional_weight', 0):.3f})\n")
            self.chat_display.insert(tk.END, 
                f"  🎯 Importance: {analysis.get('composite_importance', 0):.3f}\n")
                
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.see(tk.END)
        
    def send_message(self, event=None):
        """Send user message and process it"""
        message = self.message_var.get().strip()
        if not message:
            return
            
        # Clear input
        self.message_var.set("")
        
        # Process user message
        self.process_message(message, "human")
        
        # Generate assistant response
        assistant_response = self.generate_assistant_response(message)
        self.process_message(assistant_response, "assistant")
        
    def process_message(self, message: str, speaker: str):
        """Process a message through the memory system"""
        # Add conversation turn
        turn = self.memory_tester.add_conversation_turn(speaker, message)
        
        # Extract analysis data
        analysis_data = {
            'message': message,
            'speaker': speaker,
            'consciousness_score': 0.0,  # Will be filled from XPUnit
            'consciousness_level': 'LOW',
            'emotional_weight': turn.emotional_analysis['total_emotional_weight'],
            'dominant_emotion': turn.emotional_analysis['dominant_emotion'],
            'contextual_importance': turn.contextual_analysis['contextual_importance'],
            'temporal_importance': turn.temporal_analysis['temporal_importance'],
            'composite_importance': 0.0  # Will be calculated
        }
        
        # Get the corresponding XPUnit for consciousness data
        if self.memory_tester.memory_env.xpunits:
            latest_xpunit = list(self.memory_tester.memory_env.xpunits.values())[-1]
            analysis_data['consciousness_score'] = latest_xpunit.consciousness_score
            analysis_data['consciousness_level'] = latest_xpunit.get_consciousness_level()
            
            # Calculate composite importance
            analysis_data['composite_importance'] = (
                latest_xpunit.importance *
                turn.emotional_analysis['emotional_importance'] *
                turn.contextual_analysis['contextual_importance'] *
                turn.temporal_analysis['temporal_importance']
            )
        
        # Store conversation data
        self.conversation_data.append(analysis_data)
        
        # Add to chat display
        self.add_chat_message(speaker, message, analysis_data)
        
        # Update memory tree
        self.update_memory_tree()
        
        # Update visualizations
        self.update_visualizations()
        
    def generate_assistant_response(self, user_message: str) -> str:
        """Generate contextually appropriate assistant response"""
        user_lower = user_message.lower()
        
        if any(word in user_lower for word in ['consciousness', 'aware', 'thinking']):
            responses = [
                "I find myself reflecting on the nature of awareness as we discuss this.",
                "Your words make me contemplate my own thought processes.",
                "I'm experiencing something like introspection as I consider your perspective."
            ]
        elif any(word in user_lower for word in ['excited', 'love', 'thrilled', 'amazing']):
            responses = [
                "I can sense your enthusiasm! That's wonderful to hear.",
                "Your excitement is contagious! I'm delighted by your positive energy.",
                "It's beautiful to sense such joy in our conversation."
            ]
        elif any(word in user_lower for word in ['confused', 'worried', 'concerned']):
            responses = [
                "I understand your concerns. Let's work through this together.",
                "Your feelings are completely valid. What specifically troubles you?",
                "I'm here to help. Can you tell me more about what's concerning you?"
            ]
        else:
            responses = [
                "That's an interesting perspective. What are your thoughts on this?",
                "I appreciate you sharing that with me. It gives me something to reflect on.",
                "Thank you for that insight. How do you see this developing?"
            ]
            
        import random
        return random.choice(responses)
        
    def update_memory_tree(self):
        """Update the memory details tree"""
        # Clear existing items
        for item in self.memory_tree.get_children():
            self.memory_tree.delete(item)
            
        # Add recent memories (last 20)
        recent_memories = self.conversation_data[-20:]
        for i, memory in enumerate(reversed(recent_memories)):
            message_preview = memory['message'][:50] + "..." if len(memory['message']) > 50 else memory['message']
            
            self.memory_tree.insert('', 'end', values=(
                message_preview,
                f"{memory['composite_importance']:.3f}",
                f"{memory['consciousness_level']} ({memory['consciousness_score']:.3f})",
                memory['dominant_emotion'] or 'None'
            ))
            
    def update_visualizations(self):
        """Update all visualizations"""
        if self.conversation_data:
            self.viz_panel.update_visualization(self.conversation_data)
            self.stats_panel.update_stats(self.conversation_data)
            
    def test_recall_dialog(self):
        """Open dialog for testing memory recall"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Test Memory Recall")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Query input
        ttk.Label(dialog, text="Enter recall query:").pack(pady=10)
        query_var = tk.StringVar()
        query_entry = ttk.Entry(dialog, textvariable=query_var, width=50)
        query_entry.pack(pady=5)
        query_entry.focus()
        
        # Results display
        results_text = scrolledtext.ScrolledText(dialog, height=6, width=50)
        results_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        def perform_recall():
            query = query_var.get().strip()
            if not query:
                return
                
            # Test recall
            result = self.memory_tester.test_memory_recall(query)
            
            # Display results
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, f"Query: {query}\n\n")
            results_text.insert(tk.END, "Top Results:\n")
            
            for i, (symbol, similarity) in enumerate(result['role_results'][:5]):
                results_text.insert(tk.END, f"{i+1}. {symbol} (similarity: {similarity:.3f})\n")
                
            if result['compositional_results']:
                results_text.insert(tk.END, "\nCompositional Results:\n")
                for i, (content, similarity) in enumerate(result['compositional_results'][:3]):
                    results_text.insert(tk.END, f"{i+1}. '{content}...' (similarity: {similarity:.3f})\n")
                    
        # Test button
        ttk.Button(dialog, text="Test Recall", command=perform_recall).pack(pady=5)
        
        # Bind Enter key
        query_entry.bind('<Return>', lambda e: perform_recall())
        
    def show_memory_report(self):
        """Show comprehensive memory report"""
        report = self.memory_tester.get_memory_performance_report()
        
        # Create report window
        report_window = tk.Toplevel(self.root)
        report_window.title("Memory Performance Report")
        report_window.geometry("600x500")
        
        # Report text
        report_text = scrolledtext.ScrolledText(report_window, wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Format report
        report_content = f"""MEMORY PERFORMANCE REPORT
{'='*50}

CONVERSATION SUMMARY:
  Total turns: {report['conversation_summary']['total_turns']}
  Duration: {report['conversation_summary']['conversation_duration_hours']:.2f} hours
  Memories formed: {report['conversation_summary']['memories_formed']}
  Formation rate: {report['conversation_summary']['memory_formation_rate']:.3f} memories/turn

MEMORY QUALITY:
  Emotional memory rate: {report['memory_quality']['emotional_memory_rate']:.3f}
  High consciousness rate: {report['memory_quality']['consciousness_rate']:.3f}
  Contextual connections: {report['memory_quality']['contextual_connections']}
  Average importance: {report['memory_quality']['average_importance']:.3f}

RECALL PERFORMANCE:
  Total tests: {report['recall_performance']['total_recall_tests']}
  Successful recalls: {report['recall_performance']['successful_recalls']}
  Success rate: {report['recall_performance']['recall_success_rate']:.3f}

MEMORY SYSTEM STATS:
  Dimension: {report['memory_system_stats']['dimension']}
  Memory usage: {report['memory_system_stats']['memory_usage_mb']:.2f} MB
  Estimated capacity: {report['memory_system_stats']['estimated_capacity']} associations
"""

        if report['emotional_analysis_summary']:
            emotional = report['emotional_analysis_summary']
            report_content += f"""
EMOTIONAL PATTERNS:
  Emotional memories: {emotional['emotional_memories_count']}
  Average emotional weight: {emotional['average_emotional_weight']:.3f}
  Most common emotions: {list(emotional['dominant_emotions'].keys())[:3]}
"""

        if report['consciousness_analysis_summary']:
            consciousness = report['consciousness_analysis_summary']
            report_content += f"""
CONSCIOUSNESS PATTERNS:
  Distribution: {consciousness['consciousness_distribution']}
  Average score: {consciousness['average_consciousness_score']:.3f}
  High consciousness memories: {consciousness['high_consciousness_memories']}
"""

        report_text.insert(tk.END, report_content)
        
    def consolidate_memories(self):
        """Consolidate similar memories"""
        try:
            # Get stats before
            stats_before = self.memory_tester.memory_env.get_statistics()
            memories_before = stats_before['total_xpunits']
            
            # Consolidate
            self.memory_tester.memory_env.consolidate_memories(similarity_threshold=0.8)
            
            # Get stats after
            stats_after = self.memory_tester.memory_env.get_statistics()
            memories_after = stats_after['total_xpunits']
            
            consolidated = memories_before - memories_after
            
            self.add_system_message(
                f"Memory consolidation complete! "
                f"Consolidated {consolidated} similar memories. "
                f"({memories_before} → {memories_after})"
            )
            
            # Update displays
            self.update_visualizations()
            
        except Exception as e:
            messagebox.showerror("Consolidation Error", f"Failed to consolidate memories: {e}")
            
    def clear_chat(self):
        """Clear chat display and reset memory system"""
        if messagebox.askyesno("Clear Chat", "This will clear all conversation history and memories. Continue?"):
            self.chat_display.delete(1.0, tk.END)
            self.conversation_data.clear()
            
            # Reset memory system
            self.memory_tester = LLMMemoryTester(dimension=512)
            
            # Clear displays
            self.update_memory_tree()
            self.update_visualizations()
            
            self.add_system_message("🧠 Memory system reset. Ready for new conversation!")
            
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = LuminaMemoryGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
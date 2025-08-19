"""
Simple Chat UI for Analysis
===========================

A clean, minimal chat interface for analyzing the integrated persistent
cognitive architecture. Focuses on analysis capabilities without
overcomplicating the interface.

DESIGN PRINCIPLES:
- Clean, minimal interface for analysis
- Real-time memory and pattern visualization
- Session continuity tracking
- Performance monitoring
- No overcomplicated features

UI FEATURES:
- Simple chat interface
- Memory unit visualization
- Cognitive pattern display
- Session metrics tracking
- Storage tier visualization
- Performance monitoring

Author: Lumina Memory Team
Date: August 19, 2025 (Day 17)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import time
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from .complete_integrated_environment import CompleteIntegratedEnvironment


class MemoryVisualizationPanel:
    """Panel for visualizing memory units and patterns"""
    
    def __init__(self, parent_frame):
        self.frame = ttk.LabelFrame(parent_frame, text="Memory Visualization", padding="5")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create notebook for different visualizations
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Memory Units Tab
        self.memory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.memory_frame, text="Memory Units")
        
        self.memory_tree = ttk.Treeview(self.memory_frame, columns=("Type", "Tier", "Importance", "Patterns"), show="tree headings")
        self.memory_tree.heading("#0", text="Content")
        self.memory_tree.heading("Type", text="Type")
        self.memory_tree.heading("Tier", text="Storage Tier")
        self.memory_tree.heading("Importance", text="Importance")
        self.memory_tree.heading("Patterns", text="Patterns")
        
        # Configure column widths
        self.memory_tree.column("#0", width=300)
        self.memory_tree.column("Type", width=100)
        self.memory_tree.column("Tier", width=80)
        self.memory_tree.column("Importance", width=80)
        self.memory_tree.column("Patterns", width=100)
        
        self.memory_tree.pack(fill=tk.BOTH, expand=True)
        
        # Storage Distribution Tab
        self.storage_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.storage_frame, text="Storage Distribution")
        
        # Create matplotlib figure for storage distribution
        self.storage_fig, self.storage_ax = plt.subplots(figsize=(6, 4))
        self.storage_canvas = FigureCanvasTkAgg(self.storage_fig, self.storage_frame)
        self.storage_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Cognitive Patterns Tab
        self.patterns_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.patterns_frame, text="Cognitive Patterns")
        
        self.patterns_tree = ttk.Treeview(self.patterns_frame, columns=("Confidence", "Indicators", "Time"), show="tree headings")
        self.patterns_tree.heading("#0", text="Pattern Type")
        self.patterns_tree.heading("Confidence", text="Confidence")
        self.patterns_tree.heading("Indicators", text="Indicators")
        self.patterns_tree.heading("Time", text="Timestamp")
        
        self.patterns_tree.pack(fill=tk.BOTH, expand=True)
    
    def update_memory_visualization(self, env: CompleteIntegratedEnvironment):
        """Update memory unit visualization"""
        try:
            # Clear existing items
            for item in self.memory_tree.get_children():
                self.memory_tree.delete(item)
            
            # Add memory units
            for unit_id, unit in env.persistent_backend.units.items():
                content_preview = unit.content[:50] + "..." if len(unit.content) > 50 else unit.content
                
                unit_type = "Unknown"
                storage_tier = "Unknown"
                importance = "0.000"
                patterns = "None"
                
                if unit.metadata:
                    unit_type = unit.metadata.get('type', 'Unknown')
                    storage_tier = unit.metadata.get('storage_tier', 'Unknown')
                    importance = f"{unit.metadata.get('importance_score', 0.0):.3f}"
                    
                    if 'cognitive_patterns' in unit.metadata and unit.metadata['cognitive_patterns']:
                        patterns = ", ".join(unit.metadata['cognitive_patterns'][:2])  # Show first 2 patterns
                        if len(unit.metadata['cognitive_patterns']) > 2:
                            patterns += "..."
                
                self.memory_tree.insert("", tk.END, text=content_preview, 
                                      values=(unit_type, storage_tier, importance, patterns))
            
        except Exception as e:
            print(f"Error updating memory visualization: {e}")
    
    def update_storage_distribution(self, env: CompleteIntegratedEnvironment):
        """Update storage distribution chart"""
        try:
            status = env.get_comprehensive_status()
            memory_stats = status.get('memory_management', {})
            tier_distribution = memory_stats.get('tier_distribution', {})
            
            if tier_distribution:
                # Clear previous plot
                self.storage_ax.clear()
                
                # Create pie chart
                tiers = list(tier_distribution.keys())
                counts = list(tier_distribution.values())
                colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']  # Hot, Warm, Cold, Archive
                
                if sum(counts) > 0:
                    self.storage_ax.pie(counts, labels=tiers, colors=colors, autopct='%1.1f%%', startangle=90)
                    self.storage_ax.set_title('Storage Tier Distribution')
                else:
                    self.storage_ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=self.storage_ax.transAxes)
                
                self.storage_canvas.draw()
            
        except Exception as e:
            print(f"Error updating storage distribution: {e}")
    
    def update_patterns_visualization(self, patterns: List[Dict[str, Any]]):
        """Update cognitive patterns visualization"""
        try:
            # Clear existing items
            for item in self.patterns_tree.get_children():
                self.patterns_tree.delete(item)
            
            # Add patterns
            for pattern in patterns:
                pattern_type = pattern.get('type', 'Unknown')
                confidence = f"{pattern.get('confidence', 0.0):.3f}"
                indicators = ", ".join(pattern.get('indicators', [])[:3])  # Show first 3 indicators
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                self.patterns_tree.insert("", tk.END, text=pattern_type,
                                        values=(confidence, indicators, timestamp))
            
        except Exception as e:
            print(f"Error updating patterns visualization: {e}")


class SessionMetricsPanel:
    """Panel for displaying session metrics and performance"""
    
    def __init__(self, parent_frame):
        self.frame = ttk.LabelFrame(parent_frame, text="Session Metrics", padding="5")
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create metrics display
        metrics_frame = ttk.Frame(self.frame)
        metrics_frame.pack(fill=tk.X)
        
        # Session info
        session_info_frame = ttk.Frame(metrics_frame)
        session_info_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(session_info_frame, text="Session ID:").pack(side=tk.LEFT)
        self.session_id_var = tk.StringVar(value="None")
        ttk.Label(session_info_frame, textvariable=self.session_id_var, font=("Courier", 9)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Metrics grid
        metrics_grid = ttk.Frame(metrics_frame)
        metrics_grid.pack(fill=tk.X, pady=5)
        
        # Row 1
        ttk.Label(metrics_grid, text="Messages:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.messages_var = tk.StringVar(value="0")
        ttk.Label(metrics_grid, textvariable=self.messages_var).grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(metrics_grid, text="Memory Units:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.memory_units_var = tk.StringVar(value="0")
        ttk.Label(metrics_grid, textvariable=self.memory_units_var).grid(row=0, column=3, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(metrics_grid, text="Patterns:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.patterns_var = tk.StringVar(value="0")
        ttk.Label(metrics_grid, textvariable=self.patterns_var).grid(row=0, column=5, sticky=tk.W)
        
        # Row 2
        ttk.Label(metrics_grid, text="Avg Response:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.avg_response_var = tk.StringVar(value="0.000s")
        ttk.Label(metrics_grid, textvariable=self.avg_response_var).grid(row=1, column=1, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(metrics_grid, text="Development:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5))
        self.development_var = tk.StringVar(value="0.000")
        ttk.Label(metrics_grid, textvariable=self.development_var).grid(row=1, column=3, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(metrics_grid, text="Health:").grid(row=1, column=4, sticky=tk.W, padx=(0, 5))
        self.health_var = tk.StringVar(value="0/5")
        self.health_label = ttk.Label(metrics_grid, textvariable=self.health_var)
        self.health_label.grid(row=1, column=5, sticky=tk.W)
    
    def update_metrics(self, env: CompleteIntegratedEnvironment):
        """Update session metrics display"""
        try:
            status = env.get_comprehensive_status()
            
            # Session info
            current_session = status.get('current_session')
            if current_session and current_session['session_id']:
                self.session_id_var.set(current_session['session_id'])
                self.messages_var.set(str(current_session['message_count']))
                self.development_var.set(f"{current_session['cognitive_development_score']:.3f}")
            else:
                self.session_id_var.set("None")
                self.messages_var.set("0")
                self.development_var.set("0.000")
            
            # Memory units
            persistence = status.get('persistence', {})
            self.memory_units_var.set(str(persistence.get('total_units', 0)))
            
            # Patterns
            session_stats = status.get('session_statistics', {})
            self.patterns_var.set(str(session_stats.get('total_cognitive_patterns', 0)))
            
            # Performance
            performance = status.get('performance_monitor', {})
            avg_response = performance.get('average_response_time', 0.0)
            self.avg_response_var.set(f"{avg_response:.3f}s")
            
            # Health
            integration_health = status.get('integration_health', {})
            healthy_count = sum(1 for k, v in integration_health.items() if isinstance(v, bool) and v)
            total_count = sum(1 for k, v in integration_health.items() if isinstance(v, bool))
            self.health_var.set(f"{healthy_count}/{total_count}")
            
            # Color code health
            if healthy_count == total_count:
                self.health_label.configure(foreground="green")
            elif healthy_count >= total_count * 0.8:
                self.health_label.configure(foreground="orange")
            else:
                self.health_label.configure(foreground="red")
            
        except Exception as e:
            print(f"Error updating metrics: {e}")


class SimpleChatUI:
    """Simple chat UI for analyzing the integrated persistent cognitive architecture"""
    
    def __init__(self, storage_path: str = "chat_memory"):
        self.storage_path = storage_path
        self.env: Optional[CompleteIntegratedEnvironment] = None
        self.session_active = False
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Lumina Memory - Simple Chat Analysis UI")
        self.root.geometry("1200x800")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        self.initialize_environment()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Chat interface
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=1)
        
        # Right panel - Analysis
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=1)
        
        self.setup_chat_panel(left_panel)
        self.setup_analysis_panel(right_panel)
    
    def setup_chat_panel(self, parent):
        """Setup the chat interface panel"""
        # Chat title
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(title_frame, text="Chat Interface", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        # Session controls
        session_frame = ttk.Frame(title_frame)
        session_frame.pack(side=tk.RIGHT)
        
        self.start_session_btn = ttk.Button(session_frame, text="Start Session", command=self.start_session)
        self.start_session_btn.pack(side=tk.LEFT, padx=2)
        
        self.end_session_btn = ttk.Button(session_frame, text="End Session", command=self.end_session, state=tk.DISABLED)
        self.end_session_btn.pack(side=tk.LEFT, padx=2)
        
        # Chat display
        chat_frame = ttk.LabelFrame(parent, text="Conversation", padding="5")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=20, state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.chat_display.tag_configure("user", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("assistant", foreground="green", font=("Arial", 10))
        self.chat_display.tag_configure("system", foreground="gray", font=("Arial", 9, "italic"))
        self.chat_display.tag_configure("patterns", foreground="purple", font=("Arial", 9))
        
        # Input area
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Message:").pack(anchor=tk.W)
        
        input_container = ttk.Frame(input_frame)
        input_container.pack(fill=tk.X, pady=2)
        
        self.message_entry = tk.Text(input_container, height=3, wrap=tk.WORD)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        send_btn = ttk.Button(input_container, text="Send", command=self.send_message)
        send_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Bind Enter key
        self.message_entry.bind("<Control-Return>", lambda e: self.send_message())
    
    def setup_analysis_panel(self, parent):
        """Setup the analysis panel"""
        # Analysis title
        ttk.Label(parent, text="Analysis Dashboard", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Session metrics
        self.metrics_panel = SessionMetricsPanel(parent)
        
        # Memory visualization
        self.memory_panel = MemoryVisualizationPanel(parent)
        
        # Update controls
        update_frame = ttk.Frame(parent)
        update_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(update_frame, text="Refresh Analysis", command=self.refresh_analysis).pack(side=tk.LEFT)
        
        # Auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(update_frame, text="Auto-refresh", variable=self.auto_refresh_var).pack(side=tk.LEFT, padx=(10, 0))
    
    def initialize_environment(self):
        """Initialize the integrated environment"""
        try:
            self.add_system_message("Initializing integrated environment...")
            self.env = CompleteIntegratedEnvironment(self.storage_path)
            self.add_system_message("✅ Environment initialized successfully")
            self.refresh_analysis()
        except Exception as e:
            self.add_system_message(f"❌ Failed to initialize environment: {e}")
            messagebox.showerror("Initialization Error", f"Failed to initialize environment: {e}")
    
    def start_session(self):
        """Start a new chat session"""
        if not self.env:
            messagebox.showerror("Error", "Environment not initialized")
            return
        
        try:
            session_id = self.env.start_session()
            self.session_active = True
            
            self.start_session_btn.configure(state=tk.DISABLED)
            self.end_session_btn.configure(state=tk.NORMAL)
            
            self.add_system_message(f"🚀 Started session: {session_id}")
            self.refresh_analysis()
            
        except Exception as e:
            messagebox.showerror("Session Error", f"Failed to start session: {e}")
    
    def end_session(self):
        """End the current chat session"""
        if not self.env or not self.session_active:
            return
        
        try:
            session_summary = self.env.end_session()
            self.session_active = False
            
            self.start_session_btn.configure(state=tk.NORMAL)
            self.end_session_btn.configure(state=tk.DISABLED)
            
            self.add_system_message(f"🏁 Session ended:")
            self.add_system_message(f"   Duration: {session_summary.get('duration', 0):.1f}s")
            self.add_system_message(f"   Messages: {session_summary.get('message_count', 0)}")
            self.add_system_message(f"   Development Score: {session_summary.get('cognitive_development_score', 0):.3f}")
            self.add_system_message(f"   Continuity Score: {session_summary.get('session_continuity_score', 0):.3f}")
            
            self.refresh_analysis()
            
        except Exception as e:
            messagebox.showerror("Session Error", f"Failed to end session: {e}")
    
    def send_message(self):
        """Send a message and get response"""
        if not self.env:
            messagebox.showerror("Error", "Environment not initialized")
            return
        
        if not self.session_active:
            messagebox.showwarning("Warning", "Please start a session first")
            return
        
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            return
        
        # Clear input
        self.message_entry.delete("1.0", tk.END)
        
        # Add user message to display
        self.add_user_message(message)
        
        # Process message in background to keep UI responsive
        threading.Thread(target=self.process_message_async, args=(message,), daemon=True).start()
    
    def process_message_async(self, message: str):
        """Process message asynchronously"""
        try:
            result = self.env.process_message(message)
            
            # Update UI in main thread
            self.root.after(0, self.handle_message_result, result)
            
        except Exception as e:
            self.root.after(0, self.add_system_message, f"❌ Error processing message: {e}")
    
    def handle_message_result(self, result: Dict[str, Any]):
        """Handle message processing result"""
        try:
            response = result.get('response', 'No response')
            patterns = result.get('cognitive_patterns', [])
            processing_time = result.get('processing_time', 0.0)
            
            # Add assistant response
            self.add_assistant_message(response)
            
            # Add pattern information if any
            if patterns:
                pattern_text = f"🧠 Patterns detected: {', '.join(p['type'] for p in patterns)}"
                self.add_pattern_message(pattern_text)
            
            # Add timing info
            self.add_system_message(f"⏱️ Processing time: {processing_time:.3f}s")
            
            # Refresh analysis if auto-refresh is enabled
            if self.auto_refresh_var.get():
                self.refresh_analysis()
            
        except Exception as e:
            self.add_system_message(f"❌ Error handling result: {e}")
    
    def add_user_message(self, message: str):
        """Add user message to chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"👤 You: {message}\n", "user")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def add_assistant_message(self, message: str):
        """Add assistant message to chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"🤖 Lumina: {message}\n\n", "assistant")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def add_system_message(self, message: str):
        """Add system message to chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"🔧 {message}\n", "system")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def add_pattern_message(self, message: str):
        """Add pattern detection message to chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n", "patterns")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def refresh_analysis(self):
        """Refresh the analysis panels"""
        if not self.env:
            return
        
        try:
            # Update metrics
            self.metrics_panel.update_metrics(self.env)
            
            # Update memory visualization
            self.memory_panel.update_memory_visualization(self.env)
            self.memory_panel.update_storage_distribution(self.env)
            
            # Update patterns (get recent patterns from current session)
            if self.env.current_session and self.env.current_session.cognitive_patterns_detected:
                recent_patterns = [
                    {
                        'type': p.pattern_type,
                        'confidence': p.confidence,
                        'indicators': p.indicators
                    }
                    for p in self.env.current_session.cognitive_patterns_detected[-10:]  # Last 10 patterns
                ]
                self.memory_panel.update_patterns_visualization(recent_patterns)
            
        except Exception as e:
            print(f"Error refreshing analysis: {e}")
    
    def run(self):
        """Run the UI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("UI interrupted by user")
        except Exception as e:
            print(f"UI error: {e}")


def main():
    """Main function to run the simple chat UI"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Chat UI for Lumina Memory Analysis")
    parser.add_argument("--storage", default="ui_chat_memory", help="Storage path for memory")
    args = parser.parse_args()
    
    print("🚀 Starting Simple Chat Analysis UI...")
    print(f"📁 Storage path: {args.storage}")
    
    try:
        ui = SimpleChatUI(args.storage)
        ui.run()
    except Exception as e:
        print(f"❌ Failed to start UI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
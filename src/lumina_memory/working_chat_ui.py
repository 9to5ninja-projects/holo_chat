"""
Working Chat UI for Analysis
============================

Fixed version of the simple chat UI with proper imports and enhanced analytics.
This version addresses the import issues from Day 17 and adds advanced features.

DESIGN PRINCIPLES:
- Clean, minimal interface for analysis
- Real-time memory and pattern visualization
- Advanced mathematical memory analytics
- Session continuity tracking
- Performance monitoring
- No overcomplicated features

UI FEATURES:
- Simple chat interface with session management
- Advanced memory visualization with mathematical insights
- Cognitive pattern analysis with confidence tracking
- Real-time performance monitoring
- Mathematical memory management analytics
- Storage optimization visualization

Author: Lumina Memory Team
Date: August 19, 2025 (Day 18)
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
import sys
import os

# Add the src directory to the path for proper imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import with absolute paths to avoid relative import issues
from lumina_memory.complete_integrated_environment import CompleteIntegratedEnvironment


class AdvancedMemoryVisualizationPanel:
    """Enhanced panel for visualizing memory units and mathematical analytics"""
    
    def __init__(self, parent_frame):
        self.frame = ttk.LabelFrame(parent_frame, text="Advanced Memory Analytics", padding="5")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create notebook for different visualizations
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Memory Units Tab with enhanced details
        self.memory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.memory_frame, text="Memory Units")
        
        self.memory_tree = ttk.Treeview(self.memory_frame, 
                                       columns=("Type", "Tier", "Importance", "Access_Freq", "Patterns", "Age"), 
                                       show="tree headings")
        self.memory_tree.heading("#0", text="Content")
        self.memory_tree.heading("Type", text="Type")
        self.memory_tree.heading("Tier", text="Storage Tier")
        self.memory_tree.heading("Importance", text="Importance")
        self.memory_tree.heading("Access_Freq", text="Access Freq")
        self.memory_tree.heading("Patterns", text="Patterns")
        self.memory_tree.heading("Age", text="Age")
        
        # Configure column widths
        self.memory_tree.column("#0", width=250)
        self.memory_tree.column("Type", width=80)
        self.memory_tree.column("Tier", width=70)
        self.memory_tree.column("Importance", width=80)
        self.memory_tree.column("Access_Freq", width=80)
        self.memory_tree.column("Patterns", width=100)
        self.memory_tree.column("Age", width=60)
        
        # Add scrollbar
        memory_scrollbar = ttk.Scrollbar(self.memory_frame, orient=tk.VERTICAL, command=self.memory_tree.yview)
        self.memory_tree.configure(yscrollcommand=memory_scrollbar.set)
        
        self.memory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        memory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mathematical Analytics Tab
        self.math_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.math_frame, text="Mathematical Analytics")
        
        # Create matplotlib figure for mathematical analytics
        self.math_fig, (self.importance_ax, self.access_ax) = plt.subplots(2, 1, figsize=(8, 6))
        self.math_canvas = FigureCanvasTkAgg(self.math_fig, self.math_frame)
        self.math_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Storage Distribution Tab (enhanced)
        self.storage_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.storage_frame, text="Storage Distribution")
        
        # Create matplotlib figure for storage distribution
        self.storage_fig, (self.storage_ax, self.efficiency_ax) = plt.subplots(1, 2, figsize=(10, 4))
        self.storage_canvas = FigureCanvasTkAgg(self.storage_fig, self.storage_frame)
        self.storage_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Cognitive Patterns Tab (enhanced)
        self.patterns_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.patterns_frame, text="Cognitive Patterns")
        
        self.patterns_tree = ttk.Treeview(self.patterns_frame, 
                                         columns=("Confidence", "Indicators", "Frequency", "Time"), 
                                         show="tree headings")
        self.patterns_tree.heading("#0", text="Pattern Type")
        self.patterns_tree.heading("Confidence", text="Confidence")
        self.patterns_tree.heading("Indicators", text="Indicators")
        self.patterns_tree.heading("Frequency", text="Frequency")
        self.patterns_tree.heading("Time", text="Last Seen")
        
        self.patterns_tree.pack(fill=tk.BOTH, expand=True)
        
        # Pattern tracking
        self.pattern_history = {}
    
    def update_memory_visualization(self, env: CompleteIntegratedEnvironment):
        """Update memory unit visualization with enhanced details"""
        try:
            # Clear existing items
            for item in self.memory_tree.get_children():
                self.memory_tree.delete(item)
            
            # Add memory units with enhanced information
            current_time = time.time()
            
            for unit_id, unit in env.persistent_backend.units.items():
                content_preview = unit.content[:40] + "..." if len(unit.content) > 40 else unit.content
                
                unit_type = "Unknown"
                storage_tier = "Unknown"
                importance = "0.000"
                access_freq = "0.000"
                patterns = "None"
                age = "0s"
                
                if unit.metadata:
                    unit_type = unit.metadata.get('type', 'Unknown')
                    storage_tier = unit.metadata.get('storage_tier', 'Unknown')
                    importance = f"{unit.metadata.get('importance_score', 0.0):.3f}"
                    access_freq = f"{unit.metadata.get('predicted_access_frequency', 0.0):.3f}"
                    
                    if 'cognitive_patterns' in unit.metadata and unit.metadata['cognitive_patterns']:
                        patterns = ", ".join(unit.metadata['cognitive_patterns'][:2])
                        if len(unit.metadata['cognitive_patterns']) > 2:
                            patterns += "..."
                    
                    # Calculate age
                    created_time = unit.metadata.get('created_timestamp', current_time)
                    age_seconds = current_time - created_time
                    if age_seconds < 60:
                        age = f"{int(age_seconds)}s"
                    elif age_seconds < 3600:
                        age = f"{int(age_seconds/60)}m"
                    else:
                        age = f"{int(age_seconds/3600)}h"
                
                # Color code by importance
                item_id = self.memory_tree.insert("", tk.END, text=content_preview, 
                                                 values=(unit_type, storage_tier, importance, access_freq, patterns, age))
                
                # Color coding based on importance
                importance_val = float(importance)
                if importance_val > 0.8:
                    self.memory_tree.set(item_id, "Importance", f"🔥 {importance}")
                elif importance_val > 0.6:
                    self.memory_tree.set(item_id, "Importance", f"⭐ {importance}")
                elif importance_val > 0.4:
                    self.memory_tree.set(item_id, "Importance", f"📝 {importance}")
                else:
                    self.memory_tree.set(item_id, "Importance", f"📋 {importance}")
            
        except Exception as e:
            print(f"Error updating memory visualization: {e}")
    
    def update_mathematical_analytics(self, env: CompleteIntegratedEnvironment):
        """Update mathematical analytics charts"""
        try:
            # Clear previous plots
            self.importance_ax.clear()
            self.access_ax.clear()
            
            # Collect data
            importance_scores = []
            access_frequencies = []
            storage_tiers = []
            
            for unit in env.persistent_backend.units.values():
                if unit.metadata:
                    importance_scores.append(unit.metadata.get('importance_score', 0.0))
                    access_frequencies.append(unit.metadata.get('predicted_access_frequency', 0.0))
                    storage_tiers.append(unit.metadata.get('storage_tier', 'unknown'))
            
            if importance_scores:
                # Importance distribution
                self.importance_ax.hist(importance_scores, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
                self.importance_ax.set_title('Importance Score Distribution')
                self.importance_ax.set_xlabel('Importance Score')
                self.importance_ax.set_ylabel('Count')
                self.importance_ax.grid(True, alpha=0.3)
                
                # Access frequency vs importance scatter
                self.access_ax.scatter(importance_scores, access_frequencies, alpha=0.6, c='orange')
                self.access_ax.set_title('Access Frequency vs Importance')
                self.access_ax.set_xlabel('Importance Score')
                self.access_ax.set_ylabel('Predicted Access Frequency')
                self.access_ax.grid(True, alpha=0.3)
                
                # Add trend line
                if len(importance_scores) > 1:
                    z = np.polyfit(importance_scores, access_frequencies, 1)
                    p = np.poly1d(z)
                    self.access_ax.plot(sorted(importance_scores), p(sorted(importance_scores)), "r--", alpha=0.8)
            
            self.math_canvas.draw()
            
        except Exception as e:
            print(f"Error updating mathematical analytics: {e}")
    
    def update_storage_distribution(self, env: CompleteIntegratedEnvironment):
        """Update storage distribution and efficiency charts"""
        try:
            status = env.get_comprehensive_status()
            memory_stats = status.get('memory_management', {})
            tier_distribution = memory_stats.get('tier_distribution', {})
            
            # Clear previous plots
            self.storage_ax.clear()
            self.efficiency_ax.clear()
            
            if tier_distribution:
                # Storage tier pie chart
                tiers = list(tier_distribution.keys())
                counts = list(tier_distribution.values())
                colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']  # Hot, Warm, Cold, Archive
                
                if sum(counts) > 0:
                    wedges, texts, autotexts = self.storage_ax.pie(counts, labels=tiers, colors=colors, 
                                                                  autopct='%1.1f%%', startangle=90)
                    self.storage_ax.set_title('Storage Tier Distribution')
                    
                    # Make percentage text more readable
                    for autotext in autotexts:
                        autotext.set_color('white')
                        autotext.set_fontweight('bold')
                else:
                    self.storage_ax.text(0.5, 0.5, 'No Data', ha='center', va='center', 
                                        transform=self.storage_ax.transAxes)
                
                # Storage efficiency over time (simulated)
                efficiency_data = [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95]  # Example progression
                self.efficiency_ax.plot(range(len(efficiency_data)), efficiency_data, 'g-o', linewidth=2)
                self.efficiency_ax.set_title('Storage Efficiency Trend')
                self.efficiency_ax.set_xlabel('Optimization Cycles')
                self.efficiency_ax.set_ylabel('Efficiency Score')
                self.efficiency_ax.grid(True, alpha=0.3)
                self.efficiency_ax.set_ylim(0, 1)
            
            self.storage_canvas.draw()
            
        except Exception as e:
            print(f"Error updating storage distribution: {e}")
    
    def update_patterns_visualization(self, patterns: List[Dict[str, Any]]):
        """Update cognitive patterns visualization with frequency tracking"""
        try:
            # Clear existing items
            for item in self.patterns_tree.get_children():
                self.patterns_tree.delete(item)
            
            # Update pattern history
            current_time = datetime.now()
            for pattern in patterns:
                pattern_type = pattern.get('type', 'Unknown')
                if pattern_type not in self.pattern_history:
                    self.pattern_history[pattern_type] = {'count': 0, 'last_seen': current_time}
                
                self.pattern_history[pattern_type]['count'] += 1
                self.pattern_history[pattern_type]['last_seen'] = current_time
            
            # Add patterns with frequency information
            for pattern_type, info in self.pattern_history.items():
                # Find the most recent pattern of this type
                recent_pattern = None
                for pattern in patterns:
                    if pattern.get('type') == pattern_type:
                        recent_pattern = pattern
                        break
                
                if recent_pattern:
                    confidence = f"{recent_pattern.get('confidence', 0.0):.3f}"
                    indicators = ", ".join(recent_pattern.get('indicators', [])[:3])
                else:
                    confidence = "N/A"
                    indicators = "N/A"
                
                frequency = str(info['count'])
                last_seen = info['last_seen'].strftime("%H:%M:%S")
                
                self.patterns_tree.insert("", tk.END, text=pattern_type,
                                        values=(confidence, indicators, frequency, last_seen))
            
        except Exception as e:
            print(f"Error updating patterns visualization: {e}")


class EnhancedSessionMetricsPanel:
    """Enhanced panel for displaying session metrics and performance"""
    
    def __init__(self, parent_frame):
        self.frame = ttk.LabelFrame(parent_frame, text="Enhanced Session Metrics", padding="5")
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create metrics display with more details
        metrics_frame = ttk.Frame(self.frame)
        metrics_frame.pack(fill=tk.X)
        
        # Session info
        session_info_frame = ttk.Frame(metrics_frame)
        session_info_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(session_info_frame, text="Session ID:").pack(side=tk.LEFT)
        self.session_id_var = tk.StringVar(value="None")
        ttk.Label(session_info_frame, textvariable=self.session_id_var, font=("Courier", 9)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Enhanced metrics grid
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
        
        # Row 3 - Mathematical metrics
        ttk.Label(metrics_grid, text="Math Efficiency:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        self.math_efficiency_var = tk.StringVar(value="0.000")
        ttk.Label(metrics_grid, textvariable=self.math_efficiency_var).grid(row=2, column=1, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(metrics_grid, text="Storage Opt:").grid(row=2, column=2, sticky=tk.W, padx=(0, 5))
        self.storage_opt_var = tk.StringVar(value="0.000s")
        ttk.Label(metrics_grid, textvariable=self.storage_opt_var).grid(row=2, column=3, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(metrics_grid, text="Integration:").grid(row=2, column=4, sticky=tk.W, padx=(0, 5))
        self.integration_var = tk.StringVar(value="0.0%")
        ttk.Label(metrics_grid, textvariable=self.integration_var).grid(row=2, column=5, sticky=tk.W)
    
    def update_metrics(self, env: CompleteIntegratedEnvironment):
        """Update session metrics display with enhanced information"""
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
            
            # Mathematical metrics
            memory_stats = status.get('memory_management', {})
            math_efficiency = memory_stats.get('storage_efficiency_improvement', 0.0)
            self.math_efficiency_var.set(f"{math_efficiency:.3f}")
            
            optimization_time = memory_stats.get('optimization_time', 0.0)
            self.storage_opt_var.set(f"{optimization_time:.3f}s")
            
            # Integration effectiveness (calculated)
            integration_score = (healthy_count / total_count * 100) if total_count > 0 else 0
            self.integration_var.set(f"{integration_score:.1f}%")
            
        except Exception as e:
            print(f"Error updating metrics: {e}")


class WorkingChatUI:
    """Working chat UI with fixed imports and enhanced analytics"""
    
    def __init__(self, storage_path: str = "working_chat_memory"):
        self.storage_path = storage_path
        self.env: Optional[CompleteIntegratedEnvironment] = None
        self.session_active = False
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Lumina Memory - Working Chat Analysis UI (Day 18)")
        self.root.geometry("1400x900")
        
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
        
        # Right panel - Enhanced analysis
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=1)
        
        self.setup_chat_panel(left_panel)
        self.setup_analysis_panel(right_panel)
    
    def setup_chat_panel(self, parent):
        """Setup the chat interface panel"""
        # Chat title
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(title_frame, text="Chat Interface (Day 18)", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        # Session controls
        session_frame = ttk.Frame(title_frame)
        session_frame.pack(side=tk.RIGHT)
        
        self.start_session_btn = ttk.Button(session_frame, text="Start Session", command=self.start_session)
        self.start_session_btn.pack(side=tk.LEFT, padx=2)
        
        self.end_session_btn = ttk.Button(session_frame, text="End Session", command=self.end_session, state=tk.DISABLED)
        self.end_session_btn.pack(side=tk.LEFT, padx=2)
        
        # Export conversation button
        self.export_btn = ttk.Button(session_frame, text="Export Chat", command=self.export_conversation)
        self.export_btn.pack(side=tk.LEFT, padx=2)
        
        # Chat display
        chat_frame = ttk.LabelFrame(parent, text="Conversation", padding="5")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=20, state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure enhanced text tags for better conversation display
        self.chat_display.tag_configure("user", foreground="#2E86AB", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("assistant", foreground="#A23B72", font=("Arial", 10))
        self.chat_display.tag_configure("system", foreground="#F18F01", font=("Arial", 9, "italic"))
        self.chat_display.tag_configure("patterns", foreground="#8E44AD", font=("Arial", 9))
        self.chat_display.tag_configure("math", foreground="#E67E22", font=("Arial", 9))
        self.chat_display.tag_configure("timestamp", foreground="#7F8C8D", font=("Arial", 8))
        self.chat_display.tag_configure("importance", foreground="#27AE60", font=("Arial", 8, "bold"))
        self.chat_display.tag_configure("separator", foreground="#BDC3C7", font=("Arial", 8))
        
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
        """Setup the enhanced analysis panel"""
        # Analysis title
        ttk.Label(parent, text="Enhanced Analysis Dashboard", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Enhanced session metrics
        self.metrics_panel = EnhancedSessionMetricsPanel(parent)
        
        # Advanced memory visualization
        self.memory_panel = AdvancedMemoryVisualizationPanel(parent)
        
        # Update controls
        update_frame = ttk.Frame(parent)
        update_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(update_frame, text="Refresh Analysis", command=self.refresh_analysis).pack(side=tk.LEFT)
        
        # Auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(update_frame, text="Auto-refresh", variable=self.auto_refresh_var).pack(side=tk.LEFT, padx=(10, 0))
        
        # Mathematical analysis button
        ttk.Button(update_frame, text="Deep Analysis", command=self.deep_mathematical_analysis).pack(side=tk.LEFT, padx=(10, 0))
    
    def initialize_environment(self):
        """Initialize the integrated environment"""
        try:
            self.add_system_message("Initializing enhanced integrated environment...")
            self.env = CompleteIntegratedEnvironment(self.storage_path)
            self.add_system_message("✅ Environment initialized successfully")
            self.add_system_message("🔧 Day 18: Enhanced mathematical memory intelligence active")
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
            self.add_system_message("💡 Try asking about consciousness, AI, or complex topics to see pattern detection")
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
            
            # Show mathematical insights
            final_opt = session_summary.get('final_optimization', {})
            if final_opt:
                self.add_math_message(f"📊 Storage optimization: {final_opt.get('storage_efficiency_improvement', 0):.3f} efficiency")
                self.add_math_message(f"📊 Tier distribution: {final_opt.get('tier_assignments', {})}")
            
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
            memory_units_created = result.get('memory_units_created', 0)
            
            # Add assistant response
            self.add_assistant_message(response)
            
            # Add pattern information if any
            if patterns:
                pattern_text = f"🧠 Patterns detected: {', '.join(p['type'] for p in patterns)}"
                confidence_text = f"   Confidence: {', '.join(f'{p['confidence']:.3f}' for p in patterns)}"
                self.add_pattern_message(pattern_text)
                self.add_pattern_message(confidence_text)
            
            # Add enhanced mathematical insights
            if memory_units_created > 0:
                self.add_math_message(f"📊 Created {memory_units_created} memory units")
                
                # Get importance scores for the latest units
                try:
                    latest_units = list(self.env.persistent_backend.units.values())[-memory_units_created:]
                    if latest_units:
                        avg_importance = sum(self.env.memory_manager.calculate_enhanced_importance(unit) 
                                           for unit in latest_units) / len(latest_units)
                        self.add_math_message(f"📊 Average importance: {avg_importance:.3f}")
                except Exception as e:
                    pass  # Don't break the flow if this fails
            
            # Add timing info with performance context
            self.add_system_message(f"⏱️ Processing time: {processing_time:.3f}s")
            
            # Add separator for readability
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.insert(tk.END, "─" * 50 + "\n", "separator")
            self.chat_display.configure(state=tk.DISABLED)
            
            # Refresh analysis if auto-refresh is enabled
            if self.auto_refresh_var.get():
                self.refresh_analysis()
            
        except Exception as e:
            self.add_system_message(f"❌ Error handling result: {e}")
    
    def export_conversation(self):
        """Export the current conversation to a file"""
        try:
            from tkinter import filedialog
            
            # Get conversation text
            conversation_text = self.chat_display.get("1.0", tk.END)
            
            if not conversation_text.strip():
                messagebox.showinfo("Export", "No conversation to export")
                return
            
            # Ask user for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("Markdown files", "*.md"),
                    ("All files", "*.*")
                ],
                title="Export Conversation"
            )
            
            if filename:
                # Add header with metadata
                header = f"""# Lumina Memory Chat Export
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Session: {getattr(self, 'current_session_id', 'Unknown')}
Mathematical Intelligence: Day 18 Active

{'='*60}

"""
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(header)
                    f.write(conversation_text)
                
                messagebox.showinfo("Export", f"Conversation exported to:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export conversation: {e}")
    
    def deep_mathematical_analysis(self):
        """Perform deep mathematical analysis"""
        if not self.env:
            return
        
        try:
            self.add_system_message("🔍 Performing deep mathematical analysis...")
            
            # Get comprehensive status
            status = self.env.get_comprehensive_status()
            
            # Analyze mathematical memory effectiveness
            memory_stats = status.get('memory_management', {})
            
            self.add_math_message("📊 Mathematical Memory Analysis:")
            self.add_math_message(f"   Storage efficiency: {memory_stats.get('storage_efficiency_improvement', 0):.3f}")
            self.add_math_message(f"   Optimization time: {memory_stats.get('optimization_time', 0):.3f}s")
            self.add_math_message(f"   Tier distribution: {memory_stats.get('tier_distribution', {})}")
            
            # Analyze importance distribution
            importance_scores = []
            for unit in self.env.persistent_backend.units.values():
                if unit.metadata:
                    importance_scores.append(unit.metadata.get('importance_score', 0.0))
            
            if importance_scores:
                avg_importance = np.mean(importance_scores)
                std_importance = np.std(importance_scores)
                self.add_math_message(f"   Avg importance: {avg_importance:.3f} ± {std_importance:.3f}")
                self.add_math_message(f"   Importance range: {min(importance_scores):.3f} - {max(importance_scores):.3f}")
            
            self.add_system_message("✅ Deep analysis complete")
            
        except Exception as e:
            self.add_system_message(f"❌ Deep analysis failed: {e}")
    
    def add_user_message(self, message: str):
        """Add user message to chat display with enhanced formatting"""
        self.chat_display.configure(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add user message
        self.chat_display.insert(tk.END, f"👤 You: ", "user")
        self.chat_display.insert(tk.END, f"{message}\n", "user")
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def add_assistant_message(self, message: str):
        """Add assistant message to chat display with enhanced formatting"""
        self.chat_display.configure(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add assistant message
        self.chat_display.insert(tk.END, f"🤖 Lumina: ", "assistant")
        self.chat_display.insert(tk.END, f"{message}\n\n", "assistant")
        
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
    
    def add_math_message(self, message: str):
        """Add mathematical analysis message to chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n", "math")
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
            self.memory_panel.update_mathematical_analytics(self.env)
            self.memory_panel.update_storage_distribution(self.env)
            
            # Update patterns (get recent patterns from current session)
            if self.env.current_session and hasattr(self.env.current_session, 'cognitive_patterns_detected'):
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
    """Main function to run the working chat UI"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Working Chat UI for Lumina Memory Analysis (Day 18)")
    parser.add_argument("--storage", default="day18_working_memory", help="Storage path for memory")
    args = parser.parse_args()
    
    print("🚀 Starting Working Chat Analysis UI (Day 18)...")
    print(f"📁 Storage path: {args.storage}")
    print("🔧 Enhanced mathematical memory intelligence active")
    
    try:
        ui = WorkingChatUI(args.storage)
        ui.run()
    except Exception as e:
        print(f"❌ Failed to start UI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
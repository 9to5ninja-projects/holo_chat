#!/usr/bin/env python3
"""
Holographic Memory Widget for LLM Consciousness GUI
==================================================

Integrates the holographic memory system with emotional weighting
into the existing PySide6 GUI framework.

Features:
- Real-time memory formation visualization
- Emotional and consciousness analysis
- Interactive memory recall testing
- Memory consolidation controls
- Performance monitoring

Author: Lumina Memory Team
License: MIT
"""

import sys
import os
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTextEdit, QLineEdit,
    QPushButton, QLabel, QTreeWidget, QTreeWidgetItem, QSplitter,
    QGroupBox, QProgressBar, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QDialogButtonBox, QFormLayout
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QFont, QColor, QPalette

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

try:
    from lumina_memory.enhanced_xpunit import EnhancedXPUnit
    from lumina_memory.llm_memory_tester import (
        LLMMemoryTester, EmotionalAnalyzer, ContextualAnalyzer, TemporalAnalyzer
    )
except ImportError as e:
    print(f"Warning: Could not import memory modules: {e}")
    # Create stub classes for development
    class LLMMemoryTester:
        def __init__(self, dimension=512): pass
        def add_conversation_turn(self, speaker, message): return None
        def test_memory_recall(self, query): return {'role_results': [], 'compositional_results': []}
        def get_memory_performance_report(self): return {'conversation_summary': {}, 'memory_quality': {}}

class MemoryVisualizationWidget(QWidget):
    """Widget for visualizing memory formation patterns"""
    
    def __init__(self):
        super().__init__()
        self.memory_data = []
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🧠 Memory Formation Visualization")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Memory importance chart (simplified text-based for now)
        self.importance_display = QTextEdit()
        self.importance_display.setMaximumHeight(200)
        self.importance_display.setFont(QFont("Consolas", 9))
        layout.addWidget(self.importance_display)
        
        # Memory statistics
        stats_group = QGroupBox("Memory Statistics")
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_labels = {
            'total': QLabel("Total Memories: 0"),
            'high_consciousness': QLabel("High Consciousness: 0"),
            'emotional': QLabel("Emotional Memories: 0"),
            'avg_importance': QLabel("Average Importance: 0.000")
        }
        
        for label in self.stats_labels.values():
            label.setFont(QFont("Consolas", 9))
            stats_layout.addWidget(label)
            
        layout.addWidget(stats_group)
        
    def update_visualization(self, memory_data: List[Dict]):
        """Update visualization with new memory data"""
        self.memory_data = memory_data
        
        if not memory_data:
            return
            
        # Update importance display
        importance_text = "Memory Importance Timeline:\n"
        importance_text += "=" * 40 + "\n"
        
        for i, memory in enumerate(memory_data[-10:]):  # Show last 10
            importance = memory.get('composite_importance', 0)
            consciousness = memory.get('consciousness_level', 'LOW')
            emotion = memory.get('dominant_emotion', 'None')
            
            # Create visual bar
            bar_length = int(importance * 10)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            
            importance_text += f"{i+1:2d}. {bar} {importance:.3f} [{consciousness}] {emotion}\n"
            
        self.importance_display.setPlainText(importance_text)
        
        # Update statistics
        total = len(memory_data)
        high_consciousness = len([m for m in memory_data if m.get('consciousness_level') == 'HIGH'])
        emotional = len([m for m in memory_data if m.get('emotional_weight', 0) > 0.5])
        avg_importance = sum(m.get('composite_importance', 0) for m in memory_data) / max(1, total)
        
        self.stats_labels['total'].setText(f"Total Memories: {total}")
        self.stats_labels['high_consciousness'].setText(f"High Consciousness: {high_consciousness} ({high_consciousness/max(1,total):.1%})")
        self.stats_labels['emotional'].setText(f"Emotional Memories: {emotional} ({emotional/max(1,total):.1%})")
        self.stats_labels['avg_importance'].setText(f"Average Importance: {avg_importance:.3f}")

class MemoryRecallDialog(QDialog):
    """Dialog for testing memory recall"""
    
    def __init__(self, memory_tester, parent=None):
        super().__init__(parent)
        self.memory_tester = memory_tester
        self.setWindowTitle("Test Memory Recall")
        self.setModal(True)
        self.resize(500, 400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Query input
        form_layout = QFormLayout()
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter your recall query...")
        form_layout.addRow("Query:", self.query_input)
        layout.addLayout(form_layout)
        
        # Test button
        test_button = QPushButton("🔍 Test Recall")
        test_button.clicked.connect(self.test_recall)
        layout.addWidget(test_button)
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setFont(QFont("Consolas", 9))
        layout.addWidget(self.results_display)
        
        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        # Connect Enter key
        self.query_input.returnPressed.connect(self.test_recall)
        
    def test_recall(self):
        """Test memory recall with the entered query"""
        query = self.query_input.text().strip()
        if not query:
            return
            
        try:
            result = self.memory_tester.test_memory_recall(query)
            
            # Display results
            results_text = f"Query: {query}\n"
            results_text += "=" * 50 + "\n\n"
            
            results_text += "Role-based Results:\n"
            for i, (symbol, similarity) in enumerate(result.get('role_results', [])[:5]):
                results_text += f"  {i+1}. {symbol} (similarity: {similarity:.3f})\n"
                
            if result.get('compositional_results'):
                results_text += "\nCompositional Results:\n"
                for i, (content, similarity) in enumerate(result['compositional_results'][:3]):
                    content_preview = content[:50] + "..." if len(content) > 50 else content
                    results_text += f"  {i+1}. '{content_preview}' (similarity: {similarity:.3f})\n"
                    
            results_text += f"\nRecall Success: {'✅ YES' if result.get('recall_success', False) else '❌ NO'}"
            
            self.results_display.setPlainText(results_text)
            
        except Exception as e:
            QMessageBox.warning(self, "Recall Error", f"Failed to test recall: {e}")

class HolographicMemoryWidget(QWidget):
    """Main widget for holographic memory interaction"""
    
    # Signals
    memory_updated = Signal(list)  # Emitted when memory data changes
    
    def __init__(self):
        super().__init__()
        self.memory_tester = LLMMemoryTester(dimension=512)
        self.conversation_data = []
        self.setup_ui()
        
        # Timer for periodic updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_displays)
        self.update_timer.start(1000)  # Update every second
        
    def setup_ui(self):
        """Setup the main UI layout"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🧠 Holographic Memory System")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Chat tab
        chat_widget = self.create_chat_widget()
        tabs.addTab(chat_widget, "💬 Conversation")
        
        # Visualization tab
        self.viz_widget = MemoryVisualizationWidget()
        tabs.addTab(self.viz_widget, "📈 Visualization")
        
        # Memory details tab
        memory_details_widget = self.create_memory_details_widget()
        tabs.addTab(memory_details_widget, "🧠 Memory Details")
        
        # Control buttons
        controls_layout = QHBoxLayout()
        
        recall_button = QPushButton("🔍 Test Recall")
        recall_button.clicked.connect(self.open_recall_dialog)
        controls_layout.addWidget(recall_button)
        
        report_button = QPushButton("📊 Memory Report")
        report_button.clicked.connect(self.show_memory_report)
        controls_layout.addWidget(report_button)
        
        consolidate_button = QPushButton("🔄 Consolidate")
        consolidate_button.clicked.connect(self.consolidate_memories)
        controls_layout.addWidget(consolidate_button)
        
        clear_button = QPushButton("🗑️ Clear")
        clear_button.clicked.connect(self.clear_memory)
        controls_layout.addWidget(clear_button)
        
        layout.addLayout(controls_layout)
        
    def create_chat_widget(self):
        """Create the chat interface widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setFont(QFont("Consolas", 10))
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)
        
        layout.addLayout(input_layout)
        
        # Add welcome message
        self.add_system_message("🧠 Holographic Memory System initialized! Start a conversation to test memory formation.")
        
        return widget
        
    def create_memory_details_widget(self):
        """Create the memory details widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Memory table
        self.memory_table = QTableWidget()
        self.memory_table.setColumnCount(5)
        self.memory_table.setHorizontalHeaderLabels([
            "Message", "Speaker", "Importance", "Consciousness", "Emotion"
        ])
        
        # Set column widths
        self.memory_table.setColumnWidth(0, 300)
        self.memory_table.setColumnWidth(1, 80)
        self.memory_table.setColumnWidth(2, 100)
        self.memory_table.setColumnWidth(3, 120)
        self.memory_table.setColumnWidth(4, 100)
        
        layout.addWidget(self.memory_table)
        
        return widget
        
    def add_system_message(self, message: str):
        """Add a system message to the chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.append(f"<span style='color: #666;'>[{timestamp}] SYSTEM: {message}</span>")
        
    def add_chat_message(self, speaker: str, message: str, analysis: Dict = None):
        """Add a message to the chat with optional analysis"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color code speakers
        color = "#0066cc" if speaker.lower() == "human" else "#cc6600"
        
        self.chat_display.append(f"<span style='color: {color}; font-weight: bold;'>[{timestamp}] {speaker.upper()}:</span> {message}")
        
        if analysis:
            self.chat_display.append(
                f"<span style='color: #666; font-size: 9pt;'>"
                f"  🧠 Consciousness: {analysis.get('consciousness_level', 'N/A')} "
                f"({analysis.get('consciousness_score', 0):.3f}) | "
                f"😊 Emotional: {analysis.get('dominant_emotion', 'None')} "
                f"({analysis.get('emotional_weight', 0):.3f}) | "
                f"🎯 Importance: {analysis.get('composite_importance', 0):.3f}"
                f"</span>"
            )
            
    def send_message(self):
        """Send user message and process it"""
        message = self.message_input.text().strip()
        if not message:
            return
            
        # Clear input
        self.message_input.clear()
        
        # Process user message
        self.process_message(message, "human")
        
        # Generate assistant response
        assistant_response = self.generate_assistant_response(message)
        self.process_message(assistant_response, "assistant")
        
    def process_message(self, message: str, speaker: str):
        """Process a message through the memory system"""
        try:
            # Add conversation turn
            turn = self.memory_tester.add_conversation_turn(speaker, message)
            
            # Extract analysis data
            analysis_data = {
                'message': message,
                'speaker': speaker,
                'consciousness_score': 0.0,
                'consciousness_level': 'LOW',
                'emotional_weight': turn.emotional_analysis['total_emotional_weight'],
                'dominant_emotion': turn.emotional_analysis['dominant_emotion'],
                'contextual_importance': turn.contextual_analysis['contextual_importance'],
                'temporal_importance': turn.temporal_analysis['temporal_importance'],
                'composite_importance': 0.0
            }
            
            # Get consciousness data from XPUnit
            if hasattr(self.memory_tester, 'memory_env') and self.memory_tester.memory_env.xpunits:
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
            
            # Emit signal for other widgets
            self.memory_updated.emit(self.conversation_data)
            
        except Exception as e:
            self.add_system_message(f"Error processing message: {e}")
            
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
        
    def update_displays(self):
        """Update all displays with current data"""
        if self.conversation_data:
            self.viz_widget.update_visualization(self.conversation_data)
            self.update_memory_table()
            
    def update_memory_table(self):
        """Update the memory details table"""
        self.memory_table.setRowCount(len(self.conversation_data))
        
        for i, memory in enumerate(self.conversation_data):
            # Message preview
            message_preview = memory['message'][:50] + "..." if len(memory['message']) > 50 else memory['message']
            self.memory_table.setItem(i, 0, QTableWidgetItem(message_preview))
            
            # Speaker
            self.memory_table.setItem(i, 1, QTableWidgetItem(memory['speaker']))
            
            # Importance
            importance_item = QTableWidgetItem(f"{memory['composite_importance']:.3f}")
            if memory['composite_importance'] > 2.0:
                importance_item.setBackground(QColor(255, 200, 200))  # Light red for high importance
            self.memory_table.setItem(i, 2, importance_item)
            
            # Consciousness
            consciousness_text = f"{memory['consciousness_level']} ({memory['consciousness_score']:.3f})"
            consciousness_item = QTableWidgetItem(consciousness_text)
            if memory['consciousness_level'] == 'HIGH':
                consciousness_item.setBackground(QColor(200, 255, 200))  # Light green for high consciousness
            self.memory_table.setItem(i, 3, consciousness_item)
            
            # Emotion
            emotion_text = memory['dominant_emotion'] or 'None'
            self.memory_table.setItem(i, 4, QTableWidgetItem(emotion_text))
            
    def open_recall_dialog(self):
        """Open the memory recall testing dialog"""
        dialog = MemoryRecallDialog(self.memory_tester, self)
        dialog.exec()
        
    def show_memory_report(self):
        """Show comprehensive memory report"""
        try:
            report = self.memory_tester.get_memory_performance_report()
            
            # Create report dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("Memory Performance Report")
            dialog.resize(600, 500)
            
            layout = QVBoxLayout(dialog)
            
            report_text = QTextEdit()
            report_text.setFont(QFont("Consolas", 9))
            report_text.setReadOnly(True)
            
            # Format report
            report_content = f"""MEMORY PERFORMANCE REPORT
{'='*50}

CONVERSATION SUMMARY:
  Total turns: {report.get('conversation_summary', {}).get('total_turns', 0)}
  Memories formed: {report.get('conversation_summary', {}).get('memories_formed', 0)}
  Formation rate: {report.get('conversation_summary', {}).get('memory_formation_rate', 0):.3f} memories/turn

MEMORY QUALITY:
  Emotional memory rate: {report.get('memory_quality', {}).get('emotional_memory_rate', 0):.3f}
  High consciousness rate: {report.get('memory_quality', {}).get('consciousness_rate', 0):.3f}
  Average importance: {report.get('memory_quality', {}).get('average_importance', 0):.3f}

RECALL PERFORMANCE:
  Total tests: {report.get('recall_performance', {}).get('total_recall_tests', 0)}
  Successful recalls: {report.get('recall_performance', {}).get('successful_recalls', 0)}
  Success rate: {report.get('recall_performance', {}).get('recall_success_rate', 0):.3f}
"""
            
            report_text.setPlainText(report_content)
            layout.addWidget(report_text)
            
            # Close button
            buttons = QDialogButtonBox(QDialogButtonBox.Close)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            
            dialog.exec()
            
        except Exception as e:
            QMessageBox.warning(self, "Report Error", f"Failed to generate report: {e}")
            
    def consolidate_memories(self):
        """Consolidate similar memories"""
        try:
            # Get stats before
            stats_before = len(self.conversation_data)
            
            # Perform consolidation (simplified for now)
            if hasattr(self.memory_tester, 'memory_env'):
                self.memory_tester.memory_env.consolidate_memories(similarity_threshold=0.8)
            
            # Get stats after
            stats_after = len(self.conversation_data)
            
            self.add_system_message(f"Memory consolidation completed! ({stats_before} → {stats_after})")
            
        except Exception as e:
            QMessageBox.warning(self, "Consolidation Error", f"Failed to consolidate memories: {e}")
            
    def clear_memory(self):
        """Clear all memory data"""
        reply = QMessageBox.question(
            self, "Clear Memory", 
            "This will clear all conversation history and memories. Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.conversation_data.clear()
            self.memory_tester = LLMMemoryTester(dimension=512)
            self.chat_display.clear()
            self.memory_table.setRowCount(0)
            self.add_system_message("🧠 Memory system reset. Ready for new conversation!")
            self.memory_updated.emit([])

# Test function for standalone usage
def test_holographic_memory_widget():
    """Test the holographic memory widget standalone"""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    widget = HolographicMemoryWidget()
    widget.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_holographic_memory_widget()
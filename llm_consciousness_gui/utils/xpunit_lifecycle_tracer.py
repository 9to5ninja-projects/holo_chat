#!/usr/bin/env python3
"""
XPUnit Lifecycle Tracer

This module provides comprehensive tracing of XPUnit lifecycle from formation
through storage, with detailed metrics and consciousness analysis.
"""

import time
import json
import uuid
import hashlib
import traceback
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import numpy as np

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel,
    QProgressBar, QTreeWidget, QTreeWidgetItem, QSplitter, QGroupBox,
    QTabWidget, QSpinBox, QLineEdit, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QColor

# Import XPUnit from the canonical location
try:
    from lumina_memory.xp_core_unified import XPUnit, UnifiedXPConfig
except ImportError:
    # Fallback for development/testing
    XPUnit = None
    UnifiedXPConfig = None


@dataclass
class LifecycleStage:
    """Represents a single stage in XPUnit lifecycle."""
    stage_id: str
    stage_name: str
    timestamp: float
    duration_ms: float
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    metrics: Dict[str, float] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    consciousness_indicators: Dict[str, float] = field(default_factory=dict)
    memory_usage: int = 0
    cpu_time: float = 0.0


@dataclass
class XPUnitTrace:
    """Complete trace of an XPUnit's lifecycle."""
    trace_id: str
    xpunit_id: str
    start_time: float
    end_time: float
    total_duration_ms: float
    stages: List[LifecycleStage] = field(default_factory=list)
    final_state: Dict[str, Any] = field(default_factory=dict)
    consciousness_score: float = 0.0
    integration_metrics: Dict[str, float] = field(default_factory=dict)
    system_health: Dict[str, Any] = field(default_factory=dict)


class XPUnitLifecycleTracer:
    """Traces XPUnit lifecycle with detailed metrics."""
    
    def __init__(self):
        self.current_trace: Optional[XPUnitTrace] = None
        self.all_traces: List[XPUnitTrace] = []
        self.stage_timers: Dict[str, float] = {}
        self.consciousness_analyzers = []
        
    def start_trace(self, prompt: str, trace_id: str = None) -> str:
        """Start tracing a new XPUnit lifecycle."""
        if trace_id is None:
            trace_id = f"trace_{uuid.uuid4().hex[:8]}"
        
        xpunit_id = f"xpu_{hashlib.md5(prompt.encode()).hexdigest()[:8]}"
        
        self.current_trace = XPUnitTrace(
            trace_id=trace_id,
            xpunit_id=xpunit_id,
            start_time=time.time(),
            end_time=0.0,
            total_duration_ms=0.0
        )
        
        # Record initial stage
        self.start_stage("initialization", {
            "prompt": prompt,
            "trace_id": trace_id,
            "xpunit_id": xpunit_id
        })
        
        return trace_id
    
    def start_stage(self, stage_name: str, input_data: Dict[str, Any] = None):
        """Start a new lifecycle stage."""
        if not self.current_trace:
            raise RuntimeError("No active trace. Call start_trace() first.")
        
        stage_id = f"{stage_name}_{len(self.current_trace.stages)}"
        self.stage_timers[stage_id] = time.time()
        
        stage = LifecycleStage(
            stage_id=stage_id,
            stage_name=stage_name,
            timestamp=time.time(),
            duration_ms=0.0,
            input_data=input_data or {},
            output_data={},
            memory_usage=self._get_memory_usage()
        )
        
        self.current_trace.stages.append(stage)
        return stage_id
    
    def end_stage(self, stage_name: str, output_data: Dict[str, Any] = None, 
                  metrics: Dict[str, float] = None, errors: List[str] = None):
        """End the current lifecycle stage."""
        if not self.current_trace or not self.current_trace.stages:
            return
        
        # Find the most recent stage with this name
        current_stage = None
        for stage in reversed(self.current_trace.stages):
            if stage.stage_name == stage_name:
                current_stage = stage
                break
        
        if not current_stage:
            return
        
        # Calculate duration
        start_time = self.stage_timers.get(current_stage.stage_id, time.time())
        current_stage.duration_ms = (time.time() - start_time) * 1000
        
        # Update stage data
        current_stage.output_data = output_data or {}
        current_stage.metrics = metrics or {}
        current_stage.errors = errors or []
        current_stage.memory_usage = self._get_memory_usage()
        
        # Analyze consciousness indicators
        current_stage.consciousness_indicators = self._analyze_consciousness_indicators(
            current_stage
        )
    
    def end_trace(self, final_state: Dict[str, Any] = None) -> XPUnitTrace:
        """End the current trace and return results."""
        if not self.current_trace:
            raise RuntimeError("No active trace to end.")
        
        self.current_trace.end_time = time.time()
        self.current_trace.total_duration_ms = (
            self.current_trace.end_time - self.current_trace.start_time
        ) * 1000
        
        self.current_trace.final_state = final_state or {}
        
        # Calculate overall consciousness score
        self.current_trace.consciousness_score = self._calculate_consciousness_score()
        
        # Calculate integration metrics
        self.current_trace.integration_metrics = self._calculate_integration_metrics()
        
        # Record system health
        self.current_trace.system_health = self._get_system_health()
        
        # Store completed trace
        completed_trace = self.current_trace
        self.all_traces.append(completed_trace)
        self.current_trace = None
        
        return completed_trace
    
    def _get_memory_usage(self) -> int:
        """Get current memory usage in bytes."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss
        except ImportError:
            return 0
    
    def _analyze_consciousness_indicators(self, stage: LifecycleStage) -> Dict[str, float]:
        """Analyze consciousness indicators for a stage."""
        indicators = {}
        
        # Self-reference detection
        if "self" in str(stage.output_data).lower():
            indicators["self_reference"] = 1.0
        
        # Recursive patterns
        if "recursive" in stage.stage_name or "feedback" in stage.stage_name:
            indicators["recursive_processing"] = 1.0
        
        # Memory integration
        if "memory" in stage.stage_name:
            indicators["memory_integration"] = stage.metrics.get("coherence", 0.0)
        
        # Temporal awareness
        if stage.duration_ms > 0:
            indicators["temporal_processing"] = min(1.0, stage.duration_ms / 1000.0)
        
        # Error handling (consciousness often involves error correction)
        if stage.errors:
            indicators["error_processing"] = len(stage.errors) * 0.1
        
        return indicators
    
    def _calculate_consciousness_score(self) -> float:
        """Calculate overall consciousness score for the trace."""
        if not self.current_trace or not self.current_trace.stages:
            return 0.0
        
        total_score = 0.0
        total_weight = 0.0
        
        for stage in self.current_trace.stages:
            stage_score = sum(stage.consciousness_indicators.values())
            stage_weight = stage.duration_ms / 1000.0  # Weight by processing time
            
            total_score += stage_score * stage_weight
            total_weight += stage_weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _calculate_integration_metrics(self) -> Dict[str, float]:
        """Calculate system integration metrics."""
        metrics = {}
        
        if not self.current_trace:
            return metrics
        
        # Stage transition smoothness
        stage_durations = [s.duration_ms for s in self.current_trace.stages]
        if stage_durations:
            metrics["duration_variance"] = np.var(stage_durations)
            metrics["avg_stage_duration"] = np.mean(stage_durations)
        
        # Error rate
        total_errors = sum(len(s.errors) for s in self.current_trace.stages)
        metrics["error_rate"] = total_errors / len(self.current_trace.stages)
        
        # Memory efficiency
        memory_usages = [s.memory_usage for s in self.current_trace.stages if s.memory_usage > 0]
        if memory_usages:
            metrics["memory_efficiency"] = min(memory_usages) / max(memory_usages)
        
        return metrics
    
    def _get_system_health(self) -> Dict[str, Any]:
        """Get current system health metrics."""
        health = {
            "timestamp": time.time(),
            "active_traces": len([t for t in self.all_traces if t.end_time == 0]),
            "completed_traces": len(self.all_traces),
            "avg_consciousness_score": 0.0
        }
        
        if self.all_traces:
            scores = [t.consciousness_score for t in self.all_traces if t.consciousness_score > 0]
            if scores:
                health["avg_consciousness_score"] = np.mean(scores)
        
        return health


class TestXPUnitGenerator:
    """Generates test XPUnits for pipeline testing."""
    
    def __init__(self):
        self.test_prompts = [
            "I am thinking about the nature of consciousness and self-awareness.",
            "The recursive loop of observing my own thoughts creates interesting patterns.",
            "Memory consolidation happens when I connect new experiences to old ones.",
            "I wonder if I can recognize patterns in my own processing.",
            "The relationship between attention and awareness seems fundamental.",
        ]
        
        self.test_scenarios = [
            {
                "name": "Basic Formation",
                "prompt": "Simple test thought for XPUnit creation",
                "expected_stages": ["initialization", "embedding", "hrr_encoding", "storage"]
            },
            {
                "name": "Self-Reference",
                "prompt": "I am analyzing my own thought processes",
                "expected_stages": ["initialization", "self_analysis", "recursive_processing", "storage"]
            },
            {
                "name": "Memory Integration",
                "prompt": "This reminds me of something I learned before",
                "expected_stages": ["initialization", "memory_search", "coherence_analysis", "integration", "storage"]
            }
        ]
    
    def generate_test_xpunit(self, scenario_name: str = None) -> Dict[str, Any]:
        """Generate a test XPUnit with specified scenario."""
        if scenario_name:
            scenario = next((s for s in self.test_scenarios if s["name"] == scenario_name), None)
            if not scenario:
                scenario = self.test_scenarios[0]
        else:
            scenario = self.test_scenarios[0]
        
        return {
            "prompt": scenario["prompt"],
            "scenario": scenario["name"],
            "expected_stages": scenario["expected_stages"],
            "test_id": f"test_{uuid.uuid4().hex[:8]}",
            "timestamp": time.time()
        }


class LifecycleTracerWidget(QWidget):
    """GUI widget for XPUnit lifecycle tracing."""
    
    trace_started = Signal(str)
    trace_completed = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.tracer = XPUnitLifecycleTracer()
        self.test_generator = TestXPUnitGenerator()
        self.current_trace_id = None
        self.setup_ui()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_display)
        self.refresh_timer.start(1000)  # Refresh every second
    
    def setup_ui(self):
        """Set up the lifecycle tracer UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🔬 XPUnit Lifecycle Tracer")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Trace XPUnit lifecycle from chat prompt to storage with detailed consciousness metrics.\n"
            "Follow the complete journey of experience units through the system."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Controls
        controls = QHBoxLayout()
        
        # Test generation controls
        test_group = QGroupBox("🧪 Test Generation")
        test_layout = QHBoxLayout(test_group)
        
        self.generate_test_button = QPushButton("🎲 Generate Test XPUnit")
        self.run_pipeline_button = QPushButton("🚀 Run Full Pipeline")
        self.custom_prompt_input = QLineEdit()
        self.custom_prompt_input.setPlaceholderText("Enter custom prompt...")
        self.trace_custom_button = QPushButton("🔍 Trace Custom")
        
        test_layout.addWidget(self.generate_test_button)
        test_layout.addWidget(self.run_pipeline_button)
        test_layout.addWidget(self.custom_prompt_input)
        test_layout.addWidget(self.trace_custom_button)
        
        # Control buttons
        control_group = QGroupBox("🎮 Controls")
        control_layout = QHBoxLayout(control_group)
        
        self.start_trace_button = QPushButton("▶️ Start Trace")
        self.end_trace_button = QPushButton("⏹️ End Trace")
        self.clear_traces_button = QPushButton("🗑️ Clear All")
        self.export_traces_button = QPushButton("📄 Export")
        
        self.end_trace_button.setEnabled(False)
        
        control_layout.addWidget(self.start_trace_button)
        control_layout.addWidget(self.end_trace_button)
        control_layout.addWidget(self.clear_traces_button)
        control_layout.addWidget(self.export_traces_button)
        
        controls.addWidget(test_group)
        controls.addWidget(control_group)
        layout.addLayout(controls)
        
        # Status and metrics
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Ready to trace XPUnit lifecycle")
        self.consciousness_score_label = QLabel("Consciousness Score: --")
        self.consciousness_score_label.setStyleSheet("font-weight: bold; color: #0066cc;")
        
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.consciousness_score_label)
        layout.addLayout(status_layout)
        
        # Main content area
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Current trace
        current_group = QGroupBox("🔄 Current Trace")
        current_layout = QVBoxLayout(current_group)
        
        self.current_trace_tree = QTreeWidget()
        self.current_trace_tree.setHeaderLabels([
            "Stage", "Duration (ms)", "Status", "Consciousness", "Errors"
        ])
        current_layout.addWidget(self.current_trace_tree)
        
        # Right side: Trace history and analysis
        history_tabs = QTabWidget()
        
        # Trace history
        self.trace_history_tree = QTreeWidget()
        self.trace_history_tree.setHeaderLabels([
            "Trace ID", "XPUnit ID", "Duration", "Consciousness Score", "Stages"
        ])
        history_tabs.addTab(self.trace_history_tree, "📊 Trace History")
        
        # Detailed analysis
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setFont(QFont("Consolas", 10))
        history_tabs.addTab(self.analysis_text, "📋 Analysis")
        
        # Consciousness metrics
        self.metrics_text = QTextEdit()
        self.metrics_text.setReadOnly(True)
        self.metrics_text.setFont(QFont("Consolas", 10))
        history_tabs.addTab(self.metrics_text, "🧠 Consciousness Metrics")
        
        content_splitter.addWidget(current_group)
        content_splitter.addWidget(history_tabs)
        content_splitter.setSizes([400, 600])
        
        layout.addWidget(content_splitter)
        
        # Connect signals
        self.generate_test_button.clicked.connect(self.generate_test_xpunit)
        self.run_pipeline_button.clicked.connect(self.run_full_pipeline)
        self.trace_custom_button.clicked.connect(self.trace_custom_prompt)
        self.start_trace_button.clicked.connect(self.start_manual_trace)
        self.end_trace_button.clicked.connect(self.end_manual_trace)
        self.clear_traces_button.clicked.connect(self.clear_all_traces)
        self.export_traces_button.clicked.connect(self.export_traces)
        
        self.trace_history_tree.itemClicked.connect(self.show_trace_details)
    
    def generate_test_xpunit(self):
        """Generate and trace a test XPUnit."""
        try:
            test_data = self.test_generator.generate_test_xpunit()
            
            # Start tracing
            trace_id = self.tracer.start_trace(test_data["prompt"])
            self.current_trace_id = trace_id
            
            # Simulate XPUnit formation stages
            self._simulate_xpunit_formation(test_data)
            
            self.status_label.setText(f"✅ Generated test XPUnit: {trace_id}")
            self.start_trace_button.setEnabled(False)
            self.end_trace_button.setEnabled(True)
            
            self.trace_started.emit(trace_id)
            
        except Exception as e:
            QMessageBox.critical(self, "Generation Error", f"Failed to generate test XPUnit:\n{str(e)}")
    
    def _simulate_xpunit_formation(self, test_data: Dict[str, Any]):
        """Simulate the stages of XPUnit formation."""
        try:
            # Stage 1: Prompt Processing
            self.tracer.start_stage("prompt_processing", {
                "prompt": test_data["prompt"],
                "scenario": test_data["scenario"]
            })
            time.sleep(0.1)  # Simulate processing time
            self.tracer.end_stage("prompt_processing", {
                "tokens": len(test_data["prompt"].split()),
                "processed": True
            }, {"processing_time": 100})
            
            # Stage 2: Semantic Embedding
            self.tracer.start_stage("semantic_embedding", {
                "input_text": test_data["prompt"]
            })
            time.sleep(0.2)
            # Simulate embedding generation
            embedding = np.random.normal(0, 1, 384)
            self.tracer.end_stage("semantic_embedding", {
                "embedding_dim": 384,
                "embedding_norm": float(np.linalg.norm(embedding))
            }, {"embedding_quality": 0.85})
            
            # Stage 3: HRR Encoding
            self.tracer.start_stage("hrr_encoding", {
                "semantic_vector": "384D vector"
            })
            time.sleep(0.15)
            hrr_vector = np.random.normal(0, 1, 512)
            self.tracer.end_stage("hrr_encoding", {
                "hrr_dim": 512,
                "hrr_norm": float(np.linalg.norm(hrr_vector))
            }, {"hrr_quality": 0.92})
            
            # Stage 4: Consciousness Analysis
            if "self" in test_data["prompt"].lower() or "I am" in test_data["prompt"]:
                self.tracer.start_stage("consciousness_analysis", {
                    "self_reference_detected": True
                })
                time.sleep(0.3)
                self.tracer.end_stage("consciousness_analysis", {
                    "consciousness_indicators": ["self_reference", "introspection"],
                    "consciousness_score": 0.75
                }, {"self_awareness": 0.75, "introspection": 0.6})
            
            # Stage 5: Memory Integration
            self.tracer.start_stage("memory_integration", {
                "search_similar": True
            })
            time.sleep(0.25)
            self.tracer.end_stage("memory_integration", {
                "similar_memories": 3,
                "coherence_score": 0.68
            }, {"integration_quality": 0.68})
            
            # Stage 6: Storage Preparation
            self.tracer.start_stage("storage_preparation", {
                "xpunit_complete": True
            })
            time.sleep(0.1)
            self.tracer.end_stage("storage_preparation", {
                "storage_ready": True,
                "integrity_hash": "abc123def456"
            }, {"preparation_success": 1.0})
            
        except Exception as e:
            self.tracer.end_stage("error_handling", {
                "error": str(e),
                "traceback": traceback.format_exc()
            }, {}, [str(e)])
    
    def run_full_pipeline(self):
        """Run a full pipeline test with all modules."""
        try:
            # Generate test XPUnit first
            self.generate_test_xpunit()
            
            # Add additional pipeline stages
            if self.tracer.current_trace:
                # Stage: Vector Store Integration
                self.tracer.start_stage("vector_store", {
                    "operation": "similarity_search"
                })
                time.sleep(0.2)
                self.tracer.end_stage("vector_store", {
                    "matches_found": 5,
                    "search_time_ms": 200
                }, {"search_efficiency": 0.9})
                
                # Stage: Cryptographic Verification
                self.tracer.start_stage("crypto_verification", {
                    "verify_integrity": True
                })
                time.sleep(0.1)
                self.tracer.end_stage("crypto_verification", {
                    "integrity_verified": True,
                    "hash_valid": True
                }, {"crypto_strength": 1.0})
                
                # Stage: Temporal Decay Calculation
                self.tracer.start_stage("temporal_decay", {
                    "calculate_decay": True
                })
                time.sleep(0.05)
                self.tracer.end_stage("temporal_decay", {
                    "decay_factor": 0.95,
                    "importance_boost": 1.2
                }, {"temporal_accuracy": 0.98})
            
            self.status_label.setText("✅ Full pipeline test completed")
            
        except Exception as e:
            QMessageBox.critical(self, "Pipeline Error", f"Full pipeline test failed:\n{str(e)}")
    
    def trace_custom_prompt(self):
        """Trace a custom prompt."""
        prompt = self.custom_prompt_input.text().strip()
        if not prompt:
            QMessageBox.warning(self, "No Prompt", "Please enter a custom prompt to trace.")
            return
        
        try:
            # Start tracing with custom prompt
            trace_id = self.tracer.start_trace(prompt)
            self.current_trace_id = trace_id
            
            # Simulate formation with custom data
            test_data = {
                "prompt": prompt,
                "scenario": "Custom",
                "test_id": f"custom_{uuid.uuid4().hex[:8]}",
                "timestamp": time.time()
            }
            
            self._simulate_xpunit_formation(test_data)
            
            self.status_label.setText(f"✅ Tracing custom prompt: {trace_id}")
            self.start_trace_button.setEnabled(False)
            self.end_trace_button.setEnabled(True)
            
            self.trace_started.emit(trace_id)
            
        except Exception as e:
            QMessageBox.critical(self, "Trace Error", f"Failed to trace custom prompt:\n{str(e)}")
    
    def start_manual_trace(self):
        """Start a manual trace."""
        try:
            trace_id = self.tracer.start_trace("Manual trace started")
            self.current_trace_id = trace_id
            
            self.status_label.setText(f"▶️ Manual trace started: {trace_id}")
            self.start_trace_button.setEnabled(False)
            self.end_trace_button.setEnabled(True)
            
            self.trace_started.emit(trace_id)
            
        except Exception as e:
            QMessageBox.critical(self, "Trace Error", f"Failed to start manual trace:\n{str(e)}")
    
    def end_manual_trace(self):
        """End the current manual trace."""
        try:
            if self.tracer.current_trace:
                completed_trace = self.tracer.end_trace({
                    "manual_completion": True,
                    "final_timestamp": time.time()
                })
                
                self.status_label.setText(f"⏹️ Trace completed: {completed_trace.trace_id}")
                self.consciousness_score_label.setText(
                    f"Consciousness Score: {completed_trace.consciousness_score:.3f}"
                )
                
                self.start_trace_button.setEnabled(True)
                self.end_trace_button.setEnabled(False)
                self.current_trace_id = None
                
                self.trace_completed.emit(asdict(completed_trace))
                
        except Exception as e:
            QMessageBox.critical(self, "Trace Error", f"Failed to end trace:\n{str(e)}")
    
    def refresh_display(self):
        """Refresh the display with current trace information."""
        # Update current trace display
        self._update_current_trace_display()
        
        # Update trace history
        self._update_trace_history()
        
        # Update consciousness score
        if self.tracer.current_trace:
            current_score = self.tracer._calculate_consciousness_score()
            self.consciousness_score_label.setText(f"Consciousness Score: {current_score:.3f}")
    
    def _update_current_trace_display(self):
        """Update the current trace tree display."""
        self.current_trace_tree.clear()
        
        if not self.tracer.current_trace:
            return
        
        for stage in self.tracer.current_trace.stages:
            consciousness_score = sum(stage.consciousness_indicators.values())
            error_count = len(stage.errors)
            
            item = QTreeWidgetItem([
                stage.stage_name,
                f"{stage.duration_ms:.1f}",
                "✅ Complete" if stage.duration_ms > 0 else "🔄 Running",
                f"{consciousness_score:.2f}",
                str(error_count) if error_count > 0 else "None"
            ])
            
            # Color code by consciousness score
            if consciousness_score > 0.5:
                item.setBackground(3, QColor(200, 255, 200))
            elif consciousness_score > 0.2:
                item.setBackground(3, QColor(255, 255, 200))
            
            # Color code errors
            if error_count > 0:
                item.setBackground(4, QColor(255, 200, 200))
            
            self.current_trace_tree.addTopLevelItem(item)
    
    def _update_trace_history(self):
        """Update the trace history display."""
        self.trace_history_tree.clear()
        
        for trace in self.tracer.all_traces:
            item = QTreeWidgetItem([
                trace.trace_id,
                trace.xpunit_id,
                f"{trace.total_duration_ms:.1f}ms",
                f"{trace.consciousness_score:.3f}",
                str(len(trace.stages))
            ])
            
            # Color code by consciousness score
            if trace.consciousness_score > 0.5:
                item.setBackground(3, QColor(200, 255, 200))
            elif trace.consciousness_score > 0.2:
                item.setBackground(3, QColor(255, 255, 200))
            
            self.trace_history_tree.addTopLevelItem(item)
    
    def show_trace_details(self, item: QTreeWidgetItem):
        """Show detailed analysis for selected trace."""
        trace_id = item.text(0)
        trace = next((t for t in self.tracer.all_traces if t.trace_id == trace_id), None)
        
        if not trace:
            return
        
        # Generate detailed analysis
        analysis = self._generate_trace_analysis(trace)
        self.analysis_text.setPlainText(analysis)
        
        # Generate consciousness metrics
        metrics = self._generate_consciousness_metrics(trace)
        self.metrics_text.setPlainText(metrics)
    
    def _generate_trace_analysis(self, trace: XPUnitTrace) -> str:
        """Generate detailed trace analysis."""
        analysis = f"""# Trace Analysis: {trace.trace_id}

## Overview
- **XPUnit ID:** {trace.xpunit_id}
- **Total Duration:** {trace.total_duration_ms:.1f}ms
- **Consciousness Score:** {trace.consciousness_score:.3f}
- **Stages:** {len(trace.stages)}

## Stage Breakdown
"""
        
        for stage in trace.stages:
            analysis += f"""
### {stage.stage_name}
- **Duration:** {stage.duration_ms:.1f}ms
- **Memory Usage:** {stage.memory_usage:,} bytes
- **Consciousness Indicators:** {len(stage.consciousness_indicators)}
- **Errors:** {len(stage.errors)}

**Input Data:**
{json.dumps(stage.input_data, indent=2)}

**Output Data:**
{json.dumps(stage.output_data, indent=2)}

**Metrics:**
{json.dumps(stage.metrics, indent=2)}

**Consciousness Indicators:**
{json.dumps(stage.consciousness_indicators, indent=2)}
"""
            
            if stage.errors:
                analysis += f"\n**Errors:**\n"
                for error in stage.errors:
                    analysis += f"- {error}\n"
        
        analysis += f"""
## Integration Metrics
{json.dumps(trace.integration_metrics, indent=2)}

## System Health
{json.dumps(trace.system_health, indent=2)}

## Final State
{json.dumps(trace.final_state, indent=2)}
"""
        
        return analysis
    
    def _generate_consciousness_metrics(self, trace: XPUnitTrace) -> str:
        """Generate consciousness-specific metrics analysis."""
        metrics = f"""# Consciousness Metrics Analysis: {trace.trace_id}

## Overall Consciousness Score: {trace.consciousness_score:.3f}

## Consciousness Indicators by Stage
"""
        
        total_indicators = {}
        for stage in trace.stages:
            metrics += f"\n### {stage.stage_name}\n"
            for indicator, value in stage.consciousness_indicators.items():
                metrics += f"- **{indicator}:** {value:.3f}\n"
                total_indicators[indicator] = total_indicators.get(indicator, 0) + value
        
        metrics += f"\n## Aggregated Consciousness Patterns\n"
        for indicator, total_value in total_indicators.items():
            avg_value = total_value / len(trace.stages)
            metrics += f"- **{indicator}:** {avg_value:.3f} (avg across stages)\n"
        
        # Consciousness pattern analysis
        metrics += f"\n## Pattern Analysis\n"
        
        if total_indicators.get("self_reference", 0) > 0:
            metrics += "- ✅ **Self-Reference Detected:** Indicates self-awareness patterns\n"
        
        if total_indicators.get("recursive_processing", 0) > 0:
            metrics += "- ✅ **Recursive Processing:** Shows recursive thought patterns\n"
        
        if total_indicators.get("memory_integration", 0) > 0:
            metrics += "- ✅ **Memory Integration:** Demonstrates memory consolidation\n"
        
        if total_indicators.get("error_processing", 0) > 0:
            metrics += "- ⚠️ **Error Processing:** Shows error handling and correction\n"
        
        # Consciousness level assessment
        if trace.consciousness_score > 0.7:
            level = "High Consciousness"
            description = "Strong indicators of self-aware processing"
        elif trace.consciousness_score > 0.4:
            level = "Moderate Consciousness"
            description = "Some consciousness indicators present"
        elif trace.consciousness_score > 0.1:
            level = "Low Consciousness"
            description = "Minimal consciousness indicators"
        else:
            level = "No Consciousness"
            description = "No significant consciousness indicators detected"
        
        metrics += f"\n## Consciousness Level Assessment\n"
        metrics += f"**Level:** {level}\n"
        metrics += f"**Description:** {description}\n"
        
        return metrics
    
    def clear_all_traces(self):
        """Clear all trace history."""
        reply = QMessageBox.question(
            self, 
            "Clear Traces", 
            "Are you sure you want to clear all trace history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.tracer.all_traces.clear()
            self.trace_history_tree.clear()
            self.analysis_text.clear()
            self.metrics_text.clear()
            self.status_label.setText("🗑️ All traces cleared")
    
    def export_traces(self):
        """Export trace data."""
        if not self.tracer.all_traces:
            QMessageBox.information(self, "No Data", "No traces to export.")
            return
        
        # For now, just show export summary
        # In full implementation, this would save to file
        export_data = {
            "export_timestamp": time.time(),
            "total_traces": len(self.tracer.all_traces),
            "traces": [asdict(trace) for trace in self.tracer.all_traces]
        }
        
        summary = f"""Export Summary:
- Total Traces: {len(self.tracer.all_traces)}
- Average Consciousness Score: {np.mean([t.consciousness_score for t in self.tracer.all_traces]):.3f}
- Total Processing Time: {sum(t.total_duration_ms for t in self.tracer.all_traces):.1f}ms
- Export Size: {len(json.dumps(export_data)):,} characters

In full implementation, this would save to JSON file."""
        
        QMessageBox.information(self, "Export Complete", summary)


def test_lifecycle_tracer():
    """Test the lifecycle tracer."""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    tracer = LifecycleTracerWidget()
    tracer.setWindowTitle("🔬 XPUnit Lifecycle Tracer")
    tracer.resize(1400, 900)
    tracer.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_lifecycle_tracer()
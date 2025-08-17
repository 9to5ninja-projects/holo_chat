#!/usr/bin/env python3
"""
Intelligent XPUnit Consolidation with LLM Integration

This module provides AI-powered analysis and consolidation of XPUnit definitions
using the integrated LLM to provide intelligent suggestions and code generation.
"""

import json
import requests
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel,
    QProgressBar, QMessageBox, QSplitter, QGroupBox, QTabWidget
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

from .xpunit_consolidator import XPUnitAnalyzer, XPUnitDefinition, ConsolidationIssue


class LLMConsolidationWorker(QThread):
    """Worker thread for LLM-powered consolidation analysis."""
    
    analysis_complete = Signal(dict)
    progress_update = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, analyzer: XPUnitAnalyzer, llm_endpoint: str = "http://localhost:11434/api/generate"):
        super().__init__()
        self.analyzer = analyzer
        self.llm_endpoint = llm_endpoint
        self.model = "mistral:7b-instruct"
    
    def run(self):
        """Run the LLM-powered consolidation analysis."""
        try:
            self.progress_update.emit("🤖 Starting LLM analysis...")
            
            # Generate comprehensive analysis prompt
            analysis_prompt = self._create_analysis_prompt()
            
            self.progress_update.emit("🧠 Querying LLM for consolidation insights...")
            
            # Query LLM for analysis
            llm_response = self._query_llm(analysis_prompt)
            
            self.progress_update.emit("📋 Generating consolidation recommendations...")
            
            # Generate specific consolidation code
            consolidation_code = self._generate_consolidation_code(llm_response)
            
            self.progress_update.emit("✅ LLM analysis complete!")
            
            # Emit results
            results = {
                "llm_analysis": llm_response,
                "consolidation_code": consolidation_code,
                "recommendations": self._extract_recommendations(llm_response),
                "canonical_definition": self._generate_canonical_definition(llm_response)
            }
            
            self.analysis_complete.emit(results)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def _create_analysis_prompt(self) -> str:
        """Create a comprehensive prompt for LLM analysis."""
        # Gather all XPUnit definitions
        definitions_summary = []
        for defn in self.analyzer.definitions:
            summary = {
                "file": str(defn.file_path.name),
                "type": defn.definition_type,
                "name": defn.name,
                "attributes": defn.attributes,
                "methods": defn.methods,
                "content_preview": defn.content[:200] + "..." if len(defn.content) > 200 else defn.content
            }
            definitions_summary.append(summary)
        
        # Gather issues
        issues_summary = []
        for issue in self.analyzer.issues:
            issues_summary.append({
                "type": issue.issue_type,
                "severity": issue.severity,
                "description": issue.description,
                "suggested_fix": issue.suggested_fix
            })
        
        prompt = f"""
# XPUnit Consolidation Analysis Request

You are an expert Python architect analyzing scattered XPUnit (Experience Unit) definitions across a memory system codebase. XPUnit is the fundamental mathematical unit of experience with holographic vector representations using HRR (Holographic Reduced Representations).

## Current XPUnit Definitions Found:
{json.dumps(definitions_summary, indent=2)}

## Issues Identified:
{json.dumps(issues_summary, indent=2)}

## Context:
- XPUnit should be a holographic vector class object
- Uses HRR operations (circular convolution/correlation) for binding/unbinding
- Has mathematical properties: cryptographic identity, temporal decay, relational coherence
- Integrates with vector-based memory storage
- Should be the fundamental building block of the entire system

## Analysis Request:
1. **Identify the most complete XPUnit definition** that should serve as the canonical version
2. **Analyze inconsistencies** between different definitions
3. **Recommend consolidation strategy** to unify all definitions
4. **Suggest missing components** that should be added to make XPUnit complete
5. **Provide specific code recommendations** for the unified XPUnit class

## Key Questions:
- Which definition has the most complete mathematical foundation?
- What critical attributes or methods are missing across definitions?
- How should the holographic vector properties be standardized?
- What's the best way to maintain backward compatibility during consolidation?

Please provide a detailed analysis with specific, actionable recommendations.
"""
        return prompt
    
    def _query_llm(self, prompt: str) -> str:
        """Query the LLM with the analysis prompt."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower temperature for more focused analysis
                    "top_p": 0.9,
                    "max_tokens": 2000
                }
            }
            
            response = requests.post(
                self.llm_endpoint,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response received")
            else:
                raise Exception(f"LLM request failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to LLM: {str(e)}")
    
    def _generate_consolidation_code(self, llm_analysis: str) -> str:
        """Generate specific consolidation code based on LLM analysis."""
        code_prompt = f"""
Based on this XPUnit analysis:

{llm_analysis}

Generate a complete, unified XPUnit class definition that:
1. Includes all necessary attributes for holographic vector operations
2. Implements HRR binding/unbinding methods
3. Has proper mathematical properties (decay, coherence, etc.)
4. Follows Python best practices with type hints
5. Is compatible with the existing memory system

Provide only the Python code for the unified XPUnit class, with comprehensive docstrings.
"""
        
        try:
            return self._query_llm(code_prompt)
        except Exception as e:
            return f"# Error generating consolidation code: {str(e)}\n# Please review the analysis and create the code manually."
    
    def _extract_recommendations(self, llm_response: str) -> List[str]:
        """Extract actionable recommendations from LLM response."""
        recommendations = []
        
        # Simple extraction - in a full implementation, this could be more sophisticated
        lines = llm_response.split('\n')
        current_rec = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•')):
                if current_rec:
                    recommendations.append(current_rec.strip())
                current_rec = line
            elif current_rec and line:
                current_rec += " " + line
        
        if current_rec:
            recommendations.append(current_rec.strip())
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _generate_canonical_definition(self, llm_response: str) -> str:
        """Extract the canonical definition recommendation from LLM response."""
        # Look for mentions of specific files or definitions
        lines = llm_response.split('\n')
        for line in lines:
            if "canonical" in line.lower() or "most complete" in line.lower():
                return line.strip()
        
        return "See LLM analysis for canonical definition recommendation"


class IntelligentConsolidatorWidget(QWidget):
    """Widget for intelligent XPUnit consolidation with LLM integration."""
    
    def __init__(self):
        super().__init__()
        self.analyzer = None
        self.llm_worker = None
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the intelligent consolidator UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🧠 Intelligent XPUnit Consolidation")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "AI-powered analysis and consolidation of scattered XPUnit definitions using LLM insights.\n"
            "This tool analyzes your codebase and provides intelligent recommendations for unifying XPUnit."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Controls
        controls = QHBoxLayout()
        self.analyze_button = QPushButton("🔍 Analyze Repository")
        self.llm_analyze_button = QPushButton("🤖 LLM Analysis")
        self.generate_code_button = QPushButton("⚡ Generate Unified Code")
        self.apply_changes_button = QPushButton("✅ Apply Changes")
        
        self.llm_analyze_button.setEnabled(False)
        self.generate_code_button.setEnabled(False)
        self.apply_changes_button.setEnabled(False)
        
        controls.addWidget(self.analyze_button)
        controls.addWidget(self.llm_analyze_button)
        controls.addWidget(self.generate_code_button)
        controls.addWidget(self.apply_changes_button)
        controls.addStretch()
        
        layout.addLayout(controls)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready to analyze repository")
        layout.addWidget(self.status_label)
        
        # Results area
        results_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Analysis results
        analysis_group = QGroupBox("📊 Analysis Results")
        analysis_layout = QVBoxLayout(analysis_group)
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setFont(QFont("Consolas", 10))
        analysis_layout.addWidget(self.analysis_text)
        
        # Right side: Generated code
        code_group = QGroupBox("🐍 Generated Code")
        code_layout = QVBoxLayout(code_group)
        
        self.code_text = QTextEdit()
        self.code_text.setFont(QFont("Consolas", 10))
        code_layout.addWidget(self.code_text)
        
        results_splitter.addWidget(analysis_group)
        results_splitter.addWidget(code_group)
        results_splitter.setSizes([400, 600])
        
        layout.addWidget(results_splitter)
        
        # Connect signals
        self.analyze_button.clicked.connect(self.analyze_repository)
        self.llm_analyze_button.clicked.connect(self.run_llm_analysis)
        self.generate_code_button.clicked.connect(self.generate_unified_code)
        self.apply_changes_button.clicked.connect(self.apply_changes)
    
    def analyze_repository(self):
        """Analyze the repository for XPUnit definitions."""
        try:
            repo_root = Path(__file__).parent.parent
            
            self.status_label.setText("🔍 Analyzing repository...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            
            # Create analyzer and run analysis
            self.analyzer = XPUnitAnalyzer(repo_root)
            results = self.analyzer.analyze_repository()
            
            # Display basic analysis results
            analysis_summary = f"""# Repository Analysis Results

## Summary
- **Definitions found:** {results['definitions']}
- **References found:** {results['references']}
- **Issues identified:** {results['issues']}
- **Files analyzed:** {results['files_analyzed']}

## Definitions
"""
            
            for defn in self.analyzer.definitions:
                analysis_summary += f"""
### {defn.name} ({defn.file_path.name})
- **Type:** {defn.definition_type}
- **Line:** {defn.line_number}
- **Attributes:** {len(defn.attributes)} ({', '.join(defn.attributes[:5])})
- **Methods:** {len(defn.methods)} ({', '.join(defn.methods[:5])})
"""
            
            analysis_summary += "\n## Issues\n"
            for issue in self.analyzer.issues:
                analysis_summary += f"- **{issue.severity.upper()}**: {issue.description}\n"
            
            self.analysis_text.setPlainText(analysis_summary)
            
            self.progress_bar.setVisible(False)
            self.status_label.setText("✅ Repository analysis complete")
            self.llm_analyze_button.setEnabled(True)
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            self.status_label.setText(f"❌ Analysis failed: {str(e)}")
            QMessageBox.critical(self, "Analysis Error", f"Failed to analyze repository:\n{str(e)}")
    
    def run_llm_analysis(self):
        """Run LLM-powered analysis."""
        if not self.analyzer:
            QMessageBox.warning(self, "No Analysis", "Please run repository analysis first.")
            return
        
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            
            # Create and start LLM worker
            self.llm_worker = LLMConsolidationWorker(self.analyzer)
            self.llm_worker.analysis_complete.connect(self.on_llm_analysis_complete)
            self.llm_worker.progress_update.connect(self.status_label.setText)
            self.llm_worker.error_occurred.connect(self.on_llm_error)
            self.llm_worker.start()
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, "LLM Analysis Error", f"Failed to start LLM analysis:\n{str(e)}")
    
    def on_llm_analysis_complete(self, results: Dict[str, Any]):
        """Handle completion of LLM analysis."""
        self.progress_bar.setVisible(False)
        self.status_label.setText("✅ LLM analysis complete")
        
        # Display LLM analysis
        llm_analysis = results.get("llm_analysis", "No analysis received")
        self.analysis_text.setPlainText(f"# LLM Analysis Results\n\n{llm_analysis}")
        
        # Display generated code
        consolidation_code = results.get("consolidation_code", "No code generated")
        self.code_text.setPlainText(consolidation_code)
        
        self.generate_code_button.setEnabled(True)
        self.apply_changes_button.setEnabled(True)
    
    def on_llm_error(self, error_message: str):
        """Handle LLM analysis error."""
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"❌ LLM analysis failed: {error_message}")
        QMessageBox.critical(self, "LLM Error", f"LLM analysis failed:\n{error_message}")
    
    def generate_unified_code(self):
        """Generate unified XPUnit code."""
        # For now, just show the current code
        # In a full implementation, this could refine the code further
        current_code = self.code_text.toPlainText()
        if current_code and "class" in current_code:
            QMessageBox.information(
                self, 
                "Code Generated", 
                "Unified XPUnit code has been generated in the code panel.\n\n"
                "Review the code and click 'Apply Changes' to save it to a file."
            )
        else:
            QMessageBox.warning(
                self, 
                "No Code", 
                "No unified code has been generated yet.\n"
                "Please run LLM analysis first."
            )
    
    def apply_changes(self):
        """Apply the generated changes."""
        code = self.code_text.toPlainText()
        if not code or "class" not in code:
            QMessageBox.warning(self, "No Code", "No code to apply. Please generate unified code first.")
            return
        
        # For now, just show a preview of what would be applied
        # In a full implementation, this would actually modify files
        QMessageBox.information(
            self,
            "Apply Changes",
            f"This would apply the unified XPUnit definition to the codebase.\n\n"
            f"Code length: {len(code)} characters\n"
            f"Contains class definition: {'Yes' if 'class XPUnit' in code else 'No'}\n\n"
            f"In a full implementation, this would:\n"
            f"1. Create a new unified XPUnit file\n"
            f"2. Update all imports to use the new definition\n"
            f"3. Run tests to ensure compatibility\n"
            f"4. Create a backup of the original files"
        )


def test_intelligent_consolidator():
    """Test the intelligent consolidator."""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    consolidator = IntelligentConsolidatorWidget()
    consolidator.setWindowTitle("🧠 Intelligent XPUnit Consolidator")
    consolidator.resize(1200, 800)
    consolidator.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_intelligent_consolidator()
#!/usr/bin/env python3
"""
XPUnit Consolidation and Analysis Tool

This module analyzes the scattered XPUnit definitions across the repository,
identifies inconsistencies, and provides tools for consolidation using the GUI.
"""

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import difflib

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QPushButton, QLabel, QSplitter, QTabWidget, QGroupBox,
    QListWidget, QListWidgetItem, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor


@dataclass
class XPUnitDefinition:
    """Represents a single XPUnit definition found in the codebase."""
    file_path: Path
    line_number: int
    definition_type: str  # "class", "dataclass", "function", "variable"
    name: str
    content: str
    attributes: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    context: str = ""  # Surrounding context
    
    def __eq__(self, other):
        if not isinstance(other, XPUnitDefinition):
            return False
        return (self.name == other.name and 
                self.definition_type == other.definition_type and
                str(self.file_path) == str(other.file_path))
    
    def __hash__(self):
        return hash((self.name, self.definition_type, str(self.file_path)))


@dataclass
class XPUnitReference:
    """Represents a reference to XPUnit in the codebase."""
    file_path: Path
    line_number: int
    reference_type: str  # "import", "usage", "type_hint", "instantiation"
    context: str
    full_line: str


@dataclass
class ConsolidationIssue:
    """Represents an issue found during consolidation analysis."""
    issue_type: str  # "inconsistent_attributes", "missing_methods", "type_mismatch"
    severity: str    # "critical", "warning", "info"
    description: str
    affected_files: List[Path]
    suggested_fix: str = ""
    
    def __eq__(self, other):
        if not isinstance(other, ConsolidationIssue):
            return False
        return (self.issue_type == other.issue_type and 
                self.description == other.description and
                [str(f) for f in self.affected_files] == [str(f) for f in other.affected_files])
    
    def __hash__(self):
        return hash((self.issue_type, self.description, tuple(str(f) for f in self.affected_files)))


class XPUnitAnalyzer:
    """Analyzes XPUnit definitions and references across the repository."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.definitions: List[XPUnitDefinition] = []
        self.references: List[XPUnitReference] = []
        self.issues: List[ConsolidationIssue] = []
        
    def analyze_repository(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of XPUnit across the repository."""
        print("🔍 Starting XPUnit repository analysis...")
        
        # Find all Python files
        python_files = list(self.repo_root.rglob("*.py"))
        python_files.extend(list(self.repo_root.rglob("*.ipynb")))
        
        print(f"📁 Found {len(python_files)} files to analyze")
        
        # Analyze each file
        for file_path in python_files:
            try:
                if file_path.suffix == ".py":
                    self._analyze_python_file(file_path)
                elif file_path.suffix == ".ipynb":
                    self._analyze_notebook_file(file_path)
            except Exception as e:
                print(f"⚠️ Error analyzing {file_path}: {e}")
        
        # Perform consolidation analysis
        self._analyze_inconsistencies()
        
        return {
            "definitions": len(self.definitions),
            "references": len(self.references),
            "issues": len(self.issues),
            "files_analyzed": len(python_files)
        }
    
    def _analyze_python_file(self, file_path: Path):
        """Analyze a Python file for XPUnit definitions and references."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for structured analysis
            try:
                tree = ast.parse(content)
                self._extract_ast_definitions(tree, file_path, content)
            except SyntaxError:
                # Fallback to text-based analysis
                pass
            
            # Text-based analysis for references
            self._extract_text_references(content, file_path)
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    def _analyze_notebook_file(self, file_path: Path):
        """Analyze a Jupyter notebook for XPUnit definitions."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            for cell_idx, cell in enumerate(notebook.get('cells', [])):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    if 'XPUnit' in source:
                        # Create pseudo line numbers for notebook cells
                        base_line = cell_idx * 100
                        self._extract_text_references(source, file_path, base_line)
                        
        except Exception as e:
            print(f"Error reading notebook {file_path}: {e}")
    
    def _extract_ast_definitions(self, tree: ast.AST, file_path: Path, content: str):
        """Extract XPUnit definitions using AST parsing."""
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'XPUnit':
                # Extract class definition
                attributes = []
                methods = []
                
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and hasattr(item.target, 'id'):
                        attributes.append(item.target.id)
                    elif isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                
                definition = XPUnitDefinition(
                    file_path=file_path,
                    line_number=node.lineno,
                    definition_type="class",
                    name=node.name,
                    content=ast.get_source_segment(content, node) or "",
                    attributes=attributes,
                    methods=methods,
                    context=self._get_context(lines, node.lineno)
                )
                self.definitions.append(definition)
            
            elif isinstance(node, ast.FunctionDef) and any('XPUnit' in arg.annotation.id if hasattr(arg.annotation, 'id') else False for arg in node.args.args if arg.annotation):
                # Function with XPUnit type hints
                definition = XPUnitDefinition(
                    file_path=file_path,
                    line_number=node.lineno,
                    definition_type="function",
                    name=node.name,
                    content=ast.get_source_segment(content, node) or "",
                    context=self._get_context(lines, node.lineno)
                )
                self.definitions.append(definition)
    
    def _extract_text_references(self, content: str, file_path: Path, line_offset: int = 0):
        """Extract XPUnit references using text-based analysis."""
        lines = content.split('\n')
        
        for line_idx, line in enumerate(lines):
            line_number = line_idx + 1 + line_offset
            
            if 'XPUnit' in line:
                # Determine reference type
                ref_type = "usage"
                if "import" in line and "XPUnit" in line:
                    ref_type = "import"
                elif "class XPUnit" in line and not any(x in line for x in ["Definition", "Reference", "Analyzer", "Tracer", "Generator"]):
                    ref_type = "class_definition"
                elif "def" in line and "XPUnit" in line:
                    ref_type = "type_hint"
                elif "=" in line and "XPUnit(" in line:
                    ref_type = "instantiation"
                
                reference = XPUnitReference(
                    file_path=file_path,
                    line_number=line_number,
                    reference_type=ref_type,
                    context=self._get_context(lines, line_idx + 1),
                    full_line=line.strip()
                )
                self.references.append(reference)
    
    def _get_context(self, lines: List[str], line_number: int, context_size: int = 3) -> str:
        """Get surrounding context for a line."""
        start = max(0, line_number - context_size - 1)
        end = min(len(lines), line_number + context_size)
        context_lines = lines[start:end]
        return '\n'.join(context_lines)
    
    def _analyze_inconsistencies(self):
        """Analyze definitions for inconsistencies and issues."""
        if len(self.definitions) < 2:
            return
        
        # Group definitions by type
        class_definitions = [d for d in self.definitions if d.definition_type == "class"]
        
        if len(class_definitions) > 1:
            # Compare class definitions
            self._compare_class_definitions(class_definitions)
        
        # Check for missing imports
        self._check_missing_imports()
        
        # Check for inconsistent usage patterns
        self._check_usage_patterns()
    
    def _compare_class_definitions(self, definitions: List[XPUnitDefinition]):
        """Compare multiple class definitions for inconsistencies."""
        # Compare attributes
        all_attributes = set()
        attr_by_def = {}
        
        for defn in definitions:
            all_attributes.update(defn.attributes)
            attr_by_def[defn.file_path] = set(defn.attributes)
        
        # Find missing attributes
        for defn in definitions:
            missing_attrs = all_attributes - attr_by_def[defn.file_path]
            if missing_attrs:
                issue = ConsolidationIssue(
                    issue_type="missing_attributes",
                    severity="warning",
                    description=f"XPUnit in {defn.file_path.name} missing attributes: {', '.join(missing_attrs)}",
                    affected_files=[defn.file_path],
                    suggested_fix=f"Add missing attributes: {', '.join(missing_attrs)}"
                )
                self.issues.append(issue)
        
        # Compare methods
        all_methods = set()
        methods_by_def = {}
        
        for defn in definitions:
            all_methods.update(defn.methods)
            methods_by_def[defn.file_path] = set(defn.methods)
        
        # Find missing methods
        for defn in definitions:
            missing_methods = all_methods - methods_by_def[defn.file_path]
            if missing_methods:
                issue = ConsolidationIssue(
                    issue_type="missing_methods",
                    severity="warning",
                    description=f"XPUnit in {defn.file_path.name} missing methods: {', '.join(missing_methods)}",
                    affected_files=[defn.file_path],
                    suggested_fix=f"Add missing methods: {', '.join(missing_methods)}"
                )
                self.issues.append(issue)
    
    def _check_missing_imports(self):
        """Check for files using XPUnit without proper imports."""
        files_with_usage = set()
        files_with_imports = set()
        
        for ref in self.references:
            if ref.reference_type == "import":
                files_with_imports.add(ref.file_path)
            elif ref.reference_type in ["usage", "instantiation", "type_hint"]:
                files_with_usage.add(ref.file_path)
        
        missing_imports = files_with_usage - files_with_imports
        for file_path in missing_imports:
            issue = ConsolidationIssue(
                issue_type="missing_import",
                severity="critical",
                description=f"File {file_path.name} uses XPUnit but has no import statement",
                affected_files=[file_path],
                suggested_fix="Add proper XPUnit import statement"
            )
            self.issues.append(issue)
    
    def _check_usage_patterns(self):
        """Check for inconsistent usage patterns."""
        instantiation_patterns = defaultdict(list)
        
        for ref in self.references:
            if ref.reference_type == "instantiation":
                # Extract instantiation pattern
                pattern = re.sub(r'XPUnit\([^)]*\)', 'XPUnit(...)', ref.full_line)
                instantiation_patterns[pattern].append(ref)
        
        # Look for inconsistent patterns
        if len(instantiation_patterns) > 3:  # Too many different patterns
            issue = ConsolidationIssue(
                issue_type="inconsistent_usage",
                severity="info",
                description=f"Found {len(instantiation_patterns)} different XPUnit instantiation patterns",
                affected_files=[ref.file_path for refs in instantiation_patterns.values() for ref in refs],
                suggested_fix="Standardize XPUnit instantiation patterns"
            )
            self.issues.append(issue)
    
    def generate_consolidation_plan(self) -> Dict[str, Any]:
        """Generate a plan for consolidating XPUnit definitions."""
        plan = {
            "canonical_definition": self._identify_canonical_definition(),
            "migration_steps": self._generate_migration_steps(),
            "affected_files": list(set(str(d.file_path) for d in self.definitions)),
            "priority_issues": [i for i in self.issues if i.severity == "critical"],
            "recommendations": self._generate_recommendations()
        }
        return plan
    
    def _identify_canonical_definition(self) -> Optional[XPUnitDefinition]:
        """Identify the most complete XPUnit definition as canonical."""
        if not self.definitions:
            return None
        
        # Score definitions by completeness
        scored_definitions = []
        for defn in self.definitions:
            score = len(defn.attributes) + len(defn.methods) * 2
            if "xp_core_unified.py" in str(defn.file_path):
                score += 10  # Prefer unified implementation
            scored_definitions.append((score, defn))
        
        scored_definitions.sort(reverse=True)
        return scored_definitions[0][1] if scored_definitions else None
    
    def _generate_migration_steps(self) -> List[str]:
        """Generate step-by-step migration plan."""
        steps = [
            "1. Identify canonical XPUnit definition (most complete)",
            "2. Create unified XPUnit specification",
            "3. Update all definitions to match canonical version",
            "4. Fix missing imports and references",
            "5. Standardize instantiation patterns",
            "6. Run comprehensive tests",
            "7. Update documentation"
        ]
        return steps
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for XPUnit consolidation."""
        recommendations = []
        
        if len(self.definitions) > 1:
            recommendations.append("Consolidate multiple XPUnit definitions into single canonical version")
        
        critical_issues = [i for i in self.issues if i.severity == "critical"]
        if critical_issues:
            recommendations.append(f"Fix {len(critical_issues)} critical issues immediately")
        
        if any("missing_import" in i.issue_type for i in self.issues):
            recommendations.append("Add proper import statements for XPUnit usage")
        
        recommendations.append("Use GUI visualization to understand XPUnit relationships")
        recommendations.append("Implement automated tests for XPUnit consistency")
        
        return recommendations


class XPUnitConsolidatorWidget(QWidget):
    """GUI widget for XPUnit consolidation and analysis."""
    
    analysis_complete = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.analyzer = None
        self.analysis_results = None
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the consolidator UI."""
        layout = QVBoxLayout(self)
        
        # Title and controls
        title = QLabel("🧬 XPUnit Consolidation & Analysis")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Control buttons
        controls = QHBoxLayout()
        self.analyze_button = QPushButton("🔍 Analyze Repository")
        self.consolidate_button = QPushButton("🔧 Generate Consolidation Plan")
        self.export_button = QPushButton("📄 Export Analysis")
        
        self.analyze_button.clicked.connect(self.analyze_repository)
        self.consolidate_button.clicked.connect(self.generate_consolidation_plan)
        self.export_button.clicked.connect(self.export_analysis)
        
        controls.addWidget(self.analyze_button)
        controls.addWidget(self.consolidate_button)
        controls.addWidget(self.export_button)
        controls.addStretch()
        
        layout.addLayout(controls)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Results tabs
        self.results_tabs = QTabWidget()
        
        # Definitions tab
        self.definitions_tree = QTreeWidget()
        self.definitions_tree.setHeaderLabels(["File", "Type", "Name", "Attributes", "Methods"])
        self.results_tabs.addTab(self.definitions_tree, "📋 Definitions")
        
        # References tab
        self.references_tree = QTreeWidget()
        self.references_tree.setHeaderLabels(["File", "Line", "Type", "Context"])
        self.results_tabs.addTab(self.references_tree, "🔗 References")
        
        # Issues tab
        self.issues_tree = QTreeWidget()
        self.issues_tree.setHeaderLabels(["Severity", "Type", "Description", "Files"])
        self.results_tabs.addTab(self.issues_tree, "⚠️ Issues")
        
        # Consolidation plan tab
        self.plan_text = QTextEdit()
        self.plan_text.setReadOnly(True)
        self.plan_text.setFont(QFont("Consolas", 10))
        self.results_tabs.addTab(self.plan_text, "📋 Consolidation Plan")
        
        layout.addWidget(self.results_tabs)
        
        # Status label
        self.status_label = QLabel("Ready to analyze repository")
        layout.addWidget(self.status_label)
    
    def analyze_repository(self):
        """Analyze the repository for XPUnit definitions and issues."""
        try:
            # Get repository root (assuming we're in the GUI subdirectory)
            repo_root = Path(__file__).parent.parent
            
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.status_label.setText("🔍 Analyzing repository...")
            
            # Create analyzer and run analysis
            self.analyzer = XPUnitAnalyzer(repo_root)
            self.analysis_results = self.analyzer.analyze_repository()
            
            # Update UI with results
            self._populate_definitions()
            self._populate_references()
            self._populate_issues()
            
            self.progress_bar.setVisible(False)
            self.status_label.setText(
                f"✅ Analysis complete: {self.analysis_results['definitions']} definitions, "
                f"{self.analysis_results['references']} references, "
                f"{self.analysis_results['issues']} issues found"
            )
            
            self.analysis_complete.emit(self.analysis_results)
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            self.status_label.setText(f"❌ Analysis failed: {str(e)}")
            QMessageBox.critical(self, "Analysis Error", f"Failed to analyze repository:\n{str(e)}")
    
    def _populate_definitions(self):
        """Populate the definitions tree."""
        self.definitions_tree.clear()
        
        if not self.analyzer:
            return
        
        for defn in self.analyzer.definitions:
            item = QTreeWidgetItem([
                defn.file_path.name,
                defn.definition_type,
                defn.name,
                ", ".join(defn.attributes[:3]) + ("..." if len(defn.attributes) > 3 else ""),
                ", ".join(defn.methods[:3]) + ("..." if len(defn.methods) > 3 else "")
            ])
            
            # Color code by definition type
            if defn.definition_type == "class":
                item.setBackground(0, QColor(200, 255, 200))
            elif defn.definition_type == "function":
                item.setBackground(0, QColor(200, 200, 255))
            
            self.definitions_tree.addTopLevelItem(item)
    
    def _populate_references(self):
        """Populate the references tree."""
        self.references_tree.clear()
        
        if not self.analyzer:
            return
        
        for ref in self.analyzer.references:
            item = QTreeWidgetItem([
                ref.file_path.name,
                str(ref.line_number),
                ref.reference_type,
                ref.full_line[:50] + ("..." if len(ref.full_line) > 50 else "")
            ])
            
            # Color code by reference type
            if ref.reference_type == "import":
                item.setBackground(0, QColor(255, 255, 200))
            elif ref.reference_type == "instantiation":
                item.setBackground(0, QColor(255, 200, 255))
            
            self.references_tree.addTopLevelItem(item)
    
    def _populate_issues(self):
        """Populate the issues tree."""
        self.issues_tree.clear()
        
        if not self.analyzer:
            return
        
        for issue in self.analyzer.issues:
            item = QTreeWidgetItem([
                issue.severity,
                issue.issue_type,
                issue.description,
                ", ".join(f.name for f in issue.affected_files)
            ])
            
            # Color code by severity
            if issue.severity == "critical":
                item.setBackground(0, QColor(255, 200, 200))
            elif issue.severity == "warning":
                item.setBackground(0, QColor(255, 255, 200))
            else:
                item.setBackground(0, QColor(200, 200, 255))
            
            self.issues_tree.addTopLevelItem(item)
    
    def generate_consolidation_plan(self):
        """Generate and display consolidation plan."""
        if not self.analyzer:
            QMessageBox.warning(self, "No Analysis", "Please run repository analysis first.")
            return
        
        try:
            plan = self.analyzer.generate_consolidation_plan()
            
            # Format plan as text
            plan_text = "# XPUnit Consolidation Plan\n\n"
            
            if plan["canonical_definition"]:
                canonical = plan["canonical_definition"]
                plan_text += f"## Canonical Definition\n"
                plan_text += f"**File:** {canonical.file_path}\n"
                plan_text += f"**Line:** {canonical.line_number}\n"
                plan_text += f"**Attributes:** {len(canonical.attributes)}\n"
                plan_text += f"**Methods:** {len(canonical.methods)}\n\n"
            
            plan_text += "## Migration Steps\n"
            for step in plan["migration_steps"]:
                plan_text += f"- {step}\n"
            plan_text += "\n"
            
            plan_text += f"## Affected Files ({len(plan['affected_files'])})\n"
            for file_path in plan["affected_files"]:
                plan_text += f"- {file_path}\n"
            plan_text += "\n"
            
            if plan["priority_issues"]:
                plan_text += f"## Critical Issues ({len(plan['priority_issues'])})\n"
                for issue in plan["priority_issues"]:
                    plan_text += f"- **{issue.issue_type}**: {issue.description}\n"
                    plan_text += f"  *Fix:* {issue.suggested_fix}\n"
                plan_text += "\n"
            
            plan_text += "## Recommendations\n"
            for rec in plan["recommendations"]:
                plan_text += f"- {rec}\n"
            
            self.plan_text.setPlainText(plan_text)
            self.results_tabs.setCurrentWidget(self.plan_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Plan Generation Error", f"Failed to generate plan:\n{str(e)}")
    
    def export_analysis(self):
        """Export analysis results."""
        if not self.analysis_results:
            QMessageBox.warning(self, "No Analysis", "Please run repository analysis first.")
            return
        
        # For now, just show the results in a message box
        # In a full implementation, this would save to a file
        summary = (
            f"XPUnit Analysis Results:\n\n"
            f"Definitions found: {self.analysis_results['definitions']}\n"
            f"References found: {self.analysis_results['references']}\n"
            f"Issues identified: {self.analysis_results['issues']}\n"
            f"Files analyzed: {self.analysis_results['files_analyzed']}\n\n"
            f"Analysis complete! Use the consolidation plan to proceed."
        )
        
        QMessageBox.information(self, "Analysis Export", summary)


def test_xpunit_consolidator():
    """Test the XPUnit consolidator."""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    consolidator = XPUnitConsolidatorWidget()
    consolidator.setWindowTitle("🧬 XPUnit Consolidator")
    consolidator.resize(1000, 700)
    consolidator.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_xpunit_consolidator()
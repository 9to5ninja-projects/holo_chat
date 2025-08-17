# LLM Consciousness GUI

A sophisticated Python GUI application for exploring and analyzing code structure in the Lumina Memory System project, built with PySide6 and AST parsing.

## 🎯 Phase 1: Complete ✅

### Features Implemented

- **Hierarchical File Explorer**: Browse Python files in a tree structure
- **AST-Based Code Parsing**: Extract classes, functions, and methods automatically
- **Interactive Code Viewer**: Click to view specific code elements
- **Split-Panel Interface**: File explorer on left, code viewer on right
- **Real-Time Analysis**: Generate insights about code structure
- **Robust File Handling**: Support for multiple encodings and error recovery
- **Context Menus**: Right-click for additional options
- **Tabbed Code View**: Separate tabs for code and analysis

### Project Structure

```
llm_consciousness_gui/
│
├── main.py                    # Entry point
├── test_gui.py               # Test runner
├── demo_screenshot.py        # Demo script
├── README.md                 # This file
│
├── gui/                      # GUI Components
│   ├── __init__.py
│   ├── main_window.py        # Main application window
│   └── file_explorer.py      # File tree and code structure
│
├── parser/                   # Code Analysis
│   ├── __init__.py
│   └── ast_parser.py         # AST-based Python parser
│
└── utils/                    # Utilities
    └── llm_interface.py      # LLM integration (Phase 2)
```

## 🚀 Quick Start

### Prerequisites

```bash
pip install pyside6 astpretty
```

### Running the GUI

```bash
cd llm_consciousness_gui
python main.py
```

Or run the demo:

```bash
python demo_screenshot.py
```

## 🔍 How to Use

1. **Launch the Application**: Run `python main.py`
2. **Explore Files**: Expand directories in the left panel
3. **View Code Structure**: Click on Python files to see their classes and functions
4. **Analyze Code Elements**: Click on specific classes/functions to view their code
5. **Read Analysis**: Switch to the "Analysis" tab for code insights
6. **Navigate**: Use the menu bar for additional options

## 🏗️ Architecture

### Core Components

- **MainWindow**: Central application window with menu bar and status bar
- **FileExplorerWidget**: Tree view for files and code structure
- **CodeViewer**: Tabbed interface for code display and analysis
- **ASTParser**: Python AST-based code structure extraction
- **CodeElement**: Data structure representing code elements

### Key Features

- **Multi-Encoding Support**: Handles UTF-8, UTF-8-BOM, Latin-1, and CP1252
- **Error Recovery**: Gracefully handles parsing errors and encoding issues
- **Hierarchical Display**: Shows classes with their methods in tree structure
- **Line Number Tracking**: Displays exact line numbers for code elements
- **Docstring Extraction**: Shows documentation for classes and functions

## 🎨 GUI Layout

```
┌─────────────────────────────────────────────────────────────┐
│ File  View  Help                                    [Menu]  │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ │ ┌─────────────────────────────────────┐ │
│ │ File Explorer   │ │ │ Code Viewer                         │ │
│ │                 │ │ │ ┌─────────┬─────────────────────────┐ │ │
│ │ 📁 Project      │ │ │ │ Code    │ Analysis              │ │ │
│ │  📁 src         │ │ │ ├─────────┴─────────────────────────┤ │ │
│ │   📄 file.py    │ │ │ │                                 │ │ │
│ │    🏛️ Class     │ │ │ │ def example_function():         │ │ │
│ │     ⚙️ method   │ │ │ │     """This is a docstring"""   │ │ │
│ │    ⚙️ function  │ │ │ │     return "Hello World"        │ │ │
│ │                 │ │ │ │                                 │ │ │
│ └─────────────────┘ │ └─────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Status: Viewing example_function - Line 42                  │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Technical Details

### AST Parser Features

- Extracts top-level classes and functions
- Identifies methods within classes
- Handles both regular and async functions
- Extracts docstrings automatically
- Tracks line numbers for precise navigation

### Error Handling

- Multiple encoding detection and fallback
- Graceful handling of syntax errors
- BOM (Byte Order Mark) removal
- Null byte detection and handling

### GUI Components

- **QTreeWidget**: For hierarchical file/code display
- **QSplitter**: For resizable panels
- **QTabWidget**: For code/analysis views
- **QPlainTextEdit**: For code display
- **QTextEdit**: For rich text analysis

## 🚀 Phase 2: Next Steps

The foundation is now ready for LLM integration:

1. **Ollama Integration**: Connect to local LLM for code analysis
2. **Consciousness Simulation**: Analyze code patterns for consciousness indicators
3. **Interactive Chat**: Ask questions about the codebase
4. **Code Suggestions**: Get AI-powered code improvements
5. **Pattern Recognition**: Identify consciousness-like patterns in code structure

## 🐛 Known Issues

- Some files with encoding issues may show parse errors (handled gracefully)
- Files with null bytes cannot be parsed (displayed as errors)
- Very large files may take time to parse (future optimization needed)

## 📝 Development Notes

### Code Quality

- Type hints throughout the codebase
- Comprehensive error handling
- Modular architecture for easy extension
- Clean separation of concerns

### Performance

- Lazy loading of file contents
- Efficient AST parsing
- Minimal memory footprint
- Responsive UI with proper threading (ready for Phase 2)

## 🎉 Success Metrics

✅ **GUI Framework**: PySide6 successfully integrated  
✅ **File Parsing**: AST-based Python code analysis working  
✅ **Tree View**: Hierarchical display of code structure  
✅ **Code Display**: Interactive code viewing and navigation  
✅ **Error Handling**: Robust handling of encoding and parsing issues  
✅ **User Experience**: Intuitive interface with context menus and shortcuts  

**Phase 1 Complete!** Ready for LLM integration in Phase 2.
#!/usr/bin/env python3
"""
Live Memory Tracker for LLM Consciousness GUI

This module provides live variable and memory tracking during code execution
using sys.settrace() and other debugging techniques.
"""

import sys
import threading
import time
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import traceback
import inspect
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VariableState:
    """Represents the state of a variable at a point in time."""
    name: str
    value: Any
    type_name: str
    size: int
    timestamp: datetime
    frame_info: str
    line_number: int


@dataclass
class ExecutionFrame:
    """Represents an execution frame with variable states."""
    function_name: str
    filename: str
    line_number: int
    variables: Dict[str, VariableState]
    timestamp: datetime
    event_type: str  # 'call', 'line', 'return', 'exception'


class LiveMemoryTracker:
    """Tracks live variable states and execution flow."""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.execution_history: List[ExecutionFrame] = []
        self.current_variables: Dict[str, VariableState] = {}
        self.is_tracing = False
        self.trace_filter = None  # Optional filter function
        self.callbacks: List[Callable] = []
        self.lock = threading.Lock()
    
    def add_callback(self, callback: Callable):
        """Add a callback function to be called when variables change."""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback: Callable):
        """Remove a callback function."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _notify_callbacks(self, frame: ExecutionFrame):
        """Notify all callbacks of a new execution frame."""
        for callback in self.callbacks:
            try:
                callback(frame)
            except Exception as e:
                print(f"Error in callback: {e}")
    
    def _get_variable_info(self, name: str, value: Any, frame_info: str, line_number: int) -> VariableState:
        """Create a VariableState object from a variable."""
        try:
            type_name = type(value).__name__
            
            # Calculate size (approximate)
            try:
                if hasattr(value, '__sizeof__'):
                    size = value.__sizeof__()
                elif isinstance(value, (str, bytes)):
                    size = len(value)
                elif isinstance(value, (list, tuple, dict, set)):
                    size = len(value)
                else:
                    size = sys.getsizeof(value)
            except:
                size = 0
            
            return VariableState(
                name=name,
                value=value,
                type_name=type_name,
                size=size,
                timestamp=datetime.now(),
                frame_info=frame_info,
                line_number=line_number
            )
        except Exception as e:
            # Fallback for problematic values
            return VariableState(
                name=name,
                value=f"<Error: {str(e)}>",
                type_name="error",
                size=0,
                timestamp=datetime.now(),
                frame_info=frame_info,
                line_number=line_number
            )
    
    def _trace_function(self, frame, event, arg):
        """The main trace function called by sys.settrace()."""
        try:
            # Apply filter if set
            if self.trace_filter and not self.trace_filter(frame, event, arg):
                return self._trace_function
            
            filename = frame.f_code.co_filename
            function_name = frame.f_code.co_name
            line_number = frame.f_lineno
            
            # Skip internal Python files
            if filename.startswith('<') or 'site-packages' in filename:
                return self._trace_function
            
            # Create frame info
            frame_info = f"{function_name}@{Path(filename).name}:{line_number}"
            
            # Extract variables from frame
            variables = {}
            local_vars = frame.f_locals.copy()
            
            for var_name, var_value in local_vars.items():
                # Skip private variables and modules
                if var_name.startswith('_') or inspect.ismodule(var_value):
                    continue
                
                # Skip functions and classes (unless they're small)
                if inspect.isfunction(var_value) or inspect.isclass(var_value):
                    continue
                
                try:
                    var_state = self._get_variable_info(var_name, var_value, frame_info, line_number)
                    variables[var_name] = var_state
                except Exception as e:
                    # Skip problematic variables
                    continue
            
            # Create execution frame
            exec_frame = ExecutionFrame(
                function_name=function_name,
                filename=filename,
                line_number=line_number,
                variables=variables,
                timestamp=datetime.now(),
                event_type=event
            )
            
            # Thread-safe update
            with self.lock:
                self.execution_history.append(exec_frame)
                
                # Maintain history limit
                if len(self.execution_history) > self.max_history:
                    self.execution_history = self.execution_history[-self.max_history:]
                
                # Update current variables
                self.current_variables.update(variables)
            
            # Notify callbacks
            self._notify_callbacks(exec_frame)
            
        except Exception as e:
            # Don't let tracing errors break the program
            pass
        
        return self._trace_function
    
    def start_tracing(self, filter_func: Optional[Callable] = None):
        """Start live memory tracking."""
        if self.is_tracing:
            return
        
        self.trace_filter = filter_func
        self.is_tracing = True
        
        # Clear previous data
        with self.lock:
            self.execution_history.clear()
            self.current_variables.clear()
        
        # Set the trace function
        sys.settrace(self._trace_function)
        
        print("🔍 Live memory tracking started")
    
    def stop_tracing(self):
        """Stop live memory tracking."""
        if not self.is_tracing:
            return
        
        sys.settrace(None)
        self.is_tracing = False
        
        print("🛑 Live memory tracking stopped")
    
    def get_current_variables(self) -> Dict[str, VariableState]:
        """Get the current state of all tracked variables."""
        with self.lock:
            return self.current_variables.copy()
    
    def get_execution_history(self, limit: Optional[int] = None) -> List[ExecutionFrame]:
        """Get the execution history."""
        with self.lock:
            history = self.execution_history.copy()
            if limit:
                return history[-limit:]
            return history
    
    def get_variable_history(self, var_name: str) -> List[VariableState]:
        """Get the history of a specific variable."""
        history = []
        with self.lock:
            for frame in self.execution_history:
                if var_name in frame.variables:
                    history.append(frame.variables[var_name])
        return history
    
    def clear_history(self):
        """Clear all tracking history."""
        with self.lock:
            self.execution_history.clear()
            self.current_variables.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tracking statistics."""
        with self.lock:
            total_frames = len(self.execution_history)
            total_variables = len(self.current_variables)
            
            # Calculate memory usage
            total_memory = sum(var.size for var in self.current_variables.values())
            
            # Get function call counts
            function_calls = {}
            for frame in self.execution_history:
                if frame.event_type == 'call':
                    func_name = frame.function_name
                    function_calls[func_name] = function_calls.get(func_name, 0) + 1
            
            return {
                "total_frames": total_frames,
                "total_variables": total_variables,
                "total_memory_bytes": total_memory,
                "function_calls": function_calls,
                "is_tracing": self.is_tracing
            }


class CodeExecutor:
    """Executes Python code with live memory tracking."""
    
    def __init__(self, memory_tracker: LiveMemoryTracker):
        self.memory_tracker = memory_tracker
        self.execution_globals = {}
        self.execution_locals = {}
    
    def execute_code(self, code: str, filename: str = "<string>") -> Dict[str, Any]:
        """Execute Python code with memory tracking."""
        result = {
            "success": False,
            "output": "",
            "error": None,
            "execution_time": 0
        }
        
        try:
            # Prepare execution environment
            self.execution_globals = {"__name__": "__main__"}
            self.execution_locals = {}
            
            # Start tracking
            start_time = time.time()
            self.memory_tracker.start_tracing()
            
            # Execute code
            exec(compile(code, filename, 'exec'), self.execution_globals, self.execution_locals)
            
            # Stop tracking
            self.memory_tracker.stop_tracing()
            end_time = time.time()
            
            result["success"] = True
            result["execution_time"] = end_time - start_time
            result["output"] = "Code executed successfully"
            
        except Exception as e:
            self.memory_tracker.stop_tracing()
            result["error"] = str(e)
            result["output"] = traceback.format_exc()
        
        return result
    
    def execute_file(self, file_path: Path) -> Dict[str, Any]:
        """Execute a Python file with memory tracking."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            return self.execute_code(code, str(file_path))
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": f"Failed to read file: {str(e)}",
                "execution_time": 0
            }


def test_memory_tracker():
    """Test the memory tracker with sample code."""
    print("🧠 Testing Live Memory Tracker")
    print("=" * 50)
    
    # Create tracker
    tracker = LiveMemoryTracker(max_history=100)
    
    # Add callback to print variable changes
    def print_variables(frame: ExecutionFrame):
        if frame.event_type == 'line' and frame.variables:
            print(f"📍 {frame.function_name}:{frame.line_number} - Variables: {list(frame.variables.keys())}")
    
    tracker.add_callback(print_variables)
    
    # Test code execution
    executor = CodeExecutor(tracker)
    
    test_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b

result = fibonacci(10)
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
'''
    
    print("🚀 Executing test code...")
    result = executor.execute_code(test_code)
    
    print(f"✅ Execution result: {result}")
    
    # Get statistics
    stats = tracker.get_stats()
    print(f"📊 Tracking stats: {stats}")
    
    # Get current variables
    variables = tracker.get_current_variables()
    print(f"🔍 Current variables: {list(variables.keys())}")
    
    return tracker


if __name__ == "__main__":
    test_memory_tracker()
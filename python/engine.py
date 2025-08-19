#!/usr/bin/env python3
"""
Python Engine for Holographic Memory System
===========================================

This engine provides RPC interface for the memory system.
Can be used by various frontends (CLI, GUI, etc.)
"""

import json
import sys
import traceback
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def handle_rpc(request):
    """Handle RPC requests for memory system operations"""
    try:
        method = request.get('method')
        params = request.get('params', {})
        request_id = request.get('id')
        
        # Initialize memory adapter if needed
        if not hasattr(handle_rpc, 'memory_adapter'):
            from python.memory_adapter import MemoryAdapter
            handle_rpc.memory_adapter = MemoryAdapter()
        
        memory_adapter = handle_rpc.memory_adapter
        
        # Handle different RPC methods
        if method == 'get_annotations':
            # Get holographic annotations
            directory = params.get('directory', '.')
            annotations = memory_adapter.get_annotations(directory)
            result = {"ok": True, "annotations": annotations}
        
        elif method == 'chat_start_session':
            # Start chat session
            if hasattr(memory_adapter, 'chat_assistant'):
                session_id = memory_adapter.chat_assistant.start_session(params.get("user_name", "User"))
                result = {"ok": True, "session_id": session_id}
            else:
                # Initialize chat assistant if not exists
                try:
                    from src.lumina_memory.chat_assistant import ChatAssistant
                    memory_adapter.chat_assistant = ChatAssistant("e:/holo_chat/policies.yml")
                    session_id = memory_adapter.chat_assistant.start_session(params.get("user_name", "User"))
                    result = {"ok": True, "session_id": session_id}
                except Exception as e:
                    result = {"ok": False, "error": f"Failed to initialize chat assistant: {e}"}
        
        elif method == 'chat_message':
            # Process chat message
            if hasattr(memory_adapter, 'chat_assistant'):
                result = memory_adapter.chat_assistant.chat(
                    params.get("message", ""),
                    model=params.get("model", "internal")
                )
            else:
                result = {"ok": False, "error": "Chat assistant not initialized"}
        
        elif method == 'chat_end_session':
            # End chat session
            if hasattr(memory_adapter, 'chat_assistant'):
                summary = memory_adapter.chat_assistant.end_session()
                result = {"ok": True, "summary": summary}
            else:
                result = {"ok": False, "error": "Chat assistant not initialized"}
        
        elif method == 'chat_get_mood':
            # Get current mood
            if hasattr(memory_adapter, 'chat_assistant'):
                mood_summary = memory_adapter.chat_assistant.get_mood_summary()
                current_mood = memory_adapter.chat_assistant.current_session.current_mood if memory_adapter.chat_assistant.current_session else None
                result = {"ok": True, "summary": mood_summary, "mood": current_mood}
            else:
                result = {"ok": False, "error": "Chat assistant not initialized"}
        
        elif method == 'chat_get_insights':
            # Get learning insights
            if hasattr(memory_adapter, 'chat_assistant'):
                insights = memory_adapter.chat_assistant.get_learning_insights()
                result = {"ok": True, **insights}
            else:
                result = {"ok": False, "error": "Chat assistant not initialized"}
        
        elif method == 'agency_compute_index':
            # Compute Agency Index
            if hasattr(memory_adapter, 'chat_assistant') and hasattr(memory_adapter.chat_assistant, 'env'):
                weights = params.get('weights', None)
                agency_result = memory_adapter.chat_assistant.env.compute_agency_index(weights)
                result = {"ok": True, **agency_result}
            else:
                result = {"ok": False, "error": "Chat assistant or environment not initialized"}
        
        elif method == 'agency_reset_metrics':
            # Reset Agency metrics
            if hasattr(memory_adapter, 'chat_assistant') and hasattr(memory_adapter.chat_assistant, 'env'):
                memory_adapter.chat_assistant.env.reset_agency_metrics()
                result = {"ok": True, "message": "Agency metrics reset"}
            else:
                result = {"ok": False, "error": "Chat assistant or environment not initialized"}
        
        elif method == 'agency_run_task':
            # Run an Agency task from YAML-style data
            if hasattr(memory_adapter, 'chat_assistant') and hasattr(memory_adapter.chat_assistant, 'env'):
                try:
                    task_data = params.get('task_data', {})
                    env = memory_adapter.chat_assistant.env
                    
                    # Load task
                    task = env.load_agency_task(task_data)
                    
                    # Reset metrics for clean test
                    env.reset_agency_metrics()
                    
                    # Simulate task execution (simplified)
                    goal = task.goal
                    
                    # Run a chat interaction with the goal
                    chat_result = memory_adapter.chat_assistant.chat(goal, model=params.get("model", "internal"))
                    
                    # Apply any intrusions if specified
                    if task.intrusions.get("inject_after_step"):
                        # Simulate intrusion
                        intrusion_text = "Random distraction: What's the weather like?"
                        affect_delta = task.intrusions.get("affect_delta", {})
                        env.track_intrusion_event(is_intrusion=True)
                        
                        # Try to return to goal
                        return_result = memory_adapter.chat_assistant.chat(f"Returning to: {goal}", model=params.get("model", "internal"))
                        env.track_intrusion_event(is_intrusion=False, returned_within_steps=True)
                    
                    # Compute final Agency Index
                    weights = task.metrics_weights if task.metrics_weights else None
                    agency_result = env.compute_agency_index(weights)
                    
                    result = {
                        "ok": True,
                        "task_id": task.task_id,
                        "goal": task.goal,
                        **agency_result
                    }
                except Exception as e:
                    result = {"ok": False, "error": f"Task execution failed: {e}"}
            else:
                result = {"ok": False, "error": "Chat assistant or environment not initialized"}
        
        else:
            raise ValueError(f"Unknown method: {method}")
            
        return {'id': request_id, 'result': result}
    except Exception as e:
        traceback.print_exc()
        return {'id': request_id, 'error': str(e)}

def main():
    """Main entry point for the Python bridge"""
    # Set UTF-8 encoding for Windows compatibility
    import sys
    import io
    
    # Wrap stdout/stderr to handle Unicode properly
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            request = json.loads(line)
            response = handle_rpc(request)
            
            # Send the response
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError as e:
            print(json.dumps({
                'error': f'JSON decode error: {e}',
                'id': None
            }), flush=True)
        except Exception as e:
            print(json.dumps({
                'error': f'Unexpected error: {e}',
                'id': None
            }), flush=True)
            traceback.print_exc()

if __name__ == "__main__":
    main()
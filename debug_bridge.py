#!/usr/bin/env python3
"""
Debug Python Bridge
===================

Debug what the Python bridge is actually outputting.
"""

import json
import subprocess
import sys
from pathlib import Path

def debug_bridge():
    """Debug the Python bridge output"""
    print("🔍 Debugging Python Bridge...")
    
    # Start the bridge process
    bridge_path = Path("python/engine.py")
    
    try:
        process = subprocess.Popen(
            [sys.executable, str(bridge_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path.cwd()
        )
        
        print("✅ Bridge process started")
        
        # Send a simple request
        request = {
            "id": 1,
            "method": "chat_start_session",
            "params": {"user_name": "TestUser"}
        }
        
        print(f"📤 Sending: {json.dumps(request)}")
        
        process.stdin.write(json.dumps(request) + "\n")
        process.stdin.flush()
        
        # Read stdout and stderr
        import select
        import time
        
        # Wait a bit for response
        time.sleep(2)
        
        # Check if there's any output
        stdout_data = ""
        stderr_data = ""
        
        # Try to read stdout
        try:
            stdout_data = process.stdout.read(1024)
            print(f"📥 STDOUT: '{stdout_data}'")
        except:
            print("📥 STDOUT: No data")
        
        # Try to read stderr
        try:
            stderr_data = process.stderr.read(1024)
            print(f"📥 STDERR: '{stderr_data}'")
        except:
            print("📥 STDERR: No data")
        
        # Check process status
        poll_result = process.poll()
        print(f"📊 Process status: {poll_result}")
        
        # Terminate process
        process.terminate()
        process.wait(timeout=5)
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_bridge()
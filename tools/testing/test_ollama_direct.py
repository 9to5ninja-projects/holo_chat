#!/usr/bin/env python3
"""
Direct Ollama Test - Check why it's slow
"""

import time
import json
import urllib.request as _ur

def test_ollama_direct():
    """Test Ollama directly to see where the delay is"""
    
    print("🔍 TESTING OLLAMA DIRECTLY")
    print("=" * 40)
    
    # Test 1: Check if Ollama is responding
    print("1. Testing Ollama connection...")
    start_time = time.time()
    try:
        req = _ur.Request("http://localhost:11434/api/tags")
        with _ur.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            models = [model['name'] for model in data.get('models', [])]
            connection_time = time.time() - start_time
            print(f"   ✅ Connected in {connection_time:.3f}s")
            print(f"   📋 Models: {models}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return
    
    # Test 2: Simple generation test
    print("\n2. Testing simple generation...")
    start_time = time.time()
    try:
        req = _ur.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps({
                "model": "mistral:7b-instruct", 
                "prompt": "Hello, how are you?", 
                "stream": False
            }).encode(),
            headers={"Content-Type": "application/json"}
        )
        
        with _ur.urlopen(req, timeout=30) as response:
            data = json.loads(response.read())
            generation_time = time.time() - start_time
            response_text = data.get("response", "")
            
            print(f"   ✅ Generated in {generation_time:.3f}s")
            print(f"   📝 Response: {response_text[:100]}...")
            
    except Exception as e:
        print(f"   ❌ Generation failed: {e}")
        return
    
    # Test 3: Streaming test (what our system uses)
    print("\n3. Testing streaming generation...")
    start_time = time.time()
    try:
        req = _ur.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps({
                "model": "mistral:7b-instruct", 
                "prompt": "Hello, how are you?", 
                "stream": True
            }).encode(),
            headers={"Content-Type": "application/json"}
        )
        
        output = ""
        with _ur.urlopen(req, timeout=30) as response:
            for line in response:
                try:
                    data = json.loads(line)
                    output += data.get("response", "")
                    if data.get("done"):
                        break
                except json.JSONDecodeError:
                    continue
        
        streaming_time = time.time() - start_time
        print(f"   ✅ Streamed in {streaming_time:.3f}s")
        print(f"   📝 Response: {output[:100]}...")
        
    except Exception as e:
        print(f"   ❌ Streaming failed: {e}")
        return
    
    print(f"\n🎯 PERFORMANCE SUMMARY")
    print(f"   Connection: {connection_time:.3f}s")
    print(f"   Simple Gen: {generation_time:.3f}s") 
    print(f"   Streaming:  {streaming_time:.3f}s")

if __name__ == "__main__":
    test_ollama_direct()
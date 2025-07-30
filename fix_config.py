#!/usr/bin/env python3
"""
Configuration Fix Script for LLM Bridge
This script helps fix the model mapping and configuration issues.
"""

import os
import subprocess
import json
import requests

def check_ollama_models():
    """Check what models are available in Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            return models
        else:
            return []
    except:
        return []

def create_env_file():
    """Create a .env file with proper configuration"""
    env_content = """# LLM Bridge for Claude Code Configuration

# API Keys (set at least one)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=

# Preferred Provider (ollama, openai, anthropic, google)
PREFERRED_PROVIDER=ollama

# Model Configuration
# For Ollama, use model names like: codellama:13b, llama3:8b, mistral:7b
BIG_MODEL=codellama:13b
SMALL_MODEL=codellama:7b

# Ollama Configuration
OLLAMA_API_BASE=http://localhost:11434

# Server Configuration
HOST=0.0.0.0
PORT=8083

# Logging Configuration
LOG_LEVEL=INFO
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Created .env file")

def main():
    print("🔧 LLM Bridge Configuration Fix")
    print("=" * 40)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ No .env file found")
        create_env_file()
    else:
        print("✅ .env file exists")
    
    # Check Ollama models
    print("\n🔍 Checking Ollama models...")
    models = check_ollama_models()
    
    if models:
        print("✅ Found Ollama models:")
        for model in models:
            print(f"  - {model}")
        
        # Suggest configuration
        print("\n💡 Suggested configuration:")
        if any('codellama' in model for model in models):
            print("  BIG_MODEL=codellama:13b")
            print("  SMALL_MODEL=codellama:7b")
        elif any('llama' in model for model in models):
            print("  BIG_MODEL=llama3:8b")
            print("  SMALL_MODEL=llama3:3b")
        elif any('mistral' in model for model in models):
            print("  BIG_MODEL=mistral:7b")
            print("  SMALL_MODEL=mistral:3b")
        else:
            print("  Use any of the available models above")
    else:
        print("❌ No Ollama models found or Ollama not running")
        print("\n💡 To install models, run:")
        print("  ollama pull codellama:13b")
        print("  ollama pull codellama:7b")
    
    print("\n🎯 Next steps:")
    print("1. Edit .env file with your preferred models")
    print("2. Start Ollama: ollama serve")
    print("3. Start the proxy: uvicorn server:app --host 0.0.0.0 --port 8083")
    print("4. Test with: ./claudebr")

if __name__ == "__main__":
    main() 
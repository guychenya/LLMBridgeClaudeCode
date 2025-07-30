#!/usr/bin/env python3
"""
Configuration setup script for LLM Bridge for Claude Code.
This script helps users set up their .env file with the necessary configuration.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create a .env file from the example configuration"""
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping creation.")
        return
    
    # Check if config.env.example exists
    if os.path.exists('config.env.example'):
        source_file = 'config.env.example'
    else:
        print("❌ No configuration template found. Creating basic .env file...")
        create_basic_env()
        return
    
    # Copy the example file to .env
    try:
        with open(source_file, 'r') as src:
            content = src.read()
        
        with open('.env', 'w') as dst:
            dst.write(content)
        
        print(f"✅ Created .env file from {source_file}")
        print("📝 Please edit .env file with your actual API keys and preferences")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        create_basic_env()

def create_basic_env():
    """Create a basic .env file with default values"""
    basic_config = """# LLM Bridge for Claude Code Configuration
# Update these values with your actual API keys and preferences

# API Keys (set at least one)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Preferred Provider (openai, anthropic, google, ollama)
PREFERRED_PROVIDER=openai

# Model Configuration
BIG_MODEL=gpt-4o
SMALL_MODEL=gpt-3.5-turbo

# Ollama Configuration
OLLAMA_API_BASE=http://localhost:11434

# Server Configuration
HOST=0.0.0.0
PORT=8083

# Logging
LOG_LEVEL=INFO
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(basic_config)
        print("✅ Created basic .env file")
        print("📝 Please edit .env file with your actual API keys and preferences")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def validate_config():
    """Validate the current configuration"""
    try:
        from app.config.settings import validate_configuration
        
        issues = validate_configuration()
        if issues:
            print("❌ Configuration issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("✅ Configuration validation passed")
            return True
    except ImportError as e:
        print(f"❌ Error importing configuration: {e}")
        return False
    except Exception as e:
        print(f"❌ Error validating configuration: {e}")
        return False

def main():
    print("🔧 LLM Bridge for Claude Code - Configuration Setup")
    print("=" * 50)
    
    # Create .env file if it doesn't exist
    create_env_file()
    
    print("\n🔍 Validating configuration...")
    validate_config()
    
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your API keys and preferences")
    print("2. Run the installation script: ./install.sh")
    print("3. Start using the bridge with: ./claudebr")

if __name__ == "__main__":
    main() 
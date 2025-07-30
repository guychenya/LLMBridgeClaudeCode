#!/usr/bin/env python3
import sys
import subprocess
import os

def main():
    print("Welcome to CLED (Claude LLM Environment Dispatcher) CLI!")
    print("Available commands:")
    print("  install   - Launch the visual installer")
    print("  serve     - Start the LLMBridgeClaudeCode server")
    print("  ollama    - Check Ollama status")
    print("  help      - Show this help message")
    if len(sys.argv) < 2:
        return
    cmd = sys.argv[1]
    if cmd == "install":
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "cled_installer.py")])
    elif cmd == "serve":
        subprocess.run(["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8083"])
    elif cmd == "ollama":
        subprocess.run(["ollama", "list"])
    elif cmd == "help":
        pass
    else:
        print("Unknown command. Use 'cled help'.")

if __name__ == "__main__":
    main()
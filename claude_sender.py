import requests
import sys
import json
import re
import os

# Function to get available Ollama models
def get_ollama_models():
    try:
        ollama_api_base = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
        response = requests.get(f"{ollama_api_base}/api/tags")
        response.raise_for_status()
        models_data = response.json()
        return [model["name"] for model in models_data.get("models", [])]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Ollama models: {e}", file=sys.stderr)
        return []

def main():
    messages = []
    available_models = get_ollama_models()
    current_model = "ollama/phi3:mini" # Default model

    if not available_models:
        print("Warning: No Ollama models found. Please ensure Ollama server is running and models are downloaded.", file=sys.stderr)
        print("Using default model: ollama/phi3:mini (may not work)", file=sys.stderr)
    elif current_model not in available_models:
        print(f"Default model '{current_model}' not found. Using first available model.", file=sys.stderr)
        current_model = available_models[0]

    print(f"Starting chat with Ollama via ollamachat. Current model: {current_model}")
    print("Type 'exit' or 'quit' to end the session. Type '/' or '/menu' to change model.")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Ending chat session. Goodbye!")
                break
            
            if user_input.lower() == '/' or user_input.lower() == '/menu':
                print("\n--- Ollama Model Selection ---")
                if not available_models:
                    print("No models available. Please check your Ollama server.")
                else:
                    for i, model_name in enumerate(available_models):
                        print(f"{i+1}. {model_name}")
                    print("------------------------------")
                    while True:
                        try:
                            choice = input(f"Enter number to select model (current: {current_model}): ")
                            if choice.isdigit() and 1 <= int(choice) <= len(available_models):
                                current_model = available_models[int(choice)-1]
                                print(f"Model changed to: {current_model}")
                                break
                            else:
                                print("Invalid choice. Please enter a number from the list.")
                        except EOFError:
                            print("\nExiting model selection.")
                            break
                continue # Skip to next user input after menu interaction

            messages.append({"role": "user", "content": user_input})

            data = {
                "model": current_model,
                "max_tokens": 1024,
                "messages": messages,
                "stream": True
            }

            print("Assistant: ", end='', flush=True)
            response = requests.post(
                "http://localhost:8083/v1/messages",
                headers={"Content-Type": "application/json"},
                json=data,
                stream=True
            )
            response.raise_for_status()

            assistant_response_content = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    print(f"DEBUG: Raw received line: {decoded_line}", file=sys.stderr) # New debug print

                    if not decoded_line.startswith("data:"):
                        print(f"DEBUG: Skipping non-data line: {decoded_line}", file=sys.stderr) # New debug print
                        continue

                    event_data = decoded_line[len("data: "):].strip()
                    print(f"DEBUG: Parsed event data: {event_data}", file=sys.stderr) # New debug print

                    if event_data == "[DONE]":
                        print("DEBUG: Received [DONE] signal.", file=sys.stderr) # New debug print
                        break
                    
                    try:
                        event_json = json.loads(event_data)
                        event_type = event_json.get("type")
                        print(f"DEBUG: Parsed event type: {event_type}", file=sys.stderr) # New debug print

                        if event_type == "content_block_delta":
                            delta = event_json.get("delta", {})
                            if delta.get("type") == "text_delta":
                                text = delta.get("text", "")
                                print(f"DEBUG: Extracted text delta: '{text}'", file=sys.stderr) # New debug print
                                print(text, end='', flush=True)
                                assistant_response_content += text
                            else:
                                print(f"DEBUG: Unhandled delta type within content_block_delta: {delta.get("type")}", file=sys.stderr) # New debug print
                        elif event_type == "message_stop":
                            print("DEBUG: Received message_stop event.", file=sys.stderr) # New debug print
                            break
                        else:
                            print(f"DEBUG: Ignoring event type: {event_type}", file=sys.stderr) # New debug print

                    except json.JSONDecodeError as e:
                        print(f"DEBUG: JSONDecodeError: {e} - Line: {decoded_line}", file=sys.stderr) # New debug print
                        pass
            
            messages.append({"role": "assistant", "content": assistant_response_content.strip()})

        except requests.exceptions.RequestException as e:
            print(f"\nError communicating with the server: {e}")
            # Optionally, break or continue based on desired error handling
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    main()
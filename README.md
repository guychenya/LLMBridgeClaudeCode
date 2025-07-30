# LLM Bridge for Claude Code: Your Gateway to Free & Open-Source LLMs (via Ollama) ✨

**This project extends the original [claude-code-proxy](https://github.com/1rgs/claude-code-proxy) to seamlessly integrate with 100% free and open-source LLMs via Ollama.**

**Run Anthropic clients (like Claude Code) with your favorite local LLMs, powered by Ollama!** This proxy provides a seamless bridge to 100% free and open-source models, right from your machine. 🔗

![Ollama API Proxy](ollama_proxy.png)

## Why Try LLM Bridge for Claude Code? 💡

This project offers several compelling advantages:

-   **100% Free & Open-Source LLMs**: Leverage powerful language models without API costs or reliance on external services. Your data stays local!
-   **Enhanced Privacy**: Since models run on your machine, your interactions remain private and secure.
-   **Cost-Effective Development**: Experiment and build with LLMs without incurring API usage fees.
-   **Seamless Claude Code Integration**: Continue using the familiar Claude Code CLI, now powered by your local models.
-   **Easy Setup**: The `install.sh` script makes getting started incredibly simple, even for those new to local LLMs.
-   **Flexibility**: While optimized for Ollama, it still supports OpenAI and Google Gemini for broader compatibility.

## How It Works ⚙️

This proxy acts as a clever translator:

1.  **Receives** Anthropic API requests from your Claude client. ⬇️
2.  **Translates** them into a format LiteLLM understands (which then talks to Ollama). ↔️
3.  **Sends** the request to your local Ollama server. ⬆️
4.  **Converts** Ollama's response back to Anthropic format. ↔️
5.  **Returns** the magic to your Claude client! 🎉

It handles both streaming and non-streaming responses, keeping your Claude experience smooth. 💧

![Ollama Proxy Bottom](ollama_proxy_bottom.png)

## Installation & Usage 🚀

Getting started is a breeze with our interactive `install.sh` script! It handles everything from setting up your environment to configuring your preferred LLM provider.

**Prerequisite**: This project assumes you have the [Ollama server](https://ollama.com/download) already installed and running on your machine. If not, please download and install it first:
-   **macOS**: [Download Ollama for macOS](https://ollama.com/download/mac)
-   **Windows**: [Download Ollama for Windows](https://ollama.com/download/windows)
-   **Linux**: Follow the instructions on the [Ollama website](https://ollama.com/download/linux)

### Quick Start

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/guychenya/LLMBridgeClaudeCode.git
    cd LLMBridgeClaudeCode
    ```

2.  **Run the installer script**:
    ```bash
    bash install.sh
    ```

    The script will guide you through the setup process, including selecting a model based on your primary task (coding, chat, or multimodal).

    <details>
    <summary>Click to see installer output example</summary>

    ```text
    [INFO] Starting LLM Bridge for Claude Code Installer...
    [INFO] Checking for required tools: git, uv, npm, ollama...
    [INFO] Configuring environment variables in .env...
    ?[CHOICE] Choose your preferred LLM provider [ollama]: 
      1) ollama
      2) openai
      3) google
    #? 1
    [INFO] Set PREFERRED_PROVIDER to ollama in .env.
    [INFO] Ollama selected. No API keys needed for Ollama models.
    ?[CHOICE] Choose your primary task [coding]: 
      1) coding
      2) chat
      3) multimodal
    #? 1
    ?[CHOICE] Choose a coding model to download [codellama:13b]:
      1) codellama:13b
      2) deepseek-coder:33b-instruct
      3) starcoder2:15b
    #? 1
    [INFO] Model 'codellama:13b' not found locally. Attempting to pull...
    [SUCCESS] Successfully pulled Ollama model 'codellama:13b'.
    [INFO] Set both BIG_MODEL and SMALL_MODEL to 'codellama:13b' in .env.
    [INFO] Installing Python dependencies using uv...
    [SUCCESS] Python dependencies installed.
    [INFO] Installing Claude Code CLI globally using npm...
    [SUCCESS] Claude Code CLI installed.
    [INFO] Starting the proxy server in the background...
    [SUCCESS] Proxy server started in the background with PID: 12345. Output logged to proxy_server.log
    [INFO] To stop the server, run: kill 12345
    [SUCCESS] Installation complete!
    [INFO] Creating 'claudebr' command for easy access...
    [SUCCESS] 'claudebr' command installed successfully.

    --- Next Steps ---
    1. Run Claude Code CLI using the new 'claudebr' command:
       claudebr

    Enjoy using Claude Code with your chosen LLM backend!
    ```
    </details>

### What the Installer Does ✨

Our `install.sh` script isn't just a simple setup; it's packed with features to make your life easier:

-   **Guided Model Selection**: Helps you choose and download the best model for your task (coding, chat, or multimodal).
-   **Interactive Provider Choice**: Guides you through selecting Ollama, OpenAI, or Gemini as your primary LLM provider.
-   **Disk Space Guardian**: Before downloading large Ollama models, it checks for sufficient disk space and warns you if space is low.
-   **Automatic Server Launch**: Automatically starts the proxy server in the background after a successful installation.
-   **`claudebr` Command**: Creates a convenient `claudebr` command to run the Claude Code CLI with the local proxy.
-   **Robust Error Handling**: Provides informative messages for common issues.

## Usage Guide 📖

### Basic Usage

After installation, you can start using the LLM Bridge immediately:

```bash
claudebr
```

This command launches the Claude Code CLI connected to your local LLM proxy. You can now use all Claude Code features with your chosen local model!

### Advanced Usage

#### 1. Starting the Proxy Server Manually

If you need to start the proxy server manually:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Start the server
uvicorn server:app --host 0.0.0.0 --port 8083
```

#### 2. Using Different Models

You can change models by editing your `.env` file:

```bash
# For coding tasks
BIG_MODEL=codellama:13b
SMALL_MODEL=codellama:7b

# For general chat
BIG_MODEL=llama3.2:70b
SMALL_MODEL=llama3.2:3b

# For multimodal tasks
BIG_MODEL=llava:13b
SMALL_MODEL=llava:7b
```

#### 3. Switching Between Providers

Change your preferred provider in the `.env` file:

```bash
# For OpenAI
PREFERRED_PROVIDER=openai
OPENAI_API_KEY=your_openai_key

# For Google Gemini
PREFERRED_PROVIDER=google
GEMINI_API_KEY=your_gemini_key

# For Ollama (local models)
PREFERRED_PROVIDER=ollama
```

#### 4. Using Claude Code Features

Once running, you can use all standard Claude Code commands:

```bash
# Start a new chat
claudebr

# Ask for help
claudebr --help

# Use specific models
claudebr --model claude-3-sonnet-20240229

# Stream responses
claudebr --stream

# Use tools and functions
claudebr --tools
```

### Common Use Cases

#### 🖥️ **Coding Projects**
```bash
# Navigate to your project directory
cd /path/to/your/project

# Start Claude Code with local model
claudebr

# Ask for code reviews, debugging help, or new features
```

#### 📝 **Documentation Writing**
```bash
# Use for writing technical documentation
claudebr --model claude-3-haiku-20240307

# Ask for help with README files, API docs, etc.
```

#### 🔍 **Code Analysis**
```bash
# Analyze existing codebases
claudebr

# Ask questions like:
# - "Explain this function"
# - "Find potential bugs"
# - "Suggest improvements"
```

#### 🎨 **Multimodal Tasks** (with supported models)
```bash
# Use models like llava for image understanding
claudebr --model claude-3-haiku-20240307

# Upload images and ask questions about them
```

### Server Management

#### Check Server Status
```bash
# Check if the proxy server is running
ps aux | grep uvicorn

# Check server logs
tail -f proxy_server.log
```

#### Stop the Server
```bash
# If you know the PID (shown during installation)
kill <PID>

# Or find and kill the process
pkill -f "uvicorn server:app"
```

#### Restart the Server
```bash
# Stop the current server
pkill -f "uvicorn server:app"

# Start it again
source .venv/bin/activate
nohup uvicorn server:app --host 0.0.0.0 --port 8083 > proxy_server.log 2>&1 &
```

### Environment Variables

You can also set environment variables directly:

```bash
# Set the base URL for Claude Code
export ANTHROPIC_BASE_URL=http://localhost:8083

# Run Claude Code
claude

# Or use the convenience command
claudebr
```

### Troubleshooting Usage

#### Server Not Responding
```bash
# Check if server is running
curl http://localhost:8083/

# Restart the server if needed
pkill -f "uvicorn server:app"
source .venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8083
```

#### Model Not Found
```bash
# For Ollama models, make sure they're downloaded
ollama list

# Pull missing models
ollama pull <model_name>
```

#### Configuration Issues
```bash
# Test your configuration
python3 test_config.py

# Recreate configuration
python3 setup_config.py
```

### Example Interactions

Here are some example conversations you can have with your local LLM through Claude Code:

#### 💻 **Code Review Example**
```
User: Can you review this Python function for potential issues?

def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count

Assistant: I'll review this function for potential issues:

**Issues Found:**
1. **Division by Zero**: If `numbers` is an empty list, `len(numbers)` will be 0, causing a `ZeroDivisionError`
2. **Type Safety**: No validation that `numbers` contains numeric values
3. **Performance**: For large lists, calling `sum()` and `len()` separately is less efficient

**Improved Version:**
```python
def calculate_average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise TypeError("All elements must be numeric")
    
    return sum(numbers) / len(numbers)
```

**Additional Considerations:**
- Consider using `statistics.mean()` from the standard library for more robust averaging
- Add docstring for better documentation
```

#### 🔍 **Debugging Example**
```
User: My web app is getting a 500 error. Here's the error log:

Traceback (most recent call last):
  File "app.py", line 45, in main()
  File "app.py", line 23, in process_request()
KeyError: 'user_id'

Assistant: The error indicates that your code is trying to access a key `'user_id'` that doesn't exist in a dictionary. This is a common issue when:

1. **Form data is missing**: The user didn't submit the required field
2. **JSON parsing failed**: The request body wasn't properly parsed
3. **Database query returned None**: The user wasn't found in the database

**Quick Fix:**
```python
# Instead of:
user_id = request_data['user_id']

# Use:
user_id = request_data.get('user_id')
if user_id is None:
    return jsonify({'error': 'user_id is required'}), 400
```

**Better Fix with Validation:**
```python
from flask import request, jsonify

def process_request():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        # Continue processing...
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```
```

#### 📚 **Learning Example**
```
User: Can you explain how async/await works in Python?

Assistant: **Async/Await in Python** is a way to write concurrent code that can handle multiple operations without blocking.

**Key Concepts:**

1. **Async Functions**: Functions defined with `async def` return coroutines
2. **Await**: Used inside async functions to wait for other async operations
3. **Event Loop**: Manages and coordinates all the async tasks

**Basic Example:**
```python
import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    # These run concurrently, not sequentially
    data1 = await fetch_data('https://api1.example.com')
    data2 = await fetch_data('https://api2.example.com')
    
    print(f"Got {len(data1)} and {len(data2)} bytes")

# Run the async function
asyncio.run(main())
```

**Why Use Async/Await?**
- **I/O Bound Operations**: Perfect for web requests, file operations, database queries
- **Concurrency**: Handle multiple operations simultaneously
- **Non-blocking**: Your app remains responsive during long operations

**Common Patterns:**
```python
# Run multiple tasks concurrently
tasks = [fetch_data(url) for url in urls]
results = await asyncio.gather(*tasks)

# Timeout handling
try:
    result = await asyncio.wait_for(fetch_data(url), timeout=5.0)
except asyncio.TimeoutError:
    print("Request timed out")
```
```

### Best Practices & Tips 🎯

#### **Model Selection**
- **Coding Tasks**: Use `codellama`, `deepseek-coder`, or `starcoder` models
- **General Chat**: Use `llama3.2`, `mistral`, or `gemma` models
- **Multimodal**: Use `llava` or `minicpm-v` for image understanding
- **Resource Constraints**: Use smaller models (7B) for faster responses, larger models (70B) for better quality

#### **Performance Optimization**
```bash
# For faster responses, use smaller models
BIG_MODEL=codellama:7b
SMALL_MODEL=codellama:3b

# For better quality, use larger models (requires more RAM)
BIG_MODEL=codellama:13b
SMALL_MODEL=codellama:7b
```

#### **Memory Management**
- **Monitor RAM usage**: Large models (70B) require 16GB+ RAM
- **Use swap space**: If you have limited RAM, ensure sufficient swap
- **Close unused models**: `ollama rm <model_name>` to free space

#### **Effective Prompting**
- **Be specific**: Instead of "fix this code", say "fix the memory leak in this function"
- **Provide context**: Include relevant files, error messages, or requirements
- **Use iterative approach**: Start with high-level questions, then dive deeper
- **Ask for explanations**: Request explanations of suggested changes

#### **Project Organization**
```bash
# Keep your project organized
project/
├── src/           # Your source code
├── docs/          # Documentation
├── tests/         # Test files
└── .claude/       # Claude Code workspace files
```

#### **Version Control Integration**
```bash
# Use Claude Code with Git effectively
claudebr

# Ask for:
# - Commit message suggestions
# - Code review before committing
# - Branch naming conventions
# - Git workflow improvements
```

## Configuration & Troubleshooting 🔧

### Quick Configuration Setup

If you encounter configuration issues, you can use our setup script:

```bash
python3 setup_config.py
```

This script will:
- Create a `.env` file with default settings
- Validate your configuration
- Provide helpful setup instructions

### Configuration Files

The project uses several configuration files:

- **`config.env.example`** - Template with all available options
- **`.env`** - Your actual configuration (created during setup)
- **`app/config/settings.py`** - Centralized configuration management

### Common Issues

1. **"Invalid settings files" warning**: This usually means the `.env` file is missing or malformed. Run `python3 setup_config.py` to fix this.

2. **"No API keys found"**: Set at least one API key in your `.env` file:
   ```bash
   OPENAI_API_KEY=your_openai_key_here
   # or
   ANTHROPIC_API_KEY=your_anthropic_key_here
   # or
   GEMINI_API_KEY=your_gemini_key_here
   ```

3. **Configuration validation errors**: The system now validates your configuration on startup and will show specific issues that need to be fixed.

### Testing Configuration

You can test your configuration setup with:

```bash
python3 test_config.py
```

This will verify that all configuration components are working correctly.

If the installer warns that `/usr/local/bin` is not writable, you can manually move the `claudebr` script using `sudo`:

```bash
sudo mv claudebr /usr/local/bin/
```

**Note**: For most users, this global installation is not necessary as you will typically run `claudebr` from within the cloned project's directory.

## Model Mapping 🧭

This proxy intelligently maps Claude's `haiku` and `sonnet` models to your chosen `SMALL_MODEL` and `BIG_MODEL` respectively. When `PREFERRED_PROVIDER=ollama`, it automatically prefixes your selected Ollama models with `ollama/`.

### Supported Ollama Models

Here are some popular Ollama models you can use (make sure to `ollama pull` them first!):
-   `llama2`
-   `llama3`
-   `gemma`
-   `mistral`
-   `phi`
-   `tinyllama`
-   `codellama`
-   `deepseek-coder`
-   `starcoder`
-   `wizardcoder`
-   `llava` (multimodal)
-   `minicpm-v` (multimodal)
-   `llama3.2`
-   `qwen2`
-   `mistral-large`
-   `dolphin-2.6`

*You can find more models and their details on the [Ollama website](https://ollama.com/library).*

## Advanced Features 🚀

### Custom Model Configurations
Create custom model configurations in your `.env`:

```bash
# Custom model mappings
CUSTOM_MODEL_1=my-special-model:latest
CUSTOM_MODEL_2=finetuned-coder:1.0

# Use in your prompts
claudebr --model claude-3-opus-20240229
```

### Batch Processing
```bash
# Process multiple files at once
for file in *.py; do
    echo "Processing $file..."
    claudebr --input "$file" --prompt "Review this code for best practices"
done
```

### Integration with IDEs
You can integrate the proxy with various IDEs:

**VS Code:**
- Install Claude Code extension
- Set `ANTHROPIC_BASE_URL=http://localhost:8083` in settings

**JetBrains IDEs:**
- Install Claude plugin
- Configure to use local proxy

### API Usage
You can also use the proxy directly via API:

```bash
# Test the API directly
curl -X POST http://localhost:8083/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-sonnet-20240229",
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": "Hello, how are you?"}]
  }'
```

## `claudebr` Command

The installer creates a `claudebr` command that simplifies running the Claude Code CLI with the local proxy. Instead of typing `ANTHROPIC_BASE_URL=http://localhost:8083 claude`, you can simply run:

```bash
claudebr
```

### Global Installation (Optional)

By default, `claudebr` is created in the project directory. If you wish to use `claudebr` from any directory in your terminal, you might need to move it to a directory included in your system's PATH, such as `/usr/local/bin`.

## Quick Reference 📋

### Essential Commands
```bash
# Start using Claude Code with local model
claudebr

# Check server status
ps aux | grep uvicorn

# View server logs
tail -f proxy_server.log

# Stop server
pkill -f "uvicorn server:app"

# Test configuration
python3 test_config.py

# Setup configuration
python3 setup_config.py
```

### Common Model Commands
```bash
# List available Ollama models
ollama list

# Pull a new model
ollama pull codellama:13b

# Remove a model
ollama rm unused-model

# Run a model directly
ollama run codellama:13b
```

### Configuration Quick Edits
```bash
# Edit your configuration
nano .env

# Common settings to change:
# PREFERRED_PROVIDER=ollama|openai|google
# BIG_MODEL=your-preferred-model
# SMALL_MODEL=your-fast-model
# OPENAI_API_KEY=your-key
```

### Troubleshooting Commands
```bash
# Check if server is responding
curl http://localhost:8083/

# Check Python environment
python3 -c "import app.config.settings; print('Config OK')"

# Check Ollama status
ollama ps

# Restart everything
pkill -f "uvicorn server:app"
source .venv/bin/activate
nohup uvicorn server:app --host 0.0.0.0 --port 8083 > proxy_server.log 2>&1 &
```

## 📚 Educational Project

This project is created for **educational purposes** to demonstrate LLM integration, API proxy development, and local AI model deployment. Feel free to share with your peers, use in your learning journey, and contribute to the open-source community! 🎓

---

## Contributing 💖

Got ideas? Found a bug? Contributions are super welcome! Feel free to submit a Pull Request. 💡

---

## 🚀 CLED Visual Installer & CLI

CLED (Claude LLM Environment Dispatcher) is a cross-platform visual installer and CLI for setting up and managing your LLMBridgeClaudeCode environment. It provides a user-friendly wizard for:
- System checks (Python, pip, Ollama, disk, network)
- Model selection and disk usage warnings
- Python venv setup and requirements installation
- Connectivity tests before download
- Model download and configuration
- Final launch and server test

### Quick Start

1. Go to the `CLED` directory:
   ```bash
   cd CLED
   ```
2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Launch the visual installer:
   ```bash
   python3 cled_installer.py
   ```
4. Or use the CLI:
   ```bash
   python3 cled_cli.py install
   python3 cled_cli.py serve
   ```

For a full step-by-step guide, see [`CLED/INSTALLATION.md`](CLED/INSTALLATION.md).

---

## Made with ❤️ by Guy Chenya

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Guy%20Chenya-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/guychenya/)

Connect with me on LinkedIn for updates, discussions, and collaboration opportunities!

# LLM Bridge for Claude Code: Your Gateway to Free & Open-Source LLMs (via Ollama) ✨

**This project extends the original [claude-code-proxy](https://github.com/1rgs/claude-code-proxy) to seamlessly integrate with 100% free and open-source LLMs via Ollama.**

**Run Anthropic clients (like Claude Code) with your favorite local LLMs, powered by Ollama!** This proxy provides a seamless bridge to 100% free and open-source models, right from your machine. 🔗


![Ollama API Proxy](ollama_proxy.png)

## Installation & Usage 🚀

Getting started is a breeze with our interactive `install.sh` script! It handles everything from setting up your environment to configuring your preferred LLM provider.

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone YOUR_GITHUB_REPO_URL_HERE # Replace with your actual repo URL
    cd LLMBridgeClaudeCode # Or whatever you named the cloned directory
    ```

2.  **Run the installer script**:
    ```bash
    bash install.sh
    ```

    The script will guide you through the setup process. Here's what you can expect:

    ```text
    [INFO] Starting LLM Bridge for Claude Code Installer...
    [INFO] Checking for required tools: git, uv, npm, ollama...
    [SUCCESS] git is installed.
    [SUCCESS] uv is installed.
    [SUCCESS] npm is installed.
    [INFO] ollama is installed.
    [INFO] Repository already exists at /Users/guychenya/Documents/GitHub-Repos/claude-code-proxy-ollama. Skipping clone.
    [INFO] Configuring environment variables in .env...
    [INFO] .env file already exists. Skipping creation.
    ?[CHOICE] Choose your preferred LLM provider [ollama]: 
      1) ollama
      2) openai
      3) google
    #? 1
    [INFO] Set PREFERRED_PROVIDER to ollama in .env.
    [INFO] Ollama selected. No API keys needed for Ollama models.
    [INFO] Ollama models are typically stored in ~/.ollama/models.
    [INFO] You can change Ollama's default data directory by setting the OLLAMA_MODELS environment variable system-wide (e.g., in your .bashrc or .zshrc).
    [INFO] Example: export OLLAMA_MODELS=/path/to/your/ollama/models
    ?[INPUT] Enter minimum required disk space for Ollama models (GB) [20]: 20
    [INFO] Sufficient disk space available on '/Users/guychenya/.ollama': 132GB (Required: 20GB).
    [INFO] Attempting to pull default Ollama models (llama2 and phi) if not present...
    [INFO] Ollama model 'llama2' already present locally. Skipping pull.
    [INFO] Ollama model 'phi' already present locally. Skipping pull.
    [INFO] Now, let's set your default BIG_MODEL and SMALL_MODEL for the proxy.
    [INFO] These should be models you have installed locally (either pre-existing or just pulled).
    ?[INPUT] Enter BIG_MODEL for Ollama (e.g., llama2) [llama2]: llama3
    ?[INPUT] Enter SMALL_MODEL for Ollama (e.g., phi) [phi]: phi
    [INFO] Set BIG_MODEL and SMALL_MODEL for Ollama in .env.
    [INFO] Installing Python dependencies using uv...
    [SUCCESS] Python dependencies installed.
    [INFO] Installing Claude Code CLI globally using npm...
    [SUCCESS] Claude Code CLI installed.
    [INFO] Starting the proxy server in the background...
    [SUCCESS] Proxy server started in the background with PID: 12345. Output logged to proxy_server.log
    [INFO] To stop the server, run: kill 12345
    [SUCCESS] Installation complete!

    --- Next Steps ---
    1. Run Claude Code CLI, pointing to your proxy:
       ANTHROPIC_BASE_URL=http://localhost:8082 claude

    Enjoy using Claude Code with your chosen LLM backend!
    ```

### What the Installer Does ✨

Our `install.sh` script isn't just a simple setup; it's packed with features to make your life easier:

-   **Interactive Provider Choice**: Guides you through selecting Ollama, OpenAI, or Gemini as your primary LLM provider.
-   **Simplified Ollama Model Pulling**: If you choose Ollama, it automatically attempts to pull default models (`llama2` and `phi`) if not already present, ensuring a quick start.
-   **Disk Space Guardian**: Before downloading large Ollama models, it checks for sufficient disk space and warns you if space is low, giving you the option to proceed or abort.
-   **Automatic Server Launch**: Automatically starts the proxy server in the background after a successful installation, so you can jump straight into using Claude Code.
-   **Robust Error Handling**: Provides more informative messages if issues like repository cloning failures occur.
-   **Ollama Model Location Info**: Informs you about where Ollama stores its models and how you can configure that location if needed.

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

## How It Works ⚙️

This proxy acts as a clever translator:

1.  **Receives** Anthropic API requests from your Claude client. ⬇️
2.  **Translates** them into a format LiteLLM understands (which then talks to Ollama). ↔️
3.  **Sends** the request to your local Ollama server. ⬆️
4.  **Converts** Ollama's response back to Anthropic format. ↔️
5.  **Returns** the magic to your Claude client! 🎉

It handles both streaming and non-streaming responses, keeping your Claude experience smooth. 💧

![Ollama Proxy Bottom](ollama_proxy_bottom.png)

## Why Try LLM Bridge for Claude Code? 💡

This project offers several compelling advantages:

-   **100% Free & Open-Source LLMs**: Leverage powerful language models without API costs or reliance on external services. Your data stays local!
-   **Enhanced Privacy**: Since models run on your machine, your interactions remain private and secure.
-   **Cost-Effective Development**: Experiment and build with LLMs without incurring API usage fees.
-   **Seamless Claude Code Integration**: Continue using the familiar Claude Code CLI, now powered by your local models.
-   **Easy Setup**: The `install.sh` script makes getting started incredibly simple, even for those new to local LLMs.
-   **Flexibility**: While optimized for Ollama, it still supports OpenAI and Google Gemini for broader compatibility.

## Contributing 💖

Got ideas? Found a bug? Contributions are super welcome! Feel free to submit a Pull Request. 💡
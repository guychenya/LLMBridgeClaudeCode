#!/bin/bash

# --- Configuration ---
REPO_URL="https://github.com/guychenya/LLMBridgeClaudeCode.git" # IMPORTANT: Update this to your actual repository URL when you push this project!
REPO_NAME="claude-code-proxy-ollama"
INSTALL_DIR="/Users/guychenya/Documents/GitHub-Repos/$REPO_NAME" # Assuming current working directory is where the repo is cloned
CLAUDE_CODE_CLI="@anthropic-ai/claude-code"

# --- Colors for better output ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Helper Functions ---

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        return 1
    fi
    return 0
}

prompt_for_input() {
    local __result_var=$1
    local __prompt_msg=$2
    local __default_val=$3
    echo -n "$(echo -e "${BLUE}?[INPUT]${NC} $__prompt_msg [${YELLOW}$__default_val${NC}]: ")"
    read user_input
    if [ -z "$user_input" ]; then
        eval $__result_var="'$__default_val'"
    else
        eval $__result_var="'$user_input'"
    fi
}

prompt_for_choice() {
    local __result_var=$1
    local __prompt_msg=$2
    local __choices_str=$3 # Space-separated string of choices
    local __default_choice=$4

    local choices_array
    choices_array=($__choices_str)
    local i=1
    echo -e "${BLUE}?[CHOICE]${NC} $__prompt_msg [${YELLOW}$__default_choice${NC}]: "
    for choice in "${choices_array[@]}"; do
        echo "  $i) $choice"
        i=$((i+1))
    done
    echo -n "#? "
    read user_choice_num

    if [ -z "$user_choice_num" ]; then
        eval $__result_var="'$__default_choice'"
    elif [[ "$user_choice_num" =~ ^[0-9]+$ ]] && [ "$user_choice_num" -ge 1 ] && [ "$user_choice_num" -le ${#choices_array[@]} ]; then
        eval $__result_var="'${choices_array[$((user_choice_num-1))]}'"
    else
        log_warn "Invalid option. Defaulting to '$__default_choice'."
        eval $__result_var="'$__default_choice'"
    fi
}

check_disk_space() {
    local required_gb=$1
    local path=$2

    local FREE_SPACE_GB
    FREE_SPACE_GB=$(df -g "$path" | tail -n 1 | awk '{print $4}')

    if (( $(echo "$FREE_SPACE_GB < $required_gb" | bc -l) )); then
        log_error "Insufficient disk space!"
        log_error "Required: ${required_gb}GB, Available on '$path': ${FREE_SPACE_GB}GB."
        return 1
    else
        log_info "Sufficient disk space available on '$path': ${FREE_SPACE_GB}GB (Required: ${required_gb}GB)."
        return 0
    fi
}

# --- Main Installation Script ---

log_info "Starting LLM Bridge for Claude Code Installer..."

# 1. Check for prerequisites
log_info "Checking for required tools: git, uv, npm, ollama..."
check_command git || exit 1
check_command uv || exit 1
check_command npm || exit 1

OLLAMA_INSTALLED=false
if check_command ollama; then
    OLLAMA_INSTALLED=true
else
    log_warn "Ollama is not installed. You can still use OpenAI/Gemini, but Ollama models won't work locally."
fi

# 2. Clone repository if not already in it
if [ ! -d "$INSTALL_DIR" ]; then
    log_info "Cloning repository to $INSTALL_DIR..."
    if ! git clone "$REPO_URL" "$INSTALL_DIR" 2>/dev/null; then
        log_error "Failed to clone repository from '$REPO_URL'."
        log_error "This might mean the repository is unavailable or the URL is incorrect."
        log_error "Please verify the REPO_URL in the 'install.sh' script or contact the repository creator."
        exit 1
    fi
    log_success "Repository cloned."
else
    log_info "Repository already exists at $INSTALL_DIR. Skipping clone."
fi

# Navigate into the project directory
cd "$INSTALL_DIR" || { log_error "Failed to change directory to $INSTALL_DIR. Exiting."; exit 1; }

# 3. Configure .env
log_info "Configuring environment variables in .env..."
if [ ! -f ".env" ]; then
    cp ".env.example" ".env"
    log_info "Created .env file from .env.example."
else
    log_info ".env file already exists. Skipping creation."
fi

# Prompt for preferred provider
PREFERRED_PROVIDER_CHOICES="ollama openai google"
DEFAULT_PREFERRED_PROVIDER="ollama"
prompt_for_choice PREFERRED_PROVIDER "Choose your preferred LLM provider" "$PREFERRED_PROVIDER_CHOICES" "$DEFAULT_PREFERRED_PROVIDER"

# Update .env with preferred provider
sed -i '' "s/^PREFERRED_PROVIDER=.*/PREFERRED_PROVIDER=$PREFERRED_PROVIDER/" .env # macOS compatible sed
log_info "Set PREFERRED_PROVIDER to $PREFERRED_PROVIDER in .env."

if [ "$PREFERRED_PROVIDER" == "ollama" ]; then
    log_info "Ollama selected. No API keys needed for Ollama models."
    
    if [ "$OLLAMA_INSTALLED" = true ]; then
        # Inform about Ollama model location
        log_info "Ollama models are typically stored in ~/.ollama/models."
        log_info "You can change Ollama's default data directory by setting the OLLAMA_MODELS environment variable system-wide (e.g., in your .bashrc or .zshrc)."
        log_info "Example: export OLLAMA_MODELS=/path/to/your/ollama/models"

        # Disk space check
        DEFAULT_REQUIRED_DISK_SPACE_GB=20
        REQUIRED_DISK_SPACE_GB=""
        prompt_for_input REQUIRED_DISK_SPACE_GB "Enter minimum required disk space for Ollama models (GB)" "$DEFAULT_REQUIRED_DISK_SPACE_GB"
        if ! check_disk_space "$REQUIRED_DISK_SPACE_GB" "${HOME}/.ollama"; then
            log_warn "Proceeding with installation, but you might run out of space if you download large models."
            PROCEED_ANYWAY=""
            prompt_for_choice PROCEED_ANYWAY "Do you want to proceed anyway?" "Yes No" "No"
            if [ "$PROCEED_ANYWAY" == "No" ]; then
                log_info "Aborting installation due to insufficient disk space. Please free up space or adjust the required amount."
                exit 0
            fi
        fi

        # Define model choices based on task
        CODING_MODELS="codellama:13b-instruct deepseek-coder:33b-instruct starcoder2:15b phi3:mini llama3:8b-instruct"
        CHAT_MODELS="llama3:8b-instruct mistral:7b-instruct gemma:7b-instruct phi3:mini dolphin-mistral:7b-v2.7"
        MULTIMODAL_MODELS="llava:7b minicpm-v:2.5b bakllava:7b"

        # Prompt for primary task
        TASK_CHOICES="coding chat multimodal"
        DEFAULT_TASK="coding"
        prompt_for_choice PRIMARY_TASK "Choose your primary task" "$TASK_CHOICES" "$DEFAULT_TASK"

        SELECTED_MODELS=""
        DEFAULT_BIG_MODEL=""
        DEFAULT_SMALL_MODEL=""

        case "$PRIMARY_TASK" in
            coding)
                SELECTED_MODELS="$CODING_MODELS"
                DEFAULT_BIG_MODEL="deepseek-coder:33b-instruct"
                DEFAULT_SMALL_MODEL="codellama:13b-instruct"
                ;;
            chat)
                SELECTED_MODELS="$CHAT_MODELS"
                DEFAULT_BIG_MODEL="llama3:8b-instruct"
                DEFAULT_SMALL_MODEL="mistral:7b-instruct"
                ;;
            multimodal)
                SELECTED_MODELS="$MULTIMODAL_MODELS"
                DEFAULT_BIG_MODEL="llava:7b"
                DEFAULT_SMALL_MODEL="minicpm-v:2.5b"
                ;;
        esac

        # Prompt for BIG_MODEL
        prompt_for_choice BIG_MODEL_OLLAMA "Choose a BIG_MODEL for $PRIMARY_TASK tasks" "$SELECTED_MODELS" "$DEFAULT_BIG_MODEL"
        
        # Prompt for SMALL_MODEL
        prompt_for_choice SMALL_MODEL_OLLAMA "Choose a SMALL_MODEL for $PRIMARY_TASK tasks" "$SELECTED_MODELS" "$DEFAULT_SMALL_MODEL"

        # Pull selected models if not present
        OLLAMA_MODELS_TO_PULL=("$BIG_MODEL_OLLAMA" "$SMALL_MODEL_OLLAMA")
        for model in "${OLLAMA_MODELS_TO_PULL[@]}"; do
            if ! ollama list | grep -q "$model"; then
                log_info "Model '$model' not found locally. Attempting to pull..."
                if ! ollama pull "$model"; then
                    log_warn "Failed to pull Ollama model '$model'. Please check your Ollama server and model name."
                else
                    log_success "Successfully pulled Ollama model '$model'."
                fi
            else
                log_info "Ollama model '$model' already present locally. Skipping pull."
            fi
        done

        # Update .env with selected models
        sed -i '' "s/^BIG_MODEL=.*/BIG_MODEL=$BIG_MODEL_OLLAMA/" .env
        sed -i '' "s/^SMALL_MODEL=.*/SMALL_MODEL=$SMALL_MODEL_OLLAMA/" .env
        log_info "Set BIG_MODEL to '$BIG_MODEL_OLLAMA' and SMALL_MODEL to '$SMALL_MODEL_OLLAMA' in .env."

    else
        log_warn "Ollama is not installed. Skipping Ollama model download and configuration."
    fi

elif [ "$PREFERRED_PROVIDER" == "openai" ]; then
    prompt_for_input OPENAI_API_KEY "Enter your OpenAI API Key" "YOUR_OPENAI_API_KEY"
    sed -i '' "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_API_KEY/" .env
    log_info "Set OpenAI API Key in .env."
elif [ "$PREFERRED_PROVIDER" == "google" ]; then
    prompt_for_input GEMINI_API_KEY "Enter your Gemini API Key" "YOUR_GEMINI_API_KEY"
    sed -i '' "s/^GEMINI_API_KEY=.*/GEMINI_API_KEY=$GEMINI_API_KEY/" .env
    log_info "Set Gemini API Key in .env."
fi

# 4. Install Python dependencies using uv
log_info "Installing Python dependencies using uv..."
if ! uv sync; then
    log_error "Failed to install Python dependencies. Exiting."
    exit 1
fi
log_success "Python dependencies installed."

# 5. Install Claude Code CLI
log_info "Installing Claude Code CLI globally using npm..."
if ! npm install -g "$CLAUDE_CODE_CLI"; then
    log_warn "Failed to install Claude Code CLI. You might need to install Node.js/npm or fix permissions."
    log_warn "You can try running 'sudo npm install -g $CLAUDE_CODE_CLI' manually later."
else
    log_success "Claude Code CLI installed."
fi

# 6. Start the proxy server in the background
log_info "Starting the proxy server in the background..."
# Use nohup to ensure it runs even if the terminal closes, and redirect output to a log file
source .venv/bin/activate
nohup .venv/bin/uvicorn server:app --host 0.0.0.0 --port 8082 > proxy_server.log 2>&1 & 
SERVER_PID=$!
log_success "Proxy server started in the background with PID: $SERVER_PID. Output logged to proxy_server.log"
log_info "To stop the server, run: kill $SERVER_PID"

log_success "Installation complete!"

# 7. Create the 'claudebr' command
log_info "Creating 'claudebr' command for easy access..."
cat << 'EOF' > claudebr
#!/bin/bash
# Wrapper script to run Claude Code CLI with the local proxy

# Activate the Python virtual environment
source "$(dirname "$0")/.venv/bin/activate"

ANTHROPIC_BASE_URL=http://localhost:8082 claude "$@"
EOF

chmod +x claudebr

if [ -w "/usr/local/bin" ]; then
    log_info "Attempting to install 'claudebr' to /usr/local/bin..."
    if mv claudebr /usr/local/bin/claudebr; then
        log_success "'claudebr' command installed successfully."
    else
        log_warn "Failed to move 'claudebr' to /usr/local/bin. You might need to run with sudo."
        log_warn "You can also manually move it: sudo mv claudebr /usr/local/bin/"
    fi
else
    log_warn "/usr/local/bin is not writable. You can install 'claudebr' manually:"
    log_warn "1. Add /usr/local/bin to your PATH if it's not there."
    log_warn "2. Run: sudo mv claudebr /usr/local/bin/"
fi


# --- Final Instructions ---
echo -e "\n${BLUE}--- Next Steps ---${NC}"
echo -e "1. ${BLUE}Run Claude Code CLI using the new 'claudebr' command:${NC}"
echo -e "   ${YELLOW}claudebr${NC}"
echo -e "\n${GREEN}Enjoy using Claude Code with your chosen LLM backend!${NC}"

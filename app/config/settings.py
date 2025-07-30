import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Provider Configuration
PREFERRED_PROVIDER = os.environ.get("PREFERRED_PROVIDER", "openai").lower()

# Model Configuration
BIG_MODEL = os.environ.get("BIG_MODEL", "gpt-4o")
SMALL_MODEL = os.environ.get("SMALL_MODEL", "gpt-3.5-turbo")

# Ollama Configuration
OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

# Server Configuration
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8083"))

# Logging Configuration
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Model Lists
OPENAI_MODELS = [
    "o3-mini", "o1", "o1-mini", "o1-pro", "gpt-4.5-preview", "gpt-4o",
    "gpt-4o-audio-preview", "chatgpt-4o-latest", "gpt-4o-mini",
    "gpt-4o-mini-audio-preview", "gpt-4.1", "gpt-4.1-mini"
]

GEMINI_MODELS = [
    "gemini-2.5-pro-preview-03-25", "gemini-2.0-flash"
]

OLLAMA_MODELS = [
    "llama2", "llama3", "llama3.2", "gemma", "mistral", "phi",
    "codellama", "deepseek-coder", "qwen2", "tinyllama", "mistral-large",
    "llava", "minicpm-v", "dolphin-2.6", "starcoder", "wizardcoder"
]

# Model Alias Mapping
def get_model_alias_map() -> Dict[str, str]:
    """Get the model alias mapping based on environment variables"""
    return {
        # Claude 3.5 models (latest)
        "claude-3-5-sonnet-20241022": BIG_MODEL,
        "claude-3-5-haiku-20241022": SMALL_MODEL,
        "claude-3-5-opus-20241022": BIG_MODEL,
        
        # Claude 3 models
        "claude-3-opus-20240229": BIG_MODEL,
        "claude-3-sonnet-20240229": BIG_MODEL,
        "claude-3-haiku-20240307": SMALL_MODEL,
        
        # Claude 4 models
        "claude-opus-4-20250514": BIG_MODEL,
        "claude-sonnet-4-20250514": BIG_MODEL,
        "claude-haiku-4-20250514": SMALL_MODEL,
        
        # Legacy Claude models
        "claude-2.1": BIG_MODEL,
        "claude-2.0": BIG_MODEL,
        "claude-instant-1.2": SMALL_MODEL,
    }

# Filter out None values from the map if models are not set
MODEL_ALIAS_MAP = {k: v for k, v in get_model_alias_map().items() if v is not None}

# Validation
def validate_configuration() -> List[str]:
    """Validate the configuration and return any issues"""
    issues = []
    
    # Check if at least one API key is provided
    if not any([ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY]):
        issues.append("No API keys found. Please set at least one of: ANTHROPIC_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY")
    
    # Check if models are configured
    if not BIG_MODEL:
        issues.append("BIG_MODEL is not configured")
    if not SMALL_MODEL:
        issues.append("SMALL_MODEL is not configured")
    
    # Check provider-specific requirements
    if PREFERRED_PROVIDER == "openai" and not OPENAI_API_KEY:
        issues.append("OpenAI is set as preferred provider but OPENAI_API_KEY is not configured")
    elif PREFERRED_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
        issues.append("Anthropic is set as preferred provider but ANTHROPIC_API_KEY is not configured")
    elif PREFERRED_PROVIDER == "google" and not GEMINI_API_KEY:
        issues.append("Google is set as preferred provider but GEMINI_API_KEY is not configured")
    
    return issues 
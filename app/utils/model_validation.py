import logging
from typing import Any, Dict
from app.config.settings import (
    BIG_MODEL, SMALL_MODEL, PREFERRED_PROVIDER,
    OPENAI_MODELS, GEMINI_MODELS, OLLAMA_MODELS
)

logger = logging.getLogger(__name__)

def validate_and_map_model(model_name: str, info: Dict[str, Any]) -> str:
    original_model = model_name
    new_model = model_name  # Default to original value

    logger.debug(f"📋 MODEL VALIDATION: Original='{original_model}', Preferred='{PREFERRED_PROVIDER}', BIG='{BIG_MODEL}', SMALL='{SMALL_MODEL}'")

    # Remove provider prefixes for easier matching
    clean_v = model_name
    if clean_v.startswith('openai/'):
        clean_v = clean_v[7:]
    elif clean_v.startswith('gemini/'):
        clean_v = clean_v[7:]
    elif clean_v.startswith('ollama/'):
        clean_v = clean_v[7:]

    # --- Mapping Logic --- START ---
    mapped = False
    # Explicitly map Anthropic models to preferred provider's BIG/SMALL models
    if PREFERRED_PROVIDER == "ollama":
        if any(s in clean_v.lower() for s in ['haiku', 'claude-3-haiku', 'claude-3-5-haiku']):
            new_model = f"ollama/{SMALL_MODEL}"
            mapped = True
        elif any(s in clean_v.lower() for s in ['sonnet', 'claude-3-sonnet', 'opus', 'claude-3-opus', 'claude-opus-4']):
            new_model = f"ollama/{BIG_MODEL}"
            mapped = True
    elif PREFERRED_PROVIDER == "google":
        if any(s in clean_v.lower() for s in ['haiku', 'claude-3-haiku', 'claude-3-5-haiku']):
            new_model = f"gemini/{SMALL_MODEL}"
            mapped = True
        elif any(s in clean_v.lower() for s in ['sonnet', 'claude-3-sonnet', 'opus', 'claude-3-opus', 'claude-opus-4']):
            new_model = f"gemini/{BIG_MODEL}"
            mapped = True
    elif PREFERRED_PROVIDER == "openai":
        if any(s in clean_v.lower() for s in ['haiku', 'claude-3-haiku', 'claude-3-5-haiku']):
            new_model = f"openai/{SMALL_MODEL}"
            mapped = True
        elif any(s in clean_v.lower() for s in ['sonnet', 'claude-3-sonnet', 'opus', 'claude-3-opus', 'claude-opus-4']):
            new_model = f"openai/{BIG_MODEL}"
            mapped = True

    # If not mapped by preferred provider, try to add prefixes if they match known lists
    if not mapped:
        if clean_v in GEMINI_MODELS and not model_name.startswith('gemini/'):
            new_model = f"gemini/{clean_v}"
            mapped = True
        elif clean_v in OPENAI_MODELS and not model_name.startswith('openai/'):
            new_model = f"openai/{clean_v}"
            mapped = True
        elif clean_v in OLLAMA_MODELS and not model_name.startswith('ollama/'):
            new_model = f"ollama/{clean_v}"
            mapped = True
    # --- Mapping Logic --- END ---

    if mapped:
        logger.debug(f"📌 MODEL MAPPING: '{original_model}' ➡️ '{new_model}'")
    else:
         # If no mapping occurred and no prefix exists, log warning or decide default
         if not model_name.startswith(('openai/', 'gemini/', 'anthropic/', 'ollama/')):
             logger.warning(f"⚠️ No prefix or mapping rule for model: '{original_model}'. Using as is.")
         new_model = model_name # Ensure we return the original if no rule applied

    # Store the original model in the values dictionary
    values = info.data
    if isinstance(values, dict):
        values['original_model'] = original_model

    return new_model

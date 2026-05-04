
# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

import os
from dotenv import load_dotenv

load_dotenv()


# ========================
# LLM PROVIDER CONFIGURATION
# ========================
# Change this to switch providers: "groq", "openai", "ollama", "anthropic"
PROVIDER = os.getenv("LLM_PROVIDER", "groq")

# ========================
# PROVIDER CONFIGURATIONS
# ========================

GROQ_CONFIG = {
    "model": "groq/llama-3.3-70b-versatile",
    "api_key": os.getenv("GROQ_API_KEY"),
}

OPENAI_CONFIG = {
    "model": "gpt-4o-mini",
    "api_key": os.getenv("OPENAI_API_KEY"),
}

OLLAMA_CONFIG = {
    "model": "ollama/llama3",
    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
}

ANTHROPIC_CONFIG = {
    "model": "claude-3-5-sonnet-20241022",
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
}

HUGGINGFACE_CONFIG = {
    "model": "huggingface/HuggingFaceH4/zephyr-7b-beta",
    "api_key": os.getenv("HUGGINGFACE_API_KEY"),
}

MISTRAL_CONFIG = {
    "model": "mistral/mistral-tiny",
    "api_key": os.getenv("MISTRAL_API_KEY"),
}

GEMINI_CONFIG = {
    "model": "gemini/gemini-pro",
    "api_key": os.getenv("GEMINI_API_KEY"),
}

NVIDIA_CONFIG = {
    "model": "nvidia_nim/mistralai/mistral-medium-3.5-128b",
    "api_key": os.getenv("NVIDIA_API_KEY"),
}

# ========================
# PROVIDER MAP
# ========================
PROVIDER_CONFIGS = {
    "groq": GROQ_CONFIG,
    "openai": OPENAI_CONFIG,
    "ollama": OLLAMA_CONFIG,
    "anthropic": ANTHROPIC_CONFIG,
    "huggingface": HUGGINGFACE_CONFIG,
    "mistral": MISTRAL_CONFIG,
    "gemini": GEMINI_CONFIG,
    "nvidia": NVIDIA_CONFIG,
}


def get_llm_config():
    # Read provider dynamically to pick up changes from the UI
    current_provider = os.getenv("LLM_PROVIDER", "groq")
    
    if current_provider not in PROVIDER_CONFIGS:
        raise ValueError(
            f"Invalid LLM provider: {current_provider}. "
            f"Choose from: {', '.join(PROVIDER_CONFIGS.keys())}"
        )
    
    # Get the base config
    config = PROVIDER_CONFIGS[current_provider].copy()
    
    # Update with current environment variables
    env_key = f"{current_provider.upper()}_API_KEY"
    if os.getenv(env_key):
        config["api_key"] = os.getenv(env_key)
    
    # Validate that required credentials are present
    if current_provider in ["groq", "openai", "anthropic", "huggingface", "mistral", "gemini", "nvidia"]:
        if not config.get("api_key"):
            # Instead of raising ValueError immediately, we'll return a config with no key
            # and let the calling function handle it or wait until the user provides it.
            pass
            
    return config


def get_llm_params():
    
    config = get_llm_config()
    
    # Check if a specific model is requested via env var
    model = os.getenv("LLM_MODEL")
    if not model:
        model = config["model"]
        
    params = {
        "model": model,
        "temperature": 0.1
    }
    
    if "api_key" in config and config["api_key"]:
        params["api_key"] = config["api_key"]
    
    if "base_url" in config:
        params["base_url"] = config["base_url"]
    
    return params


# ========================
# USAGE INSTRUCTIONS
# ========================

# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License


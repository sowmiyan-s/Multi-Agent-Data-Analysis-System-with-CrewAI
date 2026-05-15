from typing import Dict, Any
from .app_config import settings
import os

def get_llm_params() -> Dict[str, Any]:
    """
    Returns the LLM parameters based on the current configuration.
    Priority: Environment Variables > Settings > Defaults
    """
    provider = os.getenv("LLM_PROVIDER", settings.DEFAULT_PROVIDER)
    model = os.getenv("LLM_MODEL", settings.DEFAULT_MODEL)
    
    # Map of providers to their respective API keys in settings
    key_map = {
        "openai": settings.OPENAI_API_KEY,
        "groq": settings.GROQ_API_KEY,
        "anthropic": settings.ANTHROPIC_API_KEY,
        "nvidia": settings.NVIDIA_API_KEY,
        "gemini": settings.GEMINI_API_KEY,
    }
    
    api_key = key_map.get(provider.lower())
    
    params = {
        "model": model,
        "temperature": 0.2,
        "max_tokens": 4096,
        "timeout": 120,
        "num_retries": 3,
    }
    
    if api_key:
        params["api_key"] = api_key
        
    return params


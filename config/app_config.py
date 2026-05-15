from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "Agentic Data Intelligence"
    VERSION: str = "3.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # LLM Configuration
    DEFAULT_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    DEFAULT_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o")
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    NVIDIA_API_KEY: Optional[str] = os.getenv("NVIDIA_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # Paths
    DATA_DIR: str = "data"
    OUTPUT_DIR: str = "outputs"
    LOG_DIR: str = "logs"

    class Config:
        case_sensitive = True

settings = Settings()

# Ensure directories exist
for directory in [settings.DATA_DIR, settings.OUTPUT_DIR, settings.LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

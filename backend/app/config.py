import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AGRICOMPLY AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Storage settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./agri_comply.db")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./data/uploads")
    
    # LLM Settings (Optional local / zero-cost fallback)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ENABLE_LOCAL_LLM: bool = os.getenv("ENABLE_LOCAL_LLM", "false").lower() == "true"
    
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()

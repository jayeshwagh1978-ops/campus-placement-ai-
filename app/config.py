import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Campus Placement AI Platform"
    APP_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: Optional[str] = None
    MONGODB_URL: Optional[str] = None
    
    # AI APIs (optional)
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET: str = "your-jwt-secret-change-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Default database if not provided
if not settings.DATABASE_URL:
    settings.DATABASE_URL = "sqlite:///./campus_placement.db"

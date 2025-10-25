"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Project Info
    PROJECT_NAME: str = "periph4all API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # Next.js default dev server
        "http://127.0.0.1:3000",
    ]
    
    # Data Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    CACHE_DIR: Path = DATA_DIR / "cache"
    DATASET_PATH: Path = DATA_DIR / "FINAL.csv"
    
    # ML Settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384  # Default for all-MiniLM-L6-v2
    TOP_K_RECOMMENDATIONS: int = 3
    
    # OpenAI Settings (optional)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # UMAP Settings
    UMAP_N_NEIGHBORS: int = 15
    UMAP_MIN_DIST: float = 0.1
    UMAP_N_COMPONENTS: int = 2
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.CACHE_DIR.mkdir(parents=True, exist_ok=True)


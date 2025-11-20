"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Project Info
    PROJECT_NAME: str = "periph4all API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS - can be set via ALLOWED_ORIGINS env var as comma-separated string
    ALLOWED_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",  # Next.js default dev server
        "http://127.0.0.1:3000",
    ]
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse ALLOWED_ORIGINS from environment or use defaults"""
        if isinstance(v, str):
            # If it's a string (from env), split by comma
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            # Always include localhost for local development
            if "http://localhost:3000" not in origins:
                origins.append("http://localhost:3000")
            if "http://127.0.0.1:3000" not in origins:
                origins.append("http://127.0.0.1:3000")
            return origins
        return v
    
    # Data Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    CACHE_DIR: Path = DATA_DIR / "cache"
    DATASET_PATH: Path = DATA_DIR / "FINAL.csv"
    
    # ML Settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384  # Default for all-MiniLM-L6-v2
    TOP_K_RECOMMENDATIONS: int = 3
    
    # Groq Settings
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-70b-versatile"  # or mixtral-8x7b-32768
    
    # UMAP Settings
    UMAP_N_NEIGHBORS: int = 15
    UMAP_MIN_DIST: float = 0.1
    UMAP_N_COMPONENTS: int = 2
    
    class Config:
        env_file = "../.env"  # Look for .env in project root
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env that aren't defined in Settings


settings = Settings()


# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.CACHE_DIR.mkdir(parents=True, exist_ok=True)


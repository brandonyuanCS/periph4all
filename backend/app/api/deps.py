"""
API Dependencies
Shared dependencies for API endpoints (e.g., service instances)
"""
from functools import lru_cache
from app.services.data_loader import DataLoader
from app.services.embeddings import EmbeddingService
from app.services.recommender import RecommenderService
from app.services.llm import LLMService


@lru_cache()
def get_data_loader() -> DataLoader:
    """Get or create DataLoader singleton"""
    return DataLoader()


@lru_cache()
def get_embedding_service() -> EmbeddingService:
    """Get or create EmbeddingService singleton"""
    return EmbeddingService()


@lru_cache()
def get_recommender_service() -> RecommenderService:
    """Get or create RecommenderService singleton"""
    data_loader = get_data_loader()
    embedding_service = get_embedding_service()
    return RecommenderService(data_loader, embedding_service)


@lru_cache()
def get_llm_service() -> LLMService:
    """Get or create LLMService singleton"""
    return LLMService()


"""
Recommendations Endpoint
Handles mouse recommendation logic based on user preferences
"""
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    UserPreferences
)
from app.services.recommender import RecommenderService
from app.api.deps import get_recommender_service

router = APIRouter()


@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    recommender: RecommenderService = Depends(get_recommender_service)
):
    """
    Get top K mouse recommendations based on user preferences
    
    Uses vector embeddings and cosine similarity to find the best matches.
    """
    try:
        recommendations = await recommender.recommend(
            preferences=request.user_preferences,
            top_k=request.top_k,
            include_reasoning=request.include_reasoning
        )
        
        return RecommendationResponse(
            recommendations=recommendations,
            user_preferences=request.user_preferences
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation generation failed: {str(e)}"
        )


@router.post("/quick", response_model=RecommendationResponse)
async def get_quick_recommendations(
    preferences: UserPreferences,
    recommender: RecommenderService = Depends(get_recommender_service)
):
    """
    Quick recommendation endpoint with default settings
    """
    try:
        recommendations = await recommender.recommend(
            preferences=preferences,
            top_k=3,
            include_reasoning=False
        )
        
        return RecommendationResponse(
            recommendations=recommendations,
            user_preferences=preferences
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quick recommendation failed: {str(e)}"
        )


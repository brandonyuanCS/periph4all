"""
Visualizations Endpoint
Handles embedding space visualization data
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.models.schemas import (
    VisualizationResponse,
    UserPreferences
)
from app.services.recommender import RecommenderService
from app.api.deps import get_recommender_service

router = APIRouter()


@router.get("/embedding-space", response_model=VisualizationResponse)
async def get_embedding_visualization(
    recommender: RecommenderService = Depends(get_recommender_service),
    include_user: bool = Query(False, description="Include user preference point"),
):
    """
    Get 2D visualization of mouse embeddings in reduced dimensional space
    
    Uses UMAP to project high-dimensional embeddings to 2D for visualization.
    """
    try:
        visualization_data = await recommender.get_visualization_data(
            include_user_point=include_user
        )
        return visualization_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Visualization generation failed: {str(e)}"
        )


@router.post("/embedding-space-with-user", response_model=VisualizationResponse)
async def get_embedding_visualization_with_user(
    user_preferences: UserPreferences,
    recommender: RecommenderService = Depends(get_recommender_service),
):
    """
    Get 2D visualization including user preference point and recommendations
    """
    try:
        visualization_data = await recommender.get_visualization_with_user(
            preferences=user_preferences
        )
        return visualization_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Visualization with user failed: {str(e)}"
        )

@router.post("/graph-data", response_model=dict)
async def get_graph_visualization(
    user_preferences: UserPreferences,
    k_neighbors: int = Query(5, description="Number of nearest neighbors per node"),
    recommender: RecommenderService = Depends(get_recommender_service),
):
    """
    Get force graph data with k-nearest neighbor edges
    """
    try:
        graph_data = await recommender.get_graph_data(
            preferences=user_preferences,
            k_neighbors=k_neighbors
        )
        return graph_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Graph data generation failed: {str(e)}"
        )

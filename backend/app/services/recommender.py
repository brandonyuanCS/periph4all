"""
Recommender Service
Core recommendation logic using embeddings and similarity
"""
import numpy as np
import umap
from typing import List, Optional
from app.models.schemas import (
    UserPreferences,
    MouseRecommendation,
    MouseInfo,
    VisualizationResponse,
    EmbeddingPoint
)
from app.services.data_loader import DataLoader
from app.services.embeddings import EmbeddingService
from app.utils.similarity import cosine_similarity, top_k_similar
from app.core.config import settings


class RecommenderService:
    """Handles mouse recommendations based on embeddings"""
    
    def __init__(self, data_loader: DataLoader, embedding_service: EmbeddingService):
        self.data_loader = data_loader
        self.embedding_service = embedding_service
        self._mouse_embeddings: Optional[np.ndarray] = None
        self._umap_reducer: Optional[umap.UMAP] = None
        self._reduced_embeddings: Optional[np.ndarray] = None
    
    def _get_mouse_embeddings(self) -> np.ndarray:
        """Get or generate mouse embeddings"""
        if self._mouse_embeddings is None:
            mice = self.data_loader.get_mice_list()
            self._mouse_embeddings = self.embedding_service.generate_mouse_embeddings(mice)
        return self._mouse_embeddings
    
    def _apply_budget_filter(self, preferences: UserPreferences) -> Optional[np.ndarray]:
        """Apply budget filtering and return valid indices"""
        if preferences.budget_min is None and preferences.budget_max is None:
            return None
        
        mice = self.data_loader.get_mice_list()
        valid_indices = []
        
        for i, mouse in enumerate(mice):
            price = mouse.get('price')
            if price is None or np.isnan(price):
                continue
            
            if preferences.budget_min is not None and price < preferences.budget_min:
                continue
            if preferences.budget_max is not None and price > preferences.budget_max:
                continue
            
            valid_indices.append(i)
        
        return np.array(valid_indices) if valid_indices else None
    
    async def recommend(self, preferences: UserPreferences, top_k: int = 3,
                       include_reasoning: bool = True) -> List[MouseRecommendation]:
        """
        Generate top K mouse recommendations
        
        Args:
            preferences: User preferences
            top_k: Number of recommendations to return
            include_reasoning: Whether to generate reasoning (requires LLM)
        
        Returns:
            List of mouse recommendations with similarity scores
        """
        # Generate user embedding
        user_embedding = self.embedding_service.generate_user_embedding(preferences)
        
        # Get mouse embeddings
        mouse_embeddings = self._get_mouse_embeddings()
        
        # Apply budget filter if specified
        valid_indices = self._apply_budget_filter(preferences)
        
        if valid_indices is not None and len(valid_indices) == 0:
            # No mice match budget constraints
            return []
        
        # Filter embeddings if needed
        if valid_indices is not None:
            filtered_embeddings = mouse_embeddings[valid_indices]
        else:
            filtered_embeddings = mouse_embeddings
            valid_indices = np.arange(len(mouse_embeddings))
        
        # Find top K similar mice
        similarities = cosine_similarity(user_embedding.reshape(1, -1), filtered_embeddings)[0]
        top_k_indices, top_k_scores = top_k_similar(similarities, k=min(top_k, len(similarities)))
        
        # Map back to original indices
        original_indices = valid_indices[top_k_indices]
        
        # Build recommendations
        mice = self.data_loader.get_mice_list()
        recommendations = []
        
        for orig_idx, score in zip(original_indices, top_k_scores):
            mouse_data = mice[orig_idx]
            
            # Convert to MouseInfo schema
            mouse_info = MouseInfo(
                name=mouse_data.get('name', 'Unknown'),
                brand=mouse_data.get('brand', 'Unknown'),
                price=mouse_data.get('price'),
                weight=mouse_data.get('weight'),
                dpi_max=mouse_data.get('dpi_max'),
                wireless=mouse_data.get('wireless'),
                shape=mouse_data.get('shape'),
                sensor=mouse_data.get('sensor'),
                url=mouse_data.get('url')
            )
            
            reasoning = None
            if include_reasoning:
                reasoning = self._generate_reasoning(mouse_data, preferences, score)
            
            recommendations.append(MouseRecommendation(
                mouse=mouse_info,
                similarity_score=float(score),
                reasoning=reasoning
            ))
        
        return recommendations
    
    def _generate_reasoning(self, mouse_data: dict, preferences: UserPreferences, 
                          score: float) -> str:
        """Generate simple rule-based reasoning for recommendation"""
        reasons = []
        
        # Check grip compatibility
        if preferences.grip_type and 'grip_compatibility' in mouse_data:
            grip_compat = str(mouse_data['grip_compatibility']).lower()
            if preferences.grip_type.value in grip_compat:
                reasons.append(f"Compatible with {preferences.grip_type.value} grip")
        
        # Check weight preference
        if preferences.weight_preference and 'weight' in mouse_data:
            weight = mouse_data['weight']
            if weight and not np.isnan(weight):
                weight_match = False
                if preferences.weight_preference == "light" and weight < 70:
                    weight_match = True
                elif preferences.weight_preference == "medium" and 70 <= weight <= 90:
                    weight_match = True
                elif preferences.weight_preference == "heavy" and weight > 90:
                    weight_match = True
                
                if weight_match:
                    reasons.append(f"Matches your {preferences.weight_preference} weight preference ({weight}g)")
        
        # Check wireless preference
        if preferences.wireless_preference is not None and 'wireless' in mouse_data:
            if mouse_data['wireless'] == preferences.wireless_preference:
                conn_type = "wireless" if preferences.wireless_preference else "wired"
                reasons.append(f"Matches your {conn_type} preference")
        
        # Check genre
        if preferences.genre and 'genre' in mouse_data:
            genre_info = str(mouse_data['genre']).lower()
            if preferences.genre.value in genre_info:
                reasons.append(f"Optimized for {preferences.genre.value} gaming")
        
        # Add similarity score
        reasons.append(f"High compatibility score: {score:.1%}")
        
        return ". ".join(reasons) if reasons else "Good match based on your overall preferences"
    
    async def get_visualization_data(self, include_user_point: bool = False) -> VisualizationResponse:
        """Get 2D embedding visualization of all mice"""
        mouse_embeddings = self._get_mouse_embeddings()
        
        # Apply UMAP for dimensionality reduction
        if self._reduced_embeddings is None or self._umap_reducer is None:
            self._umap_reducer = umap.UMAP(
                n_neighbors=settings.UMAP_N_NEIGHBORS,
                min_dist=settings.UMAP_MIN_DIST,
                n_components=settings.UMAP_N_COMPONENTS,
                random_state=42
            )
            self._reduced_embeddings = self._umap_reducer.fit_transform(mouse_embeddings)
        
        # Build visualization points
        mice = self.data_loader.get_mice_list()
        mouse_points = []
        
        for i, (x, y) in enumerate(self._reduced_embeddings):
            mouse_data = mice[i]
            mouse_points.append(EmbeddingPoint(
                x=float(x),
                y=float(y),
                mouse_name=mouse_data.get('name', 'Unknown')
            ))
        
        return VisualizationResponse(
            mouse_points=mouse_points,
            user_point=None,
            recommended_points=None
        )
    
    async def get_visualization_with_user(self, preferences: UserPreferences) -> VisualizationResponse:
        """Get visualization including user preference point and recommendations"""
        # Get base visualization
        viz_data = await self.get_visualization_data()
        
        # Generate user embedding and transform it
        user_embedding = self.embedding_service.generate_user_embedding(preferences)
        
        if self._umap_reducer is not None:
            user_2d = self._umap_reducer.transform(user_embedding.reshape(1, -1))[0]
            viz_data.user_point = EmbeddingPoint(
                x=float(user_2d[0]),
                y=float(user_2d[1]),
                mouse_name="Your Preferences"
            )
        
        # Get recommendations
        recommendations = await self.recommend(preferences, top_k=settings.TOP_K_RECOMMENDATIONS)
        
        # Find corresponding points for recommended mice
        if recommendations and self._reduced_embeddings is not None:
            mice = self.data_loader.get_mice_list()
            recommended_points = []
            
            for rec in recommendations:
                # Find index of this mouse
                for i, mouse in enumerate(mice):
                    if mouse.get('name') == rec.mouse.name:
                        x, y = self._reduced_embeddings[i]
                        recommended_points.append(EmbeddingPoint(
                            x=float(x),
                            y=float(y),
                            mouse_name=rec.mouse.name
                        ))
                        break
            
            viz_data.recommended_points = recommended_points
        
        return viz_data


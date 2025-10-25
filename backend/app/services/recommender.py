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
    
    def _apply_hard_filters(self, preferences: UserPreferences) -> Optional[np.ndarray]:
        """
        Apply hard filters (non-negotiable requirements) and return valid indices.
        
        Hard filters:
        1. Price (budget_min, budget_max)
        2. Connectivity (wireless_preference)
        """
        mice = self.data_loader.get_mice_list()
        valid_indices = []
        
        # Check if any hard filters are specified
        has_filters = (
            preferences.budget_min is not None or 
            preferences.budget_max is not None or
            preferences.wireless_preference is not None
        )
        
        if not has_filters:
            return None  # No filters, return all mice
        
        print(f"[HARD FILTERS] Applying hard filters...")
        if preferences.budget_min or preferences.budget_max:
            print(f"  - Budget: ${preferences.budget_min or 0} - ${preferences.budget_max or 'any'}")
        if preferences.wireless_preference is not None:
            print(f"  - Connection: {'Wireless' if preferences.wireless_preference else 'Wired'}")
        
        filtered_count = 0
        for i, mouse in enumerate(mice):
            mouse_name = mouse.get('Name', 'Unknown')
            
            # FILTER 1: Budget (Price)
            if preferences.budget_min is not None or preferences.budget_max is not None:
                price = mouse.get('Price')
                if price is None or np.isnan(price):
                    filtered_count += 1
                    continue
                
                if preferences.budget_min is not None and price < preferences.budget_min:
                    filtered_count += 1
                    continue
                if preferences.budget_max is not None and price > preferences.budget_max:
                    filtered_count += 1
                    continue
            
            # FILTER 2: Connectivity (Wireless/Wired)
            if preferences.wireless_preference is not None:
                connectivity = mouse.get('Connectivity')
                is_wireless = connectivity == 'Wireless' if connectivity else None
                
                if is_wireless is None:
                    filtered_count += 1
                    continue
                
                if preferences.wireless_preference and not is_wireless:
                    filtered_count += 1
                    continue
                if not preferences.wireless_preference and is_wireless:
                    filtered_count += 1
                    continue
            
            # Mouse passed all filters
            valid_indices.append(i)
        
        print(f"[HARD FILTERS] {len(valid_indices)} mice passed, {filtered_count} filtered out (total: {len(mice)})")
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
        
        # Apply hard filters (budget, connectivity, etc.)
        valid_indices = self._apply_hard_filters(preferences)
        
        if valid_indices is not None and len(valid_indices) == 0:
            # No mice match hard filter constraints
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
            
            # Convert to MouseInfo schema (CSV columns are capitalized)
            # Helper function to handle NaN values
            import pandas as pd
            def get_value(data, key, default=None):
                val = data.get(key, default)
                # Handle pandas NaN/None/empty strings using pd.isna which works for all types
                if pd.isna(val) or val == '' or val is None:
                    return default
                return val
            
            mouse_info = MouseInfo(
                name=get_value(mouse_data, 'Name', 'Unknown'),
                brand=get_value(mouse_data, 'Brand', 'Unknown'),
                price=get_value(mouse_data, 'Price'),
                weight=get_value(mouse_data, 'Weight (grams)'),
                dpi_max=get_value(mouse_data, 'DPI'),
                wireless=mouse_data.get('Connectivity') == 'Wireless' if get_value(mouse_data, 'Connectivity') else None,
                shape=get_value(mouse_data, 'Shape'),
                sensor=get_value(mouse_data, 'Sensor'),
                url=get_value(mouse_data, 'Price_URL')
            )
            
            reasoning = None
            if include_reasoning:
                reasoning = self._generate_reasoning(mouse_data, preferences, score)
            
            recommendations.append(MouseRecommendation(
                mouse=mouse_info,
                score=float(score),
                reasoning=reasoning
            ))
        
        return recommendations
    
    def _generate_reasoning(self, mouse_data: dict, preferences: UserPreferences, 
                          score: float) -> str:
        """Generate simple rule-based reasoning for recommendation"""
        reasons = []
        
        # Check weight preference (CSV column: "Weight (grams)")
        if preferences.weight_preference and 'Weight (grams)' in mouse_data:
            weight = mouse_data['Weight (grams)']
            if weight and not np.isnan(weight):
                weight_match = False
                if preferences.weight_preference == "light" and weight < 65:
                    weight_match = True
                elif preferences.weight_preference == "medium" and 65 <= weight <= 85:
                    weight_match = True
                elif preferences.weight_preference == "heavy" and weight > 85:
                    weight_match = True
                
                if weight_match:
                    reasons.append(f"Matches your {preferences.weight_preference} weight preference ({weight}g)")
        
        # Check wireless preference (CSV column: "Connectivity")
        if preferences.wireless_preference is not None and 'Connectivity' in mouse_data:
            is_wireless = mouse_data['Connectivity'] == 'Wireless'
            if is_wireless == preferences.wireless_preference:
                conn_type = "wireless" if preferences.wireless_preference else "wired"
                reasons.append(f"Matches your {conn_type} preference")
        
        # Check genre (not in CSV currently, skip for now)
        # if preferences.genre and 'genre' in mouse_data:
        #     genre_info = str(mouse_data['genre']).lower()
        #     if preferences.genre.value in genre_info:
        #         reasons.append(f"Optimized for {preferences.genre.value} gaming")
        
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


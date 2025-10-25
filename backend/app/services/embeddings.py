"""
Embedding Service
Generates vector embeddings for mice and user preferences
"""
import numpy as np
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.models.schemas import UserPreferences


class EmbeddingService:
    """Handles embedding generation and caching"""
    
    def __init__(self):
        self.model = None
        self._mouse_embeddings_cache: Optional[Dict[str, np.ndarray]] = None
    
    def load_model(self):
        """Lazy load the embedding model"""
        if self.model is None:
            print(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            print("Embedding model loaded successfully")
    
    def generate_text_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        self.load_model()
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def generate_batch_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        self.load_model()
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return embeddings
    
    def mouse_to_text(self, mouse: Dict[str, Any]) -> str:
        """
        Convert mouse data to descriptive text for embedding
        
        Combines all relevant features into a semantic text representation
        """
        parts = []
        
        # Basic info
        if 'name' in mouse:
            parts.append(f"Mouse: {mouse['name']}")
        if 'brand' in mouse:
            parts.append(f"Brand: {mouse['brand']}")
        
        # Physical properties
        if 'weight' in mouse and pd.notna(mouse['weight']):
            weight = float(mouse['weight'])
            weight_desc = "lightweight" if weight < 70 else "medium weight" if weight < 90 else "heavy"
            parts.append(f"Weight: {weight}g ({weight_desc})")
        
        if 'shape' in mouse and pd.notna(mouse['shape']):
            parts.append(f"Shape: {mouse['shape']}")
        
        # Performance
        if 'dpi_max' in mouse and pd.notna(mouse['dpi_max']):
            parts.append(f"Max DPI: {mouse['dpi_max']}")
        
        if 'sensor' in mouse and pd.notna(mouse['sensor']):
            parts.append(f"Sensor: {mouse['sensor']}")
        
        # Connectivity
        if 'wireless' in mouse and pd.notna(mouse['wireless']):
            conn = "Wireless" if mouse['wireless'] else "Wired"
            parts.append(f"Connection: {conn}")
        
        # Grip compatibility
        if 'grip_compatibility' in mouse and pd.notna(mouse['grip_compatibility']):
            parts.append(f"Grip types: {mouse['grip_compatibility']}")
        
        # Genre suitability
        if 'genre' in mouse and pd.notna(mouse['genre']):
            parts.append(f"Best for: {mouse['genre']}")
        
        return ". ".join(parts)
    
    def preferences_to_text(self, preferences: UserPreferences) -> str:
        """
        Convert user preferences to descriptive text for embedding
        """
        parts = []
        
        if preferences.hand_size:
            parts.append(f"Hand size: {preferences.hand_size}")
        
        if preferences.grip_type:
            parts.append(f"Grip type: {preferences.grip_type}")
        
        if preferences.genre:
            parts.append(f"Gaming genre: {preferences.genre}")
        
        if preferences.sensitivity:
            parts.append(f"Sensitivity: {preferences.sensitivity}")
        
        if preferences.weight_preference:
            parts.append(f"Weight preference: {preferences.weight_preference}")
        
        if preferences.wireless_preference is not None:
            conn_pref = "Wireless preferred" if preferences.wireless_preference else "Wired preferred"
            parts.append(conn_pref)
        
        if preferences.budget_min or preferences.budget_max:
            budget_parts = []
            if preferences.budget_min:
                budget_parts.append(f"minimum ${preferences.budget_min}")
            if preferences.budget_max:
                budget_parts.append(f"maximum ${preferences.budget_max}")
            parts.append(f"Budget: {' to '.join(budget_parts)}")
        
        if preferences.additional_notes:
            parts.append(preferences.additional_notes)
        
        if not parts:
            return "General gaming mouse for all purposes"
        
        return ". ".join(parts)
    
    def generate_mouse_embeddings(self, mice: List[Dict[str, Any]], 
                                  force_regenerate: bool = False) -> np.ndarray:
        """
        Generate embeddings for all mice in dataset
        
        Caches results to avoid recomputation
        """
        cache_file = settings.CACHE_DIR / "mouse_embeddings.npy"
        cache_meta_file = settings.CACHE_DIR / "mouse_embeddings_meta.json"
        
        # Try to load from cache
        if not force_regenerate and cache_file.exists() and cache_meta_file.exists():
            try:
                embeddings = np.load(cache_file)
                with open(cache_meta_file, 'r') as f:
                    meta = json.load(f)
                
                if meta.get('count') == len(mice) and meta.get('model') == settings.EMBEDDING_MODEL:
                    print(f"Loaded {len(embeddings)} mouse embeddings from cache")
                    return embeddings
            except Exception as e:
                print(f"Cache load failed: {e}. Regenerating embeddings...")
        
        # Generate new embeddings
        print("Generating mouse embeddings...")
        texts = [self.mouse_to_text(mouse) for mouse in mice]
        embeddings = self.generate_batch_embeddings(texts)
        
        # Save to cache
        try:
            np.save(cache_file, embeddings)
            with open(cache_meta_file, 'w') as f:
                json.dump({
                    'count': len(mice),
                    'model': settings.EMBEDDING_MODEL,
                    'dimension': embeddings.shape[1]
                }, f)
            print("Mouse embeddings cached successfully")
        except Exception as e:
            print(f"Failed to cache embeddings: {e}")
        
        return embeddings
    
    def generate_user_embedding(self, preferences: UserPreferences) -> np.ndarray:
        """Generate embedding for user preferences"""
        text = self.preferences_to_text(preferences)
        return self.generate_text_embedding(text)


# Import pandas for notna checks
import pandas as pd


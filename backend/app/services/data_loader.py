"""
Data Loader Service
Loads and manages mouse dataset
"""
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.core.config import settings


class DataLoader:
    """Loads and caches mouse dataset"""
    
    def __init__(self):
        self._data: Optional[pd.DataFrame] = None
        self._mice_list: Optional[List[Dict[str, Any]]] = None
    
    def load_data(self) -> pd.DataFrame:
        """Load mouse dataset from CSV"""
        if self._data is None:
            try:
                self._data = pd.read_csv(settings.DATASET_PATH)
                print(f"Loaded {len(self._data)} mice from dataset")
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Dataset not found at {settings.DATASET_PATH}. "
                    "Please ensure the data file exists."
                )
        return self._data
    
    def get_mice_list(self) -> List[Dict[str, Any]]:
        """Get mice as list of dictionaries"""
        if self._mice_list is None:
            df = self.load_data()
            self._mice_list = df.to_dict('records')
        return self._mice_list
    
    def get_mouse_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get specific mouse by name"""
        mice = self.get_mice_list()
        for mouse in mice:
            if mouse.get('name', '').lower() == name.lower():
                return mouse
        return None
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get dataset statistics and info"""
        df = self.load_data()
        return {
            "total_mice": len(df),
            "columns": list(df.columns),
            "brands": df['brand'].nunique() if 'brand' in df.columns else 0,
            "price_range": {
                "min": float(df['price'].min()) if 'price' in df.columns else None,
                "max": float(df['price'].max()) if 'price' in df.columns else None,
            } if 'price' in df.columns else None
        }
    
    def filter_by_budget(self, budget_min: Optional[float] = None, 
                        budget_max: Optional[float] = None) -> pd.DataFrame:
        """Filter mice by budget constraints"""
        df = self.load_data()
        
        if 'price' not in df.columns:
            return df
        
        # Filter out NaN prices
        df_filtered = df[df['price'].notna()]
        
        if budget_min is not None:
            df_filtered = df_filtered[df_filtered['price'] >= budget_min]
        
        if budget_max is not None:
            df_filtered = df_filtered[df_filtered['price'] <= budget_max]
        
        return df_filtered
    
    def reload_data(self):
        """Force reload of dataset"""
        self._data = None
        self._mice_list = None
        self.load_data()


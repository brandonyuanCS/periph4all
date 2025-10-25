"""
Generate Embeddings for Mouse Dataset

This script:
1. Loads the FINAL.csv dataset
2. Converts each mouse to descriptive text
3. Generates vector embeddings using SentenceTransformers
4. Saves embeddings and metadata to cache directory

Usage:
    python generate_embeddings.py [--model MODEL_NAME] [--force]
"""

import sys
import argparse
import json
from pathlib import Path

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.config import settings


def mouse_to_text(mouse: dict) -> str:
    """
    Convert mouse data to descriptive text for embedding
    
    Creates a rich semantic representation combining all relevant features
    """
    parts = []
    
    # Basic info
    if 'Name' in mouse and pd.notna(mouse['Name']):
        parts.append(f"Mouse: {mouse['Name']}")
    
    if 'Brand' in mouse and pd.notna(mouse['Brand']):
        parts.append(f"Brand: {mouse['Brand']}")
    
    # Physical properties
    if 'Weight (grams)' in mouse and pd.notna(mouse['Weight (grams)']):
        weight = float(mouse['Weight (grams)'])
        if weight < 40:
            weight_desc = "ultra-lightweight"
        elif weight < 65:
            weight_desc = "lightweight"
        elif weight < 85:
            weight_desc = "medium weight"
        else:
            weight_desc = "heavy"
        parts.append(f"Weight: {weight}g ({weight_desc})")
    
    # Dimensions
    if 'Length (mm)' in mouse and pd.notna(mouse['Length (mm)']):
        parts.append(f"Length: {mouse['Length (mm)']}mm")
    
    if 'Width (mm)' in mouse and pd.notna(mouse['Width (mm)']):
        parts.append(f"Width: {mouse['Width (mm)']}mm")
    
    if 'Height (mm)' in mouse and pd.notna(mouse['Height (mm)']):
        parts.append(f"Height: {mouse['Height (mm)']}mm")
    
    # Shape characteristics
    if 'Shape' in mouse and pd.notna(mouse['Shape']):
        parts.append(f"Shape: {mouse['Shape']}")
    
    if 'Hand compatibility' in mouse and pd.notna(mouse['Hand compatibility']):
        parts.append(f"Hand compatibility: {mouse['Hand compatibility']}")
    
    if 'Hump placement' in mouse and pd.notna(mouse['Hump placement']):
        parts.append(f"Hump: {mouse['Hump placement']}")
    
    if 'Front flare' in mouse and pd.notna(mouse['Front flare']):
        parts.append(f"Front flare: {mouse['Front flare']}")
    
    if 'Side curvature' in mouse and pd.notna(mouse['Side curvature']):
        parts.append(f"Side curvature: {mouse['Side curvature']}")
    
    # Grip features
    if 'Thumb rest' in mouse and pd.notna(mouse['Thumb rest']):
        if str(mouse['Thumb rest']).lower() == 'yes':
            parts.append("Has thumb rest")
    
    if 'Ring finger rest' in mouse and pd.notna(mouse['Ring finger rest']):
        if str(mouse['Ring finger rest']).lower() == 'yes':
            parts.append("Has ring finger rest")
    
    # Performance specs
    if 'Sensor' in mouse and pd.notna(mouse['Sensor']):
        parts.append(f"Sensor: {mouse['Sensor']}")
    
    if 'Sensor type' in mouse and pd.notna(mouse['Sensor type']):
        parts.append(f"Sensor type: {mouse['Sensor type']}")
    
    if 'DPI' in mouse and pd.notna(mouse['DPI']):
        parts.append(f"Max DPI: {mouse['DPI']}")
    
    if 'Polling rate (Hz)' in mouse and pd.notna(mouse['Polling rate (Hz)']):
        parts.append(f"Polling rate: {mouse['Polling rate (Hz)']}Hz")
    
    if 'Tracking speed (IPS)' in mouse and pd.notna(mouse['Tracking speed (IPS)']):
        parts.append(f"Tracking speed: {mouse['Tracking speed (IPS)']} IPS")
    
    # Connectivity
    if 'Connectivity' in mouse and pd.notna(mouse['Connectivity']):
        parts.append(f"Connection: {mouse['Connectivity']}")
    
    # Buttons
    if 'Side buttons' in mouse and pd.notna(mouse['Side buttons']):
        parts.append(f"Side buttons: {mouse['Side buttons']}")
    
    # Switches
    if 'Switches' in mouse and pd.notna(mouse['Switches']):
        parts.append(f"Switches: {mouse['Switches']}")
    
    if 'Switches brand' in mouse and pd.notna(mouse['Switches brand']):
        parts.append(f"Switch brand: {mouse['Switches brand']}")
    
    # Material
    if 'Material' in mouse and pd.notna(mouse['Material']):
        parts.append(f"Material: {mouse['Material']}")
    
    # Price
    if 'Price' in mouse and pd.notna(mouse['Price']):
        price = float(mouse['Price'])
        if price < 50:
            price_desc = "budget-friendly"
        elif price < 100:
            price_desc = "mid-range"
        else:
            price_desc = "premium"
        parts.append(f"Price: ${price} ({price_desc})")
    
    return ". ".join(parts)


def load_dataset(dataset_path: Path) -> pd.DataFrame:
    """Load the mouse dataset from CSV"""
    print(f"Loading dataset from: {dataset_path}")
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
    
    df = pd.read_csv(dataset_path)
    print(f"Loaded {len(df)} mice from dataset")
    print(f"Columns: {list(df.columns)}")
    
    return df


def generate_embeddings(df: pd.DataFrame, model_name: str, batch_size: int = 32) -> np.ndarray:
    """
    Generate embeddings for all mice in dataset
    
    Args:
        df: DataFrame with mouse data
        model_name: SentenceTransformer model name
        batch_size: Batch size for encoding
    
    Returns:
        numpy array of embeddings (n_mice, embedding_dim)
    """
    print(f"\nLoading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    print(f"Model loaded. Embedding dimension: {model.get_sentence_embedding_dimension()}")
    
    # Convert all mice to text
    print("\nConverting mice to descriptive text...")
    texts = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Generating text"):
        text = mouse_to_text(row.to_dict())
        texts.append(text)
    
    # Generate embeddings
    print(f"\nGenerating embeddings for {len(texts)} mice...")
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True  # Normalize for better cosine similarity
    )
    
    print(f"Embeddings generated: shape {embeddings.shape}")
    
    return embeddings


def save_embeddings(embeddings: np.ndarray, df: pd.DataFrame, model_name: str, 
                   cache_dir: Path):
    """
    Save embeddings and metadata to cache directory
    
    Args:
        embeddings: numpy array of embeddings
        df: DataFrame with mouse data (for validation)
        model_name: Model name used
        cache_dir: Directory to save cache files
    """
    # Ensure cache directory exists
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Save embeddings as numpy array
    embeddings_file = cache_dir / "mouse_embeddings.npy"
    print(f"\nSaving embeddings to: {embeddings_file}")
    np.save(embeddings_file, embeddings)
    
    # Save metadata
    metadata = {
        'count': len(embeddings),
        'model': model_name,
        'dimension': embeddings.shape[1],
        'normalized': True,
        'mouse_names': df['Name'].tolist() if 'Name' in df.columns else [],
        'dataset_columns': list(df.columns)
    }
    
    meta_file = cache_dir / "mouse_embeddings_meta.json"
    print(f"Saving metadata to: {meta_file}")
    with open(meta_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Optionally save text representations for debugging
    texts_file = cache_dir / "mouse_texts.json"
    print(f"Saving text representations to: {texts_file}")
    texts = [mouse_to_text(row.to_dict()) for _, row in df.iterrows()]
    with open(texts_file, 'w') as f:
        json.dump(texts, f, indent=2)
    
    print("\n✅ All files saved successfully!")
    print(f"   - Embeddings: {embeddings_file}")
    print(f"   - Metadata: {meta_file}")
    print(f"   - Texts: {texts_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate embeddings for mouse dataset"
    )
    parser.add_argument(
        '--model',
        type=str,
        default=settings.EMBEDDING_MODEL,
        help=f'SentenceTransformer model name (default: {settings.EMBEDDING_MODEL})'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=32,
        help='Batch size for encoding (default: 32)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force regeneration even if cache exists'
    )
    parser.add_argument(
        '--dataset',
        type=str,
        default=str(settings.DATASET_PATH),
        help=f'Path to dataset CSV (default: {settings.DATASET_PATH})'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Mouse Dataset Embedding Generator")
    print("=" * 60)
    
    # Check if embeddings already exist
    embeddings_file = settings.CACHE_DIR / "mouse_embeddings.npy"
    meta_file = settings.CACHE_DIR / "mouse_embeddings_meta.json"
    
    if embeddings_file.exists() and meta_file.exists() and not args.force:
        print("\n⚠️  Embeddings already exist!")
        print(f"   {embeddings_file}")
        print(f"   {meta_file}")
        
        # Load and show metadata
        with open(meta_file, 'r') as f:
            meta = json.load(f)
        
        print(f"\nExisting embeddings:")
        print(f"   Model: {meta.get('model')}")
        print(f"   Count: {meta.get('count')}")
        print(f"   Dimension: {meta.get('dimension')}")
        
        response = input("\nRegenerate? (y/N): ")
        if response.lower() != 'y':
            print("Aborting. Use --force to skip this prompt.")
            return
    
    try:
        # Load dataset
        dataset_path = Path(args.dataset)
        df = load_dataset(dataset_path)
        
        # Generate embeddings
        embeddings = generate_embeddings(df, args.model, args.batch_size)
        
        # Save results
        save_embeddings(embeddings, df, args.model, settings.CACHE_DIR)
        
        print("\n" + "=" * 60)
        print("✅ Embedding generation complete!")
        print("=" * 60)
        print(f"\nGenerated {len(embeddings)} embeddings")
        print(f"Embedding dimension: {embeddings.shape[1]}")
        print(f"Model used: {args.model}")
        print(f"\nCache directory: {settings.CACHE_DIR}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


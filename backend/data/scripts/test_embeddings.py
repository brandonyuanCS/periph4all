"""
Test and Verify Embeddings

Quick script to test that embeddings are working correctly
and perform basic similarity tests.

Usage:
    python test_embeddings.py
"""

import sys
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.config import settings


def load_embeddings():
    """Load embeddings and metadata from cache"""
    embeddings_file = settings.CACHE_DIR / "mouse_embeddings.npy"
    meta_file = settings.CACHE_DIR / "mouse_embeddings_meta.json"
    
    if not embeddings_file.exists():
        raise FileNotFoundError(
            f"Embeddings not found at {embeddings_file}. "
            "Run generate_embeddings.py first!"
        )
    
    print(f"Loading embeddings from: {embeddings_file}")
    embeddings = np.load(embeddings_file)
    
    print(f"Loading metadata from: {meta_file}")
    with open(meta_file, 'r') as f:
        metadata = json.load(f)
    
    return embeddings, metadata


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_similar_mice(query_embedding, embeddings, mouse_names, top_k=5):
    """Find most similar mice to a query embedding"""
    similarities = []
    
    for i, emb in enumerate(embeddings):
        sim = cosine_similarity(query_embedding, emb)
        similarities.append((i, mouse_names[i], sim))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[2], reverse=True)
    
    return similarities[:top_k]


def test_basic_properties(embeddings, metadata):
    """Test basic properties of embeddings"""
    print("\n" + "=" * 60)
    print("Basic Properties Test")
    print("=" * 60)
    
    print(f"\n✓ Shape: {embeddings.shape}")
    print(f"✓ Number of mice: {metadata['count']}")
    print(f"✓ Embedding dimension: {metadata['dimension']}")
    print(f"✓ Model used: {metadata['model']}")
    print(f"✓ Normalized: {metadata.get('normalized', False)}")
    
    # Check for NaN or Inf
    has_nan = np.any(np.isnan(embeddings))
    has_inf = np.any(np.isinf(embeddings))
    
    if has_nan:
        print("⚠️  Warning: Embeddings contain NaN values!")
    else:
        print("✓ No NaN values")
    
    if has_inf:
        print("⚠️  Warning: Embeddings contain Inf values!")
    else:
        print("✓ No Inf values")
    
    # Check normalization
    if metadata.get('normalized'):
        norms = np.linalg.norm(embeddings, axis=1)
        avg_norm = np.mean(norms)
        print(f"✓ Average norm: {avg_norm:.4f} (should be ~1.0 if normalized)")


def test_similarity_search(embeddings, metadata):
    """Test similarity search with example queries"""
    print("\n" + "=" * 60)
    print("Similarity Search Test")
    print("=" * 60)
    
    mouse_names = metadata.get('mouse_names', [])
    if not mouse_names:
        print("⚠️  No mouse names in metadata, skipping similarity test")
        return
    
    # Load the model
    print(f"\nLoading model: {metadata['model']}")
    model = SentenceTransformer(metadata['model'])
    
    # Test queries
    test_queries = [
        "lightweight wireless mouse for FPS gaming",
        "heavy ergonomic mouse with many buttons for MMO",
        "small compact mouse for claw grip",
        "budget-friendly mouse under 50 dollars",
        "I want a Razer Viper Mini Signature Edition"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 60)
        
        # Generate query embedding
        query_emb = model.encode(query, normalize_embeddings=True)
        
        # Find similar mice
        similar = find_similar_mice(query_emb, embeddings, mouse_names, top_k=3)
        
        print("Top 3 matches:")
        for rank, (idx, name, score) in enumerate(similar, 1):
            print(f"  {rank}. {name}")
            print(f"     Similarity: {score:.4f}")


def test_mouse_to_mouse_similarity(embeddings, metadata):
    """Test similarity between mice"""
    print("\n" + "=" * 60)
    print("Mouse-to-Mouse Similarity Test")
    print("=" * 60)
    
    mouse_names = metadata.get('mouse_names', [])
    if len(mouse_names) < 2:
        print("⚠️  Not enough mice for comparison")
        return
    
    # Pick first mouse as reference
    ref_idx = 0
    ref_name = mouse_names[ref_idx]
    ref_emb = embeddings[ref_idx]
    
    print(f"\nReference mouse: {ref_name}")
    print("\nFinding most similar mice...")
    
    similar = find_similar_mice(ref_emb, embeddings, mouse_names, top_k=6)
    
    # Skip first result (self-similarity)
    print("\nTop 5 most similar:")
    for rank, (idx, name, score) in enumerate(similar[1:6], 1):
        print(f"  {rank}. {name}")
        print(f"     Similarity: {score:.4f}")


def test_diversity(embeddings):
    """Test diversity of embeddings"""
    print("\n" + "=" * 60)
    print("Diversity Test")
    print("=" * 60)
    
    # Compute pairwise similarities (sample if too large)
    n_samples = min(100, len(embeddings))
    sample_indices = np.random.choice(len(embeddings), n_samples, replace=False)
    sample_embs = embeddings[sample_indices]
    
    print(f"\nComputing pairwise similarities for {n_samples} mice...")
    
    similarities = []
    for i in range(len(sample_embs)):
        for j in range(i + 1, len(sample_embs)):
            sim = cosine_similarity(sample_embs[i], sample_embs[j])
            similarities.append(sim)
    
    similarities = np.array(similarities)
    
    print(f"\nPairwise Similarity Statistics:")
    print(f"  Mean: {np.mean(similarities):.4f}")
    print(f"  Std: {np.std(similarities):.4f}")
    print(f"  Min: {np.min(similarities):.4f}")
    print(f"  Max: {np.max(similarities):.4f}")
    print(f"  Median: {np.median(similarities):.4f}")
    
    # Good diversity means not all mice are too similar
    if np.mean(similarities) > 0.9:
        print("\n⚠️  Warning: High average similarity - embeddings may lack diversity")
    elif np.mean(similarities) < 0.3:
        print("\n⚠️  Warning: Low average similarity - check if embeddings are correct")
    else:
        print("\n✓ Good diversity in embeddings")


def main():
    print("=" * 60)
    print("Embedding Test Suite")
    print("=" * 60)
    
    try:
        # Load embeddings
        embeddings, metadata = load_embeddings()
        
        # Run tests
        test_basic_properties(embeddings, metadata)
        test_similarity_search(embeddings, metadata)
        test_mouse_to_mouse_similarity(embeddings, metadata)
        test_diversity(embeddings)
        
        print("\n" + "=" * 60)
        print("✅ All tests complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


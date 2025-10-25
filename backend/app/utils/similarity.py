"""
Similarity Utilities
Functions for computing vector similarity and ranking
"""
import numpy as np
from typing import Tuple


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Compute cosine similarity between vectors
    
    Args:
        a: Array of shape (n, d) or (d,)
        b: Array of shape (m, d) or (d,)
    
    Returns:
        Similarity scores of shape (n, m) or (n,) or scalar
    """
    # Ensure 2D arrays
    if a.ndim == 1:
        a = a.reshape(1, -1)
    if b.ndim == 1:
        b = b.reshape(1, -1)
    
    # Normalize vectors
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=1, keepdims=True)
    
    # Compute dot product (cosine similarity)
    similarity = np.dot(a_norm, b_norm.T)
    
    return similarity


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Compute Euclidean distance between vectors
    
    Args:
        a: Array of shape (n, d) or (d,)
        b: Array of shape (m, d) or (d,)
    
    Returns:
        Distance scores of shape (n, m) or (n,) or scalar
    """
    if a.ndim == 1:
        a = a.reshape(1, -1)
    if b.ndim == 1:
        b = b.reshape(1, -1)
    
    # Compute pairwise distances
    # Using broadcasting: (n, 1, d) - (1, m, d) = (n, m, d)
    diff = a[:, np.newaxis, :] - b[np.newaxis, :, :]
    distances = np.linalg.norm(diff, axis=2)
    
    return distances


def top_k_similar(similarities: np.ndarray, k: int = 3) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get indices and scores of top K most similar items
    
    Args:
        similarities: Array of similarity scores
        k: Number of top items to return
    
    Returns:
        Tuple of (indices, scores) for top K items
    """
    k = min(k, len(similarities))
    
    # Get indices of top K scores (in descending order)
    top_indices = np.argsort(similarities)[::-1][:k]
    top_scores = similarities[top_indices]
    
    return top_indices, top_scores


def normalize_scores(scores: np.ndarray, method: str = "minmax") -> np.ndarray:
    """
    Normalize scores to [0, 1] range
    
    Args:
        scores: Array of scores
        method: Normalization method ("minmax" or "zscore")
    
    Returns:
        Normalized scores
    """
    if method == "minmax":
        min_score = np.min(scores)
        max_score = np.max(scores)
        if max_score - min_score == 0:
            return np.ones_like(scores)
        return (scores - min_score) / (max_score - min_score)
    
    elif method == "zscore":
        mean = np.mean(scores)
        std = np.std(scores)
        if std == 0:
            return np.zeros_like(scores)
        return (scores - mean) / std
    
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def weighted_similarity(similarities: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """
    Compute weighted combination of multiple similarity scores
    
    Args:
        similarities: Array of shape (n, m) where n is number of similarity types
        weights: Array of shape (n,) with weights for each similarity type
    
    Returns:
        Weighted similarity scores of shape (m,)
    """
    # Normalize weights
    weights = weights / np.sum(weights)
    
    # Compute weighted sum
    weighted = np.dot(weights, similarities)
    
    return weighted


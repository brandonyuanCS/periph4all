"""
Example Usage of Brand Data

Shows how to use brand quality scores and metadata in recommendations.
"""

from app.utils.brand_data import (
    get_brand_info,
    get_brand_quality_score,
    get_premium_brands,
    BrandTier,
    get_brands_by_tier
)


def example_basic_usage():
    """Basic brand info lookup"""
    print("=== Basic Usage ===\n")
    
    # Get brand info
    logitech = get_brand_info("Logitech")
    print(f"Brand: {logitech.name}")
    print(f"Tier: {logitech.tier}")
    print(f"Quality Score: {logitech.quality_score}")
    print(f"Origin: {logitech.origin}")
    print(f"Reputation: {logitech.reputation}")
    print(f"Notes: {logitech.notes}")
    print()
    
    # Quick score lookup
    razer_score = get_brand_quality_score("Razer")
    print(f"Razer quality score: {razer_score}")
    print()


def example_filtering_by_tier():
    """Filter brands by tier"""
    print("=== Filtering by Tier ===\n")
    
    premium = get_premium_brands()
    print(f"Premium brands: {', '.join(premium)}")
    print()
    
    high_quality = get_brands_by_tier(BrandTier.HIGH_QUALITY)
    print(f"High-quality brands ({len(high_quality)}):")
    for name, info in high_quality.items():
        print(f"  - {name}: {info.quality_score}")
    print()


def example_weighted_recommendation():
    """Example: Weight recommendations by brand quality"""
    print("=== Weighted Recommendation Example ===\n")
    
    # Simulated recommendation scores
    candidates = [
        {"name": "Logitech G Pro", "brand": "Logitech", "similarity": 0.85},
        {"name": "ATK F1 Pro", "brand": "ATK", "similarity": 0.90},
        {"name": "Pulsar X2", "brand": "Pulsar", "similarity": 0.87},
    ]
    
    print("Original scores (similarity only):")
    for mouse in candidates:
        print(f"  {mouse['name']}: {mouse['similarity']:.2f}")
    print()
    
    # Apply brand quality weighting
    weighted_scores = []
    for mouse in candidates:
        brand_score = get_brand_quality_score(mouse['brand'])
        # Weighted: 70% similarity, 30% brand quality
        final_score = 0.7 * mouse['similarity'] + 0.3 * brand_score
        weighted_scores.append({
            **mouse,
            'brand_score': brand_score,
            'final_score': final_score
        })
    
    # Sort by final score
    weighted_scores.sort(key=lambda x: x['final_score'], reverse=True)
    
    print("Weighted scores (70% similarity + 30% brand quality):")
    for mouse in weighted_scores:
        print(f"  {mouse['name']}:")
        print(f"    Similarity: {mouse['similarity']:.2f}")
        print(f"    Brand Quality: {mouse['brand_score']:.2f}")
        print(f"    Final Score: {mouse['final_score']:.2f}")
    print()


def example_brand_filtering():
    """Example: Filter out low-quality brands"""
    print("=== Brand Filtering Example ===\n")
    
    # Simulated mice
    mice = [
        {"name": "Mouse A", "brand": "Logitech", "price": 150},
        {"name": "Mouse B", "brand": "EWEADN", "price": 30},
        {"name": "Mouse C", "brand": "Pulsar", "price": 130},
        {"name": "Mouse D", "brand": "AJAZZ", "price": 25},
    ]
    
    # Filter: Only show brands with quality >= 0.5
    min_quality = 0.5
    filtered = [
        m for m in mice 
        if get_brand_quality_score(m['brand']) >= min_quality
    ]
    
    print(f"Mice with brand quality >= {min_quality}:")
    for mouse in filtered:
        score = get_brand_quality_score(mouse['brand'])
        print(f"  {mouse['name']} ({mouse['brand']}): Quality {score:.2f}")
    print()


def example_budget_recommendations():
    """Example: Recommend best budget brands"""
    print("=== Budget Brand Recommendations ===\n")
    
    budget_tier = get_brands_by_tier(BrandTier.BUDGET)
    mid_tier = get_brands_by_tier(BrandTier.MID_TIER)
    
    # Sort by quality score
    budget_sorted = sorted(budget_tier.items(), 
                          key=lambda x: x[1].quality_score, 
                          reverse=True)
    
    print("Best budget brands (sorted by quality):")
    for name, info in budget_sorted[:5]:
        print(f"  {name}: {info.quality_score:.2f} - {info.reputation}")
    print()
    
    print("Best mid-tier brands for value:")
    mid_sorted = sorted(mid_tier.items(), 
                       key=lambda x: x[1].quality_score, 
                       reverse=True)
    for name, info in mid_sorted[:5]:
        print(f"  {name}: {info.quality_score:.2f} - {info.reputation}")
    print()


if __name__ == "__main__":
    example_basic_usage()
    example_filtering_by_tier()
    example_weighted_recommendation()
    example_brand_filtering()
    example_budget_recommendations()


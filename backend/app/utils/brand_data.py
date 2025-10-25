"""
Brand Quality and Metadata Mapping

Contains brand information including quality ratings, tier classifications,
and other metadata for all mouse brands in the dataset.
"""

from typing import Dict, Optional
from enum import Enum


class BrandTier(str, Enum):
    """Brand tier classifications"""
    PREMIUM = "premium"           # Top-tier, established brands
    HIGH_QUALITY = "high_quality" # Strong reputation, enthusiast-grade
    MID_TIER = "mid_tier"         # Good value, decent quality
    BUDGET = "budget"             # Budget-friendly, less established


class BrandInfo:
    """Brand metadata"""
    def __init__(
        self,
        name: str,
        tier: BrandTier,
        quality_score: float,  # 0.0 to 1.0
        origin: str,
        reputation: str,
        notes: str = ""
    ):
        self.name = name
        self.tier = tier
        self.quality_score = quality_score
        self.origin = origin
        self.reputation = reputation
        self.notes = notes


# Brand Quality Mapping
# Quality Score: 1.0 = Premium, 0.75 = High Quality, 0.5 = Mid-tier, 0.25 = Budget
BRAND_DATA: Dict[str, BrandInfo] = {
    # PREMIUM TIER (0.85 - 1.0)
    "Logitech": BrandInfo(
        name="Logitech",
        tier=BrandTier.PREMIUM,
        quality_score=1.0,
        origin="Switzerland/USA",
        reputation="Industry leader, excellent build quality and sensors",
        notes="G Pro series is esports standard"
    ),
    
    "Razer": BrandInfo(
        name="Razer",
        tier=BrandTier.PREMIUM,
        quality_score=0.95,
        origin="USA/Singapore",
        reputation="Premium gaming brand, iconic designs",
        notes="Viper series highly regarded"
    ),
    
    "Endgame": BrandInfo(
        name="Endgame",
        tier=BrandTier.PREMIUM,
        quality_score=0.90,
        origin="Germany",
        reputation="High-end enthusiast brand, exceptional quality",
        notes="OP1 8K is considered one of the best"
    ),
    
    "Glorious": BrandInfo(
        name="Glorious",
        tier=BrandTier.PREMIUM,
        quality_score=0.88,
        origin="USA",
        reputation="Enthusiast favorite, great value at premium level",
        notes="Model O series very popular"
    ),
    
    # HIGH QUALITY TIER (0.65 - 0.84)
    "Pulsar": BrandInfo(
        name="Pulsar",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.84,
        origin="Singapore",
        reputation="Rising enthusiast brand, excellent lightweight designs",
        notes="X2 series highly praised"
    ),
    
    "LAMZU": BrandInfo(
        name="LAMZU",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.82,
        origin="China",
        reputation="High-quality enthusiast brand, innovative shapes",
        notes="Atlantis and Thorn are popular"
    ),
    
    "Corsair": BrandInfo(
        name="Corsair",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.80,
        origin="USA",
        reputation="Established gaming peripherals brand",
        notes="Reliable but less innovative than competitors"
    ),
    
    "ASUS": BrandInfo(
        name="ASUS",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.78,
        origin="Taiwan",
        reputation="ROG series has strong reputation",
        notes="Premium pricing, solid quality"
    ),
    
    "Ninjutso": BrandInfo(
        name="Ninjutso",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.76,
        origin="USA",
        reputation="Boutique enthusiast brand, unique shapes",
        notes="Sora and Origin One are well-regarded"
    ),
    
    "VGN": BrandInfo(
        name="VGN",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.75,
        origin="China",
        reputation="Growing enthusiast brand, good quality control",
        notes="Dragonfly series popular in Asia"
    ),
    
    "G-Wolves": BrandInfo(
        name="G-Wolves",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.74,
        origin="China",
        reputation="Modding community favorite, innovative",
        notes="Hati series is iconic"
    ),
    
    "HyperX": BrandInfo(
        name="HyperX",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.72,
        origin="USA (Kingston)",
        reputation="Reliable gaming peripherals, good warranty",
        notes="Safe choice, less cutting-edge"
    ),
    
    "ROCCAT": BrandInfo(
        name="ROCCAT",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.70,
        origin="Germany",
        reputation="German engineering, unique features",
        notes="Kone series has loyal fanbase"
    ),
    
    "Pwnage": BrandInfo(
        name="Pwnage",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.68,
        origin="USA",
        reputation="Customizable, modular designs",
        notes="StormBreaker has swappable shells"
    ),
    
    "WLmouse": BrandInfo(
        name="WLmouse",
        tier=BrandTier.HIGH_QUALITY,
        quality_score=0.66,
        origin="China",
        reputation="Boutique brand, innovative materials",
        notes="Beast series uses magnesium alloy"
    ),
    
    # MID-TIER (0.45 - 0.64)
    "Keychron": BrandInfo(
        name="Keychron",
        tier=BrandTier.MID_TIER,
        quality_score=0.64,
        origin="China",
        reputation="Known for keyboards, mice are decent value",
        notes="Good budget option with modern features"
    ),
    
    "Darmoshark": BrandInfo(
        name="Darmoshark",
        tier=BrandTier.MID_TIER,
        quality_score=0.60,
        origin="China",
        reputation="Newer brand, competitive specs for price",
        notes="M3 and M2 series offer good value"
    ),
    
    "Dareu": BrandInfo(
        name="Dareu",
        tier=BrandTier.MID_TIER,
        quality_score=0.58,
        origin="China",
        reputation="Popular in Asia, budget-friendly",
        notes="A3 series is well-reviewed"
    ),
    
    "VXE": BrandInfo(
        name="VXE",
        tier=BrandTier.MID_TIER,
        quality_score=0.56,
        origin="China",
        reputation="Budget enthusiast brand, decent quality",
        notes="R1 Pro is popular value option"
    ),
    
    "Fantech": BrandInfo(
        name="Fantech",
        tier=BrandTier.MID_TIER,
        quality_score=0.54,
        origin="China/Indonesia",
        reputation="Budget gaming brand, widely available",
        notes="Hit or miss quality control"
    ),
    
    "Valkyrie": BrandInfo(
        name="Valkyrie",
        tier=BrandTier.MID_TIER,
        quality_score=0.52,
        origin="China",
        reputation="Boutique-style brand, limited availability",
        notes="Small batch production"
    ),
    
    "Kysona": BrandInfo(
        name="Kysona",
        tier=BrandTier.MID_TIER,
        quality_score=0.50,
        origin="China",
        reputation="Lesser known, decent specs",
        notes="M600 series available"
    ),
    
    "Delux": BrandInfo(
        name="Delux",
        tier=BrandTier.MID_TIER,
        quality_score=0.48,
        origin="China",
        reputation="Budget brand, basic quality",
        notes="Very affordable but inconsistent"
    ),
    
    # BUDGET TIER (0.25 - 0.44)
    "ATK": BrandInfo(
        name="ATK",
        tier=BrandTier.BUDGET,
        quality_score=0.44,
        origin="China",
        reputation="Budget Chinese brand, aggressive pricing",
        notes="Good specs on paper, quality varies"
    ),
    
    "Attack": BrandInfo(
        name="Attack",
        tier=BrandTier.BUDGET,
        quality_score=0.42,
        origin="China",
        reputation="Budget brand (Attack Shark series)",
        notes="Popular for ultra-budget wireless"
    ),
    
    "AJAZZ": BrandInfo(
        name="AJAZZ",
        tier=BrandTier.BUDGET,
        quality_score=0.40,
        origin="China",
        reputation="Budget peripherals brand",
        notes="Very affordable, basic quality"
    ),
    
    "MCHOSE": BrandInfo(
        name="MCHOSE",
        tier=BrandTier.BUDGET,
        quality_score=0.38,
        origin="China",
        reputation="Budget brand, limited reviews",
        notes="A5 Pro and X6 series available"
    ),
    
    "Incott": BrandInfo(
        name="Incott",
        tier=BrandTier.BUDGET,
        quality_score=0.35,
        origin="China",
        reputation="Lesser known budget brand",
        notes="Limited information available"
    ),
    
    "EWEADN": BrandInfo(
        name="EWEADN",
        tier=BrandTier.BUDGET,
        quality_score=0.32,
        origin="China",
        reputation="Obscure brand, minimal presence",
        notes="Very limited reviews"
    ),
    
    "Waizowl": BrandInfo(
        name="Waizowl",
        tier=BrandTier.BUDGET,
        quality_score=0.30,
        origin="China",
        reputation="Budget brand, minimal information",
        notes="OG and ZL series mentioned"
    ),
}


# Simple quality score lookup (for backwards compatibility)
BRAND_QUALITY_SCORES: Dict[str, float] = {
    brand: info.quality_score for brand, info in BRAND_DATA.items()
}


def get_brand_info(brand_name: str) -> Optional[BrandInfo]:
    """
    Get brand information by name (case-insensitive)
    
    Args:
        brand_name: Brand name to lookup
    
    Returns:
        BrandInfo object or None if not found
    """
    # Try exact match first
    if brand_name in BRAND_DATA:
        return BRAND_DATA[brand_name]
    
    # Try case-insensitive match
    brand_lower = brand_name.lower()
    for key, info in BRAND_DATA.items():
        if key.lower() == brand_lower:
            return info
    
    return None


def get_brand_quality_score(brand_name: str, default: float = 0.5) -> float:
    """
    Get brand quality score (0.0 to 1.0)
    
    Args:
        brand_name: Brand name
        default: Default score if brand not found
    
    Returns:
        Quality score between 0.0 and 1.0
    """
    info = get_brand_info(brand_name)
    return info.quality_score if info else default


def get_brands_by_tier(tier: BrandTier) -> Dict[str, BrandInfo]:
    """
    Get all brands in a specific tier
    
    Args:
        tier: BrandTier enum value
    
    Returns:
        Dictionary of brand names to BrandInfo objects
    """
    return {
        name: info for name, info in BRAND_DATA.items()
        if info.tier == tier
    }


def get_premium_brands() -> list[str]:
    """Get list of premium brand names"""
    return [name for name, info in BRAND_DATA.items() 
            if info.tier == BrandTier.PREMIUM]


def get_budget_brands() -> list[str]:
    """Get list of budget brand names"""
    return [name for name, info in BRAND_DATA.items() 
            if info.tier == BrandTier.BUDGET]


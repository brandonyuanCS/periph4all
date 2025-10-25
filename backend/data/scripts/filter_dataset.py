"""
Filter dataset to high-performance mainstream gaming mice.

Rules:
1. Remove mod/kit brands
2. Remove brands with ≤3 mice
3. Remove low-performance mice
"""
import pandas as pd
import sys
from pathlib import Path

# Input/Output paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "backend" / "data"
INPUT_CSV = DATA_DIR / "initial_data.csv"
OUTPUT_CSV = DATA_DIR / "filtered_data.csv"


def filter_dataset(input_csv, output_csv):
    """
    Filter dataset based on specified rules.
    
    Args:
        input_csv: Path to input CSV
        output_csv: Path to output CSV
    
    Returns:
        Filtered DataFrame
    """
    print("="*70)
    print("DATASET FILTERING")
    print("="*70)
    print(f"Reading: {input_csv}")
    
    df = pd.read_csv(input_csv)
    initial_count = len(df)
    print(f"Initial dataset: {initial_count} mice\n")
    
    # ========================================
    # RULE 1: Remove mod/kit brands
    # ========================================
    print("[RULE 1] Removing mod/kit brands...")
    mod_brands = ['PMM', 'CryoMods', 'Arbiter', 'Project']
    
    before = len(df)
    df = df[~df['Brand'].isin(mod_brands)]
    removed = before - len(df)
    print(f"  Removed {removed} mice from mod brands")
    print(f"  Remaining: {len(df)} mice\n")
    
    # ========================================
    # RULE 1B: Remove low-reputation brands
    # ========================================
    print("[RULE 1B] Removing brands with weak community consensus...")
    excluded_brands = [
        'Akko', 'Alienware', 'AULA', 'Ausdom', 'CC', 'Cherry', 'Cooler',
        'Dream', 'ELECOM', 'GravaStar', 'IROK', 'Ironcat', 'JamesDonkey',
        'MACHENIKE', 'Noir', 'NZXT', 'Press', 'RAKK', 'RAWM', 'Redragon',
        'Turtle', 'Aigo', 'Arye', 'RK'
    ]
    
    before = len(df)
    df = df[~df['Brand'].isin(excluded_brands)]
    removed = before - len(df)
    print(f"  Removed {removed} mice from {len(excluded_brands)} excluded brands")
    print(f"  Remaining: {len(df)} mice\n")
    
    # ========================================
    # RULE 2: Remove brands with ≤3 mice
    # ========================================
    print("[RULE 2] Removing brands with 3 or fewer mice...")
    
    # Count mice per brand
    brand_counts = df['Brand'].value_counts()
    
    # Brands to keep (>3 mice)
    brands_to_keep = brand_counts[brand_counts > 3].index.tolist()
    
    print(f"  Brands with >3 mice: {len(brands_to_keep)}")
    print(f"  Brands being removed: {len(brand_counts) - len(brands_to_keep)}")
    
    # Show brands being removed
    removed_brands = brand_counts[brand_counts <= 3]
    if len(removed_brands) > 0:
        print(f"\n  Removing these brands:")
        for brand, count in removed_brands.items():
            print(f"    - {brand}: {count} mice")
    
    before = len(df)
    df = df[df['Brand'].isin(brands_to_keep)]
    removed = before - len(df)
    print(f"\n  Removed {removed} mice from small brands")
    print(f"  Remaining: {len(df)} mice\n")
    
    # ========================================
    # RULE 3: Remove low-performance mice
    # ========================================
    print("[RULE 3] Removing low-performance mice...")
    
    # Convert columns to numeric (handle any non-numeric values)
    df['Weight (grams)'] = pd.to_numeric(df['Weight (grams)'], errors='coerce')
    df['DPI'] = pd.to_numeric(df['DPI'], errors='coerce')
    df['Polling rate (Hz)'] = pd.to_numeric(df['Polling rate (Hz)'], errors='coerce')
    df['Tracking speed (IPS)'] = pd.to_numeric(df['Tracking speed (IPS)'], errors='coerce')
    
    # 3a. Weight > 65 grams (ultra-lightweight only)
    print("  [3a] Removing mice with weight > 65g...")
    before = len(df)
    heavy_mice = df[df['Weight (grams)'] > 65]
    if len(heavy_mice) > 0:
        print(f"      Examples being removed:")
        for _, mouse in heavy_mice.head(5).iterrows():
            print(f"        - {mouse['Name']}: {mouse['Weight (grams)']}g")
    
    df = df[df['Weight (grams)'] <= 65]
    removed = before - len(df)
    print(f"      Removed: {removed} mice")
    print(f"      Remaining: {len(df)} mice")
    
    # 3b. DPI < 18000 (high-end sensors only)
    print("\n  [3b] Removing mice with DPI < 18000...")
    before = len(df)
    low_dpi = df[df['DPI'] < 18000]
    if len(low_dpi) > 0:
        print(f"      Examples being removed:")
        for _, mouse in low_dpi.head(5).iterrows():
            print(f"        - {mouse['Name']}: {mouse['DPI']} DPI")
    
    df = df[df['DPI'] >= 18000]
    removed = before - len(df)
    print(f"      Removed: {removed} mice")
    print(f"      Remaining: {len(df)} mice")
    
    # 3c. Polling rate < 1000 Hz
    print("\n  [3c] Removing mice with polling rate < 1000 Hz...")
    before = len(df)
    low_polling = df[df['Polling rate (Hz)'] < 1000]
    if len(low_polling) > 0:
        print(f"      Examples being removed:")
        for _, mouse in low_polling.head(5).iterrows():
            print(f"        - {mouse['Name']}: {mouse['Polling rate (Hz)']} Hz")
    
    df = df[df['Polling rate (Hz)'] >= 1000]
    removed = before - len(df)
    print(f"      Removed: {removed} mice")
    print(f"      Remaining: {len(df)} mice")
    
    # 3d. Tracking speed < 400 IPS (high-performance tracking)
    print("\n  [3d] Removing mice with tracking speed < 400 IPS...")
    before = len(df)
    low_ips = df[df['Tracking speed (IPS)'] < 400]
    if len(low_ips) > 0:
        print(f"      Examples being removed:")
        for _, mouse in low_ips.head(5).iterrows():
            print(f"        - {mouse['Name']}: {mouse['Tracking speed (IPS)']} IPS")
    
    df = df[df['Tracking speed (IPS)'] >= 400]
    removed = before - len(df)
    print(f"      Removed: {removed} mice")
    print(f"      Remaining: {len(df)} mice\n")
    
    # ========================================
    # SAVE RESULTS
    # ========================================
    df.to_csv(output_csv, index=False)
    
    print("="*70)
    print("FILTERING COMPLETE")
    print("="*70)
    print(f"Initial mice: {initial_count}")
    print(f"Final mice: {len(df)}")
    print(f"Reduction: {initial_count - len(df)} mice ({(initial_count - len(df))/initial_count*100:.1f}%)")
    print(f"\nSaved to: {output_csv}")
    
    # ========================================
    # SUMMARY STATISTICS
    # ========================================
    print("\n" + "="*70)
    print("DATASET SUMMARY")
    print("="*70)
    
    print(f"\nTotal mice: {len(df)}")
    
    print(f"\nTop 15 Brands:")
    brand_counts = df['Brand'].value_counts().head(15)
    for brand, count in brand_counts.items():
        print(f"  {brand}: {count}")
    
    print(f"\nSize Distribution:")
    size_counts = df['Size'].value_counts()
    for size, count in size_counts.items():
        print(f"  {size}: {count}")
    
    print(f"\nConnectivity:")
    conn_counts = df['Connectivity'].value_counts()
    for conn, count in conn_counts.items():
        print(f"  {conn}: {count}")
    
    print(f"\nShape:")
    shape_counts = df['Shape'].value_counts()
    for shape, count in shape_counts.items():
        print(f"  {shape}: {count}")
    
    print(f"\nWeight Statistics:")
    print(f"  Min: {df['Weight (grams)'].min()}g")
    print(f"  Max: {df['Weight (grams)'].max()}g")
    print(f"  Mean: {df['Weight (grams)'].mean():.1f}g")
    print(f"  Median: {df['Weight (grams)'].median():.1f}g")
    
    print(f"\nDPI Statistics:")
    print(f"  Min: {df['DPI'].min()}")
    print(f"  Max: {df['DPI'].max()}")
    print(f"  Mean: {df['DPI'].mean():.0f}")
    
    print("\n" + "="*70)
    
    return df


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Filter dataset to high-performance mice')
    parser.add_argument('--input', type=str, help='Input CSV path')
    parser.add_argument('--output', type=str, help='Output CSV path')
    
    args = parser.parse_args()
    
    input_path = Path(args.input) if args.input else INPUT_CSV
    output_path = Path(args.output) if args.output else OUTPUT_CSV
    
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}")
        return 1
    
    filter_dataset(input_path, output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())


"""
Preview Text Representations

Quick script to preview how mice are converted to text for embeddings.
Useful for understanding and tuning the text generation.

Usage:
    python preview_texts.py [--count N]
"""

import sys
import argparse
from pathlib import Path

import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.config import settings

# Import the mouse_to_text function from generate_embeddings
from generate_embeddings import mouse_to_text


def main():
    parser = argparse.ArgumentParser(
        description="Preview mouse text representations"
    )
    parser.add_argument(
        '--count',
        type=int,
        default=5,
        help='Number of mice to preview (default: 5)'
    )
    parser.add_argument(
        '--search',
        type=str,
        help='Search for specific mouse by name'
    )
    
    args = parser.parse_args()
    
    # Load dataset
    print(f"Loading dataset from: {settings.DATASET_PATH}")
    df = pd.read_csv(settings.DATASET_PATH)
    print(f"Loaded {len(df)} mice\n")
    
    if args.search:
        # Search for specific mouse
        mask = df['Name'].str.contains(args.search, case=False, na=False)
        df_filtered = df[mask]
        
        if len(df_filtered) == 0:
            print(f"No mice found matching '{args.search}'")
            return
        
        print(f"Found {len(df_filtered)} mice matching '{args.search}':\n")
        df_display = df_filtered
    else:
        # Show first N mice
        df_display = df.head(args.count)
    
    # Display text representations
    for idx, row in df_display.iterrows():
        mouse_dict = row.to_dict()
        text = mouse_to_text(mouse_dict)
        
        print("=" * 80)
        print(f"Mouse #{idx + 1}: {mouse_dict.get('Name', 'Unknown')}")
        print("=" * 80)
        print(f"\n{text}\n")
        print(f"Character count: {len(text)}")
        print()
    
    print("=" * 80)
    print(f"Displayed {len(df_display)} mice")
    print("=" * 80)


if __name__ == "__main__":
    main()


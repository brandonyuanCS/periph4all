"""
Price scraper using ScraperAPI to avoid getting blocked.
"""
import os
import csv
import requests
from pathlib import Path
from typing import Optional, Dict
from urllib.parse import urlencode, quote_plus
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# Load environment variables from project root
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)
DATA_DIR = PROJECT_ROOT / "backend" / "data"
INPUT_CSV = DATA_DIR / "filtered_data.csv"
OUTPUT_CSV = DATA_DIR / "filtered_data_with_prices.csv"

# ScraperAPI Configuration
SCRAPERAPI_KEY = os.getenv('SCRAPERAPI_KEY')
SCRAPERAPI_BASE_URL = 'http://api.scraperapi.com/'


class ScraperAPIClient:
    """Client for ScraperAPI."""
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("SCRAPERAPI_KEY not found in environment variables")
        
        self.api_key = api_key
        self.base_url = SCRAPERAPI_BASE_URL
    
    def get(self, url: str, render_js: bool = False, country: str = 'us') -> Optional[str]:
        """
        Fetch a URL through ScraperAPI.
        
        Args:
            url: Target URL to scrape
            render_js: Whether to render JavaScript
            country: Country code for IP geolocation
        
        Returns:
            HTML content or None if failed
        """
        params = {
            'api_key': self.api_key,
            'url': url,
            'country_code': country,
        }
        
        if render_js:
            params['render'] = 'true'
        
        try:
            print(f"    [ScraperAPI] Fetching: {url}")
            response = requests.get(self.base_url, params=params, timeout=60)
            response.raise_for_status()
            
            # Check ScraperAPI credits
            credits_used = response.headers.get('scraperapi-credits-used', 'unknown')
            print(f"    [ScraperAPI] Credits used: {credits_used}")
            
            return response.text
        
        except requests.RequestException as e:
            print(f"    [ERROR] ScraperAPI request failed: {e}")
            return None


class AmazonPriceScraper:
    """Scraper for Amazon prices using ScraperAPI."""
    
    def __init__(self, scraper_client: ScraperAPIClient):
        self.client = scraper_client
        self.base_url = "https://www.amazon.com"
    
    def search_product(self, brand: str, model: str, name: str) -> Optional[Dict]:
        """
        Search for a product and get its price.
        
        Args:
            brand: Product brand
            model: Product model
            name: Full product name
        
        Returns:
            Dict with price info or None
        """
        # Build search query
        query = f"{brand} {model} gaming mouse"
        search_url = f"{self.base_url}/s?k={quote_plus(query)}&i=electronics"
        
        print(f"  Searching: {query}")
        
        # Fetch search results
        html = self.client.get(search_url)
        if not html:
            return None
        
        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find first product
        products = soup.select('[data-component-type="s-search-result"]')
        
        if not products:
            print(f"    [WARN] No products found")
            return None
        
        # Get first product details
        first_product = products[0]
        
        # Extract title
        title_elem = first_product.select_one('h2 a')
        title = title_elem.get_text(strip=True) if title_elem else ""
        
        # Extract price
        price_elem = first_product.select_one('.a-price .a-offscreen')
        if not price_elem:
            print(f"    [WARN] No price found")
            return None
        
        price_text = price_elem.get_text(strip=True)
        
        # Parse price
        try:
            # Remove currency symbols and parse
            price_value = float(price_text.replace('$', '').replace(',', ''))
        except ValueError:
            print(f"    [ERROR] Could not parse price: {price_text}")
            return None
        
        # Extract product URL
        product_url = title_elem.get('href', '') if title_elem else ''
        if product_url.startswith('/'):
            product_url = f"{self.base_url}{product_url}"
        
        # Calculate simple confidence (just checking if brand is in title)
        confidence = 0.8 if brand.lower() in title.lower() else 0.5
        
        result = {
            'price': price_value,
            'currency': 'USD',
            'url': product_url,
            'title': title,
            'confidence': confidence
        }
        
        print(f"    [FOUND] ${price_value} - {title[:50]}... (confidence: {confidence})")
        
        return result


def scrape_prices(input_csv: Path, output_csv: Path, limit: Optional[int] = None):
    """
    Scrape prices for mice in CSV.
    
    Args:
        input_csv: Input CSV path
        output_csv: Output CSV path
        limit: Limit number of mice to process
    """
    # Check for API key
    if not SCRAPERAPI_KEY:
        print("[ERROR] SCRAPERAPI_KEY not found in environment variables")
        print("Please create a .env file in the project root with:")
        print("  SCRAPERAPI_KEY=your_api_key_here")
        return
    
    print("="*70)
    print("PRICE SCRAPER (ScraperAPI)")
    print("="*70)
    print(f"API Key: {SCRAPERAPI_KEY[:8]}...{SCRAPERAPI_KEY[-4:]}")
    print(f"Input: {input_csv}")
    print(f"Output: {output_csv}")
    print("="*70)
    print()
    
    # Initialize scraper
    client = ScraperAPIClient(SCRAPERAPI_KEY)
    amazon_scraper = AmazonPriceScraper(client)
    
    # Read CSV
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        mice = list(reader)
    
    print(f"Total mice: {len(mice)}")
    if limit:
        mice = mice[:limit]
        print(f"Processing: {limit} mice")
    print()
    
    # Add price columns if not present
    fieldnames = list(mice[0].keys())
    price_fields = ['Price', 'Price_Currency', 'Price_URL', 'Price_Confidence', 'Price_Title']
    for field in price_fields:
        if field not in fieldnames:
            fieldnames.append(field)
    
    # Process each mouse
    results = []
    success_count = 0
    
    for i, mouse in enumerate(mice, 1):
        brand = mouse.get('Brand', '')
        model = mouse.get('Model', '')
        name = mouse.get('Name', '')
        
        print(f"[{i}/{len(mice)}] {name}")
        
        # Try to scrape price
        price_info = amazon_scraper.search_product(brand, model, name)
        
        if price_info:
            mouse['Price'] = price_info['price']
            mouse['Price_Currency'] = price_info['currency']
            mouse['Price_URL'] = price_info['url']
            mouse['Price_Confidence'] = price_info['confidence']
            mouse['Price_Title'] = price_info['title']
            success_count += 1
        else:
            mouse['Price'] = ''
            mouse['Price_Currency'] = ''
            mouse['Price_URL'] = ''
            mouse['Price_Confidence'] = ''
            mouse['Price_Title'] = ''
        
        results.append(mouse)
        
        # Rate limiting (be nice to ScraperAPI)
        if i < len(mice):
            print(f"  [Waiting 2s...]\n")
            time.sleep(2)
    
    # Write output
    print("\n" + "="*70)
    print(f"Writing results to: {output_csv}")
    
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Done! {success_count}/{len(mice)} prices found ({success_count/len(mice)*100:.1f}%)")
    print("="*70)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape prices using ScraperAPI')
    parser.add_argument('--input', type=str, help='Input CSV path')
    parser.add_argument('--output', type=str, help='Output CSV path')
    parser.add_argument('--limit', type=int, help='Limit number to process')
    
    args = parser.parse_args()
    
    input_path = Path(args.input) if args.input else INPUT_CSV
    output_path = Path(args.output) if args.output else OUTPUT_CSV
    
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}")
        return 1
    
    scrape_prices(input_path, output_path, args.limit)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

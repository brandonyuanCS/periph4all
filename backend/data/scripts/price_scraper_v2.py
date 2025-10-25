"""
Enhanced price scraper with multiple sources prioritizing official sites.
"""
import os
import csv
import requests
from pathlib import Path
from typing import Optional, Dict, List
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time
import re

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)
DATA_DIR = PROJECT_ROOT / "backend" / "data"
INPUT_CSV = DATA_DIR / "test_mice.csv"
# INPUT_CSV = DATA_DIR / "filtered_data.csv"
OUTPUT_CSV = DATA_DIR / "filtered_data_with_prices.csv"

# ScraperAPI Configuration
SCRAPERAPI_KEY = os.getenv('SCRAPERAPI_KEY')
SCRAPERAPI_BASE_URL = 'http://api.scraperapi.com/'

# Brand official websites and pricing patterns
BRAND_SITES = {
    'Logitech': {'domain': 'logitech.com', 'priority': 1},
    'Razer': {'domain': 'razer.com', 'priority': 1},
    'SteelSeries': {'domain': 'steelseries.com', 'priority': 1},
    'Corsair': {'domain': 'corsair.com', 'priority': 1},
    'Glorious': {'domain': 'gloriousgaming.com', 'priority': 1},
    'Pulsar': {'domain': 'pulsargg.com', 'priority': 1},
    'LAMZU': {'domain': 'lamzu.com', 'priority': 1},
    'Finalmouse': {'domain': 'finalmouse.com', 'priority': 1},
    'Endgame Gear': {'domain': 'endgamegear.com', 'priority': 1},
    'Vaxee': {'domain': 'vaxee.co', 'priority': 1},
    'Zowie': {'domain': 'zowie.benq.com', 'priority': 1},
    'ASUS': {'domain': 'asus.com', 'priority': 1},
    'HyperX': {'domain': 'hyperx.com', 'priority': 1},
    'Xtrfy': {'domain': 'xtrfy.com', 'priority': 1},
    'Ninjutso': {'domain': 'ninjutso.com', 'priority': 1},
    'Pwnage': {'domain': 'pwnage.com', 'priority': 1},
    'Keychron': {'domain': 'keychron.com', 'priority': 1},
}


class ScraperAPIClient:
    """Client for ScraperAPI."""
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("SCRAPERAPI_KEY not found in environment variables")
        
        self.api_key = api_key
        self.base_url = SCRAPERAPI_BASE_URL
    
    def get(self, url: str, render_js: bool = False, country: str = 'us') -> Optional[str]:
        """Fetch a URL through ScraperAPI."""
        params = {
            'api_key': self.api_key,
            'url': url,
            'country_code': country,
        }
        
        if render_js:
            params['render'] = 'true'
        
        try:
            print(f"      Fetching: {url[:60]}...")
            response = requests.get(self.base_url, params=params, timeout=60)
            response.raise_for_status()
            
            credits_used = response.headers.get('scraperapi-credits-used', '?')
            print(f"      Credits used: {credits_used}")
            
            return response.text
        
        except requests.RequestException as e:
            print(f"      ERROR: {e}")
            return None


class PriceScraper:
    """Multi-source price scraper."""
    
    def __init__(self, scraper_client: ScraperAPIClient):
        self.client = scraper_client
    
    def extract_price_from_text(self, text: str) -> Optional[float]:
        """Extract price from text using regex."""
        # Pattern for prices: $XX.XX or XX.XX USD or €XX.XX
        patterns = [
            r'\$(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)',  # $99.99
            r'(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)\s*USD',  # 99.99 USD
            r'€(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)',  # €99.99
            r'£(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)',  # £99.99
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    price = float(match.replace(',', ''))
                    # Sanity check: mice typically $20-500
                    if 20 <= price <= 500:
                        return price
                except ValueError:
                    continue
        
        return None
    
    def search_brand_site(self, brand: str, model: str, name: str) -> Optional[Dict]:
        """Search official brand website."""
        if brand not in BRAND_SITES:
            return None
        
        domain = BRAND_SITES[brand]['domain']
        
        # Try direct Google search for product on brand site
        query = f"site:{domain} {model}"
        search_url = f"https://www.google.com/search?q={quote_plus(query)}"
        
        print(f"    [Brand Site] {domain} - {model}")
        html = self.client.get(search_url)
        
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find first organic result link
        links = soup.find_all('a', href=True)
        product_url = None
        
        for link in links:
            href = link.get('href', '')
            if domain in href and '/url?q=' in href:
                # Extract actual URL from Google redirect
                product_url = href.split('/url?q=')[1].split('&')[0]
                break
        
        if not product_url:
            return None
        
        # Fetch product page
        print(f"      Found product page: {product_url[:60]}...")
        product_html = self.client.get(product_url, render_js=True)
        
        if not product_html:
            return None
        
        # Extract price from product page
        price = self.extract_price_from_text(product_html)
        
        if price:
            return {
                'price': price,
                'source': f'{brand} Official',
                'confidence': 0.95,
                'url': product_url
            }
        
        return None
    
    def search_amazon(self, brand: str, model: str, name: str) -> Optional[Dict]:
        """Search Amazon for product."""
        query = f"{brand} {model} gaming mouse"
        search_url = f"https://www.amazon.com/s?k={quote_plus(query)}&i=electronics"
        
        print(f"    [Amazon US] {query}")
        html = self.client.get(search_url)
        
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.select('[data-component-type="s-search-result"]')
        
        if not products:
            return None
        
        first_product = products[0]
        title_elem = first_product.select_one('h2 a')
        title = title_elem.get_text(strip=True) if title_elem else ""
        
        price_elem = first_product.select_one('.a-price .a-offscreen')
        if not price_elem:
            return None
        
        price_text = price_elem.get_text(strip=True)
        
        try:
            price_value = float(price_text.replace('$', '').replace(',', ''))
        except ValueError:
            return None
        
        product_url = title_elem.get('href', '') if title_elem else ''
        if product_url.startswith('/'):
            product_url = f"https://www.amazon.com{product_url}"
        
        # Better confidence scoring
        confidence = 0.5
        if brand.lower() in title.lower():
            confidence += 0.2
        if model.lower() in title.lower():
            confidence += 0.2
        
        return {
            'price': price_value,
            'source': 'Amazon US',
            'confidence': min(confidence, 0.9),
            'url': product_url,
            'title': title
        }
    
    def search_aliexpress(self, brand: str, model: str, name: str) -> Optional[Dict]:
        """Search AliExpress (good for Chinese brands)."""
        query = f"{brand} {model} mouse"
        search_url = f"https://www.aliexpress.com/wholesale?SearchText={quote_plus(query)}"
        
        print(f"    [AliExpress] {query}")
        html = self.client.get(search_url, render_js=True)
        
        if not html:
            return None
        
        price = self.extract_price_from_text(html)
        
        if price:
            # AliExpress prices are typically wholesale, add markup estimate
            estimated_retail = price * 1.5
            return {
                'price': estimated_retail,
                'source': 'AliExpress (estimated)',
                'confidence': 0.6,
                'url': search_url
            }
        
        return None
    
    def search_all_sources(self, brand: str, model: str, name: str) -> Optional[Dict]:
        """Search all sources in priority order."""
        sources = [
            ('Official Site', lambda: self.search_brand_site(brand, model, name)),
            ('Amazon', lambda: self.search_amazon(brand, model, name)),
            ('AliExpress', lambda: self.search_aliexpress(brand, model, name)),
        ]
        
        best_result = None
        best_confidence = 0
        
        for source_name, search_func in sources:
            try:
                result = search_func()
                if result and result['confidence'] > best_confidence:
                    best_result = result
                    best_confidence = result['confidence']
                    
                    # If we have high confidence from official site, stop
                    if best_confidence >= 0.9:
                        print(f"      ✓ High confidence result from {source_name}")
                        break
                
            except Exception as e:
                print(f"      ERROR in {source_name}: {e}")
                continue
            
            # Rate limiting between sources
            time.sleep(1)
        
        return best_result


def scrape_prices(input_csv: Path, output_csv: Path, limit: Optional[int] = None):
    """Scrape prices for mice in CSV."""
    if not SCRAPERAPI_KEY:
        print("[ERROR] SCRAPERAPI_KEY not found in environment variables")
        return
    
    print("="*70)
    print("MULTI-SOURCE PRICE SCRAPER")
    print("="*70)
    print(f"Input: {input_csv}")
    print(f"Output: {output_csv}")
    print("="*70)
    print()
    
    client = ScraperAPIClient(SCRAPERAPI_KEY)
    scraper = PriceScraper(client)
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        mice = list(reader)
    
    print(f"Total mice: {len(mice)}")
    if limit:
        mice = mice[:limit]
        print(f"Processing: {limit} mice")
    print()
    
    fieldnames = list(mice[0].keys())
    price_fields = ['Price', 'Price_Source', 'Price_Confidence', 'Price_URL', 'Price_Title']
    for field in price_fields:
        if field not in fieldnames:
            fieldnames.append(field)
    
    results = []
    success_count = 0
    
    for i, mouse in enumerate(mice, 1):
        brand = mouse.get('Brand', '')
        model = mouse.get('Model', '')
        name = mouse.get('Name', '')
        
        print(f"\n[{i}/{len(mice)}] {name}")
        print(f"  Brand: {brand} | Model: {model}")
        
        price_info = scraper.search_all_sources(brand, model, name)
        
        if price_info:
            mouse['Price'] = price_info['price']
            mouse['Price_Source'] = price_info['source']
            mouse['Price_Confidence'] = price_info['confidence']
            mouse['Price_URL'] = price_info.get('url', '')
            mouse['Price_Title'] = price_info.get('title', '')
            success_count += 1
            print(f"  ✓ FOUND: ${price_info['price']:.2f} from {price_info['source']} (confidence: {price_info['confidence']:.2f})")
        else:
            mouse['Price'] = ''
            mouse['Price_Source'] = ''
            mouse['Price_Confidence'] = ''
            mouse['Price_URL'] = ''
            mouse['Price_Title'] = ''
            print(f"  ✗ NOT FOUND")
        
        results.append(mouse)
        
        # Rate limiting between products
        if i < len(mice):
            print(f"  [Waiting 3s...]")
            time.sleep(3)
    
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
    
    parser = argparse.ArgumentParser(description='Multi-source price scraper')
    parser.add_argument('--limit', type=int, help='Limit number to process')
    args = parser.parse_args()
    
    if not INPUT_CSV.exists():
        print(f"[ERROR] Input file not found: {INPUT_CSV}")
        return 1
    
    scrape_prices(INPUT_CSV, OUTPUT_CSV, args.limit)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
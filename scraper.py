"""
Web Scraper - Main Application (FIXED)
Purpose: Scrape product data from websites and save to CSV/JSON

Author: Nauriya Lanjali
Project: Synent Technologies Internship
Date: 2026-06-07

Key Concepts:
- HTTP Requests: Fetch web pages
- HTML Parsing: Extract data using BeautifulSoup
- Data Cleaning: Process raw data
- Data Storage: Export to CSV and JSON
- Error Handling: Handle network and parsing errors
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import os
from typing import List, Dict, Optional
import logging

# Set up logging for debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebScraper:
    """
    A class to handle web scraping operations.
    
    Attributes:
        base_url (str): The website URL to scrape
        headers (dict): HTTP headers to use in requests
        output_dir (str): Directory to save output files
    """
    
    def __init__(self, base_url: str, output_dir: str = 'output'):
        """
        Initialize the scraper.
        
        Args:
            base_url: The website URL to scrape
            output_dir: Directory for output files (default: 'output')
        """
        self.base_url = base_url
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Headers to mimic a real browser (avoid being blocked)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        logger.info(f"Scraper initialized for: {base_url}")
    
    def fetch_page(self, url: str, timeout: int = 5) -> Optional[str]:
        """
        Fetch a web page using HTTP GET request.
        
        This is the first step in scraping - we need to download the HTML content.
        
        Args:
            url: The URL to fetch
            timeout: Request timeout in seconds
        
        Returns:
            HTML content as string, or None if request fails
        """
        try:
            logger.info(f"Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()  # Raise error for bad status codes
            logger.info(f"Successfully fetched: {url} (Status: {response.status_code})")
            return response.content
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error while fetching {url}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error while fetching {url}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code}: {url}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def parse_html(self, html_content: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML content using BeautifulSoup.
        
        BeautifulSoup converts raw HTML into a tree structure we can navigate.
        
        Args:
            html_content: Raw HTML as string
        
        Returns:
            BeautifulSoup object, or None if parsing fails
        """
        try:
            # 'html.parser' is built-in, no external dependencies needed
            soup = BeautifulSoup(html_content, 'html.parser')
            logger.info("HTML parsed successfully")
            return soup
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None
    
    def extract_books_data(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract book data from books.toscrape.com
        
        This demonstrates how to:
        1. Find all product containers
        2. Extract individual data points
        3. Handle missing data gracefully
        4. Clean and format data
        
        IMPORTANT: Always inspect the website first!
        Right-click → Inspect to find the correct CSS classes
        
        Args:
            soup: BeautifulSoup object
        
        Returns:
            List of dictionaries containing book data
        """
        books = []
        
        # Find all product containers
        # CORRECTED: Looking for article tags with class 'product_pod'
        products = soup.find_all('article', class_='product_pod')
        logger.info(f"Found {len(products)} products")
        
        # If still no products, try alternative selector
        if not products:
            logger.warning("No products found with 'article' tag, trying 'div'...")
            products = soup.find_all('div', class_='product_pod')
            logger.info(f"Found {len(products)} products with alternative selector")
        
        for idx, product in enumerate(products, 1):
            try:
                # Extract title from h3 > a tag's title attribute
                title_element = product.find('h3')
                if title_element:
                    title_link = title_element.find('a')
                    title = title_link.get('title', 'N/A') if title_link else 'N/A'
                else:
                    title = 'N/A'
                
                # Extract price - look for span with class 'price_color'
                price_element = product.find('p', class_='price_color')
                price_raw = price_element.text if price_element else 'N/A'
                # Clean price: remove currency symbol and extra whitespace
                price = price_raw.replace('£', '').replace('Â', '').strip()
                
                # Extract rating - stored in p tag with class 'star-rating'
                # The rating is in the class attribute (e.g., 'star-rating Three')
                rating_element = product.find('p', class_='star-rating')
                if rating_element and 'class' in rating_element.attrs:
                    # Get second class (first is 'star-rating', second is the rating)
                    classes = rating_element.get('class', [])
                    rating = classes[1] if len(classes) > 1 else 'N/A'
                else:
                    rating = 'N/A'
                
                # Extract availability from p tag with class 'instock availability'
                availability_element = product.find('p', class_='instock availability')
                availability = availability_element.text.strip() if availability_element else 'N/A'
                
                # Extract book URL from the link
                book_url = 'N/A'
                if title_element:
                    link = title_element.find('a')
                    if link and 'href' in link.attrs:
                        book_url = 'http://books.toscrape.com/' + link['href']
                
                # Create book dictionary
                book_data = {
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'availability': availability,
                    'url': book_url
                }
                
                books.append(book_data)
                logger.debug(f"Extracted book {idx}: {title}")
            
            except Exception as e:
                logger.warning(f"Error extracting book {idx}: {e}")
                continue
        
        return books
    
    def scrape_books(self, num_pages: int = 1) -> List[Dict]:
        """
        Scrape books from multiple pages.
        
        Demonstrates pagination and combining data from multiple pages.
        
        Args:
            num_pages: Number of pages to scrape (default: 1)
        
        Returns:
            List of all books scraped
        """
        all_books = []
        
        for page_num in range(1, num_pages + 1):
            # Construct page URL
            if page_num == 1:
                url = f'{self.base_url}/'
            else:
                url = f'{self.base_url}/catalogue/page-{page_num}.html'
            
            # Fetch and parse
            html_content = self.fetch_page(url)
            if html_content is None:
                logger.warning(f"Failed to fetch page {page_num}, skipping")
                continue
            
            soup = self.parse_html(html_content)
            if soup is None:
                logger.warning(f"Failed to parse page {page_num}, skipping")
                continue
            
            # Extract books from this page
            books = self.extract_books_data(soup)
            all_books.extend(books)
            
            logger.info(f"Page {page_num}: Scraped {len(books)} books")
            
            # Be respectful to servers - add delay between requests
            if page_num < num_pages:
                time.sleep(2)
        
        logger.info(f"Total books scraped: {len(all_books)}")
        return all_books
    
    def save_to_csv(self, data: List[Dict], filename: str = 'products.csv') -> bool:
        """
        Save data to CSV file.
        
        CSV (Comma-Separated Values) is great for spreadsheets.
        
        Args:
            data: List of dictionaries to save
            filename: Output filename
        
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = os.path.join(self.output_dir, filename)
            
            if not data:
                logger.warning("No data to save")
                return False
            
            # Get column names from first item
            fieldnames = data[0].keys()
            
            # Write to CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"Data saved to CSV: {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return False
    
    def save_to_json(self, data: List[Dict], filename: str = 'products.json') -> bool:
        """
        Save data to JSON file.
        
        JSON (JavaScript Object Notation) is human-readable and hierarchical.
        
        Args:
            data: List of dictionaries to save
            filename: Output filename
        
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = os.path.join(self.output_dir, filename)
            
            if not data:
                logger.warning("No data to save")
                return False
            
            # Write to JSON
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            logger.info(f"Data saved to JSON: {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            return False
    
    def display_data(self, data: List[Dict], limit: int = 5):
        """
        Display scraped data in terminal.
        
        Args:
            data: List of dictionaries to display
            limit: Number of items to show
        """
        print("\n" + "="*80)
        print(f"📊 SCRAPED DATA (Showing {min(limit, len(data))} of {len(data)} items)")
        print("="*80 + "\n")
        
        for idx, item in enumerate(data[:limit], 1):
            print(f"📌 Item {idx}:")
            for key, value in item.items():
                print(f"   {key}: {value}")
            print()


def inspect_page(url: str):
    """
    Helper function to inspect page structure for debugging.
    
    This helps you understand the website structure when selectors don't work.
    """
    print(f"\n🔍 INSPECTING PAGE: {url}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for different possible containers
        print("Checking for product containers...")
        
        articles = soup.find_all('article')
        print(f"  - <article> tags found: {len(articles)}")
        
        divs = soup.find_all('div', class_='product_pod')
        print(f"  - <div class='product_pod'> found: {len(divs)}")
        
        products = soup.find_all(class_='product_pod')
        print(f"  - Any element with class 'product_pod': {len(products)}")
        
        # Show first product structure
        if products:
            print(f"\n📝 First product HTML (first 500 chars):")
            print(str(products[0])[:500])
        
    except Exception as e:
        print(f"Error: {e}")


def main():
    """
    Main function to run the scraper.
    
    This demonstrates the complete scraping workflow.
    """
    
    print("\n" + "="*80)
    print("🌐 WEB SCRAPER - Educational Demo")
    print("="*80 + "\n")
    
    # Initialize scraper
    scraper = WebScraper('http://books.toscrape.com')
    
    # Optional: Inspect page structure for debugging
    # Uncomment the line below to see page structure
    # inspect_page('http://books.toscrape.com/')
    
    # Scrape books (1 page for demo, change to more pages if needed)
    print("🔄 Starting scrape...\n")
    books = scraper.scrape_books(num_pages=1)
    
    # Display results
    if books:
        scraper.display_data(books, limit=5)
        
        # Save to both formats
        print("\n💾 Saving data...")
        scraper.save_to_csv(books, 'books.csv')
        scraper.save_to_json(books, 'books.json')
        
        print("\n✅ Scraping completed successfully!")
        print(f"   Total items scraped: {len(books)}")
        print(f"   Files saved in: {os.path.abspath(scraper.output_dir)}/")
    else:
        print("\n❌ Failed to scrape any data")
        print("\n💡 TROUBLESHOOTING:")
        print("   1. Check if website is working (open in browser)")
        print("   2. The website structure might have changed")
        print("   3. Uncomment inspect_page() in main() to debug")
        print("   4. Right-click on website → Inspect to find correct selectors")
        print("\n   Try running: inspect_page('http://books.toscrape.com/')")


if __name__ == '__main__':
    main()

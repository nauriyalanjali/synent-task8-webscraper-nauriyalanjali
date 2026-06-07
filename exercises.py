"""
Practice Exercises for Web Scraping
Complete these to master web scraping concepts!

Each exercise builds your skills progressively.
Start with Exercise 1 and work your way up.
"""

# ==============================================================================
# EXERCISE 1: Basic HTTP Requests and Status Codes
# ==============================================================================
"""
GOAL: Understand HTTP requests and responses

TASK:
1. Make requests to different websites
2. Check status codes and headers
3. Learn what different codes mean

WHAT YOU'LL LEARN:
- How HTTP requests work
- Status codes (200, 404, 403, 500, etc.)
- Request headers and responses
"""

def exercise_1_basic_requests():
    """
    Make HTTP requests and examine responses.
    """
    import requests
    
    # Test different URLs
    urls = [
        'http://httpbin.org/get',          # Test endpoint (always works)
        'http://books.toscrape.com',       # Real website
        'http://httpbin.org/status/404',   # Intentional 404
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"\n📍 URL: {url}")
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Type: {response.headers.get('content-type')}")
            print(f"   Content Length: {len(response.content)} bytes")
        except Exception as e:
            print(f"   Error: {e}")


# ==============================================================================
# EXERCISE 2: HTML Structure and Parsing
# ==============================================================================
"""
GOAL: Learn HTML structure and BeautifulSoup basics

TASK:
1. Parse simple HTML
2. Find elements by tag, class, id
3. Extract text and attributes

WHAT YOU'LL LEARN:
- HTML structure
- CSS selectors
- BeautifulSoup methods (find, find_all)
"""

def exercise_2_html_parsing():
    """
    Parse HTML and extract data.
    """
    from bs4 import BeautifulSoup
    
    # Sample HTML
    html = """
    <div class="container">
        <h1>Welcome</h1>
        <div class="product">
            <h2>Laptop</h2>
            <span class="price">$999</span>
            <p class="description">High-performance laptop</p>
            <a href="/product/1">View Details</a>
        </div>
        <div class="product">
            <h2>Phone</h2>
            <span class="price">$599</span>
            <p class="description">Latest smartphone</p>
            <a href="/product/2">View Details</a>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find by tag
    print("\n1️⃣ Find by tag:")
    print(f"   First h1: {soup.find('h1').text}")
    
    # Find by class
    print("\n2️⃣ Find by class:")
    products = soup.find_all('div', class_='product')
    print(f"   Found {len(products)} products")
    
    # Extract data from first product
    print("\n3️⃣ Extract from first product:")
    first_product = products[0]
    title = first_product.find('h2').text
    price = first_product.find('span', class_='price').text
    link = first_product.find('a')['href']
    print(f"   Title: {title}")
    print(f"   Price: {price}")
    print(f"   Link: {link}")
    
    # Loop through all products
    print("\n4️⃣ Loop through all products:")
    for i, product in enumerate(products, 1):
        title = product.find('h2').text
        price = product.find('span', class_='price').text
        print(f"   Product {i}: {title} - {price}")


# ==============================================================================
# EXERCISE 3: CSS Selectors (Advanced Finding)
# ==============================================================================
"""
GOAL: Master CSS selectors for powerful element selection

TASK:
1. Use select() instead of find()
2. Try different selector patterns
3. Compare with find() approach

WHAT YOU'LL LEARN:
- CSS selectors (.class, #id, tag > child, etc.)
- select() method
- When to use select() vs find()
"""

def exercise_3_css_selectors():
    """
    Use CSS selectors for element selection.
    """
    from bs4 import BeautifulSoup
    
    html = """
    <div class="container">
        <div class="product" id="prod-1">
            <h2>Product 1</h2>
            <span class="price">$10</span>
        </div>
        <div class="product" id="prod-2">
            <h2>Product 2</h2>
            <span class="price">$20</span>
        </div>
        <div class="featured">
            <h2>Featured</h2>
            <span class="price">$50</span>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    print("\n1️⃣ Select by class (.product):")
    products = soup.select('.product')
    print(f"   Found: {len(products)} elements")
    
    print("\n2️⃣ Select by id (#prod-1):")
    element = soup.select('#prod-1')
    print(f"   Found: {element[0].find('h2').text if element else 'None'}")
    
    print("\n3️⃣ Select all prices (.price):")
    prices = soup.select('.price')
    for price in prices:
        print(f"   {price.text}")
    
    print("\n4️⃣ Select children (div > span):")
    children = soup.select('div > span')
    print(f"   Found: {len(children)} direct children")
    
    print("\n5️⃣ Select with attribute [id]:")
    with_id = soup.select('[id]')
    print(f"   Elements with id attribute: {len(with_id)}")


# ==============================================================================
# EXERCISE 4: Data Cleaning
# ==============================================================================
"""
GOAL: Clean and prepare scraped data

TASK:
1. Remove extra whitespace
2. Convert data types
3. Handle special characters
4. Standardize formats

WHAT YOU'LL LEARN:
- String manipulation
- Data validation
- Preparing data for storage
"""

def exercise_4_data_cleaning():
    """
    Clean raw scraped data.
    """
    
    print("\n1️⃣ Remove extra whitespace:")
    raw_text = "  Product   Name  \n\n"
    clean_text = raw_text.strip()
    print(f"   Before: '{raw_text}'")
    print(f"   After:  '{clean_text}'")
    
    print("\n2️⃣ Remove special characters:")
    raw_price = "£29.99"
    clean_price = raw_price.replace('£', '').replace(',', '')
    print(f"   Before: {raw_price}")
    print(f"   After:  {clean_price}")
    
    print("\n3️⃣ Convert to float:")
    price_str = "29.99"
    price_float = float(price_str)
    print(f"   String: '{price_str}' (type: {type(price_str).__name__})")
    print(f"   Float:  {price_float} (type: {type(price_float).__name__})")
    
    print("\n4️⃣ Standardize text:")
    raw_rating = "Four out of five"
    clean_rating = raw_rating.replace(' out of five', '').replace(' ', '').upper()
    print(f"   Before: {raw_rating}")
    print(f"   After:  {clean_rating}")
    
    print("\n5️⃣ Handle missing data:")
    data = ['Item 1', None, '', 'Item 2', '   ']
    cleaned = [item.strip() if item and item.strip() else 'N/A' for item in data]
    print(f"   Before: {data}")
    print(f"   After:  {cleaned}")


# ==============================================================================
# EXERCISE 5: Safe Data Extraction (Error Handling)
# ==============================================================================
"""
GOAL: Extract data safely without crashes

TASK:
1. Check if elements exist before accessing
2. Use try-except blocks
3. Provide default values for missing data

WHAT YOU'LL LEARN:
- Defensive programming
- Error handling patterns
- Robustness in scraping
"""

def exercise_5_safe_extraction():
    """
    Extract data safely with error handling.
    """
    from bs4 import BeautifulSoup
    
    # HTML with missing elements
    html = """
    <div class="product">
        <h2>Product 1</h2>
        <!-- No price! -->
        <p>Description</p>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    product = soup.find('div', class_='product')
    
    print("\n1️⃣ Unsafe way (WILL CRASH):")
    try:
        # This will crash because price doesn't exist
        # price = product.find('span', class_='price').text
        print("   (Skipped - would crash!)")
    except AttributeError:
        print("   AttributeError: 'NoneType' object has no attribute 'text'")
    
    print("\n2️⃣ Safe way - Check if element exists:")
    price_element = product.find('span', class_='price')
    price = price_element.text if price_element else 'N/A'
    print(f"   Price: {price}")
    
    print("\n3️⃣ Safe way - Try-except block:")
    try:
        price = product.find('span', class_='price').text
    except AttributeError:
        price = 'N/A'
    print(f"   Price: {price}")
    
    print("\n4️⃣ Safe extraction function:")
    def safe_extract(element, selector, attribute=None, default='N/A'):
        try:
            el = element.find(selector[0], class_=selector[1]) if len(selector) > 1 else element.find(selector[0])
            if attribute:
                return el[attribute] if el else default
            else:
                return el.text if el else default
        except:
            return default
    
    title = safe_extract(product, ('h2',))
    price = safe_extract(product, ('span', 'price'))
    print(f"   Title: {title}, Price: {price}")


# ==============================================================================
# EXERCISE 6: Save to CSV and JSON
# ==============================================================================
"""
GOAL: Export scraped data to files

TASK:
1. Save to CSV format
2. Save to JSON format
3. Read files back
4. Compare formats

WHAT YOU'LL LEARN:
- File I/O
- CSV and JSON formats
- Data serialization
"""

def exercise_6_save_data():
    """
    Save and load data in different formats.
    """
    import csv
    import json
    import os
    
    # Sample data
    data = [
        {'title': 'Laptop', 'price': '999', 'rating': 'Five'},
        {'title': 'Phone', 'price': '599', 'rating': 'Four'},
    ]
    
    # Create output directory
    os.makedirs('exercise_output', exist_ok=True)
    
    print("\n1️⃣ Save to CSV:")
    csv_file = 'exercise_output/products.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'price', 'rating'])
        writer.writeheader()
        writer.writerows(data)
    print(f"   Saved to: {csv_file}")
    
    print("\n2️⃣ Save to JSON:")
    json_file = 'exercise_output/products.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"   Saved to: {json_file}")
    
    print("\n3️⃣ Read CSV back:")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_data = list(reader)
    print(f"   Loaded {len(csv_data)} rows")
    print(f"   First row: {csv_data[0]}")
    
    print("\n4️⃣ Read JSON back:")
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    print(f"   Loaded {len(json_data)} items")
    print(f"   First item: {json_data[0]}")


# ==============================================================================
# EXERCISE 7: Real Website - Books.toscrape.com
# ==============================================================================
"""
GOAL: Scrape a real website (educational purpose)

TASK:
1. Inspect the website in browser
2. Find product CSS selectors
3. Extract book data
4. Save results

WHAT YOU'LL LEARN:
- Real-world scraping workflow
- Inspecting elements in browser
- Combining all previous concepts
"""

def exercise_7_real_website():
    """
    Scrape books.toscrape.com (made for learning!)
    """
    import requests
    from bs4 import BeautifulSoup
    import time
    
    url = 'http://books.toscrape.com/'
    
    print("\n🔄 Fetching website...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find books
    books = soup.find_all('div', class_='product_pod')
    print(f"✅ Found {len(books)} books\n")
    
    # Extract first 5 books
    print("📚 First 5 books:")
    for i, book in enumerate(books[:5], 1):
        title = book.find('h3').find('a')['title']
        price = book.find('p', class_='price_color').text
        rating = book.find('p', class_='star-rating')['class'][1]
        print(f"   {i}. {title}")
        print(f"      Price: {price}, Rating: {rating}\n")


# ==============================================================================
# RUN THE EXERCISES
# ==============================================================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🎓 WEB SCRAPING PRACTICE EXERCISES")
    print("="*80)
    
    exercises = [
        ("Exercise 1: Basic HTTP Requests", exercise_1_basic_requests),
        ("Exercise 2: HTML Parsing", exercise_2_html_parsing),
        ("Exercise 3: CSS Selectors", exercise_3_css_selectors),
        ("Exercise 4: Data Cleaning", exercise_4_data_cleaning),
        ("Exercise 5: Safe Extraction", exercise_5_safe_extraction),
        ("Exercise 6: Save Data", exercise_6_save_data),
        ("Exercise 7: Real Website", exercise_7_real_website),
    ]
    
    print("\nAvailable exercises:")
    for i, (name, _) in enumerate(exercises, 1):
        print(f"   {i}. {name}")
    
    # Run all exercises
    print("\n" + "="*80)
    for name, func in exercises:
        print(f"\n{'='*80}")
        print(f"▶️  {name}")
        print("="*80)
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print("\n" + "="*80)
    print("✅ All exercises completed!")
    print("="*80 + "\n")

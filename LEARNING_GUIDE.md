# 🎓 Web Scraping Learning Guide - From Basics to Advanced

## Phase 1: Core Concepts (Foundation)

### 1.1 Understanding HTTP Requests
**What you need to know:**
- HTTP is how browsers communicate with servers
- GET request = retrieve data
- POST request = send data
- Status codes: 200 (OK), 404 (Not Found), 403 (Forbidden), 500 (Error)

**Hands-on Exercise:**
```python
import requests

# Simple GET request
response = requests.get('http://httpbin.org/get')
print(response.status_code)  # See the status code
print(response.headers)       # See what server sends back
print(response.text)          # See the HTML content
```

**Learning Task:** Try different URLs and observe status codes. Document what you learn.

---

### 1.2 Understanding HTML Structure
**What you need to know:**
- HTML has tags: `<div>`, `<span>`, `<p>`, `<a>`, `<img>`
- Attributes: `class`, `id`, `href`, `src`
- DOM (Document Object Model) - tree structure
- CSS Selectors: `.class`, `#id`, `tag`, `tag.class`

**HTML Example:**
```html
<div class="product">
  <h2 id="title">Product Name</h2>
  <span class="price">$29.99</span>
  <p class="description">Great product</p>
  <div class="rating">4.5 stars</div>
</div>
```

**How to Target:**
```
.product         → Select by class
#title           → Select by id
.price           → Select by class
div.product      → Select div with class product
.product .price  → Select .price inside .product
```

**Learning Task:** Open any website, inspect HTML (Right-click → Inspect), identify product classes and IDs.

---

### 1.3 BeautifulSoup Basics
**Core Methods You'll Use:**

```python
from bs4 import BeautifulSoup

html = """
<div class="product">
  <h2>Laptop</h2>
  <span class="price">$999</span>
</div>
"""

soup = BeautifulSoup(html, 'html.parser')

# Find single element
product = soup.find('div', class_='product')

# Find all elements
prices = soup.find_all('span', class_='price')

# Get text
title = soup.find('h2').text
print(title)  # Output: Laptop

# Get attribute
link = soup.find('a')['href']
```

**Learning Task:** Practice with sample HTML. Try find(), find_all(), accessing text, and attributes.

---

## Phase 2: Building Your First Scraper

### 2.1 Step-by-Step: Scraping Books.toscrape.com

This website is specifically made for learning scraping!

**Step 1: Fetch the page**
```python
import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
```

**Step 2: Explore the HTML**
```python
# Open browser, Right-click → Inspect
# Find book containers - they use class "product_pod"
books = soup.find_all('div', class_='product_pod')
print(f"Found {len(books)} books")
```

**Step 3: Extract data from one book**
```python
# Get first book
book = books[0]

# Extract title
title = book.find('h3').find('a')['title']
print(f"Title: {title}")

# Extract price
price = book.find('p', class_='price_color').text
print(f"Price: {price}")

# Extract rating
rating = book.find('p', class_='star-rating')['class'][1]
print(f"Rating: {rating}")

# Extract availability
availability = book.find('p', class_='instock availability').text.strip()
print(f"Availability: {availability}")
```

**Step 4: Extract all books (Loop)**
```python
all_books = []

for book in books:
    title = book.find('h3').find('a')['title']
    price = book.find('p', class_='price_color').text
    rating = book.find('p', class_='star-rating')['class'][1]
    availability = book.find('p', class_='instock availability').text.strip()
    
    book_data = {
        'title': title,
        'price': price,
        'rating': rating,
        'availability': availability
    }
    all_books.append(book_data)

for book in all_books:
    print(book)
```

**Learning Task:** Run this code and verify it works. Try modifying selectors, extracting different data.

---

### 2.2 Handling Real-World Challenges

**Challenge 1: Data Cleaning**
```python
# Raw data: "£29.99"
price_raw = "£29.99"

# Clean it
price_clean = price_raw.replace('£', '').strip()
print(price_clean)  # Output: 29.99
```

**Challenge 2: Missing Elements**
```python
# Some products might not have ratings
# This will crash:
rating = book.find('p', class_='star-rating')['class'][1]

# Safe way:
rating_element = book.find('p', class_='star-rating')
rating = rating_element['class'][1] if rating_element else 'N/A'
```

**Challenge 3: Multiple Pages**
```python
# books.toscrape.com has multiple pages
all_books = []

for page_num in range(1, 3):  # Pages 1 and 2
    url = f'http://books.toscrape.com/catalogue/page-{page_num}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = soup.find_all('div', class_='product_pod')
    
    for book in books:
        # Extract data...
        pass
    
    print(f"Scraped page {page_num}")
```

**Learning Task:** Modify your scraper to handle multiple pages.

---

## Phase 3: Data Storage

### 3.1 Save to CSV
```python
import csv

books = [
    {'title': 'Book 1', 'price': '29.99', 'rating': 'Four'},
    {'title': 'Book 2', 'price': '39.99', 'rating': 'Five'}
]

# Write to CSV
with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'price', 'rating'])
    writer.writeheader()
    writer.writerows(books)
```

### 3.2 Save to JSON
```python
import json

# Write to JSON
with open('books.json', 'w', encoding='utf-8') as file:
    json.dump(books, file, indent=2, ensure_ascii=False)

# Read from JSON
with open('books.json', 'r', encoding='utf-8') as file:
    loaded_books = json.load(file)
```

**Learning Task:** Save your scraped data in both formats. Verify by opening the files.

---

## Phase 4: Best Practices & Ethics

### 4.1 Add Delays (Be Respectful to Servers)
```python
import time

for page_num in range(1, 10):
    url = f'...'
    response = requests.get(url)
    # ... scrape data ...
    
    # Wait before next request
    time.sleep(2)  # 2 second delay
    print(f"Scraped page {page_num}, waiting...")
```

### 4.2 Set User-Agent
```python
# Servers might block bot requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
```

### 4.3 Error Handling
```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise error for bad status codes
    soup = BeautifulSoup(response.content, 'html.parser')
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Connection error")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
```

**Learning Task:** Add error handling to your scraper and test it.

---

## Phase 5: Advanced Techniques

### 5.1 CSS Selectors (More Powerful)
```python
# Instead of find(), use select()
soup.select('.product .price')        # All .price inside .product
soup.select('div.product > span')     # Direct children
soup.select('a[href*="amazon"]')      # Links containing "amazon"
soup.select('tr:nth-child(2)')        # Second row in table
```

### 5.2 Handling JavaScript-Rendered Content
Some websites load content with JavaScript. BeautifulSoup can't handle this.

**Solution: Use Selenium**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get('https://example.com')
time.sleep(3)  # Wait for JS to load

# Now parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()
```

### 5.3 Pagination with Automatic Detection
```python
def scrape_all_pages(base_url):
    all_data = []
    page = 1
    
    while True:
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page}...")
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data
        products = soup.find_all('div', class_='product')
        
        if not products:  # No more products = end of pages
            break
        
        for product in products:
            # Extract and store
            pass
        
        page += 1
        time.sleep(2)
    
    return all_data
```

---

## Phase 6: Project Checklist

As you build, check off:

- [ ] **Fetch webpage** - requests.get() works
- [ ] **Parse HTML** - BeautifulSoup loads correctly
- [ ] **Find elements** - Correctly identify CSS selectors
- [ ] **Extract data** - Get title, price, etc.
- [ ] **Clean data** - Remove extra spaces, special characters
- [ ] **Handle errors** - Try-except blocks added
- [ ] **Handle missing data** - Check if elements exist
- [ ] **Add delays** - Be respectful to servers
- [ ] **Save to CSV** - Data exports correctly
- [ ] **Save to JSON** - Data exports correctly
- [ ] **Multiple pages** - Pagination works
- [ ] **User-agent header** - Set proper headers
- [ ] **Test thoroughly** - Works on multiple runs
- [ ] **Clean code** - Well-commented, organized
- [ ] **README updated** - Explain how to use

---

## Quick Reference: Common Patterns

### Pattern 1: Extract from List
```python
items = soup.find_all('div', class_='item')
data = [{'name': item.find('h3').text} for item in items]
```

### Pattern 2: Handle Missing Data
```python
price = product.find('span', class_='price')
price = price.text if price else 'N/A'
```

### Pattern 3: Extract from Table
```python
rows = soup.find_all('tr')[1:]  # Skip header
for row in rows:
    cols = row.find_all('td')
    data = [col.text.strip() for col in cols]
```

### Pattern 4: Follow Links
```python
links = soup.find_all('a')
for link in links:
    url = link['href']
    # Process each link
```

---

## 📚 Resources to Continue Learning

1. **BeautifulSoup Docs:** https://www.crummy.com/software/BeautifulSoup/bs4/doc/
2. **Requests Library:** https://requests.readthedocs.io/
3. **CSS Selectors Guide:** https://www.w3schools.com/cssref/selectors_attribute.asp
4. **Web Scraping Ethics:** https://blog.apify.com/is-web-scraping-legal/
5. **Practice Site:** http://books.toscrape.com/ (made for learning!)

---

## 🎯 Your Learning Path

1. **Week 1:** Master HTTP requests and BeautifulSoup basics
2. **Week 2:** Build scraper for books.toscrape.com
3. **Week 3:** Scrape real e-commerce site (with permission)
4. **Week 4:** Add error handling, pagination, data cleaning
5. **Week 5:** Advanced techniques and optimization

---

**Good luck! Every line of code you write teaches you something new. Keep experimenting!** 🚀

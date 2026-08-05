# (.venv) PS D:\project\laptop_pricing_intelligence_pipeline\src> python scraping/scraper.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# base url
listing_page_url = "https://www.newegg.com/All-Laptop/SubCategory/ID-32/"


# requesting and parsing
def get_soup(url : str) -> BeautifulSoup | None:
  try:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    if soup is None:
      return None
    return soup

  except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    return None
  
  except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    return None
  

# pagination
def scrape_all_listing_pages() -> list[dict]:
  soup = get_soup(listing_page_url)
  if soup is None:
    return []

  pagination = soup.find("span", class_="list-tool-pagination-text")
  pages = int(pagination.text.split("/")[1])

  laptops = scrape_listing_page(listing_page_url)
  for page in range(2, pages+1):
    path = f"Page-{page}"
    full_url = urljoin(listing_page_url, path)
    laptops.extend(scrape_listing_page(full_url))
  return laptops


# listing page
def scrape_listing_page(url:str) -> list[dict]:
  soup = get_soup(url)
  if soup is None:
    return []
  
  products = soup.find_all("div", class_="item-cell")
  laptops = []

  for product in products:

    title_tag = product.find("a", class_="item-title")
    link = title_tag.get("href").strip() if title_tag else None
    title = title_tag.text.strip() if title_tag else None

    price_current_tag = product.find("li", class_="price-current")
    price_current = price_current_tag.text.replace("\xa0–", "").strip() if price_current_tag else None

    price_was_tag = product.find("li", class_="price-was")
    price_was = price_was_tag.text.strip() if price_was_tag else None

    rating_tag = product.find("i", class_="rating")
    rating_value = float(rating_tag.get("aria-label").split()[1]) if rating_tag else None

    rating_num_tag = product.find("span", class_="item-rating-num")
    rating_num = int(rating_num_tag.text.strip("()").strip()) if rating_num_tag else None

    save_tag = product.find("span", class_="price-save-percent")
    save = save_tag.text.strip() if save_tag else None

    shipping_tag = product.find("li", class_="price-ship")
    shipping = shipping_tag.text.strip() if shipping_tag else None

    laptop = {
        "title": title,
        "link": link,
        "current_price": price_current,
        "old_price": price_was,
        "discount": save,
        "rating": rating_value,
        "rating_num": rating_num,
        "shipping": shipping
    }
    laptops.append(laptop)
  return laptops
  

# product page
def scrape_product_page(url:str) -> dict:
  soup = get_soup(url)
  if soup is None:
    return {}

  spec_table = soup.find("div", class_="tab-panes")
  if spec_table is None:
    return {}
  tables = spec_table.find_all("table", class_="table-horizontal")

  specs = {}
  for table in tables:
    rows = table.find_all("tr")
    for row in rows:
      key = row.find("th")
      value = row.find("td")

      if key and value:
        specs[key.text.strip()] = value.text.strip()
  return specs


# main
def run_scraper():
  laptops = scrape_all_listing_pages()

  for laptop in laptops:
    product_page_url = laptop['link']
    specs = scrape_product_page(product_page_url)
    laptop.update(specs)
    
  return laptops

if __name__ == "__main__":
  laptops = run_scraper()
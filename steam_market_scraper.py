import requests
from bs4 import BeautifulSoup
import time
import random

def get_market_items(url, retries=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(retries):
        try:
            time.sleep(random.uniform(5, 10))
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                items = []
                for item in soup.find_all('div', class_='market_listing_row'):
                    try:
                        item_name = item.find('span', class_='market_listing_item_name').text.strip()
                        
                        price_span = item.find('span', class_='normal_price')
                        if price_span:
                            price_text = price_span.get_text(separator="\n").strip()
                            prices = [line.strip() for line in price_text.split('\n') if line.strip().startswith('$')]
                            item_price = ", ".join(prices)
                        else:
                            item_price = "Price not found"
                        
                        items.append((item_name, item_price))
                    except AttributeError as e:
                        print(f"Error parsing item: {e}")
                        continue
                
                return items
            elif response.status_code == 429:
                print(f"Rate limited (429). Retrying in {10 * (attempt + 1)} seconds...")
                time.sleep(10 * (attempt + 1))
            else:
                print(f"Failed to retrieve data for {url}: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying...")
            time.sleep(10 * (attempt + 1))
    
    print(f"Max retries reached for {url}. Skipping...")
    return []

def get_items_from_urls(urls):
    all_items = {}
    
    for url in urls:
        print(f"Fetching items from URL: {url}")
        
        items = get_market_items(url)
        all_items[url] = items
    
    return all_items

if __name__ == "__main__":
    urls = [
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22KSCERATO+%28Gold%29+Stockholm+2021%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22VINI+%28Gold%29+Stockholm+2021%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22yuurih+%28Gold%29+Stockholm+2021%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22drop+%28Gold%29+Stockholm+2021%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22VINI+%28Gold%29+Antwerp+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22FalleN+%28Gold%29+Antwerp+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22fnx+%28Gold%29+Antwerp+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22boltz+%28Gold%29+Antwerp+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22WOOD7+%28Gold%29+Antwerp+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22JOTA+%28Gold%29+Antwerp+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22arT+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22FalleN+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22vini+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22KSCERATO+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22TRY+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22coldzera+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22fer+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22taco+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22yuurih+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22saffee+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22latto+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22dumau+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22drop+%28Gold%29+Rio+2022%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22v%24m+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22arT+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22KSCERATO+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22yuurih+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22drop+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22saffee+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22WOOD7+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22History+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22felps+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22Lucaozy+%28Gold%29+Paris+2023%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22FalleN+%28Gold%29+Copenhagen+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22arT+%28Gold%29+Copenhagen+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22chelo+%28Gold%29+Copenhagen+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22yuurih+%28Gold%29+Copenhagen+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22chelo+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22KSCERATO+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22biguzera+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22saffee+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22lux+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22snow+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22skullz+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22yuurih+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22insani+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22exit+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22kauez+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22VINI+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22decenty+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22NQZ+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22felps+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22TRY+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22drop+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22noway+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22brnz4n+%28Gold%29+Shanghai+2024%22",
        "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22FalleN+%28Gold%29+Shanghai+2024%22"
    ]
    
    all_items = get_items_from_urls(urls)
    
    for url, items in all_items.items():
        print(f"\nItems from URL: {url}")
        for item_name, item_price in items:
            print(f"Item: {item_name}, Price: {item_price}")
        print("-" * 50)
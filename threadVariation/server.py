import socket
import json
import requests
from bs4 import BeautifulSoup
import time
import random
from concurrent.futures import ThreadPoolExecutor

HOST = '127.0.0.1'
PORT = 65432

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
]

def is_blocked_page(html):
    blocked_keywords = ['captcha', 'access denied', 'try again later', 'error']
    html_lower = html.lower()
    return any(keyword in html_lower for keyword in blocked_keywords)

def get_market_items(url):
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        time.sleep(random.uniform(8, 12))
        response = requests.get(url, headers=headers, timeout=30)
        items = []

        if response.status_code == 200:
            if is_blocked_page(response.text):
                return {url: [("Error", "Blocked by Steam - captcha or access denied")]}

            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all('div', class_='market_listing_row'):
                try:
                    item_name = item.find('span', class_='market_listing_item_name').text.strip()
                    price_span = item.find('span', class_='normal_price')

                    if price_span:
                        price_text = price_span.get_text(separator="\n").strip()
                        prices = [line.strip() for line in price_text.split('\n') if line.strip().startswith('$')]
                        item_price = prices[0] if prices else "Price not found"
                    else:
                        item_price = "Price not found"

                    items.append((item_name, item_price))
                except Exception:
                    continue
            return {url: items}
        elif response.status_code == 429:
            return {url: [("Error", "Rate limited by Steam (429)")]}

        return {url: [("Error", f"HTTP status {response.status_code}")]}
    except Exception as e:
        return {url: [("Error", str(e))]}

def handle_client(conn):
    data = conn.recv(4096).decode()
    urls = json.loads(data)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_market_items, urls))

    response = {}
    for result in results:
        response.update(result)
    conn.sendall(json.dumps(response).encode())
    conn.close()

def start_server():
    print("Servidor iniciado...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            print(f"Conexão de {addr}")
            handle_client(conn)

if __name__ == "__main__":
    start_server()

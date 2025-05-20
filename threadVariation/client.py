import socket
import json

HOST = '127.0.0.1'
PORT = 65432

urls = [
    "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22KSCERATO+%28Gold%29+Stockholm+2021%22",
    "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22VINI+%28Gold%29+Stockholm+2021%22",
    "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22drop+%28Gold%29+Stockholm+2021%22",
    "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22VINI+%28Gold%29+Antwerp+2022%22",
    "https://steamcommunity.com/market/search?descriptions=1&category_730_ItemSet%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=&q=%22FalleN+%28Gold%29+Antwerp+2022%22"
]

def fetch_from_server(urls):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(urls).encode())
        data = s.recv(16384).decode()
        return json.loads(data)

if __name__ == "__main__":
    results = fetch_from_server(urls)

    for url, items in results.items():
        print(f"\nItems from URL: {url}")
        for item_name, item_price in items:
            print(f"Item: {item_name}, Price: {item_price}")
        print("-" * 50)

import requests
from bs4 import BeautifulSoup
import time
import json

# Configuration
VINTED_URL = "https://www.vinted.fr/api/v2/catalog/items?brand_id=88&order=newest_first&per_page=5&time="
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1368651642194624532/o30jr76nxEUXg-eZPzWpZbGWAppehLI9VQhBNoMvaoBJyaRXtXJ4dWbq5dkjBqoMkA8K"
LAST_ITEMS_FILE = "last_items.json"  # Fichier pour éviter les doublons

def load_last_items():
    try:
        with open(LAST_ITEMS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_last_items(items):
    with open(LAST_ITEMS_FILE, "w") as f:
        json.dump(items, f)

def get_new_items():
    response = requests.get(VINTED_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = []
    
    # Sélecteur à adapter selon Vinted (inspectez la page)
    for item in soup.find_all("div", class_="feed-grid__item"):  
        title = item.find("h3").text.strip() if item.find("h3") else "Titre non trouvé"
        price = item.find("span", class_="price").text.strip() if item.find("span", class_="price") else "Prix non trouvé"
        link = "https://www.vinted.fr" + item.find("a")["href"] if item.find("a") else "#"
        
        items.append({
            "title": title,
            "price": price,
            "link": link
        })
    
    return items

def send_to_discord(item):
    payload = {
        "embeds": [{
            "title": item["title"],
            "description": f"Prix: {item['price']}",
            "url": item["link"],
            "color": 0x00ff00  # Couleur verte
        }]
    }
    requests.post(DISCORD_WEBHOOK, json=payload)

def main():
    last_items = load_last_items()
    current_items = get_new_items()
    new_items = [item for item in current_items if item not in last_items]
    
    if new_items:
        for item in new_items:
            send_to_discord(item)
        save_last_items(current_items)
    else:
        print("Aucun nouvel article trouvé.")

if __name__ == "__main__":
    main()

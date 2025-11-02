# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def scrape_vinted(query="hotwheels", max_items=30):
    url = f"https://www.vinted.pl/catalog?search_text={query}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    items = []

    # nowy, aktualny selektor dla 2025 HTML Vinted
    selected_items = soup.select('a[href^="/item/"]')[:max_items]
    print(f"[DEBUG] {query}: znaleziono {len(selected_items)} ofert", flush=True)

    for a in selected_items:
        title_elem = a.select_one("div[class*='ItemTile_title']")
        price_elem = a.select_one("div[class*='ItemTile_price']")
        title = title_elem.get_text(strip=True) if title_elem else ""
        price = price_elem.get_text(strip=True) if price_elem else ""
        href = a.get("href", "")
        full_link = "https://www.vinted.pl" + href if href.startswith("/") else href
        items.append({"title": title, "price": price, "link": full_link})

    print(f"[DEBUG] {query}: zapisano {len(items)} ofert do listy", flush=True)
    return items

if __name__ == "__main__":
    queries = ["hotwheels", "nike", "lego"]  # zmień lub dodaj inne
    all_items = []
    for q in queries:
        try:
            items = scrape_vinted(q, max_items=15)
            all_items.extend(items)
        except Exception as e:
            print("Scrape error for", q, e, flush=True)

    # zapis do okazje.json
    try:
        with open("okazje.json", "w", encoding="utf-8") as f:
            json.dump(all_items, f, ensure_ascii=False, indent=2)
        print("Zapisano okazje.json:", len(all_items), flush=True)
    except Exception as e:
        print("Błąd zapisu:", e, flush=True)

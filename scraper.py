# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/100 Safari/537.36"}

def scrape_vinted(query="hotwheels", max_items=30):
    url = f"https://www.vinted.pl/catalog?search_text={query}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    items = []
    # selektor może się zmienić — to prosta heurystyka
    for it in soup.select(".catalog-grid__item")[:max_items]:
        a = it.select_one("a.catalog-item__link")
        if not a:
            continue
        title = a.get_text(strip=True)
        price_elem = it.select_one(".catalog-item__price")
        price = price_elem.get_text(strip=True) if price_elem else ""
        href = a.get("href", "")
        full_link = "https://www.vinted.pl" + href if href.startswith("/") else href
        items.append({"title": title, "price": price, "link": full_link})
        time.sleep(0.1)  # lekki throttling
    return items

if __name__ == "__main__":
    queries = ["hotwheels", "nike", "lego"]  # możesz zmienić
    all_items = []
    for q in queries:
        try:
            items = scrape_vinted(q, max_items=15)
            all_items.extend(items)
        except Exception as e:
            print("Scrape error for", q, e)
    # zapis do okazje.json
    try:
        with open("okazje.json", "w", encoding="utf-8") as f:
            json.dump(all_items, f, ensure_ascii=False, indent=2)
        print("Zapisano okazje.json:", len(all_items))
    except Exception as e:
        print("Błąd zapisu:", e)

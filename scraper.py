import requests
from bs4 import BeautifulSoup
import json

def scrape_vinted(query="hotwheels"):
    url = f"https://www.vinted.pl/catalog?search_text={query}"
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    items = []
    for it in soup.select(".catalog-grid__item")[:30]:
        a = it.select_one("a.catalog-item__link")
        title = a.get_text(strip=True)
        price = it.select_one(".catalog-item__price").get_text(strip=True) if it.select_one(".catalog-item__price") else ""
        href = a["href"]
        items.append({"title": title, "price": price, "link": "https://www.vinted.pl"+href})
    return items

if __name__ == "__main__":
    data = scrape_vinted("hotwheels")
    with open("okazje.json","w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

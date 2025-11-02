const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const queries = ["hotwheels","nike","lego"];
  let allItems = [];

  for (let q of queries) {
    await page.goto(`https://www.vinted.pl/catalog?search_text=${q}`, {waitUntil: 'networkidle'});
    const items = await page.$$eval('a[href^="/item/"]', els => {
      return els.slice(0,15).map(el => {
        const title = el.querySelector('div[class*="ItemTile_title"]')?.innerText || "";
        const price = el.querySelector('div[class*="ItemTile_price"]')?.innerText || "";
        const link = "https://www.vinted.pl" + el.getAttribute('href');
        return {title, price, link};
      });
    });
    allItems.push(...items);
  }

  fs.writeFileSync('okazje.json', JSON.stringify(allItems, null, 2));
  await browser.close();
})();

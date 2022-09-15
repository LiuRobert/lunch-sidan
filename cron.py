import scrapers.brandstation
import scrapers.bryners
import scrapers.estreet
import scrapers.invito
import scrapers.qbar
import json
import os

scraper_list = []
scraper_list.append(scrapers.brandstation.Scraper())
scraper_list.append(scrapers.bryners.Scraper())
scraper_list.append(scrapers.estreet.Scraper())
scraper_list.append(scrapers.invito.Scraper())
scraper_list.append(scrapers.qbar.Scraper())


menus = []
useCached = False

for scraper in scraper_list:
    try:
        menu = scraper.scrape(useCached)
        menus.append(menu)
    except Exception as e:
        menus.append({
            "name": scraper.name,
            "failed": True,
            "error": str(e)
        })

directory = os.path.dirname(os.path.abspath(__file__))
menu_path = os.path.normpath(os.path.join(directory, "static/menus.json"))

with open(menu_path, "w", encoding="utf-8") as f:
    json.dump(menus, f, ensure_ascii=False)

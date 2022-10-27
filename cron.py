import scrapers.brandstation
import scrapers.bryners
import scrapers.estreet
import scrapers.firsthotel
import scrapers.invito
import scrapers.qbar
from datetime import datetime;
import json
import os

scraper_list = []
scraper_list.append(scrapers.brandstation.Scraper())
scraper_list.append(scrapers.bryners.Scraper())
scraper_list.append(scrapers.estreet.Scraper())
scraper_list.append(scrapers.firsthotel.Scraper())
scraper_list.append(scrapers.invito.Scraper())
scraper_list.append(scrapers.qbar.Scraper())


menus = {"updated": datetime.today().strftime("%Y-%m-%d"), "menus": []}
useCached = False

for scraper in scraper_list:
    try:
        menu = scraper.scrape(useCached)
        menus["menus"].append(menu)
    except Exception as e:
        print("Scraper " + scraper.name + " failed")
        print(e)

directory = os.path.dirname(os.path.abspath(__file__))
menu_path = os.path.normpath(os.path.join(directory, "static/menus.json"))

with open(menu_path, "w", encoding="utf-8") as f:
    json.dump(menus, f, ensure_ascii=False)

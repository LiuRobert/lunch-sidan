from scrapers.helpers.base_scraper import Base_Scraper
import scrapers.helpers.util as util
from bs4 import BeautifulSoup

class Scraper(Base_Scraper):
    def __init__(self):
        super().__init__("Invito")

    def scrape(self, useFile: bool):
        adress = "https://invitobar.se/lunchmeny/"
        if useFile:
            text = util.cached_request(adress, "invito")
        else:
            text = util.request(adress)
        soup = BeautifulSoup(text, "html5lib")
        template = util.get_template(self.name)
        template["menu"]["monday"] = _get_dag_menu(soup, "Måndag")
        template["menu"]["tuesday"] = _get_dag_menu(soup, "Tisdag")
        template["menu"]["wednesday"] = _get_dag_menu(soup, "Onsdag")
        template["menu"]["thursday"] = _get_dag_menu(soup, "Torsdag")
        template["menu"]["friday"] = _get_dag_menu(soup, "Fredag")
        return template
        

def _get_dag_menu(soup, dag):
    items = []
    dagHeader = soup.find("h2", text=dag)
    for item in dagHeader.parent.parent.findNextSibling().findAll("span"):
        items.append(item.text)
    return items
    
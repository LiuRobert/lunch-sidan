from scrapers.helpers.base_scraper import Base_Scraper
import scrapers.helpers.util as util
from bs4 import BeautifulSoup

class Scraper(Base_Scraper):
    def __init__(self):
        super().__init__("Innergården")

    def scrape(self, useFile: bool):
        adress = "http://www.innergarden.se/#lunchmeny"
        if useFile:
            text = util.cached_request(adress, "innergarden", encoding="ISO-8859-1")
        else:
            text = util.request(adress)
        text = text.encode("iso-8859-1").decode("utf-8")
        soup = BeautifulSoup(text, "html5lib")
        meny = soup.find(id="lunchmeny").p.children
        template = util.get_template(self.name)

        current_list = None
        for m in meny:
            if m.text.startswith("Måndag:"):
                current_list = template["menu"]["monday"]
            elif m.text.startswith("Tisdag:"):
                current_list = template["menu"]["tuesday"]
            elif m.text.startswith("Onsdag:"):
                current_list = template["menu"]["wednesday"]
            elif m.text.startswith("Torsdag:"):
                current_list = template["menu"]["thursday"]
            elif m.text.startswith("Fredag:"):
                current_list = template["menu"]["friday"]
            elif m.text.startswith("*"):
                current_list.append(util.clean(m.text))
        return template

from scrapers.helpers.base_scraper import Base_Scraper
import scrapers.helpers.util as util
from html.parser import HTMLParser

class Scraper(Base_Scraper):
    def __init__(self):
        super().__init__("Bryners")

    def scrape(self, useFile: bool):
        adress = "https://bryners.se/veckans-lunch-v-j/"
        if useFile:
            text = util.cached_request(adress, "bryners")
        else:
            text = util.request(adress)
        # Bryners har fel encoding
        text = text.encode("iso-8859-1").decode("utf-8")
        parser = _Parser()
        parser.feed(text)
        template = util.get_template(self.name)
        counter = 0
        for week_day in util.get_week_days():
            template["menu"][week_day] = []
            template["menu"][week_day].extend(parser.day_menu[counter])
            counter += 1
        return template
        

class _Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found_day = False
        self.in_day_div = False
        self.day_menu = []
        self.week_day = -1

    def handle_data(self, data):
        # data.strip() checks for string wiithout characters
        if self.in_day_div and data.strip():
            self.day_menu[self.week_day].append(util.clean(data))

        if data.lower().startswith("måndag") or data.lower().startswith("tisdag") or data.lower().startswith("onsdag") or data.lower().startswith("torsdag") or data.lower().startswith("fredag"):
            self.found_day = True
            self.week_day += 1
            self.day_menu.append([])

    def handle_starttag(self, tag, attrs):
        if self.found_day and tag == "ul":
            self.found_day = False
            self.in_day_div = True

    def handle_endtag(self, tag):
        if tag == "ul":
            self.in_day_div = False

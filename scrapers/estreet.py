from scrapers.helpers.base_scraper import Base_Scraper
from html.parser import HTMLParser
import scrapers.helpers.util as util

class Scraper(Base_Scraper):
    def __init__(self):
        super().__init__("E street")

    def scrape(self, useCached: bool):
        adress = "https://www.estreet.nu/"
        if useCached:
            text = util.cached_request(adress, "estreet")
        else:
            text = util.request(adress)
        parser = _Parser()
        parser.feed(text)
        template = util.get_template(self.name)
        counter = 0
        for week_day in util.get_week_days():
            template["menu"][week_day] = []
            template["menu"][week_day].extend(parser.day_menu[counter])
            template["menu"][week_day].extend(parser.week_menu)
            counter += 1
        return template

class _Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found_day = False
        self.in_day_div = False
        self.found_weekly = False
        self.in_weekly_div = False
        self.day_menu = []
        self.week_menu = []
        self.week_day = -1
        self.week_menu_index = -1

    def handle_data(self, data):
        if self.in_day_div and data.strip():
            self.day_menu[self.week_day].append(util.clean(data))
        elif self.in_weekly_div and data.strip():
            self.week_menu[self.week_menu_index] += util.clean(data) + " "

        if data.lower() == "måndag" or data.lower() == "tisdag" or data.lower() == "onsdag" or data.lower() == "torsdag" or data.lower() == "fredag":
            self.found_day = True
            self.week_day += 1
            self.day_menu.append([])
        elif data.lower() == "veckans sallad" or data.lower() == "veckans vegetariska" or data.lower() == "veckans soppa":
            self.found_weekly = True
            self.week_menu_index += 1
            self.week_menu.append("")

    def handle_starttag(self, tag, attrs):
        if self.found_day:
            self.found_day = False
            self.in_day_div = True
        elif self.found_weekly and tag == "div":
            self.found_weekly = False
            self.in_weekly_div = True

    def handle_endtag(self, tag):
        self.in_day_div = False
        if self.in_weekly_div and tag == "div":
            self.in_weekly_div = False

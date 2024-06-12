from scrapers.helpers.base_scraper import Base_Scraper
import scrapers.helpers.util as util
from bs4 import BeautifulSoup
import html
import json

class Scraper(Base_Scraper):
    def __init__(self):
        super().__init__("First Hotel")

    def scrape(self, useFile: bool):
        adress = "https://www.matochmat.se/rest/menu/?restaurant=NbkeCSpNxYWWMPoxz8xxFw%3D%3D"
        if useFile:
            text = util.cached_request(adress, "first_hotel", file_ending="json")
        else:
            text = util.request(adress)

        data = json.loads(text)
        template = util.get_template(self.name)
        days = util.get_week_days()
        counter = 0
        for dag in ["mandag", "tisdag", "onsdag", "torsdag", "fredag"]:
            for course in data.get("data").get("raw")[0].get("content").get(dag):
                template["menu"][days[counter]].append(html.unescape(course.get("name")) + " " + html.unescape(course.get("description")))
            counter += 1
        return template

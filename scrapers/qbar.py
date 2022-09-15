from scrapers.helpers.base_scraper import Base_Scraper
import scrapers.helpers.util as util
import json

class Scraper(Base_Scraper):
    def __init__(self):
        super().__init__("q.bar")

    def scrape(self, useFile: bool):
        adress = "https://www.matochmat.se/rest/menu/?restaurant=Ia9qLjffoXXLoJo%2BvhPjkw%3D%3D"
        if useFile:
            text = util.cached_request(adress, "q.bar", file_ending="json")
        else:
            text = util.request(adress)
        data = json.loads(text)
        template = util.get_template(self.name)
        days = util.get_week_days()
        counter = 0
        for dag in ["mandag", "tisdag", "onsdag", "torsdag", "fredag"]:
            for course in data.get("data").get("raw")[0].get("content").get(dag):
                template["menu"][days[counter]].append(course.get("name") + " " + course.get("description"))
            counter += 1
        return template
        

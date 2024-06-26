import copy
import re
import os
import requests

def get_template(name: str):
    template = copy.deepcopy(_template)
    template["name"] = name
    return template


def get_week_days():
    return ["monday", "tuesday", "wednesday", "thursday", "friday"]


def clean(text: str) -> str:
    text = re.sub(r'[^A-Z|a-z|åäöÅÄÖéÉèÈ,. &/-]+', '', text)
    return text.strip()


def request(adress: str) -> str:
    # we are chrome
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    res = requests.get(adress, headers=headers)
    return res.text


# returns the cached request or makes a request and caches it
def cached_request(adress: str, name: str, file_ending="html", encoding="utf-8") -> str:
    temp_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tempfiles")
    if not os.path.isdir(temp_folder):
        os.mkdir(temp_folder)
    path = os.path.join(temp_folder, name + "." + file_ending)
    if os.path.isfile(path):
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    else:
        return _save_request(adress, path, encoding)


def _save_request(adress: str, path: str, encoding: str) -> str:
    text = request(adress)
    with open(path, "w", encoding=encoding) as f:
        f.write(text)
    return text


_template = {
    "name": "",
    "menu": 
    {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": []
    }
}
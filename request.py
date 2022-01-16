import requests
from bs4 import BeautifulSoup as bs4


def valid_response(r: requests.Response) -> bool:
    return str(r) == "<Response [200]>"


def fetch_link(link: str):
    r = requests.get(link)
    if valid_response(r):
        html_text = r.text
        soup = bs4(html_text, 'html.parser')  # create soup instance
        return soup
    else:
        return None

from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd

from utils import parse_wiki_multiple

if __name__ == '__main__':

    links = [
        "https://en.wikipedia.org/wiki/Category:21st-century_presidents_of_the_United_States",
        "https://en.wikipedia.org/wiki/Category:21st-century_vice_presidents_of_the_United_States",
        "https://en.wikipedia.org/wiki/Category:20th-century_presidents_of_the_United_States",
        "https://en.wikipedia.org/wiki/Category:20th-century_vice_presidents_of_the_United_States",
        "https://en.wikipedia.org/wiki/Category:20th-century_vice_presidents_of_the_United_States",
        "https://en.wikipedia.org/wiki/Category:19th-century_vice_presidents_of_the_United_States"
    ]

    for link in links:
        parse_wiki_multiple(link) # call this function to parse any wiki link

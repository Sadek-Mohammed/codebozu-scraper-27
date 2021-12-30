from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd

from utils import parse_wiki_multiple
from politico import parse_trump

if __name__ == '__main__':
    parse_trump("https://www.politico.com/news/magazine/2021/01/18/trump-presidency-administration-biggest-impact-policy-analysis-451479")

    # links = [
    #     "https://en.wikipedia.org/wiki/Category:21st-century_presidents_of_the_United_States",
    #     "https://en.wikipedia.org/wiki/Category:21st-century_vice_presidents_of_the_United_States",
    #     "https://en.wikipedia.org/wiki/Category:20th-century_presidents_of_the_United_States",
    #     "https://en.wikipedia.org/wiki/Category:20th-century_vice_presidents_of_the_United_States",
    #     "https://en.wikipedia.org/wiki/Category:20th-century_vice_presidents_of_the_United_States",
    #     "https://en.wikipedia.org/wiki/Category:19th-century_vice_presidents_of_the_United_States"
    # ]
    #
    # # """
    # for link in links:
    #     parse_wiki_multiple(link)  # call this function to parse any wiki link
    # """
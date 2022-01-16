import pandas as pd
import time

from bs4 import BeautifulSoup
from sentiment import analyze_sent
from request import fetch_link

# cnn is rendered dynamically so I must use selenium to scrape it
from selenium import webdriver

stories_dict = {}


def init(politician_list: list):
    for politician in politician_list:
        stories_dict[politician] = {"title": [], "story": [], "pos": []}
        find_by_search(politician)

    cnn_df = pd.DataFrame(stories_dict)
    # changing data frame to csv.
    cnn_df.to_csv("Insights/cnn.csv", index=False)


def analyze_article(url: str, politician: str, index: int) -> None:
    # scraping individual article
    soup = fetch_link(url)
    # print(soup)

    # title
    title = soup.find('h1', attrs={'class', 'pg-headline'})
    if title is not None:

        # story
        story = soup.find('div', attrs={'class', 'l-container'})

        pos = analyze_sent(story.text)['pos']*1000

        stories_dict[politician]['title'].append(title.text)
        stories_dict[politician]['story'].append(story.text)
        stories_dict[politician]['pos'].append(pos)


def find_by_search(keyword: str) -> None:
    url = f"https://edition.cnn.com/search?q={keyword}&size=20&from=10&page=1"

    """
    https://sites.google.com/chromium.org/driver/
    Place this file into this directory
    """

    browser = webdriver.Chrome()
    browser.get(url)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    articles = soup.find_all('h3', attrs={'class': 'cnn-search__result-headline'})

    index = 0  # indexing my dictionary per story
    for article in articles:
        analyze_article(f"https:{article.a['href']}", keyword, index)
        index += 1

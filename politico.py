from bs4 import BeautifulSoup as bs4
from error import valid_response
from math import floor
import requests
import pandas as pd

trumps = []
columns = ['Things', 'Move', 'Impact', 'Upshot']

for i in range(0, 30):
    trumps.append([])


def parse_trump(link):
    r = requests.get(link)
    html_text = r.text
    soup = bs4(html_text, 'html.parser')
    things = soup.find_all('h3', attrs={'class': 'story-text__heading-medium'})
    counter = 0
    for thing in things:
        trumps[counter].append(thing.text)
        counter += 1
    stories = soup.find_all("div", attrs={'class': 'story-text'})
    sub = 0
    counter = 0
    x = ''
    for story in stories:
        for pStory in story.find_all("p", attrs={'class': 'story-text__paragraph'}):
            if pStory.find("span") is not None:
                span_text = pStory.find("span").text
                if span_text == "The move:":
                    x = pStory.text.replace("The move: ", "")
                    sub += 1
                    trumps[counter].append(x)
                if span_text == "The impact:":
                    x = pStory.text.replace("The impact: ", "")
                    sub += 1
                    trumps[counter].append(x)
                if span_text == "The upshot:":
                    x = pStory.text.replace("The upshot: ", "")
                    sub += 1
                    trumps[counter].append(x)
                if sub == 3:
                    sub = 0
                    counter += 1
            elif pStory.find("b") is not None:
                b_text = pStory.find("b").text
                if b_text == "The move:":
                    x = pStory.text.replace("The move: ", "")
                    sub += 1
                    trumps[counter].append(x)
                if b_text == "The impact:":
                    x = pStory.text.replace("The impact: ", "")
                    sub += 1
                    trumps[counter].append(x)
                if b_text == "The upshot: ":
                    x = pStory.text.replace("The upshot: ", "")
                    sub += 1
                    trumps[counter].append(x)
                if sub == 3:
                    sub = 0
                    counter += 1

    for trump in trumps:
        print(trump)


data = pd.DataFrame([], columns)

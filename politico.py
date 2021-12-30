from math import floor
from typing import Dict, List, Any

from bs4 import BeautifulSoup as bs4
from error import valid_response
import requests
import pandas as pd

trumps: dict[str, list[Any]] = {'Things': [], "Move": [], "Impact": [], "Upshot": []}
columns = ['Things', 'Move', 'Impact', 'Upshot']

isMove = False
for i in range(0, 30):
    trumps['Things'].append([])
    trumps['Move'].append([])
    trumps['Impact'].append([])
    trumps['Upshot'].append([])


def parse_trump(link):
    global isMove
    r = requests.get(link)
    html_text = r.text
    print(r.status_code)
    soup = bs4(html_text, 'html.parser')
    things = soup.find_all('h3', attrs={'class': 'story-text__heading-medium'})
    counter = 0
    for thing in things:
        trumps['Things'][counter] = thing.text
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
                    if isMove:
                        trumps["Move"][counter] += "  |  "
                        trumps["Move"][counter] += x
                    else:
                        trumps["Move"][counter] = x
                    isMove = True
                if span_text == "The impact:":
                    x = pStory.text.replace("The impact: ", "")
                    sub += 1
                    isMove = False
                    trumps["Impact"][counter] = x
                if span_text == "The upshot:":
                    x = pStory.text.replace("The upshot: ", "")
                    sub += 1
                    isMove = False
                    trumps["Upshot"][counter] = x
                if sub == 3:
                    sub = 0
                    isMove = False
                    counter += 1
            elif pStory.find("b") is not None:
                b_text = pStory.find("b").text
                if b_text == "The move:":
                    x = pStory.text.replace("The move: ", "")
                    sub += 1
                    if isMove:
                        trumps["Move"][counter] += "  |  "
                        trumps["Move"][counter] += x
                    else:
                        trumps["Move"][counter] = x
                    isMove = True
                if b_text == "The impact:":
                    x = pStory.text.replace("The impact: ", "")
                    sub += 1
                    isMove = False
                    trumps["Impact"][counter] = x
                if b_text == "The upshot: ":
                    x = pStory.text.replace("The upshot: ", "")
                    sub += 1
                    isMove = False
                    trumps["Upshot"][counter] = x
                if sub == 3:
                    sub = 0
                    counter += 1
    for key in trumps.keys():
        for i in range(0, 30):
            if trumps[key][i] == []:
                trumps[key][i] = "is not declared"
    print(trumps)
    for key in trumps.keys():
        print(len(trumps[key]))
    data = pd.DataFrame(trumps)
    data.to_csv("donald.csv", index=False)
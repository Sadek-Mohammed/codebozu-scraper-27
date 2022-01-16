# import the typing library for best practices in coding (suggested by pycharm
from typing import Any
# import the sentiment analysis function
# import pandas for csv file writing
import pandas as pd
from sentiment import analyze_sent
from request import fetch_link
stories_trump: dict[str, list[Any]] = {"title": [], "story": [], "pos": []}
for one in range(0, 19):
    stories_trump['title'].append([])
    stories_trump['story'].append([])
    stories_trump['pos'].append([])


def avg_cal(array):
    sum = 0
    count = len(array)
    for ele in array:
        sum += ele
    sum /= count
    return sum

def get_dm_single(link):
    soup = fetch_link(link)
    if soup is None:
        return
    text = ""
    for paragraph in soup.find_all("p", attrs={"class": "mol-para-with-font"}):
        text += paragraph.text
    return text


def get_dm_multi(link):
    soup = fetch_link(link)
    if soup is None:
        return
    stories = soup.find_all("div", itemprop={"itemListElement"})
    for i in range(0, 19):
        story = stories[i]
        story_a = story.find("a")
        title = story_a.get("href")
        stories_trump['title'][i] = title
        story_link = story_a['href']
        story_text = get_dm_single(story_link)
        if story_text is None:
            print("invalid link")
            continue
        stories_trump['story'][i] = story_text
        pos = analyze_sent(story_text)
        stories_trump['pos'][i] = pos['pos']
    # print(stories_trump)
    dm_table = pd.DataFrame(stories_trump)
    # changing data frame to csv.
    dm_table.to_csv("dm.csv", index=False)
    print("positivity score of trump by Daily Mail is " + str(round(avg_cal(stories_trump['pos']), 3)))

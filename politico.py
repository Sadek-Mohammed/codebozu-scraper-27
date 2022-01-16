# import the typing library for best practices in coding (suggested by pycharm
from typing import Any
# import the beautiful soup library for scraping
from bs4 import BeautifulSoup as bs4
# import the requests library for fetching HTML from websites.
import requests
# import pandas for csv file writing
import pandas as pd
# import the response validating function from the request.py file
from request import fetch_link
# import the needed library to generate the positivity and negativity values for analyzing the media preference
from tables import generate_data


# add the trumps dictionary that will store data, where that dict part is suggested by pycharm.
trumps = {'Things': [], "Move": [], "Impact": [], "Upshot": []}
# columns is the variable holding the names of the columns of the csv file.
columns = ['Things', 'Move', 'Impact', 'Upshot']
# The purpose of this variable is to ensure that multiple consecutive "The move" spans are dealt as a single column.
isMove = False


# The purpose of the loop is to ensure that the csv will always include a maximum of 30 columns.
for i in range(0, 30):
    trumps['Things'].append([])
    trumps['Move'].append([])
    trumps['Impact'].append([])
    trumps['Upshot'].append([])


def parse_trump(link):
    # making the global variable accessible in the function
    global isMove
    soup = fetch_link(link)
    if soup is None:
        return
    # searching for the headlines (titles) of the 30 things that trump made.
    things = soup.find_all('h3', attrs={'class': 'story-text__heading-medium'})
    # The counter variable is an indexer to add each title to the appropriate column
    counter = 0
    # looping through each single headline.
    for thing in things:
        # Adding the headlines to the columns of the dict
        trumps['Things'][counter] = thing.text
        # increasing the index in order to adjust the following column
        counter += 1
    # resetting the variables and initializing needed stuff.
    # counter is the variable for counting the added stuff to adjust rows
    counter = 0
    # sub is added so that counter is adding each three sub sections (The move, The impact, and The upshot)
    sub = 0
    # This variable holds the text to be added to each column
    x = ''
    # This div usually holds 3 paragraphs containing the needed data.
    stories = soup.find_all("div", attrs={'class': 'story-text'})
    # Looping through each div to collect the needed stuff.
    for story in stories:
        # Looping through each paragraph in the div (eliminates some divs that do not contain paragraphs - not needed)
        for pStory in story.find_all("p", attrs={'class': 'story-text__paragraph'}):
            # Checking whether there is a span with the needed data or not
            if pStory.find("span") is not None:
                # Adding the text of the span to a variable
                span_text = pStory.find("span").text
                # checking the move case of the span
                if span_text == "The move:":
                    # eliminating the word "The move" from the string
                    x = pStory.text.replace("The move: ", "")
                    # increasing the sub sections count for the use in counter increasing
                    sub += 1
                    # checking for consecutive sections of the Move
                    if isMove:
                        # if consecutive add the new text separated by a separator
                        trumps["Move"][counter] += "  |  "
                        trumps["Move"][counter] += x
                    else:
                        # if not consecutive, just assign the text to the column of the dict
                        trumps["Move"][counter] = x
                    # making the variable true to verify the following section
                    isMove = True
                # checking for the impact case
                if span_text == "The impact:":
                    # replacing the headline of the section
                    x = pStory.text.replace("The impact: ", "")
                    # increase the sub section count
                    sub += 1
                    # make the variable false in order not to miss with the following case.
                    isMove = False
                    # assign the text to the impact column
                    trumps["Impact"][counter] = x
                # do exactly the same for the impact section
                if span_text == "The upshot:":
                    x = pStory.text.replace("The upshot: ", "")
                    sub += 1
                    isMove = False
                    trumps["Upshot"][counter] = x
                # whenever three sub sections have passed
                if sub == 3:
                    # make the sub sections count reset
                    sub = 0
                    # make the move false in order to eliminate the case when the column has no upshot or impact
                    # (ending with the move and the following section starts with the move)
                    isMove = False
                    # increasing the counter count of the row
                    counter += 1
            # doing exactly the same regarding the case when some sections are in <b> tag instead of <span> tag.
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
    # loop upon the cases where there are no collected data, and cause them to have an ambiguous statement
    for key in trumps.keys():
        for i in range(0, 30):
            if not trumps[key][i]:
                trumps[key][i] = "is not declared"
    # printing data for checking
    # print(trumps)
    # for key in trumps.keys():
    #     print(len(trumps[key]))
    # Adding data to a Data frame
    data = pd.DataFrame(trumps)
    # changing data frame to csv.
    data.to_csv("Insights/donald.csv", index=False)
    # Generate the positivity and negativity data
    generate_data(trumps)
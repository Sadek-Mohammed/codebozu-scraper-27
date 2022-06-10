from bs4 import BeautifulSoup as bs4
from request import fetch_link
import requests
import pandas as pd
import os
import sys
import time

president_dict = {'Politician': '',
                  'fname': '',
                  'dob': '',
                  'pob': '',
                  'day': '0',
                  'year': '0',
                  'month': '',
                  'party': '',
                  'numChild': 0}
children = False


def parse_wiki_multiple(link: str) -> None:
    soup = fetch_link(link)
    if soup is None:
        return 
    politicians = soup.find('div', attrs={'class': 'mw-content-ltr'})
    for a_tag in politicians.find_all('a')[5:-1]:
        parse_wiki_page(f"https://en.wikipedia.org{a_tag['href']}")
        time.sleep(1)


def parse_wiki_page(link: str) -> None:
    soup = fetch_link(link)
    if soup is None:
        return
    title = soup.find('h1').text
    print(f"Title: {title}\n")  # printing title
    president_dict['Politician'] = title
    # print(soup.prettify()) or this line (it's 62,000 lines long)

    # get info table
    info_table = soup.find("table", class_="infobox vcard").tbody

    # loop through every row
    for row in info_table.find_all("tr"):
        if len(row.find_all("td")) > 0 and row.find("th") is not None:
            process_thtd(row)
            continue
        if len(row.find_all("td")) > 0 and row.find("td").b is not None:
            continue
        print(f"{row.text}\n")

    df = pd.DataFrame({'Politician': [president_dict['Politician']],
                       'Birth Full Name': [president_dict['fname']],
                       'Date of Birth': [president_dict['dob']],
                       'Place of Birth': [president_dict['pob']],
                       'Political Party': [president_dict['party']],
                       'Day of Birth': [president_dict['day']],
                       'Month of Birth': [president_dict['month']],
                       'Children Number': [president_dict['numChild']],
                       'Year of Birth': [president_dict['year']]})

    df.to_csv('Politicians.csv', mode='a')


# -----------------------------util functions-----------------------------#
def process_thtd(soup) -> None:
    global children
    th_text = soup.find('th').text
    print(f"{th_text}: ")

    born = False
    political = False

    if th_text == 'Born':
        born = True
    elif th_text == 'Political party':
        political = True
    elif th_text == 'Children':
        children = True

    for td in soup.find_all("td"):
        try:
            if td.ul.li.text == "":
                raise AttributeError
            process_ul(td)

        except AttributeError:
            td_str = td.text.split(" ")
            print(td_str)
            count = 0
            date = ''
            if born:
                for i in td_str:
                    for x in i:
                        if ':' > x > '/':
                            count += 1
                            date += x
                    if count > 0:
                        break
                president_dict['fname'] = ' '.join(td_str[0:3])
                president_dict['dob'] = date
                i = president_dict['dob'].split(" ")
                president_dict['year'] = date[0:4]
                president_dict['month'] = date[4:6]
                president_dict['day'] = date[6:8]
                president_dict['pob'] = ' '.join(td_str[8:-1])
            if political:
                president_dict['party'] = td_str[0]
            print(f"{td.text}\n")


def process_ul(soup):
    global children
    if children:
        president_dict['numChild'] = len(soup.find("ul").find_all("li"))
        children = False
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            print(li.text)
    print("\n")

from bs4 import BeautifulSoup as bs4
from error import valid_response
import requests
import pandas as pd
import os
import re
import sys

verbose = True  # enable/disable this for print statements

# blocks print statements depending on the status of verbose
if verbose:
    sys.stdout = sys.__stdout__
else:
    sys.stdout = open(os.devnull, 'w')

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
    r = requests.get(link)

    html_text = r.text

    soup = bs4(html_text, 'html.parser')  # create soup instance

    politicians = soup.find_all('div', attrs={'class': 'mw-content-ltr'})

    for div in politicians:
        print(f"en.wikipedia.org{str(div.a['href'])}")

def parse_wiki_page(link: str) -> None:
    # sending a request to the website
    r = requests.get(link)
    print(r)

    # receiving response
    if valid_response(r):
        print("Status 200 means successful response.\n")
    else:
        print("Unsuccessful response.\n")

    html_text = r.text
    # print(html_text) would not recommend running this line

    soup = bs4(html_text, 'html.parser')  # create soup instance

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
            process_bold(row)
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

    df.to_csv('Politicians.csv', index=False)


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


def process_bold(soup):
    print(f"{soup.b.text}: ")
    for td in soup.find_all("td"):
        print(f"{td.text.replace(soup.b.text, '')}\n")


def process_ul(soup):
    global children
    if children:
        president_dict['numChild'] = len(soup.find("ul").find_all("li"))
        children = False
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            print(li.text)
    print("\n")

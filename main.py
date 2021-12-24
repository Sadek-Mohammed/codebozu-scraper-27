from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd


def parse_wiki_page(link):
    # sending a request to the website
    r = requests.get(link)
    print(r)

    # receiving response
    if str(r) == "<Response [200]>":
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
                       'Political Party': [president_dict['party']]})

    df.to_csv('Politicians.csv', index=False)


# -----------------------------util functions-----------------------------#
def process_thtd(soup) -> None:
    th_text = soup.find('th').text
    print(f"{th_text}: ")

    born = False
    political = False

    if th_text == 'Born':
        born = True
    elif th_text == 'Political party':
        political = True

    for td in soup.find_all("td"):
        try:
            if td.ul.li.text == "":
                raise AttributeError
            process_ul(td)

        except AttributeError:
            td_str = td.text.split(" ")
            if born:
                president_dict['fname'] = ' '.join(td_str[0:3])
                president_dict['dob'] = ' '.join(td_str[4:6])
                president_dict['pob'] = ' '.join(td_str[8:-1])
            if political:
                president_dict['party'] = td_str[0]
            print(f"{td.text}\n")



def process_bold(soup):
    print(f"{soup.b.text}: ")
    for td in soup.find_all("td"):
        print(f"{td.text.replace(soup.b.text, '')}\n")


def process_ul(soup):

    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            print(li.text)
    print("\n")


# ------------------------------------------------------------------------#

if __name__ == '__main__':
    president_dict = {'Politician': '',
                      'fname': '',
                      'dob': '',
                      'pob': '',
                      'party': ''}
    parse_wiki_page("https://en.wikipedia.org/wiki/Donald_Trump")
    # call this function to parse any wiki link

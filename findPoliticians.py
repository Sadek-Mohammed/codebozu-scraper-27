from bs4 import BeautifulSoup as bs4
import requests


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

    print(f"Title: {soup.find('h1').text}\n")  # printing title

    # print(soup.prettify()) or this line (it's 62,000 lines long)

    # get info table
    info_table = soup.find("table", class_="infobox vcard").tbody

    # loop through every row
    for row in info_table.find_all("tr"):
        if len(row.find_all("td")) > 0 and row.find("th") != None:
            process_thtd(row)
            continue
        if len(row.find_all("td")) > 0 and row.find("td").b != None:
            process_bold(row)
            continue
        print(f"{row.text}\n")


# -----------------------------util functions-----------------------------#
def process_thtd(soup):
    print(f"{soup.find('th').text}: ")
    for td in soup.find_all("td"):
        try:
            if td.ul.li.text == "":
                raise AttributeError
            process_ul(td)

        except AttributeError:
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

# Links of pages with politician names
def GetAllLinks():
    parse_wiki_page_names("https://en.wikipedia.org/wiki/Category:21st-century_presidents_of_the_United_States")
    parse_wiki_page_names("https://en.wikipedia.org/wiki/Category:21st-century_vice_presidents_of_the_United_States")
    parse_wiki_page_names("https://en.wikipedia.org/wiki/Category:20th-century_presidents_of_the_United_States")
    parse_wiki_page_names("https://en.wikipedia.org/wiki/Category:20th-century_vice_presidents_of_the_United_States")
    parse_wiki_page_names("https://en.wikipedia.org/wiki/Category:19th-century_vice_presidents_of_the_United_States")


def parse_wiki_page_names(link):
    # requests access to website
    r = requests.get(link)
    print(r)

    html_text = r.text
    # print(html_text)

    soup = bs4(html_text, 'html.parser')  # create soup instance

    # finds the part of the page with politician names
    body = soup.find("div", class_="mw-content-ltr")
    process_href(body)


def process_href(soup):
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            if len(li.find_all("a")) > 0 and li.find("a") != None:
                if li.find_all("a", href=lambda href: href and "/wiki/Category" in href):  # avoids unwanted links
                    continue
                else:
                    parse_wiki_page("https://en.wikipedia.org" + li.a[
                        'href'])  # calls the function to print politician stats with each link
    print("\n")


# ---------------------------------------------------------------#
GetAllLinks()
# call this function to parse any wiki link

from request import fetch_link

def frontpage():
    soup = fetch_link("https://www.foxnews.com/politics")
    for article in soup.find_all("article"):
        print(article.find("div", class_="info").a["href"])

def find_by_search(keyword):
    soup = fetch_link(f"https://www.foxnews.com/search-results/search?q={keyword}")
    print(soup)
    print("collection collection-search active" in str(soup))
    table = soup.find("div", class_="collection collection-search active")
    for article in table.find_all("article"):
        print(article.a["href"])

find_by_search("trump")

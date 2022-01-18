from request import fetch_link
from selenium import webdriver
from bs4 import BeautifulSoup as bs4
from sentiment import analyze_sent
import time
import pandas as pd
import spacy

politicians = [
    "trump",
    "biden",
    "obama",  # what's his last name??????
    "george w. bush",
    "bill clinton"
]

data = {}

in_depth_analysis = False


# unnecessary method - scrapes articles from the front page of Fox News
def frontpage():
    soup = fetch_link("https://www.foxnews.com/politics")
    for article in soup.find_all("article"):
        print(article.find("div", class_="info").a["href"])


# returns a list of articles that are search results for the {keyword}
def find_by_search(keyword):
    soup = bs4(get_selenium_source(f"https://www.foxnews.com/search-results/search?q={keyword}", 3), "html.parser")
    table = soup.find("div", class_="collection collection-search active")
    out = []
    for article in table.find_all("article"):
        out.append(article.a["href"])
    return out


# returns html source code of a webpage {url} after the dynamic js code loads in
# presses the "load more" button {pages} times
def get_selenium_source(url, pages):
    browser = webdriver.Chrome()
    browser.get(url)
    button = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[2]/a")
    time.sleep(1)
    while pages > 1:
        button.click()
        time.sleep(1)
        pages -= 1
    out = browser.page_source
    browser.quit()
    return out


# runs analysis on an article {url} returns (title, text, pos)
def run_analysis(url, politician):
    soup = fetch_link(url)

    try:
        title = soup.find("h1", class_="headline").text
        text = soup.find("div", class_="article-body").text
        text = subject_analysis(text, politician) if in_depth_analysis else text
        pos = analyze_sent(text)['pos'] * 1000
        return (title, text, pos)
    except AttributeError:
        print(url)

    return None

# returns the sentences that have {politician} as a subject
def subject_analysis(text, politician):
    nlp = spacy.load("en_core_web_sm")
    sentences = text.split(".")
    l = []
    for sentence in sentences:
        subjects = [str(tok).lower() for tok in nlp(sentence) if (tok.dep_ == "nsubj")]
        if politician in subjects:
            l.append(sentence)
    out = ""
    for s in l:
        out += (s + ". ")
    return out

# turns dictionary into a data frame, outputs dataframe as a csv
def create_csv():
    pd.DataFrame(data).to_csv("Insights/fox_news.csv", columns=['trump', 'biden', 'obama', 'george w. bush', 'bill clinton'])


# main execution method to scrape info about politicians and Fox News
def fox_news(ida):
    global in_depth_analysis
    in_depth_analysis = ida
    
    for politician in politicians:
        data[politician] = {
            "title": [],
            "story": [],
            "pos": []
        }
        articles = find_by_search(politician)
        for article in articles:
            result = run_analysis(article, politician)
            if result is None:
                continue
            data[politician]["title"].append(result[0])
            data[politician]["story"].append(result[1])
            data[politician]["pos"].append(result[2])

    create_csv()

#Interesting test case code below:
#Notice how the positivity value changes for Donald Trump

#Runs normal analysis
#print("Normal test:", run_analysis("https://www.foxnews.com/politics/trump-arizona-biden-destructive-florence-rally", "trump")[2])

#Runs in depth analysis
#in_depth_analysis = True
#print("In Depth Test:", run_analysis("https://www.foxnews.com/politics/trump-arizona-biden-destructive-florence-rally", "trump")[2])

#Results are printed

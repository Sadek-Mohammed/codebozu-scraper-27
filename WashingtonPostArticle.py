from bs4 import BeautifulSoup as bs4
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#creates the csv
filename = "Insights/WashingtonPost.csv"
headers = "Article Title,Article,pos\n"
#creates heacders for csv

with open(filename, "w", encoding="utf-8") as f:
    f.write(headers)


    def get_article_title(link):
        #sending a request to the website
        r = requests.get(link)

        html_text = r.text
        soup = bs4(html_text, 'html.parser') #create soup instance
        body = soup.find("body")

        #some articles have different formatting
        if(body.find("h1", id= "main-content") != None):
            article_title = body.find("h1", id= "main-content").text
        else:
            article_title = body.find("h1", itemprop= "headline").text

        return article_title

    def get_article_text(link):
        #sending a request to the website
        r = requests.get(link)

        html_text = r.text
        soup = bs4(html_text, 'html.parser') #create soup instance
        body = soup.find("body")
        article_text = body.find("div", class_='article-body').text
        return article_text


    # function to print sentiments of the sentence.
    def sentiment_scores(sentence):
     
        # Create a SentimentIntensityAnalyzer object.
        sid_obj = SentimentIntensityAnalyzer()
     
        sentiment_dict = sid_obj.polarity_scores(sentence)
        return sentiment_dict


    def parse_washington_post_article_names(link):
        article_title = get_article_title(link)
        article_text = get_article_text(link).strip()
        sentiment_dict = sentiment_scores(article_text)

        #gets the positive sentiment score
        positive_sent = sentiment_dict['pos']*100
        
        #adds everything to the csv
        f.write(article_title + "," + article_text.replace(",", "/") + "," + str(positive_sent) + "\n")
        return positive_sent


    #-------------------------------------links----------------------------------#
    #calls all articles to add to csv and gathers the positivity scores to find the average positivity
    #Trump
    avg_trump = 0
    avg_trump += parse_washington_post_article_names("https://www.washingtonpost.com/politics/2021/12/21/trump-january6-anniversary/")
    avg_trump += parse_washington_post_article_names("https://www.washingtonpost.com/nation/2021/12/21/donald-trump-covid-booster/")
    avg_trump += parse_washington_post_article_names("https://www.washingtonpost.com/politics/2022/01/06/course-donald-trump-bears-primary-blame-jan-6/")
    avg_trump += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/letters-to-the-editor/donald-trumps-reverse-scrooge-syndrome/2021/12/08/862d6d30-570a-11ec-8396-5552bef55c3c_story.html")
    avg_trump += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/2021/12/02/donald-trump-superspreader-chief/")
    print(avg_trump / 5, "% positivity")

    #Biden
    avg_biden = 0
    avg_biden += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/2021/06/05/joe-biden-europe-trip-agenda/")
    avg_biden += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/2020/05/11/joe-biden-coronavirus-op-ed/")
    avg_biden += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/2021/12/16/puzzle-joe-bidens-unpopularity/")
    avg_biden += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/2021/12/20/whos-blame-build-back-betters-demise-joe-biden/")
    avg_biden += parse_washington_post_article_names("https://www.washingtonpost.com/news/posteverything/wp/2017/07/17/joe-biden-as-a-nation-we-decided-that-health-care-is-for-all-republicans-want-to-roll-that-back/")
    print(avg_biden / 5, "% positivity")
    
    #Obama
    avg_obama = 0
    avg_obama += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/us-helping-tunisia-to-make-sure-democracy-delivers/2015/05/20/05b029e4-fe75-11e4-833c-a2de05b6b2a4_story.html")
    avg_obama += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/obama-how-we-can-make-our-vision-of-a-world-without-nuclear-weapons-a-reality/2016/03/30/3e156e2c-f693-11e5-9804-537defcc3cf6_story.html")
    avg_obama += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/barack-obama-why-we-must-rethink-solitary-confinement/2016/01/25/29a361f2-c384-11e5-8965-0607e0e265ce_story.html")
    avg_obama += parse_washington_post_article_names("https://www.washingtonpost.com/news/checkpoint/wp/2016/01/06/obama-picks-special-operations-commander-to-lead-centcom/")
    avg_obama += parse_washington_post_article_names("https://www.washingtonpost.com/politics/obama-makes-surprise-visit-to-dc-vaccination-site-amid-polarized-virus-debate/2021/11/30/2e02815e-5205-11ec-8769-2f4ecdf7a2ad_story.html")
    print(avg_obama / 5, "% positivity")

    #George W. Bush
    avg_bush = 0
    avg_bush += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/2021/04/16/george-w-bush-immigration-portraits-out-of-many-one/")
    avg_bush += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/george-w-bush-pepfar-saves-millions-of-lives-in-africa-keep-it-fully-funded/2017/04/07/2089fa46-1ba7-11e7-9887-1a5314b56a08_story.html")
    avg_bush += parse_washington_post_article_names("https://www.washingtonpost.com/politics/bush-liz-cheney-fundraiser/2021/09/22/c9824060-1baa-11ec-a99a-5fea2b2da34b_story.html")
    avg_bush += parse_washington_post_article_names("https://www.washingtonpost.com/politics/2021/09/01/george-w-bush-worst-predictions-about-aghanistan-war/")
    avg_bush += parse_washington_post_article_names("https://www.washingtonpost.com/lifestyle/style/george-w-bush-wars/2021/08/31/72f9dee8-07f4-11ec-8c3f-3526f81b233b_story.html")
    print(avg_bush / 5, "% positivity")

    #Bill Clinton
    avg_clinton = 0
    avg_clinton += parse_washington_post_article_names("https://www.washingtonpost.com/politics/2021/10/17/former-president-bill-clinton-discharged-hospital-after-treatment-infection/")
    avg_clinton += parse_washington_post_article_names("https://www.washingtonpost.com/nation/2020/08/04/bill-clintons-misunderstanding-what-stokely-carmichael-brings-black-americas-long-struggle-freedom/")
    avg_clinton += parse_washington_post_article_names("https://www.washingtonpost.com/outlook/2020/08/18/how-bill-clinton-turned-dreadful-convention-speech-into-political-stardom/")
    avg_clinton += parse_washington_post_article_names("https://www.washingtonpost.com/history/2020/06/26/russian-election-interference-meddling/")
    avg_clinton += parse_washington_post_article_names("https://www.washingtonpost.com/opinions/bill-clinton-its-time-to-overturn-doma/2013/03/07/fc184408-8747-11e2-98a3-b3db6b9ac586_story.html")
    print(avg_clinton / 5, "% positivity")

    f.close()
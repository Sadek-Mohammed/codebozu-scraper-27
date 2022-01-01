# Import the VADER sentiment analyzer from its package
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_sent(text):
    # Add an instance of the analyzer
    sid = SentimentIntensityAnalyzer()
    # Store the analysis scores in a dic
    sentiment_dict = sid.polarity_scores(text)
    # return the scores dictionary
    return sentiment_dict

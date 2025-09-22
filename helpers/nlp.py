from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def determine_sentiment(text):
    score = sia.polarity_scores(text)
    return score["compound"]

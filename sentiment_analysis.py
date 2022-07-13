from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import re
import string
from generate_data.helpers import upload_file

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


def percentage(part,whole):
 return format(100 * float(part)/float(whole), '.1f')

token = os.environ["TWITTER_TOKEN"]
auth = tweepy.OAuth2BearerHandler(token)
api = tweepy.API(auth)

keyword = "@ButternutBox"
tweet_num = 100

tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(tweet_num)
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
positive_list = []
negative_list = []

# upload_file(f'twitter_raw', 'luis-project-twitter-data')

for tweet in tweets:
    tweet_list.append(tweet.text)
    analysis = TextBlob(tweet.text)
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    polarity += analysis.sentiment.polarity

    if neg > pos:
        negative_list.append(tweet.text)
        negative += 1

    elif neg < pos:
        positive_list.append(tweet.text)
        positive += 1
    
    elif neg == pos:
        neutral_list.append(tweet.text)
        neutral += 1

# positive = percentage(positive, tweet_num)
# negative = percentage(negative, tweet_num)
# neutral = percentage(neutral, tweet_num)
# polarity = percentage(polarity, tweet_num)
users_df = pd.DataFrame(tweet_num, columns=['id', 'created_at', 'status', 'paid_at'])

#TODO: Add results to csv file and push to S3
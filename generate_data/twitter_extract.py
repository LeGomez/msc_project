import tweepy
import os
import pandas as pd
from helpers import upload_file

token = os.environ["TWITTER_TOKEN"]
auth = tweepy.OAuth2BearerHandler(token)
api = tweepy.API(auth)

keyword = "@ButternutBox"
tweet_num = 100

tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(tweet_num)
tweet_list = []

for tweet in tweets:
    tweet_list.append([tweet.text, tweet.user, tweet.created_at])

tweets_df = pd.DataFrame(tweet_list, columns=['text', 'user', 'created_at'])

tweets_df.to_csv(
    'tweet_history.csv',
    header=True,
    index=False
)

upload_file(f'tweet_history.csv', 'luis-project-twitter-data')



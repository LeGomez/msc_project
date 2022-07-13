import tweepy
import os

token = os.environ["TWITTER_TOKEN"]
auth = tweepy.OAuth2BearerHandler(token)
api = tweepy.API(auth)

keyword = "@ButternutBox"
tweet_num = 100

tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(tweet_num)
tweet_list = []

for tweet in tweets:
    tweet_list.append([tweet.text, tweet.created_at])





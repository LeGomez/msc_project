from textblob import TextBlob
import pandas as pd
import os
import boto3
from generate_data.helpers import upload_file
from io import BytesIO
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def percentage(part,whole):
 return format(100 * float(part)/float(whole), '.1f')

bucket = 'luis-project-twitter-data'
file = 'tweets.csv'

s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

response = s3_client.get_object(Bucket=bucket, Key=file)
data = response['Body'].read()

tweets = pd.read_csv(BytesIO(data))

tweets['created_at'] = pd.to_datetime(tweets['created_at']).dt.date
tweets['created_at'] = tweets['created_at'].astype("string")



positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
positive_list = []
negative_list = []
daily_results = {}

for index, tweet in tweets.iterrows():
    tweet_list.append([tweet['text'], tweet['created_at']])
    analysis = TextBlob(tweet['text'])
    score = SentimentIntensityAnalyzer().polarity_scores(tweet['text'])
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    polarity += analysis.sentiment.polarity

    if neg > pos:
        if tweet['created_at'] in daily_results:
            daily_results[tweet['created_at']][0] += 1
        else:
            daily_results[tweet['created_at']] = [1, 0, 0]
        negative += 1

    elif neg < pos:
        if tweet['created_at'] in daily_results:
            daily_results[tweet['created_at']][1] += 1
        else:
            daily_results[tweet['created_at']] = [0, 1, 0]
        positive += 1
    
    elif neg == pos:
        if tweet['created_at'] in daily_results:
            daily_results[tweet['created_at']][2] += 1
        else:
            daily_results[tweet['created_at']] = [0, 0, 1]
        neutral += 1

# positive = percentage(positive, tweet_num)
# negative = percentage(negative, tweet_num)
# neutral = percentage(neutral, tweet_num)
# polarity = percentage(polarity, tweet_num)
print(f'Positive={positive}, negative={negative}, neutral={neutral}')
print(len(tweets))

results = pd.DataFrame.from_dict(daily_results, orient='index', columns=['negative', 'positive', 'neutral'])
results['date'] = results.index

results.to_csv(
    'twitter_results.csv',
    header=True,
    index=False
)

upload_file(f'twitter_results.csv', 'luis-project-twitter-data')
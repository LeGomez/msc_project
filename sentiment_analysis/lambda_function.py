import json
import pandas as pd
import os
import boto3
from helpers import upload_file
from io import BytesIO
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', download_dir='/tmp/')
nltk.data.path.append('/tmp')


bucket = 'project-twitter-data'
file = 'tweet_history.csv'


def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
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
        score = SentimentIntensityAnalyzer().polarity_scores(tweet['text'])
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
    
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

    print(f'Positive={positive}, negative={negative}, neutral={neutral}')
    print(len(tweets))
    
    results = pd.DataFrame.from_dict(daily_results, orient='index', columns=['negative', 'positive', 'neutral'])
    results['date'] = results.index
    
    results.to_csv(
        '/tmp/twitter_results.csv',
        header=True,
        index=False
    )
    
    upload_file(f'/tmp/twitter_results.csv', 'project-twitter-data')
    


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

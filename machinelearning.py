

import tweepy 
import pandas as pd  
import numpy as np        # To consume Twitte
from credentials import *    # This will allow us to use the keys as variables

#credentials is a file in which i saved all the data of the twitter application 

# setup of the api:
def twitter_setup():
   
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api
extractor = twitter_setup()

# We create a tweet list as follows:
tweets = extractor.user_timeline(screen_name="realDonaldTrump", count=10000)
                      
# We print the most recent 20 tweets on the twitter :

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
# We add relevant data:
data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['Retweets'] = np.array([tweet.retweet_count for tweet in tweets])


from textblob import TextBlob
import re

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1
data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])

# We display the updated dataframe with the new column:
display(data.head(10))
q=[]
data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])
pos_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]
print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['Tweets'])))
q.append(len(pos_tweets)*100/len(data['Tweets']))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['Tweets'])))
q.append(len(neu_tweets)*100/len(data['Tweets']))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['Tweets'])))
q.append(len(neg_tweets)*100/len(data['Tweets']))
pie_chart = pd.Series(q, name='Sources')
pie_chart.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6));
"""
to plot the graph
tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['Retweets'].values, index=data['Date'])
tfav.plot(figsize=(6,4), label="Likes", legend=True,color='r');
tret.plot(figsize=(6,4), label="RT", legend=True);
"""

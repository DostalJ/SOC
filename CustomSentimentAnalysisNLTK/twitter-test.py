from time import sleep
from tweepy import StreamListener
import tweepy
from textblob import TextBlob
import keys
from sentiment_classifier import Classify

RC_J = Classify('short_reviews-J')
RC_JRV = Classify('short_reviews-JRV')
TC_J = Classify('twitter-J')
TC_JRV = Classify('twitter-JRV')


class MyStreamListener(StreamListener):

    def on_status(self, status):
        print(status.text)
        print('TextBlob:', TextBlob(status.text.lower()).sentiment)
        print('Movie Reviews-J:', RC_J.sentiment(status.text.lower()))
        print('Movie Reviews-JRV:', RC_JRV.sentiment(status.text.lower()))
        print('Twitter-J:', TC_J.sentiment(status.text.lower()))
        print('Twitter-JRV:', TC_JRV.sentiment(status.text.lower()))
        print('-'*40)
        sleep(5)

    def on_error(self, status_code):
        print('Error: ' + str(status_code) + '\n')
        return False


# authentication
consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
access_token = keys.access_token
access_token_secret = keys.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

myStreamListener = MyStreamListener
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener())



keywords = ['islam', 'isis', 'islamic state', 'muslim', 'muslims', 'terrorist', 'refugee', 'refugees']
myStream.filter(track=keywords, languages=['en'])

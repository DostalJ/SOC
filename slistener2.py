from tweepy import StreamListener
import tweepy
# http://docs.tweepy.org/en/v3.5.0/streaming_how_to.html


class MyStreamListener(StreamListener):

    def on_status(self, status):

        print(status.text)
        print('-'*40)

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

myStream.filter(track=['Zeman'],)

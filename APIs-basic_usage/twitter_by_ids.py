from tweepy import StreamListener
import tweepy
import keys

# authentication
consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
access_token = keys.access_token
access_token_secret = keys.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# info about about user
# user = api.get_user(screen_name='DostlJakub') # equivalent to api.get_user(id=1301048936)

ids = api.friends_ids(screen_name='DostlJakub')


class MyStreamListener(StreamListener):

    def on_status(self, status):

        print(status.text)
        print('-'*40)
        # sleep(5)

    def on_error(self, status_code):
        print('Error: ' + str(status_code) + '\n')
        return False

myStreamListener = MyStreamListener
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener())


# https://dev.twitter.com/streaming/overview/request-parameters#follow
ids = [str(x) for x in ids]

# TODO: Filtrovat pryc retweety????? RT
myStream.filter(follow=ids)

from slistener import SListener
import time, tweepy, sys
import keys

# authentication
consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
access_token = keys.access_token
access_token_secret = keys.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def main():
    track = ['obama', 'trump']

    listen = SListener(api, 'data')
    stream = tweepy.Stream(auth, listen)

    print('Streaming started...')

    # stream.filter(track = track)

    try:
        stream.filter(track = track)
    except Exception as e:
        print('Error:', e)
        stream.disconnect()

if __name__ == '__main__':
    main()

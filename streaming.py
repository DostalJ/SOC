from slistener2 import SListener
import time, tweepy, sys

# authentication
consumer_key = '4chgwRUXPcyxki21R60Araxhc'
consumer_secret = 'B2reu1M77NEPcmn4m9Ui3iDBo1coA3hUNbH5VtIt7MyRUPKyHP'
access_token = '1301048936-bNuPyw2nLxSzu75S2pwkkED0VF88Q139IN4GhEp'
access_token_secret = 'gsuXk8hJV9dSwrtKKhDNlKZkTwa45W0AQoANW8d5aRpgc'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def main():
    track = ['obama', 'trump']

    listen = SListener(api, 'data')
    stream = tweepy.Stream(auth, listen)

    print('Streaming started...')

    stream.filter(track = track)

    # try:
    #     stream.filter(track = track)
    # except Exception as e:
    #     print('Error:', e)
    #     stream.disconnect()

if __name__ == '__main__':
    main()

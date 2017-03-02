import argparse
import tweepy
import keys

def main():

    parser = argparse.ArgumentParser(description='This script collects all folowers of the given person and randoly samples given number of them and writes to the file with given name.')
    parser.add_argument('-p','--person', help="The main person. We are sampling from it's folowers.", required=True)
    parser.add_argument('-n','--number_of_people', help="The number of people to sample from the 'person's folowers.",required=True)
    parser.add_argument('-o','--output_file',help='File we are writing people to.', required=True)
    args = parser.parse_args()

    # authentication
    consumer_key = keys.consumer_key
    consumer_secret = keys.consumer_secret
    access_token = keys.access_token
    access_token_secret = keys.access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)


def collect_folowers(person, n):
    """
    followers = api.followers_ids()





## show values ##
print ("Input file: %s" % args.input )
print ("Output file: %s" % args.output )

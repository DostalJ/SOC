import argparse
import tweepy
import keys
from numpy.random import choice

def main():

    parser = argparse.ArgumentParser(description='This script collects all folowers of the given person and randoly samples given number of them and writes to the file with given name.')
    parser.add_argument('-p','--person', help="The main person. We are sampling from it's folowers.", required=True)
    parser.add_argument('-n','--number_of_people', help="The number of people to sample from the 'person's folowers.",required=True)
    parser.add_argument('-o','--output_file',help='File we are writing people to.', required=True)
    args = parser.parse_args()

    collectFollowers = CollectFollowers()
    followers = collectFollowers.collect_folowers(person=args.person, n=int(args.number_of_people))
    collectFollowers.save_to_txt(list_of_followers=followers, file_path=args.output_file)

class CollectFollowers:
    def __init__(self):
        """Authenticate the Twitter API"""
        # authentication
        consumer_key = keys.consumer_key[1]
        consumer_secret = keys.consumer_secret[1]
        access_token = keys.access_token[1]
        access_token_secret = keys.access_token_secret[1]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def collect_folowers(self, person, n):
        """
        Collects folowers of the person and randomly samples n of them
        Parameters:
            person: ID or name of person
            n: number of people to sample from person's followers
        """
        followers = self.api.followers_ids(person)
        sampled_followers = choice(a=followers, size=n, replace=False)
        return sampled_followers

    def save_to_txt(self, list_of_followers, file_path):
        """
        Writes list o followers to file.
        Parameters:
            list_of_followers: list of followers to write to file
            file_path: path to output file
        """
        try:
            f = open(file=file_path, mode='w')
            for s in list_of_followers:
                f.write(str(s)+',')
            print('Successfully saved to:', file_path)
        except Exception as e:
            print("Can't write followers to file:", e)

if __name__ == '__main__':
    main()

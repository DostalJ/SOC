from tweepy import StreamListener, TweepError
from http.client import IncompleteRead
import tensorflow as tf
import tweepy
import keys
from keras.models import load_model
from tools import Vocabulary
from pickle import load
from keras.preprocessing import sequence
import argparse
import time
from datetime import datetime


def main():

    parser = argparse.ArgumentParser(description='This script streams content that see given users and saves sentiment for every post with one of given keywords that given users might see.')
    parser.add_argument('-p','--people', help="Path to file with ids (delimited by comma). The script will stream what everything these users might see", required=True)
    parser.add_argument('-k','--keywords', help="Keywords the script will look for in the stream.",required=True)
    parser.add_argument('-o','--output_file',help='File we are writing sentiment to.', required=True)
    args = parser.parse_args()

    try:
        f = open(file=args.people, mode='r')
        people = f.read().split(',')[:-1] # [:-1] (vse az na posledni prve) je to tu proto, ze posledni prvek je prazdny string
        f.close()
    except Exception as e:
        print("Can't load file with people to follow:", e)

    keywords = args.keywords.split(',')

    print('Preparing streaming...')
    TA = TwitterAnalyzer(people=people, keywords=keywords)
    TA.stream_analyze_save(out_path=args.output_file)


class Classifier:
    def __init__(self, classifier_path, vocabulary_path):
        try:
            self.classifier = load_model(filepath=classifier_path)
            self.graph = tf.get_default_graph()

            print('-'*30)
            print('Classifier successfuly loaded.')
            print('-'*30)
        except Exception as e:
            raise Exception('Failed in loading classifier:', e)

        self.Vocabulary = Vocabulary(vocabulary_file=vocabulary_path)
    def sentiment(self, sentence):
        num_sent = self.Vocabulary.to_num(sentence)
        num_sent = sequence.pad_sequences([num_sent], maxlen=140) # doplnit, nebo ustrihnout
        global graph
        with self.graph.as_default():
            sentiment = self.classifier.predict(num_sent)
        return sentiment


class MyStreamListener(StreamListener, TweepError):
    def __init__(self, out_path):
        StreamListener.__init__(self)

        self.out_path = out_path
        self.out_path = out_path
        self.TwitterClassifier = Classifier('./classifier/HugeTwitter-classifier.h5', './classifier/HugeTwitter-vocabulary.pickle')

    def on_status(self, status):
        try:
            sent = self.TwitterClassifier.sentiment(status.text)[0,0]
            with open(self.out_path, 'a') as out_file:
                out_file.write(str(datetime.now()) + ',' + str(sent)+'\n')
        except TweepError:
            print('Error: ' + str(status_code) + '\n')
            return False

    def on_error(self, status_code):
        print('Error: ' + str(status_code) + '\n')
        if status_code == 420:
            time.sleep(5*60)
        return False

class TwitterAnalyzer:
    """
    Streams and analyzes data from twitter.
    """
    def __init__(self, people, keywords):
        # authentication
        consumer_key = keys.consumer_key
        consumer_secret = keys.consumer_secret
        access_token = keys.access_token
        access_token_secret = keys.access_token_secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

        if people != None:
            self.ids = self._filter_by_friends(people)

        self.keywords = keywords


    def _filter_by_friends(self, people):
        """
        Get list of ids of people that are followed by specified list of nodes
        """
        ids = set()
        for node in people:
            try: # some users are protected
                friends_of_node = self.api.friends_ids(node)
                ids = ids.union(friends_of_node)
            except TweepError:
                pass
        ids = [str(_id) for _id in ids]
        return ids

    def stream_analyze_save(self, out_path):
        """
        Streams the tweets and saves its sentiment to file
        """
        myStreamListener = MyStreamListener(out_path)
        myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)
        print('Streaming...')
        stop = False
        while True:
            try:
                myStream.filter(track=self.keywords, follow=self.ids, languages=['en'], filter_level=['medium'])
                # myStream.filter(track=self.keywords, languages=['en'], filter_level=['medium'])
            except KeyboardInterrupt:
                stop = True
            except Exception as e:
                print('Exception:', e)
                print('Retrying...')
                pass
            if stop:
                print('Disconnecting.')
                stream.disconnect()
                break


if __name__ == '__main__':
    main()

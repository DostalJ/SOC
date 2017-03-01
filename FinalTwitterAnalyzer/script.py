from tweepy import StreamListener, TweepError
import tensorflow as tf
import tweepy
import keys
from keras.models import load_model
from tools import Vocabulary
from pickle import load
from keras.preprocessing import sequence
import time


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
        try:
            self.out_file = open(out_path, 'w')
        except Exception as e:
            print("Can't open file", out_path, ':', e)
        self.TwitterClassifier = Classifier('HugeTwitter-classifier.h5', 'HugeTwitter-vocabulary.pickle')

    def on_status(self, status):
        try:
            sent = self.TwitterClassifier.sentiment(status.text)[0,0]
            self.out_file.write(str(status.text)+','+str(sent)+'\n')
            print(sent)
        except TweepError:
            print('Error: ' + str(status_code) + '\n')
            return False

    def on_error(self, status_code):
        print('Error: ' + str(status_code) + '\n')
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
            friends_of_node = self.api.friends_ids(node)
            ids = ids.union(friends_of_node)
        ids = [str(_id) for _id in ids]
        return ids

    def stream_analyze_save(self, out_path):
        """
        Streams the tweets and saves its sentiment to file
        """
        myStreamListener = MyStreamListener(out_path)
        myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)
        start_time = time.time()
        myStream.filter(track=self.keywords, follow=self.ids, async=True, languages=['en'])

TA = TwitterAnalyzer(people=['Conflicts'], keywords=['Trump'])
TA.stream_analyze_save(out_path='01.txt')

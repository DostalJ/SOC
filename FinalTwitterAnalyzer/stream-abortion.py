from tweepy import StreamListener, TweepError
import tweepy
import keys
from time import sleep
from numpy.random import choice
from keras.models import load_model
import tensorflow as tf
from tools import Vocabulary
from keras.preprocessing import sequence
from datetime import datetime




# authentication
consumer_key = keys.consumer_key[4]
consumer_secret = keys.consumer_secret[4]
access_token = keys.access_token[4]
access_token_secret = keys.access_token_secret[4]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

pages = ['PPact', 'Guttmacher', 'Students4LifeHQ', 'AmenditUSA', 'EvrydayFeminism']

def load_people(page):
    try:
        f = open(file='./Data/people/{}.txt'.format(page), mode='r')
        people = f.read().split(',')[:-1] # [:-1] (vse az na posledni prvek) je to tu proto, ze posledni prvek je prazdny string
        f.close()
    except Exception as e:
        print("Can't load file with people to follow:", e)
    return people

def save_followed(people, file_path):
    """
    Takes file with people and returns union of people they are following.
    Parameters:
        people: file with people
    """
    ids = set()
    for node in people:
        try: # some users are protected
            friends_of_node = api.friends_ids(node)
            ids = ids.union(friends_of_node)
            sleep(20)
        except TweepError:
            print('Error while loading friends.')
            pass
    ids = [str(_id) for _id in ids]
    print(len(ids))
    f = open(file=file_path, mode='w')
    for node_id in ids:
        f.write(str(node_id)+',')
    f.close()
    print('Successfully saved to:', file_path)

# for page in pages[4:]:
#     people = load_people(page)
#     save_followed(people[:10], './Data/followed/{}-followed.txt'.format(page))


class Classifier:
    def __init__(self, classifier_path, vocabulary_path):
        """
        Class that uses saved keras classifier to measure sentiment of tweets.
        Parameters:
            classifier_path: path to saved classifier in .h5 keras format
            vocabulary_path: path to vocabulary saved in .pickle format
        """
        try:
            self.classifier = load_model(filepath=classifier_path)
            self.graph = tf.get_default_graph()
            print('Classifier successfuly loaded.')
        except Exception as e:
            print('-'*30)
            raise Exception('Failed in loading classifier:', e)
            print('-'*30)

        self.Vocabulary = Vocabulary(vocabulary_file=vocabulary_path)
    def sentiment(self, sentence):
        num_sent = self.Vocabulary.to_num(sentence)
        num_sent = sequence.pad_sequences([num_sent], maxlen=140) # doplnit, nebo ustrihnout
        global graph
        with self.graph.as_default():
            sentiment = self.classifier.predict(num_sent)
        return sentiment

followed = dict()
for page in pages:
    f = open('./Data/followed/{}-followed.txt'.format(page), 'r')
    followed_people = f.read().split(',')[:-1]
    f.close()
    followed[page] = followed_people


class MyStreamListener(StreamListener, TweepError):
    def __init__(self):
        StreamListener.__init__(self)
        self.TwitterClassifier = Classifier('./classifier/HugeTwitter-classifier.h5', './classifier/HugeTwitter-vocabulary.pickle')


    def on_status(self, status):
        """
        Wraps default on_status method to measure sentiment and write to file.
        Prints errors.
        """
        try:
            sent = self.TwitterClassifier.sentiment(status.text)[0,0]
            for page in pages:
                if str(status.user.id) in followed[page]:
                    with open('./Data/sentiment/abortion-{}.csv'.format(page), 'a') as out_file:
                        out_file.write(str(datetime.now()) + ',' + str(sent) + '\n')
                    with open('./Data/sentiment/abortion-{}.txt'.format(page), 'a') as out_file:
                        out_file.write(status.text + '\n')
        except TweepError:
            print('Error: ' + str(status_code) + '\n')
            return False

    def on_error(self, status_code):
        print('Error: ' + str(status_code) + '\n')
        return False



def _log(e, log):
    """
    Logs errors.
    Parameters:
        e: key of the error
        log: type of logging
    """
    if log == '0':
        pass
    elif log == '1':
        print('Exception:', e)
        print('Retrying...')
    else:
        try:
            with open(log, 'a') as log_file:
                log_file.write(str(datetime.now()) + ',' + str(e)+'\n')
        except Exception as e:
            print('Exception while writing log:', e)



myStreamListener = MyStreamListener
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener())


stop = False
while True:
    try:
        myStream.filter(track=['abortion'])
    except KeyboardInterrupt:
        stop = True
    except Exception as e:
        _log(e=e, log='./Data/sentiment/abortion.log')
        pass
    if stop:
        print('Disconnecting.')
        myStream.disconnect()
        break

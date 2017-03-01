import nltk
import random
import pickle
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI

# https://pythonprogramming.net/sentiment-analysis-module-nltk-tutorial/

class VoteClassifier(ClassifierI):
    """
    helper class for counting votes of different classifiers
    """
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

class Classify:
    """
    Class for sentiment classification of the text.

    Example:
    ..............................................................................
        from sentimen_classify import Classify

        SCT = Classify('twitter-J') # sentiment classificator trained on adjectives from twitter data
        SCR = Classify('short_reviews-JRV') # sentiment classificator trained on adjectives, adverbs and verbs from short reviews data

        # return: 'pos'/'neg', confidence
        SCT.sentiment('I hate all people on this planet')
        SCR.sentiment('I hate all people on this planet')
    ..............................................................................
    """
    def __init__(self, dataset='twitter-J'):
        """
        Initial parameters:
            dataset: datate used to train classifier
        """
        if dataset == 'twitter-J':
            path = 'pickled_algos/twitter/J/'
        elif dataset == 'twitter-JRV':
            path = 'pickled_algos/twitter/JRV/'
        elif dataset == 'short_reviews-J':
            path = 'pickled_algos/short_reviews/J/'
        elif dataset == 'short_reviews-JRV':
            path = 'pickled_algos/short_reviews/JRV/'
        else:
            print('#'*60)
            print('#'*60)
            print("Classifier trained on this data doesn't exist!!!")
            print('#'*60)
            print('#'*60)

        word_features5k_f = open(path + "word_features5k.pickle", "rb")
        self.word_features = pickle.load(word_features5k_f)
        word_features5k_f.close()

        # load trained classifiers
        open_file = open(path + "originalnaivebayes5k.pickle", "rb")
        classifier = pickle.load(open_file)
        open_file.close()

        open_file = open(path + "MNB_classifier5k.pickle", "rb")
        MNB_classifier = pickle.load(open_file)
        open_file.close()

        open_file = open(path + "BernoulliNB_classifier5k.pickle", "rb")
        BernoulliNB_classifier = pickle.load(open_file)
        open_file.close()

        open_file = open(path + "LogisticRegression_classifier5k.pickle", "rb")
        LogisticRegression_classifier = pickle.load(open_file)
        open_file.close()

        open_file = open(path + "LinearSVC_classifier5k.pickle", "rb")
        LinearSVC_classifier = pickle.load(open_file)
        open_file.close()

        open_file = open(path + "SGDC_classifier5k.pickle", "rb")
        SGDC_classifier = pickle.load(open_file)
        open_file.close()

        self.voted_classifier = VoteClassifier(classifier,
                                               LinearSVC_classifier,
                                               MNB_classifier,
                                               BernoulliNB_classifier,
                                               LogisticRegression_classifier)

    # function finding features
    def find_features(self, document):
        """
        Functions that makes feature vectors
        (they inform if specific word with our
        interest is in studied document)
        """
        words = word_tokenize(document)
        features = {}
        for w in self.word_features:
            features[w] = (w in words)
        return features

    # predict method
    def sentiment(self, text):
        """
        This function decides if the text is positive or negative
        ________________
        Input:
            text: string
        Output:
            classification (='pos'/'neg'), confidence
        """
        feats = self.find_features(text)
        return self.voted_classifier.classify(feats), self.voted_classifier.confidence(feats)

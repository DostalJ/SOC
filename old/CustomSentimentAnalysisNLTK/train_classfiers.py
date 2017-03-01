import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

# https://pythonprogramming.net/new-data-set-training-nltk-tutorial/

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes)) # kolik classirieru zvolilo tuto label
        conf = choice_votes / len(votes)

# files we use to train our classifier
short_pos = open('data/short_reviews/positive.txt', 'r').read()
short_neg = open('data/short_reviews/negative.txt', 'r').read()

# move this up here
all_words = []
documents = []

# j id ajdect, r is adverb, v is verb
allowed_word_types = ['J', 'R', 'V']
# allowed_word_types = ['J']

for review in short_pos.split('\n'): # rozdelime dokument na radky (tj. jednotlive recenze)
    documents.append((review, 'pos'))
    words = word_tokenize(review) # rozdelime na jednotliva slova
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types: # pokud je slovo povoleneho druhu
            all_words.append(w[0].lower()) # pridame jeho verzi v malych pismenech
for review in short_neg.split('\n'): # rozdelime dokument na radky (tj. jednotlive recenze)
    documents.append((review, 'neg'))
    words = word_tokenize(review) # rozdelime na jednotliva slova
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types: # pokud je slovo povoleneho druhu
            all_words.append(w[0].lower()) # pridame jeho verzi v malych pismenech

# ulozime oznacena reviews
save_documents = open('pickled_algos/short_reviews/JRV/documents.pickle', 'wb')
pickle.dump(documents, save_documents)
save_documents.close()

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:5000] # prvnich 5000 nejfrekventovanejsich slov

# ulozime nejfrekventovanejsi slova
save_word_features = open('pickled_algos/short_reviews/JRV/word_features5k.pickle', 'wb')
pickle.dump(word_features, save_word_features)
save_word_features.close()

def find_features(document):
    words = word_tokenize(document) # rozdelime na jednotliva slova
    features = {}
    for w in word_features:
        # pokud slovo z naseho document v seznamu word_features prida se 1, jinak nula 0
        features[w] = (w in words)
    return features

# (featureset, pos/neg) pro kazde review
featuresets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featuresets) # pomichame
print(len(featuresets))

n = len(featuresets)
training_set = featuresets[:int(n*0.8)]
testing_set = featuresets[int(n*0.8):]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)
save_classifier = open("pickled_algos/short_reviews/JRV/originalnaivebayes5k.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)
save_classifier = open("pickled_algos/short_reviews/JRV/MNB_classifier5k.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)
save_classifier = open("pickled_algos/short_reviews/JRV/BernoulliNB_classifier5k.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
save_classifier = open("pickled_algos/short_reviews/JRV/LogisticRegression_classifier5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
save_classifier = open("pickled_algos/short_reviews/JRV/LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)
save_classifier = open("pickled_algos/short_reviews/JRV/SGDC_classifier5k.pickle","wb")
pickle.dump(SGDC_classifier, save_classifier)
save_classifier.close()

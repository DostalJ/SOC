from keras.models import load_model
from tools import Vocabulary
from pickle import load
from keras.preprocessing import sequence

max_words = 140 # maximum length of review


class Classifier:
    def __init__(self, classifier_path, vocabulary_path):
        try:
            self.classifier = load_model(filepath=classifier_path)

            print('-'*30)
            print('Classifier successfuly loaded.')
            print('-'*30)
        except Exception as e:
            raise Exception('Failed in loading classifier:', e)

        self.Vocabulary = Vocabulary(vocabulary_file=vocabulary_path)


    def sentiment(self, sentence):
        num_sent = self.Vocabulary.to_num(sentence)
        num_sent = sequence.pad_sequences([num_sent], maxlen=140) # doplnit, nebo ustrihnout
        sentiment = self.classifier.predict(num_sent)
        return sentiment

TwitterClassifier = Classifier('HugeTwitter-classifier.h5', 'HugeTwitter-vocabulary.pickle')
TwitterClassifier.sentiment("RT @narendramodi: Sonu Golkar has been an ardent cricket follower. He has played several matches &amp; also been awarded for his game. https://…")[0,0]

# def play_with_sentiment_in_console():
#     TwitterClassifier = Classifier('HugeTwitter-classifier.h5', 'HugeTwitter-vocabulary.pickle')
#
#     end = False
#     while not end:
#         print("Enter your sentence ('end' to quit()):")
#         text = input()
#         if text == 'end':
#             end = True
#         else:
#             sentiment = TwitterClassifier.sentiment(text)[0][0]
#             print('Sentiment: {:.4f}'.format(sentiment))
#             print('-'*20)
#
# if __name__ == '__main__':
#     play_with_sentiment_in_console()

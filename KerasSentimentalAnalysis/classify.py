from keras.models import load_model
from tools import Vocabulary
from pickle import load
from keras.preprocessing import sequence

max_words = 140 # maximum length of review


try:
    reviews_classifier = load_model(filepath='reviews-classifier.h5')
    print('-'*30)
    print('Classifier successfuly loaded.')
    print('-'*30)
except Exception as e:
    raise Exception('Failed in loading classifier:', e)


reviews_classifier

ReviewsVocabulary = Vocabulary(vocabulary_file='reviews-vocabulary.pickle')
reviews_num = ReviewsVocabulary.to_num("Its awfull and boring. I have never seen anything so bad as this")
reviews_num = sequence.pad_sequences([reviews_num], maxlen=max_words) # doplnit, nebo ustrihnout
reviews_sentiment = reviews_classifier.predict(reviews_num)

import numpy as np
import matplotlib.pyplot as plt
import pickle
from warnings import warn

from tensorflow.contrib import learn
from nltk.tokenize import word_tokenize

def summarize_data(X, y):
    """make summary of the date"""
    # summarize size
    print('Training data:')
    print(X.shape)
    print(y.shape)
    # Summarize number of classes
    print("Classes:")
    print(np.unique(y))
    # Summarize number of words
    print("Number of words:")
    print(len(np.unique(np.hstack(X))))
    # Summarize review length
    print('Review length: ')
    result = [len(X[i][:]) for i in range(X.shape[0])]
    print("Mean {:.2f} words ({:f})".format(np.mean(result), np.std(result)))
    plt.hist(result, 40)
    plt.show()



class Vocabulary:
    def __init__(self, pos_file_path=None, neg_file_path=None, vocabulary_file=None, vocabulary_size=None):
        if vocabulary_file == None:
            self.pos_file_path = pos_file_path
            self.neg_file_path = neg_file_path
            self.vocabulary_size = vocabulary_size
        elif vocabulary_file != None:
            try:
                open_file = open(vocabulary_file, "rb")
                self.vocabulary = pickle.load(open_file)
                open_file.close()
                print('-'*30)
                print('Vocabulary {} successfuly loaded.'.format(vocabulary_file))
                print('-'*30)
            except Exception as e:
                print('-'*30)
                print('Error while loading {}:.'.format(vocabulary_file), e)
                print('-'*30)
            self.vocabulary_size = len(self.vocabulary)

    def _load_and_convert_to_list_of_strings(self, pos_file_path=None, neg_file_path=None, return_=True, write_as_attribute=False):
        """
        load and convert to list of strings
        Parameters:
            pos_file_path: optional, is initialized in __init__
            neg_file_path: optional, is initialized in __init__
            return_: (False), if want to return: True
        """
        if (pos_file_path == None and neg_file_path == None):
            pos_file_path = self.pos_file_path
            neg_file_path = self.neg_file_path
        if (pos_file_path == None and neg_file_path == None):
            # nebyli inicializovany ani v ___init___
            raise Exception("Nebyly inicializovany parametry 'pos_file_path', 'neg_file_path'.")

        pos_data = open(pos_file_path, 'r', encoding='latin-1').readlines()
        neg_data = open(neg_file_path, 'r', encoding='latin-1').readlines()

        # pos_data = pos_data.split('\n')
        pos_data = [review.strip() for review in pos_data]
        # neg_data = neg_data.split('\n')
        neg_data = [review.strip() for review in neg_data]

        if write_as_attribute:
            self.pos_data, self.neg_data = pos_data, neg_data
        if return_:
            return pos_data, neg_data

    def prepare_data_and_labels(self, pos_data=None, neg_data=None, vocabulary_size=None):
        """
        Loads the data from file and converts them to lists of vocabulary indexes
        pos_data: list of strings
        neg_data: list of strings
        vocabulary_size: number of words in vocabulary
        """
        if pos_data == None and neg_data == None:
            pos_data, neg_data = self._load_and_convert_to_list_of_strings(return_=True)
        if vocabulary_size == None:
            vocabulary_size = self.vocabulary_size
        if vocabulary_size == None:
            raise Exception("Nebyl inicializovan parametr 'vocabulary_size'")

        pos_data, neg_data = self._load_and_convert_to_list_of_strings()
        vocabulary = self.make_vocabulary(text_data=pos_data+neg_data, return_=True)

        X = []
        for row in pos_data:
            X.append(self.to_num(sentence=row,
                                           vocabulary=vocabulary))
        for row in neg_data:
            X.append(self.to_num(sentence=row,
                                           vocabulary=vocabulary))
        y = np.array([1 for _ in range(len(pos_data))] +
                     [0 for _ in range(len(neg_data))])
        return X, y

    def make_vocabulary(self, text_data, vocabulary_size=None, return_=False, save=False, path_to_save='vocabulary.pickle'):
        """
        Makes vocabulary from text_data
        Parameters:
            text_data: list of strings
            return:
            save:
            path_to_save:
        """
        if vocabulary_size == None:
            vocabulary_size = self.vocabulary_size
        if vocabulary_size == None:
            raise Exception("Parametr 'vocabulary_size' wasn't initialized.")

        all_words = {}
        for review in text_data: # rozdelime dokument na radky (tj. jednotlive recenze)
            words = word_tokenize(review) # rozdelime na jednotliva slova
            for w in words:
                w = w.lower()
                if w in all_words.keys():
                    all_words[w] += 1
                else:
                    all_words[w] = 1
        # sort by values
        sorted_words = sorted(all_words,
                              reverse=True,
                              key=all_words.__getitem__)

        if len(sorted_words) < vocabulary_size:
            warn("Pocet slov je mensi nez pozadovana delka slovniku\n\tZmensuji 'vocabulary_size' na 'len(sorted_words)'")
            self.vocabulary_size = len(sorted_words)
            vocabulary_size = len(sorted_words)

        # make vocabulary of words (indexing from 1)
        vocabulary = {sorted_words[i]:i+1 for i in range(vocabulary_size)}

        if save:
            try:
                save = open(path_to_save, "wb")
                pickle.dump(vocabulary, save)
                save.close()
                print('-'*30)
                print('Vocabulary {} successfuly saved.'.format(path_to_save))
                print('-'*30)
            except Exception as e:
                print('-'*30)
                print('Vocabulary {} wasn\'t saved:'.format(path_to_save), e)
                print('-'*30)
        if return_:
            return vocabulary
        else:
            self.vocabulary = vocabulary

    def save_vocabulary(self, path_to_save):
        """Wrapper above Class methods that saves used vocabulary"""
        pos_data, neg_data = self._load_and_convert_to_list_of_strings()
        self.make_vocabulary(text_data=pos_data+neg_data,
                             save=True,
                             path_to_save=path_to_save)


    def to_num(self, sentence, vocabulary=None):
        """
        Translate string
        Parameters:
            sentence: string of words
            vocabulary: dictionary
        """
        if vocabulary == None:
            vocabulary = self.vocabulary
        if vocabulary == None:
            raise Exception("Parametr 'vocabulary' wasn't initialized.")

        tokenized = [word for word in word_tokenize(sentence)] # list of strings (words)

        translated = [0 for _ in range(len(tokenized))]
        for j in range(len(tokenized)):
            if tokenized[j] in vocabulary.keys():
                translated[j] = vocabulary[tokenized[j]]
        return translated

    def to_words(self, num_sentence, vocabulary=None):
        """
        Translate to words (zeros are omited)
        Parameters:
            num_sentence: list of ints
            vocabulary:
        """
        if vocabulary == None:
            vocabulary = self.vocabulary
        if vocabulary == None:
            raise Exception("Parametr 'vocabulary' wasn't initialized.")

        sentence = []
        for num in num_sentence:
            if num != 0:
                word = list(vocabulary.keys())[list(vocabulary.values()).index(num)] # find key by value
                sentence.append(word)

        str_sentence = ""
        for s in sentence:
            str_sentence += s + " "
        return str_sentence


# Vocab = Vocabulary('./data/rt-polaritydata/rt-polarity.pos',
#                    './data/rt-polaritydata/rt-polarity.neg',
#                    vocabulary_size=5000)
# a,b = Vocab._load_and_convert_to_list_of_strings()
# Vocab.make_vocabulary(a+b)
# sent = Vocab.to_num("house is absolutely amazing.")
#
# Vocab.to_words(sent)
#
# X, y = Vocab.prepare_data_and_labels()

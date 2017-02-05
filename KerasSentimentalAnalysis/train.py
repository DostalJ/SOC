import numpy as np
import matplotlib.pyplot as plt

from tools import Vocabulary

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence




###################
# hyperparameters #
###################
top_words = 5000 # number of words in vocabulary
max_words = 140 # maximum length of review

embedding_dim = 32

num_conv_filters = 32
conv_filter_len = 3
pool_length = 2

hidden = 250

num_epochs = 2
batch_size = 128
test_size = 0.1
###################

save_file = 'reviews-classifier.h5'
Vocab = Vocabulary('./data/rt-polaritydata/rt-polarity.pos',
                   './data/rt-polaritydata/rt-polarity.neg',
                   vocabulary_size=top_words)
Vocab.save_vocabulary(path_to_save='reviews-vocabulary.pickle')

X, y = Vocab.prepare_data_and_labels()
# pad dataset to a maximum review length in words
X = sequence.pad_sequences(X, maxlen=max_words) # doplnit, nebo ustrihnout

# randomly shuffle data
np.random.seed(10)
shuffle_indices = np.random.permutation(np.arange(len(y)))
X_sh = X[shuffle_indices]
y_sh = y[shuffle_indices]

# divide to training and testing sets
X_train = X_sh[0:len(X_sh) - int(len(X_sh)*test_size)]
y_train = y_sh[0:len(X_sh) - int(len(X_sh)*test_size)]
X_test = X_sh[len(X_sh) - int(len(X_sh)*test_size):-1]
y_test = y_sh[len(X_sh) - int(len(X_sh)*test_size):-1]

model = Sequential()
model.add(Embedding(input_dim=top_words+1,
                    output_dim=embedding_dim,
                    input_length=max_words))
model.add(Convolution1D(nb_filter=num_conv_filters,
                        filter_length=conv_filter_len,
                        border_mode='same',
                        activation='relu'))
model.add(MaxPooling1D(pool_length=pool_length))
model.add(Flatten())
model.add(Dense(output_dim=hidden,
               activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print(model.summary())

# fit the model
model.fit(X_train, y_train,
          validation_split=0.1,
          nb_epoch=num_epochs,
          batch_size=batch_size,)

# evaluate the model
scores = model.evaluate(X_test, y_test)
print('\nAccuracy: {:.2f} %'.format(scores[1]*100))

# save the trained classifier
try:
    model.save(save_file)
    print('-'*30)
    print('Classifier {} successfuly saved.'.format(save_file))
    print('-'*30)
except Exception as e:
    print('-'*30)
    print('Classifier wasn\'t saved:', e)
    print('-'*30)

from __future__ import print_function
import os
import data_helper
import numpy as np
from constants import *
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import Convolution1D, GlobalMaxPooling1D
#from keras.datasets import imdb
from keras.callbacks import TensorBoard


# set parameters:
max_features = 5000
maxlen = 400
batch_size = 32
embedding_dims = 50
nb_filter = 250
filter_length = 3
hidden_dims = 250
nb_epoch = 2

print('Loading data...')
#(X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)
x, y, d = data_helper.load_data_and_labels_and_dictionaries()

train_x, train_y = x[:-(NUM_TESTS + NUM_EVALS)], y[:-(NUM_TESTS + NUM_EVALS)]
test_x,  test_y  = x[-(NUM_TESTS + NUM_EVALS):-NUM_EVALS], y[-(NUM_TESTS + NUM_EVALS):-NUM_EVALS]
eval_x, eval_y = x[-NUM_EVALS:], y[-NUM_EVALS:]

X_train = train_x
y_train = train_y
X_test = test_x
y_test = test_y

print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')

print('Pad sequences (samples x time)')
X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)


print('Build model...')
model = Sequential()

# todo
model.add(.. )
:

# last layer: output shape for array[NUM_CLASSES]
model.add(Dense(NUM_CLASSES))

# todo
model.compile(.. )

tb_cb = TensorBoard(log_dir=SUMMARY_LOG_DIR, histogram_freq=1)
cbks = [tb_cb]

model.fit(X_train, y_train,
          batch_size=batch_size,
          nb_epoch=nb_epoch,
          verbose=1,
          callbacks=cbks,
          validation_data=(X_test, y_test))

print('Save...')
if not os.path.exists(CHECKPOINTS_DIR):
    os.makedirs(CHECKPOINTS_DIR)
model.save(CHECKPOINTS_FILE)

print('done')
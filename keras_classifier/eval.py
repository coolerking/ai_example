from __future__ import print_function
import os
import data_helper
import numpy as np
from data_helper import log
from constants import *

np.random.seed(1337)  # for reproducibility



from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from keras.models import load_model

max_features = 20000

maxlen = 400  # cut texts after this number of words (among top max_features most common words)
batch_size = 32


log('Loading data...')
x, y, d = data_helper.load_data_and_labels_and_dictionaries()
eval_x, eval_y = x[-NUM_EVALS:], y[-NUM_EVALS:]
y_eval = eval_y

log('Pad sequences (samples x time)')
X_eval = sequence.pad_sequences(eval_x, maxlen=maxlen)

log('load model...')
model = load_model(CHECKPOINTS_FILE)


log('Eval...')
output_y = model.predict_proba(X_eval, batch_size=batch_size, verbose=1)

log('Start saving result.')
np.savetxt(OUTPUT_FILE, output_y, delimiter=',')

log('done.')
NUM_TESTS         = 140
NUM_EVALS         = 55
#NUM_CLASSES       = 134
#NUM_CLASSES       = 47
NUM_CLASSES       = 11
NUM_EPOCHS        = 10
NUM_MINI_BATCH    = 64
EMBEDDING_SIZE    = 128
NUM_FILTERS       = 128
FILTER_SIZES      = [ 3, 4, 5 ]
L2_LAMBDA         = 0.0001
EVALUATE_EVERY    = 100
CHECKPOINTS_EVERY = 1000

SUMMARY_LOG_DIR = 'summary_log'
CHECKPOINTS_DIR = 'checkpoint'
CHECKPOINTS_FILE = CHECKPOINTS_DIR + '/cnn_' + str(NUM_CLASSES) + '.h5'

OUTPUT_FILE     = CHECKPOINTS_DIR + '/cnn_output_' + str(NUM_CLASSES) + '.csv'

RAW_FILE        = 'data/raw_' + str(NUM_CLASSES) + '.txt'
DATA_FILE       = 'data/data.npy'
LABEL_FILE      = 'data/labels.npy'
DICTIONARY_FILE = 'data/dictionaries.npy'

EVAL_DATA_FILE  = 'data/data.npy'
EVAL_LABEL_FILE = 'data/labels.npy'
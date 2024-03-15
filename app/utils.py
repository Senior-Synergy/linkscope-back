import pickle
import gzip


def load_model(filename):
    with gzip.open(filename, 'rb') as f:
        model = pickle.load(f)
    return model

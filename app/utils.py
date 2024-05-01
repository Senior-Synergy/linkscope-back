import pickle
import gzip
import joblib


def load_model(filename):
    with gzip.open(filename, 'rb') as f:
        model = pickle.load(f)
    return model


def load_joblib_model(filename):
    model = joblib.load(filename)
    return model

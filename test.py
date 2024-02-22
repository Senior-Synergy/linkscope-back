#from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from functions import *
import warnings
import pickle
import gzip
from urllib.parse import urlparse
import bz2file as bz2
warnings.filterwarnings('ignore')
from app.feature_extraction import FeatureExtraction

#with open("data/model.pkl","rb") as f:
#    model = pickle.load(f)

# def decompress_pickle(file):
#    data = bz2.BZ2File(file, "rb")
#    data = pickle.load(data)
 #   return data
#model = decompress_pickle("data/model_allfeatures.bz2")

def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object
model = load_zipped_pickle("data/model_new.gzip")

#file.close()
url = 'fakespot.com'

#url = request.form["url"]
def geturlresults(url):
    # Extract features
    obj = FeatureExtraction(url)
    x = np.array(obj.getFeaturesList()).reshape(1,29)
    extracted_df = pd.DataFrame(x, columns = feature_names)

    #1 Prediction 
    y_pred = model.predict(extracted_df)[0]                 # 0 means safe, 1 means phish
    y_pro_phishing = model.predict_proba(extracted_df)[0,1] # Probability to be phishing url
    print("There is", "%.2f" % (y_pro_phishing *100) , "% chance, the url is phishing" ) # Probability to be phishing url

# Same Results with all urls    
def getmodelresults(model) :
    #2 Feature importances
    feature_importance_map = {}
    rf_model = model.named_steps['clf']
    importances = rf_model.feature_importances_ 
    for feature, importance in zip(feature_names, importances):
        feature_importance_map[feature] = importance*100
    print(feature_importance_map)
    # Check 
# -----------------------test-----------------------------    
geturlresults(url)
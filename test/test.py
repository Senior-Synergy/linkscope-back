#from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import warnings
import pickle
import gzip
from urllib.parse import urlparse
warnings.filterwarnings('ignore')
from app.urlfeatures import FeatureExtraction


feature_names = [ 'domainlength', 'www', 'subdomain', 
                 'https', 'http', 'short_url', 'ip', 
                 '@','-', '=','.', '_','/','digit', 
                 'log', 'pay', 'web', 'cmd', 'account',
                 'pcemptylinks', 'pcextlinks', 'pcrequrl',
                 'zerolink','extfavicon', 'submit2email',
                 'sfh', 'redirection', 'domainage', 'domainend']
num_features = [ 'domainlength',  '@', '-', '=', '.', '_', '/', 'digit',  'pcemptylinks', 'pcextlinks', 'pcrequrl']
cat_features = ['www', 'subdomain', 'https', 'http','short_url','ip','log', 'pay', 'web', 'cmd', 'account','zerolink', 'extfavicon',
       'submit2email','sfh','redirection', 'domainage', 'domainend']

def replace_minus_one(X):
    return X.replace(-1, np.nan)

def cast_to_float(X):
    return X.astype(float)

def cast_to_int(X):
    return X.astype(int)

def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object
model = load_zipped_pickle("data/model_new.gzip")

#file.close()
url = '9418265.fls.doubleclick.net'

#url = request.form["url"]
def geturlresults(url):
    # Extract features
    obj = FeatureExtraction(url)
    x = np.array(obj.getFeaturesList()).reshape(1,29)
    print(x)
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
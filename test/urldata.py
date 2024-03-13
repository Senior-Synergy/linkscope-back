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
# ---------------------------------------------------------
def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object
model = load_zipped_pickle("data/model_new.gzip")
#file.close()
url = '9418265.fls.doubleclick.net'
#url = request.form["url"]
class URLresult:
    
    def __init__(self, url):
        self.url = url #1
        obj = FeatureExtraction(url)
        features_arr = np.array(obj.getFeaturesList()).reshape(1,29)
        #print(features_arr)
        self.features_df = pd.DataFrame(features_arr, columns = feature_names) #2
    
    def get_final_url(self):
        return FeatureExtraction.getfinalurl(self.url)[0]
    
    def get_phish_prob(self):
        return model.predict_proba(self.features_df)[0,1] # Probability to be phishing url
  
    def get_isPhish(self):
        return model.predict(self.features_df)[0] # 0 means safe, 1 means phish
    
#obj = URLresult(url)
#print(obj.features_df)    
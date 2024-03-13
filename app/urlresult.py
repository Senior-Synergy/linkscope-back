import numpy as np
import pandas as pd
import warnings
import pickle
import gzip
from urllib.parse import urlparse
warnings.filterwarnings('ignore')

from app.urlfeatures import FeatureExtraction

feature_names = [
            'domainlength', 'www', 'subdomain', 'https', 'http', 'short_url', 'ip',
            '@', '-', '=', '.', '_', '/', 'digit', 'log', 'pay', 'web', 'cmd', 'account',
            'pcemptylinks', 'pcextlinks', 'pcrequrl', 'zerolink', 'extfavicon', 'submit2email',
            'sfh', 'redirection', 'domainage', 'domainend'
        ]
def load_model(filename):
    with gzip.open(filename, 'rb') as f:
        model = pickle.load(f)
    return model

#url = request.form["url"]
class URLresult:
    def __init__(self, url, model):
        self.model = model
        self.url = url #1
        obj = FeatureExtraction(url)
        features_arr = np.array(obj.getFeaturesList()).reshape(1,29)
        #print(features_arr)
        self.features_df = pd.DataFrame(features_arr, columns = feature_names) #2
    
    def get_final_url(self):
        return FeatureExtraction(self.url).url
    
    def get_phish_prob(self):
        return self.model.predict_proba(self.features_df)[0,1] # Probability to be phishing url
  
    def get_isPhish(self):
        return self.model.predict(self.features_df)[0] # 0 means safe, 1 means phish

 
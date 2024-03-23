import numpy as np
import pandas as pd
import warnings
import pickle
import gzip
from urllib.parse import urlparse
warnings.filterwarnings('ignore')

from urlfeatures import URLFeatures

num_features = [
            'domainlength', '@', '-', '=', '.', '_', '/', 'digit',
            'pcemptylinks', 'pcextlinks', 'pcrequrl'
        ]
cat_features = [
            'www', 'subdomain', 'https', 'http', 'short_url', 'ip', 'log', 'pay',
            'web', 'cmd', 'account', 'zerolink', 'extfavicon', 'submit2email',
            'sfh', 'redirection', 'domainage', 'domainend'
        ]
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

class URLresult:
    def __init__(self, url, model):
        self.model = model
        self.url = url  # 1
        obj = URLFeatures(url)
        self.features_arr = np.array(obj.getFeaturesList()).reshape(1, 29)
        self.features_df = pd.DataFrame(
            self.features_arr, columns=feature_names)  # 2
        ## Extra features
        self.extra_features = obj.extra_features
        self.whois_data = obj.w
   
    def get_final_url(self):
        return URLFeatures(self.url).url

    def get_phish_prob(self):
        # Probability to be phishing url
        return self.model.predict_proba(self.features_df)[0, 1]

    def get_isPhish(self):
        # 0 means safe, 1 means phish
        return self.model.predict(self.features_df)[0]
    
    ## extrafeatures
    def get_extra_features(self):
        return  self.extra_features
    
    def get_whois_features(self):
        return  self.whois_data






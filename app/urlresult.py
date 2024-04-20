import numpy as np
import pandas as pd
from .urlfeatures import URLFeatures
from .constants import feature_names
import json
from datetime import date, datetime

def serialize_datetime(obj):
    if isinstance(obj, datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 

class URLresult:
    def __init__(self, url, model):
        
        self.model = model
        self.url = url  # 1

        self.url_obj = URLFeatures(url)        
        self.extra_info = self.url_obj.get_extra_info() # url extra information dict        
        self.model_features =self.url_obj.get_model_features() # model features dict

        self.model_features_arr = np.array(list(self.model_features.values())[:19]).reshape(1, 19)
        self.features_df = pd.DataFrame(self.model_features_arr, columns= feature_names)
        self.phish_prob = self.get_phish_prob()
        self.verdict = self.get_verdict()
        self.trust_score = self.get_trust_score()
 
    def get_final_url(self):
        return URLFeatures(self.url).url

    def get_phish_prob(self):
        # Probability to be phishing url
        prob = self.model.predict_proba(self.features_df)[0, 1]
        return float(prob)
    
    def get_verdict(self):
        if self.url_obj.soup is None:
            return 'unknown'
        else:
            if self.phish_prob > 0.90: # 0.90 - 1.0
                return 'malicious'
            elif self.phish_prob > 0.50: # 0.50 - 0.90
                return 'suspicious'
            else: # 0.50 - 0.00  
                return 'safe'

    def get_trust_score(self):
        safe_prob = 1 - self.phish_prob
        score = (safe_prob) * 5
        return round(score,2)    

    def get_isPhish(self):
        # 0 means safe, 1 means phish
        return self.model.predict(self.features_df)[0]
    
    def get_model_features(self):
        return self.model_features
    
    def get_extra_info(self):
        return self.extra_info
    

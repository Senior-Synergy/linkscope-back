import numpy as np
import pandas as pd
from .urlfeatures import URLFeatures
from .constants import feature_names, feature_names2
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
    
    #-------------extrafeatures-------------------------------------------
    def get_extra_features(self):
        return  self.extra_features
    
    def get_whois_features(self):
        whois_data = json.dumps(self.whois_data, default=serialize_datetime)
        return whois_data
    

import numpy as np
import pandas as pd
from .urlfeatures import URLFeatures
from .constants import feature_names, feature_names2


class URLresult:
    def __init__(self, url, model):
        self.model = model
        self.url = url  # 1
        obj = URLFeatures(url)
        self.features_arr = np.array(obj.getFeaturesList()).reshape(1, 29)
        self.features_df = pd.DataFrame(
            self.features_arr, columns=feature_names)  # 2

    def get_final_url(self):
        return URLFeatures(self.url).url

    def get_phish_prob(self):
        # Probability to be phishing url
        return self.model.predict_proba(self.features_df)[0, 1]

    def get_isPhish(self):
        # 0 means safe, 1 means phish
        return self.model.predict(self.features_df)[0]


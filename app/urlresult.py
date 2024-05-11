import enum
import numpy as np
import pandas as pd
from app.urlfeatures import URLFeatures
from app.constants import feature_names
from datetime import datetime

from app.utils import load_joblib_model


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


class URLResult:
    def __init__(self, feature: URLFeatures):
        model = load_joblib_model("data/model.joblib")

        # Initialize
        self.final_url = feature.final_url
        self.feature = feature

        # Format feature items to be used with the model
        feature_array = np.array(
            list(feature.get_model_features().values())[:19]).reshape(1, 19)
        feature_df = pd.DataFrame(
            feature_array, columns=feature_names)

        # Model classification
        self.is_phish = int(model.predict(feature_df)[0])
        self.phish_prob = float(model.predict_proba(feature_df)[0, 1])

        # Post-processing
        self.google_malicious_flag = feature.get_google_is_malicious()
        self.phish_prob_mod = self.get_phish_prob_mod()
        self.has_soup = self.get_has_soup()

    def get_has_soup(self):
        if self.feature.soup is None:
            return False
        else:
            return True

    def get_results(self):
        return {
            "phish_prob": self.phish_prob,
            "phish_prob_mod": self.phish_prob_mod,
            "has_soup": self.has_soup,
        }

    def get_phish_prob_mod(self):
        phish_prob_mod = self.phish_prob

        if self.google_malicious_flag is not None:
            model_weight = 0.5

            phish_prob_mod = (phish_prob_mod * model_weight) + \
                (int(self.google_malicious_flag == True) * (1 - model_weight))

        return phish_prob_mod

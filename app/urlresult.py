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
        self.google_malicious_flag = feature.google_safe_browsing()
        self.phish_prob_mod = self.get_phish_prob_mod()
        self.verdict = self.get_verdict()
        self.trust_score = self.get_trust_score()
        
    def get_phish_prob_mod(self):
        phish_prob_mod = self.phish_prob

        if self.google_malicious_flag is not None:
            model_weight = 0.5

            phish_prob_mod = (phish_prob_mod * model_weight) + \
                (int(self.google_malicious_flag == True) * (1 - model_weight))
        
        return phish_prob_mod

    def get_trust_score(self) -> float:
        safe_prob = 1 - self.phish_prob_mod
        score = (safe_prob) * 5
        return round(score, 2)

    def get_verdict(self) -> str:
        if self.feature.soup:
            if self.phish_prob_mod < 0.2:
                return "VERY_LOW"
            elif self.phish_prob_mod < 0.4:
                return "LOW"
            elif self.phish_prob_mod < 0.6:
                return "MEDIUM"
            elif self.phish_prob_mod < 0.8:
                return "HIGH"
            else:
                return "VERY_HIGH"
        else:
            return "UNKNOWN"

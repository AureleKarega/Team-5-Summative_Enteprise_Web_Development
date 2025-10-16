# Thin wrapper if you want separated file
from .cleaner import advanced_clean_and_enrich

def apply_feature_engineering(df):
    return advanced_clean_and_enrich(df)

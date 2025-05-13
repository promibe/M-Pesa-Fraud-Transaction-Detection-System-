import numpy as np
import pandas as pd
from Fraud_detective_preprocessor_and_predictor import preprocess_and_predict
from Detective_GUI import  test_df
import joblib

with open('Fraud_detection_scaler.pkl', 'rb') as std_scaler:
    std_scaler = joblib.load(std_scaler)

with open('Fraud_detection_iso_forest.pkl', 'rb') as iso:
    iso_cls = joblib.load(iso)

with open('Fraud_detection_best_rf.pkl', 'rb') as rf_model:
    rf_cls = joblib.load(rf_model)
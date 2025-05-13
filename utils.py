import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler

with open('Fraud_detection_scaler.pkl', 'rb') as std_scaler:
    std_scaler = joblib.load(std_scaler)


with open('Fraud_detection_best_rf.pkl', 'rb') as rf_model:
    rf_cls = joblib.load(rf_model)
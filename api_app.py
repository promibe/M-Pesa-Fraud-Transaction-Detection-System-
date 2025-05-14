import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from Email_Notifier import mail_sender
import os
import json
from fastapi.responses import JSONResponse


def utils():

    with open('models/Fraud_detection_scaler.pkl', 'rb') as std_scaler:
        std_scaler = joblib.load(std_scaler)

    with open('models/Fraud_detection_iso_forest.pkl', 'rb') as iso:
        iso_cls = joblib.load(iso)

    with open('models/Fraud_detection_best_rf.pkl', 'rb') as rf_model:
        rf_cls = joblib.load(rf_model)

    return std_scaler, iso_cls, rf_cls

std_scaler, iso_cls, rf_cls = utils()

app = FastAPI()

# Define the expected request format
class TransactionInput(BaseModel):
    amount: float
    sim_swap_flag: Literal["Yes", "No"]
    balance_before: float
    balance_after: float
    transaction_velocity: int
    timestamp: str  # Expected in 'YYYY-MM-DD HH:MM:SS'

@app.post("/predict/")
def preprocess_and_predict(df: TransactionInput):
    df = pd.DataFrame([df.dict()])
    original_df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Encoding the hour of day and the day of week feature to capture real life time and day instead of it numerical value
    # Derive time-based features
    df["hour_of_day"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24)

    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)

    df['sim_swap_flag'] = df['sim_swap_flag'].map({'Yes': 1, 'No': 0})

    selected_columns = ['amount', 'sim_swap_flag', 'balance_before', 'balance_after', 'transaction_velocity',
                        'hour_of_day', 'day_of_week', 'hour_sin', 'hour_cos', 'day_sin', 'day_cos']
    df_selected_columns = df.copy()
    df_selected_columns = df[selected_columns]

    # scaling
    df_scaled = df_selected_columns.copy()
    df_scaled[selected_columns] = std_scaler.transform(df_scaled)
    predictors = ['amount', 'balance_before', 'balance_after', 'hour_sin', 'hour_cos', 'day_sin', 'day_cos',
                  'transaction_velocity']
    df_for_prediction = df_scaled.copy()
    df_for_prediction = df_scaled[predictors]

    # predicting with isolation forest
    is_anomaly = iso_cls.predict(df_for_prediction)
    # trigerring ther random forest classifier if isolation forest does its prediction
    if is_anomaly[0] == -1:
        #predicting with random forest
        rf_predict = rf_cls.predict(df_for_prediction)

        # if rf_predict != is_anomaly: # if the prediction of the iso_forest is not equal to the random forest choose the random forest prediction.
        prediction = rf_predict[0]
        #original_df['is_fraud'] = prediction

        if prediction == 1:
            result = f'''Alert Fraudulent Transaction just occured
                         Time: {df['timestamp'].values[0]}
                         Amount: {df['amount'].values[0]}'''
        else:
            result = f'Genuine Transaction'
    else:
        prediction = 0
        result = f'Genuine Transaction'


    # ==========================================================================

    # Path to your transaction log file
    log_file = "input/transaction_log.json"

    # Prepare the log entry
    log_entry = {
        "amount": float(original_df["amount"].values[0]),
        "sim_swap_flag": original_df["sim_swap_flag"].values[0],
        "balance_before": float(original_df["balance_before"].values[0]),
        "balance_after": float(original_df["balance_after"].values[0]),
        "transaction_velocity": int(original_df["transaction_velocity"].values[0]),
        "timestamp": str(original_df["timestamp"].values[0]),
        "is_fraud": int(prediction)
    }


    # Read or initialize the data
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            data = json.load(f)
    else:
        data = {
            "amount": [],
            "sim_swap_flag": [],
            "balance_before": [],
            "balance_after": [],
            "transaction_velocity": [],
            "timestamp": [],
            "is_fraud": []
        }

    # Append the new log entry
    for key, value in log_entry.items():
        data[key].append(value)

    # Write back to the file
    with open(log_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Log entry saved: {log_entry}")

    # =====================================================================================

    print(result)
    print(prediction)

    mail_sender(result)

    return JSONResponse(content={
        "prediction": int(prediction),
        "result": result
    })


import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle

def utils():
    with open('models/Fraud_detection_scaler.pkl', 'rb') as std_scaler:
        std_scaler = joblib.load(std_scaler)

    with open('models/Fraud_detection_iso_forest.pkl', 'rb') as iso:
        iso_cls = joblib.load(iso)

    with open('models/Fraud_detection_best_rf.pkl', 'rb') as rf_model:
        rf_cls = joblib.load(rf_model)

    return std_scaler, iso_cls, rf_cls

std_scaler, iso_cls, rf_cls = utils()
def preprocess_and_predict(df, std_scaler, iso_cls, rf_cls):
    inputed_df = df.copy()
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
    df_1 = df.copy()
    df_1 = df[selected_columns]

    # scaling
    df_2 = df_1.copy()
    df_2[selected_columns] = std_scaler.transform(df_1)
    predictors = ['amount', 'balance_before', 'balance_after', 'hour_sin', 'hour_cos', 'day_sin', 'day_cos',
                  'transaction_velocity']
    df_3 = df_2.copy()
    df_3 = df[predictors]

    # predicting with isolation forest
    is_anomaly = iso_cls.predict(df_3)
    # trigerring ther random forest classifier if isolation forest does its prediction
    if is_anomaly == -1:
        #predicting with random forest
        rf_predict = rf_cls.predict(df_3)

        # if rf_predict != is_anomaly: # if the prediction of the iso_forest is not equal to the random forest choose the random forest prediction.
        prediction = rf_predict[0]
        inputed_df['is_fraud'] = prediction

        if prediction == 1:
            result = f'''Alert Fraudulent Transaction just occured
                         Time: {df['timestamp'].values[0]}
                         Amount: {df['amount'].values[0]}'''
        else:
            result = f'Genuine Transaction'
    else:
        prediction = 0
        result = f'Genuine Transaction'

    #saving the dataframe value to the textfile

    input_list = list(inputed_df.values[0])

    line = ', '.join(map(str, input_list)) + '\n'

    try:
        # Try opening in read mode to check if file exists
        with open('input/passed_transaction.txt', 'r'):
            pass
        # File exists, so append
        with open('input/passed_transaction.txt', 'a') as f:
            f.write(line)
    except FileNotFoundError:
        # File does not exist, create it
        with open('input/passed_transaction.txt', 'w') as f:
            f.write(line)

    print(result)
    print(prediction)
    return prediction, result




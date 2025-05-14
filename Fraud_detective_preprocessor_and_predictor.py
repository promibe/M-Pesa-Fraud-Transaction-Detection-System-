import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from utils import std_scaler, rf_cls


# creating the function for preprocessing
#steps involved in preprocessing
# 1. convert timestamp to datetime datatype
# 2. slice out the hour and day of week from the timestamp, feature engineer the sliced day and time.
# 3. scale the selected features
# 4. use the isolation model to predict
# 5. add the isolation prediction to the entered record
# 6. use the random forest model to predict if its actually an anomaly or not

#loading the required dumped files

def preprocess_and_predict(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    #Encoding the hour of day and the day of week feature to capture real life time and day instead of it numerical value
    # Derive time-based features
    df["hour_of_day"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24)

    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)

    df['sim_swap_flag'] = df['sim_swap_flag'].map({'Yes':1, 'No':0})

    selected_columns = ['amount', 'sim_swap_flag', 'balance_before', 'balance_after','transaction_velocity', 'hour_of_day', 'day_of_week', 'hour_sin','hour_cos', 'day_sin', 'day_cos']
    df_1 = df.copy()
    df_1 = df[selected_columns]
    
    #scaling
    df_2 = df_1.copy()
    df_2[selected_columns] = std_scaler.transform(df_1)
    predictors = ['amount','balance_before','balance_after','hour_sin','hour_cos','day_sin','day_cos','transaction_velocity']
    df_3 = df_2.copy()
    df_3 = df[predictors]
    
    #predicting with isolation forest
    is_anomaly = iso_cls.predict(df_3)
    #trigerring ther random forest classifier if isolation forest does its prediction
    if is_anomaly == -1:
        is_anomaly = 1  # this is to say that the transaction is an anomaly

    #    #predicting with random forest
        rf_predict = rf_cls.predict(df_3)

    #if rf_predict != is_anomaly: # if the prediction of the iso_forest is not equal to the random forest choose the random forest prediction.
        prediction = rf_predict[0]
        preprocess_and_predict.prediction = prediction
        print(preprocess_and_predict.prediction)
        if preprocess_and_predict.prediction == 1:
            result = f'''Alert Fraudulent Transaction just occured
                         Time: {df['timestamp']}
                         Amount: {df['amount']}'''
        else:
            result = f'Genuine Transaction'

    return result






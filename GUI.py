import streamlit as st
import pandas as pd
from datetime import datetime
import requests
#from api_app import preprocess_and_predict

def user_input_streamlit():
    st.title("💳 Mobile Money Transaction Checker")
    st.subheader("Enter Transaction Details")

    amount = st.number_input("Enter Transaction Amount (NGN)", min_value=0, step=500)
    sim_swap_flag = st.selectbox("Was the SIM recently swapped?", ['Yes', 'No'])
    balance_before = st.number_input("Account Balance Before Transaction (NGN)", min_value=0.0, step=100.0)
    transaction_velocity = st.slider("Number of transactions in the past hour", 0, 10, 1)

    # Separate date and time inputs
    date_part = st.date_input("Transaction Date", value=datetime.now().date())
    time_part = st.time_input("Transaction Time", value=datetime.now().time())

    # Combine into full datetime
    timestamp = datetime.combine(date_part, time_part)
    timestamp = timestamp.replace(microsecond=0)
    email = st.text_input("Enter Email Address: ")

    balance_after = balance_before - amount

    if st.button("Submit Transaction"):
        test_df = pd.DataFrame({
            'amount': [amount],
            'sim_swap_flag': [sim_swap_flag],
            'balance_before': [balance_before],
            'balance_after': [balance_after],
            'transaction_velocity': [transaction_velocity],
            'timestamp': [timestamp.strftime('%Y-%m-%d %H:%M:%S')],
            'email': [email]
        })

        # Convert to dictionary for JSON serialization
        payload = test_df.to_dict(orient='records')[0]

        response = requests.post("http://localhost:8000/predict/", json=payload)

        if response.status_code == 200:
            json_response = response.json()
            #st.success(f"Prediction: {result['result']} (Anomaly Detected: {result['anomaly_flag']})")
            st.success(f"Transaction submitted successfully! at {timestamp} - {payload} - {response}")

        else:
            st.error("Prediction failed. Check your API server.")

        return None

    return None

user_input_streamlit()




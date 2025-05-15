import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle
from utils import utils
from user_input import user_input
import smtplib
from email.message import EmailMessage

def mail_sender(result, email):
    print('sending Mail for Transaction that occured')
    MY_EMAIL = 'pro9jaeduinfo@gmail.com'
    MY_PASSWORD = 'bykfvsekinohtxkj'

    msg = EmailMessage()# Prepare the email content
    msg.set_content(result)  # Assuming format_article_list is a string
    msg['Subject'] = 'Fraudulent Transaction Alert: Notified From SigFinance'
    msg['From'] = MY_EMAIL
    msg['To'] = email

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as conn:
        conn.starttls()
        conn.login(user=MY_EMAIL, password=MY_PASSWORD)
        conn.send_message(msg)
        print('sent')

    return None
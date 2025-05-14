#from Detective_GUI import test_df
import pandas as pd
from Fraud_detective_preprocessor_and_predictor import preprocess_and_predict

amount = int(input('Enter amount: '))
sim_swap_flag = input('Was the sim swapped or Not(Yes/No) ')
balance_before = float(input('What is the account balance before transaction: '))
balance_after = float(input('What is the account balance before transaction: '))
transaction_velocity = int(input('How transaction has been done before this one? 0, 1, 2, 3, 4 ... '))
timestamp = input('What date and time was the transaction done ? eg. 2024-03-25 16:38:00 ' )


test_df = pd.DataFrame({
    'amount':[amount],
    'sim_swap_flag': [sim_swap_flag],
    'balance_before':[balance_before],
    'balance_after':[balance_after],
    'transaction_velocity':[transaction_velocity], 
    'timestamp': [timestamp]
})


preprocess_and_predict(test_df)

test_df['is_fraud'] = preprocess_and_predict.predict

input_list = list(test_df.values[0])
line = ', '.join(map(str, input_list)) + '\n'

try:
    # Try opening in read mode to check if file exists
    with open('passed_transaction.txt', 'r'):
        pass
    # File exists, so append
    with open('passed_transaction.txt', 'a') as f:
        f.write(line)
except FileNotFoundError:
    # File does not exist, create it
    with open('passed_transaction.txt', 'w') as f:
        f.write(line)
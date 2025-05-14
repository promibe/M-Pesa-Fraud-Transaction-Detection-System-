import pandas as pd

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

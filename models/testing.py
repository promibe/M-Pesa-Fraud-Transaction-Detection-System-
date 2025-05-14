import os
import json

# Path to your transaction log file
log_file = "transaction_log.json"

log_entry = {
        "amount": 20000,
        "sim_swap_flag": 'Yes',
        "balance_before": 50000,
        "balance_after": 30000,
        "transaction_velocity": 1,
        "timestamp": '2024-03-25 16:38:00',
        "is_fraud": 1
    }
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

for key, value in log_entry.items():
    data[key].append(value)

with open(log_file, "w") as f:
    json.dump(data, f, indent=4)
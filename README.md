# Project Title
## Mobile Money Fraud Detection System

### Description
This project implements a fraud detection system for mobile money transactions. It consists of:

A FastAPI backend that runs fraud detection models (Isolation Forest and Random Forest).

Two Streamlit GUIs: one for submitting transactions and getting fraud predictions, and another dashboard for viewing transaction logs, visualizing fraud distribution, and analyzing transaction trends.

### Features
1. Real-time fraud prediction API using machine learning models.
2. Interactive transaction submission interface (Streamlit GUI).
3. Transaction dashboard with pie chart, time series, and tables to monitor fraud patterns.
4. Dockerized deployment for easy setup and scaling.
5. Email alerts on detecting fraudulent transactions.

### Workflow
##### 1. Data Collection and Data Exploration:
   * The data used for this Project was provided by Sigfinance Nigeria Limited, the dataset contains about 5,0000 entries and 13 columns
   * There were no missing values and duplicates identified in the dataset.
   * There were about 9 numeric columns and 4 object columns.
##### 2. Data Preprocessing and Feature Engineering 
   * The object datatype columns were converted to numerical datatype where applicable.
   * The timestamp column was also converted to a datetime datatype, then time of day, day of week was also derived
   * The derive day and time feature were engineer so as to model real life time and days circle, using the sine and cosine function.
   * 6 relevant feature were selected for our unsupervised learning model
##### 3. Model Building and Evaluation
   * The dataset was split into train and test set.
   * The train set was fit into an unsupervised machine learning model called Isolation forest, which was able to flag an anomaly and non-anomaly transaction.
   * The flag column was inbalanced, the SMOTE function was used to balance both classes.
   * After which the flag column was then used with the train set to fit it different supervised learnin classifiers such as Random Forest, Support Vector Machine, Decision Tree.
   * After Cross-validation and fine-tuning Random Forest Model came out with the optimal f1_scure of accuracy of `73.45%` and ROC-AUC of `92.5%`
##### 4. Model Deployment
   * The GUI for both the Fraud Detector and Monitoring Dashboard were created with streamlit and Deploy.
   * A Docker image file was created for continuous deployment 

### Installation
<b>Prerequisites</b>

Python 3.10+

Docker (optional, for containerized deployment)

### Setup
1. Clone the repository

        git clone https://github.com/promibe/Mobile-Fraud-Transaction-Detection-System-.git


2. Install dependencies

        pip install -r requirements.txt

3. Run the API server

        uvicorn api_app:app --host 0.0.0.0 --port 8000

4. Run the Streamlit GUIs

        streamlit run GUI.py --server.port 8501
        streamlit run Dashboard.py --server.port 8502

5. Usage

Open your browser at http://localhost:8501 to submit transactions for fraud prediction.

Open http://localhost:8502 to view the transaction dashboard. 

### Docker Deployment
1. Build the Docker image:

        docker build -t fraud-detection-app .
2. Run the container:

        docker run -p 8000:8000 -p 8501:8501 -p 8502:8502 fraud-detection-app


### Folder structure


        
        Mobile-Fraud-Transaction-Detection-System-[M]/
        ├── input/
        │   ├── passed_transaction.txt
        │   └── transaction_log.json
        │
        ├── models/
        │   ├── Fraud_detection_best_rf.pkl
        │   ├── Fraud_detection_iso_forest.pkl
        │   └── Fraud_detection_scaler.pkl
        │
        ├── testing.py
        ├── .dockerignore
        ├── api_app.py
        ├── Dashboard.py
        ├── dataset_script.ipynb
        ├── Dockerfile
        ├── Email_Notifier.py
        ├── Fraud_detection.ipynb
        ├── GUI.py
        ├── main.py
        ├── mobile_money_transactions.csv
        ├── passed_transaction.txt
        ├── README.md
        ├── requirements.txt
        ├── Sigfinance Mobile Transaction Detector.mp4
        └── user_input.py



### Acknowledgments
1. FastAPI, Streamlit, Scikit-learn for frameworks and libraries

2. smtp module for sending fraud alerts

3. SigFinance for the Inspiration from real-world mobile money fraud use cases


Developer name: Promise Ibediogwu Ekele.

Developer email: Promiseibedogwu1@gmail.com

Phone number: (+234)7063083925


<b>SigFinance-Fraud-Transaction-Detection-System-</b>


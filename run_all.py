# run_all.py
import subprocess
import time

# Start FastAPI app
subprocess.Popen(["uvicorn", "api_app.main:app", "--host", "0.0.0.0", "--port", "8000"])

# Start Streamlit GUIs
subprocess.Popen(["streamlit", "run", "GUI.py", "--server.port=8501"])
subprocess.Popen(["streamlit", "run", "Dashboard.py", "--server.port=8502"])

# Keep container alive
while True:
    time.sleep(1)

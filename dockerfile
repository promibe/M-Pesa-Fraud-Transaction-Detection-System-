FROM python:3.10-slim

WORKDIR /fraud_detector

COPY . /fraud_detector

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8501 8502

CMD sh -c "uvicorn api_app:app --host 0.0.0.0 --port 8000 & \
                  streamlit run GUI.py --server.port 8501 & \
                  streamlit run Dashboard.py --server.port 8502 & \
                  wait"
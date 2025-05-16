FROM python:3.10-slim

WORKDIR /fraud_detector

COPY . /fraud_detector

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8501 8502

CMD ["python", "run_all.py"]
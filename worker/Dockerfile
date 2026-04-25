FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir grpcio grpcio-tools scikit-learn joblib numpy

COPY . .

RUN python train.py
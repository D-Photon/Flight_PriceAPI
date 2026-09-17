FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY flight_server.py .
COPY flight_price_model3.pkl .

EXPOSE 10000

CMD ["sh", "-c", "uvicorn flight_server:app --host 0.0.0.0 --port ${PORT:-10000}"]
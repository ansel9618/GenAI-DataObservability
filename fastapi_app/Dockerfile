FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y gcc build-essential

RUN pip install fastapi uvicorn sentence-transformers qdrant-client clickhouse-connect

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

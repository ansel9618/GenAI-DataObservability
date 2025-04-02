FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install duckdb

CMD ["python", "wal_to_duckdb.py"]

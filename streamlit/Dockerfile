
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y gcc build-essential

RUN pip install \
    streamlit \
    pandas \
    sentence-transformers \
    qdrant-client \
    duckdb

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

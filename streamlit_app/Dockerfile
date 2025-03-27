FROM python:3.10-slim

WORKDIR /app
COPY . .

# Install necessary system packages
RUN apt-get update && apt-get install -y gcc build-essential

# Install Python dependencies
RUN pip install \
    streamlit \
    requests \
    sentence-transformers \
    qdrant-client \
    clickhouse-connect==0.6.6 \
    pandas

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

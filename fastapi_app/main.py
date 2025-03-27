from fastapi import FastAPI
from pydantic import BaseModel
from embedding import embed_text
from qdrant_writer import store_vector
from clickhouse_writer import insert_log, get_client, create_logs_table

app = FastAPI()

class LogEntry(BaseModel):
    timestamp: str
    level: str
    service: str
    message: str

client = get_client()
create_logs_table(client)

@app.post("/logs")
def ingest_log(log: LogEntry):
    embedding = embed_text(log.message)
    metadata = log.model_dump()  # ✅ modern Pydantic way
    store_vector(embedding, metadata)
    insert_log(client, metadata)
    return {"status": "ok"}


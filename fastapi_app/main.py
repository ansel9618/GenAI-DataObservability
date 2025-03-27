from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from embedding import embed_text
from qdrant_writer import store_vector
from duckdb_writer import insert_log

app = FastAPI()

class LogEntry(BaseModel):
    timestamp: str
    level: str
    service: str
    message: str

@app.post("/logs")
def ingest_log(log: LogEntry):
    embedding = embed_text(log.message)
    metadata = log.dict()
    store_vector(embedding, metadata)
    insert_log(metadata)
    return {"status": "ok"}
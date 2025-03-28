from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from embedding import embed_text
from qdrant_writer import store_vector
from clickhouse_writer import insert_log, get_client, create_logs_table

app = FastAPI()

class LogEntry(BaseModel):
    timestamp: str
    level: str
    service: str
    job_name: Optional[str] = None
    step_name: Optional[str] = None
    pipeline_id: Optional[str] = None
    duration_ms: Optional[int] = 0
    records_processed: Optional[int] = 0
    records_failed: Optional[int] = 0
    status_code: Optional[int] = 0
    host: Optional[str] = None
    thread: Optional[str] = None
    environment: Optional[str] = None
    tags: Optional[List[str]] = []
    message: str
    request_id: Optional[str] = None

client = get_client()
create_logs_table(client)

@app.post("/logs")
def ingest_log(log: LogEntry):
    embedding = embed_text(log.message)
    metadata = log.model_dump()  # ✅ modern Pydantic way
    store_vector(embedding, metadata)
    insert_log(client, metadata)
    return {"status": "ok"}


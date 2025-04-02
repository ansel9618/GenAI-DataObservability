from fastapi import FastAPI
from pydantic import BaseModel
from embedding import embed_text
from qdrant_writer import store_vector
from wal_writer import write_to_wal

app = FastAPI()

class LogEntry(BaseModel):
    timestamp: str
    level: str
    service: str
    job_name: str = ""
    step_name: str = ""
    pipeline_id: str = ""
    duration_ms: int = 0
    records_processed: int = 0
    records_failed: int = 0
    status_code: int = 0
    host: str = ""
    thread: str = ""
    environment: str = ""
    tags: list = []
    message: str
    request_id: str = ""

@app.post("/logs")
def ingest_log(log: LogEntry):
    embedding = embed_text(log.message)
    metadata = log.model_dump()
    store_vector(embedding, metadata)
    write_to_wal(metadata)
    return {"status": "ok"}

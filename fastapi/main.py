from fastapi import FastAPI
from pydantic import BaseModel
from embedding import embed_log
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
    metadata = log.model_dump()
    embedding = embed_log(metadata)
    store_vector(embedding, metadata)
    write_to_wal(metadata)  # writing to the Write ahead log. 
    return {"status": "ok"}

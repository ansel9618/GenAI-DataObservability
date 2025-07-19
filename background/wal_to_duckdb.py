import json
from pathlib import Path
import duckdb
from datetime import datetime
import time

WAL_PATH = Path("/data/wal.jsonl")
PROCESSED_PATH = Path("/data/wal.processed.jsonl")
DB_PATH = "/data/logs.duckdb"

def insert_log(conn, log):
    ts = datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00"))
    conn.execute("""
        INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ts,
        log.get("level"),
        log.get("service"),
        log.get("job_name", ""),
        log.get("step_name", ""),
        log.get("pipeline_id", ""),
        log.get("duration_ms", 0),
        log.get("records_processed", 0),
        log.get("records_failed", 0),
        log.get("status_code", 0),
        log.get("host", ""),
        log.get("thread", ""),
        log.get("environment", ""),
        str(log.get("tags", [])),
        log.get("message"),
        log.get("request_id", "")
    ])
    conn.execute("CHECKPOINT")

def run():
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            timestamp TIMESTAMP,
            level TEXT,
            service TEXT,
            job_name TEXT,
            step_name TEXT,
            pipeline_id TEXT,
            duration_ms INTEGER,
            records_processed INTEGER,
            records_failed INTEGER,
            status_code INTEGER,
            host TEXT,
            thread TEXT,
            environment TEXT,
            tags TEXT,
            message TEXT,
            request_id TEXT
        )
    """)

    while True:
        if WAL_PATH.exists():
            # This opens only a single wal file that is always the same, better would be here to read all files in the wal folder
            with open(WAL_PATH, "r") as f_in, open(PROCESSED_PATH, "a") as f_out:  
                for line in f_in:
                    try:
                        log = json.loads(line)
                        insert_log(conn, log)
                        f_out.write(line)
                    except Exception as e:
                        print(f"Failed to process line: {line} — {e}")
            # this deletes the wal if successful or not. Implement logic here to store the not succesful ones. How to do retires?
            WAL_PATH.unlink() 
        time.sleep(5)

if __name__ == "__main__":
    run()

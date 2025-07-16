import duckdb
from datetime import datetime

# we don't need this when we use the write ahead log

def get_connection():
    return duckdb.connect("/data/logs.duckdb")

def create_table(conn):
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

def insert_log(conn, log):
    ts = datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00"))
    conn.execute("""
        INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ts,
        log.get("level"),
        log.get("service"),
        log.get("job_name"),
        log.get("step_name"),
        log.get("pipeline_id"),
        log.get("duration_ms", 0),
        log.get("records_processed", 0),
        log.get("records_failed", 0),
        log.get("status_code", 0),
        log.get("host"),
        log.get("thread"),
        log.get("environment"),
        str(log.get("tags", [])),
        log.get("message"),
        log.get("request_id")
    ])

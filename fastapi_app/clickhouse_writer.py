import clickhouse_connect
from datetime import datetime

# Initialize ClickHouse client
def get_client():
    return clickhouse_connect.get_client(
        host="clickhouse",
        port=8123,
        username="default",
        password="mysecret"  # Make sure this matches your config
    )

def create_logs_table(client):
    client.command("""
        CREATE TABLE IF NOT EXISTS logs (
            timestamp DateTime,
            level String,
            service String,
            job_name String,
            step_name String,
            pipeline_id String,
            duration_ms UInt32,
            records_processed UInt32,
            records_failed UInt32,
            status_code UInt16,
            host String,
            thread String,
            environment String,
            tags Array(String),
            message String,
            request_id String
        ) ENGINE = MergeTree()
        ORDER BY timestamp
    """)

def insert_log(client, log_entry):
    # Convert timestamp from string to datetime
    ts = datetime.fromisoformat(log_entry["timestamp"].replace("Z", "+00:00"))

    # Insert all fields in the correct order
    client.insert("logs", [[
        ts,
        log_entry.get("level", ""),
        log_entry.get("service", ""),
        log_entry.get("job_name", ""),
        log_entry.get("step_name", ""),
        log_entry.get("pipeline_id", ""),
        int(log_entry.get("duration_ms", 0)),
        int(log_entry.get("records_processed", 0)),
        int(log_entry.get("records_failed", 0)),
        int(log_entry.get("status_code", 0)),
        log_entry.get("host", ""),
        log_entry.get("thread", ""),
        log_entry.get("environment", ""),
        log_entry.get("tags", []),
        log_entry.get("message", ""),
        log_entry.get("request_id", "")
    ]], column_names=[
        "timestamp", "level", "service", "job_name", "step_name", "pipeline_id",
        "duration_ms", "records_processed", "records_failed", "status_code",
        "host", "thread", "environment", "tags", "message", "request_id"
    ])




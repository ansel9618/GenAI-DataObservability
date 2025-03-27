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

# Ensure the logs table exists
def create_logs_table(client):
    client.command("""
        CREATE TABLE IF NOT EXISTS logs (
            timestamp DateTime,
            level String,
            service String,
            message String
        ) ENGINE = MergeTree()
        ORDER BY timestamp
    """)

# Insert one log entry into the table
def insert_log(client, log_entry):
    # Convert timestamp string (ISO 8601) to datetime object
    ts_str = log_entry["timestamp"]
    ts_obj = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

    client.insert(
        "logs",
        [[
            ts_obj,
            log_entry["level"],
            log_entry["service"],
            log_entry["message"]
        ]],
        column_names=["timestamp", "level", "service", "message"]
    )

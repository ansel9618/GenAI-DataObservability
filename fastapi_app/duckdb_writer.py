import duckdb

conn = duckdb.connect("/data/logs.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS logs (
    timestamp TIMESTAMP,
    level VARCHAR,
    service VARCHAR,
    message TEXT
)
""")

def insert_log(log):
    conn.execute(
        "INSERT INTO logs VALUES (?, ?, ?, ?)",
        (log["timestamp"], log["level"], log["service"], log["message"])
    )
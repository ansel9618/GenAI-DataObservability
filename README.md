# Quick helper

# log into clickhouse container and run client
docker compose exec clickhouse clickhouse-client

# drop table
DROP TABLE IF EXISTS logs;

# recreate log table
CREATE TABLE logs (
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
ORDER BY timestamp;

# check table structure and data
DESCRIBE TABLE logs;
DESCRIBE TABLE logs;

# Docker path variable
export PATH="$PATH:/Applications/Docker.app/Contents/Resources/bin"

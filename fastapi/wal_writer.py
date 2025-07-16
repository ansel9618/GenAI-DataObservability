import json
from pathlib import Path

WAL_PATH = Path("/data/wal.jsonl")

# writing the logs to the WAL for processing to not have locks on the duckdb file
# Write in append mode does not lock the file, but can still lead to problems when multiple processes write at the same time which corrupts the line. 
# We would need a dynamic wal filename for this (e.g with timestamp prefix, then you could even sort it on writing the wal)

def write_to_wal(log_dict):
    with open(WAL_PATH, "a") as f:
        f.write(json.dumps(log_dict) + "\n")

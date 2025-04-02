import json
from pathlib import Path

WAL_PATH = Path("/data/wal.jsonl")

def write_to_wal(log_dict):
    with open(WAL_PATH, "a") as f:
        f.write(json.dumps(log_dict) + "\n")

import json
import requests
from time import sleep
import os

# Get path to current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
jsonl_file = os.path.join(script_dir, "sample_logs.jsonl")

# Load log entries from the JSONL file
with open(jsonl_file, "r") as f:
    log_entries = [json.loads(line.strip()) for line in f.readlines()]

# Post logs to FastAPI
for i, log in enumerate(log_entries):
    try:
        response = requests.post("http://localhost:8000/logs", json=log)
        print(f"[{i+1}/{len(log_entries)}] Status: {response.status_code}")
        sleep(0.05)  # small delay between posts
    except Exception as e:
        print(f"❌ Failed to post log {i+1}: {e}")


import json
import requests
from time import sleep

with open("sample_logs.jsonl", "r") as f:
    log_entries = [json.loads(line.strip()) for line in f.readlines()]

for i, log in enumerate(log_entries):
    try:
        response = requests.post("http://localhost:8000/logs", json=log)
        print(f"[{i+1}/100] Status: {response.status_code}")
        sleep(0.05)
    except Exception as e:
        print(f"❌ Failed to post log {i+1}: {e}")

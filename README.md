# Quick helper

# install duckdb in a container
## 1. Install wget and unzip if missing
apt-get update && apt-get install -y wget unzip

## 2. Download the DuckDB CLI binary
wget https://github.com/duckdb/duckdb/releases/download/v0.10.2/duckdb_cli-linux-amd64.zip

## 3. Unzip the binary
unzip duckdb_cli-linux-amd64.zip

## 4. Make it executable
chmod +x duckdb

## 5. Move it to /usr/local/bin so you can call it from anywhere
mv duckdb /usr/local/bin/

## 6. Clean up
rm duckdb_cli-linux-amd64.zip


# Docker path variable
export PATH="$PATH:/Applications/Docker.app/Contents/Resources/bin"


## ⚠️ Is WAL a Problem Under High Load?

Yes — it's important to think ahead if you're expecting a high volume of logs.

### 🔍 What's happening now?

Each request to FastAPI:
1. Encodes a vector with `SentenceTransformer`
2. Writes the full JSON log to `wal.jsonl` (on disk)
3. Sends the embedding + payload to Qdrant

This means every request touches the file system — even for a single log — which can cause:

| Risk                             | Explanation |
|----------------------------------|-------------|
| ⚠️ **Disk I/O pressure**         | Appending to a file thousands of times per second can slow things down |
| 🔐 **File lock contention**      | Python’s file writes are synchronous and blocking — no lock but still blocking |
| 🧱 **CPU bottleneck** (embedding) | SentenceTransformer is not async or GPU-accelerated unless you configure it |
| 🧨 **Qdrant overload**           | Too many writes to Qdrant could slow vector indexing |

---

### ✅ You're safe for...

- 💡 Dev / low-traffic apps
- 📊 Infrequent analytics use cases
- 🧪 Prototyping and testing

---

### 🧠 But for **high-throughput logging**, consider this:

#### ✅ Better write performance with **buffering**:
Use an in-memory buffer (e.g. `queue.Queue`) and flush to WAL in batches (e.g. every 1 sec or 50 logs). Faster and reduces disk writes.

#### ✅ Use **async file I/O**:
Switch from `open(..., "a")` to `aiofiles` or a dedicated log buffer thread to avoid blocking FastAPI handlers.

#### ✅ Run SentenceTransformer in **background thread or worker**:
It's CPU-heavy. Either offload to a background task (like Celery) or batch embeddings.

#### ✅ Use a real message queue (optional):
If you’re really scaling, tools like **Kafka**, **Redis Streams**, or **RabbitMQ** can replace the WAL, giving you full decoupling and resilience.

---

### ✅ Summary Table

| Load Level           | Action Needed       |
|----------------------|---------------------|
| 💡 Low (dev/test)     | ✅ You're fine       |
| ⚠️ Medium (burst logs)| 🔄 Add buffer to WAL |
| 🔥 High throughput    | 🧰 Consider queue, async I/O, batching |


                    ┌─────────────┐
                    │  FastAPI    │
                    │             │
                    │ Writes to   │
                    │ wal.jsonl   │
                    └────┬────────┘
                         │
                         ▼
             ┌─────────────────────┐
             │ WAL Processor       │
             │ (inserts into       │
             │  logs.duckdb)       │
             └────┬────────────────┘
                  │
                  ▼
          ┌─────────────────┐
          │ logs.duckdb     │
          └─────────────────┘
                  ▲
                  │  (read-only)
        ┌─────────┴────────────┐
        │     Streamlit        │
        │ Loads into memory 🧠 │
        └──────────────────────┘


--> WAL could be removed because not really necessary right now




message = Rate limit almost exceeded  |  environment = dev  | status = WARN
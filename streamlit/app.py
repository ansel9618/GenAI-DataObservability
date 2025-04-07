
import streamlit as st
import duckdb
import pandas as pd
import requests
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import shutil
import tempfile

st.title("📊 Log Inspector (DuckDB + Qdrant)")

# Qdrant client for semantic search
qdrant = QdrantClient(host="qdrant", port=6333)
model = SentenceTransformer("all-mpnet-base-v2")

temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".duckdb")
shutil.copy2("/data/logs.duckdb", temp_file.name)

# Step 2: Create an in-memory DuckDB and attach the copied DB file
conn = duckdb.connect()
conn.execute(f"ATTACH '{temp_file.name}' AS logs_db (READ_ONLY)")

query = st.text_input("Ask a question about the logs")

if st.button("Search Qdrant"):
    if query:
        query_vector = model.encode(query).tolist()
        results = qdrant.search(collection_name="logs", query_vector=query_vector, limit=30)

        if results:
            records = []
            for r in results:
                row = r.payload.copy()
                row["score"] = r.score
                records.append(row)
            df = pd.DataFrame(records)
            st.dataframe(df)
        else:
            st.warning("No results found.")
    else:
        st.warning("Please enter a query first.")

if st.button("Run SQL in DuckDB"):
    try:
        df = conn.execute("""
            SELECT service, COUNT(*) AS errors 
            FROM logs_db.logs
            WHERE level = 'ERROR'
            GROUP BY service
        """).fetchdf()
        st.bar_chart(df.set_index("service"))
    except Exception as err:
        st.error(f"DuckDB query failed: {err}")

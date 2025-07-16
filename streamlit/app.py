import streamlit as st
import duckdb
import pandas as pd
import requests
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import shutil
import tempfile

st.title("📊 Log Inspector (DuckDB + Qdrant)")

# Sidebar controls
use_formatting = st.sidebar.toggle("🧠 Use Smart Query Formatting", value=True)
score_threshold = st.sidebar.slider("🎯 Min Similarity Score", 0.0, 1.0, 0.4, 0.01)

# Qdrant client and model
qdrant = QdrantClient(host="qdrant", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")
# model = SentenceTransformer("all-mpnet-base-v2")

# Attach DuckDB (read-only snapshot)
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".duckdb")
shutil.copy2("/data/logs.duckdb", temp_file.name)
conn = duckdb.connect()
conn.execute(f"ATTACH '{temp_file.name}' AS logs_db (READ_ONLY)")

query = st.text_input("Ask a question about the logs")

def format_query(query: str) -> str:
    return (
        f"| {query} "
        f"| level | service | environment | job | step | message | status | duration | records_processed | records_failed | tags"
    )

if st.button("Search Qdrant"):
    if query:
        formatted_query = format_query(query) if use_formatting else query
        query_vector = model.encode(formatted_query).tolist()

        st.markdown("### 🔍 Query Debug Info")
        st.text(f"Formatted query: {formatted_query}")
        st.text(f"Vector length: {len(query_vector)}")
        st.text(f"Preview: {query_vector[:5]}")

        results = qdrant.search(collection_name="logs", query_vector=query_vector, limit=30)

        filtered_results = [r for r in results if r.score >= score_threshold]

        if filtered_results:
            #st.markdown("### Qdrant Results (raw debug view)")
            #for r in filtered_results:
            #    st.text(f"Score: {r.score:.2f}")
            #    st.write(r.payload.get("message", "(No message found)"))

            records = []
            for r in filtered_results:
                row = r.payload.copy()
                row["score"] = r.score
                records.append(row)

            df = pd.DataFrame(records)
            st.markdown("### Results Table")
            st.dataframe(df)
        else:
            st.warning("No results matched your threshold.")
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

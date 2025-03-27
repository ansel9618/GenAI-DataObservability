import streamlit as st
import requests
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import clickhouse_connect
import pandas as pd #in case we want to manipulate data with pandas (most likely)

st.title("📊 Log Inspector")

# Initialize clients
qdrant = QdrantClient(host="qdrant", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")
client = clickhouse_connect.get_client(
    host="clickhouse",
    port=8123,
    username="default",
    password="mysecret"
)


query = st.text_input("Ask a question about the logs")

if st.button("Search Qdrant"):
    if query:
        query_vector = model.encode(query).tolist()
        results = qdrant.search(collection_name="logs", query_vector=query_vector, limit=5)

        for r in results:
            st.markdown(f"**Message:** {r.payload.get('message')}")
            st.text(f"Score: {r.score}")
            st.json(r.payload)
    else:
        st.warning("Please enter a query first.")

if st.button("Run SQL in ClickHouse"):
    try:
        result = client.query("""
            SELECT service, COUNT(*) AS errors
            FROM logs
            WHERE level = 'ERROR'
            GROUP BY service
        """)

        # Manually build DataFrame (works on all versions)
        df = pd.DataFrame(result.result_rows, columns=result.column_names)

        st.bar_chart(df.set_index("service"))
    except Exception as e:
        st.error(f"ClickHouse query failed: {e}")

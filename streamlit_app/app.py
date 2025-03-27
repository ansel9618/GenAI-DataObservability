import streamlit as st
import duckdb
import requests

st.title("📊 Log Inspector")

query = st.text_input("Ask a question about the logs")

if st.button("Search Qdrant"):
    response = requests.post("http://fastapi:8000/embedding", json={"text": query})
    st.write("Search not yet implemented — will connect to Qdrant here.")

if st.button("Run SQL in DuckDB"):
    df = duckdb.query("""
        SELECT service, COUNT(*) AS errors FROM logs
        WHERE level='ERROR'
        GROUP BY service
    """).to_df()
    st.bar_chart(df.set_index("service"))
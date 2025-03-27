from qdrant_client import QdrantClient, models

client = QdrantClient(host="qdrant", port=6333)
COLLECTION = "logs"

def store_vector(embedding, metadata):
    client.upsert(
        collection_name=COLLECTION,
        points=[
            models.PointStruct(
                id=metadata['timestamp'] + metadata['service'],
                vector=embedding,
                payload=metadata
            )
        ]
    )
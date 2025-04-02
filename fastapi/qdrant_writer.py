from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
import uuid

client = QdrantClient(host="qdrant", port=6333)
COLLECTION = "logs"
VECTOR_SIZE = 384

def ensure_collection():
    if COLLECTION not in client.get_collections().collections:
        client.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )

ensure_collection()

def store_vector(embedding, metadata):
    point_id = str(uuid.uuid4())
    client.upsert(
        collection_name=COLLECTION,
        points=[
            models.PointStruct(
                id=point_id,
                vector=embedding,
                payload=metadata
            )
        ]
    )
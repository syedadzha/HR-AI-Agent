import os
import sys
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load env from the project root (assuming script is run from project root or similar context)
# We will try to load .env from typical locations
load_dotenv("backend/.env")
load_dotenv(".env")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "hr_docs"

def inspect():
    try:
        client = QdrantClient(url=QDRANT_URL)
        
        if not client.collection_exists(COLLECTION_NAME):
            print(f"❌ Collection '{COLLECTION_NAME}' does not exist.")
            return

        info = client.get_collection(COLLECTION_NAME)
        print(f"✅ Collection '{COLLECTION_NAME}' found.")
        print(f"   Points count: {info.points_count}")
        print(f"   Status: {info.status}")
        
        # Peek at top 3 items
        print("\n🔍 Peeking at top 3 vectors:")
        result = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=3,
            with_payload=True,
            with_vectors=False
        )
        
        for point in result[0]:
            print(f"   ID: {point.id}")
            print(f"   Payload: {point.payload}")
            print("   ---")
            
    except Exception as e:
        print(f"❌ Error connecting to Qdrant: {e}")

if __name__ == "__main__":
    inspect()

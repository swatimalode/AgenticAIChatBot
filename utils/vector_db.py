import chromadb
from config import MEMORY_PATH

client = chromadb.PersistentClient(
    path=MEMORY_PATH
)

def get_collection(name="documents"):
    return client.get_or_create_collection(
        name=name
    )
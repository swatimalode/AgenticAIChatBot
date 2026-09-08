from config import CHUNK_SIZE, OVERLAP_CHUNK_SIZE
from utils.vector_db import get_collection
from utils.embedding import create_embedding
import tiktoken
import uuid

tokenizer = tiktoken.get_encoding("cl100k_base")

def extractContent(file):
    content = file.file.read()
    return content.decode("utf-8")

def chunk(file, chunk_size=CHUNK_SIZE, overlap=OVERLAP_CHUNK_SIZE):
    text = extractContent(file)
    tokens = tokenizer.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        text_chunk = tokenizer.decode(chunk_tokens)
        chunks.append(text_chunk)
        start += chunk_size - overlap

    return chunks

def store(file):
    chunks = chunk(file)
    collection = get_collection("rag_documents")
    document_id = str(uuid.uuid4())

    for index, chunk_text in enumerate(chunks):
        embedding = create_embedding(chunk_text)
        collection.upsert(
            ids=[f"{document_id}_{index}"],
            embeddings=[embedding],
            documents=[chunk_text],
            metadatas=[{
                "document_id": document_id,
                "chunk_index": index,
                "filename": file.filename
            }]
        )
    return f"Document with Id: {document_id} uploaded successfully"

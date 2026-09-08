from memory.memory_manager import MemoryManager
from config import MAX_MESSAGES, SUMMERIZE_BATCH

memory = MemoryManager(MAX_MESSAGES, SUMMERIZE_BATCH)

def search_documents(query):
    results = memory.search_documnets(query)
    return results
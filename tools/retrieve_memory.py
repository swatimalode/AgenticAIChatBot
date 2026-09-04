from memory.memory_manager import MemoryManager
from config import MAX_MESSAGES, SUMMERIZE_BATCH, THRESHOLD

memory = MemoryManager(MAX_MESSAGES, SUMMERIZE_BATCH)

def retrieve_memory(query, memory_type, top_k=3):
    results = memory.retrieve_conversation(query, memory_type)

    return results
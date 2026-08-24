from memory.memory_manager import MemoryManager
from config import MAX_MESSAGES, SUMMERIZE_BATCH

memory = MemoryManager(MAX_MESSAGES, SUMMERIZE_BATCH)

def retrieve_user_details(memory_type):
    results = memory.retrieve_user_details(memory_type)
    return results
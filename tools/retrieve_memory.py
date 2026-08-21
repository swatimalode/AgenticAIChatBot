from memory.memory_manager import MemoryManager
from config import MAX_MESSAGES, SUMMERIZE_BATCH, THRESHOLD

memory = MemoryManager(MAX_MESSAGES, SUMMERIZE_BATCH)

def retrieve_memory(query, top_k=3):
    results = memory.retrieve(query)

    # print(results)
    relevant = [
        memory
        for memory in results[:top_k]
        if float(memory["score"]) >= THRESHOLD
    ]

    print(relevant)
    return relevant
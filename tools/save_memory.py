from memory.long_term_memory import LongTermMemory
from utils.embedding import create_embedding
from config import UPDATE_THRESHOLD

long_term_memory = LongTermMemory()


def save_memory(content, memory_type="fact"):

    results = long_term_memory.retrieve_conversation(content)

    if len(results) > 0 and results[0]['score'] >= UPDATE_THRESHOLD:
        long_term_memory.update_conversation(results[0], content)
    else:    
        embedding = create_embedding(content)

        memory = {
            "type": memory_type,
            "content": content,
            "embedding": embedding
        }

        long_term_memory.add_conversation(memory)

    return "Memory saved successfully."
from memory.long_term_memory import LongTermMemory
from utils.embedding import create_embedding
import uuid

long_term_memory = LongTermMemory()


def save_memory(content, memory_type="fact"):

    embedding = create_embedding(content)

    memory = {
        "id": str(uuid.uuid4()),
        "type": memory_type,
        "content": content,
        "embedding": embedding
    }

    long_term_memory.add_conversation(memory)

    return "Memory saved successfully."
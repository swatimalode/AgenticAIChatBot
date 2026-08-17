from memory.long_term_memory import LongTermMemory

long_term_memory = LongTermMemory()


def save_memory(content, memory_type="fact"):

    memory = {
        "type": memory_type,
        "content": content
    }

    long_term_memory.add(memory)

    return "Memory saved successfully."
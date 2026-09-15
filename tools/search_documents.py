from memory.memory_manager import MemoryManager
from config import MAX_MESSAGES, SUMMERIZE_BATCH
from utils.prompt import rag_prompt

memory = MemoryManager(MAX_MESSAGES, SUMMERIZE_BATCH)

def search_documents(query):
    results = memory.search_documnets(query)
    context = "\n\n".join(results['documents'][0])
    prompt = rag_prompt(context, query)
    return prompt
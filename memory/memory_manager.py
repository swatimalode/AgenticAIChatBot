from memory.short_term_memory import shortTermMemory
from memory.long_term_memory import LongTermMemory

class MemoryManager:

    def __init__(self,max_message, summerize_batch):
        self.short_term = shortTermMemory(max_message, summerize_batch)
        self.long_term = LongTermMemory()

    def add_short_term(self, message):
        self.short_term.add(message)

    def add_long_term(self, memory):
        self.long_term.add(memory)

    def get_short_term(self):
        return self.short_term.get_messages()

    def get_long_term(self):
        return self.long_term.get_all()

    def clear_short_term(self):
        self.short_term.clear_messages()

    def clear_long_term(self):
        self.long_term.clear()

    def retrieve_conversation(self, query, memory_type):
        return self.long_term.retrieve_conversation(query, memory_type)

    def retrieve_user_details(self, memory_type):
        return self.long_term.retrieve_user_details(memory_type)

    def update_user_details(self, memory_type, key, new_content):
        self.long_term.update_user_details(memory_type, key, new_content)

    def search_documnets(self, query):
        return self.long_term.search_documents(query)
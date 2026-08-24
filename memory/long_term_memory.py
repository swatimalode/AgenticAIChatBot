import json
from pathlib import Path
from config import MEMORY_PATH, USER_PATH
from utils.embedding import create_embedding
from utils.similarity import cosine_similarity
class LongTermMemory:

    def __init__(self):
        self.file_path = Path(MEMORY_PATH)
        self.user_path = Path(USER_PATH)
        self.memories = []
        self.user_details = []
        self._load()


    def _load(self):
        if not self.file_path.exists():
            self.memories = []
            return []

        if not self.user_path.exists():
            self.user_details = []
            return []
        
        with open(self.file_path, "r") as file:
            self.memories = json.load(file)

        with open(self.user_path, "r") as file:
            self.user_details = json.load(file)

    def _save_conversation(self):
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(self.file_path, "w") as file:
            json.dump(self.memories, file, indent=4)

    def _save_user_details(self):
        self.user_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(self.user_path, "w") as file:
            json.dump(self.user_details, file, indent=4)

    def add_user_details(self, memory):
        self.user_details.extend(memory)
        self._save_user_details()

    def add_conversation(self, memory):
        self.memories.append(memory)
        self._save_conversation()

    def get_all_conversation(self):
        return self.memories

    def get_all_user_details(self):
        return self.user_details

    def clear(self):
        self.memories = []
        self.user_details = []
        self._load()

    def retrieve_conversation(self, query):

        query_embedding = create_embedding(query)

        results = []

        for memory in self.memories:

            score = cosine_similarity(
                query_embedding,
                memory["embedding"]
            )

            results.append({
                "content": memory["content"],
                "score": score
            })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )
        return results

    def retrieve_user_details(self, memory_type):
        data = []
        for memory in self.user_details:
            if memory["memory_type"] == memory_type:
                data.append(memory)
        return data

    def update_conversation(self, old_memory, new_memory):
        print(old_memory, "-----------", new_memory)
        for memory in self.memories:
            if memory["content"] == old_memory["content"]:
                memory["content"] = new_memory
                memory["embedding"] = create_embedding(new_memory)

    def update_user_details(self, memory_type, key, new_content):
        for memory in self.user_details:
            if memory["memory_type"] == memory_type:
                if key in memory["details"]:
                    memory["details"][key] = new_content
                    self._save_user_details()

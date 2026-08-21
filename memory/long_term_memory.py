import json
from pathlib import Path
from config import MEMORY_PATH
from utils.embedding import create_embedding
from utils.similarity import cosine_similarity
class LongTermMemory:

    def __init__(self):
        self.file_path = Path(MEMORY_PATH)
        self.memories = []
        self._load()


    def _load(self):
        if not self.file_path.exists():
            self.memories = []
            return
        
        with open(self.file_path, "r") as file:
            self.memories = json.load(file)

    def _save(self):
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(self.file_path, "w") as file:
            json.dump(self.memories, file, indent=4)

    def add(self, memory):
        self.memories.append(memory)
        self._save()

    def get_all(self):
        return self.memories

    def clear(self):
        self.memories = []
        self._load()

    def search(self, query):
        results = []

        query_words = query.lower().split()

        for memory in self.memories:
            content_words = memory["content"].lower().split()

            score = 0

            for word in query_words:

                # Basic normalization
                if word.endswith("ing"):
                    word = word[:-3]
                elif word.endswith("ed"):
                    word = word[:-2]
                elif word.endswith("s"):
                    word = word[:-1]

                for content_word in content_words:

                    if content_word.startswith(word):
                        score += 1
                        break

            if score > 0:
                results.append({
                    "content": memory["content"],
                    "score": score
                })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results

    def retrieve(self, query, top_k=3):

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

    def update(self, old_memory, new_memory):
        print(old_memory, "-----------", new_memory)
        for memory in self.memories:
            if memory["content"] == old_memory["content"]:
                memory["content"] = new_memory
                memory["embedding"] = create_embedding(new_memory)
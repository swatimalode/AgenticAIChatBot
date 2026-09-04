import json
from pathlib import Path
from config import USER_PATH, THRESHOLD
from utils.embedding import create_embedding
from utils.vector_db import get_collection

class LongTermMemory:

    def __init__(self):
        # User details are still stored in JSON
        self.user_path = Path(USER_PATH)
        self.user_details = []
        # Conversation memories are stored in Chroma
        self.collection = get_collection("conversation_memory")
        self._load()

    def _load(self):
        if not self.user_path.exists():
            self.user_details = []
            return
        with open(self.user_path, "r") as file:
            self.user_details = json.load(file)

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

    def get_all_user_details(self):
        return self.user_details

    def retrieve_user_details(self, memory_type):
        data = []
        for memory in self.user_details:
            if memory["memory_type"] == memory_type:
                data.append(memory)
        return data

    def update_user_details(self, memory_type, key, new_content):
        for memory in self.user_details:
            if memory["memory_type"] == memory_type:
                if key in memory["details"]:
                    memory["details"][key] = new_content
                    self._save_user_details()
                    return True

        return False


    def add_conversation(self, memory):

        # Search only memories of the same type
        results = self.collection.query(
            query_embeddings=memory["embedding"],
            n_results=1,
            where={
                "type": memory["type"]
            }
        )
        id = memory["id"]
        if results["ids"] and results["ids"][0]:
            distance = results["distances"][0][0]

            if distance <= THRESHOLD:
                id = results["ids"][0][0]
                print("updatating existing memory")
            

        self.collection.upsert(
            ids=id,
            embeddings=[memory["embedding"]],
            documents=[memory["content"]],
            metadatas=[
                {
                    "type": memory["type"]
                }
            ]
        )

    def retrieve_conversation(self, query, memory_type, top_k=3):
        query_embedding = create_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={
                "type": memory_type
            }
        )
        return results

    def get_all_conversation(self):
        results = self.collection.get()
        return results

    def update_conversation(self, memory_id, new_content):
        new_embedding = create_embedding(
            new_content
        )
        self.collection.update(
            ids=[memory_id],
            embeddings=[new_embedding],
            documents=[new_content]
        )

    def delete_conversation(self, memory_id):
        self.collection.delete(
            ids=[memory_id]
        )

    def clear_conversation(self):
        # Delete the existing collection
        client = self.collection._client
        client.delete_collection(
            self.collection.name
        )
        # Create it again
        self.collection = client.get_or_create_collection(
            name="conversation_memory"
        )

    def clear_user_details(self):
        self.user_details = []
        self._save_user_details()
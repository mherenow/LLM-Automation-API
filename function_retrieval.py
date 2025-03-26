from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer

class FunctionRetrieval:
    def __init__(self):
        #Initialize the model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        #Initialize ChromaDB client
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name="automation-function")

        #Populate function metadata
        self._populate_function_registry()

    def _populate_function_registry(self):
        #Populate vector database
        functions = [
            {
                "name": "open_browser",
                "description": "Open the system default web browser",
                "category": "Application Control"
            },
            {
                "name": "open_calculator",
                "description": "Open the system calculator",
                "category": "Application Control"
            },
            {
                "name": "get_system_info",
                "description": "Get system resource usage information",
                "category": "System Information"
            },
            {
                "name": "run_shell_command",
                "description": "Execute a shell command",
                "category": "System Interaction"
            }
        ]

        for idx, func in enumerate(functions):
            embedding = self.model.encode(func['description']).tolist()
            self.collection.add(
                embeddings=embedding,
                metadatas=func,
                ids=[f"function_{idx}"]
            )

    def retrieve_function(self, query: str) -> Dict:
        #Retrieve the most similar function based on the query
        query_embedding = self.model.encode(query).tolist()
        results = self.collection.query(
            embeddings=query_embedding,
            n_results=1
        )

        return results['metadatas'][0][0]
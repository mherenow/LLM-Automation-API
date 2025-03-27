from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer
import logging

class FunctionRetrieval:
    def __init__(self):
        # Setup logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # Initialize the model
        self.logger.info("Initializing SentenceTransformer")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize ChromaDB client
        self.logger.info("Initializing ChromaDB")
        self.client = chromadb.Client()
        
        # Ensure collection doesn't already exist
        try:
            self.client.delete_collection("automation-function")
        except:
            pass
        
        self.collection = self.client.create_collection(name="automation-function")

        # Populate function metadata
        self._populate_function_registry()

    def _populate_function_registry(self):
        # Populate vector database
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
                "name": "open_gmail",
                "description": "Open Gmail in the default web browser",
                "category": "Application Control"
            },
            {
                "name": "get_system_info",
                "description": "Get system resource usage information",
                "category": "System Information"
            },
            {
                "name": "get_network_interfaces",
                "description": "Get network interface information",
                "category": "System Information"
            },
            {
                "name": "run_shell_command",
                "description": "Execute a shell command",
                "category": "System Interaction"
            }
        ]

        self.logger.info(f"Populating function registry with {len(functions)} functions")
        for idx, func in enumerate(functions):
            try:
                embedding = self.model.encode(func['description']).tolist()
                self.collection.add(
                    embeddings=[embedding],  # Wrap in a list
                    metadatas=[func],  # Wrap in a list
                    ids=[f"function_{idx}"]
                )
                self.logger.debug(f"Added function: {func['name']}")
            except Exception as e:
                self.logger.error(f"Error adding function {func['name']}: {e}")

    def retrieve_function(self, query: str) -> Dict:
        self.logger.info(f"Retrieving function for query: {query}")
        try:
            # Encode the query
            query_embedding = self.model.encode(query).tolist()
            
            # Perform similarity search
            results = self.collection.query(
                query_embeddings=[query_embedding],  # Wrap in a list
                n_results=1
            )
            
            # Log and return results
            if results['metadatas'] and results['metadatas'][0]:
                retrieved_function = results['metadatas'][0][0]
                self.logger.info(f"Retrieved function: {retrieved_function}")
                return retrieved_function
            else:
                self.logger.warning(f"No function found for query: {query}")
                raise ValueError(f"No matching function found for query: {query}")
        except Exception as e:
            self.logger.error(f"Error retrieving function: {e}")
            raise
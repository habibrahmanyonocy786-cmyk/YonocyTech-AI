import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional

class VectorMemory:
    """
    Vector memory using ChromaDB for persistent semantic storage.
    """
    def __init__(self, persist_directory: str = "memory/chroma_data"):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(allow_reset=True)
        )
        self.collection = self.client.get_or_create_collection(
            name="yonocytech_memory"
        )

    def add(self, text: str, metadata: Dict[str, Any], doc_id: str) -> str:
        """
        Adds a text entry with metadata to the vector store.
        """
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        return doc_id

    def search(self, query: str, n_results: int = 5, where_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Searches for the most relevant documents.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )

        formatted_results = []
        if results["documents"]:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if results["distances"] else None
                })
        return formatted_results

    def get_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a document by its unique ID.
        """
        res = self.collection.get(ids=[doc_id])
        if res["ids"]:
            return {
                "text": res["documents"][0] if res["documents"] else "",
                "metadata": res["metadatas"][0] if res["metadatas"] else {}
            }
        return None

    def delete(self, doc_id: str) -> None:
        """
        Deletes a document by its ID.
        """
        self.collection.delete(ids=[doc_id])

    def count(self) -> int:
        """
        Returns the total number of documents in the collection.
        """
        return self.collection.count()

    def clear_all(self) -> None:
        """
        Wipes the entire collection.
        """
        self.collection.delete()

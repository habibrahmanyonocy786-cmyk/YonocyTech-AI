from typing import List, Dict, Any, Optional
from memory.vector_store import VectorMemory
from core import MemoryStore, SessionMessage

class SemanticRecall:
    """
    Combines VectorMemory and MemoryStore to provide semantic context recall.
    """
    def __init__(self, vector_store: VectorMemory, json_store: MemoryStore):
        self.vector_store = vector_store
        self.json_store = json_store

    def store_conversation_pair(self, user_msg: str, assistant_msg: str, session_id: str, focus: Optional[str] = None) -> None:
        """
        Stores a Q&A pair in the vector store for future retrieval.
        """
        doc_id = f"pair_{session_id}_{int(hash(user_msg + assistant_msg))}"
        text = f"User: {user_msg}\nAssistant: {assistant_msg}"
        metadata = {
            "session_id": session_id,
            "focus": focus or "general",
            "type": "conversation_pair"
        }
        self.vector_store.add(text, metadata, doc_id)

    def find_relevant_context(self, query: str, session_id: Optional[str] = None, n_results: int = 3) -> str:
        """
        Searches for relevant context based on a query.
        """
        where_filter = None
        if session_id:
            where_filter = {"session_id": session_id}

        results = self.vector_store.search(query, n_results=n_results, where_filter=where_filter)

        if not results:
            return ""

        context_blocks = [f"Relevant Memory: {r['text']}" for r in results]
        return "\n\n".join(context_blocks)

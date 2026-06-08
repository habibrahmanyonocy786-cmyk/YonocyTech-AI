import os
import time
from typing import List, Dict, Optional

import httpx

from core import AgentResponse


class OllamaProvider:
    """
    Integration with local Ollama for Persian AI models.
    Default model: mshojaei77/gemma3persian (Persian-optimized Gemma 3)
    """
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "mshojaei77/gemma3persian")
        self.chat_url = f"{self.base_url}/api/chat"

    @property
    def is_available(self) -> bool:
        try:
            import streamlit as st
            if st.session_state.get("ollama_checked", False):
                return st.session_state.get("ollama_available", False)
            response = httpx.get(f"{self.base_url}/api/tags", timeout=2.0)
            available = response.status_code == 200
            st.session_state["ollama_checked"] = True
            st.session_state["ollama_available"] = available
            return available
        except Exception:
            return False

    async def ask(self, messages: List[Dict[str, str]], max_tokens: int = 2048) -> AgentResponse:
        start_time = time.time()

        body = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7,
            }
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(self.chat_url, json=body)
            response.raise_for_status()
            data = response.json()

        latency = (time.time() - start_time) * 1000

        return AgentResponse(
            text=data["message"]["content"],
            model=self.model,
            provider="Ollama",
            latency_ms=latency,
        )

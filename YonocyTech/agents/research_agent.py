from typing import Optional, List
from agents.base_agent import BaseAgent
from core import AgentResponse
from tools.web_search import search_web

class ResearchAgent(BaseAgent):
    """
    Specialized agent for deep research and evidence-based synthesis.
    """
    @property
    def focus(self) -> str:
        return "research"

    @property
    def description(self) -> str:
        return "Research analyst for deep-diving into topics with citations."

    async def research(self, topic: str, session_id: Optional[str] = None) -> AgentResponse:
        """
        Performs a web search and synthesizes the results with citations.
        """
        # 1. Search the web
        search_results = await search_web(topic)

        # 2. Build context
        context = "Search results for this topic:\n"
        for i, res in enumerate(search_results, 1):
            context += f"[{i}] {res['title']}: {res['snippet']} (URL: {res['url']})\n"

        # 3. Prompt for synthesis
        prompt = (
            f"Research Topic: {topic}\n\n{context}\n\n"
            "Synthesize a comprehensive report based on the provided evidence. "
            "Use citations in the format [1], [2] corresponding to the search results."
        )

        return await super().run(prompt, session_id=session_id)

    async def run(self, prompt: str, session_id: Optional[str] = None, **kwargs) -> AgentResponse:
        return await super().run(prompt, session_id=session_id)

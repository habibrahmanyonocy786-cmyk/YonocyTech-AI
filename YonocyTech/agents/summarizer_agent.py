from typing import Optional
from agents.base_agent import BaseAgent
from core import AgentResponse


class SummarizerAgent(BaseAgent):
    """
    Specialized agent for intelligent text summarization.
    """
    @property
    def focus(self) -> str:
        return "summarizer"

    @property
    def description(self) -> str:
        return "Intelligent text summarization in 3 modes: short, medium, detailed."

    async def run(
        self,
        prompt: str,
        session_id: Optional[str] = None,
        mode: str = "medium",
        **kwargs
    ) -> AgentResponse:
        mode_instructions = {
            "short": "Summarize the following text in exactly 3 sentences. Be concise and capture only the most essential points.",
            "medium": "Summarize the following text in one paragraph. Cover the main ideas and key supporting details.",
            "detailed": "Summarize the following text in detail with bullet points. Include:\n- Main idea\n- Key points\n- Important details\n- Conclusions or takeaways",
        }
        instruction = mode_instructions.get(mode, mode_instructions["medium"])
        enhanced_prompt = f"{instruction}\n\nText to summarize:\n{prompt}"
        return await self.core.ask(enhanced_prompt, focus=self.focus, session_id=session_id)

from typing import Optional
from agents.base_agent import BaseAgent
from core import AgentResponse

class WritingAgent(BaseAgent):
    """
    Specialized agent for high-quality professional and creative writing.
    """
    @property
    def focus(self) -> str:
        return "writing"

    @property
    def description(self) -> str:
        return "Professional writer for articles, emails, and creative content."

    async def run(self, prompt: str, session_id: Optional[str] = None, language: str = "auto", tone: str = "professional", **kwargs) -> AgentResponse:
        """
        Enhances the prompt with style and tone instructions before asking the core.
        """
        enhanced_prompt = f"Write this in {language} language with a {tone} tone:\n\n{prompt}"
        return await super().run(enhanced_prompt, session_id=session_id)

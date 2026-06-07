from typing import Optional
from agents.base_agent import BaseAgent
from core import AgentResponse

class MarketingAgent(BaseAgent):
    """
    Specialized agent for SEO, Growth Hacking, and Digital Marketing.
    """
    @property
    def focus(self) -> str:
        return "marketing"

    @property
    def description(self) -> str:
        return "Marketing expert for SEO, KPI tracking, and growth strategies."

    async def run(self, prompt: str, session_id: Optional[str] = None, **kwargs) -> AgentResponse:
        """
        Enhances the prompt for SEO and KPI focus.
        """
        enhanced_prompt = (
            f"As a marketing expert, optimize the following request for maximum impact, "
            f"considering SEO, conversion rates, and KPI tracking:\n\n{prompt}"
        )
        return await super().run(enhanced_prompt, session_id=session_id)

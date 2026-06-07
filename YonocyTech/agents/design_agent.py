from typing import Optional
from agents.base_agent import BaseAgent
from core import AgentResponse

class DesignAgent(BaseAgent):
    """
    Specialized agent for UI/UX and visual design specifications.
    """
    @property
    def focus(self) -> str:
        return "design"

    @property
    def description(self) -> str:
        return "UI/UX expert for generating color palettes, layouts, and design specs."

    async def generate_ui_spec(self, description: str, session_id: Optional[str] = None) -> AgentResponse:
        """
        Generates a detailed UI specification based on a product description.
        """
        prompt = (
            f"Generate a complete UI specification for the following: {description}\n\n"
            "Include: \n1. Color Palette (Hex codes)\n2. Typography (Fonts, sizes)\n"
            "3. Layout structure\n4. Accessibility guidelines\n5. Responsive breakpoints."
        )
        return await super().run(prompt, session_id=session_id)

    async def run(self, prompt: str, session_id: Optional[str] = None, **kwargs) -> AgentResponse:
        return await super().run(prompt, session_id=session_id)

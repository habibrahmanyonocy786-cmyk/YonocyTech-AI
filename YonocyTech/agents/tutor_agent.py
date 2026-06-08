from typing import Optional
from agents.base_agent import BaseAgent
from core import AgentResponse


class TutorAgent(BaseAgent):
    """
    Specialized agent for programming education and code tutoring.
    """
    @property
    def focus(self) -> str:
        return "tutor"

    @property
    def description(self) -> str:
        return "Programming tutor: explain code, teach concepts, provide challenges."

    async def run(
        self,
        prompt: str,
        session_id: Optional[str] = None,
        mode: str = "teach",
        **kwargs
    ) -> AgentResponse:
        mode_instructions = {
            "explain": (
                "You are a patient programming tutor. Explain the following code line by line. "
                "For each line or block, describe what it does, why it's written that way, "
                "and any important concepts involved. Use simple language suitable for beginners."
            ),
            "teach": (
                "You are a friendly programming tutor. Teach the following concept step by step. "
                "Start with a simple explanation, then provide a code example, "
                "and finally suggest a small exercise for practice. "
                "Assume the learner is curious but may be new to this topic."
            ),
            "challenge": (
                "You are a coding challenge creator. Based on the following topic or request, "
                "create a programming challenge that tests understanding. "
                "Include:\n- Challenge description\n- Requirements\n- Example input/output\n- Hints (optional)\n"
                "Do NOT provide the solution unless asked."
            ),
        }
        instruction = mode_instructions.get(mode, mode_instructions["teach"])
        enhanced_prompt = f"{instruction}\n\n{prompt}"
        return await self.core.ask(enhanced_prompt, focus=self.focus, session_id=session_id)

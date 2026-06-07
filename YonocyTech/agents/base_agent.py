from abc import ABC, abstractmethod
from typing import Optional
from core import YonocyTech, AgentResponse

class BaseAgent(ABC):
    """
    Abstract Base Class for all specialized agents.
    """
    def __init__(self, core: YonocyTech):
        self.core = core

    @property
    @abstractmethod
    def focus(self) -> str:
        """The focus area of the agent (e.g., 'coding')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A short description of what the agent does."""
        pass

    async def run(self, prompt: str, session_id: Optional[str] = None, **kwargs) -> AgentResponse:
        """
        Standard execution flow for the agent. Can be overridden by specialists.
        """
        return await self.core.ask(prompt, focus=self.focus, session_id=session_id)

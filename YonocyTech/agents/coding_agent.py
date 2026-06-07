import re
from typing import Optional, List, Tuple
from agents.base_agent import BaseAgent
from core import AgentResponse

class CodingAgent(BaseAgent):
    """
    Specialized agent for software engineering and code generation.
    """
    @property
    def focus(self) -> str:
        return "coding"

    @property
    def description(self) -> str:
        return "Expert software engineer for writing, debugging, and optimizing code."

    def extract_code_blocks(self, text: str) -> List[Tuple[str, str]]:
        """
        Extracts code blocks from LLM response.
        Returns a list of (language, code) tuples.
        """
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        return [(m[0] or "python", m[1]) for m in matches]

    async def run(self, prompt: str, session_id: Optional[str] = None, execute: bool = False, **kwargs) -> AgentResponse:
        """
        Executes the coding task. If execute=True, it attempts to run the Python code in a sandbox.
        """
        response = await super().run(prompt, session_id=session_id)

        if execute:
            blocks = self.extract_code_blocks(response.text)
            for lang, code in blocks:
                if lang == "python":
                    from security.guard import execute_in_sandbox
                    res = execute_in_sandbox(code)
                    if res["success"]:
                        response.text += f"\n\n--- Execution Output ---\n{res['stdout']}"
                    else:
                        response.text += f"\n\n--- Execution Error ---\n{res['stderr']}"

        return response

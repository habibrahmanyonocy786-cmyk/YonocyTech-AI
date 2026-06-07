import asyncio
from typing import List, Dict, Any, Optional
from core import YonocyTech, AgentResponse
from agents.base_agent import BaseAgent

class Orchestrator:
    """
    Orchestrates multi-agent workflows and handles context passing.
    """
    def __init__(self, core: YonocyTech, agents: Dict[str, BaseAgent]):
        self.core = core
        self.agents = agents

    def list_agents(self) -> List[str]:
        """
        Returns a list of all available specialized agents.
        """
        return list(self.agents.keys())

    async def single(self, agent_name: str, prompt: str, session_id: Optional[str] = None) -> AgentResponse:
        """
        Runs a single specialized agent for a specific prompt.
        """
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found.")

        return await agent.run(prompt, session_id=session_id)

    async def chain(self, tasks: List[Dict[str, Any]], session_id: Optional[str] = None) -> List[AgentResponse]:
        """
        Executes a sequence of tasks across different agents, passing context between them.

        tasks: List of {"agent": "coding", "prompt": "..."}
        """
        results = []
        current_context = ""

        for i, task in enumerate(tasks):
            agent_name = task["agent"]
            prompt = task["prompt"]

            # If not the first task, append previous results as context
            if i > 0 and current_context:
                enhanced_prompt = f"Based on the previous result: {current_context}\n\nTask: {prompt}"
            else:
                enhanced_prompt = prompt

            response = await self.single(agent_name, enhanced_prompt, session_id=session_id)
            results.append(response)
            current_context = response.text

        return results

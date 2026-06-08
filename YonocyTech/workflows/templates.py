from typing import List, Dict, Any, Optional

import streamlit as st

from core import AgentResponse


WORKFLOW_TEMPLATES = {
    "content_pipeline": {
        "name": "content_pipeline",
        "icon": "📝",
        "agents": ["research", "writing", "design"],
        "prompts": [
            "Research the latest trends and best practices for this topic",
            "Write a comprehensive article based on the research findings",
            "Create a visual design concept that complements the article",
        ],
    },
    "app_builder": {
        "name": "app_builder",
        "icon": "💻",
        "agents": ["research", "coding", "design"],
        "prompts": [
            "Research the best technical approach and architecture",
            "Implement the core functionality with clean code",
            "Design a clean and modern user interface",
        ],
    },
    "market_report": {
        "name": "market_report",
        "icon": "📊",
        "agents": ["research", "data", "writing"],
        "prompts": [
            "Research the market landscape and competitors",
            "Analyze data trends and extract key insights",
            "Write a professional market analysis report",
        ],
    },
    "campaign_kit": {
        "name": "campaign_kit",
        "icon": "🎯",
        "agents": ["research", "marketing", "design"],
        "prompts": [
            "Research target audience and market opportunities",
            "Create a comprehensive marketing strategy",
            "Design promotional materials and landing page concepts",
        ],
    },
}


class WorkflowTemplates:
    @staticmethod
    def get_all() -> Dict[str, Any]:
        return WORKFLOW_TEMPLATES

    @staticmethod
    def get(name: str) -> Optional[Dict[str, Any]]:
        return WORKFLOW_TEMPLATES.get(name)


class WorkflowExecutor:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    async def execute(
        self,
        workflow_name: str,
        topic: str,
        session_id: Optional[str] = None,
    ) -> List[AgentResponse]:
        template = WorkflowTemplates.get(workflow_name)
        if not template:
            raise ValueError(f"Workflow '{workflow_name}' not found")

        tasks = []
        for agent_name, prompt in zip(template["agents"], template["prompts"]):
            enriched = f"{prompt}: {topic}" if topic else prompt
            tasks.append({"agent": agent_name, "prompt": enriched})

        return await self.orchestrator.chain(tasks, session_id=session_id)

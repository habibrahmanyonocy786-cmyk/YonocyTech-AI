import pandas as pd
from typing import Optional
from agents.base_agent import BaseAgent
from core import AgentResponse
from tools.file_processor import FileProcessor

class DataAgent(BaseAgent):
    """
    Specialized agent for data analysis, CSV processing and visualization.
    """
    @property
    def focus(self) -> str:
        return "data"

    @property
    def description(self) -> str:
        return "Data scientist for analyzing datasets and extracting insights."

    async def analyze_csv(self, filepath: str, question: str, session_id: Optional[str] = None) -> AgentResponse:
        """
        Reads a CSV and generates a summary for the core engine to analyze.
        """
        content = FileProcessor.read_csv(filepath)
        if content is None or "Error" in content:
            return AgentResponse(text=f"Error processing CSV: {content}", model="N/A", provider="Local")

        # Create a data summary to fit in context
        df = pd.read_csv(filepath)
        summary = f"Dataset Info:\n{df.info()}\n\nColumns: {df.columns.tolist()}\n\nSample Data:\n{df.head().to_string()}\n\nQuestion: {question}"

        return await super().run(summary, session_id=session_id)

    async def run(self, prompt: str, session_id: Optional[str] = None, **kwargs) -> AgentResponse:
        return await super().run(prompt, session_id=session_id)

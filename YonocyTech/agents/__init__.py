from agents.coding_agent import CodingAgent
from agents.writing_agent import WritingAgent
from agents.data_agent import DataAgent
from agents.design_agent import DesignAgent
from agents.marketing_agent import MarketingAgent
from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.tutor_agent import TutorAgent

ALL_AGENTS = {
    "coding": CodingAgent,
    "writing": WritingAgent,
    "data": DataAgent,
    "design": DesignAgent,
    "marketing": MarketingAgent,
    "research": ResearchAgent,
    "summarizer": SummarizerAgent,
    "tutor": TutorAgent,
}

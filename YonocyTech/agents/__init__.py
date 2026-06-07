from agents.coding_agent import CodingAgent
from agents.writing_agent import WritingAgent
from agents.data_agent import DataAgent
from agents.design_agent import DesignAgent
from agents.marketing_agent import MarketingAgent
from agents.research_agent import ResearchAgent

# Dictionary mapping focus area to agent class
ALL_AGENTS = {
    "coding": CodingAgent,
    "writing": WritingAgent,
    "data": DataAgent,
    "design": DesignAgent,
    "marketing": MarketingAgent,
    "research": ResearchAgent,
}

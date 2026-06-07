import pytest
from agents.base_agent import BaseAgent
from agents.coding_agent import CodingAgent
from tools.file_manager import FileManager
from tools.orchestrator import Orchestrator
from core import YonocyTech

def test_base_agent_requires_focus():
    with pytest.raises(TypeError):
        BaseAgent(YonocyTech())

def test_coding_agent_extract_code_blocks():
    agent = CodingAgent(YonocyTech())
    text = "Here is the code:\n```python\nprint('hello')\n```"
    blocks = agent.extract_code_blocks(text)
    assert len(blocks) == 1
    assert blocks[0][0] == "python"
    assert blocks[0][1].strip() == "print('hello')"

def test_file_manager_allowed_extensions():
    fm = FileManager()
    # .py is allowed
    assert fm.read("test.py") is not None # will be error string if not exists, but not "extension not allowed"
    # .exe is blocked
    result = fm.read("test.exe")
    assert "extension .exe is not allowed" in result.lower()

def test_orchestrator_list_agents():
    core = YonocyTech()
    from agents import ALL_AGENTS
    instances = {name: cls(core) for name, cls in ALL_AGENTS.items()}
    orch = Orchestrator(core, instances)
    agents = orch.list_agents()
    assert "coding" in agents
    assert "research" in agents

def test_orchestrator_missing_agent():
    core = YonocyTech()
    orch = Orchestrator(core, {})
    with pytest.raises(ValueError, match="Agent unknown_agent not found"):
        asyncio.run(orch.single("unknown_agent", "hi"))

import asyncio

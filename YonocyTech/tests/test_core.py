import pytest
import asyncio
from dataclasses import is_dataclass
from core import AgentResponse, SessionMessage, MemoryStore, YonocyTech

def test_agent_response_creation():
    resp = AgentResponse(text="Hello", model="gpt-4o", provider="GitHub")
    assert resp.text == "Hello"
    assert resp.provider == "GitHub"

def test_session_message_creation():
    msg = SessionMessage(role="user", content="Hi")
    assert msg.role == "user"
    assert msg.content == "Hi"

def test_memory_store_new_session():
    store = MemoryStore(data_dir="tests/temp_mem")
    sid = store.new_session()
    assert len(sid) == 12
    assert sid in store.sessions

def test_memory_store_add_message():
    store = MemoryStore(data_dir="tests/temp_mem")
    sid = store.new_session()
    store.add_message(sid, "user", "test msg")
    assert len(store.get_history(sid)) == 1

def test_memory_store_history_limit():
    store = MemoryStore(data_dir="tests/temp_mem")
    sid = store.new_session()
    for i in range(30):
        store.add_message(sid, "user", f"msg {i}")

    # MemoryStore crops to 50, but get_history limit is 20 by default
    history = store.get_history(sid, limit=20)
    assert len(history) == 20

def test_yonocytech_init():
    agent = YonocyTech()
    assert agent.name == "YonocyTech"
    assert agent.version == "2.0"

def test_yonocytech_focus_areas():
    agent = YonocyTech()
    assert "coding" in agent.FOCUS_AREAS
    assert "research" in agent.FOCUS_AREAS

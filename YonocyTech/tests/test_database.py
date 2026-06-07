import os, sys, tempfile, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import database
from database import get_connection
from database.schema import migrate
from database.models import (
    create_user, authenticate, get_user_by_email, get_user_by_id,
    get_all_users, count_users, update_user_plan,
    create_session, ensure_session, add_message, get_session_messages, get_user_sessions,
    get_all_providers, get_active_providers, update_provider_status,
    get_all_agents, get_active_agents, update_agent_status,
    save_contact_message, get_contact_messages,
    log_usage, get_usage_stats,
    set_setting, get_setting, get_all_settings,
)


@pytest.fixture(autouse=True)
def clean_db():
    tmp_dir = tempfile.mkdtemp()
    old_path = os.environ.get("YONOCYTECH_DB_PATH")
    os.environ["YONOCYTECH_DB_PATH"] = os.path.join(tmp_dir, "test.db")
    migrate()
    yield
    if old_path:
        os.environ["YONOCYTECH_DB_PATH"] = old_path
    else:
        os.environ.pop("YONOCYTECH_DB_PATH", None)
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_migrate():
    migrate()
    conn = get_connection()
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    conn.close()
    names = [r["name"] for r in tables]
    assert "users" in names
    assert "sessions" in names
    assert "messages" in names
    assert "providers" in names
    assert "agents" in names
    assert "contact_messages" in names
    assert "usage_logs" in names
    assert "settings" in names


def test_seed_providers():
    migrate()
    provs = get_all_providers()
    ids = [p["id"] for p in provs]
    assert "openrouter" in ids
    assert "huggingface" in ids
    assert "github-models" in ids
    assert "deepai" in ids


def test_seed_agents():
    migrate()
    agents = get_all_agents()
    ids = [a["id"] for a in agents]
    assert "coding" in ids
    assert "writing" in ids
    assert "data" in ids
    assert "design" in ids
    assert "marketing" in ids
    assert "research" in ids


def test_first_user_is_admin():
    u = create_user("Alice", "alice@test.com", "secret123")
    assert u is not None
    assert u["name"] == "Alice"
    assert u["role"] == "admin"


def test_second_user_is_user():
    create_user("Admin1", "admin1@test.com", "pass")
    u = create_user("Regular", "regular@test.com", "pass")
    assert u is not None
    assert u["role"] == "user"





def test_duplicate_email():
    migrate()
    create_user("A", "dup@test.com", "pass1")
    u2 = create_user("B", "dup@test.com", "pass2")
    assert u2 is None


def test_authenticate_ok():
    migrate()
    create_user("Bob", "bob@test.com", "pass123")
    u = authenticate("bob@test.com", "pass123")
    assert u is not None
    assert u["name"] == "Bob"


def test_authenticate_wrong_password():
    migrate()
    create_user("Eve", "eve@test.com", "goodpass")
    u = authenticate("eve@test.com", "wrongpass")
    assert u is None


def test_authenticate_unknown_user():
    migrate()
    u = authenticate("nobody@test.com", "pass")
    assert u is None


def test_get_user_by_email():
    migrate()
    create_user("FindMe", "find@test.com", "pass")
    u = get_user_by_email("find@test.com")
    assert u is not None
    assert u["name"] == "FindMe"


def test_get_user_by_id():
    migrate()
    created = create_user("ById", "byid@test.com", "pass")
    u = get_user_by_id(created["id"])
    assert u is not None
    assert u["email"] == "byid@test.com"


def test_count_users():
    migrate()
    before = count_users()
    create_user("Counter", "count@test.com", "pass")
    assert count_users() == before + 1


def test_get_all_users():
    create_user("ListMe", "list@test.com", "pass")
    users = get_all_users()
    assert len(users) == 1
    assert users[0]["email"] == "list@test.com"


def test_update_user_plan():
    migrate()
    u = create_user("Plan", "plan@test.com", "pass")
    assert update_user_plan(u["id"], "pro") is True
    updated = get_user_by_id(u["id"])
    assert updated["plan"] == "pro"


def test_create_session():
    migrate()
    u = create_user("SessionUser", "session@test.com", "pass")
    sid = create_session(u["id"], "My Session")
    assert len(sid) == 12
    assert isinstance(sid, str)


def test_create_session_with_custom_id():
    migrate()
    u = create_user("CustomSID", "custom@test.com", "pass")
    sid = create_session(u["id"], session_id="my_custom_id")
    assert sid == "my_custom_id"


def test_ensure_session_creates_if_missing():
    migrate()
    u = create_user("Ensure", "ensure@test.com", "pass")
    ensure_session("ghost_session", user_id=u["id"])
    sessions = get_user_sessions(u["id"])
    ids = [s["id"] for s in sessions]
    assert "ghost_session" in ids


def test_add_and_get_messages():
    migrate()
    u = create_user("MsgUser", "msg@test.com", "pass")
    sid = create_session(u["id"])
    add_message(sid, "user", "Hello!", user_id=u["id"])
    add_message(sid, "assistant", "Hi there!", tokens=42, user_id=u["id"])

    msgs = get_session_messages(sid)
    assert len(msgs) == 2
    assert msgs[0]["role"] == "user"
    assert msgs[0]["content"] == "Hello!"
    assert msgs[1]["role"] == "assistant"
    assert msgs[1]["tokens_used"] == 42


def test_get_user_sessions():
    migrate()
    u = create_user("SessList", "slist@test.com", "pass")
    s1 = create_session(u["id"], "First")
    s2 = create_session(u["id"], "Second")
    sessions = get_user_sessions(u["id"])
    ids = [s["id"] for s in sessions]
    assert s1 in ids
    assert s2 in ids


def test_provider_status():
    migrate()
    assert update_provider_status("openrouter", "limited") is True
    active = get_active_providers()
    active_ids = [p["id"] for p in active]
    assert "openrouter" not in active_ids


def test_agent_status():
    migrate()
    assert update_agent_status("coding", "inactive") is True
    active = get_active_agents()
    active_ids = [a["id"] for a in active]
    assert "coding" not in active_ids


def test_contact_message():
    migrate()
    assert save_contact_message("Tester", "t@t.com", "Test", "Hello!") is True
    msgs = get_contact_messages()
    assert len(msgs) >= 1
    assert msgs[-1]["name"] == "Tester"


def test_usage_log_and_stats():
    migrate()
    u = create_user("Usage", "usage@test.com", "pass")
    log_usage(u["id"], "openrouter", "coding", tokens=100, latency=500.0)
    stats = get_usage_stats()
    assert stats["total_requests"] >= 1
    assert stats["total_tokens"] >= 100


def test_settings():
    migrate()
    assert set_setting("test_key", "test_value") is True
    assert get_setting("test_key") == "test_value"
    all_s = get_all_settings()
    assert "test_key" in all_s

"""
YonocyTech AI — Streamlit App v2.0
3-column professional shell: Sidebar · Main Chat · Aside panels.
"""
import sys
import os

# Fix imports: add parent directory to path so YonocyTech/ modules resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import asyncio

# Load API keys from Streamlit secrets (Streamlit Cloud) into env
try:
    for _key in ["OPENROUTER_API_KEY", "HF_API_KEY", "GITHUB_TOKEN", "DEEPAI_API_KEY"]:
        if _key in st.secrets:
            os.environ[_key] = st.secrets[_key]
except Exception:
    pass  # No secrets file; API keys should be in .env or env vars

from core import YonocyTech, register_user, login_user, get_db_providers, get_db_agents
from agents import ALL_AGENTS
from tools.file_manager import FileManager
from tools.orchestrator import Orchestrator
from database.models import (
    get_all_providers, update_provider_status, update_provider_rate_limit,
    get_all_agents, update_agent_status, update_agent_provider,
    get_all_users, get_usage_stats, get_all_settings, set_setting,
    get_contact_messages, save_contact_message, count_users
)
from ui.components import (
    apply_theme,
    render_brand,
    render_header,
    render_session_card,
    render_welcome,
    render_quick_starts,
    render_msg_bubble,
    render_typing,
    render_response_metadata,
    render_aside_provider,
    render_aside_chain,
    render_aside_memory,
    render_aside_stats,
    render_agent_badge,
)

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="YonocyTech AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()


# ----------------------------------------------------------------------------
# AUTH STATE
# ----------------------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if "show_login" not in st.session_state:
    st.session_state.show_login = True

# Login / Register page
if not st.session_state.logged_in:
    st.markdown("""
        <div style="display:flex; align-items:center; justify-content:center; min-height:100vh; padding:24px;">
            <div style="background:rgba(28,28,65,0.65); border:1px solid rgba(108,99,255,0.18);
                        border-radius:20px; padding:48px 40px; max-width:420px; width:100%;
                        backdrop-filter:blur(20px); box-shadow:0 0 0 1px rgba(108,99,255,0.25);">
                <div style="text-align:center; margin-bottom:32px;">
                    <div style="width:52px; height:52px; margin:0 auto 12px; border-radius:14px;
                                background:linear-gradient(135deg,#6C63FF,#00D9FF,#FF4FCB);
                                display:grid; place-items:center; font-size:24px;
                                box-shadow:0 8px 24px rgba(108,99,255,0.4);">Y</div>
                    <h2 style="font-size:22px; font-weight:700;">Welcome to YonocyTech</h2>
                    <p style="font-size:14px; color:#A5A5C7;">Sign in to access AI agents</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab = st.tabs(["Sign In", "Create Account"])
    with tab[0]:
        with st.form("login_form"):
            l_email = st.text_input("Email", placeholder="your@email.com")
            l_pass = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In", use_container_width=True):
                user = login_user(l_email, l_pass)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.show_login = False
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
    with tab[1]:
        with st.form("register_form"):
            r_name = st.text_input("Full Name", placeholder="Habib Rahman")
            r_email = st.text_input("Email", placeholder="your@email.com")
            r_pass = st.text_input("Password", type="password")
            r_confirm = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Create Account", use_container_width=True):
                if r_pass != r_confirm:
                    st.error("Passwords do not match.")
                elif len(r_pass) < 4:
                    st.error("Password must be at least 4 characters.")
                else:
                    user = register_user(r_name, r_email, r_pass)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.show_login = False
                        st.success("Account created! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Email already exists or registration failed.")
    st.stop()


# ----------------------------------------------------------------------------
# STATE (Authenticated)
# ----------------------------------------------------------------------------
if "agent" not in st.session_state:
    user_id = st.session_state.user.get("id")
    st.session_state.agent = YonocyTech(user_id=user_id)
    st.session_state.fm = FileManager()
    agents_instances = {name: cls(st.session_state.agent) for name, cls in ALL_AGENTS.items()}
    st.session_state.orchestrator = Orchestrator(st.session_state.agent, agents_instances)
    st.session_state.messages = []
    st.session_state.current_session_id = st.session_state.agent.memory.new_session()
    st.session_state.current_page = "Chat"
    st.session_state.active_agent = "general"
    st.session_state.chain_tasks = []


# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    render_brand()

    # User info
    user = st.session_state.user
    initials = "".join([p[0] for p in user["name"].split()[:2]]).upper() or "U"
    plan_badge = {"free": "🔹 Free", "pro": "💎 Pro", "enterprise": "🏢 Enterprise"}.get(user.get("plan", "free"), "🔹 Free")
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:10px; padding:10px 8px; margin-bottom:8px;
                    background:rgba(20,20,50,0.55); border:1px solid rgba(108,99,255,0.18);
                    border-radius:14px;">
            <div style="width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg,#6C63FF,#00D9FF,#FF4FCB);
                        display:grid; place-items:center; font-weight:700; color:#fff; font-size:13px;">
                {initials}
            </div>
            <div>
                <div style="font-size:13px; font-weight:600;">{user["name"]}</div>
                <div style="font-size:11px; color:#A5A5C7;">{plan_badge} · {user.get("role","user").title()}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h4 style='font-size:11px; text-transform:uppercase; letter-spacing:1.2px; "
        "color:var(--text-mute); margin:14px 8px 8px; font-weight:600;'>Workspace</h4>",
        unsafe_allow_html=True,
    )
    nav_pages = [("Chat", "💬"), ("Agent Chain", "⛓️"), ("Files", "📁"), ("Memory", "🧠")]
    if user.get("role") == "admin":
        nav_pages.append(("Admin Panel", "🔐"))
    for page, icon in nav_pages:
        active = st.session_state.current_page == page
        label = f"{icon}  {page}"
        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.current_page = page
            st.rerun()

    st.markdown(
        "<h4 style='font-size:11px; text-transform:uppercase; letter-spacing:1.2px; "
        "color:var(--text-mute); margin:14px 8px 8px; font-weight:600;'>Specialized Agents</h4>",
        unsafe_allow_html=True,
    )
    for name in ALL_AGENTS.keys():
        meta = {
            "coding": "💻", "writing": "✍️", "data": "📊",
            "design": "🎨", "marketing": "📈", "research": "🔍",
        }.get(name.lower(), "🤖")
        if st.button(f"{meta}  {name.title()}", key=f"agent_btn_{name}", use_container_width=True):
            st.session_state.active_agent = name.lower()
            st.session_state.current_page = "Chat"
            st.rerun()

    st.markdown(
        "<h4 style='font-size:11px; text-transform:uppercase; letter-spacing:1.2px; "
        "color:var(--text-mute); margin:14px 8px 8px; font-weight:600;'>Sessions</h4>",
        unsafe_allow_html=True,
    )
    sessions = st.session_state.agent.memory.list_sessions()
    session_ids = [st.session_state.current_session_id] + [s["id"] for s in sessions]
    selected_sid = st.selectbox("Switch session", session_ids, label_visibility="collapsed")
    if selected_sid != st.session_state.current_session_id:
        st.session_state.current_session_id = selected_sid
        st.session_state.messages = []
        st.rerun()

    render_session_card()

    if st.button("🚪  Sign Out", key="signout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.agent = None
        st.rerun()


# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
agent_label = st.session_state.active_agent.title() if st.session_state.active_agent != "general" else "General Assistant"
render_header(active_page=st.session_state.current_page, agent_label=agent_label, online=True)


# ----------------------------------------------------------------------------
# MAIN + ASIDE
# ----------------------------------------------------------------------------
main_col, aside_col = st.columns([3, 1], gap="medium")

with main_col:
    if st.session_state.current_page == "Chat":
        # Welcome when no messages
        if not st.session_state.messages:
            render_welcome()
            render_quick_starts([
                {"icon": "💡", "title": "Brainstorm", "desc": "Generate 10 SaaS landing page concepts"},
                {"icon": "🧪", "title": "Explain code", "desc": "Walk me through this Python script"},
                {"icon": "📊", "title": "Analyze data", "desc": "Summarize trends from this CSV"},
                {"icon": "✍️", "title": "Write content", "desc": "Draft a launch announcement"},
            ])

        # Chat history
        for msg in st.session_state.messages:
            meta = msg.get("meta")
            render_msg_bubble(
                role=msg["role"],
                name="Habib Rahman" if msg["role"] == "user" else "YonocyTech AI",
                content=msg["content"],
                agent_tag=msg.get("agent_tag"),
                meta=meta,
            )

        # Quick-start injection
        if "quick_prompt" in st.session_state:
            prompt = st.session_state.pop("quick_prompt")
            st.session_state.messages.append({"role": "user", "content": prompt})

            render_typing(agent_tag=agent_label)
            with st.spinner("Processing…"):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                focus = st.session_state.active_agent if st.session_state.active_agent != "general" else None
                response = loop.run_until_complete(
                    st.session_state.agent.ask(prompt, focus=focus, session_id=st.session_state.current_session_id)
                )
                meta = [
                    f"⚡ {response.provider}",
                    f"🤖 {response.model}",
                    f"⏱ {int(response.latency_ms)}ms",
                ]
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text,
                    "agent_tag": agent_label,
                    "meta": meta,
                })
            st.rerun()

        # Chat input
        if prompt := st.chat_input("Message YonocyTech AI…   (Shift+Enter for new line)"):
            st.session_state.messages.append({"role": "user", "content": prompt})

            render_typing(agent_tag=agent_label)
            with st.spinner("Processing…"):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                focus = st.session_state.active_agent if st.session_state.active_agent != "general" else None
                response = loop.run_until_complete(
                    st.session_state.agent.ask(prompt, focus=focus, session_id=st.session_state.current_session_id)
                )
                meta = [
                    f"⚡ {response.provider}",
                    f"🤖 {response.model}",
                    f"⏱ {int(response.latency_ms)}ms",
                ]
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text,
                    "agent_tag": agent_label,
                    "meta": meta,
                })
                render_response_metadata(response)
            st.rerun()

    elif st.session_state.current_page == "Agent Chain":
        st.markdown(
            "<h2 style='margin:6px 0 4px; font-size:20px;'>⛓️ Multi-Agent Orchestration</h2>"
            "<p style='color:var(--text-dim); font-size:13px; margin:0 0 16px;'>"
            "Select multiple agents and run them in sequence against the same prompt.</p>",
            unsafe_allow_html=True,
        )
        selected_agents = st.multiselect("Select agents for chain", st.session_state.orchestrator.list_agents())
        chain_prompt = st.text_area("Chain instruction", placeholder="e.g., Research the latest AI trends and write a professional summary.")
        if st.button("▶  Execute Chain"):
            if not selected_agents or not chain_prompt:
                st.warning("Please select at least one agent and provide a prompt.")
            else:
                st.session_state.chain_tasks = [{"agent": a, "prompt": chain_prompt} for a in selected_agents]
                with st.spinner("Running orchestration chain…"):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    results = loop.run_until_complete(
                        st.session_state.orchestrator.chain(st.session_state.chain_tasks, session_id=st.session_state.current_session_id)
                    )
                    for i, res in enumerate(results):
                        st.markdown(
                            f"<div class='glass-card fade-in'><b>Step {i+1}: {selected_agents[i]}</b></div>",
                            unsafe_allow_html=True,
                        )
                        st.write(res.text)
                        render_response_metadata(res)
                        st.divider()

    elif st.session_state.current_page == "Files":
        st.markdown(
            "<h2 style='margin:6px 0 16px; font-size:20px;'>📁 File Explorer</h2>",
            unsafe_allow_html=True,
        )
        files = st.session_state.fm.list_dir()
        selected_file = st.selectbox("Select file", files)
        if selected_file:
            content = st.session_state.fm.read(selected_file)
            st.code(content if content else "Empty or unreadable file")
            st.markdown("---")
            new_filename = st.text_input("New filename")
            new_content = st.text_area("Content to write")
            if st.button("💾  Save File"):
                if st.session_state.fm.write(new_filename, new_content):
                    st.success(f"Saved {new_filename}!")
                else:
                    st.error("Failed to save. Check extension or content safety.")

    elif st.session_state.current_page == "Memory":
        st.markdown(
            "<h2 style='margin:6px 0 16px; font-size:20px;'>🧠 Memory Explorer</h2>"
            "<p style='color:var(--text-dim); font-size:13px;'>Hybrid JSON + ChromaDB recall.</p>",
            unsafe_allow_html=True,
        )
        try:
            sessions = st.session_state.agent.memory.list_sessions()
            st.metric("Active sessions", len(sessions))
            st.metric("Total messages", sum(s["count"] for s in sessions))
        except Exception:
            st.info("Memory stats unavailable.")

    elif st.session_state.current_page == "Admin Panel":
        user = st.session_state.user
        if user.get("role") != "admin":
            st.error("Access denied. Admin privileges required.")
        else:
            tabs = st.tabs(["📊 Overview", "🔌 Providers", "🤖 Agents", "👥 Users", "📋 Contact", "⚙️ Settings"])

            with tabs[0]:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Users", count_users())
                col2.metric("Active Providers", len(get_all_providers()))
                col3.metric("Active Agents", len(get_all_agents()))
                stats = get_usage_stats()
                col4.metric("Total Requests", stats.get("total_requests", 0))

                st.markdown("### 📡 Provider Status")
                providers = get_all_providers()
                for p in providers:
                    status_color = {"active": "#4ADE80", "limited": "#FBBF24", "off": "#F87171"}.get(p["status"], "#A5A5C7")
                    st.markdown(
                        f"<div style='display:flex; align-items:center; gap:12px; padding:10px 14px; "
                        f"background:rgba(20,20,50,0.55); border:1px solid rgba(108,99,255,0.18); "
                        f"border-radius:10px; margin-bottom:6px;'>"
                        f"<span style='color:{status_color}; font-size:10px;'>●</span> "
                        f"<b style='flex:1;'>{p['name']}</b> "
                        f"<span style='color:#A5A5C7; font-size:13px;'>{p['rate_limit']}/min</span> "
                        f"<span style='color:var(--text-dim); font-size:13px;'>{p['status'].title()}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

            with tabs[1]:
                st.markdown("### 🔌 LLM Provider Management")
                st.caption("Enable, disable, or limit each provider.")
                providers = get_all_providers()
                for p in providers:
                    with st.expander(f"{'🟢' if p['status']=='active' else '🟡' if p['status']=='limited' else '🔴'} {p['name']}", expanded=False):
                        cols = st.columns([2, 1, 1])
                        new_status = cols[0].selectbox(
                            "Status",
                            ["active", "limited", "off"],
                            index=["active", "limited", "off"].index(p["status"]),
                            key=f"prov_status_{p['id']}"
                        )
                        new_rate = cols[1].number_input(
                            "Rate Limit (req/min)",
                            min_value=1, max_value=100,
                            value=p["rate_limit"],
                            key=f"prov_rate_{p['id']}"
                        )
                        if cols[2].button("Save", key=f"prov_save_{p['id']}"):
                            update_provider_status(p["id"], new_status)
                            update_provider_rate_limit(p["id"], new_rate)
                            st.success(f"✅ {p['name']} updated!")
                            st.rerun()

            with tabs[2]:
                st.markdown("### 🤖 Agent Management")
                st.caption("Control which agents are available.")
                agents = get_all_agents()
                for a in agents:
                    with st.expander(f"{a['icon']} {a['name']}", expanded=False):
                        cols = st.columns([2, 1])
                        new_status = cols[0].selectbox(
                            "Status",
                            ["active", "limited", "off"],
                            index=["active", "limited", "off"].index(a["status"]),
                            key=f"agent_status_{a['id']}"
                        )
                        if cols[1].button("Save", key=f"agent_save_{a['id']}"):
                            update_agent_status(a["id"], new_status)
                            st.success(f"✅ {a['name']} updated!")
                            st.rerun()

            with tabs[3]:
                st.markdown("### 👥 Registered Users")
                users = get_all_users()
                for u in users:
                    st.markdown(
                        f"<div style='display:flex; align-items:center; gap:12px; padding:10px 14px; "
                        f"background:rgba(20,20,50,0.55); border:1px solid rgba(108,99,255,0.18); "
                        f"border-radius:10px; margin-bottom:6px;'>"
                        f"<b>{u['name']}</b> "
                        f"<span style='color:#A5A5C7;'>{u['email']}</span> "
                        f"<span style='margin-left:auto;'>{'👑 Admin' if u['role']=='admin' else '👤 User'} · {u['plan']}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

            with tabs[4]:
                st.markdown("### 📋 Contact Messages")
                msgs = get_contact_messages()
                if not msgs:
                    st.info("No messages yet.")
                for m in msgs:
                    with st.expander(f"📧 {m['name']} — {m.get('subject','No Subject')}"):
                        st.write(f"**From:** {m['name']} ({m['email']})")
                        st.write(f"**Date:** {m['created_at']}")
                        st.write(f"**Message:** {m['message']}")

            with tabs[5]:
                st.markdown("### ⚙️ System Settings")
                settings = get_all_settings()
                for k, v in settings.items():
                    cols = st.columns([2, 1])
                    new_val = cols[0].text_input(k, value=v, key=f"setting_{k}")
                    if cols[1].button("Save", key=f"setting_save_{k}"):
                        set_setting(k, new_val)
                        st.success(f"✅ {k} saved!")
                st.markdown("---")
                if st.button("🗑️ Reset All Data", type="secondary"):
                    st.warning("This will clear all data. Feature coming soon.")


# ----------------------------------------------------------------------------
# ASIDE PANELS
# ----------------------------------------------------------------------------
with aside_col:
    # Provider health
    try:
        providers_meta = [
            {"role": "Primary" if i == 0 else f"Fallback {i}", "name": p.__class__.__name__.replace("Provider", "")}
            for i, p in enumerate(st.session_state.agent.providers[:3])
        ]
    except Exception:
        providers_meta = [{"role": "Primary", "name": "OpenRouter"}]
    render_aside_provider(providers_meta)

    render_aside_chain(st.session_state.chain_tasks)

    render_aside_memory([
        {"type": "vector", "text": "User prefers TypeScript + Tailwind"},
        {"type": "vector", "text": "Project: YonocyTech AI v2.0"},
        {"type": "json",   "text": f"{len(st.session_state.messages)} messages this session"},
    ])

    stats = get_usage_stats()
    render_aside_stats({
        "Messages":            str(len(st.session_state.messages)),
        "Sessions":            str(stats.get("total_sessions", len(st.session_state.agent.memory.sessions))),
        "Tokens used":         str(stats.get("total_tokens", "0")),
        "Providers":           str(len(st.session_state.agent.providers)),
    })

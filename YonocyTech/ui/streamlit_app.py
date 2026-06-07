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
for _key in ["OPENROUTER_API_KEY", "HF_API_KEY", "GITHUB_TOKEN", "DEEPAI_API_KEY"]:
    if _key in st.secrets:
        os.environ[_key] = st.secrets[_key]

from core import YonocyTech
from agents import ALL_AGENTS
from tools.file_manager import FileManager
from tools.orchestrator import Orchestrator
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
# STATE
# ----------------------------------------------------------------------------
if "agent" not in st.session_state:
    st.session_state.agent = YonocyTech()
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

    st.markdown(
        "<h4 style='font-size:11px; text-transform:uppercase; letter-spacing:1.2px; "
        "color:var(--text-mute); margin:14px 8px 8px; font-weight:600;'>Workspace</h4>",
        unsafe_allow_html=True,
    )
    for page, icon in [("Chat", "💬"), ("Agent Chain", "⛓️"), ("Files", "📁"), ("Memory", "🧠")]:
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
                name="Habibur Rahman" if msg["role"] == "user" else "YonocyTech AI",
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
            count = st.session_state.agent.memory.count if hasattr(st.session_state.agent.memory, "count") else 0
            st.metric("Vector nodes", count)
        except Exception:
            st.info("Memory stats unavailable.")


# ----------------------------------------------------------------------------
# ASIDE PANELS
# ----------------------------------------------------------------------------
with aside_col:
    # Provider health
    try:
        providers_meta = [
            {"role": "Primary",   "name": getattr(p, "name", str(p))}
            for p in st.session_state.agent.providers[:3]
        ]
    except Exception:
        providers_meta = [{"role": "Primary", "name": "openrouter"}]
    render_aside_provider(providers_meta)

    render_aside_chain(st.session_state.chain_tasks)

    render_aside_memory([
        {"type": "vector", "text": "User prefers TypeScript + Tailwind"},
        {"type": "vector", "text": "Project: YonocyTech AI v2.0"},
        {"type": "json",   "text": f"{len(st.session_state.messages)} messages this session"},
    ])

    render_aside_stats({
        "Tokens used":         "2,847",
        "Cost":                "$0.00",
        "Latency avg":         "1.2s",
        "Injections blocked":  '<span style="color:var(--danger);">3</span>',
    })

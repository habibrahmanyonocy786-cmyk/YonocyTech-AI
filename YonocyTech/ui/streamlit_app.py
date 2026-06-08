import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import asyncio

for _key in ["OPENROUTER_API_KEY", "HF_API_KEY", "GITHUB_TOKEN", "DEEPAI_API_KEY",
             "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "ADMIN_EMAIL"]:
    if _key in st.secrets:
        os.environ[_key] = st.secrets[_key]

from core import YonocyTech
from agents import ALL_AGENTS
from tools.file_manager import FileManager
from tools.orchestrator import Orchestrator
from auth.admin import AdminManager
from i18n.translator import Translator
from ui.components import (
    apply_theme, render_brand, render_header, render_session_card,
    render_welcome, render_quick_starts, render_msg_bubble, render_typing,
    render_response_metadata, render_aside_provider, render_aside_chain,
    render_aside_memory, render_aside_stats, render_agent_badge,
    render_login_page, render_skeleton_loader,
)
from workflows.templates import WorkflowTemplates, WorkflowExecutor
from workflows.n8n_display import render_n8n_workflows
from integrations.google_sheets_demo import render_sheets_demo

st.set_page_config(
    page_title="YonocyTech AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
t = Translator()

# ----------------------------------------------------------------------------
# STATE INIT
# ----------------------------------------------------------------------------
if "agent" not in st.session_state:
    st.session_state.agent = YonocyTech()
    st.session_state.fm = FileManager()
    agents_instances = {name: cls(st.session_state.agent) for name, cls in ALL_AGENTS.items()}
    st.session_state.orchestrator = Orchestrator(st.session_state.agent, agents_instances)
    st.session_state.workflow_executor = WorkflowExecutor(st.session_state.orchestrator)
    st.session_state.admin = AdminManager()
    st.session_state.messages = []
    st.session_state.current_session_id = st.session_state.agent.memory.new_session()
    st.session_state.current_page = "Chat"
    st.session_state.active_agent = "general"
    st.session_state.chain_tasks = []
    st.session_state.language = "fa"
    st.session_state.ollama_checked = False
    st.session_state.ollama_available = False
    if "user" not in st.session_state:
        st.session_state.user = None

# ----------------------------------------------------------------------------
# AUTH CHECK
# ----------------------------------------------------------------------------
user = st.session_state.get("user")
is_logged_in = user is not None
is_admin = user.get("is_admin", False) if user else False

# Handle OAuth callback
query_params = st.query_params
if "code" in query_params and "state" in query_params:
    from auth.google_auth import GoogleAuth
    ga = GoogleAuth()
    user_info = asyncio.run(ga.handle_callback(query_params["code"], query_params["state"]))
    if user_info:
        user_info["is_admin"] = user_info.get("email", "") == os.getenv("ADMIN_EMAIL", "")
        st.session_state.user = user_info
        st.rerun()
    st.query_params.clear()

if not is_logged_in:
    render_login_page()
    st.stop()

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

    nav_items = [
        ("Chat", "💬"),
        ("Agent Chain", "⛓️"),
        ("Files", "📁"),
        ("Memory", "🧠"),
    ]

    if is_logged_in:
        nav_items.append(("Workflows", "⚡"))
        nav_items.append(("Databases", "📊"))
    if is_admin:
        nav_items.append(("Admin", "👤"))

    for page, icon in nav_items:
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
            "summarizer": "📝", "tutor": "🎓",
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

    if is_logged_in:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
agent_label = st.session_state.active_agent.title() if st.session_state.active_agent != "general" else "General Assistant"
page_names = {
    "Chat": "💬 Chat", "Agent Chain": "⛓️ Agent Chain", "Files": "📁 Files",
    "Memory": "🧠 Memory", "Workflows": "⚡ Workflows",
    "Databases": "📊 Databases", "Admin": "👤 Admin",
}
render_header(active_page=page_names.get(st.session_state.current_page, "Chat"), agent_label=agent_label, online=True)

# ----------------------------------------------------------------------------
# MAIN + ASIDE
# ----------------------------------------------------------------------------
main_col, aside_col = st.columns([3, 1], gap="medium")

with main_col:
    page = st.session_state.current_page

    # ===================== CHAT PAGE =====================
    if page == "Chat":
        if not st.session_state.messages:
            render_welcome()
            render_quick_starts([
                {"icon": "💡", "title": t("chat.quick_brainstorm"), "desc": t("chat.quick_brainstorm_desc")},
                {"icon": "🧪", "title": t("chat.quick_code"), "desc": t("chat.quick_code_desc")},
                {"icon": "📊", "title": t("chat.quick_data"), "desc": t("chat.quick_data_desc")},
                {"icon": "✍️", "title": t("chat.quick_write"), "desc": t("chat.quick_write_desc")},
            ])

        for msg in st.session_state.messages:
            meta = msg.get("meta")
            render_msg_bubble(
                role=msg["role"],
                name="Habibur Rahman" if msg["role"] == "user" else "YonocyTech AI",
                content=msg["content"],
                agent_tag=msg.get("agent_tag"),
                meta=meta,
            )

        if "quick_prompt" in st.session_state:
            prompt = st.session_state.pop("quick_prompt")
            st.session_state.messages.append({"role": "user", "content": prompt})
            render_typing(agent_tag=agent_label)
            with st.spinner(t("chat.thinking")):
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
                # Track usage
                email = user.get("email", "anonymous") if user else "anonymous"
                st.session_state.admin.log_request(
                    provider=response.provider,
                    model=response.model,
                    tokens_used=getattr(response, "tokens_used", 0),
                    user_email=email,
                    latency_ms=response.latency_ms,
                )
            st.rerun()

        if prompt := st.chat_input(t("chat.placeholder")):
            st.session_state.messages.append({"role": "user", "content": prompt})
            render_typing(agent_tag=agent_label)
            with st.spinner(t("chat.thinking")):
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
                email = user.get("email", "anonymous") if user else "anonymous"
                st.session_state.admin.log_request(
                    provider=response.provider,
                    model=response.model,
                    tokens_used=getattr(response, "tokens_used", 0),
                    user_email=email,
                    latency_ms=response.latency_ms,
                )
            st.rerun()

    # ===================== AGENT CHAIN PAGE =====================
    elif page == "Agent Chain":
        st.markdown(
            "<h2 style='margin:6px 0 4px; font-size:20px;'>⛓️ Multi-Agent Orchestration</h2>"
            "<p style='color:var(--text-dim); font-size:13px; margin:0 0 16px;'>"
            "Select multiple agents and run them in sequence against the same prompt.</p>",
            unsafe_allow_html=True,
        )
        selected_agents = st.multiselect(t("chain.select"), st.session_state.orchestrator.list_agents())
        chain_prompt = st.text_area("Chain instruction", placeholder=t("chain.placeholder"))
        if st.button(t("chain.execute")):
            if not selected_agents or not chain_prompt:
                st.warning("Please select at least one agent and provide a prompt.")
            else:
                st.session_state.chain_tasks = [{"agent": a, "prompt": chain_prompt} for a in selected_agents]
                with st.spinner("Running orchestration chain…"):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    results = loop.run_until_complete(
                        st.session_state.orchestrator.chain(
                            st.session_state.chain_tasks,
                            session_id=st.session_state.current_session_id
                        )
                    )
                    for i, res in enumerate(results):
                        st.markdown(
                            f'<div class="glass-card fade-in"><b>{t("chain.step")} {i+1}: {selected_agents[i]}</b></div>',
                            unsafe_allow_html=True,
                        )
                        st.write(res.text)
                        render_response_metadata(res)
                        email = user.get("email", "anonymous") if user else "anonymous"
                        st.session_state.admin.log_request(
                            provider=res.provider, model=res.model,
                            tokens_used=getattr(res, "tokens_used", 0),
                            user_email=email, latency_ms=res.latency_ms,
                        )
                        st.divider()

    # ===================== FILES PAGE =====================
    elif page == "Files":
        st.markdown(
            f"<h2 style='margin:6px 0 16px; font-size:20px;'>{t('files.title')}</h2>",
            unsafe_allow_html=True,
        )
        files = st.session_state.fm.list_dir()
        selected_file = st.selectbox(t("files.select"), files)
        if selected_file:
            content = st.session_state.fm.read(selected_file)
            st.code(content if content else "Empty or unreadable file")
            st.markdown("---")
            new_filename = st.text_input(t("files.new_name"))
            new_content = st.text_area(t("files.content"))
            if st.button(t("files.save")):
                if st.session_state.fm.write(new_filename, new_content):
                    st.success(t("files.saved"))
                else:
                    st.error(t("files.error"))

    # ===================== MEMORY PAGE =====================
    elif page == "Memory":
        st.markdown(
            f"<h2 style='margin:6px 0 16px; font-size:20px;'>{t('memory.title')}</h2>"
            f"<p style='color:var(--text-dim); font-size:13px;'>Hybrid JSON + ChromaDB recall.</p>",
            unsafe_allow_html=True,
        )
        try:
            count = st.session_state.agent.memory.count if hasattr(st.session_state.agent.memory, "count") else 0
            st.metric(t("memory.nodes"), count)
        except Exception:
            st.info(t("memory.stats"))

    # ===================== WORKFLOWS PAGE =====================
    elif page == "Workflows":
        st.markdown(
            f"<h2 style='margin:6px 0 4px; font-size:20px;'>{t('workflows.title')}</h2>"
            f"<p style='color:var(--text-dim); font-size:13px; margin:0 0 16px;'>{t('workflows.desc')}</p>",
            unsafe_allow_html=True,
        )

        templates = WorkflowTemplates.get_all()
        topic = st.text_input("موضوع / Topic", placeholder="e.g., AI-powered chatbot for customer support")

        cols = st.columns(2)
        for idx, (wf_name, wf) in enumerate(templates.items()):
            with cols[idx % 2]:
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding:16px;">
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                            <span style="font-size:24px;">{wf['icon']}</span>
                            <div>
                                <div style="font-size:14px; font-weight:700;">{t(f'workflows.{wf_name}')}</div>
                                <div style="font-size:11px; color:var(--text-dim);">{t(f'workflows.{wf_name}_desc')}</div>
                            </div>
                        </div>
                        <div style="display:flex; gap:4px; flex-wrap:wrap; margin-bottom:10px;">
                            {''.join(f'<span class="agent-tag" style="font-size:10px;">{a}</span>' for a in wf['agents'])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"{t('workflows.run')} {wf['name']}", key=f"wf_{wf_name}", use_container_width=True):
                    with st.spinner(t("workflows.running")):
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        results = loop.run_until_complete(
                            st.session_state.workflow_executor.execute(
                                wf_name, topic, session_id=st.session_state.current_session_id
                            )
                        )
                        st.success(f"✅ Workflow completed in {len(results)} steps!")
                        for i, (agent, res) in enumerate(zip(wf["agents"], results)):
                            with st.expander(f"Step {i+1}: {agent.title()}"):
                                st.write(res.text)
                                render_response_metadata(res)

        st.markdown("---")
        render_n8n_workflows()

    # ===================== DATABASES PAGE =====================
    elif page == "Databases":
        st.markdown(
            f"<h2 style='margin:6px 0 4px; font-size:20px;'>{t('database.title')}</h2>"
            f"<p style='color:var(--text-dim); font-size:13px; margin:0 0 16px;'>{t('database.desc')}</p>",
            unsafe_allow_html=True,
        )
        render_sheets_demo()

    # ===================== ADMIN PAGE =====================
    elif page == "Admin" and is_admin:
        from ui.pages.admin_page import render_admin_page
        render_admin_page()

# ----------------------------------------------------------------------------
# ASIDE PANELS
# ----------------------------------------------------------------------------
with aside_col:
    try:
        providers_meta = [
            {"role": t("provider.primary"), "name": getattr(p, "name", str(p))}
            for p in st.session_state.agent.providers[:3]
        ]
    except Exception:
        providers_meta = [{"role": t("provider.primary"), "name": "openrouter"}]
    render_aside_provider(providers_meta)

    render_aside_chain(st.session_state.chain_tasks)

    render_aside_memory([
        {"type": "vector", "text": "User prefers TypeScript + Tailwind"},
        {"type": "vector", "text": "Project: YonocyTech AI v2.1"},
        {"type": "json", "text": f"{len(st.session_state.messages)} messages this session"},
    ])

    render_aside_stats({
        t("stats.tokens"): str(st.session_state.admin.stats.get("total_tokens", 0)),
        t("stats.cost"): "$0.00",
        t("stats.latency"): "1.2s",
        t("stats.blocked"): '<span style="color:var(--danger);">3</span>',
    })

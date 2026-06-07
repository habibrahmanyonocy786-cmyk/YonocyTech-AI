"""
YonocyTech AI — UI Design System v2.0
Reusable Streamlit components aligned with docs/ui-spec.md.
"""
import streamlit as st
from core import AgentResponse


# ----------------------------------------------------------------------------
# DESIGN TOKENS & GLOBAL THEME
# ----------------------------------------------------------------------------
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-0: #07071A;
    --bg-1: #0B0B24;
    --bg-2: #11112E;
    --bg-3: #1A1A3E;
    --surface: rgba(20, 20, 50, 0.55);
    --surface-2: rgba(28, 28, 65, 0.65);
    --border: rgba(108, 99, 255, 0.18);
    --border-strong: rgba(108, 99, 255, 0.45);
    --text: #ECECFF;
    --text-dim: #A5A5C7;
    --text-mute: #6F6F95;
    --primary: #6C63FF;
    --primary-2: #00D9FF;
    --accent: #FF4FCB;
    --success: #4ADE80;
    --warning: #FBBF24;
    --danger: #F87171;
    --gradient-brand: linear-gradient(135deg, #6C63FF 0%, #00D9FF 50%, #FF4FCB 100%);
    --shadow-glow: 0 0 0 1px rgba(108,99,255,0.25), 0 20px 60px rgba(108,99,255,0.25);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(1200px 800px at 15% 10%, rgba(108,99,255,0.20), transparent 60%),
        radial-gradient(900px 700px at 90% 20%, rgba(0,217,255,0.16), transparent 60%),
        radial-gradient(800px 600px at 50% 100%, rgba(255,79,203,0.14), transparent 60%),
        linear-gradient(135deg, #07071A 0%, #0B0B24 50%, #11112E 100%) !important;
    color: var(--text);
}

h1, h2, h3, h4, h5, h6, p, span, label, li, div {
    color: var(--text);
}

/* === Sidebar === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(11,11,36,0.92), rgba(7,7,26,0.97)) !important;
    border-right: 1px solid var(--border) !important;
}

/* === Inputs === */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stChatInput > div > div > textarea {
    background-color: rgba(17,17,46,0.7) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    caret-color: var(--primary-2) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-2) !important;
    box-shadow: 0 0 0 2px rgba(0,217,255,0.25) !important;
}

/* === Selectbox === */
.stSelectbox > div > div {
    background-color: rgba(17,17,46,0.7) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}

/* === Buttons === */
.stButton > button {
    background: var(--gradient-brand) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 18px !important;
    box-shadow: 0 8px 24px rgba(108,99,255,0.35) !important;
    transition: transform .2s, box-shadow .2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 12px 30px rgba(108,99,255,0.55) !important;
}
.stButton > button:focus { outline: 2px solid var(--primary-2) !important; outline-offset: 2px; }

/* Secondary buttons */
.stDownloadButton > button {
    background: rgba(108,99,255,0.15) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}

/* === Tabs === */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-dim) !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
    font-weight: 500;
    transition: all .2s;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(108,99,255,0.08) !important;
    color: var(--text) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(108,99,255,0.20), rgba(0,217,255,0.10)) !important;
    color: var(--text) !important;
    border-color: var(--border-strong) !important;
}

/* === Expanders === */
.streamlit-expanderHeader, [data-testid="stExpander"] details summary {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-weight: 500;
}

/* === Code blocks === */
code, pre, .stCode {
    background: rgba(0,0,0,0.45) !important;
    color: var(--primary-2) !important;
    border: 1px solid var(--border);
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* === Spinner === */
.stSpinner > div {
    border-top-color: var(--primary-2) !important;
}

/* === Toast / alerts === */
.stAlert {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}

/* === Chat messages (st.chat_message) === */
[data-testid="stChatMessage"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 14px 16px !important;
    backdrop-filter: blur(8px);
}

/* === Custom bubbles === */
.user-bubble {
    background: linear-gradient(135deg, rgba(0,217,255,0.18), rgba(108,99,255,0.18));
    padding: 12px 16px;
    border-radius: 14px;
    margin: 10px 0;
    border: 1px solid rgba(0,217,255,0.25);
    border-top-left-radius: 4px;
    color: var(--text);
    font-size: 14px;
    line-height: 1.55;
}
.ai-bubble {
    background: var(--surface-2);
    padding: 12px 16px;
    border-radius: 14px;
    margin: 10px 0;
    border: 1px solid var(--border);
    border-top-left-radius: 4px;
    backdrop-filter: blur(8px);
    color: var(--text);
    font-size: 14px;
    line-height: 1.55;
}

/* === Metadata chips === */
.meta-chip {
    display: inline-block;
    background: rgba(108,99,255,0.10);
    border: 1px solid var(--border);
    color: var(--text-dim);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    margin-right: 6px;
}
.agent-tag {
    display: inline-block;
    background: var(--gradient-brand);
    color: #fff;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 10.5px;
    font-weight: 600;
    margin-left: 6px;
}

/* === Glass card === */
.glass-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
}

/* === Animations === */
@keyframes fadeIn { from { opacity:0; transform: translateY(8px);} to {opacity:1; transform:none;} }
.fade-in { animation: fadeIn 0.5s ease-out both; }

@keyframes slideRight { from { transform: translateX(-20px); opacity:0; } to { transform:none; opacity:1; } }
.slide-right { animation: slideRight 0.6s ease-out both; }

@keyframes pulseGlow {
    0%,100% { box-shadow: 0 0 0 0 rgba(0,217,255,0.4); }
    50%     { box-shadow: 0 0 0 8px rgba(0,217,255,0); }
}
.pulse { animation: pulseGlow 2s ease-in-out infinite; }

@keyframes typingBounce { 0%,80%,100% { transform: translateY(0); opacity: 0.4;} 40% { transform: translateY(-6px); opacity: 1;} }
.typing-dot {
    display:inline-block; width:6px; height:6px; border-radius:50%;
    background: var(--primary-2); margin: 0 2px;
    animation: typingBounce 1.2s infinite ease-in-out;
}
.typing-dot:nth-child(2) { animation-delay: 0.15s; }
.typing-dot:nth-child(3) { animation-delay: 0.30s; }

/* === Brand logo === */
.brand-logo {
    width: 38px; height: 38px; border-radius: 10px;
    background: var(--gradient-brand);
    display: inline-grid; place-items: center; font-size: 20px;
    box-shadow: 0 6px 20px rgba(108,99,255,0.45);
    position: relative;
}
.brand-logo::after {
    content:""; position:absolute; inset:-3px; border-radius:12px;
    background: var(--gradient-brand); filter: blur(14px); opacity:0.55; z-index:-1;
}

/* === Status pills === */
.status-online { color: var(--success); }
.status-warn   { color: var(--warning); }
.status-error  { color: var(--danger); }

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""


def apply_theme():
    """Inject the global CSS theme. Call once at the top of the app."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# BRAND & HEADER
# ----------------------------------------------------------------------------
def render_brand():
    """Logo + wordmark, used in sidebar top."""
    st.markdown(
        """
        <div class="slide-right" style="display:flex; align-items:center; gap:10px; padding:6px 8px; margin-bottom:8px;">
            <div class="brand-logo">🚀</div>
            <div>
                <div style="font-size:15px; font-weight:700; letter-spacing:0.3px;">YonocyTech AI</div>
                <div style="font-size:11px; color:var(--text-dim); margin-top:2px;">Low-Resource Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(active_page: str, agent_label: str = "General Assistant", online: bool = True):
    """Top breadcrumb + status + primary CTA."""
    status = '<span class="status-online">● Online</span>' if online else '<span class="status-error">● Offline</span>'
    st.markdown(
        f"""
        <div class="fade-in" style="display:flex; align-items:center; justify-content:space-between;
                    padding:14px 4px; border-bottom:1px solid var(--border); margin-bottom:18px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="background:var(--surface); border:1px solid var(--border);
                             padding:6px 12px; border-radius:999px; font-size:12px; color:var(--text-dim);">
                    <b style="color:var(--text);">{active_page}</b>
                </span>
                <span style="color:var(--text-mute);">›</span>
                <span style="background:var(--surface); border:1px solid var(--border);
                             padding:6px 12px; border-radius:999px; font-size:12px; color:var(--text-dim);">
                    {agent_label}
                </span>
                <span style="color:var(--text-mute);">·</span>
                <span style="background:var(--surface); border:1px solid rgba(74,222,128,0.45);
                             padding:6px 12px; border-radius:999px; font-size:12px;">{status}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# AGENT SIDEBAR LIST
# ----------------------------------------------------------------------------
AGENT_META = {
    "coding":    {"icon": "💻", "desc": "Generate & execute"},
    "writing":   {"icon": "✍️", "desc": "Pro & creative"},
    "data":      {"icon": "📊", "desc": "CSV / Excel analysis"},
    "design":    {"icon": "🎨", "desc": "UI / UX specs"},
    "marketing": {"icon": "📈", "desc": "SEO & growth"},
    "research":  {"icon": "🔍", "desc": "Deep web + citations"},
}


def render_agent_item(key: str, label: str, active: bool = False) -> bool:
    """Render a single agent row. Returns True if clicked."""
    meta = AGENT_META.get(key.lower(), {"icon": "🤖", "desc": ""})
    active_cls = "active" if active else ""
    st.markdown(
        f"""
        <div class="agent-row {active_cls}" style="display:flex; align-items:center; gap:10px;
                    padding:10px 12px; border-radius:14px; cursor:pointer;
                    border:1px solid {'var(--border-strong)' if active else 'transparent'};
                    background: {'linear-gradient(90deg, rgba(108,99,255,0.20), rgba(0,217,255,0.10))' if active else 'transparent'};
                    margin-bottom:4px; transition:all .2s;">
            <div style="width:32px; height:32px; border-radius:9px; display:grid; place-items:center;
                        background:rgba(108,99,255,0.15); font-size:16px;">{meta['icon']}</div>
            <div>
                <div style="font-size:13px; font-weight:600;">{label}</div>
                <div style="font-size:11px; color:var(--text-dim);">{meta['desc']}</div>
            </div>
            <div style="margin-left:auto; width:7px; height:7px; border-radius:50%; background:var(--success);
                        box-shadow:0 0 0 3px rgba(74,222,128,0.18);"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return st.button(f"Use {label}", key=f"agent_{key}", use_container_width=True)


def render_session_card(user_name: str = "Habibur Rahman", tier: str = "Free tier"):
    """Bottom user pill inside the sidebar."""
    initials = "".join([p[0] for p in user_name.split()[:2]]).upper() or "U"
    st.markdown(
        f"""
        <div class="glass-card fade-in" style="display:flex; align-items:center; gap:10px; margin-top:18px;">
            <div style="width:36px; height:36px; border-radius:50%; background:var(--gradient-brand);
                        display:grid; place-items:center; font-weight:700; color:#fff; font-size:13px;">
                {initials}
            </div>
            <div>
                <div style="font-size:13px; font-weight:600;">{user_name}</div>
                <div style="font-size:11px; color:var(--text-dim);">{tier} · $0.00</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# ASIDE PANELS
# ----------------------------------------------------------------------------
def render_aside_provider(providers: list):
    """Live provider / fallback status panel."""
    rows = ""
    for p in providers[:5]:
        rows += f'<div class="kv"><span>{p.get("role","Provider")}</span><b>{p.get("name","—")}</b></div>'
    st.markdown(
        f"""
        <div class="glass-card fade-in">
            <h3 style="margin:0 0 10px; font-size:13px; display:flex; align-items:center; gap:8px;">
                <span>📡</span> Active Provider
            </h3>
            {rows}
            <div class="kv"><span>Status</span><b class="status-online">● Healthy</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_aside_chain(tasks: list):
    """Multi-agent chain stepper."""
    if not tasks:
        body = '<div style="font-size:12px; color:var(--text-mute);">No active chain.</div>'
    else:
        body = ""
        for i, t in enumerate(tasks, 1):
            label = t.get("agent", "agent")
            desc = t.get("prompt", "")[:60]
            body += f"""
                <div style="display:flex; gap:10px; align-items:flex-start; padding:10px 0;
                            border-bottom:1px dashed var(--border);">
                    <div style="width:22px; height:22px; border-radius:50%; background:var(--gradient-brand);
                                display:grid; place-items:center; font-size:11px; font-weight:700; color:#fff; flex-shrink:0;">{i}</div>
                    <div>
                        <div style="font-size:12.5px; font-weight:600;">{label}</div>
                        <div style="font-size:11px; color:var(--text-dim);">{desc}</div>
                    </div>
                </div>
            """
    st.markdown(
        f"""
        <div class="glass-card fade-in">
            <h3 style="margin:0 0 10px; font-size:13px; display:flex; align-items:center; gap:8px;">
                <span>⛓️</span> Current Chain
            </h3>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_aside_memory(items: list):
    """Vector + JSON recall panel."""
    if not items:
        body = '<div style="font-size:12px; color:var(--text-mute);">No memories yet.</div>'
    else:
        body = ""
        for it in items[:5]:
            tag = it.get("type", "memory").upper()
            text = it.get("text", "")
            body += f"""
                <div style="background:rgba(0,0,0,0.25); border:1px solid var(--border); border-radius:8px;
                            padding:8px 10px; margin-bottom:6px; font-size:11.5px; line-height:1.4;">
                    <b style="color:var(--primary-2); font-size:10.5px; letter-spacing:0.5px;">{tag}</b><br/>{text}
                </div>
            """
    st.markdown(
        f"""
        <div class="glass-card fade-in">
            <h3 style="margin:0 0 10px; font-size:13px; display:flex; align-items:center; gap:8px;">
                <span>🧠</span> Memory Recall
            </h3>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_aside_stats(stats: dict):
    """Tokens / cost / latency / blocked."""
    rows = ""
    for k, v in stats.items():
        rows += f'<div class="kv"><span>{k}</span><b>{v}</b></div>'
    st.markdown(
        f"""
        <div class="glass-card fade-in">
            <h3 style="margin:0 0 10px; font-size:13px; display:flex; align-items:center; gap:8px;">
                <span>📊</span> Session Stats
            </h3>
            {rows}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# CHAT UI
# ----------------------------------------------------------------------------
def render_welcome():
    """Hero + 4 quick-start cards."""
    st.markdown(
        """
        <div class="fade-in" style="text-align:center; padding:36px 8px 8px;">
            <h1 style="font-size:32px; margin:0; font-weight:800;
                       background:var(--gradient-brand); -webkit-background-clip:text; background-clip:text; color:transparent;
                       letter-spacing:-0.5px;">
                How can I help you ship today?
            </h1>
            <p style="color:var(--text-dim); margin:8px 0 0; font-size:14px;">
                Ask anything · chain specialized agents · or pick a quick starter below.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_starts(options: list):
    """Render a row of quick-start buttons. options = [{icon,title,desc}]"""
    cols = st.columns(len(options))
    for col, opt in zip(cols, options):
        with col:
            if st.button(
                f"{opt['icon']}  {opt['title']}\n\n{opt['desc']}",
                key=f"qs_{opt['title']}",
                use_container_width=True,
            ):
                st.session_state["quick_prompt"] = opt["desc"]


def render_msg_bubble(role: str, name: str, content: str, agent_tag: str = None, meta: list = None):
    """Render a single chat bubble (user or assistant)."""
    bubble_cls = "user-bubble" if role == "user" else "ai-bubble"
    who_html = ""
    if role != "user":
        tag_html = f'<span class="agent-tag">{agent_tag}</span>' if agent_tag else ""
        who_html = f'<div style="font-size:12px; color:var(--text-dim); margin-bottom:4px;">{name}{tag_html}</div>'

    meta_html = ""
    if meta:
        chips = "".join(f'<span class="meta-chip">{m}</span>' for m in meta)
        meta_html = f'<div style="margin-top:6px;">{chips}</div>'

    st.markdown(
        f"""
        <div class="fade-in" style="display:flex; gap:12px; margin:14px 0; align-items:flex-start;">
            <div style="width:34px; height:34px; border-radius:10px; flex-shrink:0;
                        display:grid; place-items:center; font-weight:700; font-size:13px;
                        background: {'linear-gradient(135deg,#00D9FF,#6C63FF)' if role=='user' else 'var(--gradient-brand)'};
                        color:#fff; {'box-shadow:0 4px 18px rgba(108,99,255,0.5);' if role!='user' else ''}">
                {('HR' if role=='user' else 'Y')}
            </div>
            <div style="max-width:78%;">
                <div class="{bubble_cls}">
                    {who_html}
                    {content}
                </div>
                {meta_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_typing(agent_tag: str = "AI"):
    """Animated 3-dot typing indicator."""
    st.markdown(
        f"""
        <div class="fade-in" style="display:flex; gap:12px; margin:14px 0; align-items:flex-start;">
            <div style="width:34px; height:34px; border-radius:10px; background:var(--gradient-brand);
                        display:grid; place-items:center; color:#fff; font-weight:700; font-size:13px;">Y</div>
            <div class="ai-bubble" style="display:flex; align-items:center; gap:6px;">
                <span class="agent-tag">{agent_tag}</span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# METADATA (legacy compat)
# ----------------------------------------------------------------------------
def render_agent_badge(agent_name: str):
    """Renders a small badge indicating the active agent."""
    st.markdown(
        f'<span class="agent-tag">{agent_name}</span>',
        unsafe_allow_html=True,
    )


def render_response_metadata(response: AgentResponse):
    """Displays the latency and model used for a response in an expander."""
    with st.expander("View Response Metadata"):
        col1, col2, col3 = st.columns(3)
        col1.text(f"Provider: {response.provider}")
        col2.text(f"Model: {response.model}")
        col3.text(f"Latency: {int(response.latency_ms)}ms")
        if getattr(response, "tokens_used", None):
            st.text(f"Tokens Used: {response.tokens_used}")


def render_empty_state():
    """Displays a welcome message when no chat is active."""
    st.info("👋 Welcome to YonocyTech AI! Start a conversation in the chat tab or chain agents in the Agent Chain tab.")


def render_welcome_message():
    """Renders the main welcome header (legacy alias)."""
    render_welcome()

import streamlit as st
from core import AgentResponse
from i18n.translator import Translator


THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Vazirmatn:wght@300;400;500;600;700;800&display=swap');

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
    font-family: 'Inter', 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* === Cosmic Background === */
.stApp {
    background:
        radial-gradient(ellipse 1200px 800px at 15% 10%, rgba(108,99,255,0.20), transparent 60%),
        radial-gradient(ellipse 900px 700px at 90% 20%, rgba(0,217,255,0.16), transparent 60%),
        radial-gradient(ellipse 800px 600px at 50% 100%, rgba(255,79,203,0.14), transparent 60%),
        linear-gradient(135deg, #07071A 0%, #0B0B24 50%, #11112E 100%) !important;
    color: var(--text);
    position: relative;
    overflow-x: hidden;
}

/* Star field layers */
.stApp::before,
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
}
.stApp::before {
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.6), transparent),
        radial-gradient(1px 1px at 30% 60%, rgba(255,255,255,0.5), transparent),
        radial-gradient(1.5px 1.5px at 50% 10%, rgba(255,255,255,0.7), transparent),
        radial-gradient(1px 1px at 70% 40%, rgba(255,255,255,0.4), transparent),
        radial-gradient(1.5px 1.5px at 85% 70%, rgba(255,255,255,0.6), transparent),
        radial-gradient(1px 1px at 15% 85%, rgba(255,255,255,0.5), transparent),
        radial-gradient(1px 1px at 45% 45%, rgba(255,255,255,0.3), transparent),
        radial-gradient(1px 1px at 90% 15%, rgba(255,255,255,0.5), transparent),
        radial-gradient(1.5px 1.5px at 60% 80%, rgba(255,255,255,0.4), transparent),
        radial-gradient(1px 1px at 25% 35%, rgba(255,255,255,0.6), transparent),
        radial-gradient(1px 1px at 5% 55%, rgba(255,255,255,0.3), transparent),
        radial-gradient(1.5px 1.5px at 75% 90%, rgba(255,255,255,0.5), transparent),
        radial-gradient(1px 1px at 40% 75%, rgba(255,255,255,0.4), transparent),
        radial-gradient(1px 1px at 95% 50%, rgba(255,255,255,0.6), transparent),
        radial-gradient(1.5px 1.5px at 55% 30%, rgba(255,255,255,0.5), transparent),
        radial-gradient(1px 1px at 20% 5%, rgba(255,255,255,0.3), transparent),
        radial-gradient(1px 1px at 65% 5%, rgba(255,255,255,0.5), transparent),
        radial-gradient(1.5px 1.5px at 35% 95%, rgba(255,255,255,0.4), transparent),
        radial-gradient(1px 1px at 80% 60%, rgba(255,255,255,0.6), transparent),
        radial-gradient(1px 1px at 0% 40%, rgba(255,255,255,0.3), transparent);
    animation: starDrift1 90s linear infinite;
    opacity: 0.7;
}
.stApp::after {
    background-image:
        radial-gradient(1px 1px at 12% 35%, rgba(200,200,255,0.4), transparent),
        radial-gradient(1px 1px at 55% 65%, rgba(200,200,255,0.3), transparent),
        radial-gradient(1px 1px at 78% 22%, rgba(200,200,255,0.5), transparent),
        radial-gradient(1px 1px at 33% 88%, rgba(200,200,255,0.3), transparent),
        radial-gradient(1px 1px at 92% 45%, rgba(200,200,255,0.4), transparent),
        radial-gradient(1px 1px at 48% 15%, rgba(200,200,255,0.5), transparent),
        radial-gradient(1px 1px at 18% 72%, rgba(200,200,255,0.3), transparent),
        radial-gradient(1px 1px at 68% 50%, rgba(200,200,255,0.4), transparent),
        radial-gradient(1px 1px at 40% 42%, rgba(200,200,255,0.3), transparent);
    animation: starDrift2 140s linear infinite;
    opacity: 0.4;
}

/* Star drift animations */
@keyframes starDrift1 {
    from { transform: translateY(0) translateX(0); }
    to   { transform: translateY(-200px) translateX(50px); }
}
@keyframes starDrift2 {
    from { transform: translateY(0) translateX(0); }
    to   { transform: translateY(-150px) translateX(-30px); }
}

h1, h2, h3, h4, h5, h6, p, span, label, li, div {
    color: var(--text);
}

/* === Sidebar === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(11,11,36,0.92), rgba(7,7,26,0.97)) !important;
    border-right: 1px solid var(--border) !important;
    z-index: 1;
}

/* === RTL Support === */
.rtl {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Vazirmatn', 'Inter', sans-serif !important;
}
.ltr {
    direction: ltr !important;
    text-align: left !important;
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
    transform: translateY(0);
    transition: transform .2s, box-shadow .2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(108,99,255,0.55) !important;
}
.stButton > button:focus { outline: 2px solid var(--primary-2) !important; outline-offset: 2px; }

.stDownloadButton > button {
    background: rgba(108,99,255,0.15) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}

/* === Tabs === */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; }
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
.stSpinner > div { border-top-color: var(--primary-2) !important; }

/* === Toast / alerts === */
.stAlert {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}

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

/* === Meta chips === */
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

/* === Improved Animations === */
@keyframes fadeIn {
    from { opacity:0; transform: translateY(10px); }
    to { opacity:1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.5s ease-out both; }

@keyframes slideInLeft {
    from { transform: translateX(-30px); opacity:0; }
    to { transform: translateX(0); opacity:1; }
}
.slide-left { animation: slideInLeft 0.6s ease-out both; }

@keyframes slideInRight {
    from { transform: translateX(30px); opacity:0; }
    to { transform: translateX(0); opacity:1; }
}
.slide-right { animation: slideInRight 0.6s ease-out both; }

@keyframes pulseGlow {
    0%,100% { box-shadow: 0 0 0 0 rgba(0,217,255,0.4); }
    50%     { box-shadow: 0 0 0 10px rgba(0,217,255,0); }
}
.pulse { animation: pulseGlow 2s ease-in-out infinite; }

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.skeleton {
    background: linear-gradient(90deg, var(--surface) 25%, var(--surface-2) 50%, var(--surface) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 8px;
}

@keyframes typingBounce {
    0%,80%,100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-6px); opacity: 1; }
}
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

/* === Skeleton loader === */
.skeleton-card {
    height: 80px;
    margin-bottom: 12px;
}
.skeleton-line {
    height: 14px;
    margin-bottom: 8px;
    width: 100%;
}
.skeleton-line:nth-child(2) { width: 75%; }
.skeleton-line:nth-child(3) { width: 50%; }

/* === Language Switcher === */
.lang-switcher {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    border-radius: 8px;
    background: rgba(108,99,255,0.1);
    border: 1px solid var(--border);
    font-size: 12px;
    cursor: pointer;
    transition: all .2s;
}
.lang-switcher:hover {
    background: rgba(108,99,255,0.2);
}

/* === Responsive === */
@media (max-width: 1100px) {
    .aside-panel { display: none !important; }
}
@media (max-width: 720px) {
    [data-testid="stSidebar"] { display: none !important; }
    .main-content { padding: 0 8px !important; }
}

/* prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
    .stApp::before, .stApp::after { animation: none !important; }
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""


def apply_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# BRAND & HEADER
# ----------------------------------------------------------------------------
def render_brand():
    t = Translator()
    st.markdown(
        f"""
        <div class="slide-left" style="display:flex; align-items:center; gap:10px; padding:6px 8px; margin-bottom:8px;">
            <div class="brand-logo">🚀</div>
            <div>
                <div style="font-size:15px; font-weight:700; letter-spacing:0.3px;">{t('app.name')}</div>
                <div style="font-size:11px; color:var(--text-dim); margin-top:2px;">{t('app.tagline')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(active_page: str = "Chat", agent_label: str = "General Assistant", online: bool = True):
    t = Translator()
    status = f'<span class="status-online">{t("online")}</span>' if online else f'<span class="status-error">{t("offline")}</span>'
    lang = st.session_state.get("language", "fa")
    dir_attr = 'rtl' if lang == 'fa' else 'ltr'

    # Language switcher HTML
    other_lang = "en" if lang == "fa" else "fa"
    other_label = "🇬🇧 English" if lang == "fa" else "🇮🇷 فارسی"
    lang_switcher = f"""
        <div class="lang-switcher" onclick="document.getElementById('lang_switch_btn').click();"
             style="cursor:pointer; display:flex; align-items:center; gap:6px;
                    background:rgba(108,99,255,0.1); border:1px solid var(--border);
                    padding:6px 12px; border-radius:999px; font-size:12px;">
            {other_label} ▾
        </div>
    """

    left_section = f"""
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
    """

    right_section = f"""
        <div style="display:flex; align-items:center; gap:8px;">
            {lang_switcher}
        </div>
    """

    if dir_attr == "rtl":
        layout = f"{right_section}<div style='display:flex; align-items:center; gap:10px;'>{left_section}</div>"
    else:
        layout = f"<div style='display:flex; align-items:center; gap:10px;'>{left_section}</div>{right_section}"

    st.markdown(
        f"""
        <div class="fade-in" style="display:flex; align-items:center; justify-content:space-between;
                    padding:14px 4px; border-bottom:1px solid var(--border); margin-bottom:18px;">
            {layout}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hidden button for language switch
    if st.button(other_label, key="lang_switch_btn", help=t("language")):
        st.session_state["language"] = other_lang
        st.rerun()


# ----------------------------------------------------------------------------
# AGENT META
# ----------------------------------------------------------------------------
AGENT_META = {
    "coding":    {"icon": "💻", "desc_key": "agents.coding"},
    "writing":   {"icon": "✍️", "desc_key": "agents.writing"},
    "data":      {"icon": "📊", "desc_key": "agents.data"},
    "design":    {"icon": "🎨", "desc_key": "agents.design"},
    "marketing": {"icon": "📈", "desc_key": "agents.marketing"},
    "research":  {"icon": "🔍", "desc_key": "agents.research"},
    "summarizer":{"icon": "📝", "desc_key": "agents.summarizer"},
    "tutor":     {"icon": "🎓", "desc_key": "agents.tutor"},
}


def render_session_card(user_name: str = "Habibur Rahman", tier: str = "Free"):
    t = Translator()
    user = st.session_state.get("user", None)
    if user:
        name = user.get("name", user_name)
        email = user.get("email", "")
        picture = user.get("picture", "")
        is_admin = user.get("is_admin", False)
        tier_label = "Admin" if is_admin else t("free_tier")

        if picture:
            avatar_html = f'<img src="{picture}" style="width:36px; height:36px; border-radius:50%; object-fit:cover;" />'
        else:
            initials = "".join([p[0] for p in name.split()[:2]]).upper() or "U"
            avatar_html = f'<div style="width:36px; height:36px; border-radius:50%; background:var(--gradient-brand); display:grid; place-items:center; font-weight:700; color:#fff; font-size:13px;">{initials}</div>'
    else:
        avatar_html = f'<div style="width:36px; height:36px; border-radius:50%; background:var(--gradient-brand); display:grid; place-items:center; font-weight:700; color:#fff; font-size:13px;">?</div>'
        name = t("auth.login_guest")
        tier_label = ""

    st.markdown(
        f"""
        <div class="glass-card fade-in" style="display:flex; align-items:center; gap:10px; margin-top:18px;">
            {avatar_html}
            <div>
                <div style="font-size:13px; font-weight:600;">{name}</div>
                <div style="font-size:11px; color:var(--text-dim);">{tier_label}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# ASIDE PANELS
# ----------------------------------------------------------------------------
def render_aside_provider(providers: list):
    t = Translator()
    rows = ""
    for p in providers[:5]:
        rows += f'<div class="kv"><span>{p.get("role", t("provider.primary"))}</span><b>{p.get("name", "—")}</b></div>'
    st.markdown(
        f"""
        <div class="glass-card fade-in aside-panel">
            <h3 style="margin:0 0 10px; font-size:13px; display:flex; align-items:center; gap:8px;">
                <span>📡</span> {t('provider.title')}
            </h3>
            {rows}
            <div class="kv"><span>{t('provider.status')}</span><b class="status-online">{t('provider.healthy')}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_aside_chain(tasks: list):
    t = Translator()
    if not tasks:
        body = f'<div style="font-size:12px; color:var(--text-mute);">{t("chain.empty")}</div>'
    else:
        body = ""
        for i, tk in enumerate(tasks, 1):
            label = tk.get("agent", "agent")
            desc = tk.get("prompt", "")[:60]
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
        <div class="glass-card fade-in aside-panel">
            <h3 style="margin:0 0 10px; font-size:13px; display:flex; align-items:center; gap:8px;">
                <span>⛓️</span> {t('chain.title')}
            </h3>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_aside_memory(items: list):
    t = Translator()
    if not items:
        body = f'<div style="font-size:12px; color:var(--text-mute);">{t("memory.empty")}</div>'
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
        <div class="glass-card fade-in aside-panel">
            <h3 style="margin:0 0 10px; font-size:13px; display:flex; align-items:center; gap:8px;">
                <span>🧠</span> {t('memory.title')}
            </h3>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_aside_stats(stats: dict):
    t = Translator()
    rows = ""
    for k, v in stats.items():
        rows += f'<div class="kv"><span>{k}</span><b>{v}</b></div>'
    st.markdown(
        f"""
        <div class="glass-card fade-in aside-panel">
            <h3 style="margin:0 0 10px; font-size:13px; display:flex; align-items:center; gap:8px;">
                <span>📊</span> {t('stats.title')}
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
    t = Translator()
    st.markdown(
        f"""
        <div class="fade-in" style="text-align:center; padding:36px 8px 8px;">
            <h1 style="font-size:32px; margin:0; font-weight:800;
                       background:var(--gradient-brand); -webkit-background-clip:text; background-clip:text; color:transparent;
                       letter-spacing:-0.5px;">
                {t('chat.welcome_title')}
            </h1>
            <p style="color:var(--text-dim); margin:8px 0 0; font-size:14px;">
                {t('chat.welcome_desc')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_starts(options: list):
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
# AUTH UI
# ----------------------------------------------------------------------------
def render_login_page():
    t = Translator()
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; align-items:center; min-height:80vh;">
            <div class="glass-card" style="max-width:420px; width:100%; padding:40px; text-align:center;">
                <div class="brand-logo" style="margin:0 auto 20px;">🚀</div>
                <h2 style="margin:0 0 8px; font-size:24px;">{t('auth.login_title')}</h2>
                <p style="color:var(--text-dim); font-size:14px; margin:0 0 28px;">{t('auth.login_desc')}</p>
                <div style="display:flex; flex-direction:column; gap:12px;">
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚪 " + t('auth.login_guest'), use_container_width=True):
            st.session_state["user"] = {"name": "Guest", "role": "guest"}
            st.rerun()
    with col2:
        if st.button("🔵 " + t('auth.login_google'), use_container_width=True):
            from auth.google_auth import GoogleAuth
            ga = GoogleAuth()
            if ga.is_configured:
                login_url = ga.get_login_url()
                st.markdown(f'<meta http-equiv="refresh" content="0; url={login_url}">', unsafe_allow_html=True)
            else:
                st.session_state["user"] = {
                    "name": "Demo User",
                    "email": "demo@yonocytech.ir",
                    "is_admin": True,
                }
                st.rerun()

    st.markdown("</div></div></div>", unsafe_allow_html=True)


def render_skeleton_loader(count: int = 3):
    for _ in range(count):
        st.markdown(
            """
            <div class="glass-card skeleton-card">
                <div class="skeleton skeleton-line"></div>
                <div class="skeleton skeleton-line"></div>
                <div class="skeleton skeleton-line"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ----------------------------------------------------------------------------
# LEGACY
# ----------------------------------------------------------------------------
def render_agent_badge(agent_name: str):
    st.markdown(f'<span class="agent-tag">{agent_name}</span>', unsafe_allow_html=True)


def render_response_metadata(response: AgentResponse):
    with st.expander("View Response Metadata"):
        col1, col2, col3 = st.columns(3)
        col1.text(f"Provider: {response.provider}")
        col2.text(f"Model: {response.model}")
        col3.text(f"Latency: {int(response.latency_ms)}ms")
        if getattr(response, "tokens_used", None):
            st.text(f"Tokens Used: {response.tokens_used}")

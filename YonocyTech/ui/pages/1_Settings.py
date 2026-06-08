import os
import streamlit as st
from core import YonocyTech
from i18n.translator import Translator

def main():
    t = Translator()

    st.title("⚙️ " + t("settings.title"))

    if "agent" not in st.session_state:
        st.error("Agent not initialized. Please return to the main app.")
        return

    agent = st.session_state.agent

    # Account section
    st.markdown("### 👤 Account")
    user = st.session_state.get("user")
    if user:
        st.success(f"✅ Logged in as **{user.get('name', 'User')}** ({user.get('email', '')})")
        if user.get("is_admin"):
            st.markdown(
                '<span style="background:var(--gradient-brand); padding:2px 10px; '
                'border-radius:999px; font-size:12px; color:#fff;">👑 Admin</span>',
                unsafe_allow_html=True,
            )
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.rerun()
    else:
        st.warning("🔒 Not logged in")
        if st.button("🔵 Login with Google"):
            st.session_state.current_page = "Chat"
            st.rerun()

    st.markdown("---")

    # API Status
    st.markdown("### 🔑 " + t("settings.api_status"))
    providers = agent.providers
    if not providers:
        st.warning(t("error.no_providers"))
    else:
        for p in providers:
            st.success(f"✅ {p.__class__.__name__} is Active")

    # Ollama status
    try:
        from integrations.ollama_provider import OllamaProvider
        op = OllamaProvider()
        if op.is_available:
            st.success(f"✅ Ollama ({op.model}) is available")
        else:
            st.info("⏸️ Ollama not detected. Install Ollama and pull a model for local Persian AI.")
    except Exception:
        st.info("⏸️ Ollama check skipped")

    st.markdown("---")
    st.markdown("### 🛡️ " + t("settings.security"))
    st.info(t("settings.security_desc"))

    st.markdown("---")
    st.markdown("### 🧠 " + t("settings.memory_stats"))
    try:
        size = os.path.getsize("memory/data/conversations.json") / 1024
        st.write(f"Conversation Log Size: {size:.2f} KB")
    except Exception:
        st.write("Log size unavailable.")

    if st.button("🗑️ " + t("settings.clear_memory")):
        with open("memory/data/conversations.json", "w") as f:
            f.write("{}")
        st.success(t("settings.memory_cleared"))
        st.rerun()

if __name__ == "__main__":
    main()

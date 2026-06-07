import streamlit as st
from core import YonocyTech

def main():
    st.title("⚙️ System Settings")

    if "agent" not in st.session_state:
        st.error("Agent not initialized. Please return to the main app.")
        return

    agent = st.session_state.agent

    st.markdown("### 🔑 API Status")
    providers = agent.providers
    if not providers:
        st.warning("No providers available. Check your .env file.")
    else:
        for p in providers:
            st.success(f"✅ {p.__class__.__name__} is Active")

    st.markdown("---")
    st.markdown("### 🛡️ Security Center")
    st.info("Active Guards: Prompt Injection Detection, Dangerous Code Regex, Rate Limiting (30 req/min).")

    st.markdown("---")
    st.markdown("### 🧠 Memory Statistics")
    # Since MemoryStore is JSON, we can check file size
    try:
        import os
        size = os.path.getsize("memory/data/conversations.json") / 1024
        st.write(f"Conversation Log Size: {size:.2f} KB")
    except Exception:
        st.write("Log size unavailable.")

    if st.button("Clear All Memory"):
        # Clear the JSON file
        with open("memory/data/conversations.json", "w") as f:
            f.write("{}")
        st.success("Memory cleared successfully!")
        st.rerun()

if __name__ == "__main__":
    main()

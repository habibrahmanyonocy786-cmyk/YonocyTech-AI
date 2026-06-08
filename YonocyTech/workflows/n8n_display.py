"""
Display pre-built N8N workflow templates.
In production, this could fetch from an N8N instance API.
"""
import streamlit as st


N8N_WORKFLOWS = [
    {
        "name": "AI Content Generator",
        "description": "Automatically generate blog posts using AI and publish to WordPress",
        "steps": [
            "🔍 RSS Feed Trigger → New post detected",
            "🤖 OpenAI Node → Generate article from topic",
            "✍️ Edit Content → Human-in-the-loop approval",
            "📤 WordPress → Publish as draft",
            "📧 Telegram → Notify admin",
        ],
        "icon": "🤖",
        "nodes": 5,
    },
    {
        "name": "Social Media Monitor",
        "description": "Monitor brand mentions and auto-respond on social media",
        "steps": [
            "🐦 Twitter Webhook → New mention detected",
            "🧠 AI Classifier → Positive/negative/neutral",
            "📨 If negative → Slack alert to support team",
            "💬 If positive → Auto-reply with thank you",
            "📊 Google Sheets → Log all mentions",
        ],
        "icon": "📡",
        "nodes": 6,
    },
    {
        "name": "Customer Support Pipeline",
        "description": "Route and respond to support tickets automatically",
        "steps": [
            "📧 Email Trigger → New support ticket",
            "🤖 AI Router → Categorize (billing/tech/general)",
            "👤 If billing → Forward to Stripe node",
            "🔧 If technical → Search knowledge base + suggest solution",
            "📋 Asana → Create task if unresolved",
            "📱 WhatsApp → Send status update to customer",
        ],
        "icon": "🎫",
        "nodes": 7,
    },
    {
        "name": "Data Sync & Backup",
        "description": "Synchronize data between Google Sheets, Database, and Slack",
        "steps": [
            "⏰ Schedule Trigger → Every 6 hours",
            "📊 Google Sheets → Read new rows",
            "🗄️ PostgreSQL → Upsert data",
            "📈 Generate summary report",
            "📤 Slack → Post summary to team channel",
            "🗑️ Archive processed rows",
        ],
        "icon": "🔄",
        "nodes": 6,
    },
]


def render_n8n_workflows():
    from i18n.translator import Translator
    t = Translator()

    st.markdown(
        f"<h2 style='margin:6px 0 4px; font-size:20px;'>{t('n8n.title')}</h2>"
        f"<p style='color:var(--text-dim); font-size:13px; margin:0 0 16px;'>{t('n8n.desc')}</p>",
        unsafe_allow_html=True,
    )

    for wf in N8N_WORKFLOWS:
        with st.container():
            st.markdown(
                f"""
                <div class="glass-card fade-in" style="margin-bottom:16px;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                        <span style="font-size:28px;">{wf['icon']}</span>
                        <div>
                            <div style="font-size:16px; font-weight:700;">{wf['name']}</div>
                            <div style="font-size:12px; color:var(--text-dim);">{wf['description']}</div>
                        </div>
                        <span style="margin-left:auto; background:var(--surface); padding:4px 10px;
                                   border-radius:999px; font-size:11px; color:var(--text-dim);">
                            {wf['nodes']} nodes
                        </span>
                    </div>
                    <div style="background:rgba(0,0,0,0.2); border-radius:10px; padding:12px;">
                """,
                unsafe_allow_html=True,
            )
            for step in wf["steps"]:
                st.markdown(
                    f'<div style="padding:4px 0; font-size:12.5px; color:var(--text); '
                    f'border-bottom:1px dashed rgba(255,255,255,0.05);">{step}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

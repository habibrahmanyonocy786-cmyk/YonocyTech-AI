import streamlit as st
from i18n.translator import Translator


def render_admin_page():
    t = Translator()
    admin = st.session_state.admin
    summary = admin.get_summary()

    st.markdown(
        f"<h2 style='margin:6px 0 4px; font-size:22px;'>{t('admin.title')}</h2>"
        f"<p style='color:var(--text-dim); font-size:13px; margin:0 0 20px;'>{t('admin.usage_desc')}</p>",
        unsafe_allow_html=True,
    )

    # Top metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t("admin.total_tokens"), f"{summary['total_tokens']:,}")
    m2.metric(t("admin.total_requests"), f"{summary['total_requests']:,}")
    m3.metric(t("admin.requests_today"), summary["requests_today"])
    m4.metric(t("admin.tokens_today"), f"{summary['tokens_today']:,}")

    st.markdown("---")

    # Provider health
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"<h3 style='font-size:16px; margin:0 0 12px;'>{t('admin.provider_health')}</h3>",
            unsafe_allow_html=True,
        )
        providers = admin.stats.get("requests_by_provider", {})
        if providers:
            for p_name, p_count in providers.items():
                p_tokens = admin.stats.get("tokens_by_provider", {}).get(p_name, 0)
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding:12px; margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <div style="font-weight:600; font-size:13px;">{p_name}</div>
                                <div style="font-size:11px; color:var(--text-dim);">
                                    {p_count} requests · {p_tokens:,} tokens
                                </div>
                            </div>
                            <span class="status-online">● {'Healthy' if p_count > 0 else 'Idle'}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No provider data yet.")

    with col2:
        st.markdown(
            f"<h3 style='font-size:16px; margin:0 0 12px;'>{t('admin.active_providers')}</h3>",
            unsafe_allow_html=True,
        )
        for p in st.session_state.agent.providers:
            st.markdown(
                f"""
                <div class="glass-card" style="padding:12px; margin-bottom:8px;
                            display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:13px; font-weight:500;">{p.__class__.__name__}</span>
                    <span class="status-online">● Active</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Top users
    st.markdown("---")
    st.markdown(
        "<h3 style='font-size:16px; margin:0 0 12px;'>👥 Top Users</h3>",
        unsafe_allow_html=True,
    )
    top_users = summary.get("top_users", {})
    if top_users:
        for u_name, u_count in list(top_users.items())[:5]:
            u_tokens = admin.stats.get("tokens_by_user", {}).get(u_name, 0)
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; padding:8px 12px;
                            border-bottom:1px solid var(--border); font-size:13px;">
                    <span>{u_name}</span>
                    <span style="color:var(--text-dim);">{u_count} req · {u_tokens:,} tok</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No user data yet.")

    # Controls
    st.markdown("---")
    if st.button(f"🗑️ {t('admin.reset_stats')}", use_container_width=True):
        admin.reset()
        st.success("Stats reset!")
        st.rerun()

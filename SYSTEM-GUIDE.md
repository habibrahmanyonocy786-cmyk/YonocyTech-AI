# YonocyTech System Guide — راهنمای کامل سیستم

**Developer:** Habib Rahman Yonocy (حبیب رحمان یونسی)
**Version:** 2.0 | **Last Update:** June 2026

---

## 1. SYSTEM OVERVIEW — نمای کلی

```
┌─────────────────────────────────────────────────────────┐
│                    YonocyTech System                      │
├──────────────────┬──────────────────┬────────────────────┤
│   Marketing Site  │   AI Platform     │   Database          │
│   (GitHub Pages)  │   (Streamlit)     │   (SQLite)          │
│                   │                   │                    │
│   index.html      │   core.py         │   users            │
│   services.html   │   agents/         │   sessions         │
│   pricing.html    │   tools/          │   messages         │
│   about.html      │   security/       │   providers        │
│   contact.html    │   memory/         │   agents           │
│   login.html      │   ui/             │   contact_msgs     │
│   dashboard.html  │                   │   usage_logs       │
│   admin.html      │                   │   settings         │
└──────────────────┴──────────────────┴────────────────────┘
```

---

## 2. FILE STRUCTURE — ساختار فایل‌ها

```
📁 YonocyTech/
├── 📄 core.py                    # Main AI engine + auth + provider fallback
├── 📄 requirements.txt           # Python dependencies
├── 📄 packages.txt               # Streamlit Cloud packages
│
├── 📁 agents/                    # Specialized AI agents
│   ├── __init__.py               # Agent registry (ALL_AGENTS)
│   ├── base_agent.py             # Abstract base class
│   ├── coding_agent.py           # 💻 Code generation + sandbox
│   ├── writing_agent.py          # ✍️ Content writing
│   ├── data_agent.py             # 📊 CSV/Excel analysis
│   ├── design_agent.py           # 🎨 UI/UX design specs
│   ├── marketing_agent.py        # 📈 SEO & growth
│   └── research_agent.py         # 🔍 Web research + citations
│
├── 📁 database/                  # SQLite database layer
│   ├── __init__.py               # DB connection manager
│   ├── schema.py                 # 8 tables + migrations + seed
│   └── models.py                 # Full CRUD operations
│
├── 📁 memory/                    # Memory systems
│   ├── __init__.py
│   ├── vector_store.py           # ChromaDB vector storage
│   └── semantic_recall.py        # Hybrid recall (JSON + Vector)
│
├── 📁 security/                  # Security layer
│   ├── __init__.py
│   └── guard.py                  # Injection detection, sandbox, rate limiter
│
├── 📁 tools/                     # Utility tools
│   ├── __init__.py
│   ├── orchestrator.py           # Multi-agent chain orchestration
│   ├── file_manager.py           # Secure file operations
│   ├── file_processor.py         # PDF/DOCX/Excel/CSV reader
│   ├── image_gen.py              # Pollinations.ai + DeepAI
│   ├── voice_input.py            # Web Speech API component
│   └── web_search.py             # DuckDuckGo search
│
├── 📁 ui/                        # Streamlit frontend
│   ├── __init__.py
│   ├── streamlit_app.py          # Main app with auth + admin panel
│   ├── components.py             # UI design system (dark space theme)
│   └── pages/
│       └── 1_Settings.py         # Legacy settings (Admin panel in main app)
│
├── 📁 config/
│   └── .env.example              # API key template
│
├── 📁 .streamlit/
│   └── secrets.toml.example      # Streamlit Cloud secrets template
│
├── 📁 tests/                     # Test suite
│   ├── test_core.py
│   ├── test_agents.py
│   ├── test_security.py
│   ├── test_vector_memory.py
│   ├── test_advanced.py
│   └── test_database.py          # Database integration tests
│
├── 📁 docs/
│   ├── ui-spec.md                # UI design specification
│   ├── ui-mockup.html            # Interactive UI prototype
│   └── monetization.md           # Monetization strategy
│
└── 📁 .github/workflows/
    └── test.yml                  # CI pipeline

📁 Root (Marketing Site)
├── 📄 index.html                 # Main landing page
├── 📄 services.html              # Services detail page
├── 📄 pricing.html               # Pricing (Free/Pro/Enterprise)
├── 📄 about.html                 # About developer
├── 📄 contact.html               # Contact form
├── 📄 login.html                 # Auth (login/register)
├── 📄 dashboard.html             # User dashboard
├── 📄 admin.html                 # Admin panel (model/agent/user mgmt)
├── 📄 README.md                  # Main documentation
├── 📄 SYSTEM-GUIDE.md            # This guide
├── 📄 requirements.txt           # Root dependencies
│
├── 📁 assets/
│   ├── css/style.css             # Full design system (dark space)
│   ├── js/main.js                # Core JS + animations
│   ├── js/auth.js                # Authentication logic
│   ├── js/admin.js               # Admin panel logic
│   └── images/social-preview.svg # OG social image
│
└── 📁 .streamlit/
    └── config.toml               # Streamlit config
```

---

## 3. DATABASE SCHEMA — دیتابیس

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `users` | User accounts + roles | id, name, email, password, role, plan |
| `sessions` | Chat sessions | id, user_id, title, focus |
| `messages` | Conversation history | id, session_id, role, content, tokens_used |
| `providers` | LLM model config | id, name, status (active/limited/off), rate_limit |
| `agents` | AI agent config | id, name, icon, status, default_provider |
| `contact_messages` | Contact form data | id, name, email, subject, message, is_read |
| `usage_logs` | API usage tracking | id, user_id, provider_id, tokens_used, latency |
| `settings` | System settings | key, value |

**Default data seeded on first run:**
- 4 Providers: OpenRouter, HuggingFace, GitHub Models, DeepAI
- 6 Agents: Coding, Writing, Data, Design, Marketing, Research
- 8 System settings (site_name, version, etc.)

---

## 4. AUTH SYSTEM — احراز هویت

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Static   │     │ Streamlit│     │ SQLite   │
│  Site     │────▶│  App     │────▶│ DB       │
│(localSt.) │     │(session) │     │(persist) │
└──────────┘     └──────────┘     └──────────┘
```

**Static Site (HTML):**
- Login/Register via `auth.js`
- Session stored in `localStorage` (`yonocytech_session`)
- First user → role=admin (auto-detected)
- Protected routes: `dashboard.html`, `admin.html`

**Streamlit App:**
- Login/Register via SQLite `database/models.py`
- Session in `st.session_state`
- Admin panel for provider/agent management
- Usage logging per request

---

## 5. ADMIN CONTROLS — کنترل مدیر

| Feature | Location | Description |
|---------|----------|-------------|
| LLM Provider Management | Admin Panel → Providers | Enable/disable/limit each model |
| Agent Management | Admin Panel → Agents | Control 6 agent statuses |
| User Management | Admin Panel → Users | View all registered users |
| Contact Messages | Admin Panel → Contact | Read user inquiries |
| System Settings | Admin Panel → Settings | Configure system parameters |
| Usage Stats | Overview tab | Total requests, tokens, latency |

**Provider statuses:** `active` (green) → `limited` (yellow) → `off` (red)

---

## 6. API PROVIDERS — سرویس‌های AI

| Provider | Type | Cost | Fallback Priority |
|----------|------|------|-------------------|
| **OpenRouter** | Chat Completion | Free | 1 (Primary) |
| **HuggingFace** | Inference API | Free | 2 |
| **GitHub Models** | Azure AI | Free | 3 |
| **DeepAI** | Image Generation | Free | 4 |

**Fallback Chain:** If Provider 1 fails → automatically tries Provider 2 → then 3

---

## 7. SECURITY — امنیت

| Layer | Protection |
|-------|-----------|
| Prompt Injection | 25+ regex patterns detected |
| Dangerous Code | 15+ patterns blocked |
| Sandbox Execution | Isolated subprocess with timeout |
| Rate Limiting | Sliding window (30 req/min default) |
| Password | SHA-256 hashing (stored in DB) |
| File Safety | Extension whitelist + code scan |

---

## 8. DEPLOYMENT — استقرار

### GitHub Pages (Marketing Site)
```
Settings → Pages → Deploy from branch → master → / (root) → Save
URL: https://habibrahmanyonocy786-cmyk.github.io/YonocyTech-AI/
```

### Streamlit Cloud (AI Platform)
```
1. Go to share.streamlit.io
2. Connect repo: habibrahmanyonocy786-cmyk/YonocyTech-AI
3. Main file: YonocyTech/ui/streamlit_app.py
4. Add Secrets (API keys):
   - OPENROUTER_API_KEY
   - HF_API_KEY
   - GITHUB_TOKEN
   - DEEPAI_API_KEY
5. Deploy
URL: https://yonocytech-ai.streamlit.app
```

### Local Development
```bash
# AI Platform
cd YonocyTech
pip install -r requirements.txt
streamlit run ui/streamlit_app.py

# Marketing Site
python -m http.server 3000
# Open: http://localhost:3000
```

---

## 9. TESTING — تست

```bash
cd YonocyTech
pytest tests/ --tb=short
```

| Test File | Coverage |
|-----------|----------|
| test_core.py | Core engine, providers |
| test_agents.py | Agent functionalities |
| test_security.py | Injection detection, sandbox |
| test_vector_memory.py | ChromaDB operations |
| test_advanced.py | Integration tests |
| test_database.py | Database CRUD operations |

---

## 10. KEY CONFIGURATIONS — تنظیمات کلیدی

### Environment Variables (YonocyTech/config/.env)
```env
OPENROUTER_API_KEY=your_key          # Primary AI provider
HF_API_KEY=your_key                  # Fallback AI provider
GITHUB_TOKEN=your_token              # GitHub Models (Azure)
DEEPAI_API_KEY=your_key              # Image generation
```

### System Settings (via Admin Panel)
```json
{
  "site_name": "YonocyTech",
  "site_version": "2.0",
  "default_rate_limit": "30",
  "max_session_messages": "50",
  "allow_registration": "1",
  "maintenance_mode": "0"
}
```

---

## 11. PAGES OVERVIEW — صفحات

| Page | File | Purpose | Auth Required |
|------|------|---------|:---:|
| 🏠 Home | `index.html` | Landing + hero + features | ❌ |
| 📋 Services | `services.html` | AI, Web Dev, Database | ❌ |
| 💰 Pricing | `pricing.html` | Free/Pro/Enterprise | ❌ |
| 👤 About | `about.html` | Developer info + skills | ❌ |
| 📞 Contact | `contact.html` | Form + social links | ❌ |
| 🔑 Login | `login.html` | Sign in / Register | ❌ |
| 📊 Dashboard | `dashboard.html` | User control panel | ✅ |
| 🔐 Admin | `admin.html` | System management | ✅ (admin) |

---

## 12. CONTACT — تماس

```
Developer:  Habib Rahman Yonocy (حبیب رحمان یونسی)
Phone:      0093 784 258 414
Email:      habibrahmanyonocy786@gmail.com
GitHub:     github.com/habibrahmanyonocy786-cmyk
```

---

*Generated on June 7, 2026 — YonocyTech System Guide v1.0*

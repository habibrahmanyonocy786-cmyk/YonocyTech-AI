# YonocyTech — AI · Web · Database Solutions

**Developer:** Habib Rahman Yonocy (حبیب رحمان یونسی)

Professional AI agent platform, web development, and database management services.

---

## 🌐 Website

The YonocyTech marketing website is deployed on **GitHub Pages**:
- **URL:** `https://habibrahmanyonocy786-cmyk.github.io/YonocyTech-AI/`

### Pages

| Page | Description |
|------|-------------|
| `index.html` | Main landing page with hero, features, services overview, AI agents showcase |
| `services.html` | Detailed AI platform, web development, and database services |
| `pricing.html` | Free, Pro ($9/mo), and Enterprise ($29/mo) pricing tiers |
| `about.html` | About Habib Rahman Yonocy and the YonocyTech vision |
| `contact.html` | Contact form and social links |
| `login.html` | User login and registration with admin auto-detection |
| `dashboard.html` | User dashboard with AI agent access, sessions, memory explorer |
| `admin.html` | Admin panel for LLM provider management, agent control, user management |

### Features

- **Authentication**: LocalStorage-based user system. First user automatically becomes admin.
- **Admin Controls**: Enable/disable/limit each LLM provider (OpenRouter, HuggingFace, GitHub Models, DeepAI)
- **Agent Management**: Control status of 6 specialized AI agents
- **User Management**: View all registered users and their plans
- **Zero Budget**: Fully hosted on GitHub Pages (free) and Streamlit Cloud (free for the AI app)

---

## 🤖 AI Platform (Streamlit App)

The YonocyTech AI Agent runs on Streamlit Cloud:
- **URL:** `https://yonocytech-ai.streamlit.app`

### Architecture

```
User → Security Guard → Orchestrator → Specialized Agent → LLM Provider (Fallback Chain) → Memory Store
```

### AI Agents

| Agent | Focus |
|-------|-------|
| 💻 Coding | Code generation and sandbox execution |
| ✍️ Writing | Professional and creative content |
| 📊 Data | CSV/Excel analysis with pandas |
| 🎨 Design | UI/UX specifications |
| 📈 Marketing | SEO and growth strategies |
| 🔍 Research | Deep web research with citations |

### LLM Providers (Fallback Chain)

1. **OpenRouter** (Primary) — Free tier models
2. **HuggingFace Inference** — Free API
3. **GitHub Models** — Azure AI Inference

### Security

- Prompt Injection Detection (25+ patterns)
- Dangerous Code Detection (15+ patterns)
- Restricted Sandbox Execution
- Per-user Rate Limiting (30 req/min)

### Memory

- **JSON Store**: Conversation history (last 50 messages per session)
- **ChromaDB Vector Store**: Semantic search across conversation pairs

---

## 🛠️ Local Development

### Website (Static)

```bash
# Just open any HTML file in a browser
open index.html
```

### AI Agent

```bash
cd YonocyTech

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp config/.env.example config/.env
# Add your API keys to config/.env

# CLI Mode
python core.py

# Web UI Mode
streamlit run ui/streamlit_app.py

# Run Tests
pytest tests/ --tb=short
```

---

## 🚀 Deployment

### GitHub Pages (Marketing Website)

1. Go to **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: **main**, folder: **/ (root)**
4. Site will be live at: `https://habibrahmanyonocy786-cmyk.github.io/YonocyTech-AI/`

### Streamlit Cloud (AI Platform)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set the main file path: `YonocyTech/ui/streamlit_app.py`
5. Add secrets (API keys) in the Streamlit Cloud dashboard

---

## 📄 License

MIT License — See the `YonocyTech/` directory for full details.

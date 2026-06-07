# 🚀 YonocyTech AI Agent v2.0

**Developer:** Habibur Rahman Younesi (حبیب الرحمن یونسی)  
**Goal:** High-performance, zero-budget AI agent for software engineering, content creation, and data analysis.

## 🌟 Features
- **Zero Budget Architecture**: Leverages free tiers of OpenRouter, HuggingFace, and GitHub Models.
- **Provider Fallback Chain**: Automatically switches models if a provider hits a rate limit or fails.
- **Security-First Design**: 
  - Prompt Injection Guards (25+ patterns).
  - Dangerous Code Detection (15+ patterns).
  - Restricted Sandbox Execution.
  - Per-user Rate Limiting.
- **Specialized Agent Personas**:
  - 💻 **Coding**: Code generation and sandbox execution.
  - ✍️ **Writing**: Professional and creative content enhancement.
  - 📊 **Data**: CSV/Excel analysis via pandas.
  - 🎨 **Design**: UI/UX specifications and accessibility.
  - 📈 **Marketing**: SEO and Growth Hacking strategies.
  - 🔍 **Research**: Deep web research with automated citations.
- **Hybrid Memory**: Combines a JSON conversation log with a ChromaDB vector store for semantic long-term recall.
- **Modern Interface**: Dark Space themed Streamlit UI.

## 🛠️ Quick Start

### 1. Setup
```bash
# Clone the repo
git clone https://github.com/your-username/YonocyTech-AI.git
cd YonocyTech-AI

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Copy `.env.example` to `.env` and add your free API keys:
```env
OPENROUTER_API_KEY=your_key
HF_API_KEY=your_key
GITHUB_TOKEN=your_key
```

### 3. Run the Agent
**CLI Mode:**
```bash
python core.py
```

**Web UI Mode:**
```bash
streamlit run ui/streamlit_app.py
```

## 📐 Architecture
`User` $\rightarrow$ `Security Guard` $\rightarrow$ `Orchestrator` $\rightarrow$ `Specialized Agent` $\rightarrow$ `LLM Provider (Fallback Chain)` $\rightarrow$ `Memory Store`

## 📦 Project Structure
- `core.py`: Main engine and provider logic.
- `agents/`: Persona-specific implementations.
- `tools/`: Web search, file processing, and orchestration.
- `security/`: Guardrails and sandboxing.
- `memory/`: JSON and Vector storage.
- `ui/`: Streamlit frontend.
- `tests/`: Mocked verification suite.

## 💰 Monetization
See `docs/monetization.md` for the detailed global market strategy.

## 📜 License
MIT License

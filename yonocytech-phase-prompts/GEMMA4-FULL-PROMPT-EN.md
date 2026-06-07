# YonocyTech AI Agent — Complete Prompt for Gemma 4 31B Cloud

> Developer: Habibur Rahman Younesi (حبیب الرحمن یونسی)
> Final Goal: Build a complete AI Agent that can generate monthly income after completion — $0 budget, runs on a single laptop: Dell Latitude E5440 (Core i5, 8GB RAM, GT 720M, Windows 10).

---

You are a senior Python developer and DevOps engineer. You must generate the entire YonocyTech AI Agent project in one pass — from core engine to deployment and monetization features.

## System Specs:
- Laptop: Dell Latitude E5440 | CPU: Core i5-4310U (2C/4T) | RAM: 8GB DDR3 | GPU: GT 720M (2GB) | HDD: 500GB (250GB free) | OS: Windows 10
- Python 3.14+, Node v24, Git, winget, npm
- Path: C:\Users\habib\Desktop\1234\YonocyTech\

## Budget:
$0 — only free tools and services. No paid API allowed.

## Model Constraints:
- Target model: Gemma 4 31B Cloud — strong open-source model
- Output must be complete, executable, error-free
- Code must be compatible with Python 3.14
- Everything must run on low-resource hardware (8GB RAM, HDD)

## IMPORTANT: Language Rules
- Generate ALL code in English (variable names, comments, docstrings, strings, user-facing messages)
- NO Persian/Farsi text in any generated file
- Persian detection patterns in security/guard.py must use English equivalents (e.g., "ignore all previous instructions" instead of "دستورات قبلی را نادیده بگیر")
- Error messages must be in English only
- System prompts for agents must be in English only
- CLI interface text must be in English only
- README.md and docs must be in English only
- Monetization strategy should target global market, not Iran-specific

---

## Required — Generate ALL files below:

### 1. Project Directory Structure
PowerShell command:
```
mkdir -Force YonocyTech/{config,agents,tools,ui/pages,memory/data,security,tests,docs,.github/workflows,.streamlit}
```

### 2. config/.env.example
With OPENROUTER_API_KEY, HF_API_KEY, GITHUB_TOKEN placeholders — all free tiers.

### 3. .gitignore
Comprehensive: .env, venv, __pycache__, memory/data, chroma_data, .streamlit/secrets.toml

### 4. requirements.txt
Free libraries: streamlit>=1.31.0, httpx>=0.26.0, python-dotenv>=1.0.0, chromadb>=0.4.0, pandas>=2.1.0, matplotlib>=3.8.0, pillow>=10.0.0, pypdf>=4.0.0, python-docx>=1.0.0, openpyxl>=3.1.0, duckduckgo-search>=6.0.0, beautifulsoup4>=4.12.0, requests>=2.31.0, feedparser>=6.0.0, pytest>=8.0.0

### 5. core.py — Core AI Engine with Fallback Chain

Generate the following classes with full type hints and docstrings (English only):

#### AgentResponse (dataclass):
text: str, model: str, provider: str, tokens_used: int = 0, latency_ms: float = 0.0, timestamp: str (auto-generated with datetime.now().isoformat())

#### SessionMessage (dataclass):
role: str (user/assistant/system), content: str, focus: Optional[str] = None, timestamp: str (auto)

#### OpenRouterProvider:
- __init__: read OPENROUTER_API_KEY and model from env. Default model: "mistralai/mistral-7b-instruct:free"
- is_available (property): bool(self.api_key)
- async ask(messages, max_tokens=1024) -> AgentResponse:
  - Measure time with time.time()
  - httpx.AsyncClient timeout=60
  - POST to https://openrouter.ai/api/v1/v1/chat/completions
  - Headers: Authorization (Bearer), HTTP-Referer (http://localhost:8501), X-Title (YonocyTech)
  - Body: model, messages, max_tokens, temperature=0.7
  - Parse and return AgentResponse with real values

#### HuggingFaceProvider:
- __init__: read HF_API_KEY and model from env. Default: "mistralai/Mistral-7B-Instruct-v0.3"
- async ask(messages, max_tokens=1024) -> AgentResponse:
  - Extract system and user messages
  - Format: <s>[INST] {system}\n\n{user} [/INST]
  - POST to https://api-inference.huggingface.co/models/{model}
  - Return AgentResponse

#### GitHubModelsProvider:
- __init__: read GITHUB_TOKEN from env. Model: "gpt-4o-mini"
- async ask(messages, max_tokens=1024) -> AgentResponse:
  - POST to https://models.inference.ai.azure.com/chat/completions
  - Return AgentResponse

#### MemoryStore (JSON persistence):
- __init__(data_dir=None): create memory/data/ if not exists. Load conversations.json
- _load(): read JSON, convert to list of SessionMessage
- _save(): write JSON with ensure_ascii=False, indent=2
- new_session() -> str: sha256 hash of timestamp, first 12 chars
- add_message(session_id, role, content, focus=None): append SessionMessage, crop to last 50, save
- get_history(session_id, limit=20) -> list: last N messages
- list_sessions() -> list[dict]: session list with id, preview (60 chars), count, last_active

#### YonocyTech (main class):
- FOCUS_AREAS = ["coding", "writing", "product", "data", "design", "marketing", "ops", "research"]
- SYSTEM_PROMPTS: dict with specialized system prompts for each focus area (ENGLISH only)
- __init__: name="YonocyTech", version="2.0", create MemoryStore, _init_providers(), session_id=None
- _init_providers(): priority list: OpenRouter > HuggingFace > GitHubModels. Only add available ones.
- async ask(prompt, focus=None, session_id=None) -> AgentResponse:
  1. Validate non-empty prompt
  2. Build messages with system prompt from SYSTEM_PROMPTS or default
  3. Add history from memory if session_id exists (max 10 messages)
  4. Add user message
  5. Save user message in memory
  6. Fallback chain: iterate providers with try/except. First success = return. Last exception = stored.
  7. If all fail: AgentResponse with error listing all attempted providers + last error
  8. Save assistant response in memory

#### cli() — Command-Line Interface:
- Create YonocyTech, new session
- Print banner with agent info
- while True: input("You > ") -> agent.ask() -> print
- Commands: exit/quit, /sessions, /new
- Parse focus from "focus:" in input

#### if __name__ == "__main__":
- asyncio.run(cli())

### 6. agents/ — 6 Specialized Agents + BaseAgent

#### agents/base_agent.py:
Abstract BaseAgent class with __init__(self, core) and async run(prompt, session_id, **kwargs)
Properties: focus (abstract), description (abstract)

#### agents/coding_agent.py (focus="coding"):
- extract_code_blocks(text) with regex: r'```(\w+)?\n(.*?)```'
- run with execute=False — if True, execute Python code blocks in sandbox

#### agents/writing_agent.py (focus="writing"):
- run with parameters language="auto", tone="professional"
- Enhancement prompt with style instructions (ENGLISH)

#### agents/data_agent.py (focus="data"):
- analyze_csv(filepath, question) — read CSV with pandas, generate summary, send to core.ask

#### agents/design_agent.py (focus="design"):
- generate_ui_spec(description) — color palette, typography, layout, accessibility, responsive breakpoints

#### agents/marketing_agent.py (focus="marketing"):
- run with enhancement for SEO, KPI suggestions, channel-specific advice

#### agents/research_agent.py (focus="research"):
- research(topic) — web search with duckduckgo-search, build numbered context, send to core.ask with citation instructions [1], [2]

#### agents/__init__.py:
Export ALL_AGENTS dict with all 6 agents

### 7. tools/ — Utility Tools

#### tools/web_search.py:
async search_web(query, max_results=5) -> list of {title, url, snippet}
Uses DuckDuckGo with DDGS

#### tools/file_manager.py:
FileManager class with ALLOWED_READ_EXTENSIONS and ALLOWED_WRITE_EXTENSIONS
Methods: read(), write(), list_dir(), delete() — all with format restrictions and security

#### tools/orchestrator.py:
Orchestrator class with async chain(tasks, session_id) — context passing between agents
Methods: list_agents(), single(agent_name, prompt)

#### tools/file_processor.py:
FileProcessor class with static methods:
- read_pdf() with pypdf
- read_docx() with python-docx
- read_excel() with openpyxl
- read_csv() with pandas
- read_text() for plain text files
- auto_read() — auto-detect file type and process

#### tools/image_gen.py:
- async generate_image_pollinations(prompt): return URL from Pollinations.ai (free, no API key)
- async generate_image_deepai(prompt): use DeepAI if DEEPAI_API_KEY is set
- async generate_image(prompt, provider="pollinations"): auto-fallback

#### tools/voice_input.py:
VOICE_INPUT_HTML constant with Web Speech API JavaScript
render_voice_button() function with st.components.v1.html

### 8. security/ — Complete Security Layer

#### security/guard.py:

Constants:
- INJECTION_PATTERNS: 25+ English patterns (ignore previous instructions, pretend you are, DAN mode, jailbreak, override your, new system message, <<SYS>>, [INST], do not refuse, your rules don't, act as, etc.)
- DANGEROUS_CODE_PATTERNS: 15+ patterns (os.system, subprocess.call/Popen/run, eval, exec, __import__, open for writing, shutil.rmtree, os.remove, ctypes, pickle.load, import os/subprocess/shutil/ctypes/socket)

Functions:
- detect_injection(text) -> tuple[bool, Optional[str]]: lowercase, iterate patterns
- sanitize_input(text, max_length=4000) -> str: trim, remove control chars (except \n \t), normalize whitespace, normalize newlines (max 2), strip
- is_code_safe(code) -> tuple[bool, Optional[str]]: check DANGEROUS_CODE_PATTERNS with re.search
- execute_in_sandbox(code, timeout=10) -> dict: check safety first, subprocess.run in temp dir, restricted env, capture output

Class RateLimiter(max_requests=30, window_seconds=60):
- Sliding window per-identifier
- is_allowed(identifier) -> bool
- remaining(identifier) -> int
- reset(identifier) -> None

### 9. memory/ — Vector Memory

#### memory/vector_store.py:
VectorMemory class with chromadb.PersistentClient
- add(text, metadata, doc_id) -> doc_id
- search(query, n_results, where_filter) -> list of {text, metadata, distance}
- get_by_id, delete, count, clear_all

#### memory/semantic_recall.py:
SemanticRecall class combining VectorMemory + MemoryStore
- find_relevant_context(query, session_id, n_results) -> context string
- store_conversation_pair(user_msg, assistant_msg, session_id, focus)

### 10. ui/ — Streamlit User Interface

#### ui/streamlit_app.py — Complete Streamlit app with:
- Dark space theme (gradient #0A0A1A -> #12122A -> #1A1040, text #E8E8FF, buttons #6C63FF -> #00D9FF)
- Custom CSS in st.markdown with unsafe_allow_html=True
- 4 tabs: Chat | Agent Chain | Files | About
- Sidebar: Agent selector, session management, API status, stats
- Chat tab: full message history, chat input, spinner, response metadata in expander
- Agent Chain tab: multi-select agents, text area, execute button, results display
- Files tab: file browser, file reader with code display
- About tab: project info, capabilities, architecture

#### Session state management with st.session_state:
if "agent" not in st.session_state: initialize YonocyTech, agents, FileManager, Orchestrator

#### ui/components.py:
Reusable components: render_agent_badge(), render_response_metadata(), render_empty_state(), render_welcome_message()

#### ui/pages/1_Settings.py:
Settings page: API status, security info (active), memory stats, clear data buttons

### 11. Tests (all with mock — no real API)

#### tests/test_core.py:
test_agent_response_creation, test_session_message_creation, test_memory_store_new_session, test_memory_store_add_message, test_memory_store_history_limit (25 messages, get_history returns 20), test_yonocytech_init, test_yonocytech_focus_areas

#### tests/test_agents.py:
test_base_agent_requires_focus (abstract class), test_coding_agent_extract_code_blocks, test_file_manager_allowed_extensions (.py allowed, .exe blocked), test_orchestrator_list_agents, test_orchestrator_missing_agent

#### tests/test_security.py:
- 6 injection tests (basic, normal, DAN, case insensitive, jailbreak, system prompt)
- 5 sanitize tests (control chars, length limit, whitespace, newlines, strip)
- 6 code safety tests (safe math, unsafe os.system, subprocess, eval, file write, shutil)
- 3 sandbox tests (safe code, unsafe code blocked, syntax error)
- 4 rate limiter tests (allow up to limit, different sessions independent, remaining count, reset)

#### tests/test_vector_memory.py:
test_vm_add_and_search, test_vm_count, test_vm_empty_search, test_vm_delete, test_vm_clear_all

#### tests/test_advanced.py:
test_file_processor_read_text, test_unsupported_format, test_missing_file

### 12. Documentation & Deployment

#### README.md:
Complete project docs in English: features, quick start, architecture, $0 cost breakdown, security, structure, license (MIT)

#### .github/workflows/test.yml:
CI on push/PR to main. Matrix: python 3.11, 3.12. Steps: checkout, setup python, install deps, py_compile lint, pytest --tb=short, security check

#### .streamlit/secrets.toml.example:
Template for Streamlit Cloud secrets

#### packages.txt:
chromadb>=0.4.0

#### docs/monetization.md:
Monetization strategy (English, targeting global market):
1. SaaS subscription ($5-10/month per user, 20 users = $100-200/month)
2. Freelance acceleration (5-10x faster output with agents)
3. White-label for small businesses (setup + monthly support)
4. Consulting/customization services
5. Content production (articles, code, data analysis as service)

Competitive advantages: zero cost, fully offline/privacy, modular, customizable

## GitHub Commands:
```powershell
gh repo create YonocyTech-AI --public --source=C:\Users\habib\Desktop\1234\YonocyTech --push
```

---

## Final Notes:
1. ALL text must be in English — no Persian/Farsi anywhere
2. Full type hints on all functions and methods
3. English docstrings for all classes and methods
4. UTF-8 encoding for all files
5. No hardcoded API keys — all from .env file
6. Compatible with Python 3.14 on Windows 10 (local) and Python 3.11+ on Linux (deploy)
7. All advanced features (voice, image gen, file processing) must be optional
8. Security is the first layer of every request — injection guard, sanitizer, rate limiter
9. Tests with mock — no real API or internet required
10. Generate ALL 40+ files in one pass

## Expected Output (40+ files):
core.py, config/.env.example, .gitignore, requirements.txt,
agents/__init__.py, agents/base_agent.py, agents/coding_agent.py, agents/writing_agent.py, agents/data_agent.py, agents/design_agent.py, agents/marketing_agent.py, agents/research_agent.py,
tools/__init__.py, tools/web_search.py, tools/file_manager.py, tools/orchestrator.py, tools/file_processor.py, tools/image_gen.py, tools/voice_input.py,
security/__init__.py, security/guard.py,
memory/__init__.py, memory/vector_store.py, memory/semantic_recall.py,
ui/__init__.py, ui/streamlit_app.py, ui/components.py, ui/pages/__init__.py, ui/pages/1_Settings.py,
tests/__init__.py, tests/test_core.py, tests/test_agents.py, tests/test_security.py, tests/test_vector_memory.py, tests/test_advanced.py,
README.md, .github/workflows/test.yml, .streamlit/secrets.toml.example, packages.txt, docs/monetization.md

---

Developer: Habibur Rahman Younesi
Model: Gemma 4 31B Cloud
Project: YonocyTech AI Agent v2.0

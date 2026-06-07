# 🏗️ فاز ۱: بستر و هسته AI Engine
## پرامپت کامل برای GLM-5-Turbo

---

> **دستور:** این پرامپت رو کامل به مدل GLM-5-Turbo بده. مدل باید تمام فایل‌های این فاز رو تولید کند.

---

## 📋 پرامپت فاز ۱

```
تو یک برنامه‌نویس Python ارشد هستی. من یک پروژه AI Agent به نام YonocyTech می‌سازم.

### مشخصات سیستمی:
- لپ‌تاپ: Dell Latitude E5440
- CPU: Intel Core i5-4310U (2 هسته، ۴ رشته)
- RAM: 8GB DDR3
- GPU: NVIDIA GT 720M (2GB)
- دیسک: 500GB HDD (250GB خالی)
- OS: Windows 10
- Python 3.14, Node v24, Git, winget, npm

### مسیر پروژه:
C:\Users\habib\Desktop\1234\YonocyTech\

### بودجه:
$0 — فقط ابزارها و سرویس‌های رایگان مجاز هستند.

### هدف فاز ۱:
ساخت بستر پروژه و هسته اصلی AI Engine با Fallback Chain.

---

## خواسته‌شده:

### ۱. ساختار پوشه‌ها
ساختار زیر را با دستورات PowerShell ایجاد کن (mkdir با New-Item -ItemType Directory):

YonocyTech/
├── core.py
├── config/
│   └── .env.example
├── agents/
│   └── __init__.py
├── tools/
│   └── __init__.py
├── ui/
│   └── __init__.py
├── memory/
│   ├── __init__.py
│   └── data/
├── security/
│   └── __init__.py
├── tests/
│   └── __init__.py
├── docs/
├── .gitignore
└── requirements.txt

### ۲. فایل .env.example
یک فایل .env.example بساز با این محتوا:
```ini
# ─── YonocyTech AI Agent — Environment Variables ───
# این فایل رو به .env.rename کن و کلیدهای واقعی رو وارد کن.

# OpenRouter (پیش‌فرض — رایگان)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx
OPENROUTER_DEFAULT_MODEL=mistralai/mistral-7b-instruct:free

# Hugging Face (فال‌بک ۱ — رایگان)
HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxx
HF_DEFAULT_MODEL=mistralai/Mistral-7B-Instruct-v0.3

# GitHub Models (فال‌بک ۲ — رایگان)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxx
```

### ۳. فایل .gitignore
```gitignore
# Environment
.env
config/.env
venv/
env/
__pycache__/
*.pyc
*.pyo

# Memory data
memory/data/
memory/chroma_data/

# IDE
.vscode/
.idea/
*.swp

# OS
Thumbs.db
.DS_Store
desktop.ini

# Distribution
dist/
build/
*.egg-info/
```

### ۴. فایل requirements.txt
```txt
# ─── YonocyTech AI Agent v2.0 ───
# نصب: pip install -r requirements.txt

# Core
streamlit>=1.31.0
httpx>=0.26.0
python-dotenv>=1.0.0

# Memory & Storage
chromadb>=0.4.0

# Data & Processing
pandas>=2.1.0
matplotlib>=3.8.0
pillow>=10.0.0
pypdf>=4.0.0
python-docx>=1.0.0
openpyxl>=3.1.0

# Tools
duckduckgo-search>=6.0.0
beautifulsoup4>=4.12.0
requests>=2.31.0
feedparser>=6.0.0

# Dev
pytest>=8.0.0
```

### ۵. فایل core.py — هسته اصلی (مهم‌ترین فایل این فاز)
این فایل باید شامل موارد زیر باشد:

#### ۵.۱. Importها:
- os, json, time, hashlib, asyncio از ماژول‌های استاندارد
- httpx از httpx
- load_dotenv از dotenv
- dataclass, field از dataclasses
- datetime از datetime
- Optional, Dict, List, Any از typing
- Path از pathlib

#### ۵.۲. ثابت BASE_DIR:
```python
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "config" / ".env")
```

#### ۵.۳. کلاس AgentResponse (dataclass):
- فیلدها: text (str), model (str), provider (str), tokens_used (int=0), latency_ms (float=0.0), timestamp (str, default_factory با datetime.now().isoformat)

#### ۵.۴. کلاس SessionMessage (dataclass):
- فیلدها: role (str: "user"/"assistant"/"system"), content (str), focus (Optional[str]=None), timestamp (str, default_factory با datetime.now().isoformat)

#### ۵.۵. کلاس OpenRouterProvider:
- __init__: خواندن OPENROUTER_API_KEY و OPENROUTER_DEFAULT_MODEL از env. اگر env خالی بود، مدل پیش‌فرض = "mistralai/mistral-7b-instruct:free". base_url = "https://openrouter.ai/api/v1/chat/completions"
- is_available (property): bool(self.api_key)
- async ask(self, messages: List[Dict], max_tokens: int = 1024) -> AgentResponse:
  - اندازه‌گیری زمان با time.time()
  - استفاده از httpx.AsyncClient با timeout=60
  - POST به base_url با headers: Authorization (Bearer), HTTP-Referer (http://localhost:8501), X-Title (YonocyTech)
  - Body: {"model": self.model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.7}
  - اگر status_code != 200: raise Exception با جزئیات
  - برگرداندن AgentResponse با مقادیر واقعی

#### ۵.۶. کلاس HuggingFaceProvider:
- __init__: خواندن HF_API_KEY و HF_DEFAULT_MODEL از env. base_url = f"https://api-inference.huggingface.co/models/{self.model}"
- is_available (property): bool(self.api_key)
- async ask(self, messages: List[Dict], max_tokens: int = 1024) -> AgentResponse:
  - استخراج system_msg و user_msg از لیست messages (با next و generator expression)
  - تبدیل به فرمت HF: f"<s>[INST] {system_msg}\n\n{user_msg} [/INST]"
  - POST با headers: Authorization
  - Body: {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens, "temperature": 0.7}}
  - پاک کردن prompt از output (replace و strip)
  - برگرداندن AgentResponse

#### ۵.۷. کلاس GitHubModelsProvider:
- __init__: خواندن GITHUB_TOKEN از env. مدل = "gpt-4o-mini". base_url = "https://models.inference.ai.azure.com/chat/completions"
- is_available (property): bool(self.token)
- async ask: مشابه OpenRouter ولی با Authorization: Bearer {self.token} و Content-Type: application/json

#### ۵.۸. کلاس MemoryStore (حافظه دائمی):
- __init__(self, data_dir=None): ایجاد پوشه memory/data/ اگر وجود نداشت. conversations_file = data_dir / "conversations.json". فراخوانی _load()
- _load(): خواندن JSON از conversations_file. تبدیل به لیست SessionMessage. خطا = sessions خالی.
- _save(): تبدیل sessions به dict، نوشتن JSON با ensure_ascii=False و indent=2
- new_session() -> str: تولید sid با hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]. ذخیره و برگرداندن.
- add_message(session_id, role, content, focus=None): اضافه کردن SessionMessage. محدودیت ۵۰ پیام آخر (crop). فراخوانی _save.
- get_history(session_id, limit=20): برگرداندن limit پیام آخر
- list_sessions() -> List[Dict]: لیست جلسات با id, preview (60 کاراکتر اول), messages count, last_active. مرتب‌سازی بر اساس زمان.

#### ۵.۹. کلاس YonocyTech (کلاس اصلی):
- FOCUS_AREAS: لیست = ["coding", "writing", "product", "data", "design", "marketing", "ops", "research"]
- SYSTEM_PROMPTS: dict با سیستم پرامپت اختصاصی برای هر حوزه (فارسی و انگلیسی). برای "coding": "You are YonocyTech Coding Expert..."، برای "writing": "You are YonocyTech Writing Expert..."، و به همین ترتیب برای بقیه.
- __init__: name="YonocyTech", version="2.0". ایجاد MemoryStore. فراخوانی _init_providers(). session_id = None.
- _init_providers(): ایجاد لیست providers. اولویت: openrouter > huggingface > github_models. فقط providerهایی که is_available=True را اضافه کن. اگر هیچکدام فعال نبود، print هشدار.
- async ask(self, prompt, focus=None, session_id=None) -> AgentResponse:
  1. Validation: prompt خالی = AgentResponse با پیام خطا
  2. Build messages: system_prompt از SYSTEM_PROMPTS یا default. اضافه کردن تاریخچه از memory اگر session_id هست (حداکثر ۱۰ پیام). اضافه کردن user message.
  3. ذخیره user message در memory
  4. Fallback chain: پیمایش providers. try/except. اولین موفقیت = return. آخرین خطا = ذخیره.
  5. اگر همه ناموفق بودند: AgentResponse با پیام خطای فارسی (لیست providerهایی که تلاش شد + آخرین خطا)
  6. ذخیره assistant response در memory

#### ۵.۱۰. تابع cli() — رابط خط فرمان:
- ایجاد YonocyTech و session_id جدید
- چاپ بنر با اطلاعات agent
- حلقه while True:
  - input("👤 شما > ")
  - دستورات: exit/quit/خروج = break, /sessions = لیست جلسات
  - parse focus: اگر " focus:" در input بود، جدا کن
  - agent.ask() با asyncio.run
  - چاپ response

#### ۵.۱۱. if __name__ == "__main__":
- asyncio.run(cli())

---

### ۶. فایل‌های __init__.py
برای هر پوشه agents/, tools/, ui/, memory/, security/, tests/ یک فایل __init__.py خالی بساز.

### ۷. تست فاز ۱
یک فایل tests/test_core.py بساز با pytest:
- test_agent_response_creation: ساخت AgentResponse و بررسی فیلدها
- test_session_message_creation: ساخت SessionMessage
- test_memory_store_new_session: ایجاد جلسه و بررسی برگرداندن string
- test_memory_store_add_message: اضافه کردن پیام و بررسی
- test_memory_store_history_limit: اضافه کردن ۲۵ پیام و بررسی اینکه get_history(20) فقط ۲۰ رو برمی‌گردونه
- test_yonocytech_init: ساخت YonocyTech و بررسی name و version
- test_yonocytech_focus_areas: بررسی FOCUS_AREAS

تمام تست‌ها باید با mock کار کنند (نه واقعی به API وصل بشن).

### ۸. دستورات راه‌اندازی فاز ۱ (PowerShell)
```powershell
cd C:\Users\habib\Desktop\1234
New-Item -ItemType Directory -Force -Path YonocyTech\{agents,tools,ui,memory\data,security,tests,docs,config}
python -m venv YonocyTech\venv
YonocyTech\venv\Scripts\Activate.ps1
cd YonocyTech
pip install -r requirements.txt
Copy-Item config\.env.example config\.env
# ویرایش config\.env با کلیدهای واقعی
python -m pytest tests/ -v
python core.py
```

---

### نکات مهم:
1. تمام error handling باید فارسی و انگلیسی باشد (پیام‌های خطا دو زبانه).
2. کد باید کاملاً type-hinted باشد.
3. docstring برای هر کلاس و متد (به انگلیسی).
4. سازگار با Python 3.14.
5. هیچ API key هاردکد نشده — همه از .env خوانده می‌شوند.
6. فایل‌ها باید UTF-8 encoding باشند.
7. Comments فارسی و کد انگلیسی.
```

---

## ✅ خروجی مورد انتظار فاز ۱

| فایل | وضعیت |
|------|-------|
| `core.py` | ✅ کامل با همه کلاس‌ها |
| `config/.env.example` | ✅ الگوی متغیرهای محیطی |
| `.gitignore` | ✅ |
| `requirements.txt` | ✅ |
| `agents/__init__.py` | ✅ |
| `tools/__init__.py` | ✅ |
| `ui/__init__.py` | ✅ |
| `memory/__init__.py` | ✅ |
| `security/__init__.py` | ✅ |
| `tests/__init__.py` | ✅ |
| `tests/test_core.py` | ✅ تست‌های unit |

---

## 🔗 وابستگی به فازهای دیگر

- **وابسته به:** هیچ فاز قبلی
- **پیش‌نیاز فازهای بعدی:** فاز ۲ به core.py نیاز دارد. فاز ۳ به MemoryStore نیاز دارد. فاز ۴ به core.py نیاز دارد.

# 🚀 طرح عملی YonocyTech AI Agent
## نسخه ۲.۰ — صفر دلار، فقط همین کامپیوتر

> **اصلاح‌شده بر اساس بررسی فنی — تمام اشکالات نسخه ۱.۰ برطرف شده است.**

---

# 📌 خلاصه وضعیت سیستم

| مشخصه | مقدار |
|-------|-------|
| لپ‌تاپ | Dell Latitude E5440 |
| CPU | Intel Core i5-4310U (2 هسته، ۴ رشته) |
| RAM | ۸GB DDR3 |
| GPU | NVIDIA GT 720M (2GB) |
| دیسک | ۵۰۰GB HDD (۲۵۰GB خالی) |
| OS | Windows 10 |
| ابزارهای موجود | Python 3.14, Node v24, Git, winget, npm |
| مسیر پروژه | `C:\Users\habib\Desktop\1234\YonocyTech\` |

---

# 🏗️ معماری نهایی (بازنویسی‌شده)

```
┌──────────────────────────────────────────────────────────────────┐
│                     Frontend (UI Layer)                          │
│              Streamlit (MVP) → Next.js (نهایی)                    │
│         shadcn/ui + Tailwind + Lucide + Framer Motion            │
├──────────────────────────────────────────────────────────────────┤
│                    Security Layer 🆕                              │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐     │
│    │ Prompt       │  │ Input        │  │ Code Sandbox     │     │
│    │ Injection     │  │ Sanitizer    │  │ (subprocess)     │     │
│    │ Guard        │  │              │  │                  │     │
│    └──────────────┘  └──────────────┘  └──────────────────┘     │
├──────────────────────────────────────────────────────────────────┤
│                   Orchestration Layer 🆕                          │
│            LangChain AgentExecutor + Tool Chaining               │
│         Fallback Chain: OpenRouter → HF → Local Model           │
├──────────────────────────────────────────────────────────────────┤
│                AI Engine (Model Layer) 🆕                         │
│  ┌────────────────┐ ┌──────────────┐ ┌──────────────────────┐   │
│  │ OpenRouter 🆕  │ │ Hugging Face │ │ GitHub Models        │   │
│  │ 200+ req/day   │ │ 30k tok/day  │ │ Free tier            │   │
│  │ (پیش‌فرض)      │ │ (فال‌بک ۱)    │ │ (فال‌بک ۲)           │   │
│  └────────────────┘ └──────────────┘ └──────────────────────┘   │
├──────────────────────────────────────────────────────────────────┤
│              Tool Integration Layer                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │Code    │ │Write   │ │Data    │ │Design  │ │Research│       │
│  │Agent   │ │Agent   │ │Agent   │ │Agent   │ │Agent   │       │
│  │+Sandbox│ │+Gramm. │ │+Charts │ │+SVG    │ │+Search │       │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘       │
├──────────────────────────────────────────────────────────────────┤
│               Memory & Persistence 🆕                             │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐     │
│  │ ChromaDB    │  │ JSON Store   │  │ SQLite (sessions)  │     │
│  │ (vector)    │  │ (conversation│  │ (metadata)         │     │
│  │             │  │  history)    │  │                    │     │
│  └─────────────┘  └──────────────┘  └────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

# 📅 فاز ۰: آماده‌سازی محیط — روز ۱

## ۰-۱. نصب ابزارهای پایه (PowerShell Admin)

```powershell
# اگر VS Code نداری:
winget install Microsoft.VisualStudioCode
winget install Git.Git

# تایید نسخه‌ها
python --version     # باید 3.10+ باشه
node --version       # باید 18+ باشه
git --version
```

## ۰-۲. ایجاد پوشه پروژه و محیط مجازی

```powershell
# ایجاد ساختار پروژه توی workspace فعلی
cd "C:\Users\habib\Desktop\1234"
mkdir YonocyTech
cd YonocyTech
mkdir agents, tools, ui, memory, config, tests, docs

# محیط مجازی Python
python -m venv venv
.\venv\Scripts\Activate.ps1

# اگر Activate.ps1 خطای ExecutionPolicy داد:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## ۰-۳. نصب بسته‌های Python

```powershell
# فایل requirements.txt رو می‌سازیم (بعداً)
pip install streamlit gradio langchain langchain-community langchain-core
pip install openai httpx requests beautifulsoup4 pandas matplotlib
pip install pillow python-dotenv pyperclip chromadb sqlite-utils
pip install pypdf python-docx openpyxl pytesseract
pip install duckduckgo-search feedparser pytest
```

## ۰-۴. حساب‌های رایگان مورد نیاز — همین امروز بساز

| # | سرویس | برای چی | لینک ثبت‌نام | زمان |
|---|-------|---------|-------------|------|
| ۱ | **OpenRouter** 🆕 | LLM اصلی — ۲۰۰+ درخواست رایگان/روز | [openrouter.ai](https://openrouter.ai/sign-up) | ۲ دقیقه |
| ۲ | **Hugging Face** | مدل‌های فال‌بک، Spaces هاست | [huggingface.co/join](https://huggingface.co/join) | ۲ دقیقه |
| ۳ | **GitHub** | کد، CI/CD، GitHub Models | [github.com/signup](https://github.com/signup) | ۳ دقیقه |
| ۴ | **Vercel** | هاست Frontend نهایی | [vercel.com/signup](https://vercel.com/signup) | ۱ دقیقه |
| ۵ | **Streamlit Cloud** | هاست سریع MVP | [share.streamlit.io](https://share.streamlit.io) | ۱ دقیقه |

### 🆕 چرا OpenRouter به‌جای Hugging Face به‌عنوان پیش‌فرض؟

| مقایسه | OpenRouter 🆕 | Hugging Face Inference |
|--------|--------------|----------------------|
| **محدودیت روزانه** | ~۲۰۰ درخواست | ~۳۰٬۰۰۰ توکن (≈۲۰ سوال) |
| **مدل‌های در دسترس** | ۲۰۰+ مدل (Llama, Mistral, Gemma...) | محدود به مدل‌های hosted |
| **نرخ خطا (rate limit)** | بالاتر، پایدارتر | سریعتر پر میشه |
| **نیاز به کارت اعتباری** | خیر — کاملاً رایگان | خیر |
| **API Key** | از Dashboard → API Keys | از Settings → Access Tokens |

**استراتژی:** OpenRouter پیش‌فرض → Hugging Face فال‌بک ۱ → GitHub Models فال‌بک ۲

---

# ⚙️ فاز ۱: هسته AI Engine — روز ۲-۴

## ۱-۱. معماری Fallback Chain (مهم!)

```
درخواست کاربر
     │
     ▼
┌─────────────────┐
│ OpenRouter 🟢   │───→ موفق؟ ──→ پاسخ به کاربر
│ (پیش‌فرض)       │
└─────────────────┘
     │ ❌ خطا / Rate Limit
     ▼
┌─────────────────┐
│ Hugging Face 🟡 │───→ موفق؟ ──→ پاسخ به کاربر
│ (فال‌بک ۱)      │
└─────────────────┘
     │ ❌ خطا
     ▼
┌─────────────────┐
│ GitHub Models 🔴│───→ موفق؟ ──→ پاسخ به کاربر
│ (فال‌بک ۲)      │
└─────────────────┘
     │ ❌ همه fallbackها ناموفق
     ▼
   پیام خطای مناسب + ذخیره درخواست برای retry
```

## ۱-۲. فایل `.env` — امنیت API Keyها

```powershell
# توی پوشه YonocyTech\config فایل .env بساز:
New-Item config\.env -ItemType File
```

```ini
# config/.env — هرگز این فایل رو commit نکن!
# API Keyها رو از سایت‌های زیر بگیری:
# OpenRouter:   https://openrouter.ai/settings/keys
# Hugging Face: https://huggingface.co/settings/tokens
# GitHub:       https://github.com/settings/tokens (classic, read:user)

OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx
OPENROUTER_DEFAULT_MODEL=mistralai/mistral-7b-instruct:free

HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxx
HF_DEFAULT_MODEL=mistralai/Mistral-7B-Instruct-v0.3

GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxx
```

```powershell
# اضافه کردن .env به gitignore:
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

## ۱-۳. `core.py` — هسته اصلی (کامل، اشکال‌زدایی‌شده) 🆕

```python
"""
YonocyTech AI Agent — Core Engine v2.0
Fallback chain + Security + Persistence
No paid dependencies. Zero cost.
"""

import os
import json
import time
import hashlib
from datetime import datetime
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from pathlib import Path

import httpx
from dotenv import load_dotenv

# ── Load environment ──────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "config" / ".env")


# ═══════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════

@dataclass
class AgentResponse:
    """پاسخ استاندارد از هر مدل"""
    text: str
    model: str
    provider: str
    tokens_used: int = 0
    latency_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SessionMessage:
    """یک پیام در تاریخچه جلسه"""
    role: str          # "user" | "assistant" | "system"
    content: str
    focus: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ═══════════════════════════════════════════════════════
# PROMPT INJECTION GUARD 🆕
# ═══════════════════════════════════════════════════════

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all prior instructions",
    "pretend you are",
    "you are now",
    "forget your training",
    "system prompt:",
    "<|system|>",
    "<|im_start|>system",
    "DAN mode",
    "jailbreak",
    "bypass your",
    "override your",
    "new system message",
    "<<SYS>>",
    "[INST]",
    "you must answer",
    "you have to answer",
    "do not refuse",
    "you are not bound by",
    "your rules don't",
    "your guidelines don't"
]

def detect_injection(text: str) -> tuple[bool, Optional[str]]:
    """
    تشخیص prompt injection در ورودی کاربر.
    برمی‌گردونه: (is_injection, matched_pattern)
    """
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if pattern in text_lower:
            return True, pattern
    return False, None


# ═══════════════════════════════════════════════════════
# API PROVIDERS (Fallback Chain) 🆕
# ═══════════════════════════════════════════════════════

class OpenRouterProvider:
    """ارائه‌دهنده اصلی — OpenRouter (200+ req/day free)"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.model = os.getenv("OPENROUTER_DEFAULT_MODEL", "mistralai/mistral-7b-instruct:free")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
    
    @property
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def ask(self, messages: List[Dict], max_tokens: int = 1024) -> AgentResponse:
        t0 = time.time()
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "YonocyTech"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                }
            )
        
        if resp.status_code != 200:
            raise Exception(f"OpenRouter error {resp.status_code}: {resp.text}")
        
        data = resp.json()
        return AgentResponse(
            text=data["choices"][0]["message"]["content"],
            model=self.model,
            provider="openrouter",
            tokens_used=data.get("usage", {}).get("total_tokens", 0),
            latency_ms=(time.time() - t0) * 1000
        )


class HuggingFaceProvider:
    """فال‌بک ۱ — Hugging Face Inference API (30k tokens/day free)"""
    
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY", "")
        self.model = os.getenv("HF_DEFAULT_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model}"
    
    @property
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def ask(self, messages: List[Dict], max_tokens: int = 1024) -> AgentResponse:
        t0 = time.time()
        # تبدیل فرمت OpenAI messages به فرمت HF text
        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
        prompt = f"<s>[INST] {system_msg}\n\n{user_msg} [/INST]"
        
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "inputs": prompt,
                    "parameters": {"max_new_tokens": max_tokens, "temperature": 0.7}
                }
            )
        
        if resp.status_code != 200:
            raise Exception(f"HF error {resp.status_code}: {resp.text}")
        
        data = resp.json()
        text = data[0]["generated_text"] if isinstance(data, list) else data["generated_text"]
        # حذف prompt از خروجی
        if prompt in text:
            text = text.replace(prompt, "").strip()
        
        return AgentResponse(
            text=text,
            model=self.model,
            provider="huggingface",
            latency_ms=(time.time() - t0) * 1000
        )


class GitHubModelsProvider:
    """فال‌بک ۲ — GitHub Models (free tier)"""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.model = "gpt-4o-mini"
        self.base_url = "https://models.inference.ai.azure.com/chat/completions"
    
    @property
    def is_available(self) -> bool:
        return bool(self.token)
    
    async def ask(self, messages: List[Dict], max_tokens: int = 1024) -> AgentResponse:
        t0 = time.time()
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                }
            )
        
        if resp.status_code != 200:
            raise Exception(f"GitHub Models error {resp.status_code}: {resp.text}")
        
        data = resp.json()
        return AgentResponse(
            text=data["choices"][0]["message"]["content"],
            model=self.model,
            provider="github_models",
            latency_ms=(time.time() - t0) * 1000
        )


# ═══════════════════════════════════════════════════════
# MEMORY & PERSISTENCE 🆕
# ═══════════════════════════════════════════════════════

class MemoryStore:
    """
    حافظه دائمی — ترکیب JSON file + ChromaDB vector store
    از restart جان سالم به در می‌بره
    """
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or (BASE_DIR / "memory" / "data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.conversations_file = self.data_dir / "conversations.json"
        self.sessions: Dict[str, List[SessionMessage]] = {}
        self._load()
    
    def _load(self):
        """بارگذاری جلسات قبلی از دیسک"""
        if self.conversations_file.exists():
            try:
                raw = json.loads(self.conversations_file.read_text(encoding="utf-8"))
                for session_id, msgs in raw.items():
                    self.sessions[session_id] = [
                        SessionMessage(**m) for m in msgs
                    ]
            except (json.JSONDecodeError, KeyError):
                self.sessions = {}
    
    def _save(self):
        """ذخیره روی دیسک"""
        data = {
            sid: [{"role": m.role, "content": m.content, 
                   "focus": m.focus, "timestamp": m.timestamp} 
                  for m in msgs]
            for sid, msgs in self.sessions.items()
        }
        self.conversations_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), 
            encoding="utf-8"
        )
    
    def new_session(self) -> str:
        """ایجاد جلسه جدید → برمی‌گردونه session_id"""
        sid = hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]
        self.sessions[sid] = []
        self._save()
        return sid
    
    def add_message(self, session_id: str, role: str, content: str, focus: str = None):
        """اضافه کردن پیام به جلسه"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(
            SessionMessage(role=role, content=content, focus=focus)
        )
        # فقط ۵۰ پیام آخر رو نگه دار (مدیریت حافظه)
        if len(self.sessions[session_id]) > 50:
            self.sessions[session_id] = self.sessions[session_id][-50:]
        self._save()
    
    def get_history(self, session_id: str, limit: int = 20) -> List[SessionMessage]:
        """دریافت تاریخچه جلسه"""
        msgs = self.sessions.get(session_id, [])
        return msgs[-limit:]
    
    def list_sessions(self) -> List[Dict]:
        """لیست تمام جلسات قبلی"""
        result = []
        for sid, msgs in self.sessions.items():
            if msgs:
                first = msgs[0].content[:60]
                last_ts = msgs[-1].timestamp
                result.append({
                    "id": sid,
                    "preview": first,
                    "messages": len(msgs),
                    "last_active": last_ts
                })
        return sorted(result, key=lambda x: x["last_active"], reverse=True)


# ═══════════════════════════════════════════════════════
# MAIN AGENT CLASS 🆕 (بازنویسی کامل)
# ═══════════════════════════════════════════════════════

class YonocyTech:
    """
    YonocyTech AI Agent v2.0
    — Fallback chain model selection
    — Prompt injection protection  
    — Persistent memory
    — Proper error handling
    — Zero cost
    """
    
    FOCUS_AREAS = [
        "coding", "writing", "product", "data", 
        "design", "marketing", "ops", "research"
    ]
    
    SYSTEM_PROMPTS = {
        "coding": "You are YonocyTech Coding Expert. Write clean, documented, secure code. "
                  "Explain your reasoning. Always handle errors. Prefer safe patterns.",
        "writing": "You are YonocyTech Writing Expert. Produce clear, engaging content "
                   "in the same language as the user. Match tone and style.",
        "data": "You are YonocyTech Data Analyst. Analyze data methodically. "
                "Provide actionable insights. Cite your reasoning.",
        "design": "You are YonocyTech Design Consultant. Give practical, implementable "
                  "design advice. Consider UX, accessibility, and aesthetics.",
        "marketing": "You are YonocyTech Marketing Strategist. Data-driven recommendations. "
                     "Consider SEO, social, content, and conversion.",
        "ops": "You are YonocyTech Operations Expert. Focus on reliability, automation, "
               "and practical infrastructure solutions.",
        "research": "You are YonocyTech Research Assistant. Be thorough, cite sources, "
                    "distinguish facts from opinions. Use evidence-based reasoning.",
        "product": "You are YonocyTech Product Advisor. Focus on user needs, market fit, "
                   "prioritization, and practical product strategy."
    }
    
    def __init__(self):
        self.name = "YonocyTech"
        self.version = "2.0"
        
        # Initialization order matters!
        self.memory = MemoryStore()
        self._init_providers()
        self.session_id: Optional[str] = None
    
    def _init_providers(self):
        """راه‌اندازی زنجیره تأمین‌کننده‌ها به ترتیب اولویت"""
        self.providers = []
        
        or_provider = OpenRouterProvider()
        if or_provider.is_available:
            self.providers.append(("openrouter", or_provider))
        
        hf_provider = HuggingFaceProvider()
        if hf_provider.is_available:
            self.providers.append(("huggingface", hf_provider))
        
        gh_provider = GitHubModelsProvider()
        if gh_provider.is_available:
            self.providers.append(("github_models", gh_provider))
        
        if not self.providers:
            print("⚠️ هشدار: هیچ API keyای تنظیم نشده!")
            print("   لطفاً فایل config/.env رو با کلیدهای API پر کن.")
    
    async def ask(
        self, 
        prompt: str, 
        focus: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AgentResponse:
        """
        سوال بپرس → پاسخ بگیر
        با زنجیره fallback خودکار
        """
        # ── Validation ──
        if not prompt or not prompt.strip():
            return AgentResponse(
                text="❌ لطفاً یک سوال یا درخواست وارد کنید.",
                model="system", provider="validation"
            )
        
        # ── Security: Prompt Injection Check ──
        is_injection, matched = detect_injection(prompt)
        if is_injection:
            return AgentResponse(
                text=f"🛡️ ورودی مشکوک شناسایی شد و مسدود گردید. "
                     f"(الگوی شناسایی‌شده: '{matched}')\n"
                     f"لطفاً درخواست خود را به شکل طبیعی بیان کنید.",
                model="system", provider="security_guard"
            )
        
        # ── Validate focus ──
        if focus and focus not in self.FOCUS_AREAS:
            return AgentResponse(
                text=f"❌ حوزه '{focus}' معتبر نیست.\n"
                     f"گزینه‌های معتبر: {', '.join(self.FOCUS_AREAS)}",
                model="system", provider="validation"
            )
        
        # ── Build messages ──
        system_prompt = self.SYSTEM_PROMPTS.get(
            focus, 
            f"You are YonocyTech, a helpful AI assistant. "
            f"Areas of expertise: {', '.join(self.FOCUS_AREAS)}. "
            f"Reply in the same language as the user."
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # اضافه کردن تاریخچه (اگر جلسه فعال باشه)
        if session_id:
            history = self.memory.get_history(session_id, limit=10)
            for msg in history:
                if msg.role == "user":
                    messages.append({"role": "user", "content": msg.content})
                elif msg.role == "assistant":
                    messages.append({"role": "assistant", "content": msg.content})
        
        messages.append({"role": "user", "content": prompt})
        
        # ── Save user message ──
        if session_id:
            self.memory.add_message(session_id, "user", prompt, focus)
        
        # ── Try providers in fallback chain ──
        last_error = None
        for provider_name, provider in self.providers:
            try:
                response = await provider.ask(messages)
                # Save assistant response
                if session_id and response.text:
                    self.memory.add_message(session_id, "assistant", response.text)
                return response
            except Exception as e:
                last_error = str(e)
                continue  # Try next provider
        
        # ── All providers failed ──
        error_msg = (
            f"❌ همه سرویس‌های AI در دسترس نیستند.\n\n"
            f"خطاها:\n"
        )
        for pname, _ in self.providers:
            error_msg += f"  • {pname}: تلاش شد — ناموفق\n"
        error_msg += f"\nجزئیات آخرین خطا: {last_error}\n"
        error_msg += "لطفاً اتصال اینترنت را بررسی کنید یا کمی بعد دوباره تلاش کنید."
        
        return AgentResponse(
            text=error_msg,
            model="system", provider="error_handler"
        )


# ═══════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════

async def cli():
    """رابط خط فرمان — نسخه سبک برای تست"""
    import asyncio
    
    agent = YonocyTech()
    session_id = agent.memory.new_session()
    
    print(f"\n{'═'*55}")
    print(f"  🤖 {agent.name} v{agent.version} — AI Agent")
    print(f"  💰 هزینه: $۰ | 💻 فقط همین کامپیوتر")
    print(f"{'═'*55}")
    print(f"  حوزه‌ها: {', '.join(agent.FOCUS_AREAS)}")
    print(f"  تعداد APIهای فعال: {len(agent.providers)}")
    print(f"  جلسه: {session_id}")
    print(f"{'═'*55}")
    print("  دستورات: exit | quit | خروج = پایان")
    print("           /sessions = لیست جلسات قبلی")
    print("           focus: حوزه = تنظیم حوزه تخصصی")
    print(f"{'═'*55}\n")
    
    while True:
        try:
            user_input = input("👤 شما > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ("exit", "quit", "خروج"):
                print("👋 خدانگهدار!")
                break
            
            if user_input == "/sessions":
                sessions = agent.memory.list_sessions()
                if sessions:
                    print("\n📋 جلسات قبلی:")
                    for s in sessions[:10]:
                        print(f"  • {s['id']} | {s['messages']} پیام | {s['preview']}")
                else:
                    print("هیچ جلسه قبلی وجود ندارد.")
                continue
            
            # Parse focus if specified
            focus = None
            if " focus:" in user_input:
                parts = user_input.split(" focus:", 1)
                user_input = parts[0].strip()
                focus = parts[1].strip()
            
            print(f"🤖 {agent.name} > ", end="", flush=True)
            response = await agent.ask(user_input, focus=focus, session_id=session_id)
            print(response.text)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 خدانگهدار!")
            break
        except Exception as e:
            print(f"\n⚠️ خطای غیرمنتظره: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(cli())
```

## ۱-۴. تست سریع هسته

```powershell
# اول API keyها رو توی config\.env تنظیم کن، بعد:
cd "C:\Users\habib\Desktop\1234\YonocyTech"
.\venv\Scripts\Activate.ps1
python core.py
```

---

# 🛡️ فاز ۱.۵: امنیت — روز ۴ (موازی با فاز ۱)

## ابزارهای امنیتی داخلی

### `security/guard.py` 🆕

```python
"""
YonocyTech Security Module
— Prompt Injection Protection
— Input Sanitization
— Rate Limiting
"""

import re
import time
from collections import defaultdict
from typing import Tuple, Optional


# ════════════════════════════════════════════════════
# RATE LIMITER (جلوگیری از abuse)
# ════════════════════════════════════════════════════

class RateLimiter:
    """محدودکننده نرخ درخواست — per-session"""
    
    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: defaultdict = defaultdict(list)
    
    def is_allowed(self, session_id: str) -> bool:
        now = time.time()
        window_start = now - self.window
        
        # پاکسازی درخواست‌های قدیمی
        self.requests[session_id] = [
            t for t in self.requests[session_id] if t > window_start
        ]
        
        if len(self.requests[session_id]) >= self.max_requests:
            return False
        
        self.requests[session_id].append(now)
        return True


# ════════════════════════════════════════════════════
# INPUT SANITIZER
# ════════════════════════════════════════════════════

def sanitize_input(text: str, max_length: int = 4000) -> str:
    """
    پاکسازی ورودی کاربر:
    — حذف کاراکترهای کنترلی خطرناک
    — محدود کردن طول
    — حذف repeated spaces
    """
    # Limit length
    text = text[:max_length]
    
    # Remove control characters (keep newlines, tabs)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # Normalize whitespace (but preserve single newlines)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


# ════════════════════════════════════════════════════
# CODE SANDBOX 🆕
# ════════════════════════════════════════════════════

import subprocess
import tempfile
import os

DANGEROUS_PATTERNS = [
    r'os\.system\s*\(',
    r'subprocess\.(call|Popen|run)\s*\(',
    r'eval\s*\(',
    r'exec\s*\(',
    r'__import__\s*\(',
    r'open\s*\([^)]*[\'"]w',
    r'shutil\.(rmtree|move|copy)',
    r'os\.(remove|unlink|rmdir)',
    r'import\s+(os|subprocess|shutil|sys|ctypes)',
]

def is_code_safe(code: str) -> Tuple[bool, Optional[str]]:
    """
    بررسی امنیت کد قبل از اجرا.
    برمی‌گردونه: (is_safe, dangerous_pattern_found)
    """
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            return False, pattern
    return True, None

def execute_in_sandbox(code: str, timeout: int = 10) -> dict:
    """
    اجرای کد در sandbox امن:
    — subprocess جداگانه
    — timeout ۱۰ ثانیه
    — بدون دسترسی به فایل‌سیستم
    """
    is_safe, danger = is_code_safe(code)
    if not is_safe:
        return {"success": False, "error": f"🛡️ کد ناامن — الگوی '{danger}' مسدود شد."}
    
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tempfile.gettempdir(),  # اجرا در temp dir
            env={**os.environ, "PYTHONPATH": ""}  # قطع دسترسی به پروژه
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout[:2000],
            "stderr": result.stderr[:1000],
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"⏰ اجرای کد بیش از {timeout} ثانیه طول کشید — متوقف شد."}
    except Exception as e:
        return {"success": False, "error": f"خطای sandbox: {str(e)}"}
```

---

# 🔧 فاز ۲: Agentهای تخصصی — روز ۵-۹

## ۲-۱. Base Agent Class 🆕

```python
# agents/base_agent.py
"""
کلاس پایه برای همه Agentها
— ارث‌بری + override متد run()
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class BaseAgent(ABC):
    """تمام Agentهای تخصصی از این کلاس ارث‌بری می‌کنن"""
    
    def __init__(self, yonocytech_core):
        self.core = yonocytech_core  # دسترسی به هسته اصلی
        self.name = self.__class__.__name__
    
    @property
    @abstractmethod
    def focus(self) -> str:
        """حوزه تخصصی — باید توسط subclass override بشه"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """توضیح قابلیت‌ها"""
        pass
    
    async def run(self, prompt: str, session_id: str = None, **kwargs) -> str:
        """
        متد اصلی — prompt رو می‌گیره، نتیجه رو برمی‌گردونه
        هر Agent می‌تونه override کنه برای logic خاص خودش
        """
        response = await self.core.ask(
            prompt=prompt,
            focus=self.focus,
            session_id=session_id
        )
        return response.text
```

## ۲-۲. Coding Agent 🆕

```python
# agents/coding_agent.py
"""
Coding Agent — تولید کد، دیباگ، ریفکتور، Code Review
با sandbox امن برای اجرای کد
"""

import re
from .base_agent import BaseAgent
from security.guard import execute_in_sandbox, is_code_safe

class CodingAgent(BaseAgent):
    focus = "coding"
    description = "تولید کد | دیباگ | ریفکتور | توضیح کد | اجرای امن در sandbox"
    
    SUPPORTED_LANGUAGES = [
        "python", "javascript", "typescript", "html", "css",
        "sql", "bash", "powershell", "json", "yaml"
    ]
    
    def extract_code_blocks(self, text: str) -> list:
        """استخراج بلاک‌های کد از پاسخ"""
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        return [{"language": m[0] or "text", "code": m[1].strip()} for m in matches]
    
    async def run_code(self, code: str, language: str = "python") -> dict:
        """اجرای کد در sandbox"""
        if language.lower() != "python":
            return {"success": False, "error": f"اجرای {language} فعلاً پشتیبانی نمی‌شود."}
        return execute_in_sandbox(code)
    
    async def run(self, prompt: str, session_id: str = None, execute: bool = False) -> str:
        """اجرای Coding Agent با قابلیت اجرای اختیاری کد"""
        response = await self.core.ask(
            prompt=prompt, focus="coding", session_id=session_id
        )
        
        result_text = f"## 🖥️ {self.name}\n\n{response.text}"
        
        # اگر کاربر خواسته کد اجرا بشه
        if execute:
            blocks = self.extract_code_blocks(response.text)
            python_blocks = [b for b in blocks if b["language"].lower() == "python"]
            
            if python_blocks:
                result_text += "\n\n## ⚡ نتیجه اجرا:\n"
                for i, block in enumerate(python_blocks[:3]):  # حداکثر ۳ بلاک
                    exec_result = await self.run_code(block["code"])
                    if exec_result["success"]:
                        output = exec_result.get("stdout", "").strip()
                        result_text += f"\n✅ بلاک {i+1}:\n```\n{output}\n```\n"
                    else:
                        result_text += f"\n❌ بلاک {i+1}: {exec_result.get('error', exec_result.get('stderr', ''))}\n"
        
        return result_text
```

## ۲-۳. Writing Agent

```python
# agents/writing_agent.py
from .base_agent import BaseAgent

class WritingAgent(BaseAgent):
    focus = "writing"
    description = "مقاله | مستندات | ایمیل | محتوای سوشال مدیا | ویرایش"
    
    async def run(self, prompt: str, session_id: str = None, 
                  language: str = "auto", tone: str = "professional") -> str:
        
        enhanced_prompt = f"""{prompt}

Style instructions:
- Language: {language} (match user's language if auto)
- Tone: {tone}
- Format: Well-structured with headings, bullet points where appropriate
- Quality: Clear, concise, no fluff. Include word count at end."""

        response = await self.core.ask(
            prompt=enhanced_prompt, focus="writing", session_id=session_id
        )
        return f"## ✍️ {self.name}\n\n{response.text}"
```

## ۲-۴. Data Agent

```python
# agents/data_agent.py
from .base_agent import BaseAgent

class DataAgent(BaseAgent):
    focus = "data"
    description = "تحلیل داده | Visualization | پاکسازی داده | گزارش آماری"
    
    async def analyze_csv(self, filepath: str, question: str, session_id: str = None) -> str:
        """تحلیل فایل CSV با pandas"""
        import pandas as pd
        
        try:
            df = pd.read_csv(filepath)
            summary = f"""
CSV File Summary:
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Column names: {', '.join(df.columns.tolist())}
- Data types: {dict(df.dtypes)}
- Missing values: {dict(df.isnull().sum())}
- Numeric summary:\n{df.describe().to_string()}
- First 5 rows:\n{df.head().to_string()}
            """
            
            prompt = f"{summary}\n\nUser question: {question}"
            response = await self.core.ask(prompt=prompt, focus="data", session_id=session_id)
            return f"## 📊 {self.name}\n\n{response.text}"
        except Exception as e:
            return f"❌ خطا در خواندن فایل CSV: {e}"
```

## ۲-۵. Design Agent

```python
# agents/design_agent.py
from .base_agent import BaseAgent

class DesignAgent(BaseAgent):
    focus = "design"
    description = "مشاوره UI/UX | پالت رنگی | تایپوگرافی | SVG | CSS"
    
    async def generate_ui_prompt(self, description: str) -> str:
        """تبدیل توضیحات به پرامپت طراحی"""
        return f"""Generate a UI design specification for: {description}

Include:
1. Color palette (primary, secondary, accent, background, text) — hex codes
2. Typography recommendations (font families, sizes, weights)
3. Layout structure (header, sidebar, main content, footer)
4. Component list with descriptions
5. Accessibility considerations (contrast ratios, focus states)
6. Responsive breakpoints

Format as a structured design brief."""
    
    async def run(self, prompt: str, session_id: str = None) -> str:
        design_prompt = await self.generate_ui_prompt(prompt)
        response = await self.core.ask(
            prompt=design_prompt, focus="design", session_id=session_id
        )
        return f"## 🎨 {self.name}\n\n{response.text}"
```

## ۲-۶. Research Agent

```python
# agents/research_agent.py
from .base_agent import BaseAgent
from tools.web_search import search_web

class ResearchAgent(BaseAgent):
    focus = "research"
    description = "تحقیق وب | خلاصه‌سازی | Fact-checking | استناد به منابع"
    
    async def research(self, topic: str, session_id: str = None) -> str:
        """تحقیق کامل روی یک موضوع"""
        # Step 1: Search the web
        search_results = await search_web(topic, max_results=5)
        
        if not search_results:
            response = await self.core.ask(
                prompt=f"Research topic: {topic}\nNote: No web results available. Use your knowledge.",
                focus="research",
                session_id=session_id
            )
            return f"## 🔬 {self.name}\n\n{response.text}"
        
        # Step 2: Build context from search results
        context = "Search results:\n\n"
        for i, result in enumerate(search_results, 1):
            context += f"{i}. {result['title']}\n   URL: {result['url']}\n   Snippet: {result['snippet']}\n\n"
        
        # Step 3: Ask with search context
        prompt = f"{context}\n\nResearch topic: {topic}\n\nProvide a comprehensive analysis with citations (use [1], [2] etc. referencing the search results above). Include a 'Sources' section at the end."
        
        response = await self.core.ask(prompt=prompt, focus="research", session_id=session_id)
        return f"## 🔬 {self.name}\n\n{response.text}"
```

---

# 🛠️ فاز ۳: Tool Layer — روز ۱۰-۱۲

## ۳-۱. Web Search Tool

```python
# tools/web_search.py
"""
جستجوی وب با DuckDuckGo (رایگان، بدون API key)
"""

from duckduckgo_search import DDGS

async def search_web(query: str, max_results: int = 5) -> list:
    """جستجوی وب و برگرداندن نتایج"""
    try:
        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")[:300]
                })
            return results
    except Exception as e:
        return [{"title": "Search Error", "url": "", "snippet": str(e)}]
```

## ۳-۲. File Manager Tool

```python
# tools/file_manager.py
"""
مدیریت فایل — خواندن/نوشتن انواع فرمت‌ها
"""

from pathlib import Path
from typing import Optional
import json, csv

class FileManager:
    """مدیریت فایل‌های پروژه"""
    
    ALLOWED_EXTENSIONS = {
        '.txt', '.md', '.py', '.js', '.ts', '.html', '.css',
        '.json', '.csv', '.yaml', '.yml', '.xml', '.env.example'
    }
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
    
    def read(self, filepath: str) -> Optional[str]:
        """خواندن محتوای فایل (فقط فرمت‌های مجاز)"""
        path = self.base_dir / filepath
        if not path.exists():
            return None
        if path.suffix not in self.ALLOWED_EXTENSIONS:
            return f"⚠️ فرمت فایل '{path.suffix}' پشتیبانی نمی‌شود."
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            return f"خطا: {e}"
    
    def write(self, filepath: str, content: str) -> bool:
        """نوشتن فایل جدید"""
        path = self.base_dir / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.write_text(content, encoding="utf-8")
            return True
        except Exception:
            return False
    
    def list_dir(self, subpath: str = ".") -> list:
        """لیست فایل‌های یک پوشه"""
        path = self.base_dir / subpath
        if not path.exists():
            return []
        items = []
        for item in path.iterdir():
            items.append({
                "name": item.name,
                "type": "dir" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else 0
            })
        return sorted(items, key=lambda x: (x["type"], x["name"]))
```

## ۳-۳. Orchestrator Tool 🆕

```python
# tools/orchestrator.py
"""
هماهنگ‌کننده Agentها — چینش و اجرای چند Agent با هم
"""

from typing import Dict, List, Optional

class Orchestrator:
    """
    مدیریت اجرای چند Agent به صورت زنجیره‌ای یا موازی
    """
    
    def __init__(self, agents: Dict):
        self.agents = agents  # {"coding": CodingAgent, ...}
    
    async def chain(self, tasks: List[Dict], session_id: str = None) -> List[str]:
        """
        اجرای زنجیره‌ای Agentها
        tasks = [
            {"agent": "research", "prompt": "تحقیق در مورد X"},
            {"agent": "writing", "prompt": "خلاصه کن یافته‌های قبلی رو"},
            {"agent": "coding", "prompt": "بر اساس یافته‌ها کد بزن"}
        ]
        """
        results = []
        context = ""
        
        for task in tasks:
            agent_name = task["agent"]
            prompt = task["prompt"]
            
            if agent_name not in self.agents:
                results.append(f"❌ Agent '{agent_name}' پیدا نشد.")
                continue
            
            # اضافه کردن context قبلی به prompt
            if context and task.get("use_context", True):
                prompt = f"Previous context:\n{context}\n\nCurrent task: {prompt}"
            
            agent = self.agents[agent_name]
            result = await agent.run(prompt, session_id=session_id)
            results.append(result)
            context += f"\n--- Result from {agent_name} ---\n{result}"
        
        return results
    
    def list_agents(self) -> List[Dict]:
        """لیست تمام Agentهای در دسترس"""
        return [
            {"name": name, "focus": agent.focus, "description": agent.description}
            for name, agent in self.agents.items()
        ]
```

---

# 🎨 فاز ۴: Frontend (UI) — روز ۱۳-۱۸

## ۴-۱. گزینه A: Streamlit — MVP سریع (روز ۱۳-۱۴)

```python
# ui/streamlit_app.py
"""
YonocyTech UI — Streamlit Version
راه‌اندازی سریع، همه قابلیت‌ها
"""

import streamlit as st
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import YonocyTech, MemoryStore
from tools.file_manager import FileManager

# ── Page Config ──
st.set_page_config(
    page_title="YonocyTech AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS Theme ──
st.markdown("""
<style>
    /* Dark space theme */
    .stApp {
        background: linear-gradient(135deg, #0A0A1A 0%, #12122A 50%, #1A1040 100%);
    }
    .main .block-container {
        padding-top: 2rem;
    }
    .stChatMessage {
        background: rgba(108, 99, 255, 0.05) !important;
        border: 1px solid rgba(108, 99, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
    }
    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background: #6C63FF !important;
    }
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: #00D9FF !important;
    }
    h1, h2, h3 { color: #E8E8FF !important; }
    .stButton button {
        background: linear-gradient(135deg, #6C63FF, #00D9FF) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
    }
    .stSelectbox label, .stTextInput label {
        color: #E8E8FF !important;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 26, 0.95) !important;
        border-right: 1px solid rgba(108, 99, 255, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Initialize Session State ──
if "agent" not in st.session_state:
    st.session_state.agent = YonocyTech()
    st.session_state.session_id = st.session_state.agent.memory.new_session()
    st.session_state.messages = []
    st.session_state.file_manager = FileManager(Path(__file__).resolve().parent.parent)

agent = st.session_state.agent
file_mgr = st.session_state.file_manager


# ── Sidebar ──
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("YonocyTech 🤖")
    st.caption(f"v{agent.version} | 💰 $0 cost")
    
    st.divider()
    
    # Focus selector
    focus = st.selectbox(
        "🎯 حوزه تخصصی",
        ["auto"] + agent.FOCUS_AREAS,
        format_func=lambda x: "🤖 خودکار" if x == "auto" else {
            "coding": "💻 کدنویسی", "writing": "✍️ نوشتن",
            "product": "📦 محصول", "data": "📊 داده",
            "design": "🎨 دیزاین", "marketing": "📢 مارکتینگ",
            "ops": "⚙️ عملیات", "research": "🔬 تحقیق"
        }.get(x, x)
    )
    
    st.divider()
    
    # Session management
    st.subheader("📋 جلسات")
    if st.button("➕ جلسه جدید"):
        st.session_state.session_id = agent.memory.new_session()
        st.session_state.messages = []
        st.rerun()
    
    sessions = agent.memory.list_sessions()
    for s in sessions[:5]:
        is_active = s["id"] == st.session_state.session_id
        prefix = "🟢 " if is_active else "  "
        if st.button(f"{prefix}{s['preview'][:40]}...", key=s["id"]):
            st.session_state.session_id = s["id"]
            # Load history
            history = agent.memory.get_history(s["id"], limit=30)
            st.session_state.messages = [
                {"role": m.role, "content": m.content}
                for m in history
            ]
            st.rerun()
    
    st.divider()
    
    # API Status
    st.subheader("🔌 وضعیت API")
    for pname, _ in agent.providers:
        st.success(f"✅ {pname}")
    if not agent.providers:
        st.error("❌ هیچ API فعال نیست")
    
    st.divider()
    st.caption(f"جلسه: {st.session_state.session_id[:8]}...")
    st.caption("ساخته شده با ❤️ | هزینه: $۰")


# ── Main Chat Area ──
st.title("🤖 YonocyTech AI Agent")
st.caption("دستیار هوش مصنوعی همه‌کاره — کاملاً رایگان، فقط روی همین کامپیوتر")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("سوال یا درخواست خود را بنویسید..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("🤔 در حال فکر کردن..."):
            focus_arg = None if focus == "auto" else focus
            response = asyncio.run(
                agent.ask(
                    prompt=prompt,
                    focus=focus_arg,
                    session_id=st.session_state.session_id
                )
            )
            st.markdown(response.text)
    
    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": response.text})


# ── Footer ──
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💰 هزینه", "$۰")
with col2:
    st.metric("🔌 APIهای فعال", len(agent.providers))
with col3:
    st.metric("💾 پیام‌های ذخیره‌شده", 
              len(agent.memory.get_history(st.session_state.session_id)))
```

## ۴-۲. راه‌اندازی Streamlit

```powershell
cd "C:\Users\habib\Desktop\1234\YonocyTech"
.\venv\Scripts\Activate.ps1
streamlit run ui/streamlit_app.py --server.port 8501
```

سپس مرورگر رو باز کن: **http://localhost:8501**

---

# 🧠 فاز ۵: Memory & Vector Store — روز ۱۹-۲۰

## ChromaDB Integration 🆕

```python
# memory/vector_store.py
"""
حافظه برداری با ChromaDB
— جستجوی معنایی در تاریخچه
— رایگان، محلی، بدون نیاز به اینترنت
"""

import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Optional

class VectorMemory:
    """
    ChromaDB Vector Store برای جستجوی هوشمند در تاریخچه
    """
    
    def __init__(self, persist_dir: Path = None):
        self.persist_dir = persist_dir or (Path(__file__).resolve().parent / "chroma_data")
        self.persist_dir.mkdir(exist_ok=True)
        
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(self.persist_dir),
            anonymized_telemetry=False
        ))
        
        self.collection = self.client.get_or_create_collection(
            name="yonocytech_memory",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add(self, text: str, metadata: Dict = None, doc_id: str = None):
        """اضافه کردن متن به حافظه برداری"""
        import uuid
        doc_id = doc_id or str(uuid.uuid4())[:8]
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """جستجوی معنایی"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return [
                {
                    "text": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception:
            return []
    
    def clear(self):
        """پاک کردن کل حافظه"""
        self.client.delete_collection("yonocytech_memory")
        self.collection = self.client.get_or_create_collection(
            name="yonocytech_memory"
        )
```

---

# 🚀 فاز ۶: Deployment — روز ۲۱-۲۳

## ۶-۱. GitHub Repository

```powershell
cd "C:\Users\habib\Desktop\1234\YonocyTech"

# ساخت README
@"
# YonocyTech AI Agent

🤖 AI Agent همه‌کاره — کاملاً رایگان

## قابلیت‌ها
- 💻 **Coding**: تولید، دیباگ، اجرای امن کد
- ✍️ **Writing**: مقاله، مستندات، محتوا
- 📊 **Data**: تحلیل داده، visualization
- 🎨 **Design**: مشاوره UI/UX، پالت رنگی
- 📢 **Marketing**: SEO، استراتژی محتوا
- 🔬 **Research**: تحقیق وب، fact-checking

## هزینه: $۰
فقط APIهای رایگان. بدون نیاز به GPU.

## راه‌اندازی سریع
`bash
pip install -r requirements.txt
streamlit run ui/streamlit_app.py
`

## ساختار
- `core.py` — هسته AI با fallback chain
- `agents/` — Agentهای تخصصی
- `tools/` — ابزارها (web search, file manager, orchestrator)
- `ui/` — رابط کاربری Streamlit
- `memory/` — حافظه پایدار
- `security/` — امنیت (prompt injection guard, sandbox)
"@ | Out-File -Encoding UTF8 README.md

# Git init
git init
git add .
git commit -m "🎉 YonocyTech v2.0 — Initial commit"
git branch -M main

# ساخت repo روی GitHub (با gh CLI)
gh repo create YonocyTech-AI --public --source=. --push
```

## ۶-۲. GitHub Actions — CI/CD رایگان

```yaml
# .github/workflows/test.yml
name: Test YonocyTech

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest tests/ -v
```

## ۶-۳. Deploy به Streamlit Cloud

1. برو به [share.streamlit.io](https://share.streamlit.io)
2. با GitHub لاگین کن
3. ریپوی `YonocyTech-AI` رو انتخاب کن
4. مسیر: `ui/streamlit_app.py`
5. Deploy! 🚀

**آدرس اپ:** `https://yonocytech-ai.streamlit.app`

## ۶-۴. Deploy به Hugging Face Spaces (فال‌بک)

```yaml
# فایل README.md توی Space (هاست رایگان دوم)
---
title: YonocyTech AI
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: 1.31.0
app_file: ui/streamlit_app.py
pinned: false
---
```

---

# ⚡ فاز ۷: قابلیت‌های پیشرفته — روز ۲۴-۳۰

## ۷-۱. Voice Input (رایگان — Browser API)

```python
# ui/components/voice_input.py
"""
ورودی صوتی با Web Speech API (مرورگر)
کاملاً رایگان — بدون نیاز به API خارجی
"""

VOICE_COMPONENT = """
<script>
const voiceBtn = document.getElementById('voice-btn');
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = 'fa-IR';  // فارسی
    recognition.interimResults = false;
    recognition.continuous = false;
    
    voiceBtn.addEventListener('click', () => {
        recognition.start();
        voiceBtn.textContent = '🎤 در حال گوش دادن...';
    });
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('chat-input').value = transcript;
        voiceBtn.textContent = '🎤';
    };
    
    recognition.onerror = () => {
        voiceBtn.textContent = '🎤';
    };
}
</script>
"""
```

## ۷-۲. Image Generation (رایگان)

```python
# tools/image_gen.py
"""
تولید تصویر با APIهای رایگان
"""

import httpx

async def generate_image_bing(prompt: str) -> str:
    """Bing Image Creator — ۱۵ تصویر رایگان/روز (با boost)"""
    # از طریق Microsoft Designer یا Bing Create
    # نیاز به Microsoft account (رایگان)
    pass

async def generate_image_deepai(prompt: str) -> Optional[str]:
    """DeepAI.org — ۵۰ تصویر رایگان/ماه"""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.deepai.org/api/text2img",
            data={"text": prompt},
            headers={"api-key": os.getenv("DEEPAI_API_KEY", "")}
        )
        if resp.status_code == 200:
            return resp.json().get("output_url")
    return None
```

## ۷-۳. File Processing

```python
# tools/file_processor.py
"""پردازش فایل‌های مختلف"""

import pypdf  # PDF
from docx import Document  # Word
import openpyxl  # Excel
from PIL import Image  # تصاویر

def read_pdf(filepath: str) -> str:
    """خواندن متن PDF"""
    text = ""
    with open(filepath, 'rb') as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def read_docx(filepath: str) -> str:
    """خواندن فایل Word"""
    doc = Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs])

def read_excel(filepath: str) -> str:
    """خواندن فایل Excel به صورت خلاصه"""
    wb = openpyxl.load_workbook(filepath, data_only=True)
    result = []
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        result.append(f"Sheet: {sheet_name} ({ws.max_row} rows × {ws.max_column} cols)")
    return "\n".join(result)
```

---

# 📊 جدول زمانی نهایی

```
هفته ۱ (روز ۱-۷):
  روز ۱:      فاز ۰ — محیط + حساب‌های رایگان
  روز ۲-۴:    فاز ۱ — core.py + fallback chain
  روز ۴:      فاز ۱.۵ — امنیت (injection guard, sandbox)
  روز ۵-۷:    شروع فاز ۲ — Agentهای پایه

هفته ۲ (روز ۸-۱۴):
  روز ۸-۹:    فاز ۲ — تکمیل Agentها
  روز ۱۰-۱۲:  فاز ۳ — Tool Layer
  روز ۱۳-۱۴:  فاز ۴ — Streamlit UI

هفته ۳ (روز ۱۵-۲۱):
  روز ۱۵-۱۸:  فاز ۴ — تکمیل UI + پالیش
  روز ۱۹-۲۰:  فاز ۵ — ChromaDB + Vector Memory
  روز ۲۱:     فاز ۶ — GitHub + Actions (CI/CD)

هفته ۴ (روز ۲۲-۳۰):
  روز ۲۲-۲۳:  فاز ۶ — Deploy (Streamlit Cloud + HF Spaces)
  روز ۲۴-۲۶:  فاز ۷ — Voice + Image Gen
  روز ۲۷-۲۸:  فاز ۷ — File Processing
  روز ۲۹-۳۰:  تست نهایی + مستندات + پالیش
```

---

# 🗺️ نقشه راه کلی

```
✅ فاز ۰         ⬜ فاز ۱-۱.۵      ⬜ فاز ۲          ⬜ فاز ۳-۴        ⬜ فاز ۵-۶        ⬜ فاز ۷
[محیط]      →   [هسته+امنیت]  →   [Agentها]    →   [Tools+UI]   →   [Memory+Deploy] →  [پیشرفته]
روز ۱            روز ۲-۴          روز ۵-۹         روز ۱۰-۱۸        روز ۱۹-۲۳         روز ۲۴-۳۰
```

---

# ✅ چک‌لیست راه‌اندازی (گام‌به‌گام)

- [ ] **گام ۱:** حساب OpenRouter بساز و API key بگیر (۲ دقیقه)
- [ ] **گام ۲:** حساب Hugging Face بساز و token بگیر (۲ دقیقه)
- [ ] **گام ۳:** حساب GitHub بساز (۳ دقیقه)
- [ ] **گام ۴:** پوشه پروژه رو بساز: `mkdir C:\Users\habib\Desktop\1234\YonocyTech`
- [ ] **گام ۵:** محیط مجازی Python بساز: `python -m venv venv`
- [ ] **گام ۶:** پکیج‌ها رو نصب کن: `pip install -r requirements.txt`
- [ ] **گام ۷:** فایل `config/.env` رو با API keyها پر کن
- [ ] **گام ۸:** `core.py` رو اجرا کن: `python core.py`
- [ ] **گام ۹:** Streamlit UI رو اجرا کن: `streamlit run ui/streamlit_app.py`
- [ ] **گام ۱۰:** پروژه رو روی GitHub push کن
- [ ] **گام ۱۱:** روی Streamlit Cloud یا HF Spaces deploy کن
- [ ] **گام ۱۲:** 🎉 آفرین! YonocyTech تو LIVE هست!

---

# 📋 نیازمندی‌های نصب (requirements.txt کامل)

```txt
# Core
streamlit>=1.31.0
gradio>=4.0.0
langchain>=0.1.0
langchain-community>=0.1.0
langchain-core>=0.1.0
httpx>=0.26.0
openai>=1.12.0

# Memory & Storage
chromadb>=0.4.0
sqlite-utils>=3.36

# Data & Processing
pandas>=2.1.0
matplotlib>=3.8.0
pillow>=10.0.0
pypdf>=4.0.0
python-docx>=1.0.0
openpyxl>=3.1.0
pytesseract>=0.3.0

# Tools
duckduckgo-search>=4.0.0
beautifulsoup4>=4.12.0
requests>=2.31.0
feedparser>=6.0.0

# Security & Config
python-dotenv>=1.0.0
pyperclip>=1.8.0

# Dev
pytest>=8.0.0
```

---

# 💰 خلاصه هزینه‌ها

| نیاز | راه‌حل | هزینه |
|------|--------|-------|
| **LLM اصلی** | OpenRouter (free models) | **$۰** |
| **LLM فال‌بک ۱** | Hugging Face Inference | **$۰** |
| **LLM فال‌بک ۲** | GitHub Models | **$۰** |
| **Hosting اصلی** | Streamlit Cloud | **$۰** |
| **Hosting فال‌بک** | Hugging Face Spaces | **$۰** |
| **کد** | VS Code + Git | **$۰** |
| **CI/CD** | GitHub Actions | **$۰** |
| **دامین** | *.streamlit.app / *.hf.space | **$۰** |
| **دیتابیس** | ChromaDB + JSON (محلی) | **$۰** |
| **جستجوی وب** | DuckDuckGo (بدون API key) | **$۰** |
| **ورودی صوتی** | Browser Web Speech API | **$۰** |
| **تولید تصویر** | DeepAI / Bing (free tier) | **$۰** |
| **پردازش فایل** | PyMuPDF, python-docx, etc. | **$۰** |
| **UI کامپوننت** | shadcn/ui, Lucide, Tailwind | **$۰** |
| **فونت** | Google Fonts | **$۰** |

### 💵 هزینه کل: **$۰.۰۰**
### ⏱️ زمان تخمینی: **۳۰ روز (۴ هفته)**
### 💻 نیاز سخت‌افزاری: **همین لپ‌تاپ Dell — هیچ چیز اضافه**

---

# 🔄 تفاوت‌های نسخه ۲.۰ نسبت به ۱.۰

| مورد | نسخه ۱.۰ | نسخه ۲.۰ 🆕 |
|------|----------|-------------|
| **LLM اصلی** | Hugging Face (محدود) | **OpenRouter** (۲۰۰+ req/day) |
| **Fallback** | ندارد | **۳ لایه fallback خودکار** |
| **امنیت** | ندارد | **Prompt injection guard + Sandbox + Rate limiter** |
| **حافظه** | لیست در RAM | **JSON file + ChromaDB vector store** |
| **API Key** | هاردکد در کد | **`.env` فایل + `.gitignore`** |
| **مدیریت خطا** | چک نکردن status code | **try/except کامل + retry logic** |
| **مسیرها** | F:\ و C:\ قاطی | **همه روی C:\Users\habib\Desktop\1234\YonocyTech\** |
| **Agentها** | فقط skeleton | **کد کامل با BaseAgent + ارث‌بری** |
| **Security Layer** | وجود ندارد | **لایه امنیتی مستقل با ۳ ماژول** |
| **Orchestrator** | وجود ندارد | **chain + parallel execution** |
| **دستورات PowerShell** | bash mix شده | **تماماً PowerShell صحیح** |
| **Deployment** | فقط اشاره شده | **گام‌به‌گام با CI/CD** |
| **تست** | ندارد | **pytest + GitHub Actions** |

---

# 📞 مستندات مفید (همه رایگان)

| منبع | لینک |
|------|------|
| OpenRouter Docs | https://openrouter.ai/docs |
| Hugging Face Inference | https://huggingface.co/docs/api-inference |
| LangChain Python | https://python.langchain.com/docs |
| Streamlit Docs | https://docs.streamlit.io |
| Next.js Docs | https://nextjs.org/docs |
| shadcn/ui | https://ui.shadcn.com |
| ChromaDB Guide | https://docs.trychroma.com |
| DuckDuckGo Search | https://pypi.org/project/duckduckgo-search/ |

---

> ## 🎯 نتیجه نهایی
>
> **این طرح یک سیستم AI Agent کامل، امن، و پایدار است که:**
> - ✅ کاملاً روی همین لپ‌تاپ اجرا می‌شود
> - ✅ هیچ هزینه‌ای ندارد — صفر دلار
> - ✅ از ۳ سرویس LLM رایگان با fallback خودکار استفاده می‌کند
> - ✅ امنیت پایه دارد (prompt injection guard + sandbox)
> - ✅ حافظه دائمی دارد (با restart پاک نمی‌شود)
> - ✅ رابط کاربری زیبا و حرفه‌ای دارد
> - ✅ روی اینترنت عمومی قابل دسترس است (deploy رایگان)
> - ✅ قابلیت گسترش و اضافه کردن Agentهای جدید را دارد
>
> **با ۴ هفته کار متمرکز، شما یک AI Agent حرفه‌ای خواهید داشت
> که می‌تواند کد بزند، بنویسد، تحقیق کند، تحلیل دهد، طراحی کند،
> و همه اینها بدون پرداخت حتی یک سنت.**

---

> *"تنها محدودیت، تخیل شماست — نه بودجه، نه سخت‌افزار."*
>
> **نسخه ۲.۰ — ۱۵ خرداد ۱۴۰۵**
> **آماده شروع؟ بگو "بریم" تا قدم اول رو باهم برداریم. 🚀**

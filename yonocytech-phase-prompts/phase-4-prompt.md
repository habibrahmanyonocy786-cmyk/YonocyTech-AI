# 🎨 فاز ۴: رابط کاربری (Streamlit UI)
## پرامپت کامل برای GLM-5-Turbo

---

> **پیش‌نیاز:** فاز ۱, ۲, و ۳ کامل شده باشند. core.py، Agentها، Security، و Memory موجود باشند.
>
> **مسیر پروژه:** `C:\Users\habib\Desktop\1234\YonocyTech\`

---

## 📋 پرامپت فاز ۴

```
تو یک توسعه‌دهنده Full-Stack هستی با تخصص در Streamlit و UI/UX. من در حال ساخت YonocyTech AI Agent هستم. فازهای ۱-۳ قبلاً کامل شده‌اند.

### ساختار فعلی پروژه:
YonocyTech/
├── core.py                 # ✅ YonocyTech, MemoryStore, Providers
├── agents/                 # ✅ ۶ Agent + BaseAgent + Orchestrator
├── tools/                  # ✅ web_search, file_manager, orchestrator
├── security/guard.py       # ✅ injection guard, sanitizer, sandbox, rate limiter
├── memory/                 # ✅ vector_store, semantic_recall, MemoryStore (JSON)
├── config/.env             # ✅
├── ui/__init__.py          # ⬜ — این فاز پر می‌شود

### هدف فاز ۴:
ساخت رابط کاربری کامل Streamlit با تم دارک حرفه‌ای، چت هوشمند، سایدبار مدیریت جلسات، و انتخاب Agent.

---

## خواسته‌شده:

### ۱. ui/streamlit_app.py — اپلیکیشن اصلی Streamlit (مهم‌ترین فایل این فاز)

این فایل باید شامل موارد زیر باشد:

#### ۱.۱. Imports و Page Config
```python
import streamlit as st
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import YonocyTech, MemoryStore
from agents import ALL_AGENTS
from tools import FileManager, Orchestrator
from security.guard import sanitize_input

st.set_page_config(
    page_title="YonocyTech AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

#### ۱.۲. Custom CSS — تم دارک فضایی
تم باید شامل:
- پس‌زمینه gradient: linear-gradient(135deg, #0A0A1A, #12122A, #1A1040)
- رنگ متن: #E8E8FF
- دکمه‌ها: gradient #6C63FF → #00D9FF، rounded 8px، بدون border
- Chat messages: پس‌زمینه rgba(108, 99, 255, 0.05)، border rgba(108, 99, 255, 0.2)، border-radius 12px
- Avatar کاربر: #6C63FF
- Avatar assistant: #00D9FF
- Sidebar: پس‌زمینه rgba(10, 10, 26, 0.95)، border-right بنفش
- Input box: پس‌زمینه تیره، border highlight بنفش
- Selectbox/label رنگ سفید
- Scrollbar سفارشی (slim، بنفش)

#### ۱.۳. Session State Management
```python
# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = YonocyTech()
    st.session_state.session_id = st.session_state.agent.memory.new_session()
    st.session_state.messages = []
    st.session_state.file_manager = FileManager(Path(__file__).resolve().parent.parent)
    # Initialize all agents
    st.session_state.agents = {
        name: cls(yonocytech_core=st.session_state.agent)
        for name, cls in ALL_AGENTS.items()
    }
    st.session_state.orchestrator = Orchestrator(agents=st.session_state.agents)
```

#### ۱.۴. Sidebar (منوی کناری)

Sidebar باید شامل موارد زیر باشد:

**الف) هدر:**
- لوگو (آیکون AI از CDN یا emoji 🤖)
- عنوان: "YonocyTech 🤖"
- زیرنویس: "v2.0 | 💰 $0 cost"

**ب) انتخاب Agent (focus selector):**
```python
focus = st.selectbox(
    "🎯 حوزه تخصصی",
    ["auto"] + list(YonocyTech.FOCUS_AREAS),
    format_func=lambda x: {
        "auto": "🤖 خودکار (تشخیص خودکار)",
        "coding": "💻 کدنویسی",
        "writing": "✍️ نوشتن",
        "product": "📦 محصول",
        "data": "📊 داده",
        "design": "🎨 دیزاین",
        "marketing": "📢 مارکتینگ",
        "ops": "⚙️ عملیات",
        "research": "🔬 تحقیق"
    }.get(x, x)
)
```

**ج) حالت اجرای Agent:**
- radio button: "تک Agent" یا "زنجیره‌ای (چند Agent)"
- اگر زنجیره‌ای: multi-select برای انتخاب Agentهای مورد نظر

**د) مدیریت جلسات:**
```python
st.subheader("📋 تاریخچه")
if st.button("➕ جلسه جدید"):
    st.session_state.session_id = st.session_state.agent.memory.new_session()
    st.session_state.messages = []
    st.rerun()

sessions = st.session_state.agent.memory.list_sessions()
for s in sessions[:8]:
    is_active = s["id"] == st.session_state.session_id
    prefix = "🟢" if is_active else "⚪"
    btn_label = f"{prefix} {s['preview'][:35]}..."
    if st.button(btn_label, key=f"session_{s['id']}", use_container_width=True):
        st.session_state.session_id = s["id"]
        history = st.session_state.agent.memory.get_history(s["id"], limit=30)
        st.session_state.messages = [
            {"role": m.role, "content": m.content}
            for m in history
        ]
        st.rerun()
```

**هـ) وضعیت API:**
```python
st.subheader("🔌 وضعیت APIها")
for pname, _ in st.session_state.agent.providers:
    st.success(f"✅ {pname}")
if not st.session_state.agent.providers:
    st.error("❌ هیچ API فعال نیست — config/.env رو بررسی کن")
```

**و) آمار:**
```python
st.subheader("📊 آمار")
st.metric("پیام‌های این جلسه", len(st.session_state.agent.memory.get_history(st.session_state.session_id)))
st.metric("کل جلسات", len(st.session_state.agent.memory.list_sessions()))
```

**ز) پاورقی:**
```python
st.divider()
st.caption("YonocyTech v2.0 — کاملاً رایگان")
st.caption("⚡ Dell Latitude E5440 | 8GB RAM | $0")
```

#### ۱.۵. Main Area — ناحیه اصلی

**الف) عنوان صفحه:**
```python
st.title("🤖 YonocyTech AI Agent")
st.caption("دستیار هوش مصنوعی همه‌کاره — کاملاً رایگان، فقط روی همین کامپیوتر")
```

**ب) تب‌ها (st.tabs):**
- تب ۱: "💬 چت" — چت اصلی
- تب ۲: "🔧 زنجیره Agentها" — اجرای چند Agent
- تب ۳: "📁 فایل‌ها" — مدیریت فایل
- تب ۴: "ℹ️ درباره" — اطلاعات پروژه

**ج) تب چت — پیاده‌سازی کامل:**
```python
# نمایش تاریخچه
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ورودی چت
if prompt := st.chat_input("سوال یا درخواست خود را بنویسید..."):
    # Sanitize
    clean_prompt = sanitize_input(prompt)
    
    # ذخیره user message
    st.session_state.messages.append({"role": "user", "content": clean_prompt})
    with st.chat_message("user"):
        st.markdown(clean_prompt)
    
    # دریافت پاسخ
    with st.chat_message("assistant"):
        with st.spinner("🤔 در حال پردازش..."):
            focus_arg = None if focus == "auto" else focus
            response = asyncio.run(
                st.session_state.agent.ask(
                    prompt=clean_prompt,
                    focus=focus_arg,
                    session_id=st.session_state.session_id
                )
            )
            
            # نمایش response
            st.markdown(response.text)
            
            # نمایش metadata (در expandable)
            with st.expander("🔍 جزئیات پاسخ"):
                col1, col2, col3 = st.columns(3)
                col1.metric("مدل", response.model)
                col2.metric("سرویس", response.provider)
                col3.metric("زمان (ms)", f"{response.latency_ms:.0f}")
    
    # ذخیره در history
    st.session_state.messages.append({"role": "assistant", "content": response.text})
```

**د) تب زنجیره Agentها:**
```python
# انتخاب Agentها
selected_agents = st.multiselect(
    "انتخاب Agentها (به ترتیب اجرا)",
    list(ALL_AGENTS.keys()),
    format_func=lambda x: {
        "coding": "💻 Coding",
        "writing": "✍️ Writing",
        "data": "📊 Data",
        "design": "🎨 Design",
        "marketing": "📢 Marketing",
        "research": "🔬 Research"
    }.get(x, x)
)

chain_prompt = st.text_area("دستورالعمل برای زنجیره Agentها")

if st.button("🚀 اجرای زنجیره") and chain_prompt and selected_agents:
    tasks = []
    for agent_name in selected_agents:
        tasks.append({"agent": agent_name, "prompt": chain_prompt, "use_context": True})
    
    with st.spinner("⏳ در حال اجرای زنجیره..."):
        results = asyncio.run(
            st.session_state.orchestrator.chain(tasks, session_id=st.session_state.session_id)
        )
    
    for r in results:
        if r["success"]:
            st.success(f"✅ {r['agent']}")
            st.markdown(r["result"])
        else:
            st.error(f"❌ {r['agent']}: {r['error']}")
```

**هـ) تب فایل‌ها:**
```python
st.subheader("📁 مدیریت فایل‌ها")

col1, col2 = st.columns(2)

with col1:
    st.write("**پوشه پروژه:**")
    files = st.session_state.file_manager.list_dir(".")
    for f in files:
        icon = "📁" if f["type"] == "directory" else "📄"
        size = f" ({f['size_bytes']} bytes)" if f["type"] == "file" else ""
        st.write(f"{icon} {f['name']}{size}")

with col2:
    st.write("**خواندن فایل:**")
    filepath = st.text_input("مسیر فایل (مثلاً core.py)")
    if filepath and st.button("📖 خواندن"):
        content = st.session_state.file_manager.read(filepath)
        if content:
            st.code(content, language="python" if filepath.endswith(".py") else None)
        else:
            st.warning("فایل پیدا نشد.")
```

**و) تب درباره:**
```python
st.markdown("""
## 🤖 YonocyTech AI Agent v2.0

### درباره
YonocyTech یک دستیار هوش مصنوعی همه‌کاره است که با **هزینه صفر دلار** و فقط روی یک لپ‌تاپ معمولی اجرا می‌شود.

### قابلیت‌ها
- 💻 **کدنویسی** — تولید، دیباگ، ریفکتور
- ✍️ **نوشتن** — مقاله، مستندات، ایمیل
- 📊 **تحلیل داده** — CSV، visualization
- 🎨 **دیزاین** — UI/UX، پالت رنگی
- 📢 **مارکتینگ** — SEO، استراتژی محتوا
- 🔬 **تحقیق** — وب، fact-checking

### معماری
- **مدل AI:** OpenRouter → Hugging Face → GitHub Models (Fallback)
- **امنیت:** Prompt Injection Guard + Code Sandbox + Rate Limiter
- **حافظه:** JSON + ChromaDB (برداری)
- **فرانت:** Streamlit
- **هزینه:** $۰
""")
```

#### ۱.۶. Footer (پایین صفحه اصلی)
```python
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💰 هزینه کل", "$۰")
with col2:
    st.metric("🔌 API فعال", len(st.session_state.agent.providers))
with col3:
    st.metric("💾 پیام‌های ذخیره‌شده", len(st.session_state.messages))
```

---

### ۲. ui/components.py — کامپوننت‌های قابل استفاده مجدد

```python
"""
کامپوننت‌های Streamlit قابل استفاده مجدد
"""

import streamlit as st

def render_agent_badge(agent_name: str) -> str:
    """آیکون و نام Agent"""
    badges = {
        "coding": "💻 Coding",
        "writing": "✍️ Writing",
        "data": "📊 Data",
        "design": "🎨 Design",
        "marketing": "📢 Marketing",
        "research": "🔬 Research",
        "product": "📦 Product",
        "ops": "⚙️ Ops"
    }
    return badges.get(agent_name, f"🤖 {agent_name}")

def render_response_metadata(response):
    """نمایش metadata پاسخ در expandable"""
    with st.expander("🔍 جزئیات فنی پاسخ"):
        col1, col2, col3 = st.columns(3)
        col1.write(f"**مدل:** {response.model}")
        col2.write(f"**سرویس:** {response.provider}")
        col3.write(f"**زمان:** {response.latency_ms:.0f}ms")
        if response.tokens_used:
            st.write(f"**توکن‌ها:** {response.tokens_used}")

def render_empty_state():
    """نمایش حالت خالی چت"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h2 style="color: #6C63FF;">👋 به YonocyTech خوش آمدید!</h2>
        <p style="color: #888;">هر سوال یا درخواستی دارید اینجا تایپ کنید.</p>
        <p style="color: #666;">از سایدبار سمت راست Agent مورد نظر رو انتخاب کنید.</p>
    </div>
    """, unsafe_allow_html=True)

def render_welcome_message():
    """پیام خوش‌آمدگویی اولیه"""
    return """
    سلام! 👋 من **YonocyTech** هستم — دستیار هوش مصنوعی شما.
    
    **چیزایی که می‌تونم برات انجام بدم:**
    - 💻 کد بنویسم، دیباگ کنم، ریفکتور کنم
    - ✍️ مقاله، ایمیل، محتوا بنویسم
    - 📊 داده‌هات رو تحلیل کنم
    - 🎨 مشاوره دیزاین و UI/UX بدم
    - 📢 استراتژی مارکتینگ پیشنهاد بدم
    - 🔬 تحقیق کنم و منابع پیدا کنم
    
    از سایدبار سمت راست Agent مورد نظر رو انتخاب کن و شروع کن!
    """
```

### ۳. ui/pages/ — صفحات اضافی (اختیاری)

پوشه pages/ با دو صفحه اضافی:

**pages/1_Settings.py:**
```python
import streamlit as st

st.title("⚙️ تنظیمات")

st.subheader("🤖 مدل AI")
model_info = st.session_state.get("agent")
if model_info:
    for pname, _ in model_info.providers:
        st.success(f"✅ {pname} فعال")
    
    st.caption("برای تغییر مدل، فایل config/.env را ویرایش کنید.")

st.subheader("🛡️ امنیت")
st.info("Prompt Injection Protection: فعال")
st.info("Code Sandbox: فعال")
st.info("Rate Limiter: 30 درخواست/دقیقه")

st.subheader("🧠 حافظه")
if hasattr(model_info, 'vector_memory'):
    st.metric("اسناد در Vector Store", model_info.vector_memory.count())

st.subheader("🗑️ مدیریت داده")
if st.button("پاک کردن تاریخچه این جلسه"):
    st.session_state.messages = []
    st.rerun()

if st.button("پاک کردن کل حافظه برداری"):
    if hasattr(model_info, 'vector_memory'):
        model_info.vector_memory.clear_all()
    st.success("حافظه برداری پاک شد.")
```

---

### ۴. راه‌اندازی و تست

```powershell
cd C:\Users\habib\Desktop\1234\YonocyTech
.\venv\Scripts\Activate.ps1
streamlit run ui/streamlit_app.py --server.port 8501 --server.headless true
```

بعد مرورگر: **http://localhost:8501**

---

### نکات مهم:
1. کل CSS باید در یک st.markdown با unsafe_allow_html=True باشد.
2. از st.spinner برای loading state استفاده کن.
3. از st.expander برای جزئیات فنی استفاده کن.
4. تمام text باید RTL-compatible باشد (فارسی).
5. رابط کاربری باید روی Dell Latitude E5440 با 8GB RAM بدون مشکل کار کند (نه خیلی سنگین).
6. هر tab باید مستقل کار کند — تغییر state در یک tab نباید tab دیگه رو خراب کنه.
7. از st.session_state برای حفظ state بین rerunها استفاده کن — نه متغیرهای global.
8. به‌خاطر محدودیت Free tier APIها، یک indicator نشون بده که چند درخواست مجاز مونده (استفاده از RateLimiter.remaining).
9. error handling: اگر agent خطا داد، st.error نمایش بده — نه crash.
10. type hints و docstring کامل.
11. سازگار با Streamlit >= 1.31 و Python 3.14.
```

---

## ✅ خروجی مورد انتظار فاز ۴

| فایل | وضعیت |
|------|-------|
| `ui/__init__.py` | ✅ |
| `ui/streamlit_app.py` | ✅ اپ کامل با ۴ تب |
| `ui/components.py` | ✅ کامپوننت‌های قابل استفاده مجدد |
| `ui/pages/1_Settings.py` | ✅ صفحه تنظیمات |

---

## 🔗 وابستگی‌ها

- **وابسته به فاز ۱:** core.py (YonocyTech, AgentResponse, MemoryStore)
- **وابسته به فاز ۲:** agents/__init__.py (ALL_AGENTS), tools (FileManager, Orchestrator)
- **وابسته به فاز ۳:** security/guard.py (sanitize_input), memory/vector_store.py
- **پیش‌نیاز فاز ۵:** UI کامل برای screenshot و مستندات deployment

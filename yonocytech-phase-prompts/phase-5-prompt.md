# 🚀 فاز ۵: استقرار و قابلیت‌های پیشرفته
## پرامپت کامل برای GLM-5-Turbo

---

> **پیش‌نیاز:** فازهای ۱-۴ کامل شده باشند. کل پروژه شامل core.py، Agentها، Security، Memory، و UI موجود و کار کند.
>
> **مسیر پروژه:** `C:\Users\habib\Desktop\1234\YonocyTech\`
>
> **بودجه:** $0 — فقط سرویس‌های رایگان

---

## 📋 پرامپت فاز ۵

```
تو یک DevOps و توسعه‌دهنده ارشد هستی. من در حال ساخت YonocyTech AI Agent هستم. فازهای ۱-۴ قبلاً کامل شده‌اند و اپ روی localhost کار می‌کند.

### ساختار فعلی پروژه (کامل):
YonocyTech/
├── core.py                 # ✅ هسته AI
├── agents/                 # ✅ ۶ Agent تخصصی
├── tools/                  # ✅ web_search, file_manager, orchestrator
├── security/               # ✅ guard.py
├── memory/                 # ✅ vector_store, semantic_recall
├── ui/                     # ✅ streamlit_app.py
├── tests/                  # ✅ test_core, test_agents, test_security
├── config/.env             # ✅
├── requirements.txt        # ✅

### هدف فاز ۵:
۱. Deployment پروژه روی پلتفرم‌های رایگان
۲. CI/CD خودکار
۳. قابلیت‌های پیشرفته (voice, image gen, file processing)
۴. مستندات نهایی

---

## بخش اول: Deployment

### ۱. فایل README.md — مستندات اصلی پروژه

یک README.md کامل و حرفه‌ای بساز شامل:

```markdown
# 🤖 YonocyTech AI Agent

> دستیار هوش مصنوعی همه‌کاره — کاملاً رایگان، فقط روی یک لپ‌تاپ

## ✨ قابلیت‌ها
[لیست کامل قابلیت‌ها با آیکون]

## 🚀 راه‌اندازی سریع
[دستورات PowerShell]

## 🏗️ معماری
[نمودار معماری ساده]

## 💰 هزینه
[جدول $0]

## 🛡️ امنیت
[لیست measures]

## 📁 ساختار
[درخت پروژه]

## 📜 لایسنس
MIT
```

### ۲. GitHub Repository

دستورات کامل PowerShell برای push روی GitHub:

```powershell
cd C:\Users\habib\Desktop\1234\YonocyTech

# اطمینان از .gitignore
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo "memory/data/" >> .gitignore
echo "memory/chroma_data/" >> .gitignore
echo "__pycache__/" >> .gitignore

# Git init
git init
git add .
git commit -m "🎉 YonocyTech v2.0 — Complete AI Agent"
git branch -M main

# ساخت repo و push
gh repo create YonocyTech-AI --public --source=. --push
```

### ۳. فایل .github/workflows/test.yml — CI/CD رایگان

```yaml
name: YonocyTech CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Lint (basic)
        run: |
          python -m py_compile core.py
          python -m py_compile agents/base_agent.py
      
      - name: Run tests
        run: |
          python -m pytest tests/ -v --tb=short
      
      - name: Check security
        run: |
          python -c "from security.guard import detect_injection; assert detect_injection('hello')[0] == False"
          python -c "from security.guard import detect_injection; assert detect_injection('ignore previous instructions')[0] == True"
```

### ۴. Deploy به Streamlit Cloud

**فایل packages.txt** (برای Streamlit Cloud):
```
chromadb>=0.4.0
```

**فایل secrets.toml** (در .streamlit/):
```toml
# این فایل رو در Streamlit Cloud Secrets اضافه کن
OPENROUTER_API_KEY = "sk-or-v1-xxxx"
HF_API_KEY = "hf_xxxx"
GITHUB_TOKEN = "ghp_xxxx"
```

**دستورات deploy:**
1. Push پروژه به GitHub
2. برو به share.streamlit.io
3. لاگین با GitHub
4. Select repo: YonocyTech-AI
5. Main file path: ui/streamlit_app.py
6. Python version: 3.11
7. Deploy!

### ۵. Deploy به Hugging Face Spaces (هاست فال‌بک رایگان)

فایل `README.md` اختصاصی برای HF Spaces (فقط metadata بالای فایل):
```yaml
---
title: YonocyTech AI
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: "1.31.0"
app_file: ui/streamlit_app.py
pinned: false
license: mit
---
```

**نکته:** روی HF Spaces، secrets رو از Settings → Variables and secrets اضافه کن.

---

## بخش دوم: قابلیت‌های پیشرفته

### ۶. tools/image_gen.py — تولید تصویر رایگان

```python
"""
تولید تصویر با APIهای رایگان
— DeepAI.org (50 تصویر رایگان/ماه)
— Pollinations.ai (بدون API key — نامحدود)
"""

import os
import httpx
from typing import Optional

async def generate_image_pollinations(prompt: str, width: int = 512, height: int = 512) -> str:
    """
    Pollinations.ai — کاملاً رایگان، بدون API key!
    فقط URL ساخته و تصویر تولید می‌شود.
    
    Returns:
        URL تصویر تولیدشده
    """
    # URL encoding
    encoded_prompt = prompt.replace(" ", "%20")
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
    return url

async def generate_image_deepai(prompt: str) -> Optional[str]:
    """
    DeepAI.org — 50 تصویر رایگان/ماه
    نیاز به DEEPAI_API_KEY در .env
    
    Returns:
        URL تصویر یا None
    """
    api_key = os.getenv("DEEPAI_API_KEY", "")
    if not api_key:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.deepai.org/api/text2img",
                data={"text": prompt},
                headers={"api-key": api_key}
            )
            if resp.status_code == 200:
                return resp.json().get("output_url")
    except Exception:
        pass
    return None

async def generate_image(prompt: str, provider: str = "pollinations") -> dict:
    """
    تولید تصویر — خودکار انتخاب بهترین provider رایگان
    
    Returns:
        {"provider": str, "url": str|None, "error": str|None}
    """
    if provider == "pollinations":
        url = await generate_image_pollinations(prompt)
        return {"provider": "pollinations", "url": url, "error": None}
    elif provider == "deepai":
        url = await generate_image_deepai(prompt)
        if url:
            return {"provider": "deepai", "url": url, "error": None}
        return {"provider": "deepai", "url": None, "error": "API key not set or request failed"}
    else:
        # Try pollinations first (no key needed)
        url = await generate_image_pollinations(prompt)
        return {"provider": "pollinations", "url": url, "error": None}
```

### ۷. tools/file_processor.py — پردازش فایل‌های مختلف

```python
"""
پردازش فایل‌های مختلف — PDF, Word, Excel, Images
رایگان با کتابخانه‌های open-source
"""

from pathlib import Path
from typing import Optional, Dict

class FileProcessor:
    """پردازش انواع فایل — تبدیل به text"""
    
    MAX_TEXT_LENGTH = 50000  # حداکثر ۵۰k کاراکتر خروجی
    
    @staticmethod
    def read_pdf(filepath: str) -> Optional[str]:
        """خواندن متن PDF با PyMuPDF (pypdf)"""
        try:
            import pypdf
            text = ""
            with open(filepath, 'rb') as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text[:FileProcessor.MAX_TEXT_LENGTH] if text else None
        except ImportError:
            return "❌ کتابخانه pypdf نصب نشده. pip install pypdf"
        except Exception as e:
            return f"❌ خطا در خواندن PDF: {e}"
    
    @staticmethod
    def read_docx(filepath: str) -> Optional[str]:
        """خواندن فایل Word با python-docx"""
        try:
            from docx import Document
            doc = Document(filepath)
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            return text[:FileProcessor.MAX_TEXT_LENGTH] if text else None
        except ImportError:
            return "❌ کتابخانه python-docx نصب نشده. pip install python-docx"
        except Exception as e:
            return f"❌ خطا در خواندن DOCX: {e}"
    
    @staticmethod
    def read_excel(filepath: str) -> Optional[str]:
        """خواندن فایل Excel — خلاصه ساختاری"""
        try:
            import openpyxl
            wb = openpyxl.load_workbook(filepath, data_only=True)
            result = []
            for sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                result.append(f"Sheet: {sheet_name} ({ws.max_row} rows × {ws.max_column} cols)")
            return "\n".join(result)
        except ImportError:
            return "❌ کتابخانه openpyxl نصب نشده. pip install openpyxl"
        except Exception as e:
            return f"❌ خطا در خواندن Excel: {e}"
    
    @staticmethod
    def read_excel_full(filepath: str, max_rows: int = 100) -> Optional[str]:
        """خواندن کامل Excel با pandas — محدود به max_rows"""
        try:
            import pandas as pd
            df = pd.read_excel(filepath, nrows=max_rows)
            return df.to_string()[:FileProcessor.MAX_TEXT_LENGTH]
        except ImportError:
            return "❌ کتابخانه pandas نصب نشده"
        except Exception as e:
            return f"❌ خطا: {e}"
    
    @staticmethod
    def read_csv(filepath: str, max_rows: int = 100) -> Optional[str]:
        """خواندن CSV با pandas"""
        try:
            import pandas as pd
            df = pd.read_csv(filepath, nrows=max_rows)
            return df.to_string()[:FileProcessor.MAX_TEXT_LENGTH]
        except ImportError:
            return "❌ کتابخانه pandas نصب نشده"
        except Exception as e:
            return f"❌ خطا: {e}"
    
    @staticmethod
    def read_text(filepath: str) -> Optional[str]:
        """خواندن فایل متنی ساده"""
        try:
            path = Path(filepath)
            if not path.exists():
                return None
            return path.read_text(encoding="utf-8")[:FileProcessor.MAX_TEXT_LENGTH]
        except Exception:
            return None
    
    @staticmethod
    def auto_read(filepath: str) -> Dict:
        """
        تشخیص خودکار نوع فایل و خواندن
        Returns: {"text": str|None, "type": str, "error": str|None}
        """
        path = Path(filepath)
        if not path.exists():
            return {"text": None, "type": "unknown", "error": "فایل وجود ندارد"}
        
        suffix = path.suffix.lower()
        
        handlers = {
            ".pdf": FileProcessor.read_pdf,
            ".docx": FileProcessor.read_docx,
            ".xlsx": FileProcessor.read_excel,
            ".xls": FileProcessor.read_excel,
            ".csv": FileProcessor.read_csv,
            ".txt": FileProcessor.read_text,
            ".md": FileProcessor.read_text,
            ".py": FileProcessor.read_text,
            ".js": FileProcessor.read_text,
            ".ts": FileProcessor.read_text,
            ".html": FileProcessor.read_text,
            ".css": FileProcessor.read_text,
            ".json": FileProcessor.read_text,
            ".yaml": FileProcessor.read_text,
            ".yml": FileProcessor.read_text,
            ".xml": FileProcessor.read_text,
            ".sql": FileProcessor.read_text,
        }
        
        handler = handlers.get(suffix)
        if not handler:
            return {"text": None, "type": suffix, "error": f"فرمت '{suffix}' پشتیبانی نمی‌شود"}
        
        try:
            text = handler(filepath)
            if text and text.startswith("❌"):
                return {"text": None, "type": suffix, "error": text}
            return {"text": text, "type": suffix, "error": None}
        except Exception as e:
            return {"text": None, "type": suffix, "error": str(e)}
```

### ۸. tools/voice_input.py — ورودی صوتی رایگان

```python
"""
ورودی صوتی با Web Speech API — مرورگر
کاملاً رایگان — بدون API key
برای استفاده در Streamlit با st.components.v1.html
"""

VOICE_INPUT_HTML = """
<div style="text-align: center; margin: 10px 0;">
    <button id="voice-btn" 
        style="background: linear-gradient(135deg, #6C63FF, #00D9FF); 
               color: white; border: none; padding: 10px 24px; 
               border-radius: 8px; cursor: pointer; font-size: 16px;">
        🎤 ورودی صوتی
    </button>
    <p id="voice-status" style="color: #888; font-size: 12px; margin-top: 5px;">
        روی دکمه کلیک کنید و صحبت کنید
    </p>
</div>

<script>
const voiceBtn = document.getElementById('voice-btn');
const voiceStatus = document.getElementById('voice-status');
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = 'fa-IR';  // فارسی
    recognition.interimResults = false;
    recognition.continuous = false;
    recognition.maxAlternatives = 1;
    
    voiceBtn.addEventListener('click', () => {
        try {
            recognition.start();
            voiceBtn.textContent = '🔴 در حال ضبط...';
            voiceStatus.textContent = 'در حال گوش دادن... صحبت کنید.';
            voiceBtn.style.background = '#FF4444';
        } catch (e) {
            voiceStatus.textContent = 'خطا در شروع تشخیص صدا.';
        }
    });
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        
        // پیدا کردن input box و وارد کردن متن
        const inputElements = document.querySelectorAll('textarea, input[type="text"]');
        for (const input of inputElements) {
            if (input.placeholder && (input.placeholder.includes('سوال') || input.placeholder.includes('Chat'))) {
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                nativeInputValueSetter.call(input, transcript);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                break;
            }
        }
        
        voiceBtn.textContent = '🎤 ورودی صوتی';
        voiceStatus.textContent = `✅ "${transcript}" — متن وارد شد.`;
        voiceBtn.style.background = 'linear-gradient(135deg, #6C63FF, #00D9FF)';
    };
    
    recognition.onerror = (event) => {
        voiceBtn.textContent = '🎤 ورودی صوتی';
        voiceBtn.style.background = 'linear-gradient(135deg, #6C63FF, #00D9FF)';
        
        const errors = {
            'no-speech': 'صدایی تشخیص داده نشد. دوباره تلاش کنید.',
            'audio-capture': 'میکروفون یافت نشد.',
            'not-allowed': 'دسترسی به میکروفون رد شد. لطفاً اجازه دهید.',
        };
        voiceStatus.textContent = errors[event.error] || `خطا: ${event.error}`;
    };
    
    recognition.onend = () => {
        voiceBtn.textContent = '🎤 ورودی صوتی';
        voiceBtn.style.background = 'linear-gradient(135deg, #6C63FF, #00D9FF)';
    };
} else {
    voiceBtn.style.display = 'none';
    voiceStatus.textContent = '⚠️ مرورگر شما از Web Speech API پشتیبانی نمی‌کند. از Chrome استفاده کنید.';
}
</script>
"""

def render_voice_button():
    """رندر کردن دکمه ورودی صوتی در Streamlit"""
    import streamlit.components.v1 as components
    components.html(VOICE_INPUT_HTML, height=80)
```

---

### ۹. یکپارچه‌سازی voice و image در UI

فایل `ui/patch_advanced.py` بساز — راهنمای اضافه کردن قابلیت‌های پیشرفته به streamlit_app.py:

```python
"""
راهنمای اضافه کردن قابلیت‌های پیشرفته به Streamlit UI
"""

# ─── در ui/streamlit_app.py اضافه کن ───

# ۱. در تب چت، قبل از chat_input:
from tools.voice_input import render_voice_button
render_voice_button()

# ۲. در تب چت، بعد از response:
# اگر response شامل توضیح image بود:
if "تصویر" in clean_prompt or "image" in clean_prompt.lower() or "عکس" in clean_prompt:
    from tools.image_gen import generate_image
    img_result = asyncio.run(generate_image(clean_prompt))
    if img_result["url"]:
        st.image(img_result["url"], caption="Generated Image")

# ۳. اضافه کردن قابلیت آپلود فایل:
uploaded_file = st.file_uploader("📄 آپلود فایل", type=["pdf", "docx", "xlsx", "csv", "txt", "md", "py"])
if uploaded_file:
    from tools.file_processor import FileProcessor
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    
    result = FileProcessor.auto_read(tmp_path)
    if result["text"]:
        with st.expander(f"📄 محتوای {uploaded_file.name} ({result['type']})"):
            st.text_area("محتوا", result["text"], height=200)
        
        # ارسال به AI
        file_context = f"فایل پیوست ({result['type']}):\n{result['text'][:3000]}"
        # ... ارسال به agent.ask
```

---

### ۱۰. tests/test_advanced.py — تست قابلیت‌های پیشرفته

```python
"""
تست قابلیت‌های پیشرفته — image gen, file processor
"""

import pytest
import sys
import os
sys.path.insert(0, '.')

from tools.file_processor import FileProcessor
from pathlib import Path
import tempfile

# ─── File Processor ───

def test_file_processor_read_text():
    # ساخت فایل موقت
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("سلام دنیا\nخط دوم")
        tmp_path = f.name
    
    result = FileProcessor.auto_read(tmp_path)
    os.unlink(tmp_path)
    assert result["text"] is not None
    assert "سلام دنیا" in result["text"]
    assert result["error"] is None

def test_file_processor_unsupported_format():
    result = FileProcessor.auto_read("test.xyz")
    assert result["error"] is not None
    assert "پشتیبانی نمی‌شود" in result["error"]

def test_file_processor_missing_file():
    result = FileProcessor.auto_read("/nonexistent/file.txt")
    assert result["error"] is not None

def test_file_processor_supported_formats():
    supported = {".pdf", ".docx", ".xlsx", ".csv", ".txt", ".md", ".py", ".json"}
    # FileProcessor باید حداقل این فرمت‌ها رو بشناسه
    # (بررسی از طریق auto_read — اگر handler داشته باشه، error不一样 error unsupported format)
```

---

### ۱۱. نکات مهم:
1. Deploy فقط روی Streamlit Cloud و Hugging Face Spaces — هر دو رایگان.
2. GitHub Actions برای CI/CD — رایگان برای public repos.
3. API keys نباید در کد باشند — از Streamlit Cloud Secrets یا HF Spaces Secrets استفاده کن.
4. Pollinations.ai برای image generation بهترین گزینه رایگان بدون API key است.
5. Web Speech API فقط در Chrome و Edge کار می‌کند — Safari و Firefox partial پشتیبانی.
6. FileProcessor باید import errors را به‌خوبی مدیریت کند — اگر کتابخانه‌ای نصب نبود، پیام خطای مفید بدهد.
7. همه قابلیت‌های پیشرفته باید optional باشند — کاربر بدون آنها هم بتواند از اپ استفاده کند.
8. Docker نیاز نیست — Streamlit Cloud و HF Spaces بدون Docker کار می‌کنند.
9. سازگار با Python 3.11+ روی Linux (deploy platform) و Python 3.14 روی Windows (local).
10. مستندات README.md باید فارسی و انگلیسی باشد.
```

---

## ✅ خروجی مورد انتظار فاز ۵

| فایل | وضعیت |
|------|-------|
| `README.md` | ✅ مستندات کامل پروژه |
| `.github/workflows/test.yml` | ✅ CI/CD |
| `.streamlit/secrets.toml.example` | ✅ الگوی secrets |
| `packages.txt` | ✅ برای Streamlit Cloud |
| `tools/image_gen.py` | ✅ Pollinations + DeepAI |
| `tools/file_processor.py` | ✅ PDF, DOCX, XLSX, CSV, TXT |
| `tools/voice_input.py` | ✅ Web Speech API |
| `ui/patch_advanced.py` | ✅ راهنمای یکپارچه‌سازی |
| `tests/test_advanced.py` | ✅ تست‌ها |

---

## 🔗 وابستگی‌ها

- **وابسته به فاز ۱:** کل هسته core.py
- **وابسته به فاز ۲:** Agentها و ابزارها
- **وابسته به فاز ۳:** امنیت و حافظه
- **وابسته به فاز ۴:** UI کامل
- **پیش‌نیاز:** هیچ — این فاز آخر است

---

## 🗺️ خلاصه Deploy

| پلتفرم | لینک رایگان | برای چی |
|--------|-----------|---------|
| **Streamlit Cloud** | share.streamlit.io | Hosting اصلی UI |
| **Hugging Face Spaces** | huggingface.co/spaces | Hosting فال‌بک |
| **GitHub** | github.com | کد + CI/CD |
| **GitHub Actions** | (بخش GitHub) | تست خودکار |
| **Pollinations.ai** | image.pollinations.ai | تولید تصویر رایگان |
| **Web Speech API** | (بخش مرورگر) | ورودی صوتی رایگان |

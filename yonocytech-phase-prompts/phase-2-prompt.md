# 🤖 فاز ۲: Agentهای تخصصی و ابزارها
## پرامپت کامل برای GLM-5-Turbo

---

> **پیش‌نیاز:** فاز ۱ باید کامل اجرا شده باشد. فایل core.py با کلاس YonocyTech، AgentResponse، SessionMessage و MemoryStore موجود باشد.
>
> **مسیر پروژه:** `C:\Users\habib\Desktop\1234\YonocyTech\`

---

## 📋 پرامپت فاز ۲

```
تو یک برنامه‌نویس Python ارشد هستی. من در حال ساخت YonocyTech AI Agent هستم. فاز ۱ (هسته core.py) قبلاً کامل شده.

### ساختار فعلی پروژه:
YonocyTech/
├── core.py           # ✅ موجود — شامل YonocyTech, AgentResponse, SessionMessage, MemoryStore, OpenRouterProvider, HuggingFaceProvider, GitHubModelsProvider
├── config/.env       # ✅ موجود
├── agents/__init__.py
├── tools/__init__.py
├── ui/
├── memory/
├── security/
├── tests/

### هدف فاز ۲:
ساخت ۶ Agent تخصصی + BaseAgent class + ۳ ابزار (web search, file manager, orchestrator).

---

## خواسته‌شده:

### ۱. agents/base_agent.py — کلاس پایه

```python
"""
Base Agent — کلاس پایه برای همه Agentهای تخصصی
تمام Agentها از این کلاس ارث‌بری می‌کنند.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class BaseAgent(ABC):
    """کلاس پایه Agent — ارث‌بری + override متد run()"""
    
    def __init__(self, yonocytech_core):
        """
        Args:
            yonocytech_core: نمونه‌ای از کلاس YonocyTech از core.py
        """
        self.core = yonocytech_core
        self.name = self.__class__.__name__
    
    @property
    @abstractmethod
    def focus(self) -> str:
        """حوزه تخصصی — باید توسط هر subclass override شود"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """توضیح قابلیت‌های Agent"""
        pass
    
    async def run(self, prompt: str, session_id: str = None, **kwargs) -> str:
        """
        متد اصلی — prompt را می‌گیرد، نتیجه را برمی‌گرداند.
        هر Agent می‌تواند این متد را override کند.
        """
        response = await self.core.ask(
            prompt=prompt,
            focus=self.focus,
            session_id=session_id
        )
        return response.text
```

### ۲. agents/coding_agent.py — Agent کدنویسی

```python
"""
Coding Agent — تولید کد، دیباگ، ریفکتور، Code Review
با قابلیت استخراج بلاک کد و اجرای امن (sandbox)
"""
```

- ارث‌بری از BaseAgent
- focus = "coding"
- description = "تولید کد | دیباگ | ریفکتور | توضیح کد | اجرای امن در sandbox"
- متد extract_code_blocks(self, text: str) -> list:
  - استفاده از regex: r'```(\w+)?\n(.*?)```' با re.DOTALL
  - برگرداندن لیست دیکت: [{"language": str, "code": str}]
- متد async run(self, prompt, session_id=None, execute=False) -> str:
  - فراخوانی self.core.ask با focus="coding"
  - اگر execute=True: استخراج بلاک‌های پایتون از پاسخ، اجرای هر کدوم
  - نتیجه شامل بخش کاربر + بخش نتیجه اجرا (اگر فعال بود)
  - فرمت markdown با ## headers

### ۳. agents/writing_agent.py — Agent نوشتن

- ارث‌بری از BaseAgent
- focus = "writing"
- description = "مقاله | مستندات | ایمیل | محتوای سوشال مدیا | ویرایش"
- متد async run(self, prompt, session_id=None, language="auto", tone="professional") -> str:
  - enhancement prompt با style instructions:
    - Language: auto = match user's language
    - Tone: professional/casual/academic/creative
    - Format: well-structured, headings, bullets
    - Quality: clear, concise, no fluff. Word count at end.
  - فراخوانی self.core.ask با enhanced_prompt

### ۴. agents/data_agent.py — Agent تحلیل داده

- ارث‌بری از BaseAgent
- focus = "data"
- description = "تحلیل داده | Visualization | پاکسازی داده | گزارش آماری"
- متد async analyze_csv(self, filepath: str, question: str, session_id=None) -> str:
  - خواندن CSV با pandas
  - تولید summary: rows, columns, dtypes, missing values, describe(), head(5)
  - ارسال summary + question به self.core.ask با focus="data"
- متد async run: override base — اگر prompt شامل مسیر فایل CSV بود، از analyze_csv استفاده کن، وگرنه run معمولی

### ۵. agents/design_agent.py — Agent طراحی

- ارث‌بری از BaseAgent
- focus = "design"
- description = "مشاوره UI/UX | پالت رنگی | تایپوگرافی | SVG | CSS"
- متد async generate_ui_spec(self, description: str) -> str:
  - ساخت prompt برای تولید UI design spec شامل:
    1. Color palette (primary, secondary, accent, bg, text) با hex codes
    2. Typography (font families, sizes, weights)
    3. Layout structure
    4. Component list
    5. Accessibility considerations
    6. Responsive breakpoints
- متد async run: فراخوانی generate_ui_spec + self.core.ask

### ۶. agents/marketing_agent.py — Agent مارکتینگ

- ارث‌بری از BaseAgent
- focus = "marketing"
- description = "SEO | سوشال مدیا | استراتژی محتوا | تبلیغات | A/B تست"
- متد async run: enhancement prompt با:
  - Market context awareness
  - Actionable recommendations
  - KPI suggestions
  - Channel-specific advice

### ۷. agents/research_agent.py — Agent تحقیق

- ارث‌بری از BaseAgent
- focus = "research"
- description = "تحقیق وب | خلاصه‌سازی | Fact-checking | استناد به منابع"
- import از tools.web_search (که در همین فاز ساخته میشه)
- متد async research(self, topic: str, session_id=None) -> str:
  1. search_web(topic, max_results=5)
  2. اگر نتایج بود: ساخت context با شماره‌گذاری + title + URL + snippet
  3. ارسال context + topic به self.core.ask با دستور استناد [1], [2], ...
  4. اگر نتایجی نبود: ارسال بدون context
- متد async run: فراخوانی research

### ۸. agents/__init__.py — صادرات

```python
from .base_agent import BaseAgent
from .coding_agent import CodingAgent
from .writing_agent import WritingAgent
from .data_agent import DataAgent
from .design_agent import DesignAgent
from .marketing_agent import MarketingAgent
from .research_agent import ResearchAgent

ALL_AGENTS = {
    "coding": CodingAgent,
    "writing": WritingAgent,
    "data": DataAgent,
    "design": DesignAgent,
    "marketing": MarketingAgent,
    "research": ResearchAgent,
}
```

---

### ۹. tools/web_search.py — جستجوی وب رایگان

```python
"""
جستجوی وب با DuckDuckGo — کاملاً رایگان، بدون API key
"""

from duckduckgo_search import DDGS

async def search_web(query: str, max_results: int = 5) -> list:
    """
    جستجوی وب و برگرداندن نتایج.
    
    Returns:
        لیست دیکت: [{"title": str, "url": str, "snippet": str}]
    """
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

### ۱۰. tools/file_manager.py — مدیریت فایل

```python
"""
مدیریت فایل — خواندن/نوشتن انواع فرمت‌ها
فقط فرمت‌های مجاز برای امنیت.
"""

from pathlib import Path
from typing import Optional
import json, csv

class FileManager:
    """مدیریت فایل‌های پروژه با محدودیت فرمت"""
    
    ALLOWED_READ_EXTENSIONS = {
        '.txt', '.md', '.py', '.js', '.ts', '.tsx', '.html', '.css',
        '.json', '.csv', '.yaml', '.yml', '.xml', '.toml',
        '.env.example', '.gitignore', '.sql'
    }
    
    ALLOWED_WRITE_EXTENSIONS = {
        '.txt', '.md', '.py', '.js', '.ts', '.html', '.css',
        '.json', '.csv', '.yaml', '.yml', '.xml', '.sql'
    }
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
    
    def read(self, filepath: str) -> Optional[str]:
        """خواندن فایل — فقط فرمت‌های مجاز"""
        path = self.base_dir / filepath
        if not path.exists():
            return None
        if path.suffix.lower() not in self.ALLOWED_READ_EXTENSIONS:
            return f"⚠️ فرمت '{path.suffix}' برای خواندن مجاز نیست."
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            return f"❌ خطا در خواندن: {e}"
    
    def write(self, filepath: str, content: str) -> dict:
        """
        نوشتن فایل — فقط فرمت‌های مجاز
        Returns: {"success": bool, "path": str, "error": str|None}
        """
        path = self.base_dir / filepath
        if path.suffix.lower() not in self.ALLOWED_WRITE_EXTENSIONS:
            return {"success": False, "error": f"فرمت '{path.suffix}' برای نوشتن مجاز نیست."}
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return {"success": True, "path": str(path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_dir(self, subpath: str = ".") -> list:
        """لیست فایل‌های یک پوشه"""
        path = self.base_dir / subpath
        if not path.exists() or not path.is_dir():
            return []
        items = []
        try:
            for item in path.iterdir():
                if item.name.startswith('.'):
                    continue  # مخفی‌ها رو نپوشون
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size_bytes": item.stat().st_size if item.is_file() else 0
                })
        except PermissionError:
            return []
        return sorted(items, key=lambda x: (x["type"], x["name"]))
    
    def delete(self, filepath: str) -> dict:
        """حذف فایل — فقط فایل، نه پوشه"""
        path = self.base_dir / filepath
        if not path.exists():
            return {"success": False, "error": "فایل وجود ندارد."}
        if path.is_dir():
            return {"success": False, "error": "حذف پوشه مجاز نیست. فقط فایل قابل حذف است."}
        try:
            path.unlink()
            return {"success": True, "path": str(path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### ۱۱. tools/orchestrator.py — هماهنگ‌کننده Agentها

```python
"""
Orchestrator — اجرای زنجیره‌ای چند Agent با هم
context هر Agent به Agent بعدی منتقل می‌شود.
"""

from typing import Dict, List, Optional

class Orchestrator:
    """مدیریت اجرای چند Agent به صورت زنجیره‌ای با context passing"""
    
    def __init__(self, agents: Dict):
        """
        Args:
            agents: دیکت از نمونه‌های Agent {"coding": CodingAgent(...), ...}
        """
        self.agents = agents
    
    async def chain(self, tasks: List[Dict], session_id: str = None) -> List[Dict]:
        """
        اجرای زنجیره‌ای Agentها — خروجی هر Agent به ورودی بعدی اضافه می‌شود.
        
        Args:
            tasks: لیست دیکت:
                [
                    {"agent": "research", "prompt": "تحقیق درباره X", "use_context": True},
                    {"agent": "writing", "prompt": "بر اساس تحقیق بنویس"},
                    {"agent": "coding", "prompt": "بر اساس مقاله کد بزن"}
                ]
        
        Returns:
            لیست دیکت: [{"agent": str, "success": bool, "result": str, "error": str|None}]
        """
        results = []
        accumulated_context = ""
        
        for task in tasks:
            agent_name = task.get("agent", "")
            prompt = task.get("prompt", "")
            use_context = task.get("use_context", True)
            
            if agent_name not in self.agents:
                results.append({
                    "agent": agent_name,
                    "success": False,
                    "result": None,
                    "error": f"Agent '{agent_name}' پیدا نشد. Agentهای موجود: {list(self.agents.keys())}"
                })
                continue
            
            # اضافه کردن context قبلی
            final_prompt = prompt
            if use_context and accumulated_context:
                final_prompt = (
                    f"--- Context from previous agents ---\n"
                    f"{accumulated_context}\n"
                    f"--- End of context ---\n\n"
                    f"Current task: {prompt}"
                )
            
            try:
                agent = self.agents[agent_name]
                result_text = await agent.run(final_prompt, session_id=session_id)
                
                results.append({
                    "agent": agent_name,
                    "success": True,
                    "result": result_text,
                    "error": None
                })
                
                accumulated_context += f"\n### Result from {agent_name}:\n{result_text}"
                
            except Exception as e:
                results.append({
                    "agent": agent_name,
                    "success": False,
                    "result": None,
                    "error": str(e)
                })
        
        return results
    
    def list_agents(self) -> List[Dict]:
        """لیست تمام Agentهای در دسترس با focus و description"""
        return [
            {
                "name": name,
                "focus": agent.focus,
                "description": agent.description
            }
            for name, agent in self.agents.items()
        ]
    
    async def single(self, agent_name: str, prompt: str, session_id: str = None, **kwargs) -> Dict:
        """اجرای یک Agent واحد"""
        if agent_name not in self.agents:
            return {"success": False, "error": f"Agent '{agent_name}' پیدا نشد."}
        try:
            result = await self.agents[agent_name].run(prompt, session_id=session_id, **kwargs)
            return {"success": True, "result": result, "agent": agent_name}
        except Exception as e:
            return {"success": False, "error": str(e), "agent": agent_name}
```

### ۱۲. tools/__init__.py — صادرات

```python
from .web_search import search_web
from .file_manager import FileManager
from .orchestrator import Orchestrator
```

---

### ۱۳. tests/test_agents.py — تست Agentها

```python
"""
تست Agentهای تخصصی — با mock بدون نیاز به API واقعی
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
sys.path.insert(0, '.')

from core import YonocyTech, AgentResponse, MemoryStore

# ─── Test BaseAgent ───
def test_base_agent_requires_focus():
    """BaseAgent abstract — نمونه‌سازی مستقیم نباید ممکن باشد"""
    from agents.base_agent import BaseAgent
    with pytest.raises(TypeError):
        BaseAgent(yonocytech_core=None)

# ─── Test CodingAgent ───
@pytest.mark.asyncio
async def test_coding_agent_extract_code_blocks():
    from agents.coding_agent import CodingAgent
    mock_core = MagicMock()
    agent = CodingAgent(yonocytech_core=mock_core)
    
    text = 'Here is code:\n```python\nprint("hello")\n```\nMore text:\n```javascript\nconsole.log("hi")\n```'
    blocks = agent.extract_code_blocks(text)
    
    assert len(blocks) == 2
    assert blocks[0]["language"] == "python"
    assert blocks[0]["code"] == 'print("hello")'
    assert blocks[1]["language"] == "javascript"

# ─── Test FileManager ───
def test_file_manager_allowed_extensions():
    from tools.file_manager import FileManager
    fm = FileManager(base_dir="/tmp/test")
    assert '.py' in fm.ALLOWED_READ_EXTENSIONS
    assert '.exe' not in fm.ALLOWED_READ_EXTENSIONS
    assert '.bat' not in fm.ALLOWED_READ_EXTENSIONS

# ─── Test Orchestrator ───
@pytest.mark.asyncio
async def test_orchestrator_list_agents():
    from tools.orchestrator import Orchestrator
    mock_agent = MagicMock()
    mock_agent.focus = "coding"
    mock_agent.description = "test"
    orch = Orchestrator(agents={"coding": mock_agent})
    agents = orch.list_agents()
    assert len(agents) == 1
    assert agents[0]["name"] == "coding"

@pytest.mark.asyncio
async def test_orchestrator_missing_agent():
    from tools.orchestrator import Orchestrator
    orch = Orchestrator(agents={})
    results = await orch.chain([{"agent": "nonexistent", "prompt": "test"}])
    assert results[0]["success"] == False
    assert "پیدا نشد" in results[0]["error"]
```

---

### ۱۴. نحوه استفاده از Agentها (مثال):

```python
# مثال استفاده در core.py یا UI:
from agents import CodingAgent, WritingAgent, ResearchAgent
from tools import Orchestrator, FileManager

# ساخت agentها
agent = YonocyTech()
coding = CodingAgent(yonocytech_core=agent)
writing = WritingAgent(yonocytech_core=agent)
research = ResearchAgent(yonocytech_core=agent)

# ساخت orchestrator
orch = Orchestrator(agents={
    "coding": coding,
    "writing": writing,
    "research": research
})

# اجرای زنجیره‌ای
results = await orch.chain([
    {"agent": "research", "prompt": "تحقیق درباره Python web frameworks 2024"},
    {"agent": "writing", "prompt": "بر اساس تحقیق یک مقاله مقایسه‌ای بنویس"},
    {"agent": "coding", "prompt": "یک مثال ساده از بهترین framework بساز"}
])

for r in results:
    if r["success"]:
        print(f"✅ {r['agent']}: {r['result'][:100]}...")
    else:
        print(f"❌ {r['agent']}: {r['error']}")
```

---

### نکات مهم:
1. تمام Agentها باید async باشند (چون core.ask async است).
2. هر Agent فقط کاری را انجام دهد که حوزه تخصصی‌اش هست — بیش از حد تعمیم نکن.
3. importهای داخلی پروژه از فرمت import相对 استفاده کنند.
4. تمام error handling فارسی-انگلیسی.
5. type hints کامل.
6. docstring انگلیسی، comment فارسی.
7. سازگار با Python 3.14.
```

---

## ✅ خروجی مورد انتظار فاز ۲

| فایل | وضعیت |
|------|-------|
| `agents/__init__.py` | ✅ صادرات همه Agentها |
| `agents/base_agent.py` | ✅ کلاس پایه abstract |
| `agents/coding_agent.py` | ✅ با extract_code_blocks |
| `agents/writing_agent.py` | ✅ با language/tone |
| `agents/data_agent.py` | ✅ با analyze_csv |
| `agents/design_agent.py` | ✅ با UI spec generator |
| `agents/marketing_agent.py` | ✅ |
| `agents/research_agent.py` | ✅ با web search integration |
| `tools/__init__.py` | ✅ |
| `tools/web_search.py` | ✅ DuckDuckGo |
| `tools/file_manager.py` | ✅ با محدودیت فرمت |
| `tools/orchestrator.py` | ✅ با chain execution |
| `tests/test_agents.py` | ✅ تست‌های unit |

---

## 🔗 وابستگی‌ها

- **وابسته به فاز ۱:** core.py (YonocyTech, AgentResponse, SessionMessage, MemoryStore)
- **پیش‌نیاز فاز ۳:** security/guard.py برای sandbox Coding Agent
- **پیش‌نیاز فاز ۴:** همه Agentها و Orchestrator برای UI integration

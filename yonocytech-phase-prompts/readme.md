# 🚀 YonocyTech AI Agent — پرامپت‌های ۵ فازی

## نحوه استفاده

هر فایل `PHASE-X-prompt.md` یک پرامپت کامل و مستقل برای مدل **GLM-5-Turbo** است.

**روش:**
1. فایل پرامپت فاز مورد نظر رو باز کن
2. کل محتوای فایل رو کپی کن
3. در GLM-5-Turbo (یا هر مدل دیگه‌ای) پیست کن
4. مدل تمام کدهای اون فاز رو برات تولید می‌کنه

**ترتیب اجرا (حیاتی — فازها به هم وابسته‌اند):**
```
فاز ۱ ← فاز ۲ ← فاز ۳ ← فاز ۴ ← فاز ۵
```

---

## خلاصه ۵ فاز

| فاز | عنوان | مدت تخمینی | خروجی |
|-----|-------|-----------|-------|
| **۱** | بستر و هسته AI Engine | ۳-۴ روز | core.py + providers + .env + project structure |
| **۲** | Agentهای تخصصی و ابزارها | ۴-۵ روز | ۶ Agent + BaseAgent + web search + file manager + orchestrator |
| **۳** | امنیت و حافظه پایدار | ۳-۴ روز | injection guard + sandbox + rate limiter + ChromaDB + JSON memory |
| **۴** | رابط کاربری (UI) — **v2.0** | ۴-۵ روز | Streamlit shell سه‌ستونه + Design System + ماکاپ تعاملی |
| **۵** | استقرار و قابلیت‌های پیشرفته | ۴-۵ روز | GitHub + CI/CD + Deploy + voice + image gen + file processing |

**زمان کل:** ~۱۸-۲۳ روز کار متمرکز
**هک هزینه:** $۰.۰۰

---

## ✨ فاز ۴ — UI v2.0 (آخرین تغییرات اعمال‌شده)

### 🎨 Design System
تم **Dark Space** با گرادینت نئونی `indigo → cyan → magenta`، glassmorphism، انیمیشن‌های نرم (slide-in، fade-in، typing dots، pulse glow) و ستاره‌های متحرک در پس‌زمینه.

### 🗂 فایل‌های جدید / به‌روزرسانی‌شده

| فایل | نقش | وضعیت |
|------|------|------|
| `YonocyTech/ui/streamlit_app.py` | Shell سه‌ستونه (Sidebar · Main · Aside) | ✅ بازنویسی‌شده |
| `YonocyTech/ui/components.py` | Design System + ۱۳+ کامپوننت قابل‌استفاده‌مجدد | ✅ بازنویسی‌شده |
| `YonocyTech/docs/ui-mockup.html` | ماکاپ تعاملی مستقل (در مرورگر باز شود) | 🆕 جدید |
| `YonocyTech/docs/ui-spec.md` | مستند کامل طراحی: توکن‌ها، تایپوگرافی، layout، انیمیشن‌ها | 🆕 جدید |

### 🧩 کامپوننت‌های Design System
- `apply_theme()` — inject global CSS theme
- `render_brand()` / `render_header()` — brand و top bar
- `render_agent_item()` / `render_session_card()` — sidebar
- `render_welcome()` / `render_quick_starts()` — chat empty state
- `render_msg_bubble()` / `render_typing()` — chat UI با metadata chips
- `render_aside_provider()` / `render_aside_chain()` / `render_aside_memory()` / `render_aside_stats()` — پنل‌های کناری
- `render_response_metadata()` — نمایش provider/model/latency

### 📐 Layout
```
┌────────┬──────────────┬────────┐
│        │   HEADER     │        │
│ SIDE   ├──────────────┤ ASIDE  │
│ BAR    │     MAIN     │ panels │
│        ├──────────────┤        │
│        │  COMPOSER    │        │
└────────┴──────────────┴────────┘
```

### ▶ اجرا
```bash
cd YonocyTech
pip install -r requirements.txt
streamlit run ui/streamlit_app.py
```

ماکاپ را مستقیماً در مرورگر باز کنید:
```bash
start docs/ui-mockup.html        # Windows
open docs/ui-mockup.html         # macOS
```

---

## 📁 ساختار کلی پروژه

```
YonocyTechAgent/
├── YonocyTech/                    # اپلیکیشن اصلی
│   ├── core.py
│   ├── agents/                    # ۶ agent تخصصی
│   ├── tools/                     # web search, file manager, orchestrator, ...
│   ├── security/                  # injection guard, sandbox
│   ├── memory/                    # JSON + ChromaDB
│   ├── ui/                        # Streamlit (v2.0 redesign)
│   │   ├── streamlit_app.py
│   │   ├── components.py
│   │   └── pages/
│   ├── docs/                      # مستندات + ماکاپ
│   │   ├── ui-mockup.html
│   │   ├── ui-spec.md
│   │   └── monetization.md
│   ├── tests/
│   ├── .streamlit/
│   └── .github/workflows/
│
└── yonocytech-phase-prompts/      # پرامپت‌های ۵ فاز (همین پوشه)
    ├── readme.md                  # این فایل
    ├── phase-1-prompt.md
    ├── phase-2-prompt.md
    ├── phase-3-prompt.md
    ├── phase-4-prompt.md          # منبع پرامپت UI (اکنون v2.0 اعمال شده)
    ├── phase-5-prompt.md
    ├── YonocyTech-Plan-v2.md
    └── GEMMA4-FULL-PROMPT-EN.md
```

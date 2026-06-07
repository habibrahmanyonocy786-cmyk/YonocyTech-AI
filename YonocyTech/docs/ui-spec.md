# YonocyTech AI — UI Design Specification v2.0

> Professional, dark space-themed Streamlit redesign aligned with the agent project's purpose.

---

## 1. Design Goals

| Goal | Outcome |
|------|---------|
| **Professional SaaS feel** | Inspired by Claude / Linear / Vercel — minimal, focused, premium. |
| **Project identity** | "YonocyTech AI — Low-Resource Enterprise Intelligence" — deep space + neon. |
| **Function-first** | Surfacing 6 specialized agents, multi-agent chain, hybrid memory, security status. |
| **Bilingual** | Persian + English labels; full RTL-safe layout. |
| **Animations** | Subtle, GPU-cheap: drift stars, slide-in sidebar, typing dots, pulse status. |

---

## 2. Color System

```
--bg-0        #07071A   deepest space
--bg-1        #0B0B24   panels
--bg-2        #11112E   cards
--bg-3        #1A1A3E   hover
--surface     rgba(20,20,50,0.55)   glass
--border      rgba(108,99,255,0.18)
--text        #ECECFF
--text-dim    #A5A5C7
--primary     #6C63FF   indigo
--primary-2   #00D9FF   cyan
--accent      #FF4FCB   magenta
--success     #4ADE80
--warning     #FBBF24
--danger      #F87171

Brand gradient: 135deg, #6C63FF → #00D9FF → #FF4FCB
```

---

## 3. Typography

- **Primary:** `Inter` (300 / 400 / 500 / 600 / 700 / 800)
- **Code:** `JetBrains Mono`
- **Fallback:** `-apple-system, BlinkMacSystemFont, "Segoe UI"`

Scale: 11 / 12 / 13 / 14 / 15 / 18 / 24 / 32 / 42

---

## 4. Layout

3-column desktop shell:

```
┌────────┬──────────────┬────────┐
│        │   HEADER     │        │
│ SIDE   ├──────────────┤ ASIDE  │
│ BAR    │              │        │
│        │     MAIN     │ panels │
│        │   (chat)     │        │
│        ├──────────────┤        │
│        │  COMPOSER    │        │
└────────┴──────────────┴────────┘
```

- Sidebar **280px** — brand, workspace nav, 6 agents, sessions, user card.
- Header **64px** — breadcrumbs, status pill, notifications, primary CTA.
- Main — chat scroll + sticky composer with tools.
- Aside **320px** — provider health, active chain, memory recall, session stats.

Responsive:
- `≤1100px` hide aside.
- `≤720px` hide sidebar (use Streamlit hamburger).

---

## 5. Component Library

| Component | Purpose |
|---|---|
| `render_brand()` | Logo + wordmark with glow. |
| `render_sidebar_agents(ALL_AGENTS)` | Agent list with active highlight bar. |
| `render_session_card(user)` | User pill at sidebar bottom. |
| `render_header(active_page, agent)` | Breadcrumb + status + CTA. |
| `render_aside_provider(engine)` | Live provider/fallback status. |
| `render_aside_chain(tasks)` | Multi-agent chain stepper. |
| `render_aside_memory(engine)` | Vector + JSON recall. |
| `render_aside_stats(session)` | Tokens, cost, latency, blocked. |
| `render_welcome()` | Hero + 4 quick-start cards. |
| `render_msg_bubble(role, name, tag, html, meta)` | Chat bubble with metadata chips. |
| `render_typing()` | 3-dot animated indicator. |
| `render_composer()` | Glass input with attach / voice / search / image / memory tools. |
| `render_response_metadata(response)` | Provider / model / latency / tokens expander. |

---

## 6. Animations

- **Cosmos background** — radial gradients + drifting star layers (90s / 140s / 220s loops).
- **Sidebar** — slide from left (600ms).
- **Header** — fade-down (600ms, 100ms delay).
- **Aside** — slide from right (600ms, 150ms delay).
- **Chat messages** — fade-in + 8px upward translate.
- **Typing dots** — 1.2s bounce stagger.
- **Buttons** — translateY(-1px) on hover, gradient glow.
- **Active agent** — gradient bar slides in on left edge.

All animations respect `prefers-reduced-motion` (set via CSS media query if needed).

---

## 7. Files Delivered

| File | Role |
|---|---|
| `docs/ui-mockup.html` | Standalone interactive prototype (open in browser). |
| `docs/ui-spec.md` | This document. |
| `ui/components.py` | New design system + reusable components. |
| `ui/streamlit_app.py` | Rebuilt 3-column shell using the new components. |

---

## 8. Accessibility

- Contrast: text vs background ≥ 4.5:1.
- Focus rings: 2px cyan outline on all interactive elements.
- Keyboard: tab order follows visual order; `Shift+Enter` newline in composer (via `st.chat_input`).
- Status indicators use **both** color and text label ("● Online" / "● Healthy").

---

## 9. Brand Voice

- Headlines: confident, action-oriented ("How can I help you ship today?").
- Empty state: friendly, never blank.
- Errors: warm + specific, never alarming.

---

## 10. Future Iterations

- Light-mode toggle (preserved CSS variables).
- Mobile-first drawer for sidebar.
- Drag-and-drop file zone in composer.
- Real-time provider latency sparkline.
- Per-agent accent color (Coding = cyan, Writing = magenta, Data = green, etc.).

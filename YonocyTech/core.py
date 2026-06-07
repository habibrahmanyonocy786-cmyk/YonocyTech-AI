import asyncio
import datetime
import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")
load_dotenv()

# Initialize SQLite database (runs once at import)
# Migration is idempotent: only runs if schema version < current
os.environ.setdefault("DATABASE_URL", "sqlite")
from database.schema import migrate as _migrate_db
_migrate_db()

# ----------------------------------------------------------------------------
# DATA MODELS
# ----------------------------------------------------------------------------

@dataclass
class AgentResponse:
    """
    Represents a response from an AI model provider.
    """
    text: str
    model: str
    provider: str
    tokens_used: int = 0
    latency_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class SessionMessage:
    """
    Represents a single message within a conversation session.
    """
    role: str  # 'user', 'assistant', or 'system'
    content: str
    focus: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "focus": self.focus,
            "timestamp": self.timestamp,
        }

# ----------------------------------------------------------------------------
# PROVIDER IMPLEMENTATIONS
# ----------------------------------------------------------------------------

class OpenRouterProvider:
    """
    Integration with OpenRouter API for free model access.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    async def ask(self, messages: List[Dict[str, str]], max_tokens: int = 1024) -> AgentResponse:
        start_time = time.time()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "YonocyTech",
        }
        body = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.url, headers=headers, json=body)
            data = response.json()
            if response.status_code != 200:
                error_detail = data.get("error", {}).get("message", str(data))
                raise Exception(error_detail)

        latency = (time.time() - start_time) * 1000
        return AgentResponse(
            text=data["choices"][0]["message"]["content"],
            model=self.model,
            provider="OpenRouter",
            tokens_used=data.get("usage", {}).get("total_tokens", 0),
            latency_ms=latency,
        )

class HuggingFaceProvider:
    """
    Integration with HuggingFace Inference API.
    """
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.model = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
        self.url = f"https://api-inference.huggingface.co/models/{self.model}"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    async def ask(self, messages: List[Dict[str, str]], max_tokens: int = 1024) -> AgentResponse:
        start_time = time.time()

        # HF Inference API often expects a single string or specific format
        # We'll extract system and user messages and format as Mistral template
        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "You are a helpful assistant.")
        user_msg = messages[-1]["content"] if messages else ""

        formatted_prompt = f"<s>[INST] {system_msg}\n\n{user_msg} [/INST]"

        headers = {"Authorization": f"Bearer {self.api_key}"}
        body = {
            "inputs": formatted_prompt,
            "parameters": {"max_new_tokens": max_tokens, "temperature": 0.7},
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()

        latency = (time.time() - start_time) * 1000

        # HF response format varies; usually a list of dicts
        text = data[0]["generated_text"] if isinstance(data, list) else data.get("generated_text", "")
        # Remove the prompt from the output if present
        text = text.replace(formatted_prompt, "").strip()

        return AgentResponse(
            text=text,
            model=self.model,
            provider="HuggingFace",
            latency_ms=latency,
        )

class GitHubModelsProvider:
    """
    Integration with GitHub Models (Azure AI Inference).
    """
    def __init__(self):
        self.api_key = os.getenv("GITHUB_TOKEN")
        self.model = "gpt-4o-mini"
        self.url = "https://models.inference.ai.azure.com/chat/completions"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    async def ask(self, messages: List[Dict[str, str]], max_tokens: int = 1024) -> AgentResponse:
        start_time = time.time()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()

        latency = (time.time() - start_time) * 1000
        return AgentResponse(
            text=data["choices"][0]["message"]["content"],
            model=self.model,
            provider="GitHubModels",
            tokens_used=data.get("usage", {}).get("total_tokens", 0),
            latency_ms=latency,
        )

# ----------------------------------------------------------------------------
# MEMORY SYSTEM
# ----------------------------------------------------------------------------

class MemoryStore:
    """
    Handles persistent JSON storage for conversation sessions.
    """
    def __init__(self, data_dir: str = "memory/data"):
        self.data_dir = data_dir
        self.file_path = os.path.join(self.data_dir, "conversations.json")
        os.makedirs(self.data_dir, exist_ok=True)
        self.sessions: Dict[str, List[SessionMessage]] = self._load()

    def _load(self) -> Dict[str, List[SessionMessage]]:
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    sid: [SessionMessage(**msg) for msg in msgs]
                    for sid, msgs in data.items()
                }
        except (json.JSONDecodeError, IOError):
            return {}

    def _save(self) -> None:
        serializable = {
            sid: [msg.to_dict() for msg in msgs]
            for sid, msgs in self.sessions.items()
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)

    def new_session(self) -> str:
        timestamp = datetime.datetime.now().isoformat()
        session_id = hashlib.sha256(timestamp.encode()).hexdigest()[:12]
        self.sessions[session_id] = []
        self._save()
        return session_id

    def add_message(self, session_id: str, role: str, content: str, focus: Optional[str] = None) -> None:
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        msg = SessionMessage(role=role, content=content, focus=focus)
        self.sessions[session_id].append(msg)

        # Crop to last 50 messages to prevent file bloat
        if len(self.sessions[session_id]) > 50:
            self.sessions[session_id] = self.sessions[session_id][-50:]

        self._save()

    def get_history(self, session_id: str, limit: int = 20) -> List[SessionMessage]:
        msgs = self.sessions.get(session_id, [])
        return msgs[-limit:]

    def list_sessions(self) -> List[Dict[str, Any]]:
        sessions_info = []
        for sid, msgs in self.sessions.items():
            if not msgs: continue
            last_msg = msgs[-1].content
            sessions_info.append({
                "id": sid,
                "preview": (last_msg[:57] + "...") if len(last_msg) > 60 else last_msg,
                "count": len(msgs),
                "last_active": msgs[-1].timestamp,
            })
        return sessions_info

# ----------------------------------------------------------------------------
# DATABASE AUTH INTEGRATION
# ----------------------------------------------------------------------------

def register_user(name: str, email: str, password: str) -> Optional[Dict]:
    from database.models import create_user, get_user_by_email
    return create_user(name, email, password)


def login_user(email: str, password: str) -> Optional[Dict]:
    from database.models import authenticate
    user = authenticate(email, password)
    if user:
        user.pop("password", None)
    return user


def get_db_providers() -> List[Dict]:
    from database.models import get_active_providers
    return get_active_providers()


def get_db_agents() -> List[Dict]:
    from database.models import get_active_agents
    return get_active_agents()


# ----------------------------------------------------------------------------
# MAIN AI AGENT CLASS
# ----------------------------------------------------------------------------

class YonocyTech:
    """
    The main AI Agent class orchestrating providers and memory.
    """
    FOCUS_AREAS = ["coding", "writing", "product", "data", "design", "marketing", "ops", "research"]

    SYSTEM_PROMPTS = {
        "coding": "You are an expert software engineer. Provide clean, efficient, and well-documented code. Always prioritize security and performance.",
        "writing": "You are a professional content writer. Focus on clarity, engagement, and a tone that suits the intended audience. Use a polished style.",
        "product": "You are a senior product manager. Focus on user value, market fit, and actionable product specifications.",
        "data": "You are a data scientist. Provide rigorous analysis, identify patterns, and suggest data-driven insights using pandas and matplotlib.",
        "design": "You are a UI/UX designer. Focus on accessibility, modern aesthetics, responsive layouts, and user-centric design.",
        "marketing": "You are a growth marketing expert. Focus on SEO, conversion rates, KPI tracking, and high-impact channel strategies.",
        "ops": "You are a DevOps engineer. Focus on scalability, CI/CD pipelines, security, and infrastructure as code.",
        "research": "You are a detailed research analyst. Provide comprehensive summaries with clear citations [1], [2] and evidence-based conclusions.",
        "default": "You are YonocyTech AI, a highly capable assistant. Be helpful, precise, and objective."
    }

    def __init__(self, name: str = "YonocyTech", version: str = "2.0", user_id: Optional[int] = None):
        self.name = name
        self.version = version
        self.user_id = user_id
        self.memory = MemoryStore()
        self.providers = []
        self._init_providers()
        self.session_id = None
        self._semantic = None

    @property
    def semantic_recall(self):
        if self._semantic is None:
            try:
                from memory.vector_store import VectorMemory
                from memory.semantic_recall import SemanticRecall
                vs = VectorMemory()
                self._semantic = SemanticRecall(vs, self.memory)
            except Exception:
                self._semantic = None
        return self._semantic

    def _init_providers(self) -> None:
        db_providers = get_db_providers()
        db_active_ids = {p["id"] for p in db_providers}

        provider_map = {
            "openrouter": OpenRouterProvider(),
            "huggingface": HuggingFaceProvider(),
            "github-models": GitHubModelsProvider(),
        }

        self.providers = []
        for key, prov in provider_map.items():
            if key in db_active_ids and prov.is_available:
                self.providers.append(prov)

        # Fallback: if DB is empty, use all available providers
        if not self.providers:
            self.providers = [p for p in provider_map.values() if p.is_available]

    async def ask(self, prompt: str, focus: Optional[str] = None,
                  session_id: Optional[str] = None) -> AgentResponse:
        if not prompt:
            raise ValueError("Prompt cannot be empty")

        from security.guard import detect_injection, sanitize_input

        injection_detected, pattern = detect_injection(prompt)
        if injection_detected:
            return AgentResponse(
                text=f"Prompt blocked: injection pattern detected ({pattern}). Your message was not processed.",
                model="N/A", provider="SecurityGuard"
            )

        prompt = sanitize_input(prompt)

        sid = session_id or self.session_id or self.memory.new_session()
        self.session_id = sid

        # 1. Build System Prompt
        system_text = self.SYSTEM_PROMPTS.get(focus, self.SYSTEM_PROMPTS["default"])
        messages = [{"role": "system", "content": system_text}]

        # 2. Add history (last 10 messages)
        history = self.memory.get_history(sid, limit=10)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # 3. Add current user message
        messages.append({"role": "user", "content": prompt})

        # 4. Save user message to memory (JSON)
        self.memory.add_message(sid, "user", prompt, focus=focus)

        # 5. Save to SQLite if user is authenticated
        if self.user_id and sid:
            try:
                from database.models import add_message as db_add_message
                db_add_message(sid, "user", prompt, focus, user_id=self.user_id)
            except Exception:
                pass

        # 6. Fallback Chain
        last_exception = None
        last_provider_name = None
        for provider in self.providers:
            try:
                response = await provider.ask(messages)
                # Save assistant response to JSON memory
                self.memory.add_message(sid, "assistant", response.text, focus=focus)

                # Save to SQLite
                if self.user_id and sid:
                    try:
                        db_add_message(sid, "assistant", response.text, focus,
                                       tokens=response.tokens_used, user_id=self.user_id)
                        from database.models import log_usage
                        log_usage(self.user_id, response.provider, focus or "general",
                                  tokens=response.tokens_used, latency=response.latency_ms)
                    except Exception:
                        pass

                # Save to vector memory for semantic recall
                try:
                    if self.semantic_recall:
                        self.semantic_recall.store_conversation_pair(
                            prompt, response.text, sid, focus=focus
                        )
                except Exception:
                    pass

                return response
            except Exception as e:
                last_exception = e
                last_provider_name = provider.__class__.__name__
                continue

        # 7. If all fail
        provider_names = [p.__class__.__name__ for p in self.providers]
        error_text = str(last_exception) if last_exception else "Unknown error"

        if "image" in error_text.lower() and "not support" in error_text.lower():
            user_friendly = (
                "This model only supports text. Images and files cannot be processed. "
                "Please describe what's in the image or file using text."
            )
        else:
            user_friendly = f"All providers failed. Attempted: {', '.join(provider_names)}. Last error: {error_text}"

        return AgentResponse(text=user_friendly, model="N/A", provider="None")

# ----------------------------------------------------------------------------
# CLI INTERFACE
# ----------------------------------------------------------------------------

async def cli():
    agent = YonocyTech()
    session_id = agent.memory.new_session()
    agent.session_id = session_id

    print(f"=== {agent.name} v{agent.version} ===")
    print("Type 'exit' or 'quit' to stop. Use '/sessions' to list or '/new' for new session.")
    print("Specify focus using 'focus:coding <prompt>'\n")

    while True:
        try:
            user_input = input("You > ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                break

            if user_input == "/sessions":
                sessions = agent.memory.list_sessions()
                for s in sessions:
                    print(f"ID: {s['id']} | {s['preview']} ({s['count']} msgs)")
                continue

            if user_input == "/new":
                agent.session_id = agent.memory.new_session()
                print(f"New session started: {agent.session_id}")
                continue

            # Parse focus
            focus = None
            prompt = user_input
            if user_input.startswith("focus:"):
                parts = user_input.split(" ", 1)
                focus = parts[0][6:] # remove 'focus:'
                prompt = parts[1] if len(parts) > 1 else ""

            print("Thinking...", end="\r")
            response = await agent.ask(prompt, focus=focus, session_id=agent.session_id)
            print(f"AI > {response.text}")
            print(f"({response.provider} | {response.model} | {int(response.latency_ms)}ms)")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(cli())

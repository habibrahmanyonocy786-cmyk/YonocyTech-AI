from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: str = Field(..., max_length=320)
    password: str = Field(..., min_length=4)

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=320)
    password: str = Field(..., min_length=4)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    plan: str
    created_at: Optional[str] = None
    last_login: Optional[str] = None
    is_active: int = 1

class AuthResponse(BaseModel):
    user: UserResponse
    token: str


# ─────────────────────────────────────────────
# SESSIONS & MESSAGES
# ─────────────────────────────────────────────
class SessionCreate(BaseModel):
    user_id: int
    title: str = "New Session"
    focus: Optional[str] = None
    session_id: Optional[str] = None

class SessionResponse(BaseModel):
    id: str
    user_id: Optional[int] = None
    title: str
    focus: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    message_count: int = 0

class MessageCreate(BaseModel):
    session_id: str
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., max_length=10000)
    focus: Optional[str] = None
    tokens: int = 0
    user_id: Optional[int] = None

class MessageResponse(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    focus: Optional[str] = None
    tokens_used: int = 0
    timestamp: Optional[str] = None


# ─────────────────────────────────────────────
# PROVIDERS
# ─────────────────────────────────────────────
class ProviderResponse(BaseModel):
    id: str
    name: str
    status: str
    rate_limit: int
    priority: int
    api_key_set: int
    updated_at: Optional[str] = None

class ProviderUpdate(BaseModel):
    status: Optional[str] = None
    rate_limit: Optional[int] = None


# ─────────────────────────────────────────────
# AGENTS
# ─────────────────────────────────────────────
class AgentResponse(BaseModel):
    id: str
    name: str
    icon: str
    status: str
    default_provider: Optional[str] = None
    priority: int
    updated_at: Optional[str] = None

class AgentUpdate(BaseModel):
    status: Optional[str] = None
    default_provider: Optional[str] = None


# ─────────────────────────────────────────────
# CONTACT
# ─────────────────────────────────────────────
class ContactCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: str = Field(..., max_length=320)
    subject: Optional[str] = Field(None, max_length=200)
    message: str = Field(..., max_length=5000)

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    subject: Optional[str] = None
    message: str
    is_read: int
    created_at: Optional[str] = None


# ─────────────────────────────────────────────
# USAGE & ADMIN
# ─────────────────────────────────────────────
class UsageStats(BaseModel):
    total_requests: int
    total_tokens: int
    avg_latency: float
    failed: int

class SettingUpdate(BaseModel):
    key: str
    value: str


# ─────────────────────────────────────────────
# GENERIC
# ─────────────────────────────────────────────
class ErrorResponse(BaseModel):
    detail: str

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "2.0"

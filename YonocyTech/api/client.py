"""
Python API client for YonocyTech REST API.
Provides typed methods for all endpoints with token-based auth.
"""
from typing import Optional, List
import httpx


class YonocyTechAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000", token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    @property
    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        with httpx.Client(timeout=30) as client:
            resp = client.request(method, url, headers=self._headers, **kwargs)
            resp.raise_for_status()
            return resp.json()

    # ──────────── AUTH ────────────
    def login(self, email: str, password: str) -> dict:
        data = self._request("POST", "/auth/login", json={"email": email, "password": password})
        self.token = data["token"]
        return data

    def register(self, name: str, email: str, password: str) -> dict:
        data = self._request("POST", "/auth/register", json={"name": name, "email": email, "password": password})
        self.token = data["token"]
        return data

    def me(self) -> dict:
        return self._request("GET", "/auth/me")

    # ──────────── SESSIONS ────────────
    def create_session(self, user_id: int, title: str = "New Session", focus: Optional[str] = None, session_id: Optional[str] = None) -> dict:
        return self._request("POST", "/sessions/", json={"user_id": user_id, "title": title, "focus": focus, "session_id": session_id})

    def list_sessions(self) -> list:
        return self._request("GET", "/sessions/")

    def get_messages(self, session_id: str, limit: int = 50) -> list:
        return self._request("GET", f"/sessions/{session_id}/messages", params={"limit": limit})

    def send_message(self, session_id: str, role: str, content: str, focus: Optional[str] = None, tokens: int = 0, user_id: Optional[int] = None) -> dict:
        return self._request("POST", f"/sessions/{session_id}/messages", json={"session_id": session_id, "role": role, "content": content, "focus": focus, "tokens": tokens, "user_id": user_id})

    # ──────────── PROVIDERS ────────────
    def list_providers(self, active_only: bool = False) -> list:
        return self._request("GET", "/providers/", params={"active_only": active_only})

    def get_provider(self, provider_id: str) -> dict:
        return self._request("GET", f"/providers/{provider_id}")

    def update_provider(self, provider_id: str, status: Optional[str] = None, rate_limit: Optional[int] = None) -> dict:
        body = {}
        if status: body["status"] = status
        if rate_limit: body["rate_limit"] = rate_limit
        return self._request("PATCH", f"/providers/{provider_id}", json=body)

    # ──────────── AGENTS ────────────
    def list_agents(self, active_only: bool = False) -> list:
        return self._request("GET", "/agents/", params={"active_only": active_only})

    def get_agent(self, agent_id: str) -> dict:
        return self._request("GET", f"/agents/{agent_id}")

    def update_agent(self, agent_id: str, status: Optional[str] = None, default_provider: Optional[str] = None) -> dict:
        body = {}
        if status: body["status"] = status
        if default_provider: body["default_provider"] = default_provider
        return self._request("PATCH", f"/agents/{agent_id}", json=body)

    # ──────────── CONTACT ────────────
    def submit_contact(self, name: str, email: str, subject: str, message: str) -> dict:
        return self._request("POST", "/contact/", json={"name": name, "email": email, "subject": subject, "message": message})

    def list_contact(self) -> list:
        return self._request("GET", "/contact/")

    # ──────────── ADMIN ────────────
    def list_users(self) -> list:
        return self._request("GET", "/admin/users")

    def get_stats(self) -> dict:
        return self._request("GET", "/admin/stats")

    def get_counts(self) -> dict:
        return self._request("GET", "/admin/counts")

    def change_plan(self, user_id: int, plan: str) -> dict:
        return self._request("PATCH", f"/admin/users/{user_id}/plan", params={"plan": plan})

    def get_settings(self) -> dict:
        return self._request("GET", "/admin/settings")

    def update_setting(self, key: str, value: str) -> dict:
        return self._request("PUT", f"/admin/settings/{key}", json={"key": key, "value": value})

import json
import os
import time
from collections import defaultdict
from typing import Dict, Any, Optional


class AdminManager:
    def __init__(self, data_dir: str = "memory/data"):
        self.data_dir = data_dir
        self.file_path = os.path.join(data_dir, "usage_stats.json")
        os.makedirs(data_dir, exist_ok=True)
        self.stats = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            return {
                "total_tokens": 0,
                "total_requests": 0,
                "requests_by_provider": {},
                "tokens_by_provider": {},
                "requests_by_hour": {},
                "requests_by_user": {},
                "tokens_by_user": {},
                "start_time": time.time(),
                "daily_stats": {},
            }
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)

    def log_request(
        self,
        provider: str,
        model: str,
        tokens_used: int = 0,
        user_email: str = "anonymous",
        latency_ms: float = 0.0,
    ) -> None:
        self.stats["total_tokens"] = self.stats.get("total_tokens", 0) + tokens_used
        self.stats["total_requests"] = self.stats.get("total_requests", 0) + 1

        # Per provider
        provider_stats = self.stats.setdefault("requests_by_provider", {})
        provider_stats[provider] = provider_stats.get(provider, 0) + 1

        token_stats = self.stats.setdefault("tokens_by_provider", {})
        token_stats[provider] = token_stats.get(provider, 0) + tokens_used

        # Per user
        user_req = self.stats.setdefault("requests_by_user", {})
        user_req[user_email] = user_req.get(user_email, 0) + 1

        user_tok = self.stats.setdefault("tokens_by_user", {})
        user_tok[user_email] = user_tok.get(user_email, 0) + tokens_used

        # Per hour
        hour_key = time.strftime("%Y-%m-%dT%H:00:00")
        hour_stats = self.stats.setdefault("requests_by_hour", {})
        hour_stats[hour_key] = hour_stats.get(hour_key, 0) + 1

        # Daily
        day_key = time.strftime("%Y-%m-%d")
        daily = self.stats.setdefault("daily_stats", {})
        day_data = daily.setdefault(day_key, {"requests": 0, "tokens": 0})
        day_data["requests"] += 1
        day_data["tokens"] += tokens_used

        self._save()

    def get_summary(self) -> Dict[str, Any]:
        now = time.time()
        start = self.stats.get("start_time", now)
        uptime_hours = (now - start) / 3600

        day_key = time.strftime("%Y-%m-%d")
        daily = self.stats.get("daily_stats", {}).get(day_key, {})

        return {
            "total_tokens": self.stats.get("total_tokens", 0),
            "total_requests": self.stats.get("total_requests", 0),
            "uptime_hours": round(uptime_hours, 1),
            "requests_today": daily.get("requests", 0),
            "tokens_today": daily.get("tokens", 0),
            "active_providers": list(self.stats.get("requests_by_provider", {}).keys()),
            "requests_by_provider": self.stats.get("requests_by_provider", {}),
            "tokens_by_provider": self.stats.get("tokens_by_provider", {}),
            "top_users": dict(
                sorted(
                    self.stats.get("requests_by_user", {}).items(),
                    key=lambda x: x[1],
                    reverse=True,
                )[:10]
            ),
            "requests_by_hour": dict(
                sorted(self.stats.get("requests_by_hour", {}).items())[-24:]
            ),
        }

    def reset(self) -> None:
        self.stats = {
            "total_tokens": 0,
            "total_requests": 0,
            "requests_by_provider": {},
            "tokens_by_provider": {},
            "requests_by_hour": {},
            "requests_by_user": {},
            "tokens_by_user": {},
            "start_time": time.time(),
            "daily_stats": {},
        }
        self._save()

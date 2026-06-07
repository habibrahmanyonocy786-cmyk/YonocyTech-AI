from fastapi import APIRouter, Depends, HTTPException
from typing import List

from database.models import (
    get_all_users, get_usage_stats, get_all_settings,
    set_setting, update_user_plan, count_users,
)
from api.schemas import UserResponse, UsageStats, SettingUpdate
from api.routes.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


def _require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/users", response_model=List[UserResponse])
def list_users(_=Depends(_require_admin)):
    users = get_all_users()
    return [UserResponse(**dict(u)) for u in users]


@router.get("/stats", response_model=UsageStats)
def stats(_=Depends(_require_admin)):
    return UsageStats(**get_usage_stats())


@router.get("/counts")
def counts(_=Depends(_require_admin)):
    return {
        "users": count_users(),
        "sessions": 0,
        "messages": 0,
    }


@router.patch("/users/{user_id}/plan")
def change_plan(user_id: int, plan: str, _=Depends(_require_admin)):
    if plan not in ("free", "pro", "enterprise"):
        raise HTTPException(status_code=400, detail="Invalid plan")
    success = update_user_plan(user_id, plan)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": f"User {user_id} plan updated to {plan}"}


@router.get("/settings")
def get_settings(_=Depends(_require_admin)):
    return get_all_settings()


@router.put("/settings/{key}")
def update_setting(key: str, body: SettingUpdate, _=Depends(_require_admin)):
    set_setting(key, body.value)
    return {"detail": f"Setting {key} updated"}

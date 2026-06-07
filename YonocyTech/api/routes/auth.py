import hashlib
import hmac
import os
import time
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional

from database.models import authenticate, create_user, get_user_by_id
from api.schemas import LoginRequest, RegisterRequest, AuthResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = os.getenv("API_SECRET_KEY", "yonocytech-dev-key-change-in-prod")


def _generate_token(user_id: int) -> str:
    payload = f"{user_id}:{int(time.time()) + 86400}"
    sig = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]
    return f"{payload}:{sig}"


def _verify_token(token: str) -> Optional[int]:
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return None
        user_id, expiry, sig = parts
        expected = hmac.new(SECRET_KEY.encode(), f"{user_id}:{expiry}".encode(), hashlib.sha256).hexdigest()[:16]
        if not hmac.compare_digest(sig, expected):
            return None
        if int(expiry) < time.time():
            return None
        return int(user_id)
    except (ValueError, IndexError):
        return None


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    user_id = _verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return dict(user)


@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest):
    user = authenticate(body.email, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = _generate_token(user["id"])
    user.pop("password", None)
    return AuthResponse(user=UserResponse(**user), token=token)


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(body: RegisterRequest):
    from security.guard import sanitize_input
    name = sanitize_input(body.name, 100)
    user = create_user(name, body.email, body.password)
    if not user:
        raise HTTPException(status_code=409, detail="Email already exists or registration failed")
    token = _generate_token(user["id"])
    user.pop("password", None)
    return AuthResponse(user=UserResponse(**user), token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: dict = Depends(get_current_user)):
    current_user.pop("password", None)
    return UserResponse(**current_user)

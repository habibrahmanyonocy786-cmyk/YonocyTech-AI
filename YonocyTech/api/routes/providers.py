from fastapi import APIRouter, Depends, HTTPException
from typing import List

from database.models import (
    get_all_providers, get_active_providers,
    update_provider_status, update_provider_rate_limit,
)
from api.schemas import ProviderResponse, ProviderUpdate
from api.routes.auth import get_current_user

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get("/", response_model=List[ProviderResponse])
def list_providers(active_only: bool = False):
    providers = get_active_providers() if active_only else get_all_providers()
    return [ProviderResponse(**dict(p)) for p in providers]


@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: str):
    providers = get_all_providers()
    for p in providers:
        if p["id"] == provider_id:
            return ProviderResponse(**dict(p))
    raise HTTPException(status_code=404, detail="Provider not found")


@router.patch("/{provider_id}", response_model=ProviderResponse)
def update_provider(provider_id: str, body: ProviderUpdate, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if body.status:
        update_provider_status(provider_id, body.status)
    if body.rate_limit:
        update_provider_rate_limit(provider_id, body.rate_limit)
    providers = get_all_providers()
    for p in providers:
        if p["id"] == provider_id:
            return ProviderResponse(**dict(p))
    raise HTTPException(status_code=404, detail="Provider not found")

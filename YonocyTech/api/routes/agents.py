from fastapi import APIRouter, Depends, HTTPException
from typing import List

from database.models import (
    get_all_agents, get_active_agents,
    update_agent_status, update_agent_provider,
)
from api.schemas import AgentResponse, AgentUpdate
from api.routes.auth import get_current_user

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("/", response_model=List[AgentResponse])
def list_agents(active_only: bool = False):
    agents = get_active_agents() if active_only else get_all_agents()
    return [AgentResponse(**dict(a)) for a in agents]


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str):
    agents = get_all_agents()
    for a in agents:
        if a["id"] == agent_id:
            return AgentResponse(**dict(a))
    raise HTTPException(status_code=404, detail="Agent not found")


@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: str, body: AgentUpdate, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if body.status:
        update_agent_status(agent_id, body.status)
    if body.default_provider:
        update_agent_provider(agent_id, body.default_provider)
    agents = get_all_agents()
    for a in agents:
        if a["id"] == agent_id:
            return AgentResponse(**dict(a))
    raise HTTPException(status_code=404, detail="Agent not found")

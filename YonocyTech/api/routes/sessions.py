from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from database.models import (
    create_session, get_user_sessions, get_session_messages,
    add_message, ensure_session
)
from api.schemas import SessionCreate, SessionResponse, MessageCreate, MessageResponse
from api.routes.auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/", response_model=SessionResponse, status_code=201)
def new_session(body: SessionCreate):
    sid = create_session(body.user_id, body.title, body.focus, body.session_id)
    return SessionResponse(
        id=sid,
        user_id=body.user_id,
        title=body.title,
        focus=body.focus,
        message_count=0,
    )


@router.get("/", response_model=List[SessionResponse])
def list_sessions(current_user: dict = Depends(get_current_user)):
    sessions = get_user_sessions(current_user["id"])
    return [SessionResponse(**dict(s)) for s in sessions]


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
def list_messages(session_id: str, limit: int = Query(50, ge=1, le=200)):
    ensure_session(session_id)
    msgs = get_session_messages(session_id, limit=limit)
    return [MessageResponse(**dict(m)) for m in msgs]


@router.post("/{session_id}/messages", response_model=MessageResponse, status_code=201)
def send_message(session_id: str, body: MessageCreate):
    from security.guard import sanitize_input
    content = sanitize_input(body.content, 10000)
    add_message(
        session_id, body.role, content,
        focus=body.focus, tokens=body.tokens,
        user_id=body.user_id
    )
    return MessageResponse(
        id=0, session_id=session_id,
        role=body.role, content=content,
        focus=body.focus, tokens_used=body.tokens,
    )

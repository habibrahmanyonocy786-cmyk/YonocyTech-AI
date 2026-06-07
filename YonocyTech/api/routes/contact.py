from fastapi import APIRouter, Depends
from typing import List

from database.models import save_contact_message, get_contact_messages
from api.schemas import ContactCreate, ContactResponse
from api.routes.auth import get_current_user

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post("/", status_code=201)
def submit_contact(body: ContactCreate):
    from security.guard import sanitize_input
    name = sanitize_input(body.name, 100)
    email = sanitize_input(body.email, 320)
    subject = sanitize_input(body.subject or "", 200)
    message = sanitize_input(body.message, 5000)
    success = save_contact_message(name, email, subject, message)
    if not success:
        return {"detail": "Failed to save message"}
    return {"detail": "Message sent successfully"}


@router.get("/", response_model=List[ContactResponse])
def list_contact(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        return []
    msgs = get_contact_messages()
    return [ContactResponse(**dict(m)) for m in msgs]

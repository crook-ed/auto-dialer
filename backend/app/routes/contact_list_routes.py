from fastapi import APIRouter, Depends
from ..handlers.contact_list_handler import ContactListHandler
from ..schemas.contact_list import ContactListCreate, ContactListResponse
from typing import List
from ..utils.auth import get_current_user
from ..models.user import User
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=ContactListResponse)
async def create_contact_list(
    contact_list: ContactListCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    handler = ContactListHandler(db)
    return await handler.create_contact_list(contact_list, current_user)

@router.get("/", response_model=List[ContactListResponse])
async def get_user_contact_lists(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    handler = ContactListHandler(db)
    return await handler.get_user_contact_lists(current_user)

@router.post("/{contact_list_id}/contacts/{contact_id}", response_model=ContactListResponse)
async def add_contact_to_list(
    contact_list_id: int,
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    handler = ContactListHandler(db)
    return await handler.add_contact_to_list(contact_list_id, contact_id, current_user)

@router.delete("/{contact_list_id}/contacts/{contact_id}", response_model=ContactListResponse)
async def remove_contact_from_list(
    contact_list_id: int,
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    handler = ContactListHandler(db)
    return await handler.remove_contact_from_list(contact_list_id, contact_id, current_user)
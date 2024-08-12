from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from ..utils.auth import get_current_user
from ..handlers.contact_handler import ContactHandler
from ..models.user import User

router = APIRouter()

@router.post("/", response_model=ContactResponse)
async def create_contact(
    contact: ContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ContactHandler.create_contact(contact, current_user, db)

@router.get("/", response_model=list[ContactResponse])
async def get_user_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ContactHandler.get_user_contacts(current_user, db)



@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ContactHandler.delete_contact(contact_id, current_user, db)
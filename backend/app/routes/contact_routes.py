from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.contact_service import ContactService
from ..repositories.contact_repository import ContactRepository

router = APIRouter()

@router.post("/contacts/")
def create_contact(first_name: str, last_name: str, phone_number: str, user_id: int, db: Session = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact_service = ContactService(contact_repo)
    return contact_service.create_contact(first_name, last_name, phone_number, user_id)

@router.get("/contacts/{contact_id}")
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact_service = ContactService(contact_repo)
    contact = contact_service.get_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Add other routes as needed
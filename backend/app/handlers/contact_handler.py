from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.contact_service import ContactService
from ..repositories.contact_repository import ContactRepository
from ..schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from ..utils.auth import get_current_user

class ContactHandler:
    @staticmethod
    async def create_contact(contact: ContactCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        contact_repo = ContactRepository(db)
        contact_service = ContactService(contact_repo)
        new_contact = contact_service.create_contact(current_user["id"], contact.first_name, contact.last_name, contact.city, contact.phone_number)
        return ContactResponse.from_orm(new_contact)

    @staticmethod
    async def get_user_contacts(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        contact_repo = ContactRepository(db)
        contact_service = ContactService(contact_repo)
        contacts = contact_service.get_user_contacts(current_user["id"])
        return [ContactResponse.from_orm(contact) for contact in contacts]

    @staticmethod
    async def update_contact(contact_id: int, contact: ContactUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        contact_repo = ContactRepository(db)
        contact_service = ContactService(contact_repo)
        updated_contact = contact_service.update_contact(contact_id, **contact.dict(exclude_unset=True))
        return ContactResponse.from_orm(updated_contact)

    @staticmethod
    async def delete_contact(contact_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        contact_repo = ContactRepository(db)
        contact_service = ContactService(contact_repo)
        contact_service.delete_contact(contact_id)
        return {"message": "Contact deleted successfully"}
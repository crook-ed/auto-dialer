from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.contact_service import ContactService
from ..repositories.contact_repository import ContactRepository
from ..schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from ..utils.auth import get_current_user
from ..models.user import User

class ContactHandler:
    @staticmethod
    async def create_contact(contact: ContactCreate, current_user: User, db: Session = Depends(get_db)):
        contact_repo = ContactRepository(db)
        contact_service = ContactService(contact_repo)
        new_contact = contact_service.create_or_update_contact(current_user.id, contact.first_name, contact.last_name, contact.city, contact.phone_number)
        return ContactResponse.from_orm(new_contact)

    @staticmethod
    async def get_user_contacts(current_user: User, db: Session):
        contact_repo = ContactRepository(db)
        contact_service = ContactService(contact_repo)
        contacts = contact_service.get_user_contacts(current_user.id)
        return [ContactResponse.from_orm(contact) for contact in contacts]

   

    @staticmethod
    async def delete_contact(contact_id: int, current_user: User, db: Session = Depends(get_db)):
        contact_repo = ContactRepository(db)
        contact_service = ContactService(contact_repo)
        return contact_service.delete_contact(contact_id, current_user.id)
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.contact_list_service import ContactListService
from ..repositories.contact_list_repository import ContactListRepository
from ..schemas.contact_list import ContactListCreate, ContactListResponse
from ..utils.auth import get_current_user

class ContactListHandler:
    @staticmethod
    async def create_contact_list(contact_list: ContactListCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        contact_list_repo = ContactListRepository(db)
        contact_list_service = ContactListService(contact_list_repo)
        new_contact_list = contact_list_service.create_contact_list(current_user["id"], contact_list.name)
        return ContactListResponse.from_orm(new_contact_list)

    @staticmethod
    async def get_user_contact_lists(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        contact_list_repo = ContactListRepository(db)
        contact_list_service = ContactListService(contact_list_repo)
        contact_lists = contact_list_service.get_user_contact_lists(current_user["id"])
        return [ContactListResponse.from_orm(contact_list) for contact_list in contact_lists]

    @staticmethod
    async def add_contact_to_list(contact_list_id: int, contact_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        contact_list_repo = ContactListRepository(db)
        contact_list_service = ContactListService(contact_list_repo)
        updated_contact_list = contact_list_service.add_contact_to_list(contact_list_id, contact_id)
        return ContactListResponse.from_orm(updated_contact_list)

    @staticmethod
    async def remove_contact_from_list(contact_list_id: int, contact_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        contact_list_repo = ContactListRepository(db)
        contact_list_service = ContactListService(contact_list_repo)
        updated_contact_list = contact_list_service.remove_contact_from_list(contact_list_id, contact_id)
        return ContactListResponse.from_orm(updated_contact_list)
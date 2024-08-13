from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..services.contact_list_service import ContactListService
from ..repositories.contact_list_repository import ContactListRepository
from ..schemas.contact_list import ContactListCreate, ContactListResponse
from ..models.user import User

class ContactListHandler:
    def __init__(self, db: Session):
        self.db = db
        self.contact_list_repo = ContactListRepository(db)
        self.contact_list_service = ContactListService(self.contact_list_repo)

    async def create_contact_list(self, contact_list: ContactListCreate, current_user: User):
        new_contact_list = self.contact_list_service.create_contact_list(current_user.id, contact_list.name)
        return ContactListResponse.from_orm(new_contact_list)

    async def get_user_contact_lists(self, current_user: User):
        contact_lists = self.contact_list_service.get_user_contact_lists(current_user.id)
        return [ContactListResponse.from_orm(cl) for cl in contact_lists]

    async def add_contact_to_list(self, contact_list_id: int, contact_id: int, current_user: User):
        updated_contact_list = self.contact_list_service.add_contact_to_list(contact_list_id, contact_id, current_user.id)
        return ContactListResponse.from_orm(updated_contact_list)

    async def remove_contact_from_list(self, contact_list_id: int, contact_id: int, current_user: User):
        updated_contact_list = self.contact_list_service.remove_contact_from_list(contact_list_id, contact_id, current_user.id)
        return ContactListResponse.from_orm(updated_contact_list)
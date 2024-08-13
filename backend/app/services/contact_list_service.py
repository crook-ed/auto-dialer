from ..repositories.contact_list_repository import ContactListRepository
from fastapi import HTTPException

class ContactListService:
    def __init__(self, contact_list_repository: ContactListRepository):
        self.contact_list_repository = contact_list_repository

    def create_contact_list(self, user_id: int, name: str):
        return self.contact_list_repository.create(user_id, name)

    def get_contact_list(self, contact_list_id: int):
        contact_list = self.contact_list_repository.get_by_id(contact_list_id)
        if not contact_list:
            raise HTTPException(status_code=404, detail="Contact list not found")
        return contact_list

    def get_user_contact_lists(self, user_id: int):
        return self.contact_list_repository.get_all_by_user(user_id)

    def add_contact_to_list(self, contact_list_id: int, contact_id: int, user_id: int):
        contact_list = self.get_contact_list(contact_list_id)
        if contact_list.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this contact list")
        return self.contact_list_repository.add_contact(contact_list_id, contact_id)

    def get_contact_list(self, contact_list_id: int):
        contact_list = self.contact_list_repository.get_by_id(contact_list_id)
        if not contact_list:
            raise HTTPException(status_code=404, detail="Contact list not found")
        return contact_list

    def remove_contact_from_list(self, contact_list_id: int, contact_id: int, user_id: int):
        contact_list = self.get_contact_list(contact_list_id)
        if contact_list.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this contact list")
        return self.contact_list_repository.remove_contact(contact_list_id, contact_id)
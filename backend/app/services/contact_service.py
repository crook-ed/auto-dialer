from ..repositories.contact_repository import ContactRepository
from fastapi import HTTPException

class ContactService:
    def __init__(self, contact_repository: ContactRepository):
        self.contact_repository = contact_repository

    def create_or_update_contact(self, user_id: int, first_name: str, last_name: str, city: str, phone_number: str):
        return self.contact_repository.create_or_update(user_id, first_name, last_name, city, phone_number)

    def get_contact(self, contact_id: int, user_id: int):
        contact = self.contact_repository.get_by_id(contact_id, user_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact

    def get_user_contacts(self, user_id: int):
        return self.contact_repository.get_all_by_user(user_id)

  
    def delete_contact(self, contact_id: int, user_id: int):
        contact = self.contact_repository.delete(contact_id, user_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return {"message": "Contact deleted successfully"}
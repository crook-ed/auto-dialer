from ..repositories.contact_repository import ContactRepository
from fastapi import HTTPException

class ContactService:
    def __init__(self, contact_repository: ContactRepository):
        self.contact_repository = contact_repository

    def create_or_update_contact(self, user_id: int, contact_data: dict):
        contact_id = contact_data.pop('id', None)
        if contact_id:
            contact = self.contact_repository.get_by_id(contact_id, user_id)
            if contact:
                return self.contact_repository.update(contact_id, user_id, **contact_data)
            else:
                raise HTTPException(status_code=404, detail="Contact not found")
        else:
            try:
                return self.contact_repository.create(user_id, **contact_data)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

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
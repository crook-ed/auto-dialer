from ..repositories.contact_repository import ContactRepository
from ..models.contact import Contact

class ContactService:
    def __init__(self, contact_repository: ContactRepository):
        self.contact_repository = contact_repository

    def create_contact(self, first_name: str, last_name: str, phone_number: str, user_id: int):
        new_contact = Contact(first_name=first_name, last_name=last_name, phone_number=phone_number, user_id=user_id)
        return self.contact_repository.create(new_contact)

    def get_contact(self, contact_id: int):
        return self.contact_repository.get_by_id(contact_id)

    # Add other business logic methods as needed
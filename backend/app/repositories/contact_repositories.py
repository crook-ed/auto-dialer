from sqlalchemy.orm import Session
from ..models.contact import Contact

class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, contact: Contact):
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def get_by_id(self, contact_id: int):
        return self.db.query(Contact).filter(Contact.id == contact_id).first()

    # Add other CRUD methods as needed
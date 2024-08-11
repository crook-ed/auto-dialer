from sqlalchemy.orm import Session
from ..models.contact import Contact

class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, first_name: str, last_name: str, city: str, phone_number: str):
        db_contact = Contact(user_id=user_id, first_name=first_name, last_name=last_name, city=city, phone_number=phone_number)
        self.db.add(db_contact)
        self.db.commit()
        self.db.refresh(db_contact)
        return db_contact

    def get_by_id(self, contact_id: int):
        return self.db.query(Contact).filter(Contact.id == contact_id).first()

    def get_all_by_user(self, user_id: int):
        return self.db.query(Contact).filter(Contact.user_id == user_id).all()

    def update(self, contact_id: int, **kwargs):
        self.db.query(Contact).filter(Contact.id == contact_id).update(kwargs)
        self.db.commit()
        return self.get_by_id(contact_id)

    def delete(self, contact_id: int):
        contact = self.get_by_id(contact_id)
        if contact:
            self.db.delete(contact)
            self.db.commit()
        return contact
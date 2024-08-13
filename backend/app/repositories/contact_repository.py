from sqlalchemy.orm import Session
from ..models import Contact
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, first_name: str, last_name: str, city: str, phone_number: str):
        try:
            contact = Contact(user_id=user_id, first_name=first_name, last_name=last_name, city=city, phone_number=phone_number)
            self.db.add(contact)
            self.db.commit()
            self.db.refresh(contact)
            return contact
        except IntegrityError as e:
            self.db.rollback()
            # Check if the error is due to a duplicate phone number for the same user
            existing_contact = self.db.query(Contact).filter(
                and_(Contact.user_id == user_id, Contact.phone_number == phone_number)
            ).first()
            if existing_contact:
                raise ValueError("A contact with this phone number already exists for this user")
            else:
                # If it's not due to a duplicate for the same user, we can proceed
                return self.create(user_id, first_name, last_name, city, phone_number)

    def update(self, contact_id: int, user_id: int, **kwargs):
        contact = self.get_by_id(contact_id, user_id)
        if contact:
            for key, value in kwargs.items():
                setattr(contact, key, value)
            self.db.commit()
            self.db.refresh(contact)
        return contact
    
    def get_all_by_user(self, user_id: int):
        return self.db.query(Contact).filter(Contact.user_id == user_id).all()

    def get_by_id(self, contact_id: int, user_id: int):
        return self.db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()

    def delete(self, contact_id: int, user_id: int):
        contact = self.get_by_id(contact_id, user_id)
        if contact:
            self.db.delete(contact)
            self.db.commit()
        return contact
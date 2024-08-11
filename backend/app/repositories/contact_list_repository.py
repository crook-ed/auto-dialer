from sqlalchemy.orm import Session
from ..models.contact_list import ContactList

class ContactListRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, name: str):
        db_contact_list = ContactList(user_id=user_id, name=name)
        self.db.add(db_contact_list)
        self.db.commit()
        self.db.refresh(db_contact_list)
        return db_contact_list

    def get_by_id(self, contact_list_id: int):
        return self.db.query(ContactList).filter(ContactList.id == contact_list_id).first()

    def get_all_by_user(self, user_id: int):
        return self.db.query(ContactList).filter(ContactList.user_id == user_id).all()

    def add_contact(self, contact_list_id: int, contact_id: int):
        contact_list = self.get_by_id(contact_list_id)
        contact = self.db.query(Contact).filter(Contact.id == contact_id).first()
        if contact_list and contact:
            contact_list.contacts.append(contact)
            self.db.commit()
        return contact_list

    def remove_contact(self, contact_list_id: int, contact_id: int):
        contact_list = self.get_by_id(contact_list_id)
        contact = self.db.query(Contact).filter(Contact.id == contact_id).first()
        if contact_list and contact:
            contact_list.contacts.remove(contact)
            self.db.commit()
        return contact_list
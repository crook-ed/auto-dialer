from sqlalchemy.orm import Session, joinedload
from ..models.contact_list import ContactList
from ..models.contact import Contact
import logging

logger = logging.getLogger(__name__)

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
        return self.db.query(ContactList).options(joinedload(ContactList.contacts)).filter(ContactList.id == contact_list_id).first()

    def get_by_id(self, contact_list_id: int):
        contact_list = self.db.query(ContactList).options(joinedload(ContactList.contacts)).filter(ContactList.id == contact_list_id).first()
        if contact_list:
            logger.info(f"Contact list {contact_list_id} found with {len(contact_list.contacts)} contacts")
            for contact in contact_list.contacts:
                logger.info(f"Contact: id={contact.id}, first_name={contact.first_name}, city={contact.city}, phone={contact.phone_number}")
        else:
            logger.warning(f"Contact list {contact_list_id} not found")
        return contact_list

    def add_contact(self, contact_list_id: int, contact_id: int, user_id: int):
        contact_list = self.get_by_id(contact_list_id)
        contact = self.db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()
        if contact_list and contact and contact_list.user_id == user_id:
            if contact not in contact_list.contacts:
                contact_list.contacts.append(contact)
                self.db.commit()
                return contact_list
        return None

    def remove_contact(self, contact_list_id: int, contact_id: int, user_id: int):
        contact_list = self.get_by_id(contact_list_id)
        contact = self.db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()
        if contact_list and contact and contact_list.user_id == user_id:
            contact_list.contacts.remove(contact)
            self.db.commit()
        return contact_list
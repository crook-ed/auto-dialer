from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import Base

contact_list_association = Table('contact_list_association', Base.metadata,
    Column('contact_id', Integer, ForeignKey('contacts.id')),
    Column('contact_list_id', Integer, ForeignKey('contact_lists.id'))
)

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    city = Column(String)
    phone_number = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="contacts")
    contact_lists = relationship("ContactList", secondary=contact_list_association, back_populates="contacts")
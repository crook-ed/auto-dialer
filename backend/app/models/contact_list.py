from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import Base
from .associations import contact_list_association

# contact_list_association = Table('contact_list_association', Base.metadata,
#     Column('contact_id', Integer, ForeignKey('contacts.id')),
#     Column('contact_list_id', Integer, ForeignKey('contact_lists.id'))
# )

class ContactList(Base):
    __tablename__ = "contact_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="contact_lists")
    contacts = relationship("Contact", secondary=contact_list_association, back_populates="contact_lists")
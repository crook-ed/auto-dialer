from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    city = Column(String)
    phone_number = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="contacts")
    contact_lists = relationship("ContactList", secondary="contact_list_association", back_populates="contacts")

    __table_args__ = (
        UniqueConstraint('user_id', 'phone_number', name='uq_user_phone'),
    )
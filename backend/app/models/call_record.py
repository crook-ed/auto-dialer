from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from ..database import Base

class CallRecord(Base):
    __tablename__ = "call_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    call_datetime = Column(DateTime)
    duration = Column(Integer)  # in seconds
    cost = Column(Float)
    status = Column(String)

    user = relationship("User")
    contact = relationship("Contact")
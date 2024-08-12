from pydantic import BaseModel
from typing import List
from .contact import ContactResponse

class ContactListBase(BaseModel):
    name: str

class ContactListCreate(ContactListBase):
    pass

class ContactListResponse(ContactListBase):
    id: int
    user_id: int
    contacts: List[ContactResponse] = []

    class Config:
        orm_mode = True
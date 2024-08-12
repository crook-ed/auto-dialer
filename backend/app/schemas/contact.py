from pydantic import BaseModel
from typing import Optional

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    city: str
    phone_number: str

class ContactCreate(ContactBase):
    id: Optional[int] = None

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    city: Optional[str] = None
    phone_number: Optional[str] = None

class ContactResponse(ContactBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    city: str
    phone_number: str

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    first_name: str | None = None
    last_name: str | None = None
    city: str | None = None
    phone_number: str | None = None

class ContactResponse(ContactBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
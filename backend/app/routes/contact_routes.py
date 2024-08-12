from fastapi import APIRouter, Depends
from ..handlers.contact_handler import ContactHandler
from ..schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate, handler: ContactHandler = Depends()):
    return await handler.create_contact(contact)

@router.get("/", response_model=List[ContactResponse])
async def get_user_contacts(handler: ContactHandler = Depends()):
    return await handler.get_user_contacts()

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactUpdate, handler: ContactHandler = Depends()):
    return await handler.update_contact(contact_id, contact)

@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, handler: ContactHandler = Depends()):
    return await handler.delete_contact(contact_id)
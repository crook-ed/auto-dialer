from fastapi import APIRouter, Depends
from ..handlers.contact_list_handler import ContactListHandler
from ..schemas.contact_list import ContactListCreate, ContactListResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=ContactListResponse)
async def create_contact_list(contact_list: ContactListCreate, handler: ContactListHandler = Depends()):
    return await handler.create_contact_list(contact_list)

@router.get("/", response_model=List[ContactListResponse])
async def get_user_contact_lists(handler: ContactListHandler = Depends()):
    return await handler.get_user_contact_lists()

@router.post("/{contact_list_id}/contacts/{contact_id}")
async def add_contact_to_list(contact_list_id: int, contact_id: int, handler: ContactListHandler = Depends()):
    return await handler.add_contact_to_list(contact_list_id, contact_id)

@router.delete("/{contact_list_id}/contacts/{contact_id}")
async def remove_contact_from_list(contact_list_id: int, contact_id: int, handler: ContactListHandler = Depends()):
    return await handler.remove_contact_from_list(contact_list_id, contact_id)
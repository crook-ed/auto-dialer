from fastapi import APIRouter, Depends
from ..handlers.auto_dialer_handler import AutoDialerHandler
from ..schemas.auto_dialer import AutoDialerRequest, CallRecordResponse
from typing import List

router = APIRouter()

@router.post("/initiate", response_model=List[CallRecordResponse])
async def initiate_calls(request: AutoDialerRequest, handler: AutoDialerHandler = Depends()):
    return await handler.initiate_calls(request)

@router.get("/records", response_model=List[CallRecordResponse])
async def get_call_records(handler: AutoDialerHandler = Depends()):
    return await handler.get_call_records()
from fastapi import APIRouter, Depends
from ..handlers.auto_dialer_handler import AutoDialerHandler
from ..schemas.auto_dialer import AutoDialerRequest, CallRecordResponse
from typing import List
from ..utils.auth import get_current_user
from ..models.user import User
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/initiate", response_model=List[CallRecordResponse])
async def initiate_calls(
    request: AutoDialerRequest, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    handler = AutoDialerHandler()
    call_records = await handler.initiate_calls(request, current_user, db)
    if not call_records:
        return {"message": "No calls were initiated. Check server logs for details."}, 400
    return call_records

@router.get("/records", response_model=List[CallRecordResponse])
async def get_call_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        handler = AutoDialerHandler()
        return await handler.get_call_records(current_user, db)
    except Exception as e:
        return {"error": str(e)}, 500 
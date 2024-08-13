from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.auto_dialer_service import AutoDialerService
from ..repositories.contact_list_repository import ContactListRepository
from ..repositories.call_record_repository import CallRecordRepository
from ..schemas.auto_dialer import AutoDialerRequest, CallRecordResponse
from ..utils.auth import get_current_user
from ..models.user import User
from typing import List

class AutoDialerHandler:
    @staticmethod
    async def initiate_calls(
        request: AutoDialerRequest, 
        current_user: User = Depends(get_current_user), 
        db: Session = Depends(get_db)
    ):
        contact_list_repo = ContactListRepository(db)
        call_record_repo = CallRecordRepository(db)
        auto_dialer_service = AutoDialerService(contact_list_repo, call_record_repo)
        try:
            call_records = await auto_dialer_service.initiate_calls(current_user.id, request.contact_list_id, request.message)
            return [CallRecordResponse.from_orm(record) for record in call_records]
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_call_records(
        current_user: User = Depends(get_current_user), 
        db: Session = Depends(get_db)
    ):
        try:
            call_record_repo = CallRecordRepository(db)
            auto_dialer_service = AutoDialerService(None, call_record_repo)
            call_records = auto_dialer_service.get_call_records(current_user.id)
            return [CallRecordResponse.from_orm(record) for record in call_records]
        except Exception as e:
            print(f"Error retrieving call records: {str(e)}")
            return []
from sqlalchemy.orm import Session
from ..models.call_record import CallRecord
from datetime import datetime

class CallRecordRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, contact_id: int, call_datetime: datetime, duration: int, cost: float, status: str):
        db_call_record = CallRecord(
            user_id=user_id,
            contact_id=contact_id,
            call_datetime=call_datetime,
            duration=duration,
            cost=cost,
            status=status
        )
        self.db.add(db_call_record)
        self.db.commit()
        self.db.refresh(db_call_record)
        return db_call_record

    def get_by_user(self, user_id: int):
        return self.db.query(CallRecord).filter(CallRecord.user_id == user_id).all()
    
    def update(self, call_record_id: int, **kwargs):
        call_record = self.db.query(CallRecord).filter(CallRecord.id == call_record_id).first()
        if call_record:
            for key, value in kwargs.items():
                setattr(call_record, key, value)
            self.db.commit()
            self.db.refresh(call_record)
        return call_record
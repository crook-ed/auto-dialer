from pydantic import BaseModel
from datetime import datetime

class AutoDialerRequest(BaseModel):
    contact_list_id: int
    message: str

class CallRecordBase(BaseModel):
    call_datetime: datetime
    duration: int
    cost: float
    status: str

class CallRecordResponse(CallRecordBase):
    id: int
    user_id: int
    contact_id: int

    class Config:
        from_attributes = True
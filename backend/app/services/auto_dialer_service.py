from ..repositories.contact_list_repository import ContactListRepository
from ..repositories.call_record_repository import CallRecordRepository
from fastapi import HTTPException
from twilio.rest import Client
from ..config import settings
import datetime

class AutoDialerService:
    def __init__(self, contact_list_repository: ContactListRepository, call_record_repository: CallRecordRepository):
        self.contact_list_repository = contact_list_repository
        self.call_record_repository = call_record_repository
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def initiate_calls(self, user_id: int, contact_list_id: int, message: str):
        contact_list = self.contact_list_repository.get_by_id(contact_list_id)
        if not contact_list:
            raise HTTPException(status_code=404, detail="Contact list not found")

        call_records = []
        for contact in contact_list.contacts:
            personalized_message = f"Hello {contact.first_name} from {contact.city}. {message}"
            try:
                call = self.twilio_client.calls.create(
                    twiml=f'<Response><Say>{personalized_message}</Say></Response>',
                    to=contact.phone_number,
                    from_=settings.TWILIO_PHONE_NUMBER
                )
                call_record = self.call_record_repository.create(
                    user_id=user_id,
                    contact_id=contact.id,
                    call_datetime=datetime.datetime.utcnow(),
                    duration=0,  # Duration will be updated when the call is completed
                    cost=0,  # Cost will be updated when the call is completed
                    status=call.status
                )
                call_records.append(call_record)
            except Exception as e:
                # Log the error and continue with the next contact
                print(f"Error calling {contact.phone_number}: {str(e)}")

        return call_records

    def get_call_records(self, user_id: int):
        return self.call_record_repository.get_by_user(user_id)
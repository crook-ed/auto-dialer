import asyncio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from ..config import settings
from ..repositories.contact_list_repository import ContactListRepository
from ..repositories.call_record_repository import CallRecordRepository
from datetime import datetime

class AutoDialerService:
    def __init__(self, contact_list_repository: ContactListRepository, call_record_repository: CallRecordRepository):
        self.contact_list_repository = contact_list_repository
        self.call_record_repository = call_record_repository
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    async def initiate_calls(self, user_id: int, contact_list_id: int, message: str):
        contact_list = self.contact_list_repository.get_by_id(contact_list_id)
        if not contact_list:
            raise ValueError(f"Contact list with id {contact_list_id} not found")

        call_records = []
        tasks = []
        for contact in contact_list.contacts:
            task = asyncio.create_task(self._make_call(user_id, contact, message))
            tasks.append(task)

        call_records = await asyncio.gather(*tasks)
        return [record for record in call_records if record is not None]

    async def _make_call(self, user_id: int, contact, message: str):
        personalized_message = f"Hello {contact.first_name} from {contact.city}. {message}"
        try:
            call = await self.twilio_client.calls.create(
                twiml=f'<Response><Say>{personalized_message}</Say></Response>',
                to=contact.phone_number,
                from_=settings.TWILIO_PHONE_NUMBER
            )
            return self.call_record_repository.create(
                user_id=user_id,
                contact_id=contact.id,
                call_datetime=datetime.utcnow(),
                duration=0,
                cost=0,
                status=call.status
            )
        except TwilioRestException as e:
            print(f"Twilio error for {contact.phone_number}: {str(e)}")
            # Log the error
        except Exception as e:
            print(f"Unexpected error calling {contact.phone_number}: {str(e)}")
            # Log the error
        return None

    def get_call_records(self, user_id: int, skip: int = 0, limit: int = 100):
        all_records = self.call_record_repository.get_by_user(user_id)
        return all_records[skip:skip+limit]
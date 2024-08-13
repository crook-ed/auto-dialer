import asyncio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from ..config import settings
from ..repositories.contact_list_repository import ContactListRepository
from ..repositories.call_record_repository import CallRecordRepository
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoDialerService:
    def __init__(self, contact_list_repository: ContactListRepository, call_record_repository: CallRecordRepository):
        self.contact_list_repository = contact_list_repository
        self.call_record_repository = call_record_repository
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    async def initiate_calls(self, user_id: int, contact_list_id: int, message: str):
        contact_list = self.contact_list_repository.get_by_id(contact_list_id)
        if not contact_list:
            logger.error(f"Contact list with id {contact_list_id} not found")
            return []

        call_records = []
        for contact in contact_list.contacts:
            personalized_message = f"Hello {contact.first_name} from {contact.city}. {message}"
            try:
                call = await self.make_call(contact.phone_number, personalized_message)
                call_record = self.call_record_repository.create(
                    user_id=user_id,
                    contact_id=contact.id,
                    call_datetime=datetime.utcnow(),
                    duration=0,  # Duration will be updated when the call is completed
                    cost=0,  # Cost will be updated when the call is completed
                    status=call.status
                )
                call_records.append(call_record)
                logger.info(f"Call initiated for {contact.phone_number}, status: {call.status}")
            except Exception as e:
                logger.error(f"Error calling {contact.phone_number}: {str(e)}")

        return call_records

    async def make_call(self, to_number: str, message: str):
        try:
            call = await asyncio.to_thread(
                self.twilio_client.calls.create,
                twiml=f'<Response><Say>{message}</Say></Response>',
                to=to_number,
                from_=settings.TWILIO_PHONE_NUMBER
            )
            return call
        except TwilioRestException as e:
            logger.error(f"Twilio error: {e}")
            raise

    def get_call_records(self, user_id: int):
        return self.call_record_repository.get_by_user(user_id)
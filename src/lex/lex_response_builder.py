import logging
from src.schedule_service.dependencies import ResponseBuilder
from src.persistent_data import PersistentData

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


class LexResponseBuilder(ResponseBuilder):
    'Class responsible for building responses in the format accepted by AWS Lex.'

    def ask_for_input(self, intent_name, slots, slot_to_elicit, message, session_attributes: PersistentData):
        elicit = {
            'sessionAttributes': session_attributes.data(),
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': intent_name,
                'slots': slots,
                'slotToElicit': slot_to_elicit,
                'message': {
                    'contentType': 'PlainText',
                    'content': message
                }
            }
        }

        LOGGER.debug(f'eliciting input={elicit}')
        return elicit

    def confirm_inputs(self, intent_name, slots, message, session_attributes: PersistentData):
        confirmation = {
            'sessionAttributes': session_attributes.data(),
            'dialogAction': {
                'type': 'ConfirmIntent',
                'intentName': intent_name,
                'slots': slots,
                'message': {
                    'contentType': 'PlainText',
                    'content': message
                }
            }
        }

        LOGGER.debug(f'confirming inputs={confirmation}')
        return confirmation

    def notify_completion(self, is_complete, message, session_attributes: PersistentData):
        fulfillment_state = 'Fulfilled' if is_complete else 'Failed'
        response = {
            'sessionAttributes': session_attributes.data(),
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': fulfillment_state,
                'message': {
                    'contentType': 'PlainText',
                    'content': message
                }
            }
        }

        LOGGER.debug(f'closing={response}')
        return response

from src.schedule_service.service_scheduler import ServiceScheduler
from src.lex.lex_response_builder import LexResponseBuilder
from src.persistent_data import PersistentData


def dispatch(event):
    current_intent = event['currentIntent']
    confirmation_status = None if current_intent[
        'confirmationStatus'] == 'None' else current_intent['confirmationStatus']

    if not current_intent['name'] == 'ScheduleService':
        raise Exception(
            f"Intent with name {current_intent['name']} not supported.")

    return ServiceScheduler(
        current_intent['slots']['serviceSelection'],
        current_intent['slots']['serviceDate'],
        current_intent['slots']['serviceTime'],
        confirmation_status,
        LexResponseBuilder(),
        PersistentData.load(event['sessionAttributes'])
    ).next_step()

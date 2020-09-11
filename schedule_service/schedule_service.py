from schedule_service.service_scheduler import ServiceScheduler
from schedule_service.lex_response_builder import LexResponseBuilder

def lambda_handler(event, context):
    current_intent = event['currentIntent']
    if not current_intent['name'] == 'ScheduleService':
        raise Exception(f"Intent with name {current_intent['name']} not supported.")

    return ServiceScheduler(
        current_intent['slots']['serviceSelection'],
        current_intent['slots']['serviceDate'],
        current_intent['slots']['serviceTime'],
        LexResponseBuilder()
    ).next_step()

import time
import os
import logging

from list_actions import list_actions
from schedule_service import schedule_service

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    os.environ['TZ'] = 'America/Sao_Paulo'
    time.tzset()
    logger.debug(f'event={event}')

    intentName = event['currentIntent']['name']
    if intentName == 'ListAvailableActions':
        return list_actions.dispatch(event)
    elif intentName == 'ScheduleService':
        return schedule_service.dispatch(event)
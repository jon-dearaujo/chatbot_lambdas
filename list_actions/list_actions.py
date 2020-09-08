import json
import time
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

'''
Fixed messages;
'''
def buildResponseMessage():
    return '''
Olá, sou o Assistente Virtual da BioFace.

Abaixo estão as ações disponíveis neste canal. Digite a opção que corresponde à ação desejada:

- Agendar um serviço.
- Cancelar um serviço.
    '''

def elicitIntent(sessionAttributes):
    return {
        'sessionAttributes': sessionAttributes,
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': {
                'contentType': 'PlainText',
                'content': buildResponseMessage()
            }
        }
    }

def dispatch(event):

    intentName = event['currentIntent']['name']
    invocationSource = event['invocationSource']

    if not intentName == 'ListAvailableActions':
        raise Exception('Intent with name ' + intentName + ' not supported')

    if not invocationSource == 'FulfillmentCodeHook':
        raise Exception('ListAvailableActions needs only a fulfillment handler')

    return elicitIntent(
        event['sessionAttributes'] if event['sessionAttributes'] is not None else {},
    )


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    os.environ['TZ'] = 'America/Sao_Paulo'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
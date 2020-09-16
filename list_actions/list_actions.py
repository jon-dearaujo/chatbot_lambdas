'List the actions available in the Chatbot, like "schedule appointment" or "cancel appointment".'
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

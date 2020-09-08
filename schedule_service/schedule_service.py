services = [
    'Radiografias Intra-Bucais.',
    'Radiografias Extra-Bucais.',
    'Tomografia Computadorizada de Feixe Cônico.',
    'Documentação Ortodôntica Digital.',
    'Documentação Padrão Dolphin 2D / 3D.'
]


def buildServicesListMessage():
    baseMessage = """
Este são os serviços disponíveis para agendamento.
Digite 'Opção' seguido pela letra da opção. Exemplo: 'Opção 1'
    """
    return baseMessage.join(["""
        {} - {}
    """.format(index + 1, service) for index, service in enumerate(services)])


def _validateServiceNumber(serviceSlot):
    pass


def lambda_handler(event, context):

    currentIntent = event['currentIntent']
    inputSlots = currentIntent['slots']

    if not currentIntent['name'] == 'ScheduleService':
        raise Exception('Intent with name {} not supported'.format(currentIntent['name']))

    if inputSlots['serviceNumber']:
        _validateServiceNumber(inputSlots['serviceNumber'])

    return {
        'dialogAction': {
            'intentName': 'ScheduleService',
            'type': 'ElicitSlot',
            'message': {
                'contentType': 'PlainText',
                'content': buildServicesListMessage()
            },
            'slotToElicit': 'serviceNumber',
            'slots': {
                'serviceNumber': None
            }
        }
    }
import unittest
from schedule_service import schedule_service

class TestScheduleService(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.event = {
            'invocationSource': 'DialogCodeHook',
            'currentIntent': {
                'name': 'ScheduleService',
                'slots': {
                    'serviceNumber': None
                }
            },
            'bot': {
                'name': 'BioFaceAppointment'
            },
            'sessionAttributes': None
        }

    def test_response_must_ask_list_services_and_ask_for_user_selection(self):
        result = schedule_service.lambda_handler(self.event, self.context)
        dialogAction = result['dialogAction']
        dialogActionMessage = dialogAction['message']

        self.assertEqual('ScheduleService', dialogAction['intentName'])
        self.assertEqual('ElicitSlot', dialogAction['type'])
        self.assertTrue('PlainText' in dialogActionMessage['contentType'])

        self._assert_available_services(dialogActionMessage['content'])


    def test_response_must_include_slots_and_slot_to_elicit_if_service_number_not_provided_yet(self):
        self.event['currentIntent']['slots']['serviceNumber'] = None
        result = schedule_service.lambda_handler(self.event, self.context)
        dialogAction = result['dialogAction']

        self.assertEqual('serviceNumber', dialogAction['slotToElicit'])
        self.assertTrue('serviceNumber' in dialogAction['slots'])


    def test_handler_must_only_handle_ScheduleService_intent(self):
        self.event['currentIntent']['name'] = 'AnotherIntent'
        with self.assertRaises(Exception) as capturedError:
            schedule_service.lambda_handler(self.event, self.context)

        self.assertEqual(
            'Intent with name AnotherIntent not supported',
            str(capturedError.exception)
        )


    def test_handler_must_ask_again_if_provided_option__for_serviceNumber_is_invalid(self):
        self.event['currentIntent']['slots'] = {'serviceNumber': 'whateverinvalidvalue'}
        result = schedule_service.lambda_handler(self.event, self.context)
        dialogAction = result['dialogAction']

        self.assertEqual('ElicitSlot', dialogAction['type'])
        self.assertTrue('PlainText' in dialogAction['message']['contentType'])

        self.assertTrue(
            'Não consegui identificar a opção selecionada. Por gentileza, tente novamente'
                in dialogAction['message']['content'],
            'Validation message not present'
        )
        self._assert_available_services(dialogAction['message']['content'])



    def _assert_available_services(self, messageText):
        services =[
            'Radiografias Intra-Bucais.',
            'Radiografias Extra-Bucais.',
            'Tomografia Computadorizada de Feixe Cônico.',
            'Documentação Ortodôntica Digital.',
            'Documentação Padrão Dolphin 2D / 3D.'
        ]
        for service in services:
            self.assertTrue(service in messageText, '{} not found'.format(service))


import unittest
import json
from src.schedule_service import schedule_service


class TestScheduleService(unittest.TestCase):
    def setUp(self):
        self.event = {
            'invocationSource': 'DialogCodeHook',
            'currentIntent': {
                'name': 'ScheduleService',
                'slots': {
                    'serviceSelection': None,
                    'serviceDate': None,
                    'serviceTime': None
                },
                'confirmationStatus': None
            },
            'bot': {
                'name': 'BioFaceAppointment'
            },
            'sessionAttributes': None
        }
        self.__available_services = [
            'Radiografias Intra-Bucais',
            'Radiografias Extra-Bucais',
            'Tomografia Computadorizada de Feixe Cônico',
            'Documentação Ortodôntica Digital',
            'Documentação Padrão Dolphin 2D / 3D'
        ]

        self.__available_dates = [
            '10/09/2020',
            '11/09/2020',
            '12/09/2020',
            '13/09/2020',
            '14/09/2020',
            '15/09/2020',
            '16/09/2020',
            '17/09/2020',
        ]

        self.__available_times = [
            '10:00 AM',
            '11:00 AM',
            '12:00 AM',
            '01:00 PM',
            '02:00 PM',
            '03:00 PM',
        ]

    def test_response_must_list_services_and_ask_for_user_selection(self):
        result = schedule_service.dispatch(self.event)
        dialogAction = result['dialogAction']
        dialogActionMessage = dialogAction['message']

        self.assertEqual('ScheduleService', dialogAction['intentName'])
        self.assertEqual('ElicitSlot', dialogAction['type'])
        self.assertTrue('PlainText' in dialogActionMessage['contentType'])

        self.__assert_available_services(dialogActionMessage['content'])

    def test_response_must_include_slots_and_slot_to_elicit_if_service_number_not_provided_yet(self):
        self.event['currentIntent']['slots']['serviceSelection'] = None
        result = schedule_service.dispatch(self.event)
        dialogAction = result['dialogAction']

        self.assertEqual('serviceSelection', dialogAction['slotToElicit'])
        self.assertTrue('serviceSelection' in dialogAction['slots'])

    def test_handler_must_only_handle_ScheduleService_intent(self):
        self.event['currentIntent']['name'] = 'AnotherIntent'
        with self.assertRaises(Exception) as capturedError:
            schedule_service.dispatch(self.event)

        self.assertEqual(
            'Intent with name AnotherIntent not supported.',
            str(capturedError.exception)
        )

    def test_handler_must_ask_again_if_provided_option_for_serviceNumber_is_invalid(self):
        self.event['currentIntent']['slots']['serviceSelection'] = 'whateverinvalidvalue'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services)
        }

        result = schedule_service.dispatch(self.event)
        dialogAction = result['dialogAction']

        self.assertEqual('ElicitSlot', dialogAction['type'])
        self.assertTrue('serviceNumber', dialogAction['slotToElicit'])
        self.assertTrue('PlainText' in dialogAction['message']['contentType'])

        self.assertTrue(
            'Não consegui identificar o serviço desejado. Por gentileza, tente novamente.'
            in dialogAction['message']['content'],
            'Validation message not present'
        )
        self.__assert_available_services(dialogAction['message']['content'])

    def test_handler_must_ask_for_service_date_given_that_serviceNumber_is_already_provided(self):
        self.event['currentIntent']['slots']['serviceSelection'] = '1'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services),
        }
        result = schedule_service.dispatch(self.event)

        dialog_action = result['dialogAction']

        self.assertEqual('ElicitSlot', dialog_action['type'])
        self.assertTrue('serviceData', dialog_action['slotToElicit'])

        self.assertTrue(
            'Estas são as datas disponíveis' in dialog_action['message']['content']
        )

    def test_handler_must_ask_again_for_service_date_if_it_has_invalid_value(self):
        self.event['currentIntent']['slots']['serviceSelection'] = '1'
        self.event['currentIntent']['slots']['serviceDate'] = '10'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services),
            'availableDates': json.dumps(self.__available_dates),
        }
        result = schedule_service.dispatch(self.event)

        dialog_action = result['dialogAction']

        self.assertEqual('ElicitSlot', dialog_action['type'])
        self.assertTrue('serviceData', dialog_action['slotToElicit'])

        self.assertTrue(
            'Não consegui identificar a data desejada. Por gentileza, tente novamente.'
            in dialog_action['message']['content']
        )
        self.assertTrue(
            'Estas são as datas disponíveis' in dialog_action['message']['content']
        )

    def test_handler_must_ask_for_service_time_given_that_serviceNumber_and_serviceDate_are_already_provided(self):
        self.event['currentIntent']['slots']['serviceSelection'] = '1'
        self.event['currentIntent']['slots']['serviceDate'] = '1'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services),
            'availableDates': json.dumps(self.__available_dates),
        }

        result = schedule_service.dispatch(self.event)

        dialog_action = result['dialogAction']

        self.assertEqual('ElicitSlot', dialog_action['type'])
        self.assertTrue('serviceTime', dialog_action['slotToElicit'])

        self.assertTrue(
            'Estes são os horários disponíveis' in dialog_action['message']['content']
        )

    def test_handler_must_ask_again_for_service_time_if_it_has_invalid_value(self):
        self.event['currentIntent']['slots']['serviceSelection'] = '1'
        self.event['currentIntent']['slots']['serviceDate'] = '1'
        self.event['currentIntent']['slots']['serviceTime'] = '10'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services),
            'availableDates': json.dumps(self.__available_dates),
            'availableTimes': json.dumps(self.__available_times)
        }

        result = schedule_service.dispatch(self.event)

        dialog_action = result['dialogAction']

        self.assertEqual('ElicitSlot', dialog_action['type'])
        self.assertTrue('serviceTime', dialog_action['slotToElicit'])

        expected_warning_message = 'Não consegui identificar o horário desejado. Por gentileza, tente novamente.'
        self.assertTrue(
            expected_warning_message
            in dialog_action['message']['content'],
            f"'{expected_warning_message}' not found"
        )
        self.assertTrue(
            'Estes são os horários disponíveis' in dialog_action['message']['content'],
            "'Estes são os horários disponíveis' not found"
        )

    def test_handler_must_confirm_values_after_all_inputs_are_provided(self):
        self.event['currentIntent']['slots']['serviceSelection'] = '1'
        self.event['currentIntent']['slots']['serviceDate'] = '1'
        self.event['currentIntent']['slots']['serviceTime'] = '1'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services),
            'availableDates': json.dumps(self.__available_dates),
            'availableTimes': json.dumps(self.__available_times)
        }

        result = schedule_service.dispatch(self.event)
        dialog_action = result['dialogAction']

        self.assertEqual('ConfirmIntent', dialog_action['type'])
        self.assertEqual('PlainText', dialog_action['message']['contentType'])
        self.assertTrue(
            'Você confirma o agendamento de' in dialog_action['message']['content'])

    def test_handler_must_close_interaction_once_all_inputs_are_fulfilled_and_user_has_confirmed(self):
        self.event['currentIntent']['slots']['serviceSelection'] = '1'
        self.event['currentIntent']['slots']['serviceDate'] = '1'
        self.event['currentIntent']['slots']['serviceTime'] = '1'
        self.event['currentIntent']['confirmationStatus'] = 'Confirmed'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services),
            'availableDates': json.dumps(self.__available_dates),
            'availableTimes': json.dumps(self.__available_times)
        }

        result = schedule_service.dispatch(self.event)
        dialog_action = result['dialogAction']

        self.assertEqual('Close', dialog_action['type'])
        self.assertEqual('Fulfilled', dialog_action['fulfillmentState'])
        self.assertTrue('Agendamento realizado com sucesso, você receberá um lembrete no dia anterior. Tenha um bom dia'
                        in dialog_action['message']['content'])

    def test_handler_must_close_interaction_without_schedulling_once_all_inputs_are_fulfilled_and_user_has_denied_confirmation(self):
        self.event['currentIntent']['slots']['serviceSelection'] = '1'
        self.event['currentIntent']['slots']['serviceDate'] = '1'
        self.event['currentIntent']['slots']['serviceTime'] = '1'
        self.event['currentIntent']['confirmationStatus'] = 'Denied'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services),
            'availableDates': json.dumps(self.__available_dates),
            'availableTimes': json.dumps(self.__available_times)
        }

        result = schedule_service.dispatch(self.event)
        dialog_action = result['dialogAction']

        self.assertEqual('Close', dialog_action['type'])
        self.assertEqual('Failed', dialog_action['fulfillmentState'])
        self.assertTrue('Agendamento não realizado. Para interagir novamente, basta enviar uma nova mensagem e reiniciaremos o processo.'
                        in dialog_action['message']['content'])

    def test_handler_must_persist_loaded_available_services_when_asking_for_service_number(self):
        result = schedule_service.dispatch(self.event)

        self.assertIsNotNone(result['sessionAttributes']['availableServices'])

    def test_handler_must_persist_loaded_available_dates_when_asking_for_service_date(self):
        self.event['currentIntent']['slots']['serviceSelection'] = '1'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services),
        }
        result = schedule_service.dispatch(self.event)

        self.assertIsNotNone(result['sessionAttributes']['availableDates'])

    def test_handler_must_persist_loaded_available_times_when_asking_for_service_time(self):
        self.event['currentIntent']['slots']['serviceSelection'] = '1'
        self.event['currentIntent']['slots']['serviceDate'] = '1'
        self.event['sessionAttributes'] = {
            'availableServices': json.dumps(self.__available_services),
            'availableDates': json.dumps(self.__available_dates),
        }
        result = schedule_service.dispatch(self.event)

        self.assertIsNotNone(result['sessionAttributes']['availableTimes'])

    def __assert_available_services(self, messageText):
        services = [
            'Radiografias Intra-Bucais',
            'Radiografias Extra-Bucais',
            'Tomografia Computadorizada de Feixe Cônico',
            'Documentação Ortodôntica Digital',
            'Documentação Padrão Dolphin 2D / 3D'
        ]
        for service in services:
            self.assertTrue(service in messageText,
                            '{} not found'.format(service))

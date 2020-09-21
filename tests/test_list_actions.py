import unittest
import json
from src.list_actions import list_actions


class TestListActions(unittest.TestCase):

    def setUp(self):
        self.event = {
            'invocationSource': 'FulfillmentCodeHook',
            'currentIntent': {
                'name': 'ListAvailableActions'
            },
            'bot': {
                'name': 'BioFaceAppointment'
            },
            'sessionAttributes': None
        }

    def test_throws_error_when_not_list_options_intent(self):
        self.event['currentIntent']['name'] = 'anotherIntent'
        with self.assertRaises(Exception) as capturedError:
            list_actions.dispatch(self.event)

        self.assertEqual(
            'Intent with name anotherIntent not supported',
            str(capturedError.exception)
        )

    def test_throws_error_when_not_fulfillment_invocation_source(self):
        self.event['invocationSource'] = 'DialogCodeHook'
        with self.assertRaises(Exception) as capturedError:
            list_actions.dispatch(self.event)
        self.assertEqual(
            'ListAvailableActions needs only a fulfillment handler',
            str(capturedError.exception)
        )

    def test_must_return_an_ElicitIntent_asking_the_user_for_the_desired_action(self):
        response = list_actions.dispatch(self.event)
        response_dialog_action = response['dialogAction']
        self.assertEqual(
            'ElicitIntent',
            response_dialog_action['type']
        )

        self.assertEqual(
            'PlainText',
            response_dialog_action['message']['contentType']
        )
        self.assertTrue(
            '- Agendar um serviço.' in response_dialog_action['message']['content']
        )

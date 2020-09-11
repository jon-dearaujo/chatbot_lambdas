class LexResponseBuilder:
    def ask_for_input(self, intent_name, slots, slot_to_elicit, message):
        return {
            'sessionAttributes': None,
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
import logging

from src.schedule_service.dependencies import ResponseBuilder
from src.persistent_data import PersistentData

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


class ServiceScheduler:
    'Class responsible for controlling the appointment flow based on user provided inputs'

    def __init__(self, service_selection, service_date, service_time, confirmation_status,
                 response_builder: ResponseBuilder, persistent_data: PersistentData):
        self.__action_name = 'ScheduleService'
        self.__service_selection = service_selection
        self.__service_date = service_date
        self.__service_time = service_time
        self.__confirmation_status = confirmation_status
        self.__response_builder = response_builder
        self.__available_services = persistent_data.get('availableServices')
        self.__available_dates = persistent_data.get('availableDates')
        self.__available_times = persistent_data.get('availableTimes')

    def next_step(self):
        validation_result = self.__validate()
        if not validation_result['is_valid']:
            fields = self.__fields_to_object()
            fields[validation_result['invalid_field']] = None
            return self.__response_builder.ask_for_input(
                self.__action_name,
                fields,
                validation_result['invalid_field'],
                validation_result['message'],
                self.__get_persistent_data()
            )

        if not self.__service_selection:
            self.__load_services()
            return self.__response_builder.ask_for_input(
                self.__action_name,
                self.__fields_to_object(),
                'serviceSelection',
                self.__build_services_message(),
                self.__get_persistent_data()
            )

        if self.__service_selection and not self.__service_date:
            self.__load_service_dates()
            return self.__response_builder.ask_for_input(
                self.__action_name,
                self.__fields_to_object(),
                'serviceDate',
                self.__build_dates_message(),
                self.__get_persistent_data()
            )

        if self.__service_selection and self.__service_date and not self.__service_time:
            self.__load_service_times()
            return self.__response_builder.ask_for_input(
                self.__action_name,
                self.__fields_to_object(),
                'serviceTime',
                self.__build_times_message(),
                self.__get_persistent_data()
            )

        if not self.__confirmation_status:
            return self.__response_builder.confirm_inputs(
                self.__action_name,
                self.__fields_to_object(),
                self.__build_confirmation_message(),
                self.__get_persistent_data())
        elif self.__confirmation_status == 'Confirmed':
            # Schedule service on gcalendar
            return self.__response_builder.notify_completion(
                True,
                'Agendamento realizado com sucesso, você receberá um lembrete no dia anterior. Tenha um bom dia',
                self.__get_persistent_data())
        elif self.__confirmation_status == 'Denied':
            return self.__response_builder.notify_completion(
                False,
                'Agendamento não realizado. Para interagir novamente, basta enviar uma nova mensagem e reiniciaremos o processo.',
                self.__get_persistent_data())

    def __get_persistent_data(self) -> PersistentData:
        return PersistentData.dump({
            'availableServices': self.__available_services,
            'availableDates': self.__available_dates,
            'availableTimes': self.__available_times,
        })

    def __load_services(self):
        # Replace with real fetch from backend
        self.__available_services = [
            'Radiografias Intra-Bucais',
            'Radiografias Extra-Bucais',
            'Tomografia Computadorizada de Feixe Cônico',
            'Documentação Ortodôntica Digital',
            'Documentação Padrão Dolphin 2D / 3D'
        ]

    def __load_service_dates(self):
        # Replace with real fetch from backend
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

    def __load_service_times(self):
        # Replace with real fetch from backend
        self.__available_times = [
            '10:00 AM',
            '11:00 AM',
            '12:00 AM',
            '01:00 PM',
            '02:00 PM',
            '03:00 PM',
        ]

    def __fields_to_object(self):
        return {
            'serviceSelection': self.__service_selection,
            'serviceDate': self.__service_date,
            'serviceTime': self.__service_time
        }

    def __validate(self):
        if self.__service_selection and self.__available_services and not self.__service_selection_is_valid():
            return self.__build_validation_result(
                False,
                'serviceSelection',
                self.__build_services_message('Não consegui identificar o serviço desejado. Por gentileza, tente novamente.'))

        # REQUIRES THE AVAILABLE DATES TO BE ALREADY REQUESTED FROM G CALENDAR
        # In the ideal flow, it will be request right after the selection of the service
        # so there is no way of having a service_date without having it listed
        if self.__service_date and self.__available_dates and not self.__service_date_is_valid():
            return self.__build_validation_result(
                False,
                'serviceDate',
                self.__build_dates_message(
                    'Não consegui identificar a data desejada. Por gentileza, tente novamente.')
            )

        if self.__service_time and self.__available_times and not self.__service_time_is_valid():
            return self.__build_validation_result(
                False,
                'serviceTime',
                self.__build_times_message(
                    'Não consegui identificar o horário desejado. Por gentileza, tente novamente.')
            )
        return self.__build_validation_result(True, None, None)

    def __build_validation_result(self, is_valid, invalid_field_name, message):
        result = {'is_valid': is_valid,
                  'invalid_field': invalid_field_name, 'message': message}
        LOGGER.debug(f'Invalid input={result}')
        return result

    def __service_time_is_valid(self):
        return self.__option_index_is_valid_and_within_range(self.__service_time, len(self.__available_times))

    def __service_date_is_valid(self):
        return self.__option_index_is_valid_and_within_range(self.__service_date, len(self.__available_dates))

    def __service_selection_is_valid(self):
        return self.__option_index_is_valid_and_within_range(self.__service_selection, len(self.__available_services))

    def __option_index_is_valid_and_within_range(self, option_text, list_size):
        if not option_text.isnumeric():
            return False

        index = int(option_text)
        return index and index > 0 and index <= list_size

    def __build_times_message(self, text_to_append_before=''):
        return f"""
{text_to_append_before}
Estes são os horários disponíveis para {self.__available_services[int(self.__service_selection) - 1]} no dia {self.__available_dates[int(self.__service_date) - 1]}.
Digite o número da opção desejada.

{str().join([f'''{index + 1} - {time}
''' for index, time in enumerate(self.__available_times)])}
        """

    def __build_dates_message(self, text_to_append_before=''):
        return f"""
{text_to_append_before}
Estas são as datas disponíveis para {self.__available_services[int(self.__service_selection) - 1]}.
Digite o número da opção desejada.

{str().join([f'''{index + 1} - {date}
''' for index, date in enumerate(self.__available_dates)])}
        """

    def __build_services_message(self, text_to_append_before=''):
        return f"""
{text_to_append_before}
Este são os serviços disponíveis para agendamento.
Digite o número da opção desejada.

{str().join([f'''{index + 1} - {service}
''' for index, service in enumerate(self.__available_services)])}
        """

    def __build_confirmation_message(self):
        return f'''
Você confirma o agendamento de {self.__available_services[int(self.__service_selection) - 1]} no dia {self.__available_dates[int(self.__service_date) - 1]}
 às {self.__available_times[int(self.__service_time) - 1]}?
        '''

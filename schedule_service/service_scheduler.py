class ServiceScheduler:

    def __init__(self, service_selection, service_date, service_time, response_builder):
        self.__action_name = 'ScheduleService'
        self.service_selection = service_selection
        self.service_date = service_date
        self.service_time = service_time
        self.__response_builder = response_builder

        # If we want to use dynamic service list, we can put it in the session attributes
        # of the event and load it here
        self.services = [
            'Radiografias Intra-Bucais.',
            'Radiografias Extra-Bucais.',
            'Tomografia Computadorizada de Feixe Cônico.',
            'Documentação Ortodôntica Digital.',
            'Documentação Padrão Dolphin 2D / 3D.'
        ]

        # TEMPORARY MOCKS. We might load the dates and times from gcalendar once the service is selected
        # and store it into the session attributes of the event
        # self.available_dates = json.parse(event['sessionAttributes'])
        self.available_dates = [
            '10/09/2020',
            '11/09/2020',
            '12/09/2020',
            '13/09/2020',
            '14/09/2020',
            '15/09/2020',
            '16/09/2020',
            '17/09/2020',
        ]

        self.available_times = [
            '10:00 AM',
            '11:00 AM',
            '12:00 AM',
            '01:00 PM',
            '02:00 PM',
            '03:00 PM',
        ]

    def next_step(self):
        validation_result = self.__validate()

        if not validation_result['is_valid']:
            fields = self.__fields_to_object()
            fields[validation_result['invalid_field']] = None
            return self.__response_builder.ask_for_input(
                self.__action_name,
                fields,
                validation_result['invalid_field'],
                validation_result['message']
            )

        if not self.service_selection:
            return self.__response_builder.ask_for_input(
                self.__action_name,
                self.__fields_to_object(),
                'serviceSelection',
                self.__build_services_message()
            )

        if self.service_selection and not self.service_date:
            self.__load_service_dates()
            return self.__response_builder.ask_for_input(
                self.__action_name,
                self.__fields_to_object(),
                'serviceDate',
                self.__build_dates_message()
            )

        if self.service_selection and self.service_date and not self.service_time:
            self.__load_service_times()
            return self.__response_builder.ask_for_input(
                self.__action_name,
                self.__fields_to_object(),
                'serviceTime',
                self.__build_times_message()
            )

    def __load_service_dates(self):
        pass

    def __load_service_times(self):
        pass

    def __fields_to_object(self):
        return {
            'serviceSelection': self.service_selection,
            'serviceDate': self.service_date,
            'serviceTime': self.service_time
        }

    def __validate(self):
        if self.service_selection and not self.__service_selection_is_valid():
            return self.__build_validation_result(
                False,
                'ServiceSelection',
                self.__build_services_message('Não consegui identificar o serviço desejado. Por gentileza, tente novamente.'))

        # REQUIRES THE AVAILABLE DATES TO BE ALREADY REQUESTED FROM G CALENDAR
        # In the ideal flow, it will be request right after the selection of the service
        # so there is no way of having a service_date without having it listed
        if self.service_date and self.available_dates and not self.__service_date_is_valid():
            return self.__build_validation_result(
                False,
                'ServiceDate',
                self.__build_dates_message('Não consegui identificar a data desejada. Por gentileza, tente novamente.')
            )

        if self.service_time and self.available_times and not self.__service_time_is_valid():
            return self.__build_validation_result(
                False,
                'ServiceDate',
                self.__build_times_message('Não consegui identificar o horário desejado. Por gentileza, tente novamente.')
            )
        return self.__build_validation_result(True, None, None)


    def __build_validation_result(self, is_valid, invalid_field_name, message):
        return {'is_valid': is_valid, 'invalid_field': invalid_field_name, 'message': message}

    def __service_time_is_valid(self):
        return self.__option_index_is_valid_and_within_range(self.service_time, len(self.available_times))

    def __service_date_is_valid(self):
        return self.__option_index_is_valid_and_within_range(self.service_date, len(self.available_dates))

    def __service_selection_is_valid(self):
        return self.__option_index_is_valid_and_within_range(self.service_selection, len(self.services))

    def __option_index_is_valid_and_within_range(self, option_text, list_size):
        if not len(option_text.split()) == 2:
            return False
        index = int(option_text.split()[1])
        return index and (index > 0 and index <= list_size)

    def __build_times_message(self, text_to_append_before=''):
        return f"""
{text_to_append_before}
Estas são os horários disponíveis para {self.services[self.service_selection - 1]} no dia {self.available_dates[self.service_date]}.
Digite 'Opção' seguido pela número da opção. Exemplo: 'Opção 1'.

        """.join([f"""
        {index + 1} - {time}
        """ for index, time in enumerate(self.available_times)])

    def __build_dates_message(self, text_to_append_before=''):
        return f"""
{text_to_append_before}
Estas são as datas disponíveis para {self.services[self.service_selection - 1]}.
Digite 'Opção' seguido pela número da opção. Exemplo: 'Opção 1'.

        """.join([f"""
        {index + 1} - {date}
        """ for index, date in enumerate(self.available_dates)])


    def __build_services_message(self, text_to_append_before=''):
        return f"""
{text_to_append_before}
Este são os serviços disponíveis para agendamento.
Digite 'Opção' seguido pelo número da opção. Exemplo: 'Opção 1'.

        """ + str().join([f"""
        {index + 1} - {service}
        """ for index, service in enumerate(self.services)])
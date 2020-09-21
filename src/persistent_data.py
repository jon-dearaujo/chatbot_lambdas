import json


class PersistentData:
    'A data bag to send data that is supposed to be persistent between requests (session data).'

    def __init__(self):
        self.__data = {}

    def data(self):
        return {k: json.dumps(v) for k, v in self.__data.copy().items()}

    def set(self, key, value):
        self.__data[key] = value

    def get(self, key):
        return self.__data.get(key, None)

    @staticmethod
    def load(raw_data: dict) -> 'PersistentData':
        'Load data containing json attributes'
        persistent_data = PersistentData()
        for k, v in raw_data.items() if raw_data else {}.items():
            persistent_data.set(k, json.loads(v))
        return persistent_data

    @staticmethod
    def dump(data: dict) -> 'PersistentData':
        ''
        persistent_data = PersistentData()
        for k, v in data.items() if data else {}.items():
            persistent_data.set(k, v)
        return persistent_data


'''
    create a persistent_data from real data
    parse the persistent_data into an object {'label': 'dumped-json'}
    parse back an object {'label': 'dumped-json'} into the real data
'''

import json
import unittest
from src.persistent_data import PersistentData


class TestPersistentData(unittest.TestCase):

    def setUp(self):
        self.pd = PersistentData()

    def test_is_possible_to_load_data_whose_attributes_are_json(self):
        attr = {'a': 1, 'b': 2}
        raw_data = {'data': json.dumps(attr)}

        persistent_data = PersistentData.load(raw_data)

        returned_inner_data = persistent_data.get('data')

        self.assertEqual(1, returned_inner_data.get('a'))
        self.assertEqual(2, returned_inner_data.get('b'))

    def test_is_possible_to_dump_data_whose_attributes_are_objects(self):
        attr = {'a': 1, 'b': 2}
        raw_data = {'data': attr}

        persistent_data = PersistentData.dump(raw_data)
        # import pdb
        # pdb. set_trace()

        returned_inner_data = persistent_data.get('data')

        self.assertEqual(1, returned_inner_data.get('a'))
        self.assertEqual(2, returned_inner_data.get('b'))

    def test_is_possible_to_get_parsed_data_with_attributes_as_json(self):
        attr = {'a': 1, 'b': 2}
        raw_data = {'data': attr}
        persistent_data = PersistentData.dump(raw_data)

        self.assertEqual(
            {'data': json.dumps(attr)},
            persistent_data.data())

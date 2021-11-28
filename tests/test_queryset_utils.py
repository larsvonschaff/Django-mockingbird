from djangomockingbird.queryset_utils import annotate_mock_class, make_mock_list_from_args, get_keys_from_dict, make_mock_in_bulk_dict, make_mock_aggregate_dict, annotate_return_value
from unittest.mock import MagicMock
import unittest

class TestAnnotateMockClass(unittest.TestCase):

    def test_annotate_mock_class(self):
        mock_model = MagicMock()
        kwargs = {'test':'test'}
        mock_class = annotate_mock_class(kwargs, mock_model)
        self.assertTrue(hasattr(mock_class, 'test'))
        self.assertEqual(mock_class.test, 'test')

class TestMakeMockListFromArgs(unittest.TestCase):

    def test_make_mock_list_from_args(self):
        args = ['test', 'test2']
        mock_values_list = make_mock_list_from_args(args)
        self.assertEqual(mock_values_list, [1, 1])

    def test_make_mock_list_from_args_empty_args(self):
        args = []
        mock_values_list = make_mock_list_from_args(args)
        self.assertEqual(mock_values_list, [1])

class TestGetKeysFromDict(unittest.TestCase):

    def test_get_keys_from_dict(self):
        test_dict = {'key1': 1, 'key2': 2}
        keys_list = get_keys_from_dict(test_dict)
        self.assertEqual(keys_list, ['key1', 'key2'])


class TestMakeMockInBulkDict(unittest.TestCase):

    def test_make_mock_in_bulk_dict(self):
        args = ['test']
        mock_in_bulk_dict = make_mock_in_bulk_dict(args)
        self.assertEqual(mock_in_bulk_dict, {'test': ' '})

    def test_make_mock_in_bulk_dict_empty_args(self):
        args = []
        mock_in_bulk_dict = make_mock_in_bulk_dict(args)
        self.assertEqual(mock_in_bulk_dict, {'1': ' '})


class TestMakeMockAnnotateDict(unittest.TestCase):

    def test_make_mock_aggregate_dict(self):  
        kwargs = {'test': 'test'}
        mock_aggregate_dict = make_mock_aggregate_dict(kwargs)
        self.assertEqual(mock_aggregate_dict, {'test': 'test'} )


class TestAnnotateReturnValue(unittest.TestCase):

    def test_annotate_return_value(self):
        kwargs = {'test':'test'}
        return_value = {'original_key':'original_value'}
        new_return_value = annotate_return_value(kwargs, return_value)
        self.assertEqual(new_return_value, {'original_key': ' ', 'test': ' '})






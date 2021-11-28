import unittest
from djangomockingbird import utils
from unittest.mock import MagicMock



#setup some objects that mimic the behaviour of actual objects for testing purposes. these are used where using MagicMock would be too convoluted.

class MockClass(object):
    pass

class ManagerClass(object):
    pass

class MockField(object):

    auto_created = True
    concrete = False
    one_to_one = False
    related_name = 'test'
    one_to_many = True
    many_to_many = True
    test_field = ' '

    def ___repr___(self):
        return 'field'
    
    def __str__(self):
        return 'field'


class MockField2(object):
    name = 'test'
    test = ' '
    concrete = True

      



class TestMakeSpecDict(unittest.TestCase):

    def test_make_spec_dict(self):
        model_name = 'Test model'
        model_fields = [MockField2()]
        spec_dict = utils.make_spec_dict(model_fields, model_name, specs={'test' : 'test'})
        self.assertEqual(type(spec_dict), dict)
        self.assertEqual(spec_dict['id'], " ")
        self.assertEqual(spec_dict['pk'], 1)
        self.assertEqual(spec_dict['test'], 'test')

    def test_nonexistant_field(self):
        model_name = 'Test model'
        specs = {'something': 'something'}
        fields = [MockField2()]
        self.assertRaises(Exception, utils.make_spec_dict, fields, model_name, specs )



class TestGetCustomMethods(unittest.TestCase):

    def test_get_custom_methods(self):
        model_name = MagicMock()
        custom_methods = utils.get_custom_methods(model_name)
        self.assertEqual(type(custom_methods), list)


class TestCreateFunction(unittest.TestCase):

    def test_create_function(self):
        function = utils.create_function('test_function', 1, None )
        self.assertTrue(type(function(1)), None)


class TestGetModelManager(unittest.TestCase):

    def test_get_model_manager(self):
        model_name = MagicMock()
        model_manager = utils.get_model_manager(model_name)
        self.assertTrue(type(model_manager), str)


class TestSetBackwardsManager(unittest.TestCase):

    def test_set_backwards_manager(self):
        model_fields = [MockField()]
        mock_class = utils.set_backwards_managers(model_fields, MockClass, ManagerClass)
        self.assertTrue(hasattr(mock_class, 'test'))
        self.assertTrue(isinstance(mock_class.test, type))


class TestSetForwardsManager(unittest.TestCase):

    def test_set_forwards_manager(self):
        model_fields = [MockField()]
        mock_class = utils.set_forwards_managers(model_fields, MockClass, ManagerClass)
        self.assertTrue(hasattr(mock_class, 'field'))
        self.assertTrue(isinstance(mock_class.field, type))
















import unittest
from djangomockingbird import decorator_utils


class TestDecoratorUtils(unittest.TestCase):
    def test_resolve_input_path(self):
        test_input_path = 'test_app.test_module.test_file.TestModel'
        module, model_name = decorator_utils.resolve_input_path(test_input_path)
        self.assertEqual(module, 'test_app.test_module.test_file')
        self.assertEqual(model_name, 'TestModel')

    def build_file_path(self):
        test_module = 'test_app.test_module.test_file'
        final_path = decorator_utils.build_file_path(test_module)
        self.assertEqual(final_path, 'test_app/test_module/test_file.py')

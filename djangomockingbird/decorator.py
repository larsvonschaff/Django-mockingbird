from unittest.mock import patch
from djangomockingbird import make_mocks
from os import path
from djangomockingbird import decorator_utils


def mock_model(string_path, specs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            module, model_name = decorator_utils.resolve_input_path(string_path)
            final_path = decorator_utils.build_file_path(module)
            if not path.exists(final_path):
                raise Exception('Invalid input path. Please specify a correct path to the model you would like to mock!')
            importlib = __import__('importlib')
            blogposts = importlib.import_module(module)
            blog_post = getattr(blogposts, model_name)
            mock_model = make_mocks.make_mocks(blog_post, specs=specs)
            setattr(blogposts, model_name, mock_model)
            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorator
    

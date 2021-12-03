from unittest.mock import patch
from djangomockingbird.make_mocks import make_mocks

def mock_model(path, specs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            model_name, module = resolve_path(path)
            importlib = __import__('importlib')
            blogposts = importlib.import_module(module)
            blog_post = getattr(blogposts, model_name)
            mock_model = make_mocks(blog_post, specs=specs)
            setattr(blogposts, model_name, mock_model)
            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorator


#TODO: terrible. need to refactor -  minimize state.
def resolve_path(path):
    importlib = __import__('importlib')
    parts = path.split('.')
    parts.reverse()
    model_name = parts[0]
    parts.remove(model_name)
    parts.reverse()
    module = '.'.join(parts)
    return model_name, module


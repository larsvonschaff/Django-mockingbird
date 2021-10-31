import types
from typing import Any, Dict, List, Callable, Union


# construct a dict from the model
def make_spec_dict(model_fields: List[Any], model_name: Any, specs: Union[None, Dict] = None) -> Dict[Any, Any]:
    fields = [field.name for field in model_fields if field.concrete]
    model_dict = {field: ' ' for field in fields}

    if specs:
        for k, v in specs.items():
            if k not in fields:
                # if the user has specified an invalid field, raise exception
                raise Exception(
                    'The model {} does not have a {} field'.format(model_name, k))

        model_dict.update(specs)

    model_dict['id'] = " "
    model_dict['pk'] = 1    # type: ignore

    return model_dict


# get all methods of a model which are custom/user defined/not inherited.
def get_custom_methods(model_name: Any) -> List[Any]:
    custom_methods = []
    for name, item in model_name.__dict__.items():
        if isinstance(item, types.FunctionType):
            custom_methods.append(name)

    return custom_methods


# function for creating functions with dynamic names and return values. used for mocking custom model methods.
def create_function(name: str, arg: Any, return_value: Any) -> Callable:
    def inner(arg):
        return return_value
    inner.__name__ = name
    return inner


def get_model_manager(model_name: Any) -> str:
    manager_name = str(model_name._meta.default_manager)
    manager_name.split('.')

    return (manager_name.split('.'))[2]


def set_backwards_managers(model_fields: List[Any], mock_class: object, manager: object) -> object:
    #get all reverse relations
    reverse_relation_fields = [
        field for field in model_fields if field.auto_created and not field.concrete and not field.one_to_one]

    for field in reverse_relation_fields:
        manager_name = str(field.related_name) if field.related_name else str(field.name) + '_set'
        if field.one_to_many or field.many_to_many:
            setattr(mock_class, manager_name, manager)

    return mock_class        


def set_forwards_managers(model_fields: List[Any], mock_class: object, manager: object) -> object:

    for field in model_fields:
        if field.many_to_many:
            setattr(mock_class, str(field), manager)

    return mock_class    
